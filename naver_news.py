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
def naver_news():                   # 함수정의 : 함수명 naver_news
    # part1. 네이버에서 뉴스 기사 스크랩핑
    now = datetime.datetime.now()   # 현재 날짜와 시각 객체 now 생성
    date = now.strftime("%Y%m%d")   # 날짜와 시각 형식을 "년/월/일"로 전환
    ## 뉴스 크롤링하려는 사이트 주소를 url에 입력
    url = "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=title&date={}".format(date)
    ## 크롤링 대상 사이트에서 일정한 형식으로 크롤링을 위해 user-agent생성
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    response = requests.get(url, headers = headers) # url에 웹페이지 code를 요청
    html = response.text                            # 웹페이지 code중에서 텍스트만 선별
    soup = BeautifulSoup(html, "html.parser")       # html parser로 html만 soup에 반환

    ## HTML구조에서 뉴스 기사가 있는 곳까지 경로를 추종하여 a태그 하위의 html을 titles에 반환
    titles = soup.select("#main_content > div.list_body.newsflash_body > ul > li > a")
    news_titles = []                                # 빈 리스트 news_titles생성
    for title in titles:                            # titles에서 title로 구성요소 전달                   
        news_titles.append(title.text)              # title의 텍스텍 요소를 news_titles저장

    # part2.동일한 뉴스 기사 제거 : 뉴스 정제
    news_titles = list(set(news_titles))            # 중복되는 news titles를 제거
    index = []                                      # 빈 리스트 index 생성
    news = []                                       # 빈 리스트 news 생성
    
    # part3.정제된 최종 뉴스와 인덱스 빈 리스트에 저장
    for i, article in enumerate(news_titles):       # news_titles에 구성요소를 aritcle에 전달
        index.append(i+1)                           # 인덱스i는 리스트index에 추가
        news.append(article)                        # 기사article은 리스트 article에 추가
        
    # part4.데이터 프레임 생성
    df = pd.DataFrame({
        "No.":index, "Articles":news})              # 리스트 index와 article로 데이터프레임 생성
    
    return df                                       # 데이터 프레임을 반환


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
    if button1:                                     # button1을 누르면
        df = naver_news()                           # naver_news()함수 실행하여 df를 반환받음
        
    if button2:                                     # button2를 누르면
        st.dataframe(data = df,                     # 데이터 프레임 생성
                     use_container_width = True,    # 데이터는 df를 사용
                     hide_index = True)             # 폭은 현재 컨테이너 넓이 적용, 인덱스는 생략
    
[출처] [파이썬 응용:순한 맛] Streamlit(7):실시간 네이버 뉴스를 제공하는 대시보드(Web App)|작성자 코딩 연금술사
