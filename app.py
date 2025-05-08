
from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Google Sheets CSV 링크 (공유 시트 → File > Share > Anyone with the link)
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1K4ts2bZ-96u315XDtIfoZF72N4CZ_5pWG3HO6-K7wko/export?format=csv"

def fetch_student_data():
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        return df
    except Exception as e:
        return None

@app.route("/", methods=["GET", "POST"])
def chatbot():
    message = ""
    student_name = ""
    if request.method == "POST":
        user_id = request.form.get("student_id")
        question = request.form.get("question")

        df = fetch_student_data()
        if df is None:
            message = "학사일정 데이터를 불러오는 데 실패했습니다."
        elif user_id not in df["교육원아이디"].astype(str).values:
            message = "입력하신 교육원아이디가 존재하지 않습니다."
        else:
            student_row = df[df["교육원아이디"].astype(str) == user_id].iloc[0]
            student_name = student_row["이름"]
            matched = False

            for column in df.columns:
                if column == "교육원아이디" or column == "이름" or column == "교육원":
                    continue
                if column.replace(" ", "")[:-2] in question.replace(" ", ""):
                    value = student_row[column]
                    if pd.isna(value):
                        continue
                    message = f"{student_name}님, {column}은(는) {value}입니다."
                    matched = True
                    break

            if not matched:
                message = "질문을 이해하지 못했어요. 일정명(예: 복습시험, 과제, 토론 등)을 포함해주세요."

    return render_template("index.html", message=message, name=student_name)

if __name__ == "__main__":
    app.run(debug=True)
