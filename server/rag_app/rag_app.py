from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import SKLearnVectorStore
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
# Load environment variables from .env.local file
load_dotenv(dotenv_path='.env.local')

class RAGApplication:
    def __init__(self, urls: List[str]):
        self.embedding_model = os.getenv('OLLAMA_EMBEDDING_MODEL') or "nomic-embed-text:latest"
        self.llm_model = os.getenv('OLLAMA_RAG_LLM') or "llama3.2:1b"
        self.urls = urls
        self.ollama_embeddings = OllamaEmbeddings(model=self.embedding_model)
        self.vectorstore = SKLearnVectorStore(embedding=self.ollama_embeddings)
        
        # Load initial documents and set up retriever
        if len(urls) != 0:
            self.load_and_index_documents(urls)

        # Define the prompt template for the LLM
        prompt = PromptTemplate(
            template="""You are an assistant for question-answering tasks.
            Use the following documents to answer the question.
            If you don't know the answer, just say that you don't know.
            Use three sentences maximum and keep the answer concise:
            Question: {question}
            Documents: {documents}
            Answer:
            """,
            input_variables=["question", "documents"],
        )

        # Initialize the LLM with Llama 3.1 model
        llm = ChatOllama(model=self.llm_model, temperature=0)

        # Create a chain combining the prompt template and LLM
        self.rag_chain = prompt | llm | StrOutputParser()

    def load_and_index_documents(self, urls):
        """Load and index documents from a list of URLs."""
        # Load and split documents
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        # Initialize a text splitter
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )
        doc_splits = text_splitter.split_documents(docs_list)

        # Add documents to the vector store
        self.vectorstore.add_documents(doc_splits)

        # Set the retriever with the updated vector store
        self.retriever = self.vectorstore.as_retriever(k=4)

    def add_urls(self, new_urls):
        """Method to add new URLs, load documents, split, embed, and index them."""
        self.load_and_index_documents(new_urls)
        print(f"Added {len(new_urls)} new URLs to the RAG system.")

    def run(self, question):
        # Retrieve relevant documents
        documents = self.retriever.invoke(question)
        # Extract content from retrieved documents
        doc_texts = "\n".join([doc.page_content for doc in documents])
        # Get the answer from the language model
        answer = self.rag_chain.invoke({"question": question, "documents": doc_texts})
        return answer
    
    def run_stream(self, question):
        # Retrieve relevant documents
        documents = self.retriever.invoke(question)
        # Extract content from retrieved documents
        doc_texts = "\n".join([doc.page_content for doc in documents])
        # Get the answer from the language model
        for chunk in self.rag_chain.stream({"question": question, "documents": doc_texts}):
            yield chunk
