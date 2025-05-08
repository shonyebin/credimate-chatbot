
# 여기에 수정된 app.py 내용 추가 (필요 시 내용 수정)

import openai
from flask import Flask, render_template, request, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 구글 시트 연동
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credimate-credentials.json", scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1K4ts2bZ-96u315XDtIfoZF72N4CZ_5pWG3HO6-K7wko/edit#gid=0").sheet1

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    student_id = session.get("student_id", "")

    if request.method == "POST":
        question = request.form["question"]
        session["student_id"] = request.form["student_id"]
        student_id = session["student_id"]

        student_data = None
        student_list = sheet.get_all_records()
        for row in student_list:
            if str(row["교육원아이디"]) == str(student_id):
                student_data = row
                break

        # 명령어 처리
        if "시험자료" in question:
            answer = "시험자료는 [링크]에서 확인 가능합니다."
        elif question.startswith("토론 작성해줘"):
            topic = question.replace("토론 작성해줘", "").strip(" :")
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"토론 주제: {topic}"}]
            )
            answer = gpt_response.choices[0].message.content.strip()
        else:
            answer = "기타 질문은 담당자에게 문의해주세요."

    return render_template("chat.html", answer=answer, question=question)

if __name__ == "__main__":
    app.run(debug=True)
