from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from rag_app.rag_app import RAGApplication
from routes.chat_history import post_chat_message

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class ServerChatResponse(BaseModel):
    response: str

class UrlsRequest(BaseModel):
    urls: List[str]

r_app = RAGApplication(urls=[])

@router.post("/add_urls/", response_class=JSONResponse)
async def add_urls(request: UrlsRequest):
    try:
        r_app.add_urls(request.urls)
        return {"message": "URLs added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask/", response_class=JSONResponse, response_model=ServerChatResponse)
async def ask_question(request: QuestionRequest):
    try:
        await post_chat_message(request)
        rag_response = r_app.run(request.question)
        await post_chat_message({"response": rag_response})
        return {"response": rag_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))