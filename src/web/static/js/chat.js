const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");

const SESSION_USER_ID = "web_user_999";

sendButton.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    appendMessage(message, "user-message");

    userInput.value = "";

    sendButton.disabled = true;

    const loadingMessage = appendMessage(
        "Thinking...",
        "ai-message"
    );

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                user_id: SESSION_USER_ID,

                message: message

            })

        });

        const data = await response.json();

        loadingMessage.innerText = data.reply;

    } catch (error) {

        loadingMessage.innerText =
            "Unable to connect to the server.";

    } finally {

        sendButton.disabled = false;

        userInput.focus();

    }
}

function appendMessage(text, className) {

    const message = document.createElement("div");

    message.className = `message ${className}`;

    message.innerText = text;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;

    return message;
}