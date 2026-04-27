from pypdf import PdfReader
from pypdf.errors import PdfReadError

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text=""
    for page_num,page in enumerate(reader.pages):
        page_text=page.extract_text()
        if page_text:
            text+=page_text +'\n'
    return text  

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
         # Try not to cut in middle of sentence
        if end < len(text):
            while end < len(text) and text[end] not in [".", "\n"]:
                end += 1
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap  # move with overlap

    return chunks

def main():
    file_path = "sample.pdf"
    print("hello")
    text = extract_text_from_pdf(file_path)

    chunks = chunk_text(text)

    print(f"Total chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:3]):  # preview first 3
        print(f"--- Chunk {i} ---")
        print(chunk)
        print("\n")

if __name__ == "__main__":
    main()