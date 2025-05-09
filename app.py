
from flask import Flask, render_template, request
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
openai.api_key = "sk-proj-LBBNz8QaZKjVvsncB380T3BlbkFJxQPBjZ2uvZs5iFAlR6dC"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1K4ts2bZ-96u315XDtIfoZF72N4CZ_5pWG3HO6-K7wko").sheet1

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form["question"].strip()
        if question.lower() == "시험자료":
            answer = "https://naver.me/FW6MU4wD 이수하시는 과목명에 맞춰 다운로드 해주세요"
        elif question in ["학습자등록", "학점인정"]:
            answer = "학습자등록 및 학점인정 신청은 1월, 4월, 7월, 10월에 가능합니다."
        elif question == "학위신청":
            answer = "학위신청은 1월, 7월 중 가능합니다."
        elif question.startswith("토론 작성해줘:") or question.startswith("이게 토론 주제야:"):
            topic = question.split(":", 1)[-1].strip()
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"{topic}에 대해 A4 반페이지 분량의 토론글을 써줘."}]
            )
            answer = gpt_response['choices'][0]['message']['content']
        else:
            answer = "담당자를 통해 질문 남겨주시면 그에 맞춰 확인되는대로 신속한 답변 받아보실 수 있으실거에요 ^^ 화이팅입니다!"
    return render_template("chat.html", answer=answer)
