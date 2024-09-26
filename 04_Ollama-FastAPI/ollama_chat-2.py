from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from typing import List, Dict

app = FastAPI()

class Query(BaseModel):
    prompt: str
    model: str = "llama2"

class Conversation(BaseModel):
    id: str
    messages: List[Dict[str, str]] = []

conversations: Dict[str, Conversation] = {}

@app.post("/generate")
async def generate_text(query: Query):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": query.model, "prompt": query.prompt}
        )
        response.raise_for_status()
        return {"generated_text": response.json()["response"]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

@app.get("/models")
async def list_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        return {"models": response.json()["models"]}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")

@app.post("/models/download")
async def download_model(model_name: str):
    try:
        response = requests.post(
            "http://localhost:11434/api/pull",
            json={"name": model_name}
        )
        response.raise_for_status()
        return {"message": f"Model {model_name} downloaded successfully"}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error downloading model: {str(e)}")

@app.post("/conversation/start")
async def start_conversation(conv_id: str):
    if conv_id in conversations:
        raise HTTPException(status_code=400, detail="Conversation ID already exists")
    conversations[conv_id] = Conversation(id=conv_id)
    return {"message": f"Conversation {conv_id} started"}

@app.post("/conversation/{conv_id}/message")
async def add_message(conv_id: str, query: Query):
    if conv_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation = conversations[conv_id]
    conversation.messages.append({"role": "user", "content": query.prompt})
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": query.model, "prompt": query.prompt}
        )
        response.raise_for_status()
        generated_text = response.json()["response"]
        conversation.messages.append({"role": "assistant", "content": generated_text})
        return {"generated_text": generated_text}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

@app.get("/conversation/{conv_id}")
async def get_conversation(conv_id: str):
    if conv_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversations[conv_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)