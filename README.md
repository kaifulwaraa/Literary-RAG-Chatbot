# 📖 Literary RAG Chatbot

An offline Retrieval-Augmented Generation (RAG) chatbot that lets you query and reason over any PDF document — research papers, legal files, internal reports, or corporate manuals — with zero internet dependency.

Uses *The Forty Rules of Love* by Elif Shafak as a demo, but the real use case is querying **sensitive documents that should never leave your machine**.

---

## 🧠 Architecture
PDF Novel
↓
pypdf (text extraction)
↓
ChromaDB (vector storage + semantic search)
↓
Mistral 7B via llama.cpp (local LLM, no API)
↓
Streamlit UI (chat interface)

---

## ✨ Features

- **100% offline** — no OpenAI, no API keys, no internet required
- **Upload any PDF novel** via the sidebar
- **Two reasoning modes** auto-detected from your question:
  - **Fact retrieval** — "Who is Shams of Tabriz?"
  - **What-if reasoning** — "What if Shams had never met Rumi?"
- **Persistent chat history** within a session
- **ChromaDB vector search** for semantically relevant context

---

## 🗂️ Project Structure
literary_chatbot/
├── app.py              ← Streamlit app + RAG pipeline
├── ingest.py           ← Indexes the default novel into ChromaDB
├── requirements.txt    ← Dependencies
├── .gitignore
├── models/
│   └── mistral-7b-instruct-v0.2.Q4_K_M.gguf   ← Local LLM (not in repo)
├── data/
│   └── 40_Rules_of_Love.pdf                    ← Default novel (not in repo)
└── db/                 ← ChromaDB vector database (not in repo)

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/kaifulwaraa/Literary-RAG-Chatbot.git
cd Literary-RAG-Chatbot
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate.bat

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the Mistral model
Download [`mistral-7b-instruct-v0.2.Q4_K_M.gguf`](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF) and place it in the `models/` folder.

### 5. Add your novel
Place any PDF in the `data/` folder, then run:
```bash
python ingest.py
```

---

## 🚀 Run the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💬 Demo Questions

| Question | Mode |
|---|---|
| "What are the 40 rules of love?" | Fact retrieval |
| "Who is Shams of Tabriz?" | Fact retrieval |
| "What if Shams had never met Rumi?" | What-if reasoning |
| "What would have happened if Ella stayed with her husband?" | What-if reasoning |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Mistral 7B Instruct (Q4_K_M) |
| LLM Runtime | llama-cpp-python |
| Vector Database | ChromaDB |
| Embeddings | all-MiniLM-L6-v2 (SentenceTransformers) |
| PDF Parsing | pypdf |
| UI | Streamlit |

---

## 🔒 Why Offline?

Built for environments where data privacy matters — research papers, legal documents, internal reports, corporate manuals, or any sensitive PDF you wouldn't want sent to a cloud API.

The novel (*40 Rules of Love*) is used purely as a demo to showcase the RAG pipeline. The real value is that **any confidential document stays entirely on your machine** — no OpenAI, no cloud logging, no internet required after setup.

## 📸 Demo

**What-If Reasoning Mode**
![What-If Reasoning](ss%202.JPG)

**Fact Retrieval Mode**
![Fact Retrieval](literary%20chatbot%20ss.JPG)

## 👤 Author

**Kaiful Waraa**  
[GitHub](https://github.com/kaifulwaraa)