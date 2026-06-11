from flask import Flask, request, send_file, jsonify
import requests
import os

app = Flask(__name__)

# API anahtarını kodun içine değil, Render'ın "Environment" kısmına ekleyeceğiz.
API_KEY = os.environ.get("API_KEY")
MODEL = "llama-3.1-8b-instant"
APK_ISMI = "forsy_v2.apk"
# Dosya yolunu doğru şekilde ayarladık
APK_YOLU = os.path.join(os.path.dirname(os.path.abspath(__file__)), APK_ISMI)

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Forsy AI</title>
        <meta charset="UTF-8">
        <style>
            body { text-align: center; font-family: sans-serif; background: #121212; color: white; padding: 20px; }
            .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 25px; border-radius: 20px; }
            #chat-box { height: 300px; border: 1px solid #333; margin-bottom: 20px; overflow-y: auto; padding: 10px; background: #181818; text-align: left; }
            input { width: 70%; padding: 10px; }
            button { padding: 10px; cursor: pointer; }
            .download-btn { display: block; margin-top: 20px; padding: 15px; background: #28a745; color: white; text-decoration: none; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Forsy AI</h1>
            <div id="chat-box"></div>
            <input type="text" id="userInput" placeholder="Mesajınızı yazın...">
            <button onclick="sendMessage()">Gönder</button>
            <a href="/indir" class="download-btn">🤖 APK İNDİR</a>
        </div>
        <script>
            async function sendMessage() {
                const input = document.getElementById("userInput");
                const box = document.getElementById("chat-box");
                if(!input.value) return;
                box.innerHTML += `<div><b>Sen:</b> ${input.value}</div>`;
                const res = await fetch("/ask", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: input.value})
                });
                const data = await res.json();
                box.innerHTML += `<div><b>AI:</b> ${data.response}</div>`;
                input.value = "";
            }
        </script>
    </body>
    </html>
    """

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    # API çağrısı buraya gelecek
    return jsonify({"response": "Sistem aktif!"})

@app.route('/indir')
def indir():
    if os.path.exists(APK_YOLU):
        return send_file(APK_YOLU, as_attachment=True)
    return "Dosya bulunamadı!", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)# API çağrısı için basit bir yapı
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
        ai_response = "AI şu an yanıt veremiyor."
        
    return jsonify({"response": ai_response})