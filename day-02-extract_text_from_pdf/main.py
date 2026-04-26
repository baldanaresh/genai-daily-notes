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

def main():
    filepath="sample.pdf"    
    print("your pdf :")
    text=extract_text_from_pdf(file_path=filepath)
    print("your text is: \n ")
    print(text[:1000])

if __name__ == "__main__":
    main()