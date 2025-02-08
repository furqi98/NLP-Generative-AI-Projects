## OpenAI-Based YouTube Assistant  

### 📌 Overview  
OpenAI-Based YouTube Assistant is a Streamlit web application that allows users to ask questions about a YouTube video by providing its URL. The backend uses OpenAI's language model to process and generate answers based on the video transcript.  

### 🚀 Features  
- Extracts transcript from a YouTube video  
- Answers user queries about the video content  
- Simple and interactive Streamlit frontend  
- Fast retrieval of relevant video sections using FAISS  

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
streamlit run main.py
```
[![Watch the Demo]![YouTube Assistant](Youtube%20assistant.png)
](https://youtu.be/_x-Bpli6mNs)



### 🎯 Usage  
1. Enter the YouTube video URL.  
2. Ask a question related to the video content.  
3. Click on the **Submit** button.  
4. Get an AI-generated answer based on the video transcript.  

### 🛠️ Technologies Used  
- `python-dotenv` – For environment variable management  
- `langchain` – For processing text data  
- `openai` – For generating responses  
- `youtube-transcript-api` – For extracting video transcripts  
- `faiss-cpu` – For efficient text search and retrieval  
- `streamlit` – For building the frontend  

### 🤝 Contributing  
Contributions are welcome! You can enhance the project by:  
- Replacing OpenAI’s model with open-source alternatives like **Llama 3.2**  
- Improving transcript processing and retrieval efficiency  

