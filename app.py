from flask import Flask, render_template, request, session, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'credimate-secret'

student_schedule = {
    "홍길동": {
        "개강일": "2025-06-01",
        "중간평가": "2025-06-15",
        "종강일": "2025-06-30"
    },
    "김영희": {
        "개강일": "2025-07-01",
        "중간평가": "2025-07-15",
        "종강일": "2025-07-31"
    }
}

def generate_response(student, message):
    message = message.strip().lower()
    data = student_schedule.get(student, {})

    if any(key in message for key in ["개강", "시작"]):
        return f"{student}님, 개강일은 {data.get('개강일', '등록되지 않음')}입니다."
    elif "중간" in message:
        return f"{student}님, 중간평가는 {data.get('중간평가', '등록되지 않음')} 예정입니다."
    elif any(key in message for key in ["종강", "끝"]):
        return f"{student}님, 종강일은 {data.get('종강일', '등록되지 않음')}입니다."
    elif "상담" in message:
        return f"상담 관련 문의는 담당자에게 연결해 드릴게요."
    else:
        return f"죄송해요. 정확한 정보를 찾을 수 없어요. 관리자에게 문의해 주세요."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    student = request.form.get("name")
    session['student'] = student
    return jsonify({"message": f"안녕하세요, {student}님! 무엇이 궁금하신가요?"})

@app.route("/ask", methods=["POST"])
def ask():
    student = session.get('student')
    message = request.form.get("message")
    answer = generate_response(student, message)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
