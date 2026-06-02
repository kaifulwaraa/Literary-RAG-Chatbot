# app.py
import re
import streamlit as st
from llama_cpp import Llama
import chromadb
from chromadb.utils import embedding_functions

# -----------------------------
# Load your LLM (offline)
# -----------------------------
llm = Llama(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_threads=8,
    n_ctx=4096,
    n_gpu_layers=0
)

# -----------------------------
# Load ChromaDB
# -----------------------------
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_collection("novel")

# -----------------------------
# Prompt templates
# -----------------------------
FACT_PROMPT = """
You are a precise literary assistant. Answer the question using ONLY the text from the novel below. Be concise and specific.
If the answer is not in the text, respond: "Not mentioned in the novel".
Do not repeat the question. Do not add outside knowledge.

Context:
{context}

Question:
{question}

Answer (be concise):
"""

WHATIF_PROMPT = """
You are an intelligent reasoning assistant. Based on the following context from the novel, answer the question by reasoning about alternative possibilities. 
- Use the information in the context as the foundation. 
- If the question asks "what if", analyze plausible outcomes based on the events, characters, and strategies described. 
- Keep the answer consistent with the novel's world.

Answer step by step, considering the events and characters. Then conclude with the most likely outcome.

Context:
{context}

Question:
{question}

Answer:
"""

# -----------------------------
# Ingest uploaded PDF
# -----------------------------
def ingest_pdf(uploaded_file):
    from pypdf import PdfReader
    import io

    reader = PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    chunk_size = 1000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    collection_name = re.sub(r'[^a-zA-Z0-9._-]', '_', uploaded_file.name.replace(".pdf", ""))[:50]
    collection_name = re.sub(r'^[^a-zA-Z0-9]+', '', collection_name)
    collection_name = re.sub(r'[^a-zA-Z0-9]+$', '', collection_name)
    if len(collection_name) < 3:
        collection_name = "uploaded_book"

    new_collection = chroma_client.get_or_create_collection(
        collection_name,
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    )

    for i, chunk in enumerate(chunks):
        new_collection.add(documents=[chunk], ids=[str(i)])

    return new_collection, len(chunks)

# -----------------------------
# Generate answer
# -----------------------------
def generate_answer(query, active_collection):
    results = active_collection.query(query_texts=[query], n_results=5)
    context = "\n".join(results["documents"][0])

    query_lower = query.lower()
    if any(kw in query_lower for kw in ["what if", "could have", "would have", "instead"]):
        prompt = WHATIF_PROMPT.format(context=context, question=query)
    else:
        prompt = FACT_PROMPT.format(context=context, question=query)

    output = llm(
        prompt,
        max_tokens=512,
        temperature=0.7,
        repeat_penalty=1.2
    )
    return output['choices'][0]['text'].strip()

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📖 Novel Reasoning Chatbot (Offline)")

with st.sidebar:
    st.header("📂 Upload a Book")
    uploaded_file = st.file_uploader("Upload a PDF novel", type="pdf")

    if uploaded_file:
        if st.button("Load Book"):
            with st.spinner("Reading and indexing your book..."):
                new_collection, num_chunks = ingest_pdf(uploaded_file)
                st.session_state.collection = new_collection
                st.session_state.messages = []
            st.success(f"✅ Loaded {num_chunks} chunks from {uploaded_file.name}")

    st.markdown("---")
    if "collection" in st.session_state:
        st.info(f"📖 Active book: {st.session_state.collection.name}")
    else:
        st.info("📖 Active book: 40 Rules of Love (default)")

active_collection = st.session_state.get("collection", collection)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

query = st.chat_input("Ask a question about the novel...")

if query:
    with st.chat_message("user"):
        st.write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = generate_answer(query, active_collection)
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})