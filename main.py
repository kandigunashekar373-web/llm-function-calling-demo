from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.assistant import FunctionCallingAssistant

app = FastAPI(title="LLM Function Calling Demo", version="1.0.0")

assistant = None

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.on_event("startup")
def startup():
    global assistant
    try:
        assistant = FunctionCallingAssistant()
    except RuntimeError:
        assistant = None

@app.get("/")
def home():
    return {"project": "LLM Function Calling Demo", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "openai_configured": "yes" if assistant else "no"}

@app.post("/chat")
def chat(request: ChatRequest):
    if assistant is None:
        raise HTTPException(status_code=503, detail="Add OPENAI_API_KEY to .env and restart.")
    return assistant.chat(request.session_id, request.message)
