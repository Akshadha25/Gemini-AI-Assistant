from flask import Flask
from services.database import init_db
from routes.chat import chat_bp

app = Flask(__name__)

init_db()

app.register_blueprint(chat_bp)


if __name__ == "__main__":
    app.run(debug=True)
    