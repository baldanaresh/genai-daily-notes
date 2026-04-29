import faiss
import numpy as np
import os
from pypdf import PdfReader
from google.genai import Client 
from dotenv import load_dotenv

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'
    return text  

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            while end < len(text) and text[end] not in [".", "\n"]:
                end += 1
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def embed_query(query):
    client = Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=[query]   # must be a list
    )

    return response.embeddings[0].values

def get_embeddings(chunks):
    client = Client(api_key=os.getenv("GEMINI_API_KEY"))
    
#    the support mode is models/gemini-embedding-001
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=chunks
    )
    
    # 3. Extract the values from every embedding in the response
    return [e.values for e in response.embeddings]

def build_faiss_index(embeddings):
    dimension = len(embeddings[0])  # e.g., 768

    index = faiss.IndexFlatL2(dimension)

    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)

    return index
    
def search(index, query_embedding, chunks, k=3):
    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = []
    for i in indices[0]:
        results.append(chunks[i])

    return results

def main():
    load_dotenv()
    
    file_path = "sample.pdf"

    # Step 1: Extract + chunk
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    # Step 2: Embed chunks
    embeddings = get_embeddings(chunks)

    # Step 3: Build FAISS index
    index = build_faiss_index(embeddings)

    print("Semantic search ready!\n")

    while True:
        query = input("Ask: ")

        if query.lower() in ["exit", "quit"]:
            break

        query_embedding = embed_query(query)

        results = search(index, query_embedding, chunks)

        print("\nTop results:\n")
        for i, res in enumerate(results):
            print(f"--- Result {i+1} ---")
            print(res[:300])
            print()    

if __name__ == "__main__":
    main()            