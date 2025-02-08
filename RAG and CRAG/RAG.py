import os
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from io import BytesIO
import json

# Load environment variables from .env
load_dotenv()

# Initialize embeddings and vector store setup
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
persistent_directory = "db/furqichroma_db"  # Change this as needed

# Initialize chat history (for the session)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to process the uploaded PDF file
def process_uploaded_file(uploaded_file):
    # Save the uploaded file to a temporary location
    temp_file_path = "temp_uploaded_file.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
    
    # Create a PDF loader with the saved file
    loader = PyPDFLoader(temp_file_path)
    documents = loader.load_and_split()
    
    # Create a vector store from the document
    db = Chroma.from_documents(documents, embeddings, persist_directory=persistent_directory)
    
    # Clean up the temporary file
    os.remove(temp_file_path)
    
    return db, documents

# Function to get contextual chat history for CRAG
def get_contextual_history():
    # Use the last N interactions as context (adjust the number of messages as needed)
    max_history_length = 3  # Use the last 3 messages (can adjust based on requirements)
    context = "\n".join([msg['content'] for msg in st.session_state.chat_history[-max_history_length:]])
    return context

# CRAG implementation (Contextualized Retrieval-Augmented Generation)
def crag_implementation(query, documents):
    # Get contextual history
    context = get_contextual_history()

    # Combine the query with the historical context
    combined_input = f"Context from previous conversations:\n{context}\n\nCurrent query: {query}\n\nRelevant Documents:\n" + "\n\n".join([doc.page_content for doc in documents])

    # Create a ChatOpenAI model (use the CRAG context)
    model = ChatOpenAI(model="gpt-4o")

    # Define the messages for the model
    messages = [
        SystemMessage(content="You are a helpful assistant using CRAG to process contextual information."),
        HumanMessage(content=combined_input),
    ]

    # Invoke the model with the combined input
    result = model.invoke(messages)
    return result.content

# Streamlit app
st.title("PDF Query Answering System")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# If a file is uploaded, process the file and allow the user to ask questions
if uploaded_file is not None:
    # Process the uploaded file
    db, documents = process_uploaded_file(uploaded_file)

    st.subheader("Document loaded successfully!")
    st.write(f"Number of document chunks: {len(documents)}")

    # User choice: Similarity Search or CRAG
    choice = st.radio("Choose the retrieval method:", ("Similarity Search RAG", "CRAG"))

    # User input for query
    query = st.text_input("Please enter your query:")

    if query:
        # Store user query and display chat history only for CRAG
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        # Display chat history only if CRAG is selected
        if choice == "CRAG":
            st.write("Chat History:")
            for idx, msg in enumerate(st.session_state.chat_history, 1):
                st.write(f"{idx}. {msg['role'].capitalize()}: {msg['content']}")

        if choice == "Similarity Search RAG":
            # Simple RAG: perform similarity search
            retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
            relevant_docs = retriever.invoke(query)

            # Combine the query and the relevant document contents
            combined_input = (
                "Here are some documents that might help answer the question: "
                + query
                + "\n\nRelevant Documents:\n"
                + "\n\n".join([doc.page_content for doc in relevant_docs])
                + "\n\nPlease provide an answer based only on the provided documents. If the answer is not found in the documents, respond with 'I'm not sure'."
            )

            # Create a ChatOpenAI model
            model = ChatOpenAI(model="gpt-4o")

            # Define the messages for the model
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=combined_input),
            ]

            # Invoke the model with the combined input
            result = model.invoke(messages)

            # Store the assistant's response in chat history
            st.session_state.chat_history.append({"role": "assistant", "content": result.content})

            # Display the result
            st.subheader("Answer:")
            st.write(result.content)

        elif choice == "CRAG":
            # CRAG implementation
            crag_result = crag_implementation(query, documents)

            # Store the assistant's response in chat history
            st.session_state.chat_history.append({"role": "assistant", "content": crag_result})

            # Display the CRAG result
            st.subheader("Answer (CRAG):")
            st.write(crag_result)

else:
    st.write("Please upload a PDF file to get started.")
