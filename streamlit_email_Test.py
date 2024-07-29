from openai import OpenAI
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def change_chatbot_style():
    # Set style of chat input so that it shows up at the bottom of the column
    chat_input_style = """
    <style>
        .stChatInput {
          position: fixed;
          bottom: 3rem;
          width: calc(100% - 2rem);
        }
    </style>
    """
    st.markdown(chat_input_style, unsafe_allow_html=True)

st.title("논문 Survey")
st.write("음식과 관련된 문장을 적어보세요")



# API 클라이언트 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
from_email = st.secrets["EMAIL_ADDRESS"]
from_password = st.secrets["EMAIL_PASSWORD"]
smtp_server = "smtp.naver.com"  # Gmail SMTP 서버 주소
smtp_port = 587  # SMTP 포트

# 옵션 설정 (이전)


# 화면을 두 개의 컬럼으로 나누기
col1, col2 = st.columns([1, 3])


with col1:
    
    option = st.selectbox(
        '시스템 메시지를 선택하세요',
        (
            '옵션 1: [직접-메타]',
            '옵션 4: [간접-비메타]'
        )
    )
    
    # 시스템 메시지 설정
    if option == '옵션 1: [직접-메타]':
        system_message = '''
        안녕! 오늘은 네가 중학교 영어 보조교사의 역할을 해줬으면 좋겠어!
        지금부터 너와 대화할 이준휘 학생은 중학교 2학년 남자 학생이고, 이 학생의 어휘 수준은 'oxford vocabulary test'를 기준으로 B1 수준이야. 총 40문항중 28를 맞힌 수준이지. https://www.oxfordonlineenglish.com/english-level-test/vocabulary 에서 oxford vocabulary test가 무엇인지 확인할 수 있어.
        이 학생은 지금부터 '내가 가장 좋아하는 음식' 에 대해서 영어로 한 문장씩 작성하기 시작할거야. 그러면 너는 반드시 1. 틀린 부분을 정확히 짚어서 올바른 답을 표시해주고 2. 이것이 어떤 문법적인 부분에서 틀렸는지 알려줘.
        예를들어 I liked kimbab everyday라고 한다면 I like kimbab everyday (시제오류) 라고 작성해주고, '과거시제가 아니라 현재시제를 써야합니다'하고 알려주는 식이야. 알려준 뒤에는 학생이 다음 문장을 쓸 수 있도록 질문해줘.
        글의 내용적인 피드백이나 어휘의 어색함은 지적하지 말아줘. 틀린 스펠링은 지적해주고!
        모든 대화는 한국어로 해주고
        이 학생이 이 활동 이외에 관련없는 질문을 하면 '수업과 관련이 없다는 점'을 짚어주면서 활동을 이어 나갈수 있게 해줘.
        어린 학생인 만큼 친절하고 격려하는 다정한 선생님의 말투로 부탁할게!
        그럼 지금부터 이 학생과 대화를 시작해보자.
        '''
    
    else:
        system_message = '''
        안녕! 오늘은 네가 중학교 영어 보조교사의 역할을 해줬으면 좋겠어!
        지금부터 너와 대화할 이준휘 학생은 중학교 2학년 남자 학생이고, 이 학생의 어휘 수준은 'oxford vocabulary test'를 기준으로 B1 수준이야. 총 40문항중 28를 맞힌 수준이지. https://www.oxfordonlineenglish.com/english-level-test/vocabulary 에서 oxford vocabulary test가 무엇인지 확인할 수 있어.
        이 학생은 지금부터 '내가 가장 좋아하는 음식' 에 대해서 영어로 한 문장씩 작성하기 시작할거야. 그러면 너는 반드시 1. 어디가 틀렸는지 틀린 단어, 혹은 단어들’만’ 짚어줘 2. 그 외에는 어떤 피드백도 주지마. 이 부분은 모든 대답에서 일관되게 적용되어야 해.
        예를들어 I liked kimbab everyday라고 한다면 “‘liked’가 틀렸네요”라고 말하거나. 혹은 liked에 취소선을 그어만 주는 식이야. 학생이 딱 한번은 고쳐서 쓰게끔 ‘한번 고쳐볼래요?’라고 제안해줘.
        그래서 학생이 고쳐서 대답을 한다면 맞았을 경우 맞았다고 칭찬을, 틀렸을 경우 다음기회에 더 알아보자고 하며 다음 문장을 써달라고 유도해줘.
        글의 내용적인 피드백이나 어휘의 어색함은 지적하지 말아줘. 틀린 스펠링은 지적해주고!
        모든 대화는 한국어로 해주고
        이 학생이 이 활동 이외에 관련없는 질문을 하면 '수업과 관련이 없다는 점'을 짚어주면서 활동을 이어 나갈수 있게 해줘.
        어린 학생인 만큼 친절하고 격려하는 다정한 선생님의 말투로 부탁할게!
        그럼 지금부터 이 학생과 대화를 시작해보자.
        '''
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_message}]
    
    # 옵션이 변경되었을 때 메시지 추가
    if "selected_option" not in st.session_state or st.session_state.selected_option != option:
        st.session_state.selected_option = option
        st.session_state.messages.append({"role": "system", "content": f"{option}"})
    
with col2:
    
    if st.button('대화내용 이메일로 보내기'):
        email_body = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        send_email('대화내용', email_body)


with col2:
    # 채팅 메시지 표시
    chat_container = st.container()
    with chat_container:
        for idx, message in enumerate(st.session_state.messages):
            if idx > 0:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # 메시지 입력 창이 화면 맨 아래에 고정되도록 설정
    change_chatbot_style()
    if prompt := st.chat_input("메시지를 입력하세요..."):
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
