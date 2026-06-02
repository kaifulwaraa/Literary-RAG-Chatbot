import os
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader


# Load your novel
pdf_path = "data/40_Rules_of_Love.pdf"
reader = PdfReader(pdf_path)

text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# Split into chunks
chunk_size = 500
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Initialize Chroma
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_or_create_collection(
    "novel",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
)

# Add chunks
for i, chunk in enumerate(chunks):
    collection.add(documents=[chunk], ids=[str(i)])

print("✅ Ingest complete. Stored", len(chunks), "chunks.")
