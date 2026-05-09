# main.py
from loaders.pdf_loader import load_and_split_pdfs
from vectorstore.chroma_store import get_or_create_vectorstore
from models.llm import create_llm
from agent.rag_agent import create_rag_agent
import os, sys
from config import VECTOR_DB_PATH  # 确保定义了路径，如 "./chroma_db"

def main():
    # === 智能加载向量库（只在首次构建）===
    if not os.path.exists(os.path.join(VECTOR_DB_PATH, "chroma.sqlite3")):
        print("首次运行：正在加载 PDF 并构建向量库...")
        all_splits = load_and_split_pdfs()
        vector_store = get_or_create_vectorstore(documents=all_splits)
    else:
        print("加载已有向量库...")
        vector_store = get_or_create_vectorstore()  # 仅加载

    # === 初始化 LLM 和 Agent（传入 vector_store）===
    chat_model = create_llm()
    agent = create_rag_agent(chat_model, vector_store)  # ← 关键：传入 vector_store

    # === 保留你原有的聊天循环（完全不变）===
    print("\n🤖  RAG Chatbot is ready! Type 'exit' or 'quit' to stop.\n")
    messages = []
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if not user_input or user_input.lower() in {"exit", "quit"}:
                print("👋 Bye!")
                break

            messages.append({"role": "user", "content": user_input})

            response = ""
            for step in agent.stream({"messages": messages}, stream_mode="values"):
                ai_message = step["messages"][-1]
                if hasattr(ai_message, 'content'):
                    response = ai_message.content

            print(f"🤖 AI: {response}\n")
            messages.append({"role": "assistant", "content": response})

        except KeyboardInterrupt:
            print("👋 Bye!")
            sys.exit(0)

if __name__ == "__main__":
    main()