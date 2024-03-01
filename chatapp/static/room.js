const chatLog = document.querySelector('#chat-log');
const roomName = JSON.parse(document.getElementById('room_name').textContent);

function scrollToBottom() {
    let objDiv = document.getElementById("chat-log");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollToBottom();

if (chatLog.childNodes.length <= 1 ) {
    const emptyText = document.createElement('h3')

    emptyText.id = 'emptyText'
    emptyText.innerText = 'No Messages'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    const messageElement = document.createElement('div')

    const userId = data['user_id']
    const userName = data['user_name']

    const loggedInUserID = JSON.parse(document.getElementById('user_id').textContent)

    messageElement.innerHTML = `${userName}: ${data.message}`

    if (userId === loggedInUserID) {
        messageElement.classList.add('message', 'sender')
    } else {
        messageElement.classList.add('message', 'receiver')
    }

    chatLog.appendChild(messageElement)

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }

    scrollToBottom();
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};