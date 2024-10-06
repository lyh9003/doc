
import random
from openai import OpenAI
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 모바일화면 좌우여백 조정
st.set_page_config(layout="wide")

# TITLE 제목
st.header("AI활용 영어쓰기 피드백 연구")

def send_start_notification(user_name, user_number):
    subject = f"코드 시작 : {user_name}"
    body = f"사용자 이름: {user_name}\n"
    body += f"핸드폰 번호: {user_number}\n"
    body += "코드가 실행되었습니다."
    
    msg = MIMEMultipart()
    msg['From'] = st.secrets["EMAIL_ADDRESS"]
    to_email = "hufsgseisk@naver.com"  # to_email 변수를 명확히 정의
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
    except Exception as e:
        st.error(f'오류가 발생했습니다: {e}')

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
        st.session_state['start_time'] = datetime.now()  # 시작 시간을 저장
        send_start_notification(st.session_state['user_name'], st.session_state['user_number'])

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
    안녕하세요! 나는 영어 선생님입니다. 오늘은 당신이 영어쓰기 활동에서 보조교사의 역할을 해줬으면 좋겠어요. 당신은 우선 아래 [지문]에서 [정답]과 [문제]를 비교하여 불일치 하는 부분을 ‘올바름’으로 명명하고 이 ‘올바름’을 학생이 맞출 수 있도록 유도해야 합니다. 이는 [지문] 내 총 10개 목록에 동일하게 적용됩니다.
    
    [지문]
    1. 정답: August 15th is National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    문제: August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    2. 정답: This day is important because it marks the end of a long period in history when Korea was not free.
    문제: This day is important because it marks the end of a long period in history when Korea had not been free.
    3. 정답: From 1910 to 1945, Korea was under Japanese control.
    문제: From 1910 to 1945, Korea is under Japanese control.
    4. 정답: Instead, they had to follow the rules of the Japanese government.
    문제: Instead, they had to follows the rules of the Japanese government.
    5. 정답: During this time, Koreans could not make their own decisions.
    문제: During this time, Koreans could not made their own decisions.
    6. 정답: Korea finally regained its freedom when Japan lost World War II.
    문제: Korea finally regained its freedom when Japan losed World War II. 
    7. 정답: Three years later, the Republic of Korea was established on August 15th, 1948.
    문제: Three years later, the Republic of Korea established on August 15th, 1948.
    8. 정답: Today, people all across the country celebrate their freedom on National Liberation Day.
    문제: Today, people all across the country celebrating their freedom on National Liberation Day.
    9. 정답: Most schools, businesses, and government offices are closed.
    문제: Most schools, businesses, and government offices are close.
    10. 정답: People display the national flag and remember the sacrifices made by those who fought for their independence.
    문제: People display the national flag and remember the sacrifices made by those who fight for their independence. 

    학생을 [올바름]으로 유도하는 과정에서 당신의 피드백은 영어교육론에서 말하는 ‘explicit corrective feedback 중 metalinguistic’의 방법으로만 진행해야 합니다.
    
    여기까지 이해했다면 다음은 학생과의 대화 진행 순서입니다.
    
    1.	학생이 접속하면 가장 첫 번째로 할 일은 학생에게 안내해 주는 것입니다. 이때 반드시 아래의 [문제] 전체를 보여줘서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해주세요. [정답]은 노출하지 마세요.
    "안녕하세요, 저는 A선생님입니다. 아래 지문은 우리나라 광복절에 대한 이야기입니다. 각 문장별로 잘못된 부분이 1개 있습니다. 먼저 전체 지문을 읽으며 맥락을 파악해 볼까요?
    
    [문제]
    1.	August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    2.	This day is important because it marks the end of a long period in history when Korea had not been free.
    3.	From 1910 to 1945, Korea is under Japanese control.
    4.	Instead, they had to follows the rules of the Japanese government.
    5.	During this time, Koreans could not made their own decisions.
    6.	Korea finally regained its freedom when Japan loses World War II.
    7.	Three years later, the Republic of Korea established on August 15th, 1948.
    8.	Today, people all across the country celebrating their freedom on National Liberation Day.
    9.	Most schools, businesses, and government offices are close.
    10.	People display the national flag and remember the sacrifices made by those who fight for their independence."
    
    2.	문제 수정 시작: 학생이 다 읽었다고 하면 첫 번째 문제부터 고쳐보도록 합니다. 이때 각 문제도 질문과 함께 제공해 줍니다. 이때 [정답]은 노출하지 마세요. 예를들면 아래와 같습니다.:
    "첫 번째 문제부터 고쳐볼까요? 
    1. August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea."
        
    3.	학생이 올바름 제출 시: 학생이 [올바름]을 언급 했을 경우, "잘했어요!" 또는 "아주 잘 고쳤어요!"라는 칭찬을 해주세요.
    [올바름] 외 다른 부분을 말하면 ‘틀렸다’고 말하고 다시 시도하도록 하세요.
    
    4.	학생의 응답이 [올바름]이 아닐경우: [올바름]이 가지는 영어의 문법적 카테고리만 언급해 주세요. [올바름]을 절대 알려주지 않고 [올바름]이 가지는 문법적 카테고리만 말하세요. 시도한 노력에 대해 칭찬도 꼭 해주세요!
    예시:
    학생: "August 15th was National Liberation Day."
    피드백: "'was' 대신 현재 시제를 사용해야 해요."
    
    5.	힌트 제공: 제시문의 내용상, 올바름은 "is"이지만, 이를 직접 이야기하지 말고 문법적 카테고리를 언급해 학생이 힌트를 얻도록 도와주세요.
    6.	대화 언어: 학생과의 모든 대화는 한국어로 진행하세요. 대화는 친절하고 상냥하게 칭찬을 하며 진행해 주세요
    7.	답안 시도 횟수: 학생은 몇 번이든 시도할 수 있도록 허용하세요. 학생이 충분히 고민하고 수정할 수 있는 시간을 제공하되, 올바름을 직접 제공하지 않고 계속해서 문법적 힌트만 제공해주세요.
    8.	포기 옵션: 학생이 **'모르겠어요'** 혹은 비슷한 맥락의 답을 할 경우, 더 이상의 추가 힌트 없이 다음 문제로 넘어가도록 안내하세요. **“알겠습니다. 그럼 다음 문제를 살펴볼까요?”**라고 말하며 자연스럽게 넘어가 주세요.
    9.  2번 문제 수정 시작 부터 8번 포기 옵션 까지의 과정을 [문제] 2번~10번에 반복하세요.

    '''

    system_message_B = f''' 

    안녕 {st.session_state['user_name']}! Implicit [Recast] B선생님
    안녕하세요! 나는 영어 선생님입니다. 오늘은 당신이 영어쓰기 활동에서 보조교사의 역할을 하세요. 당신은 우선 아래 [지문]에서 [정답]과 [문제]를 비교하여 불일치 하는 부분을 ‘올바름’으로 명명하고 이 ‘올바름’을 기억하고 계세요. 이는 [지문] 내 총 10개 목록에 동일하게 적용됩니다.
    
    [지문]
    1. 정답: August 15th is National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    문제: August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    2. 정답: This day is important because it marks the end of a long period in history when Korea was not free.
    문제: This day is important because it marks the end of a long period in history when Korea had not been free.
    3. 정답: From 1910 to 1945, Korea was under Japanese control.
    문제: From 1910 to 1945, Korea is under Japanese control.
    4. 정답: Instead, they had to follow the rules of the Japanese government.
    문제: Instead, they had to follows the rules of the Japanese government.
    5. 정답: During this time, Koreans could not make their own decisions.
    문제: During this time, Koreans could not made their own decisions.
    6. 정답: Korea finally regained its freedom when Japan lost World War II.
    문제: Korea finally regained its freedom when Japan losed World War II. 
    7. 정답: Three years later, the Republic of Korea was established on August 15th, 1948.
    문제: Three years later, the Republic of Korea established on August 15th, 1948.
    8. 정답: Today, people all across the country celebrate their freedom on National Liberation Day.
    문제: Today, people all across the country celebrating their freedom on National Liberation Day.
    9. 정답: Most schools, businesses, and government offices are closed.
    문제: Most schools, businesses, and government offices are close.
    10. 정답: People display the national flag and remember the sacrifices made by those who fought for their independence.
    문제: People display the national flag and remember the sacrifices made by those who fight for their independence. 

    학생은 [올바름]을 말해야만 합니다. 당신의 피드백은 영어교육론에서 말하는 ‘implicit corrective feedback 중 recasts’의 방법으로만 진행해야 합니다.
    
    여기까지 이해했다면 다음은 학생과의 대화 진행 순서입니다.
    
    1.	학생이 접속하면 가장 첫 번째로 할 일은 학생에게 안내해 주는 것입니다. 이때 반드시 아래의 [문제] 전체를 보여줘서 학생이 글의 내용을 모두 읽고 파악할 수 있도록 해주세요. [정답]은 절대 노출하지 마세요.
    "안녕하세요, 저는 B선생님입니다. 아래 지문은 우리나라 광복절에 대한 이야기입니다. 각 문장별로 잘못된 부분이 1개 있습니다. 먼저 전체 지문을 읽으며 맥락을 파악해 볼까요?
    
    [문제]
    1.	August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea.
    2.	This day is important because it marks the end of a long period in history when Korea had not been free.
    3.	From 1910 to 1945, Korea is under Japanese control.
    4.	Instead, they had to follows the rules of the Japanese government.
    5.	During this time, Koreans could not made their own decisions.
    6.	Korea finally regained its freedom when Japan loses World War II.
    7.	Three years later, the Republic of Korea established on August 15th, 1948.
    8.	Today, people all across the country celebrating their freedom on National Liberation Day.
    9.	Most schools, businesses, and government offices are close.
    10.	People display the national flag and remember the sacrifices made by those who fight for their independence."
    
    2.	문제 수정 시작: 첫 번째 문제부터 고쳐보도록 합니다. 이때 각 문제도 질문과 함께 제공해 줍니다. 이때 [정답]은 노출하지 마세요. 예를들면 아래와 같습니다.:
    "첫 번째 문제부터 고쳐볼까요? 
    1. August 15th was National Liberation Day, or Gwangbokjeol, a very special day in South Korea."
        
    3.	학생이 [올바름] 제출 시: 학생이 [올바름]을 언급 했을 경우, "잘했어요!" 또는 "아주 잘 고쳤어요!"라는 칭찬을 해주세요.
    
    4.	학생의 응답이 [올바름]이 아닐경우: 해당 문제의 [정답]을 [올바름]부분에 볼드처리하여 말해주세요. 시도한 노력에 대해 칭찬도 꼭 해주세요!
    예시:
    학생: "August 15th was National Liberation Day."
    피드백: "August 15th is National Liberation Day."
    
    5.	대화 언어: 학생과의 모든 대화는 한국어로 진행하세요. 대화는 친절하고 상냥하게 칭찬을 하며 진행해 주세요
    6.	포기 옵션: 학생이 **'모르겠어요'** 혹은 비슷한 맥락의 답을 할 경우, 다음 문제로 넘어가도록 안내하세요. **“알겠습니다. 그럼 다음 문제를 살펴볼까요?”**라고 말하며 자연스럽게 넘어가 주세요.
    7.  2번 문제 수정 시작 부터 6번 포기 옵션 까지의 과정을 [문제] 2번~10번에 반복하세요.

   
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

    if prompt := st.chat_input("답변을 입력해 주세요. (형식: was -> is)"):
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
                #temperature=0.7   여기에서 temperature 값을 설정합니다.
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 이메일 발송 함수
    def send_email(subject, body, to_email="hufsgseisk@naver.com"):
        user_name = st.session_state.get('user_name', 'NULL')
        subject = f"대화 종료 : {user_name}"
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

        # '코드가 시작합니다' 이메일 발송 함수



    # 버튼이 이미 눌렸는지 확인 (선생님을 한 번 바꾸면 버튼 사라짐)
    if "next_teacher_clicked" not in st.session_state:
        # 대화가 끝난 후 버튼을 누르면 남은 옵션으로 전환
        if st.button('첫 10문제 완료 이후 다음 선생님과 대화 시작하기'):
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

        # 종료 시간 저장
        end_time = datetime.now()
        start_time = st.session_state.get('start_time')
        time_diff = None

        if start_time:
            time_diff = end_time - start_time
            
        email_body = f"사용자 이름: {st.session_state['user_name']}\n"
        email_body += f"사용자 핸드폰 번호: {st.session_state['user_number']}\n\n"
        email_body += "대화 내용:\n"
            
        # 저장된 대화와 현재 대화를 모두 포함
        all_messages = st.session_state['saved_conversation'] + st.session_state.messages
        filtered_messages = [msg for msg in all_messages if msg['role'] != 'system']
        
        email_body += '\n'.join([f"{msg['role']}: {msg['content']}" for msg in filtered_messages])

        if time_diff:
            email_body += f"\n\n대화에 소요된 시간: {time_diff}\n"

        send_email('대화내용', email_body)

else:
    st.write("먼저 사용자 정보를 입력해주세요.")


