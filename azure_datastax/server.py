from chat import ChatApp
from fastapi import FastAPI


app = FastAPI()
chat_app = ChatApp()
chatbot = chat_app.init_chatbot()


@app.post("/")
def read_root():
    return {"message": "Hello world from Chat Server."}


@app.post("/ask")
def ask_chatbot(question):
    chatbot_response = chat_app.get_response(chatbot, question)
    return {"response": chatbot_response}
