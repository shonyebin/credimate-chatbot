
from flask import Flask, render_template, request, session
import openai
import os
import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = "your_secret_key"

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 구글 시트 연동
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credimate-credentials.json", scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1K4ts2bZ-96u315XDtIfoZF72N4CZ_5pWG3HO6-K7wko/edit#gid=0").sheet1

# 예시 명령어 텍스트
example_commands = "예시: '시험자료' / '토론 작성해줘 : [주제]' / '학점인정은 언제야?'"

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    student_id = session.get("student_id", "")

    if request.method == "POST":
        question = request.form["question"]
        session["student_id"] = request.form["student_id"]
        student_id = session["student_id"]

        # 시트에서 해당 학생 데이터 찾기
        student_data = None
        try:
            student_list = sheet.get_all_records()
            for row in student_list:
                if str(row["교육원아이디"]) == str(student_id):
                    student_data = row
                    break
        except Exception:
            answer = "구글 시트에서 데이터를 불러오는 중 문제가 발생했어요. 잠시 후 다시 시도해주세요."
            return render_template("chat.html", answer=answer, question=question, example_commands=example_commands)

        # 명령어 처리
        if "시험자료" in question:
            answer = '<a href="https://naver.me/FW6MU4wD" target="_blank">https://naver.me/FW6MU4wD</a> 이수하시는 과목명에 맞춰 다운로드 해주세요'
        elif question.startswith("토론 작성해줘"):
            topic = question.replace("토론 작성해줘", "").strip(" :")
            gpt_prompt = f"너는 학점은행제를 담당하는 교수로써 학생들에게 토론자료를 제공해주는 역할이야. 이어진 문장으로 토론 주제에 대한 글을 완성해줘. 주제: {topic}. 400자 이상. 모사율에 걸리지 않게 해줘."
            try:
                gpt_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": gpt_prompt}
                    ]
                )
                answer = gpt_response.choices[0].message.content.strip()
            except Exception:
                answer = "GPT 응답에 문제가 발생했습니다. 다시 시도해주세요."
        elif "교육원" in question and "어디" in question:
            if student_data and "교육원" in student_data:
                answer = f'현재 재학 중인 교육원은 "{student_data["교육원"]}"입니다.'
            else:
                answer = "재학 중인 교육원을 찾을 수 없습니다."
        elif any(kw in question for kw in ["학습자등록", "학점인정", "학위신청"]):
            answer = "학습자등록과 학점인정 신청은 1월, 4월, 7월, 10월에 진행되며, 학위신청은 1월과 7월에 가능합니다."
        else:
            answer = "담당자를 통해 질문 남겨주시면 그에 맞춰 확인되는대로 신속한 답변 받아보실 수 있으실거에요 ^^ 화이팅입니다!"

    return render_template("chat.html", answer=answer, question=question, student_id=student_id, example_commands=example_commands)

if __name__ == "__main__":
    app.run(debug=True)
