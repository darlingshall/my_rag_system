# 文件: loaders/pdf_loader.py (或你当前的文件)
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import PDF_PATHS, CHUNK_SIZE, CHUNK_OVERLAP
import hashlib  # 可选：用于更健壮的 ID 生成

def generate_chunk_id(doc):
    """为每个 chunk 生成唯一 ID"""
    source = doc.metadata.get("source", "unknown")
    start_index = doc.metadata.get("start_index", 0)
    # 方法1：简单拼接（够用）
    # return f"{os.path.basename(source)}_{start_index}"

    # 方法2（更健壮）：用内容哈希（防止同一位置内容变了但 ID 不变）
    content_hash = hashlib.md5(doc.page_content.encode()).hexdigest()[:8]
    return f"{os.path.basename(source)}_{start_index}_{content_hash}"


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

    # 👇 新增：为每个 split 生成唯一 ID
    ids = [generate_chunk_id(split) for split in splits]

    return splits, ids  # 👈 同时返回 splits 和 ids

# ################################################################################
'''
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
'''