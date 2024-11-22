import os
import json
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from tqdm import tqdm
from langchain.chains import RetrievalQA

import langchain
langchain.verbose = False

from dotenv import load_dotenv
load_dotenv(".env")



class ChatApp:
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        verbose=False,
        temperature=0.3,
    )
    embedding = AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_EMB_ENDPOINT"),
        openai_api_key=os.getenv("AZURE_OPENAI_EMB_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_EMB_API_VERSION"),
    )

    def get_vstore(self, collection_name):
        vstore = AstraDBVectorStore(
            collection_name=collection_name,
            embedding=ChatApp.embedding,
            token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
            api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
            namespace="defra_chatbot_keyspace",
        )
        return vstore

    def load_documents(self, collection_name):
        vstore = self.get_vstore(collection_name)
        jsons = os.listdir("./docs")
        for jfile in tqdm(jsons):
            with open(f"./docs/" + jfile, "rt") as file:
                jobj = json.loads(file.read())
                metadata = {"url": jobj["url"]}
                docs = []
                for i, chunk in enumerate(jobj["chunks"]):
                    metadata["chunk_order"] = i
                    doc = Document(page_content=chunk, metadata=metadata)
                    docs.append(doc)
                vstore.add_documents(docs)

    def init_chatbot(self):
        vstore = self.get_vstore("funding_for_farmers")
        retriever = vstore.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=ChatApp.llm, retriever=retriever)
        return qa_chain

    def get_response(self, chatbot, user_input):
        return chatbot.invoke(user_input)["result"]
