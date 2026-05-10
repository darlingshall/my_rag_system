from langchain_chroma import Chroma
from models.embeddings import create_embeddings
from loaders.pdf_loader import load_and_split_pdfs
from config import VECTOR_DB_PATH, COLLECTION_NAME


def get_or_create_vectorstore(documents=None):
    embeddings = create_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTOR_DB_PATH,
    )
def update_vectorstore_with_pdfs():
    """加载 PDF 并安全地追加到向量库（自动去重）"""
    documents, doc_ids = load_and_split_pdfs()
    vector_store = get_or_create_vectorstore()

    existing_ids = set(vector_store.get()["ids"])
    print(f"Already have {len(existing_ids)} chunks in DB.")

    new_docs = []
    new_ids = []
    for doc, did in zip(documents, doc_ids):
        if did not in existing_ids:
            new_docs.append(doc)
            new_ids.append(did)

    if new_docs:
        print(f"Adding {len(new_docs)} new chunks...")
        vector_store.add_documents(documents=new_docs, ids=new_ids)
    else:
        print("No new documents to add.")

    return vector_store