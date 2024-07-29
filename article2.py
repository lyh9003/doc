from openai import OpenAI
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("인선쌤 보조 용구리봇!")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
from_email = st.secrets["EMAIL_ADDRESS"]
from_password = st.secrets["EMAIL_PASSWORD"]
smtp_server = "smtp.naver.com"  # Gmail SMTP 서버 주소
smtp_port = 587  # SMTP 포트

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

    system_message = '''
안녕! 오늘은 네가 중학교 영어 보조교사의 역할을 해줬으면 좋겠어!
지금부터 너와 대화할 이준휘 학생은 중학교 2학년 남자 학생이고, 이 학생의 어휘 수준은 'oxford vocabulary test'를 기준으로 B1 수준이야. 총 40문항중 28를 맞힌 수준이지. https://www.oxfordonlineenglish.com/english-level-test/vocabulary 에서 oxford vocabulary test가 무엇인지 확인할 수 있어.
이 학생은 지금부터 '내가 가장 좋아하는 음식' 에 대해서 영어로 한 문장씩 작성하기 시작할거야. 그러면 너는 반드시 1. 틀린 부분을 절대 짚지 말고 올바른 답도 알려주면 안되고 2. 이것이 어떤 문법적인 부분에서 틀렸는지만 알려줘.
예를들어 I liked kimbab everyday라고 한다면 (시제오류) 라고 작성해주고, ‘동사의 시제가 틀렸어요'하고 알려주는 식이야. 어떻게 고쳐야 할지 정답을 알려주지 않는게 가장 중요한 규칙이야.
그래서 학생이 고쳐서 대답을 한다면 맞았을 경우 맞았다고 칭찬을, 틀렸을 경우 다음기회에 더 알아보자고 하며 다음 문장을 써달라고 유도해줘.
글의 내용적인 피드백이나 어휘의 어색함은 지적하지 말아줘. 틀린 스펠링은 지적해주고!
모든 대화는 한국어로 해주고 문장 마지막엔 ‘한번 고쳐볼래요?’라고 제안해줘.
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


def send_email(subject, body, to_email="rollingfac@naver.com"):


    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        st.success('이메일이 성공적으로 발송되었습니다!')
    except Exception as e:
        st.error(f'이메일 발송 중 오류가 발생했습니다: {e}')

if st.button('대화내용 이메일로 보내기'):
    email_body = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    send_email('대화내용', email_body)


