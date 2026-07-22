from services.database import init_db
from flask import Flask, render_template, request, jsonify
from services.gemini import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    msg = data.get("message")

    reply = get_response(msg)

    return jsonify({
        "reply": reply
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    
    