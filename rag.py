from pypdf import PdfReader
import chromadb

def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    return full_text 

def split_into_chunks(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def create_collection(chunks: list, collection_name: str = "pdf_chunks"):
    client = chromadb.Client()
    collection = client.create_collection(name=collection_name)
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )
    return collection

def search_collection(collection, query: str, n_results: int = 3) -> list:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]