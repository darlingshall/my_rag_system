# main.py
from vectorstore.chroma_store import update_vectorstore_with_pdfs
from models.llm import create_llm
from agent.rag_agent import create_rag_agent
import os, sys

def main():

    # === 智能加载向量库（只在首次构建）===
    vector_store = update_vectorstore_with_pdfs()  # 仅加载

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