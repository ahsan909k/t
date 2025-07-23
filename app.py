from flask import Flask, request, jsonify, render_template
from agent.intent_router import handle_message

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")  # ⬅️ Now it renders the chat UI

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Missing message"}), 400

    response = handle_message(message)
    # Check if response is already a dictionary or a string
    if isinstance(response, dict):
        return jsonify(response)
    else:
        return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
