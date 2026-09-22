from fastapi import FastAPI,Request
from app.schemas import ChatRequest,EmbeddingRequest,BatchChatRequest
from app.services import generate_chat_answer,generate_embedding,generate_batch_chat_answers

app = FastAPI()
@app.get("/health")
async def health():
    return {"status":"ok"}

@app.post("/chat")
async def chat(request:ChatRequest):
    data = request.message
    result = generate_chat_answer(data)
    return {"answer":result}
@app.post("/batch_chat")
async def batch_chat(request:BatchChatRequest):
    data = request.messages
    result = generate_batch_chat_answers(data)
    return {"answers":result}

@app.post("/embedding")
async def embedding(request:EmbeddingRequest):
    response = request.text
    result = generate_embedding(response)
    return {"embedding": result}