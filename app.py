from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import openai

app = Flask(__name__)

# GPT API 키 설정
openai.api_key = "sk-proj-LBBNz8QaZKjVvsncB380T3BlbkFJxQPBjZ2uvZs5iFAlR6dC"

# Google Sheet CSV 연동 링크
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

    if message.startswith("토론") or "토론 작성" in message:
        reply = generate_debate(message.replace("토론 작성해줘:", "").strip())
    else:
        reply = f"Q. {message}\nA. '{message}'에 대한 일반적인 응답입니다. (예시 응답)"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
