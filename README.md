# 🤖 Gemini AI Assistant

A full-stack AI chatbot built with Flask, SQLite, JavaScript, and Google's Gemini API.

## Features

- 🤖 Gemini AI chatbot
- 💬 Multiple conversations
- 💾 Persistent chat history using SQLite
- ✏️ Automatic chat titles
- 🆕 Create new conversations
- 🗑️ Delete conversations
- 🔄 Load previous conversations
- 📝 Markdown support
- 💻 Code syntax highlighting
- 🌙 Dark-themed responsive interface

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap
- Marked.js
- Highlight.js

### Backend
- Python
- Flask
- Google Gemini API

### Database
- SQLite

## Project Structure

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
│   └── gemini.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── templates/
    └── index.html