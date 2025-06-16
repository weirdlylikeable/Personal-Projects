from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os
from dotenv import load_dotenv
from groq import Groq
import logging
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Create FastAPI app
app = FastAPI()

# Groq response function
async def get_groq_response(user_input: str) -> str:
    try:
        logger.info(f"Sending input to Groq: {user_input}")
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            stream=False,
        )
        reply = response.choices[0].message.content
        logger.info(f"Groq reply: {reply}")
        return reply
    except Exception as e:
        logger.error(f"Groq API error: {str(e)}")
        return f"Error: {str(e)}"

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_ip = websocket.client.host
    logger.info(f"Client connected: {client_ip}")

    try:
        while True:
            message = await websocket.receive_text()
            logger.info(f"Received message: {message}")
            reply = await get_groq_response(message)
            await websocket.send_text(reply)
    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {client_ip}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

# Run with: python main.py
if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
