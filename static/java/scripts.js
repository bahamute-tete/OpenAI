document.getElementById("sendMessage").addEventListener("click", function () {
    var messageInput = document.getElementById("messageInput");
    var messageText = messageInput.value.trim();

    if (messageText) {
        // Send AJAX request to the Flask server
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'message': messageText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.reply) {
                addMessageToChat("You", messageText);
                addMessageToChat("AI", data.reply);
            }
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });

        messageInput.value = "";
    }
});

function addMessageToChat(sender, text) {
    var chatArea = document.getElementById("chatArea");

    var newMessage = document.createElement("div");
    newMessage.classList.add("card", "mb-3");

    var newMessageBody = document.createElement("div");
    newMessageBody.classList.add("card-body");

    var newMessageTitle = document.createElement("h5");
    newMessageTitle.classList.add("card-title");
    newMessageTitle.textContent = sender;

    var newMessageText = document.createElement("p");
    newMessageText.classList.add("card-text");
    newMessageText.textContent = text;

    newMessageBody.appendChild(newMessageTitle);
    newMessageBody.appendChild(newMessageText);
    newMessage.appendChild(newMessageBody);
    chatArea.insertBefore(newMessage, chatArea.querySelector(".input-group"));
}
