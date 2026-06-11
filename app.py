from flask import Flask, request, send_file, jsonify
import requests
import os

app = Flask(__name__)

# Render'ın "Environment" kısmından API_KEY'i alıyoruz
API_KEY = os.environ.get("API_KEY")
MODEL = "llama-3.1-8b-instant"
APK_ISMI = "forsy_v2.apk"
APK_YOLU = os.path.join(os.path.dirname(os.path.abspath(__file__)), APK_ISMI)

@app.route('/')
def index():
    return """
    <html>
    <head><meta charset="UTF-8"><title>Forsy AI</title></head>
    <body style="text-align:center; background:#121212; color:white;">
        <h1>Forsy AI</h1>
        <div id="chat-box" style="height:300px; overflow-y:auto; border:1px solid #333; margin:20px; padding:10px;"></div>
        <input type="text" id="userInput" placeholder="Mesaj yaz...">
        <button onclick="sendMessage()">Gönder</button><br>
        <a href="/indir" style="color:green;">🤖 APK İNDİR</a>
        <script>
            async function sendMessage() {
                const input = document.getElementById("userInput");
                const val = input.value;
                document.getElementById("chat-box").innerHTML += "<div>Sen: " + val + "</div>";
                const res = await fetch("/ask", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: val})
                });
                const data = await res.json();
                document.getElementById("chat-box").innerHTML += "<div>AI: " + data.response + "</div>";
                input.value = "";
            }
        </script>
    </body>
    </html>
    """

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        data = response.json()
        ai_response = data['choices'][0]['message']['content']
    except:
        ai_response = "Hata: API anahtarı veya bağlantı sorunu."
    return jsonify({"response": ai_response})

@app.route('/indir')
def indir():
    return send_file(APK_YOLU, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)