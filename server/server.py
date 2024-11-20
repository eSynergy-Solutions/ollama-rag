from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes import chat_history, chat_with_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_history.router)
app.include_router(chat_with_model.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6969)