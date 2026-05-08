from langchain_chroma import Chroma
from models.embeddings import create_embeddings
from config import VECTOR_DB_PATH, COLLECTION_NAME


def get_or_create_vectorstore(documents=None):
    embeddings = create_embeddings()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTOR_DB_PATH,
    )

    if documents:
        print("Adding documents to vector store...")
        ids = vector_store.add_documents(documents)
        print(f"Added {len(ids)} document chunks.")

    return vector_store