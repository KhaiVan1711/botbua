from groq import Groq
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key="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")

def chat_with_groq(message):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Mày là bot siêu bựa, trả lời hài hước, chửi nhẹ nếu hỏi ngu nha!"},
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
