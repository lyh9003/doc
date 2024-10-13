# 1.필요한 라이브러리 호출
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

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
    news_titles = []  # 뉴스 제목 리스트
    news_links = []   # 뉴스 링크 리스트

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
            news_titles.append(title.text.strip())  # 뉴스 제목을 리스트에 저장
            news_links.append(title['href'])        # 뉴스 링크를 리스트에 저장

    # 중복 제거
    news_titles = list(set(news_titles))  # 중복 뉴스 제목 제거
    news_links = list(set(news_links))    # 중복 뉴스 링크 제거

    index = []  # 인덱스 리스트
    news_with_links = []  # 뉴스 제목과 링크를 합친 리스트

    # 정제된 뉴스와 인덱스 리스트에 저장
    for i, (title, link) in enumerate(zip(news_titles, news_links)):
        index.append(i + 1)  # 인덱스 저장
        news_with_links.append(f"[{title}]({link})")  # 제목에 링크를 추가한 markdown 형식으로 저장

    # 데이터 프레임 생성
    df = pd.DataFrame({
        "No.": index,
        "Articles": news_with_links
    })  # 인덱스와 뉴스 제목 + 링크로 데이터프레임 생성

    return df  # 데이터프레임 반환

# 5.Page Layout설계
col1, col2 = st.columns([2, 8])                     # 페이지 Layout를 2개의 Column으로 분할

# 6.col1 설계                       
with col1:                                          
    button1 = st.button(label = "뉴스 크롤링",      # button1 생성 : 레이블("뉴스 크롤링")
                        use_container_width = True)
    button2 = st.button(label = "뉴스 보기",        # button2 생성 : 레이블("뉴스 보기")
                        use_container_width = True)

# 7.col2 설계
with col2:
    # 빈 데이터프레임 미리 선언 (세션 상태를 사용하여 df 유지)
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()  # 세션 상태에 빈 데이터프레임 저장

    if button1:  # button1을 누르면
        st.session_state.df = naver_news()  # 세션 상태에 df 저장 (크롤링 결과)

    if button2:  # button2를 누르면
        if not st.session_state.df.empty:  # df가 비어있지 않은 경우에만 출력
            for index, row in st.session_state.df.iterrows():  # 각 뉴스 기사에 대해 반복
                st.markdown(f"{row['No.']}. {row['Articles']}", unsafe_allow_html=True)  # 인덱스와 링크 출력
        else:
            st.write("뉴스 크롤링을 먼저 수행해 주세요.")  # df가 비어있을 때 메시지 출력
