
from flask import Flask, request, render_template, session, redirect
import pandas as pd
import openai
import os

app = Flask(__name__)
app.secret_key = "credimate_secret_key"

openai.api_key = os.getenv("OPENAI_API_KEY")

GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1K4ts2bZ-96u315XDtIfoZF72N4CZ_5pWG3HO6-K7wko/export?format=csv"

def fetch_student_data():
    try:
        return pd.read_csv(GOOGLE_SHEET_CSV_URL)
    except:
        return None

def answer_from_sheet(df, user_id, question):
    student_row = df[df["교육원아이디"].astype(str) == user_id].iloc[0]
    for column in df.columns:
        if column in ["교육원아이디", "이름", "교육원"]:
            continue
        keyword = column.replace(" ", "").replace("시작", "").replace("종료", "")
        if keyword in question.replace(" ", ""):
            value = student_row[column]
            if pd.isna(value):
                continue
            return f"{student_row['이름']}님, {column}은(는) {value}입니다."
    return None

def answer_from_gpt(question, mode="default"):
    try:
        system_prompt = (
            "너는 학점은행제를 담당하는 교수로서 학생들에게 토론자료를 제공해주는 역할이야. "
            "그래서 이어진 문장으로 토론에 대한 주제로 내가 자료를 요청하면 "
            "완벽하게 모사율에 걸리지 않는 자료로 만들어서 나에게 보내줘. "
            "글자수는 400자를 넘겨줘."
        ) if mode == "discussion" else "당신은 친절하고 정확한 교육 상담 챗봇입니다."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except:
        return "GPT 응답에 문제가 발생했습니다. 다시 시도해주세요."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "student_id" in request.form:
            session["student_id"] = request.form["student_id"]
            return redirect("/")
        elif "question" in request.form and "student_id" in session:
            df = fetch_student_data()
            if df is None:
                return render_template("chat.html", message="구글 시트를 불러올 수 없습니다.")
            user_id = session["student_id"]
            if user_id not in df["교육원아이디"].astype(str).values:
                return render_template("chat.html", message="등록되지 않은 교육원아이디입니다.")
            question = request.form["question"]

            if "토론 작성해줘" in question or "이게 토론 주제야" in question:
                gpt_answer = answer_from_gpt(question, mode="discussion")
                return render_template("chat.html", message=gpt_answer)

            sheet_answer = answer_from_sheet(df, user_id, question)
            if sheet_answer:
                return render_template("chat.html", message=sheet_answer)
            else:
                gpt_answer = answer_from_gpt(question)
                return render_template("chat.html", message=gpt_answer)
    return render_template("chat.html")

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
