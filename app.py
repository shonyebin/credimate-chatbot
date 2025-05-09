from flask import Flask, render_template, request
import openai

app = Flask(__name__)

openai.api_key = "sk-proj-LBBNz8QaZKjVvsncB380T3BlbkFJxQPBjZ2uvZs5iFAlR6dC"

@app.route("/", methods=["GET", "POST"])
def chat():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        if "시험자료" in question:
            answer = "https://naver.me/FW6MU4wD 이수하시는 과목명에 맞춰 다운로드 해주세요"
        elif "소속" in question:
            answer = "재학 중입니다"
        elif "교육원이 어디야" in question or "교육원" in question:
            answer = "귀하가 등록하신 교육원의 이름은 시스템에 등록되어 있습니다."
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}]
            )
            answer = response["choices"][0]["message"]["content"]
    return render_template("chat.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
