import os
import traceback
from dotenv import load_dotenv
from google import genai

from services.database import save_message, get_messages

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_response(prompt):
    try:
        # Save user's message
        save_message("user", prompt)

        # Send entire conversation
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=get_messages()
        )

        reply = response.text

        # Save AI response
        save_message("model", reply)

        return reply

    except Exception:
        traceback.print_exc()
        return "Sorry, I couldn't generate a response." 
    