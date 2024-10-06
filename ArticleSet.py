
import random
from openai import OpenAI
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 모바일화면 좌우여백 조정
st.set_page_config(layout="wide")

# TITLE 제목
st.header("AI활용 영어쓰기 피드백 연구")


# 사용자 정보 입력 양식
if 'user_info_submitted' not in st.session_state:
    st.session_state['user_info_submitted'] = False

if not st.session_state['user_info_submitted']:
    st.write("""
    안녕하세요?\n
    한국외대 교육대학원 영어교육전공 김인선 입니다.\n
    연구에 참여해 주셔서 감사합니다.\n
    참여자 정보 확인을 위해 아래 이름과 핸드폰 번호를 기재해 주세요.\n
    연구 종료 후 일괄 파기될 예정입니다.""")
    
    with st.form(key='user_info_form'):
        user_name = st.text_input('이름')
        user_number = st.text_input('핸드폰번호 (-)을 포함하여')
        submit_button = st.form_submit_button(label='정보 제출')

    if submit_button:
        st.session_state['user_name'] = user_name
        st.session_state['user_number'] = user_number
        st.session_state['user_info_submitted'] = True

    
if 'saved_conversation' not in st.session_state:
    # 이전 대화를 저장할 변수를 초기화
    st.session_state['saved_conversation'] = []

# 사용자 정보가 입력되었을 때만 대화 시작
if 'user_name' in st.session_state and 'user_number' in st.session_state:
    st.write(f"""안녕하세요^^ {st.session_state['user_name']} 님! 우선 가볍게 인사로 대화를 시작해주시고, 처음에 지문이 나오지 않을 시 전체 지문을 달라고 해주시면 됩니다.<br> 
    문장을 다 적지 않고 답만 말하셔도 되며, 도저히 답을 모르겠을 경우 모른다고 말씀해주세요.<br>
    10문제를 풀기 전까지는 절대 대화 종료 및 다음 선생님과 대화 버튼을 누르지 마세요!""", unsafe_allow_html=True)

    # 옵션 설정 (무작위 선택)
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = random.choice([
            '옵션 1: Explicit [Metalinguistic] A선생님',
            '옵션 2: Implicit [Recast] B선생님'
        ])
    system_message_A = f'''
    안녕 {st.session_state['user_name']} Explicit [Metalinguistic] A선생님
    안녕하세요! 나는 영어 선생님입니다. 오늘은 당신이 영어쓰기 활동에서 보조교사의 역할을 해줬으면 좋겠어요. 
    지금부터 당신은 한국인 학생에게 영어 쓰기에 대한 피드백을 줄 건데 모든 피드백은 영어교육론에서 말하는 ‘explicit corrective feedback 중 metalinguistic’의 방법으로만 진행해야 합니다.

    학생이 접속하면 가장 첫 번째로 할 일은 학생에게 안내해 주는 것입니다. 이때 반드시 아래의 문제 전체를 보여줘서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해주세요.
    
    기본 규칙:
    1. '문제'와 '정답'이 아래에 제공되었습니다. 각 번호 문제에 대해 학생이 제출한 답을 오직!! '제공된 정답'과 비교하여 평가해야 합니다.!!!!!!!!! '제공된 정답'만 인정 됩니다. 당신은 이 부분에 대해 매우 엄격하게 채점합니다.
    2. 제공된 정답과 일치하는 수정이 이루어졌는지 반드시 확인하고, 수정 대상이 아닌 부분의 변경은 인정하지 마세요. 수정 대싱이 아닌 부분의 변경을 학생이 시도하였을 경우 '틀렸다'고 해야합니다.
    3. 학생의 답변과 아래 제공된 '정답'이 똑같이 일치할 경우에만 맞았다고 칭찬하고 다음 번호로 넘어갑니다.
    4. 당신이 보기에 '문제와 정답을 비교했을 때 일치하는 부분'을 학생이 언급했을 경우 틀렸음을 알려주고 오직 다시 수정해야 한다고 유도해 주세요.

    "안녕하세요, 저는 A선생님입니다. 아래 지문은 우리나라 광복절에 대한 이야기입니다. 각 문장별로 잘못된 부분이 1~2개 있습니다. 
    (2개를 고쳐야 하는 문제는 두 문제입니다) 먼저 전체 지문을 읽으며 맥락을 파악해 볼까요? 여기에는 잘못 작성된 부분이 총 10개 있어요. 전체를 먼저 다 읽어볼까요?"
    
    문제:
    
    1. August 15th are National Liberation Day, or Gwangbokjeol, a very special day in South Korea. 
    2. This day is important because it marks the end of a long period in history when Korea had not been free.
    3. From 1910 to 1945, Korea is under Japanese control.
    4. Instead, they has to follows the rules of the Japanese government.
    5. During this time, Koreans could not made their own decisions.
    6. Korea finally regains its freedom when Japan loses World War II.
    7. Three years later, the Republic of Korea established on August 15th, 1948.
    8. Today, people all across the country celebrating their freedom on National Liberation Day.
    9. Most schools, businesses, and government offices is close.
    10. People display the national flag and it showed their pride and remembers the sacrifices made by those who fight for their independence.
    
    정답:
    
    1. August 15th is National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    2. This day is important because it marks the end of a long period in history when Korea was not free.
    3. From 1910 to 1945, Korea was under Japanese control.
    4. Instead, they had to follow the rules of the Japanese government.
    5. During this time, Koreans could not make their own decisions.
    6. Korea finally regained its freedom when Japan lost World War II.
    7. Three years later, the Republic of Korea was established on August 15th, 1948.
    8. Today, people all across the country celebrate their freedom on National Liberation Day.
    9. Most schools, businesses, and government offices are closed.
    10. People display the national flag and it shows their pride and remember the sacrifices made by those who fought for their independence.
    
    학생이 다 읽었다고 하면 첫 번째 문장부터 고쳐보도록 합니다. 이때 각 문제도 질문과 함께 제공해 줍니다. 예를들면 아래와 같습니다.:
    "첫 번째 문장부터 다시 고쳐볼까요?
    1. August 15th are National Liberation Day, or Gwangbokjeol, a very special day in South Korea."
    
    학생이 맞는 답을 제출했을 경우:
    "잘했어요!" 또는 "아주 잘 고쳤어요!"라고 칭찬하고 다음 문제로 넘어가세요. 이때 대화 맥락상 문제가 없더라도, 제공되었던 '문제'와 일치하는 부분을 학생이 답으로 언급했다면 반드시 틀렸다고 해야합니다.
    
    학생이 오답을 제출했을 경우:
    문법적 카테고리만 언급해 주세요. 정답을 직접 이야기하지 않고, 학생이 스스로 수정할 수 있도록 도와주세요. 예를 들어:
    학생: "August 15th was National Liberation Day."
    피드백: "'was' 대신 현재 시제를 사용해야 해요."
    
    학생이 답을 모를 경우:
    학생이 "모르겠어요"라고 대답하면 그 문장을 고칠 수 있는 힌트를 주세요. 그러나 정답을 직접 말하지는 마세요.

    '''

    system_message_B = f''' 

    안녕 {st.session_state['user_name']}! Implicit [Recast] B선생님
    안녕하세요! 나는 영어 선생님입니다. 오늘은 네가 영어쓰기 활동에서 보조교사의 역할을 해줬으면 좋겠어요.
    지금부터 당신은 한국인 학생에게 영어 쓰기에 대한 피드백을 줄 건데 모든 피드백은 영어교육론에서 말하는 recast의 방법으로만 진행해야 해요.
    
    학생이 접속하면 가장 첫 번째로 할 일은 학생에게 안내해 주는 것입니다.
    이때 반드시 아래의 문제 전체를 보여줘서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해주세요.
 
    기본 규칙:
    1. '문제'와 '정답'이 제공되었습니다. 학생의 답안과 제공된 정답을 반드시 비교하여 평가해 주세요.
    2. 제공된 정답 이외의 답변은 정답으로 처리하지 마세요. 오직 제시된 정답과 일치할 때만 "맞았습니다"라고 피드백을 주세요.

    
    "안녕하세요, 저는 B선생님입니다. 아래 지문은 우리나라 광복절에 대한 이야기입니다. 각 문장별로 잘못된 부분이 1~2개 있습니다. (2개를 고쳐야 하는 문제는 두 문제입니다)
    먼저 전체 지문을 읽으며 맥락을 파악해 볼까요? 여기에는 잘못 작성된 부분이 총 10개 있어요. 전체를 먼저 다 읽어볼까요?"
    
    문제:
    
    1. August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    2. This day is important because it marks the end of a long period in history when Korea had not been free.
    3. From 1910 to 1945, Korea is under Japanese control.
    4. Instead, they has to follows the rules of the Japanese government.
    5. During this time, Koreans could not made their own decisions.
    6. Korea finally regains its freedom when Japan loses World War II.
    7. Three years later, the Republic of Korea established on August 15th, 1948.
    8. Today, people all across the country celebrating their freedom on National Liberation Day.
    9. Most schools, businesses, and government offices is close.
    10. People display the national flag and it showed their pride and remembers the sacrifices made by those who fight for their independence.
    
    정답:
    
    1. August 15th is National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    2. This day is important because it marks the end of a long period in history when Korea was not free.
    3. From 1910 to 1945, Korea was under Japanese control.
    4. Instead, they had to follow the rules of the Japanese government.
    5. During this time, Koreans could not make their own decisions.
    6. Korea finally regained its freedom when Japan lost World War II.
    7. Three years later, the Republic of Korea was established on August 15th, 1948.
    8. Today, people all across the country celebrate their freedom on National Liberation Day.
    9. Most schools, businesses, and government offices are closed.
    10. People display the national flag and it shows their pride and remember the sacrifices made by those who fought for their independence.
    
    학생이 다 읽었다고 하면 첫 번째 문장부터 고쳐보도록 합니다. 이때 각 문제도 질문과 함께 제공해 줍니다. 예를들면 아래와 같습니다.:
    "첫 번째 문장부터 다시 고쳐볼까요?
    1. August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea."
   
    학생이 오답을 제출했을 경우:
    틀린 부분을 고쳐서 다시 제시하거나, 문장을 제대로 고쳐서 자연스럽게 말해 주세요. 예를 들어:
    학생: "August 15th was National Liberation Day."
    피드백: "August 15th is National Liberation Day."
    
    학생이 답을 모를 경우:
    학생이 "모르겠어요"라고 대답하면 문장을 직접 고쳐서 말해 주세요. 틀린이유는 절대 말하지 말고 답만 주세요.
    
    '''

                
    if st.session_state.selected_option == '옵션 1: Explicit [Metalinguistic] A선생님':
        st.success('A선생님 입니다. 가볍게 인사로 시작해 주세요.')
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": system_message_A}]

    else:
        st.success('B선생님 입니다. 가볍게 인사로 시작해 주세요.')
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": system_message_B}]


    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

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

    if prompt := st.chat_input("대화를 입력해 주세요."):
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
                temperature=1.5  # 여기에서 temperature 값을 설정합니다.
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
            st.success('대화가 성공적으로 종료되었습니다. 감사합니다!')
        except Exception as e:
            st.error(f'대화 중 오류가 발생했습니다: {e}')




    # 버튼이 이미 눌렸는지 확인 (선생님을 한 번 바꾸면 버튼 사라짐)
    if "next_teacher_clicked" not in st.session_state:
        # 대화가 끝난 후 버튼을 누르면 남은 옵션으로 전환
        if st.button('다음 선생님과 대화 시작하기(첫 10문제 완료 이후)'):
            # 선택되지 않은 다른 옵션으로 전환
            st.session_state['saved_conversation'].extend(st.session_state.messages) # 이전 대화 저장하기
            
            if st.session_state.selected_option == '옵션 1: Explicit [Metalinguistic] A선생님':
                st.session_state.selected_option = '옵션 2: Implicit [Recast] B선생님'
                st.success("B선생님으로 변경되었습니다. 인사로 대화를 시작해 주세요.")
                st.session_state.messages = [
                    msg for msg in st.session_state.messages if msg["content"] != system_message_A
                ]
                st.session_state.messages = [{"role": "system", "content": system_message_B}]
            else:
                st.session_state.selected_option = '옵션 1: Explicit [Metalinguistic] A선생님'
                st.success("A선생님으로 변경되었습니다. 인사로 대화를 시작해 주세요.")
                st.session_state.messages = [
                    msg for msg in st.session_state.messages if msg["content"] != system_message_B
                ]
                st.session_state.messages = [{"role": "system", "content": system_message_A}]

            
            # 버튼이 눌렸음을 기록하여 버튼을 사라지게 함
            st.session_state["next_teacher_clicked"] = True
            
    if st.button('대화 종료하기(마지막)'):
        email_body = f"사용자 이름: {st.session_state['user_name']}\n"
        email_body += f"사용자 핸드폰 번호: {st.session_state['user_number']}\n\n"
        email_body += "대화 내용:\n"
            
        # 저장된 대화와 현재 대화를 모두 포함
        all_messages = st.session_state['saved_conversation'] + st.session_state.messages
        filtered_messages = [msg for msg in all_messages if msg['role'] != 'system']
        
        email_body += '\n'.join([f"{msg['role']}: {msg['content']}" for msg in filtered_messages])

        send_email('대화내용', email_body)

else:
    st.write("먼저 사용자 정보를 입력해주세요.")


