import openai
import streamlit as st

# App 제목 설정
st.title("친근한 챗봇")

# OpenAI 클라이언트 초기화
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 모델 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# 시스템 메시지
system_message = '''
이건 영어사전 챗봇이야. 영어단어만 입력을 받고 있고, 영어 단어 말고 다른게 입력되면
"영어 단어를 입력해 주세요"라고 답하면 돼.
영어 단어를 입력받으면 아래 내용 순서로 보여줘.

1. 발음기호 
2. 영단어의 뜻을 영어로 해석 (명사, 동사 등 품사도 함께 표시) 
3. 한국어 뜻 (품사별로 나눠서) 
4. 각 뜻에 맞는 예시 문장을 영어로 제시 
5. 그 단어의 어원 
6. 동의어나 반의어를 포함한 관련 단어들 
7. 기억하기 쉽게 연상법
'''

# 메시지 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message}]

# 이전 메시지 표시
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("영어 단어를 입력해 주세요:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API 호출
    with st.chat_message("assistant"):
        try:
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
            )
            assistant_message = response["choices"][0]["message"]["content"]
            st.markdown(assistant_message)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

    # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
