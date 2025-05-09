
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        question = request.form["question"].strip()
        if question == "시험자료":
            answer = "https://naver.me/FW6MU4wD 이수하시는 과목명에 맞춰 다운로드 해주세요"
        elif question in ["학습자등록", "학점인정"]:
            answer = "학습자등록 및 학점인정 신청은 1월, 4월, 7월, 10월에 가능합니다."
        elif question == "학위신청":
            answer = "학위신청은 1월, 7월 중 가능합니다."
        elif question.startswith("토론 작성해줘:") or question.startswith("이게 토론 주제야:"):
            answer = "토론글 자동 생성 기능은 현재 준비 중입니다."
        else:
            answer = "담당자를 통해 질문 남겨주시면 그에 맞춰 신속한 답변 받아보실 수 있으실거에요 ^^ 화이팅입니다!"
    return render_template("chat.html", answer=answer)

if __name__ == "__main__":
    app.run()
