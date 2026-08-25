from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Predefined input patterns and responses for commercial use (Task 4 requirement)
BOT_RESPONSES = {
    "hello": [
        "Hello! Welcome to CodeAlpha Cloud Services. How can I help you today?", 
        "Hi there! What can I assist you with?"
    ],
    "services": [
        "We offer cloud infrastructure management, scalable cloud solutions, and software development.", 
        "Our focus is on scalable, secure, and efficient cloud solutions."
    ],
    "internship": [
        "This internship program provides practical experience in cloud technologies, virtualization, and containerization!",
        "You can earn completion certificates, recommendation letters, and placement support."
    ],
    "contact": [
        "You can reach us via email at services@codealpha.tech or visit www.codealpha.tech."
    ],
    "default": [
        "That's an interesting question! Could you please clarify or check our website for details?",
        "I am trained to help with CodeAlpha cloud services and internship queries. How else can I assist?"
    ]
}

def get_bot_response(user_message):
    user_message = user_message.lower()
    for key in BOT_RESPONSES:
        if key in user_message:
            return random.choice(BOT_RESPONSES[key])
    return random.choice(BOT_RESPONSES["default"])

# HTML Template with integrated website chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodeAlpha Cloud Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .chat-container { width: 100%; max-width: 400px; background: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 500px; }
        .chat-header { background: #007bff; color: white; padding: 15px; text-align: center; font-weight: bold; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px; border-radius: 6px; max-width: 80%; line-height: 1.4; }
        .user-message { background: #007bff; color: white; align-self: flex-end; }
        .bot-message { background: #e9ecef; color: #333; align-self: flex-start; }
        .chat-input-area { display: flex; border-top: 1px solid #ddd; padding: 10px; background: #fff; }
        .chat-input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; outline: none; }
        .chat-input-area button { background: #007bff; color: white; border: none; padding: 10px 15px; margin-left: 5px; border-radius: 4px; cursor: pointer; }
        .chat-input-area button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">CodeAlpha Support Chatbot</div>
        <div class="chat-box" id="chatBox">
            <div class="message bot-message">Hello! I am your CodeAlpha assistant. Ask me about our cloud services or internship!</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="userInput" placeholder="Type a message..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            let inputField = document.getElementById("userInput");
            let text = inputField.value.trim();
            if (text === "") return;

            let chatBox = document.getElementById("chatBox");
            chatBox.innerHTML += `<div class="message user-message">${text}</div>`;
            inputField.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            fetch("/get_response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            })
            .then(res => res.json())
            .then(data => {
                chatBox.innerHTML += `<div class="message bot-message">${data.response}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        }
        function handleKeyPress(e) {
            if (e.key === "Enter") sendMessage();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_msg = data.get("message", "")
    bot_reply = get_bot_response(user_msg)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)