# 示例：在初始化或更新向量库的地方

from loaders.pdf_loader import load_and_split_pdfs  # 假设你的加载函数在这里
from chroma_store import get_or_create_vectorstore

# 1. 加载文档和 IDs
documents, doc_ids = load_and_split_pdfs()

# 2. 获取或创建向量库
vector_store = get_or_create_vectorstore()  # 注意：这里先不传 documents

# 3. 手动去重后插入
existing_ids = set(vector_store.get()["ids"])  # 获取已存在的所有 ID
print(f"Already have {len(existing_ids)} chunks in DB.")

# 筛选出新文档
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