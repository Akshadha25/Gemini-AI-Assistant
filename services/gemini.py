import os
from dotenv import load_dotenv
from google import genai
from tavily import TavilyClient

from services.database import (
    save_message,
    get_messages,
    get_chat,
    rename_chat
)

load_dotenv()

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def needs_web_search(prompt):
    keywords = [
        "current",
        "today",
        "latest",
        "recent",
        "now",
        "price",
        "weather",
        "news",
        "score",
        "stock",
        "bitcoin",
        "btc",
        "temperature",
        "who won",
        "this week",
        "this month"
    ]

    prompt_lower = prompt.lower()

    return any(word in prompt_lower for word in keywords)


def web_search(prompt):

    try:

        results = tavily_client.search(
            query=prompt,
            search_depth="basic",
            max_results=5
        )

        context = ""

        for result in results.get("results", []):

            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            context += f"""
Title: {title}
Content: {content}
Source: {url}

"""

        return context

    except Exception as e:

        print("Tavily Error:", e)

        return ""


def get_response(chat_id, prompt):

    try:

        save_message(chat_id, "user", prompt)

        chat = get_chat(chat_id)

        if chat and chat["title"] == "New Chat":

            title = prompt.strip()[:40]

            if len(prompt) > 40:
                title += "..."

            rename_chat(chat_id, title)

        history = get_messages(chat_id)

        contents = []

        for msg in history:

            contents.append({
                "role": msg["role"],
                "parts": msg["parts"]
            })

        if needs_web_search(prompt):

            search_context = web_search(prompt)

            if search_context:

                contents.append({
                    "role": "user",
                    "parts": [
                        {
                            "text": f"""
Use the following real-time web search results
to answer the user's question.

WEB SEARCH RESULTS:

{search_context}

Answer using the latest information available.
Mention the source when appropriate.
"""
                        }
                    ]
                })

        response = gemini_client.models.generate_content(
            model="gemini-flash-latest",
            contents=contents
        )

        reply = response.text

        save_message(chat_id, "model", reply)

        return reply

    except Exception as e:

        print("Gemini Error:", e)

        return "Sorry, something went wrong."