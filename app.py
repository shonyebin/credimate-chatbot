
from flask import Flask, request, render_template, session, redirect
import pandas as pd
import openai
import os

app = Flask(__name__)
app.secret_key = "credimate_secret_key"  # 세션용 시크릿 키

# OpenAI API 키 설정
openai.api_key = "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"

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

def answer_from_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 학사일정을 도와주는 친절한 교육 조교입니다."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
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
