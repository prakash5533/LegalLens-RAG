import os
import fitz  # PyMuPDF
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DOCS_DIR = os.path.join(BASE_DIR, "media", "knowledge_base_raw")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

def extract_clean_legal_text(pdf_path):3.
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))
        for b in blocks:
            text = b[4].strip()
            if text and not text.startswith("Page ") and len(text) > 10:
                full_text += text + "\n"
    return full_text

def chunk_text(text, max_chunk_size=900, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks

def run_ingestion():
    os.makedirs(CHROMA_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    collection = client.get_or_create_collection(
        name="legal_knowledge_base",
        embedding_function=embed_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    if not os.path.exists(RAW_DOCS_DIR):
        print(f"Directory {RAW_DOCS_DIR} does not exist.")
        return

    files = [f for f in os.listdir(RAW_DOCS_DIR) if f.endswith(".pdf")]
    print(f"Found {len(files)} Acts ready for indexing.")

    doc_counter = 0
    for filename in files:
        act_name = filename.replace(".pdf", "").replace("_", " ").title()
        pdf_path = os.path.join(RAW_DOCS_DIR, filename)
        
        print(f"Extracting: {act_name}...")
        extracted_text = extract_clean_legal_text(pdf_path)
        chunks = chunk_text(extracted_text)
        
        ids, documents, metadatas = [], [], []
        for idx, chunk in enumerate(chunks):
            doc_counter += 1
            ids.append(f"act_chunk_{doc_counter}")
            documents.append(chunk)
            metadatas.append({
                "act_name": act_name,
                "source_file": filename,
                "chunk_index": idx
            })

        batch_size = 100
        for i in range(0, len(ids), batch_size):
            collection.add(
                ids=ids[i:i+batch_size],
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size]
            )
        print(f"Indexed {len(ids)} chunks for {act_name}.")

    print("Module 1 complete: Knowledge base indexed in ChromaDB.")

if __name__ == "__main__":
    run_ingestion()