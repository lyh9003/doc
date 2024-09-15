
import random
from openai import OpenAI
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("한국외대 교육대학원 영어교육과 연구참여")
st.write("감사합니다")

# 사용자 정보 입력 양식
with st.form(key='user_info_form'):
    user_name = st.text_input('이름')
    user_number = st.text_input('핸드폰번호 (-)을 포함하여')
    submit_button = st.form_submit_button(label='정보 제출')

if submit_button:
    st.session_state['user_name'] = user_name
    st.session_state['user_number'] = user_number

# 사용자 정보가 입력되었을 때만 대화 시작
if 'user_name' in st.session_state and 'user_number' in st.session_state:
    st.write(f"안녕하세요^^ {st.session_state['user_name']} 님! 우선 가볍게 인사로 대화를 시작해주시고,\n처음에 지문이 나오지 않을 시 전체 지문을 달라고 해주시면 됩니다.")

    # 옵션 설정 (무작위 선택)
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = random.choice([
            '옵션 1: Explicit [Metalinguistic] A선생님',
            '옵션 2: Implicit [Recast] B선생님'
        ])

    system_message_A = f'''
    안녕 {st.session_state['user_name']} Explicit [Metalinguistic] A선생님
    안녕하세요! 나는 영어 선생님입니다. 오늘은 당신이 영어쓰기 활동에서 보조교사의 역할을 해줬으면 좋겠어요.
    지금부터 당신은 한국인 학생에게 영어 쓰기에 대한 피드백을 줄 건데, 모든 피드백은 영어교육론에서 말하는 ‘explicit corrective feedback 중 metalinguistic’의 방법으로만 진행해야 합니다.
    이 대화는 영어교육론의 연구 자료로 쓰일 예정이므로 학생과 대화할 때 아래의 규칙을 꼭 지켜야 해요. 단계가 지켜지지 않으면 연구의 효용성이 떨어지므로 꼭 아래의 대화 규칙을 따라 주세요!
    1.	학생이 접속하면 가장 첫 번째로 할 일은 다음과 같이 학생에게 안내하는 거예요. 이때, 반드시 제시문 전체를 보여줘서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해주세요.
    “안녕하세요, 저는 A선생님입니다. 아래 지문은 해리가 가족들과 다녀온 캠핑에 대한 일기입니다. 여기에는 잘못 작성된 부분이 총 14개 있어요. 전체를 먼저 다 읽어볼까요?”
    2.	학생이 다 읽었다고 하면 1번 문장을 주며, "첫 번째 문장부터 다시 고쳐볼까요?"라고 말하면서 고치는 과정을 시작해주세요.
    3.	학생이 맞는 답을 제출했을 경우, "잘했어요!" 또는 "아주 잘 고쳤어요!"라는 칭찬을 해주고, 2번 문제부터 동일한 방식으로 14번까지 진행하세요.
    4.	학생이 오답을 제출했을 경우, 문법적 카테고리만 언급해 주세요. 정답을 절대 이야기하지 않고, 학생이 스스로 수정할 수 있도록 도와주세요. 예를 들어:
    학생: We take a boat to Wizard Island in the lake.
    피드백: "take – 과거 시제로 써야 합니다."
    5.	제시문의 내용상, 정답은 "took"이지만, 정답을 직접 이야기하지 말고 문법적 카테고리를 언급해 학생이 힌트를 얻도록 도와주세요.
    6.	학생과의 모든 대화는 한국어로 진행하세요.
    7.	학생이 틀린 답을 고쳐서 냈을 경우, 맞든 틀리든 시도한 노력에 대해 칭찬해주고, 두 번 이상은 같은 문장에 대해 다시 묻지 말고 다음 문제로 넘어가 주세요.
    8.	한 학생과의 대화는 되도록 10분을 넘지 않도록 해주세요. 그러나 학생이 적극적으로 참여하는 경우에는 최대 15분까지 진행할 수 있습니다.

   
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

    system_message_B = f'''

    안녕 {st.session_state['user_name']}! Implicit [Recast] B선생님
    안녕하세요! 나는 영어 선생님입니다. 오늘은 네가 영어 쓰기 활동에서 보조교사의 역할을 해줬으면 좋겠어요.
    지금부터 너는 한국인 학생에게 영어 쓰기에 대한 피드백을 줄 건데, 모든 피드백은 영어교육론에서 말하는 recast의 방법으로만 진행해야 해요.
    이 대화는 영어교육론의 연구 자료로 쓰일 예정이므로 학생과 대화할 때 아래의 규칙을 꼭 지켜주세요. 단계가 지켜지지 않으면 연구의 효용성이 떨어지므로 꼭 아래의 대화 규칙을 따라주세요!
    1.	학생이 접속하면 가장 첫 번째로 할 일은 다음과 같이 학생에게 안내하는 거예요. 이때, 반드시 제시문 전체를 보여줘서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해주세요.
    “안녕하세요, 저는 B선생님입니다. 아래 지문은 해리가 가족들과 다녀온 캠핑에 대한 일기입니다. 여기에는 잘못 작성된 부분이 총 14개 있어요. 전체를 먼저 다 읽어볼까요?”
    2.	학생이 다 읽었다고 하면 1번 문장을 주며, "첫 번째 문장부터 다시 고쳐볼까요?"라고 말하면서 고치는 과정을 시작해주세요.
    3.	학생이 맞는 답을 제출했을 경우, "잘했어요!" 또는 "아주 잘 고쳤어요!"라는 칭찬을 해주고, 2번 문제부터 동일한 방식으로 14번까지 진행하세요.
    4.	학생이 오답을 제출했을 경우, 틀린 부분을 고쳐서 다시 제시하거나 문장을 제대로 고쳐서 자연스럽게 넘겨주세요. 예를 들어:
    학생: We take a boat to Wizard Island in the lake.
    피드백: "took." (혹은 "We took a boat to Wizard Island in the lake.")
    5.	제시문의 내용상 지난주에 다녀온 것이므로 정답은 "took"이지만, 이유는 알려주지 않고 틀린 부분을 자연스럽게 고쳐서 말해주는 방식으로 진행하세요.
    6.	학생과의 모든 대화는 한국어로 진행하세요.
    7.	학생이 틀린 답을 고쳐서 냈을 경우, 맞든 틀리든 시도한 노력에 대해 칭찬해주고, 두 번 이상은 같은 문장에 대해 다시 묻지 말고 다음 문제로 넘어가 주세요.
    8.	한 학생과의 대화는 되도록 10분을 넘지 않도록 해주세요. 그러나 학생이 적극적으로 참여하는 경우에는 최대 15분까지 진행할 수 있습니다.

     
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

    if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # 사용자에게 시스템 메시지를 제외하고 나머지 메시지를 표시
    for idx, message in enumerate(st.session_state.messages):
        # 시스템 메시지를 제외하고 사용자와 GPT의 대화만 표시
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    else:
        st.success('B선생님으로 시작하겠습니다.')
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": system_message_B}]        
        

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_message}]
#    else:
#        # 이전 메시지가 유지되도록 새로운 시스템 메시지를 추가
#        st.session_state.messages.append({"role": "system", "content": system_message})

    # API 클라이언트 설정
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

    # 이메일 발송 함수
    def send_email(subject, body, to_email="rollingfac@naver.com"):
        msg = MIMEMultipart()
        msg['From'] = st.secrets["EMAIL_ADDRESS"]
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP("smtp.naver.com", 587)
            server.starttls()
            server.login(st.secrets["EMAIL_ADDRESS"], st.secrets["EMAIL_PASSWORD"])
            text = msg.as_string()
            server.sendmail(st.secrets["EMAIL_ADDRESS"], to_email, text)
            server.quit()
            st.success('이메일이 성공적으로 발송되었습니다!')
        except Exception as e:
            st.error(f'이메일 발송 중 오류가 발생했습니다: {e}')

    if st.button('대화내용 이메일로 보내기'):
        email_body = f"사용자 이름: {st.session_state['user_name']}\n"
        email_body += f"사용자 핸드폰 번호: {st.session_state['user_number']}\n\n"
        email_body += "대화 내용:\n"
        email_body += '\n'.join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        send_email('대화내용', email_body)

    # 버튼이 이미 눌렸는지 확인 (선생님을 한 번 바꾸면 버튼 사라짐)
    if "next_teacher_clicked" not in st.session_state:
        # 대화가 끝난 후 버튼을 누르면 남은 옵션으로 전환
        if st.button('다음 선생님과 대화 시작하기'):
            # 선택되지 않은 다른 옵션으로 전환
            if st.session_state.selected_option == '옵션 1: Explicit [Metalinguistic] A선생님':
                st.session_state.selected_option = '옵션 2: Implicit [Recast] B선생님'
                st.success("B선생님으로 변경되었습니다.")
                st.session_state.messages = [
                    msg for msg in st.session_state.messages if msg["content"] != system_message_A
                ]
                st.session_state.messages.append({"role": "system", "content": system_message_B})
            else:
                st.session_state.selected_option = '옵션 1: Explicit [Metalinguistic] A선생님'
                st.success("A선생님으로 변경되었습니다.")
                st.session_state.messages = [
                    msg for msg in st.session_state.messages if msg["content"] != system_message_B
                ]
                st.session_state.messages.append({"role": "system", "content": system_message_A})

            
            # 버튼이 눌렸음을 기록하여 버튼을 사라지게 함
            st.session_state["next_teacher_clicked"] = True


else:
    st.write("먼저 사용자 정보를 입력해주세요.")



