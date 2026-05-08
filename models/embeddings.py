from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_DIR

def create_embeddings():
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_DIR)
    print("Embedding model ready.")
    return embeddings