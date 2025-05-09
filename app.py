from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import openai

app = Flask(__name__)
openai.api_key = "sk-proj-LBBNz8QaZKjVvsncB380T3BlbkFJxQPBjZ2uvZs5iFAlR6dC"
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1K4ts2bZ-96u315XDtIfoZF72N4CZ_5pWG3HO6-K7wko/export?format=csv'

def load_student_data():
    return pd.read_csv(SHEET_URL)

def generate_debate(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 학점은행제 토론 과제 전문가야. 서론, 본론, 결론 구조로 600자 이상 작성해줘."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content.strip()

def match_schedule(student, message):
    mapping = {
        "개강": "개강일", "복습시작": "복습시험시작", "복습종료": "복습시험종료",
        "과제시작": "과제시작", "과제종료": "과제종료",
        "중간": "중간시작", "중간종료": "중간종료",
        "토론시작": "토론시작", "토론종료": "토론종료"
    }
    for k, col in mapping.items():
        if k in message:
            return f"{k} 일정은 {student.get(col, '등록되지 않음')}입니다."
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        df = load_student_data()
        match = df[df['교육원아이디'] == int(user_id)]
        if not match.empty:
            student = match.iloc[0].to_dict()
            return render_template('chat.html', student=student)
        else:
            error = "존재하지 않는 교육원아이디입니다."
    return render_template('login.html', error=error)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    message = data.get("message")
    student = data.get("student")

    schedule = match_schedule(student, message)
    if schedule:
        return jsonify({"response": schedule})

    if "토론" in message:
        reply = generate_debate(message.replace("토론 작성해줘:", "").strip())
    else:
        reply = f"Q. {message}\nA. '{message}'에 대한 일반적인 응답입니다."
    return jsonify({"response": reply})
