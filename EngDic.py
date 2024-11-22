from openai import OpenAI
import streamlit as st

st.set_page_config(layout="wide")

# TITLE 제목
st.header("인선쌤 영어사전")

api_key =  st.secrets["OPENAI_API_KEY"]

if api_key:
    client = OpenAI(api_key=api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    system_message = '''
    이건 영어사전 챗봇이야. 영어만 입력을 받고 있고, 영어 말고 다른게 입력되면
    "영어 단어를 입력해 주세요"라고 답하면 돼.
    영어 단어를 입력받으면 아래 내용 순서로 보여줘.
    
    1. 발음기호 : 한국어 발음으로도 같이
    2. 영어 뜻 : 영영사전적 뜻. 품사별로 나눠서
    3. 한국어 뜻 : 영한사전적 뜻. 품사별로 나눠서
    4. 예시 문장 : 3개 문장 제시
    5. 동의어나 반의어를 포함한 관련 단어
    6. 활용 : 해당 단어의 다른 형태(예: 동사의 경우 시제 변형).
    7. 단어의 어원 : 단어의 어원을 설명. 한국어로 번역할 것.
    8. 문화적 맥락 : 필요하면 단어가 특정 문화나 맥락에서 자주 사용되는 방식 설명.
    9. 관련 표현: 이 단어와 함께 자주 사용되는 구나 표현.
    10. 문법 참고사항 : 해당 단어와 관련된 특정 문법 포인트. 예: "동사로 사용될 때 뒤에 반드시 목적어가 따라와야 함."
    11. 파생어 : 해당 단어에서 파생된 다른 단어 목록. 예: "Friend (명사) → Friendly (형용사) → Friendship (명사)."
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
