const WebSocket = require('ws');

const port = 8080 

const wss = new WebSocket.Server({ port: port});

wss.on('connection', function connection(ws) {
  console.log('A client connected');

  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
    // Echo the message back with a prefix
    ws.send('Bot reply: You said "' + message + '"');
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

console.log(`WebSocket server running on ws://localhost:${port}`);