"""
LangChain RAG智能问答系统 - DeepSeek版本
使用传统的LangChain链式调用实现检索增强生成(RAG)
包含文档加载、向量化、检索、生成等完整流程
"""

# 执行
# uv run python 01_langchain_deepseek.py

# 导入必要的模块和环境变量配置
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量，包括API密钥等敏感信息
load_dotenv()

# 导入公共RAG基础模块
from rag_base import setup_rag_pipeline

# 第一步：使用公共模块设置RAG管道
print("🚀 开始设置RAG管道...")
rag_base = setup_rag_pipeline(
    urls=["https://zh.wikipedia.org/wiki/深度求索"],  # 深度求索的维基百科页面
    chunk_size=1000,  # 每个文本块的最大字符数
    chunk_overlap=200,  # 相邻文本块之间的重叠字符数
    model_name="BAAI/bge-small-zh",  # 中文嵌入模型
    device="cpu"  # 使用CPU设备
)

# 第二步：检索阶段
# 构建用户查询
question = "DeepSeek有哪些核心技术？"

# 在向量存储中搜索相关文档，并准备上下文内容
print(f"🔍 正在搜索相关问题: {question}")
retrieved_docs = rag_base.search_documents(question, k=3)  # k=3表示检索前3个最相关的文档块
# 将检索到的文档内容拼接成一个字符串，作为大模型的上下文
docs_content = rag_base.get_docs_content(retrieved_docs)

# 构建提示模板
from langchain_core.prompts import ChatPromptTemplate

# 创建提示模板，定义大模型的角色和任务
prompt = ChatPromptTemplate.from_template(
    """基于以下上下文，请详细回答问题。要求：
1. 如果上下文中没有相关信息，请明确说明
2. 如果上下文中有相关信息，请尽可能详细地提取和总结
3. 回答要客观、准确，避免过度推断

上下文: {context}

问题: {question}

回答:"""
)

# 第三步：生成阶段
# 使用大语言模型生成答案
from langchain_deepseek import ChatDeepSeek  # 需要安装: pip install langchain-deepseek

# 初始化DeepSeek聊天模型
llm = ChatDeepSeek(
    model="deepseek-chat",  # DeepSeek API 支持的聊天模型名称
    temperature=0.1,  # 控制输出的随机性（0-1之间，越高越随机，越低越确定）
    max_tokens=2048,  # 最大输出token数量，控制回答长度
    api_key=os.getenv("DEEPSEEK_API_KEY", ""),  # 从环境变量加载API密钥
)

# 使用提示模板格式化问题和上下文，然后调用大模型生成答案
formatted_prompt = prompt.format(question=question, context=docs_content)
answer = llm.invoke(formatted_prompt)

# 格式化输出答案
print("=" * 80)
print("🤖 LangChain RAG 智能问答系统 (DeepSeek版本)")
print("=" * 80)
print(f"📝 问题: {question}")
print("-" * 80)
print("💡 答案:")
# 安全地提取答案内容，兼容不同的返回格式
print(answer.content if hasattr(answer, "content") else str(answer))
print("-" * 80)
print("📚 参考文档数量:", len(retrieved_docs))
print("🔍 检索到的相关片段:")

# 逐个显示检索到的文档片段，便于用户了解答案来源
for i, doc in enumerate(retrieved_docs, 1):
    print(f"\n片段 {i}:")
    # 截取前200个字符显示，避免输出过长
    content_preview = doc.page_content[:200]
    if len(doc.page_content) > 200:
        content_preview += "..."
    print(f"  内容: {content_preview}")

    # 如果文档有元数据（如来源URL），则显示
    if hasattr(doc, "metadata") and doc.metadata:
        print(f"  来源: {doc.metadata}")

print("=" * 80)
