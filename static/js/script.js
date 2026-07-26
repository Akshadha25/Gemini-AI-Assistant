let chatId = null;

const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("chatBox");
const historyBox = document.getElementById("chat-history");
const newChatBtn = document.getElementById("newChatBtn");


/* ================= MESSAGE DISPLAY ================= */

function addMessage(msg, cls) {

    const div = document.createElement("div");

    div.className = cls;

    if (window.marked) {
        div.innerHTML = marked.parse(msg);
    } else {
        div.innerText = msg;
    }

    chatBox.appendChild(div);

    if (window.hljs) {

        div.querySelectorAll("pre code").forEach(block => {
            hljs.highlightElement(block);
        });

    }

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* ================= CLEAR CHAT ================= */

function clearChat() {
    chatBox.innerHTML = "";
}


/* ================= LOAD ALL CHATS ================= */

async function loadChats() {

    try {

        const res = await fetch("/chats");

        if (!res.ok) {
            throw new Error("Failed to load chats");
        }

        const chats = await res.json();

        historyBox.innerHTML = "";

        chats.forEach(chat => {

            const item = document.createElement("div");

            item.className = "history-item";

            if (Number(chat.id) === Number(chatId)) {
                item.classList.add("active");
            }


            /* Chat title */

            const title = document.createElement("span");

            title.className = "chat-title";

            title.innerText = chat.title;

            title.title = chat.title;


            /* Delete button */

            const deleteBtn = document.createElement("button");

            deleteBtn.className = "delete-chat";

            deleteBtn.innerHTML = "🗑";

            deleteBtn.title = "Delete chat";


            deleteBtn.addEventListener("click", function(event) {

                event.stopPropagation();

                deleteChat(chat.id);

            });


            item.appendChild(title);

            item.appendChild(deleteBtn);


            /* Open chat */

            item.addEventListener("click", function() {

                loadChat(chat.id);

            });


            historyBox.appendChild(item);

        });

    } catch (error) {

        console.error("Failed to load chats:", error);

    }

}


/* ================= DELETE CHAT ================= */

async function deleteChat(id) {

    const confirmed = confirm(
        "Are you sure you want to delete this conversation?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const res = await fetch(`/chat/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            throw new Error("Failed to delete chat");
        }


        if (Number(chatId) === Number(id)) {

            chatId = null;

            clearChat();

            addMessage(
                "👋 Hello! I'm your AI Assistant.",
                "ai-msg"
            );

        }


        await loadChats();

    } catch (error) {

        console.error(error);

        alert("Could not delete the conversation.");

    }

}


/* ================= LOAD SINGLE CHAT ================= */

async function loadChat(id) {

    try {

        chatId = id;

        const res = await fetch(`/chat/${id}`);

        if (!res.ok) {
            throw new Error("Failed to load chat");
        }

        const messages = await res.json();

        clearChat();


        if (messages.length === 0) {

            addMessage(
                "👋 Hello! I'm your AI Assistant.",
                "ai-msg"
            );

        }


        messages.forEach(msg => {

            if (msg.role === "user") {

                addMessage(
                    msg.message,
                    "user-msg"
                );

            } else {

                addMessage(
                    msg.message,
                    "ai-msg"
                );

            }

        });


        await loadChats();

        input.focus();

    } catch (error) {

        console.error("Failed to load chat:", error);

    }

}


/* ================= CREATE NEW CHAT ================= */

async function createNewChat() {

    try {

        const res = await fetch("/new-chat", {
            method: "POST"
        });

        if (!res.ok) {
            throw new Error("Failed to create chat");
        }

        const data = await res.json();

        chatId = data.chat_id;

        clearChat();

        addMessage(
            "👋 Hello! I'm your AI Assistant.",
            "ai-msg"
        );

        await loadChats();

        input.focus();

    } catch (error) {

        console.error("Failed to create chat:", error);

    }

}


/* ================= SEND MESSAGE ================= */

async function sendMessage() {

    const msg = input.value.trim();

    if (msg === "") {
        return;
    }


    addMessage(msg, "user-msg");

    input.value = "";


    sendBtn.disabled = true;
    input.disabled = true;


    const loading = document.createElement("div");

    loading.className = "ai-msg";

    loading.innerText = "🤖 Thinking...";

    chatBox.appendChild(loading);

    chatBox.scrollTop = chatBox.scrollHeight;


    try {

        const res = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                chat_id: chatId,

                message: msg

            })

        });


        if (!res.ok) {

            const errorText = await res.text();

            console.error("Server response:", errorText);

            throw new Error(`Server error: ${res.status}`);

        }


        const data = await res.json();


        chatId = data.chat_id;


        loading.remove();


        addMessage(
            data.reply,
            "ai-msg"
        );


        await loadChats();


    } catch (error) {

        console.error("Send message error:", error);

        loading.remove();

        addMessage(
            "❌ Something went wrong. Check the Flask terminal.",
            "ai-msg"
        );

    }


    sendBtn.disabled = false;

    input.disabled = false;

    input.focus();

}


/* ================= ENTER KEY ================= */

input.addEventListener("keypress", function(e) {

    if (e.key === "Enter") {

        e.preventDefault();

        sendMessage();

    }

});


/* ================= BUTTONS ================= */

sendBtn.addEventListener(
    "click",
    sendMessage
);


newChatBtn.addEventListener(
    "click",
    createNewChat
);


/* ================= START APP ================= */

loadChats();

input.focus();