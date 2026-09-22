from pydantic import BaseModel
class ChatRequest(BaseModel):
    message:str
class EmbeddingRequest(BaseModel):
    text:str
class BatchChatRequest(BaseModel):
    messages:list[str]