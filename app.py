from flask import Flask, render_template, request
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = "sk-proj-LBBNz8QaZKjVvsncB380T3BlbkFJxQPBjZ2uvZs5iFAlR6dC"

# 구글 시트 연동 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1K4ts2bZ-96u315XDtIfoZF72N4CZ_5pWG3HO6-K7wko/edit?gid=0#gid=0").sheet1

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        if "시험자료" in question:
            answer = "https://naver.me/FW6MU4wD 이수하시는 과목명에 맞춰 다운로드 해주세요"
        elif "학사일정" in question:
            answer = "학사일정 관련 문의는 담당자를 통해 질문 남겨주시면 그에 맞춰 신속한 답변 받아보실 수 있으실거에요 ^^ 화이팅입니다!"
        else:
            answer = "담당자를 통해 질문 남겨주시면 그에 맞춰 확인되는대로 신속한 답변 받아보실 수 있으실거에요 ^^ 화이팅입니다!"
    return render_template("chat.html", answer=answer)

if __name__ != "__main__":
    gunicorn_app = app