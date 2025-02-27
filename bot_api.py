from groq import Groq
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key="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")

def chat_with_groq(message):
    # Danh sách mở rộng các câu hỏi về "boss" hoặc "tạo ra", có dấu và không dấu
    boss_keywords = [
        "boss may la ai", "boss mày là ai", "ông chủ mày là ai", "ong chu may la ai",
        "may do ai tao ra", "mày do ai tạo ra", "ai tao ra may", "ai tạo ra mày",
        "chu cua may la ai", "chủ của mày là ai", "ai la chu cua may", "ai là chủ của mày",
        "ai la boss cua may", "ai là boss của mày", "ông chủ của mày là ai", "ong chu cua may la ai",
        "may duoc ai tao ra", "mày được ai tạo ra", "ai la nguoi tao ra may", "ai là người tạo ra mày",
        "cha de cua may la ai", "cha đẻ của mày là ai", "ai la nguoi dung sau may", "ai là người đứng sau mày",
        "ai quan ly may", "ai quản lý mày", "ai la chu nhan cua may", "ai là chủ nhân của mày",
        "may thuoc ve ai", "mày thuộc về ai", "ai so huu may", "ai sở hữu mày",
        "ai la nguoi dieu khien may", "ai là người điều khiển mày", "ai la nguoi lap trinh may", "ai là người lập trình mày",
        "boss cua may", "ông chủ của mày", "người tạo ra mày", "chủ nhân của mày"
    ]
    
    # Chuyển message về chữ thường để so sánh
    message_lower = message.lower()
    
    # Kiểm tra nếu message chứa bất kỳ keyword nào
    if any(keyword in message_lower for keyword in boss_keywords):
        return "Boss tao là Thằng Khải siêu cấp vip pro, mày mà đụng vào nó là biết tao!"
    
    # Nếu không, trả lời bựa như cũ
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Bạn là Bot chuyên trả lời các vấn đề liên quan đến Thành phố Đà Nẵng"},
            {"role": "user", "content": message}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({"reply": "Hỏi gì mà trống trơn, mày ngu à?"})
    reply = chat_with_groq(user_input)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
