const chatBox = document.getElementById('chat-box');
const input = document.getElementById('chat-input');

const socket = new WebSocket('ws://localhost:8000/ws');

socket.addEventListener('open', () => {
  console.log('Connected to WebSocket server');
});

socket.addEventListener('message', (event) => {
  addMessage(event.data, 'bot');
});

function sendMessage() {
  const text = input.value.trim();
  if (text === '' || socket.readyState !== WebSocket.OPEN) return;

  addMessage(text, 'user');
  socket.send(text);
  input.value = '';
}

function addMessage(text, sender) {
  const msg = document.createElement('div');
  msg.className = 'message ' + sender;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
}