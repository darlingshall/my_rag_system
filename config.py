import os

# LangSmith tracing (optional)
os.environ["LANGCHAIN_PROJECT"] = "my-rag-app"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
PAT_TOKEN = os.getenv("GITHUB_PAT")

# Paths
PDF_PATHS = [
    "/home/ubuntu/Downloads/鸟哥的Linux私房菜-基础篇第四版.pdf",
    # 可添加更多
]

LOCAL_LLM_DIR = "/home/ubuntu/PyCharmMiscProject/AI/models/microsoft-Phi-3-mini-4k-instruct"
EMBEDDING_MODEL_DIR = "/home/ubuntu/PyCharmMiscProject/AI/models/models--sentence-transformers--paraphrase-multilingual-mpnet-base"
VECTOR_DB_PATH = "/home/ubuntu/PyCharmMiscProject/my_rag_system/data"
COLLECTION_NAME = "example_collection"

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Generation
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.95
REPETITION_PENALTY = 1.1