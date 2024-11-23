# 1.필요한 라이브러리 호출
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

# 1. 웹탭 타이틀 및 아이콘 설정
st.set_page_config(
    page_title="Naver News",
    page_icon=":newspaper:",
    layout="centered"
)

# 2. 페이지 타이틀 및 서브 타이틀
st.title("네이버 뉴스 크롤링")
st.header("실시간 뉴스 Headline 살펴보기")
now = datetime.datetime.now().strftime("%y/%m/%d %H:%M")
st.subheader(f"날짜: {now}")
st.markdown("---")

# 3. 데이터프레임 초기화 (세션 상태 유지)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()  # 빈 데이터프레임 생성

# 4. 뉴스 크롤링 함수
def naver_news_with_likes(pages=3):
    news_titles_links_likes = []
    for page in range(1, pages + 1):
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        url = f"https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001&listType=title&date={date}&page={page}"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"뉴스 데이터를 가져오는데 실패했습니다: {e}")
            return pd.DataFrame()
        
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.select("#main_content > div.list_body.newsflash_body > ul > li > a")
        like_counts = soup.select("span.u_likeit_text._count.num")
        if not titles or not like_counts:
            st.warning("뉴스 기사를 찾을 수 없습니다. 다시 시도해 주세요.")
            return pd.DataFrame()
        
        for title, like_count in zip(titles, like_counts):
            title_text = title.text.strip()
            link = title['href']
            likes = like_count.text.strip()
            news_titles_links_likes.append((title_text, link, likes))

    news_titles_links_likes = list(dict.fromkeys(news_titles_links_likes))
    index = []
    news_with_links_and_likes = []
    for i, (title, link, likes) in enumerate(news_titles_links_likes):
        index.append(i + 1)
        news_with_links_and_likes.append(f"[{title}]({link}) (좋아요: {likes})")
    df = pd.DataFrame({"No.": index, "Articles": news_with_links_and_likes})
    return df

# 5. 버튼 레이아웃
col1, col2 = st.columns([2, 8])
with col1:
    button1 = st.button("뉴스 크롤링", use_container_width=True)
    button2 = st.button("뉴스 보기", use_container_width=True)

# 6. 버튼 클릭 동작
if button1:
    st.session_state.df = naver_news_with_likes()
    if not st.session_state.df.empty:
        st.success("뉴스 크롤링 완료!")

if button2:
    if not st.session_state.df.empty:
        for index, row in st.session_state.df.iterrows():
            st.markdown(f"{row['No.']}. {row['Articles']}", unsafe_allow_html=True)
    else:
        st.warning("뉴스 크롤링을 먼저 수행해 주세요.")
