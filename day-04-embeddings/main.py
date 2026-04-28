import os
from pypdf import PdfReader
from google.genai import Client 
from dotenv import load_dotenv

load_dotenv()

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

def get_embeddings(chunks):
    client = Client(api_key=os.getenv("GEMINI_API_KEY"))
    
  
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=chunks
    )
    
    # 3. Extract the values from every embedding in the response
    return [e.values for e in response.embeddings]

def main():
    file_path = "sample.pdf"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    
    if not chunks:
        print("No text extracted.")
        return

    embeddings = get_embeddings(chunks)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} vectors.")
        print(f"Vector size: {len(embeddings[0])}")

if __name__ == "__main__":
    main()