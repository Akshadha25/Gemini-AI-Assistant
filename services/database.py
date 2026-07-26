import sqlite3

DB_PATH = "database/chat.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chat_sessions(id)
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Chat Session Functions
# -----------------------------

def create_chat(title="New Chat"):
    conn = get_connection()

    cursor = conn.execute(
        "INSERT INTO chat_sessions(title) VALUES(?)",
        (title,)
    )

    conn.commit()

    chat_id = cursor.lastrowid

    conn.close()

    return chat_id


def get_chats():
    conn = get_connection()

    chats = conn.execute("""
        SELECT *
        FROM chat_sessions
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return chats


def get_chat(chat_id):
    conn = get_connection()

    chat = conn.execute(
        """
        SELECT *
        FROM chat_sessions
        WHERE id = ?
        """,
        (chat_id,)
    ).fetchone()

    conn.close()

    return chat


def rename_chat(chat_id, title):
    conn = get_connection()

    conn.execute(
        """
        UPDATE chat_sessions
        SET title = ?
        WHERE id = ?
        """,
        (title, chat_id)
    )

    conn.commit()
    conn.close()


def delete_chat(chat_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM messages WHERE chat_id = ?",
        (chat_id,)
    )

    conn.execute(
        "DELETE FROM chat_sessions WHERE id = ?",
        (chat_id,)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Message Functions
# -----------------------------

def save_message(chat_id, role, message):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO messages(chat_id, role, message)
        VALUES (?, ?, ?)
        """,
        (chat_id, role, message)
    )

    conn.commit()
    conn.close()


def get_messages(chat_id):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT role, message
        FROM messages
        WHERE chat_id = ?
        ORDER BY id
        """,
        (chat_id,)
    ).fetchall()

    conn.close()

    history = []

    for row in rows:
        history.append({
            "role": row["role"],
            "parts": [
                {
                    "text": row["message"]
                }
            ]
        })

    return history


def clear_messages(chat_id):
    conn = get_connection()

    conn.execute(
        """
        DELETE FROM messages
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    conn.commit()
    conn.close()