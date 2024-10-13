# 1.필요한 라이브러리 호출
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import re

# 2.웹 탭 타이틀 및 아이콘 설정
st.set_page_config(
    page_title = "Naver News",      # 웹탭의 타이틀
    page_icon = ":newspaper:",      # 웹팁의 아이콘(이모지)
    layout = "centered")            # 웹페이지의 Layout : 가운데 디스플레이

# 3.페이지 타이틀 및 서브 타이틀
st.title("네이버 뉴스 크롤링")      # 웹페이지의 타이틀
st.header("실시간 뉴스 Headline 살펴보기") # 웹페이지의 헤더
now = datetime.datetime.now().strftime("%y/%m/%d %H:%M") # 현재 날짜와 시각
st.subheader("날짜:{}".format(now)) # 웹페이지 서브헤더에 날짜와 시각 출력하기
st.markdown("---")                  # 경계선 생성

# 4.뉴스 기사 크롤링 함수
def naver_news(pages=3):  # pages 인자를 통해 몇 페이지를 크롤링할지 결정
    news_titles_links_comments = []  # 뉴스 제목, 링크, 댓글 수를 저장할 리스트 (튜플 형태로)

    # 여러 페이지 크롤링
    for page in range(1, pages+1):  # 원하는 페이지 수만큼 반복
        now = datetime.datetime.now()   # 현재 날짜와 시각 객체 now 생성
        date = now.strftime("%Y%m%d")   # 날짜와 시각 형식을 "년/월/일"로 전환
        ## 뉴스 크롤링하려는 사이트 주소를 url에 입력, 페이지 번호 추가
        url = f"https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=title&date={date}&page={page}"
        ## 크롤링 대상 사이트에서 일정한 형식으로 크롤링을 위해 user-agent 생성
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        response = requests.get(url, headers=headers)  # url에 웹페이지 code를 요청
        html = response.text  # 웹페이지 code 중에서 텍스트만 선별
        soup = BeautifulSoup(html, "html.parser")  # html parser로 html만 soup에 반환

        # 뉴스 제목과 링크 가져오기
        titles = soup.select("#main_content > div.list_body.newsflash_body > ul > li > a")

        for title in titles:  # 각 title에 대해 반복
            news_title = title.text.strip()  # 뉴스 제목
            news_link = title['href']        # 뉴스 링크

            # 뉴스 링크에서 oid와 aid 추출 (정규 표현식 사용)
            oid = re.search(r'oid=(\d+)', news_link).group(1)  # 언론사 ID
            aid = re.search(r'aid=(\d+)', news_link).group(1)  # 기사 ID

            # 네이버 뉴스 댓글 API를 통해 댓글 수 가져오기
            comment_api_url = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=view_politics&pool=cbox5&lang=ko&country=KR&objectId=news{oid},{aid}"
            comment_response = requests.get(comment_api_url, headers=headers)
            comment_data = re.search(r'"commentCount":(\d+)', comment_response.text)  # 댓글 수 추출

            if comment_data:
                comment_count = comment_data.group(1)  # 댓글 수
            else:
                comment_count = "0"  # 댓글이 없으면 0으로 표시

            news_titles_links_comments.append((news_title, news_link, comment_count))  # 제목, 링크, 댓글 수 추가

    # 중복 제거
    news_titles_links_comments = list(dict.fromkeys(news_titles_links_comments))  # 중복 제거

    # 인덱스 리스트 및 뉴스 리스트 생성
    index = []
    titles = []
    links = []
    comments = []

    # 정제된 뉴스와 인덱스 리스트에 저장
    for i, (title, link, comment) in enumerate(news_titles_links_comments):
        index.append(i + 1)  # 인덱스 저장
        titles.append(f"[{title}]({link})")  # 제목과 링크 저장
        comments.append(comment)  # 댓글 수 저장

    # 데이터 프레임 생성
    df = pd.DataFrame({
        "No.": index,
        "Articles": titles,
        "Comments": comments  # 댓글 수 추가
    })

    return df  # 데이터프레임 반환


# 5.Page Layout 설계
col1, col2, col3 = st.columns([2, 6, 2])  # 페이지 Layout을 3개의 Column으로 분할

# 6.col1 설계                       
with col1:                                          
    button1 = st.button(label="뉴스 크롤링",  # button1 생성 : 레이블("뉴스 크롤링")
                        use_container_width=True)
    button2 = st.button(label="뉴스 보기",  # button2 생성 : 레이블("뉴스 보기")
                        use_container_width=True)

# 7.col2 및 col3 설계
with col2:
    if button1:  # button1을 누르면
        df = naver_news()  # naver_news() 함수 실행하여 df를 반환받음
        
    if button2:  # button2를 누르면
        if not df.empty:  # df가 빈 데이터프레임이 아닐 경우에만
            st.dataframe(data=df[['No.', 'Articles']],  # 데이터 프레임 생성
                         use_container_width=True,   # 데이터는 df 사용
                         hide_index=True)  # 폭은 현재 컨테이너 넓이 적용, 인덱스 생략

with col3:
    if button2:  # button2를 누르면
        if not df.empty:  # df가 빈 데이터프레임이 아닐 경우에만
            st.dataframe(data=df[['Comments']],  # 댓글 수만 별도로 표시
                         use_container_width=True,   # 데이터는 df 사용
                         hide_index=True)  # 폭은 현재 컨테이너 넓이 적용, 인덱스 생략
