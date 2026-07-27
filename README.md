# 🤖 Gemini AI Assistant

A full-stack AI chatbot that combines **Google Gemini** with persistent conversation memory and real-time web search.

The application provides a modern conversational interface where users can interact with Gemini, maintain multiple conversations, revisit previous chats, and retrieve up-to-date information from the web.

## ✨ Features

* 🤖 AI-powered conversations using Google Gemini
* 💬 Multiple independent conversations
* 💾 Persistent conversation history with SQLite
* 🧠 Context-aware responses using previous messages
* 🌐 Real-time web search using Tavily
* 🔎 Up-to-date answers for current information
* ✏️ Automatic conversation titles
* 🆕 Create new conversations
* 🗑️ Delete conversations
* 🔄 Load previous conversations
* 📝 Markdown rendering
* 💻 Code syntax highlighting
* 🌙 Dark-themed responsive interface

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap
* Marked.js
* Highlight.js

### Backend

* Python
* Flask
* Google Gemini API
* Tavily Search API
* python-dotenv

### Database

* SQLite

## 🧠 How It Works

The application follows a simple conversational pipeline:

1. The user enters a message through the web interface.
2. Flask receives the request from the frontend.
3. The user's message is stored in the SQLite database.
4. Previous messages from the conversation are retrieved to maintain context.
5. Gemini processes the conversation and generates a response.
6. When current information is required, Tavily is used to retrieve relevant web results.
7. The response is returned to the frontend.
8. The generated response is stored in the database for future context.

This allows the assistant to combine **conversational memory with real-time information retrieval**.

## 📁 Project Structure

```text
Gemini-AI-Assistant/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── database/
│   └── chat.db
│
├── routes/
│   └── chat.py
│
├── services/
│   ├── database.py
│   ├── gemini.py
│   └── search.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── templates/
    └── index.html
```

## ⚙️ Requirements

The project uses the following Python packages:

```text
Flask
google-genai
python-dotenv
tavily-python
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

API keys should never be committed to GitHub.

## 🚀 Running the Project

Clone the repository and navigate into the project:

```bash
git clone https://github.com/Akshadha25/Gemini-AI-Assistant.git
cd Gemini-AI-Assistant
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the environment variables in `.env`, then start the Flask application:

```bash
python app.py
```

Open the local application in your browser at:

```text
http://127.0.0.1:5000
```

## 🔐 Security

API credentials are stored using environment variables and excluded from version control through `.gitignore`.

The `.env` file and local SQLite database should not be uploaded to the repository.

## 🎯 Purpose

This project demonstrates how modern AI applications can combine:

* Large language models
* Conversation memory
* Database persistence
* Real-time web search
* REST-style Flask routes
* Interactive frontend development

It serves as a foundation for building more advanced AI assistants and intelligent web applications.

## 📌 Future Improvements

Potential extensions include:

* 🎤 Voice input and speech recognition
* 🔊 Text-to-speech responses
* 📎 File and document uploads
* 🖼️ Image understanding
* 👤 User authentication
* ⚡ Streaming AI responses
* 📱 Improved mobile interface
* 🧩 Additional external API integrations

## 👩‍💻 Author

**Akshadha Vikraman**

Built as a practical AI application using Python, Flask, Google Gemini, SQLite, and real-time web search.
