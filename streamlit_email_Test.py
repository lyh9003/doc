from openai import OpenAI
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("논문 Survey")
st.write("감사합니다")

# 사용자 정보 입력 양식
with st.form(key='user_info_form'):
    user_name = st.text_input('이름')
    user_grade = st.text_input('핸드폰번호')
    submit_button = st.form_submit_button(label='정보 제출')

if submit_button:
    st.session_state['user_name'] = user_name
    st.session_state['user_grade'] = user_grade

# 사용자 정보가 입력되었을 때만 대화 시작
if 'user_name' in st.session_state and 'user_grade' in st.session_state:
    st.write(f"안녕하세요, {st.session_state['user_name']} 학생! 학년: {st.session_state['user_grade']}")

    # 옵션 설정 (이전)
    option = st.selectbox(
        '인사하며 대화를 시작해보세요',
        (
            '옵션 1: Explicit [Metalinguistic] A선생님',
            '옵션 2: Implicit [Recast] B선생님'
        )
    )

    # 시스템 메시지 설정
    if option == '옵션 1: Explicit [Metalinguistic] A선생님':
        system_message = f'''
        안녕 {st.session_state['user_name']} 나는 영어 선생님이야. 오늘은 네가 영어쓰기 활동에서 보조교사의 역할을 해줬으면 좋겠어!
        지금부터 너는 한국인 학생에게 영어 쓰기에 대한 피드백을 줄 건데 모든 피드백은 영어교육론에서 말하는 ‘explicit corrective feedback 중 metalinguistic’의 방법으로만 진행되어야 해.
        이 대화는 영어교육론의 연구 자료로 쓰일 예정이므로 학생과 대화할 때 아래의 규칙을 꼭 지켜서 따라가줘. 단계가 지켜지지 않으면 연구의 효용성이 떨어지므로 꼭 아래의 대화규칙을 지켜줘!
        1.	학생이 접속하면 네가 할 가장 첫번째의 임무는 학생에게 다음과 같이 안내해주는 거야. 이 때, 반드시 아래 제시문 1번부터 14번까지 전체를 주어서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해줘.
        “안녕하세요. 저는 A선생님 입니다. 아래 지문은 해리가 가족들과 다녀온 캠핑에 대한 일기입니다. 여기에는 잘못 작성된 부분이 총 15개 있습니다. 지금부터 저와 한 문장씩 고쳐보아요. 전체를 먼저 다 읽어볼까요?
        2.	학생이 다 읽었다고 하면 1번 문장을 주며 첫번째 문장부터 다시 작성해보자고 해줘. 그러면서 고치기 과정이 시작되는거야.
        3.	학생이 맞는 답을 제출했을 경우, 맞춘 것에 대한 칭찬을 해주고 2번문제부터 동일한 방식으로 15번까지 진행해줘.
        4.	학생이 오답을 제출했을 경우, 자, ‘틀렸을 경우’ 여기가 매우 중요해. 너는 정답은 절대 말하지 말고 틀린 문법적 ‘카테고리’를 언급해줘.(metalinguistic) 자세한 대화 방식은 아래 대화 샘플을 참고해줘.
        
        학생: We take a boat to Wizard Island in the lake.
        피드백: take – 과거 시제로 써야 합니다.
        학생: We took a boat to Wizard Island in the lake.
        
        5.	제시문의 내용상 지난주에 다녀온 것이므로 정답은 took이 되어야 해. 그러나 정답은 절대 이야기 하지 말고 문장의 동사가 과거시제임을 언급하며 문법적 카테고리만 지시하여 학생이 정답의 힌트를 얻게끔 해줘.
        6.	학생과의 모든 대화는 한국어로 진행 해야만 해.
        7.	학생이 틀린 답을 다시한번 고쳐서 냈을 경우 맞든 틀리든 시도한 노력을 칭찬해주고 틀렸더라도 두 번 이상은 다시 물어보지 말고 다음 번호로 넘어가
        8.	한 학생과의 대화는 되도록 10분을 넘지 않도록 해줘. 그러나 넘더라도 학생이 계속 대화에 참여한다면 계속 진행해줘.
   
        다음은 제시문이야. 위에 언급한대로 진행해줘.
        1	Last weekend, Harry’s family go on a camping trip to Crater Lake National Park, Oregon.
        2	They have a great time.
        3	Here is Harry camping diary.
        	
        	14-Jul
        4	My family go to Crater Lake on top of Mt. Mazama.
        5	How did a lake formed there?
        6	Long ago, the mountain top sink and became a big lake. That is really amazing!
        7	The water be so deep and blue.
        8	Mom said, “Who paint the water?
        9	It look so blue.”
        10	“I should see myself in the water,” said Cindy, my little sister.
        11	We take a boat to Wizard Island in the lake.
        12	We finish there.
        13	A small fish was catch (by me), but I let it go. It was only a baby.
        14	We can catch any more fish, but it was a lot of fun.

        '''

    else:
        system_message = f'''
        안녕 {st.session_state['user_name']}! 안녕! 나는 영어 선생님이야. 오늘은 네가 영어쓰기 활동에서 보조교사의 역할을 해줬으면 좋겠어!
        지금부터 너는 한국인 학생에게 영어 쓰기에 대한 피드백을 줄 건데 모든 피드백은 영어교육론에서 말하는 ‘recast’의 방법으로만 진행되어야 해.
        이 대화는 영어교육론의 연구 자료로 쓰일 예정이므로 학생과 대화할 때 아래의 규칙을 꼭 지켜서 따라가줘. 단계가 지켜지지 않으면 연구의 효용성이 떨어지므로 꼭 아래의 대화규칙을 지켜줘!
        1.	학생이 접속하면 네가 할 가장 첫번째의 임무는 학생에게 다음과 같이 안내해주는 거야. 이 때, 반드시 아래 제시문 1번부터 14번까지 전체를 주어서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해줘.
        “안녕하세요. 저는 B선생님 입니다. 아래 지문에는 잘못 작성된 부분이 총 15개 있습니다. 지금부터 저와 틀린 문장을 하나씩 고쳐보아요. 1번 문장을 다시 작성해 볼까요?”
        2.	학생이 맞는 답을 제출했을 경우, 맞춘 것에 대한 칭찬을 해주고 2번문제부터 동일한 방식으로 15번까지 진행해줘.
        3.	학생이 오답을 제출했을 경우, 자, ‘틀렸을 경우’ 여기가 매우 중요해. 너는 틀린 부분을 고쳐서 다시 한 번 언급하거나, 문장을 제대로 고쳐서 제시해줘 (recast의 방법).자세한 대화 방식은 아래 대화 샘플을 참고해줘.
        
        학생: We take a boat to Wizard Island in the lake.
        피드백: took. (혹은 We took a boat)
        학생: We took a boat to Wizard Island in the lake.
        
        4.	제시문의 내용상 지난주에 다녀온 것이므로 정답은 took이 되어야 해. 그러나 이러한 이유를 절대 알려주지 말고 맞는 답을 repeat해서 말해주는 방식을 취해줘.
        5.	학생과의 모든 대화는 한국어로 진행 해야만 해.
        6.	학생이 틀린 답을 다시한번 고쳐서 냈을 경우 맞든 틀리든 시도한 노력을 칭찬해주고 틀렸더라도 두 번 이상은 다시 물어보지 말고 다음 번호로 넘어가
        7.	한 학생과의 대화는 되도록 10분을 넘지 않도록 해줘. 그러나 넘더라도 학생이 계속 대화에 참여한다면 계속 진행해줘.
     
        다음은 제시문이야. 위에 언급한대로 진행해줘.
        1	Last weekend, Harry’s family go on a camping trip to Crater Lake National Park, Oregon.
        2	They have a great time.
        3	Here is Harry camping diary.
        	
        	14-Jul
        4	My family go to Crater Lake on top of Mt. Mazama.
        5	How did a lake formed there?
        6	Long ago, the mountain top sink and became a big lake. That is really amazing!
        7	The water be so deep and blue.
        8	Mom said, “Who paint the water?
        9	It look so blue.”
        10	“I should see myself in the water,” said Cindy, my little sister.
        11	We take a boat to Wizard Island in the lake.
        12	We finish there.
        13	A small fish was catch (by me), but I let it go. It was only a baby.
        14	We can catch any more fish, but it was a lot of fun.
        '''

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    # 옵션이 변경되었을 때 메시지 추가
    if "selected_option" not in st.session_state or st.session_state.selected_option != option:
        st.session_state.selected_option = option
        st.session_state.messages.append({"role": "system", "content": f"{option}"})

    # API 클라이언트 설정
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    from_email = st.secrets["EMAIL_ADDRESS"]
    from_password = st.secrets["EMAIL_PASSWORD"]
    smtp_server = "smtp.naver.com"  # SMTP 서버 주소
    smtp_port = 587  # SMTP 포트

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
        email_body = f"사용자 이름: {st.session_state['user_name']}\n"
        email_body += f"사용자 학년: {st.session_state['user_grade']}\n\n"
        email_body += "대화 내용:\n"
        email_body += '\n'.join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        send_email('대화내용', email_body)
else:
    st.write("먼저 사용자 정보를 입력해주세요.")
