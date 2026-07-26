import os
from dotenv import load_dotenv
from google import genai

from services.database import (
    save_message,
    get_messages,
    get_chat,
    rename_chat
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_response(chat_id, prompt):

    try:

        # Save user's message
        save_message(chat_id, "user", prompt)

        # Auto rename first message
        chat = get_chat(chat_id)

        print("==========")
        print("Chat:", dict(chat) if chat else None)

        if chat:
            print("Current title:", chat["title"])

        if chat and chat["title"] == "New Chat":

            print("Renaming chat...")

            title = prompt.strip()[:40]

            if len(prompt) > 40:
                title += "..."

            rename_chat(chat_id, title)

            print("Renamed to:", title)

        else:
            print("Rename skipped")

        # Get conversation history
        history = get_messages(chat_id)

        # Ask Gemini
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=history
        )

        reply = response.text

        # Save AI response
        save_message(chat_id, "model", reply)

        return reply

    except Exception as e:

        print(e)

        return "Sorry, something went wrong."