from groq import Groq
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key="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")

def chat_with_groq(message):
    # Danh sách mở rộng các câu hỏi về "Chị Liên" hoặc "tạo ra", có dấu và không dấu
    boss_keywords = [
        "Chị Liên la ai"
    ]
    
    # Chuyển message về chữ thường để so sánh
    message_lower = message.lower()
    
    # Kiểm tra nếu message chứa bất kỳ keyword nào
    if any(keyword in message_lower for keyword in boss_keywords):
        return "Chị Liên xinh đẹp nhứt ở Trung tâm IOC!"
    
    # Nếu không, trả lời bựa như cũ
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Bạn là Bot bựa trả lời hài hước"},
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
