function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatBox = document.getElementById("chat-box");

    // Append user message
    chatBox.innerHTML += `<div class="user-message">${userInput}</div>`;

    // Fetch response from the server
    fetch("/get_data", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `user_input=${encodeURIComponent(userInput)}`
    })
        .then(response => response.json())
        .then(data => {
            // Append bot response
            chatBox.innerHTML += `<div class="bot-message">${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
        });

    // Clear input field
    document.getElementById("user-input").value = "";
}
