
import openai

def get_answer(question):
    # Check if the question contains '시험자료' and provide the URL
    if "시험자료" in question:
        return "https://naver.me/FW6MU4wD 이수하시는 과목명에 맞춰 다운로드 해주세요."
    
    # Default answer for other questions
    return "담당자를 통해 질문 남겨주시면 그에 맞춰 확인되는대로 신속한 답변 받아보실 수 있으실거에요 ^^ 화이팅입니다!"

# Example test
question = "시험자료"
print(get_answer(question))  # Test with a question containing '시험자료'
