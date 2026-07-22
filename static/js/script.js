const input = document.querySelector("input");
const sendBtn = document.querySelector(".btn-success");
const chatBox = document.querySelector(".chat-box");

function addMessage(msg, cls) {
    const div = document.createElement("div");
    div.className = cls;
    div.innerText = msg;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {

    const msg = input.value.trim();

    if(msg==="") return;

    addMessage(msg,"user-msg");

    input.value="";

    const res = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:msg
        })
    });

    const data = await res.json();

    addMessage(data.reply,"ai-msg");
}

sendBtn.addEventListener("click",sendMessage);

input.addEventListener("keypress",function(e){
    if(e.key==="Enter"){
        sendMessage();
    }
})
