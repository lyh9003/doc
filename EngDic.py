from openai import OpenAI
import streamlit as st

st.title("친근한 챗봇")

api_key =  st.secrets["OPENAI_API_KEY"]

if api_key:
    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    for idx, message in enumerate(st.session_state.messages):
        if idx > 0:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("영어 단어를 입력해 주세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("API key가 만료되었습니다.")
