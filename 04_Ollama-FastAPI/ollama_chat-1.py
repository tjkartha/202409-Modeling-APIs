from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class Query(BaseModel):
    prompt: str
    model: str = "tinyllama"

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

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)