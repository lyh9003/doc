# 필요한 라이브러리 호출
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

# 웹 탭 타이틀 및 아이콘 설정
st.set_page_config(
    page_title="Naver News",
    page_icon=":newspaper:",
    layout="centered"
)

# 페이지 타이틀 및 서브 타이틀
st.title("네이버 뉴스 크롤링")
st.header("실시간 뉴스 Headline 살펴보기")
now = datetime.datetime.now().strftime("%y/%m/%d %H:%M")
st.subheader(f"날짜: {now}")
st.markdown("---")

# 뉴스 크롤링 함수 (제목과 댓글 수 포함)
def naver_news(pages=3):  # pages 인자를 통해 몇 페이지를 크롤링할지 결정
    news_data = []  # 뉴스 제목과 링크, 댓글 수를 저장할 리스트

    for page in range(1, pages + 1):
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        url = f"https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=title&date={date}&page={page}"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # 뉴스 제목, 링크, 댓글 수 가져오기
        articles = soup.select("#main_content > div.list_body.newsflash_body > ul > li > a")
        for article in articles:
            title = article.text.strip()
            link = article['href']

            # 댓글 수 크롤링
            comment_tag = article.find_next("a", class_="media_end_head_cmtcount_button _COMMENT_COUNT_VIEW")
            comment_count = comment_tag.text.strip() if comment_tag else "N/A"

            news_data.append((title, link, comment_count))  # 제목, 링크, 댓글 수 저장

    # 중복 뉴스 제거
    news_data = list(dict.fromkeys(news_data))

    # 데이터 프레임 생성
    df = pd.DataFrame(news_data, columns=["Title", "Link", "Comments"])
    return df

# Page Layout 설계
col1, col2 = st.columns([2, 8])

# col1 설계
with col1:
    button1 = st.button(label="뉴스 크롤링", use_container_width=True)
    button2 = st.button(label="뉴스 보기", use_container_width=True)

# col2 설계
with col2:
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    if button1:
        st.session_state.df = naver_news()

    if button2:
        if not st.session_state.df.empty:
            for index, row in st.session_state.df.iterrows():
                st.markdown(
                    f"{index + 1}. [{row['Title']}]({row['Link']}) - 댓글: {row['Comments']}",
                    unsafe_allow_html=True
                )
        else:
            st.write("뉴스 크롤링을 먼저 수행해 주세요.")
