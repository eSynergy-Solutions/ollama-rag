from fastapi import APIRouter
from pydantic import BaseModel, model_validator, ValidationError
from typing import List
import json
import os

router = APIRouter()

CHAT_HISTORY_FILE = 'server/chat_history/chat_history.json'

class ChatEntryQuestion(BaseModel):
    question: str

class ChatEntryResponse(BaseModel):
    response: str

class ChatEntry(BaseModel):
    question: str | None = None  # Optional field for "question"
    response: str | None = None  # Optional field for "response"

    @model_validator(mode="before")
    def validate_fields(cls, values):
        question = values.get("question")
        response = values.get("response")

        # Ensure only one of "question" or "response" is provided
        if (question and response) or (not question and not response):
            raise ValueError("You must provide either 'question' or 'response', but not both.")

        return values
    
    class Config:
        from_attributes = True

@router.get("/chat_history", response_model=List[ChatEntryQuestion | ChatEntryResponse])
async def get_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []

    with open(CHAT_HISTORY_FILE, 'r') as file:
        chat_history_data = json.load(file)

    # Validate and sanitize chat history entries
    chat_history = []
    for entry in chat_history_data:
        try:
            validated_entry = ChatEntry(**entry).model_dump(exclude_none=True)
            chat_history.append(validated_entry)
        except ValidationError as e:
            # Log or handle invalid entries
            print(f"Invalid chat entry skipped: {e}")

    return chat_history


@router.post("/chat_history", response_model=List[ChatEntry])
async def post_chat_message(chat_message: ChatEntry | dict):
    # Ensure `chat_message` is a `ChatEntry` instance
    if isinstance(chat_message, dict):
        chat_message = ChatEntry(**chat_message)

    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as file:
            chat_history = json.load(file)
    else:
        chat_history = []

    chat_history.append(chat_message.model_dump(exclude_none=True))  # Now this will work
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(chat_history, file, indent=4)
    return
