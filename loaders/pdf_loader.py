import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import PDF_PATHS, CHUNK_SIZE, CHUNK_OVERLAP

def load_and_split_pdfs():
    docs = []
    for path in PDF_PATHS:
        if os.path.exists(path):
            print(f"Loading PDF: {path}")
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        else:
            print(f"Warning: {path} not found!")

    if not docs:
        raise FileNotFoundError("No valid PDFs loaded.")

    print(f"📄 加载了 {len(docs)} 个文档")
    if docs:
        print("前100字符:", docs[0].page_content[:100])

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )
    splits = text_splitter.split_documents(docs)
    print(f"Split into {len(splits)} chunks.")
    return splits