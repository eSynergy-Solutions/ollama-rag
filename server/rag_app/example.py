import rag_app as rag_app
import time

start_time = time.time()

# Example usage
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

new_urls = ["https://stackoverflow.com/questions/31778413/run-javascript-in-visual-studio-code"]

app = rag_app.RAGApplication(urls)
response = app.run("What is prompt engineering?")
print(map(response, lambda x: x['answer']))

app.add_urls(new_urls)
response = app.run("How to run JavaScript in Visual Studio Code?")
print(response)

print("Time taken: ", time.time() - start_time)