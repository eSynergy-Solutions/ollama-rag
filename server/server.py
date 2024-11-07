from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from rag_app import RAGApplication
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

r_app = RAGApplication(urls=[])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class UrlsRequest(BaseModel):
    urls: List[str]

@app.post("/add_urls/", response_class=JSONResponse)
async def add_urls(request: UrlsRequest):
    try:
        r_app.add_urls(request.urls)
        return {"message": "URLs added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/", response_class=JSONResponse)
async def ask_question(request: QuestionRequest):
    try:
        response = r_app.run(request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6969)