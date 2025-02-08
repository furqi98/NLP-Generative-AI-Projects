## PDF Q&A Assistant with RAG & CRAG

### 📌 Overview  
This project demonstrates a **PDF Q&A Assistant** powered by **Retrieval-Augmented Generation (RAG)** and **Contextual RAG (CRAG)**, using **LangChain**, **Ollama** hosted **Llama 3.2**. The application runs on **Streamlit**, allowing users to easily upload PDF documents and ask questions, receiving context-aware AI-generated answers.

### 🎥 Watch the Demo  
Check out the demo video to see how the PDF Q&A Assistant works:  

[![Watch the Demo](https://img.youtube.com/vi/YksOKFDVaT8/0.jpg)](https://youtu.be/YksOKFDVaT8)

### 📥 Installation & Setup  

#### Prerequisites  
1. Create a virtual environment:  
   ```bash
   python -m venv env
   source env/bin/activate  # On MacOS/Linux
   env\Scripts\activate  # On Windows
   ```  
2. Create a `.env` file and add your OpenAI API key:  
   ```
   OPENAI_API_KEY=your_api_key_here
   ```  
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

#### Running the Application  
Start the Streamlit app by running:  
```bash
streamlit run RAG.py
```


### 🚀 Features  
- **PDF Upload**: Easily upload PDF documents.  
- **Context-Aware Q&A**: Ask any question, and get precise answers based on the PDF content.  
- **Streamlit Interface**: A simple and user-friendly interface to interact with the assistant.  
- **Powered by RAG & CRAG**: Leverage the power of **Retrieval-Augmented Generation** and **Contextual RAG** for accurate, context-driven responses.

### 🛠️ Technologies Used  
- `LangChain` – For chaining together document retrieval and generation tasks.  
- `Ollama` – For locally hosting Llama 3.2 model  
- `Llama 3.2` – Open source AI model.  
- `Streamlit` – For building the interactive web interface.  

### 🤝 Contributing  
Contributions are welcome! You can:
- Improve the document retrieval and answer generation process.
- Replace Llama 3.2 with other models for testing and performance improvement.


