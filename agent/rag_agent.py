# agent/rag_agent.py

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

def create_rag_agent(chat_model, vector_store):
    # 在 create_rag_agent 内部定义 middleware，通过闭包捕获 vector_store
    @dynamic_prompt
    def prompt_with_context(request: ModelRequest) -> str:
        last_query = request.state["messages"][-1].text
        print(f"用户问题: {last_query}")

        retrieved_docs = vector_store.similarity_search(last_query, k=3)
        print(f"🔍 检索到 {len(retrieved_docs)} 篇文档")
        for i, doc in enumerate(retrieved_docs):
            print(f"  [{i + 1}] {doc.page_content[:100]}...")

        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

        system_message = (
            "你是一个严谨的助手。请严格遵守以下规则：\n"
        "1. 仅根据下方【检索到的上下文】回答问题。\n"
        "2. 如果上下文中没有相关信息，请明确回答：'根据提供的资料，我无法回答该问题。'\n"
        "3. 不要编造、推测或引用外部知识。\n"
        "4. 回答需简洁准确，避免冗余。\n\n"
        "【检索到的上下文】：\n{context}"
            f"\n\n{docs_content}"
        )
        return system_message

    # 创建 agent，传入这个绑定 vector_store 的 middleware
    agent = create_agent(
        chat_model,
        tools=[],
        middleware=[prompt_with_context]  # ← 直接传这个被装饰的函数
    )
    return agent