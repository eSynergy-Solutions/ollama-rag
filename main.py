import rag_app

rag_application = rag_app.RAGApplication(retriever=rag_app.retriever, rag_chain=rag_app.rag_chain)

# Example usage
question = "What is prompt engineering"
answer = rag_application.run(question)
print("Question:", question)
print("Answer:", answer)