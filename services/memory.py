conversation = []


def add_message(role, text):
    conversation.append({
        "role": role,
        "parts": [{"text": text}]
    })


def get_history():
    return conversation


def clear_history():
    conversation.clear()
    