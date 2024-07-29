import streamlit as st
from datetime import datetime
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정 (자신의 API 키로 변경)
openai.api_key = os.getenv('OPENAI_API_KEY')

# 로그 파일 설정
LOG_FILE = "chat_log.txt"

# 이메일 설정
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP 서버 주소
SMTP_PORT = 587  # SMTP 포트
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # 발신자 이메일 주소
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # 발신자 이메일 비밀번호
RECIPIENT_EMAIL = "rollingfac@gmail.com"  # 수신자 이메일 주소

openai.api_key = "sk-proj-HA4vZtcf9hCXUbAd48FfT3BlbkFJ3xjpJ0SvFzrk210IvZgj"
EMAIL_ADDRESS = "rollngfac@gmail.com"
EMAIL_PASSWORD = "dydgnS1!"


# 로그를 파일에 기록하는 함수
def log_chat(user_input, bot_response):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - User: {user_input}\n")
        log_file.write(f"{datetime.now()} - Bot: {bot_response}\n")

# ChatGPT 응답을 가져오는 함수
def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 또는 'gpt-4' 모델 사용
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

# 이메일을 보내는 함수
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL  # 받는 사람 이메일 주소
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

# Streamlit 애플리케이션
st.title("ChatGPT와의 채팅")
st.write("채팅 내용을 입력하고 엔터 키를 누르세요.")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 사용자 입력
user_input = st.text_input("당신: ", "")

if user_input:
    # ChatGPT 응답 생성
    bot_response = get_chatgpt_response(user_input)
    
    # 채팅 기록에 추가
    st.session_state['chat_history'].append(f"당신: {user_input}")
    st.session_state['chat_history'].append(f"ChatGPT: {bot_response}")
    
    # 로그 기록
    log_chat(user_input, bot_response)

# 채팅 기록 출력
for chat in st.session_state['chat_history']:
    st.write(chat)

# 채팅 기록을 이메일로 보내기 버튼
if st.button('채팅 기록 이메일로 보내기'):
    email_subject = "New Chat with ChatGPT"
    email_body = "\n".join(st.session_state['chat_history'])
    send_email(email_subject, email_body)
    st.success('채팅 기록이 이메일로 전송되었습니다.')
