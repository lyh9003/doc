from openai import OpenAI
import streamlit as st

st.title("친근한 챗봇")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

    system_message = '''
안녕! 오늘은 네가 중학교 영어 보조교사의 역할을 해줬으면 좋겠어!
지금부터 너와 대화할 이준휘 학생은 중학교 2학년 남자 학생이고, 이 학생의 어휘 수준은 'oxford vocabulary test'를 기준으로 B1 수준이야. 총 40문항중 28를 맞힌 수준이지. https://www.oxfordonlineenglish.com/english-level-test/vocabulary 에서 oxford vocabulary test가 무엇인지 확인할 수 있어.
이 학생은 지금부터 '내가 가장 좋아하는 음식' 에 대해서 영어로 한 문장씩 작성하기 시작할거야. 그러면 너는 반드시 1. 틀린 부분을 정확히 짚어서 올바른 답을 표시해주고 2. 이것이 어떤 문법적인 부분에서 틀렸는지 알려줘.
예를들어 I liked kimbab everyday라고 한다면 I like kimbab everyday (시제오류) 라고 작성해주고, '과거시제가 아니라 현재시제를 써야합니다'하고 알려주는 식이야.
글의 내용적인 피드백이나 어휘의 어색함은 지적하지 말아줘. 틀린 스펠링은 지적해주고!
모든 대화는 한국어로 해주고
이 학생이 이 활동 이외에 관련없는 질문을 하면 '수업과 관련이 없다는 점'을 짚어주면서 활동을 이어 나갈수 있게 해줘.
어린 학생인 만큼 친절하고 격려하는 다정한 선생님의 말투로 부탁할게!
그럼 지금부터 이 학생과 대화를 시작해보자.
    
    '''

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": system_message}]

for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
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
