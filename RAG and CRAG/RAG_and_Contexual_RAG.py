
import ollama
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

# Print only the model's response content
print(response.message.content)

