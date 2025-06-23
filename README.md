# AI Chat Application

This project is a simple full-stack AI chat application featuring a FastAPI backend with WebSocket support and a modern frontend UI. The backend uses the Groq API to generate AI responses in real time.

## Features
- **Real-time chat**: Communicate instantly with the AI assistant using WebSockets.
- **FastAPI backend**: Handles WebSocket connections and integrates with the Groq API for AI-powered responses.
- **Modern frontend**: Clean, responsive chat interface built with HTML, CSS, and JavaScript.

## Project Structure
- `main.py` — FastAPI server with WebSocket endpoint and Groq API integration.
- `app.js` — Frontend JavaScript for WebSocket communication and chat UI logic.
- `index.html` — Main HTML file for the chat interface.
- `style.css` — Styles for the chat UI.
- `package.json` — Node.js dependencies (for WebSocket support if needed).

## Setup Instructions

### Backend (Python)
1. Install dependencies:
   ```sh
   pip install fastapi uvicorn python-dotenv groq
   ```
2. Set your Groq API key in a `.env` file:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
3. Start the FastAPI server:
   ```sh
   python main.py
   ```

### Frontend
1. Open `index.html` in your browser.
2. The chat UI will connect to the backend WebSocket at `ws://localhost:8000/ws`.

## Customization
- Update the frontend styles in `style.css` as desired.
- Modify the backend logic in `main.py` to change AI behavior or add features.

## License
MIT

---

## Getting Started Guide (For Beginners)

Follow these simple steps to run your own AI chat application:

### 1. Install Python
- Download and install Python from [python.org](https://www.python.org/downloads/).

### 2. Install Required Python Packages
- Open a terminal (Command Prompt or PowerShell on Windows).
- Type the following command and press Enter:
  ```sh
  pip install fastapi uvicorn python-dotenv groq
  ```

### 3. Set Up Your API Key
- Create a new file named `.env` in the project folder.
- Add this line to the file (replace `your_api_key_here` with your actual Groq API key):
  ```env
  GROQ_API_KEY=your_api_key_here
  ```

### 4. Start the Chat Server
- In the terminal, run:
  ```sh
  python main.py
  ```
- The server will start and listen for chat connections.

### 5. Open the Chat Interface
- Double-click `index.html` or open it in your web browser.
- Type a message and click "Send" to chat with the AI.

### Troubleshooting
- If you see errors, make sure you installed all packages and entered your API key correctly.
- The server must be running before you open the chat page.

You’re ready to chat with your AI assistant!

---

## Step-by-Step Guide: Building the AI Chat Application from Scratch

Follow these steps to create the program using all files in this folder:

### 1. Create the Project Folder
- Make a new folder for your project (e.g., `AIChatApp`).

### 2. Create the Backend (Python)
#### a. `main.py`
- Create a file named `main.py`.
- Add the FastAPI server code that:
  - Sets up a WebSocket endpoint (`/ws`).
  - Connects to the Groq API for AI responses.
  - Handles incoming and outgoing chat messages.

#### b. `.env`
- Create a file named `.env`.
- Add your Groq API key:
  ```env
  GROQ_API_KEY=your_api_key_here
  ```

#### c. Install Python Packages
- In your terminal, run:
  ```sh
  pip install fastapi uvicorn python-dotenv groq
  ```

### 3. Create the Frontend
#### a. `index.html`
- Create a file named `index.html`.
- Add the HTML structure for the chat interface, including:
  - A container for chat messages.
  - An input box and send button.
  - A script tag to include your JavaScript file.

#### b. `style.css`
- Create a file named `style.css`.
- Add CSS to style the chat interface (centered box, message bubbles, etc.).

#### c. `app.js`
- Create a file named `app.js`.
- Add JavaScript to:
  - Connect to the backend WebSocket (`ws://localhost:8000/ws`).
  - Send user messages and display responses.
  - Update the chat UI dynamically.

### 4. (Optional) Node.js WebSocket Support
#### a. `package.json`
- Create a file named `package.json` if you want to use Node.js WebSocket utilities.
- Add the following:
  ```json
  {
    "dependencies": {
      "ws": "^8.18.2"
    }
  }
  ```
- Install dependencies (optional):
  ```sh
  npm install
  ```

### 5. Run the Application
- Start the backend server:
  ```sh
  python main.py
  ```
- Open `index.html` in your web browser.
- Start chatting with the AI assistant!

---

This guide walks you through creating each file and setting up the environment to build the full AI chat application from scratch.
