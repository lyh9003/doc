import streamlit as st
import openai
import os
import re

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다. 환경 변수를 확인해 주세요.")
    st.stop()

# Streamlit 앱 제목
st.title("영어사전 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 영어 단어 여부를 확인하는 함수
def is_english_word(word):
    return re.match(r"^[a-zA-Z]+$", word.strip())

# OpenAI API를 사용하여 영어 단어 정보를 가져오는 함수
def get_word_info(word):
    prompt = f"""
    아래 요구 사항을 충족하는 {word}의 정보를 제공해 주세요:
    1. 발음기호
    2. 영어 뜻 (명사, 동사 등 품사별로 구분)
    3. 한국어 뜻 (품사별로 나눠서)
    4. 각 뜻에 맞는 영어 예문
    5. 어원
    6. 동의어와 반의어를 포함한 관련 단어
    7. 기억하기 쉬운 연상법
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-4"
            messages=[
                {"role": "system", "content": "이것은 영어 단어 정보를 제공하는 사전 챗봇입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("영어 단어를 입력하세요:"):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 입력이 영어 단어인지 확인
    if is_english_word(prompt):
        # OpenAI API를 통한 단어 정보 생성
        word_info = get_word_info(prompt)
        st.session_state.messages.append({"role": "assistant", "content": word_info})
        with st.chat_message("assistant"):
            st.markdown(word_info)
    else:
        # 영어 단어가 아닌 경우 경고 메시지
        warning = "영어 단어를 입력해 주세요."
        st.session_state.messages.append({"role": "assistant", "content": warning})
        with st.chat_message("assistant"):
            st.markdown(warning)
