from flask import Flask, render_template, request
import openai

app = Flask(__name__)
openai.api_key = "sk-proj-LBBNz8QaZKjVvsncB380T3BlbkFJxQPBjZ2uvZs5iFAlR6dC"

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        if "시험자료" in question:
            answer = "https://naver.me/FW6MU4wD 를 참고해서 과목명에 맞춰 다운로드 해주세요."
        else:
            answer = "담당자를 통해 질문 남겨주시면 그에 맞춰 신속한 답변 받아보실 수 있으실 거예요 ^^ 화이팅입니다!"
    return render_template("chat.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
