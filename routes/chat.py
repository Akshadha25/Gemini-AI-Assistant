from flask import Blueprint, render_template, request, jsonify

from services.gemini import get_response
from services.database import (
    create_chat,
    get_chats,
    get_messages,
    delete_chat
)

chat_bp = Blueprint("chat", __name__)


# =============================
# HOME
# =============================

@chat_bp.route("/")
def home():
    return render_template("index.html")


# =============================
# SEND MESSAGE
# =============================

@chat_bp.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message")
    chat_id = data.get("chat_id")

    if not message:
        return jsonify({
            "reply": "Please enter a message."
        }), 400

    if not chat_id:
        chat_id = create_chat()

    reply = get_response(chat_id, message)

    return jsonify({
        "reply": reply,
        "chat_id": chat_id
    })


# =============================
# CREATE NEW CHAT
# =============================

@chat_bp.route("/new-chat", methods=["POST"])
def new_chat():

    chat_id = create_chat()

    return jsonify({
        "chat_id": chat_id
    })


# =============================
# GET ALL CHATS
# =============================

@chat_bp.route("/chats")
def chats():

    chats = get_chats()

    return jsonify([
        {
            "id": chat["id"],
            "title": chat["title"]
        }
        for chat in chats
    ])


# =============================
# LOAD ONE CHAT
# =============================

@chat_bp.route("/chat/<int:chat_id>", methods=["GET"])
def load_chat(chat_id):

    history = get_messages(chat_id)

    messages = []

    for msg in history:

        messages.append({
            "role": msg["role"],
            "message": msg["parts"][0]["text"]
        })

    return jsonify(messages)


# =============================
# DELETE CHAT
# =============================

@chat_bp.route("/chat/<int:chat_id>", methods=["DELETE"])
def remove_chat(chat_id):

    chat = get_chats()

    chat_exists = any(
        int(c["id"]) == chat_id
        for c in chat
    )

    if not chat_exists:

        return jsonify({
            "error": "Chat not found"
        }), 404

    delete_chat(chat_id)

    return jsonify({
        "success": True,
        "message": "Chat deleted successfully"
    })