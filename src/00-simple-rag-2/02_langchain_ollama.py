"""
LangChain RAG智能问答系统 - Ollama本地版本
使用传统的LangChain链式调用实现检索增强生成(RAG)
通过Ollama调用本地部署的大语言模型，无需API密钥，保护数据隐私
适合离线环境或对数据安全有严格要求的场景
"""

# 导入必要的模块和环境变量配置
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量（Ollama版本通常不需要API密钥）
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
# 使用ollama本地大语言模型生成答案
from langchain_ollama import ChatOllama  # 需要安装: pip install langchain-ollama

# 初始化Ollama聊天模型
# 注意：使用前需要先通过命令行安装对应模型，例如: ollama pull qwen2.5:7b
llm = ChatOllama(
    model="qwen3:1.7b",  # 本地模型名称，可以根据需要更换其他模型（如llama3.1, mistral, codellama等）
    # model="qwen2.5:7b",  # 本地模型名称，可以根据需要更换其他模型（如llama3.1, mistral, codellama等）
    request_timeout=300.0  # 增加超时时间（秒），本地模型推理可能需要更长时间
    # temperature=0.7,  # 可选：控制输出随机性，某些Ollama版本支持
    # num_ctx=4096,     # 可选：上下文窗口大小
)

# 使用提示模板格式化问题和上下文，然后调用本地大模型生成答案
formatted_prompt = prompt.format(question=question, context=docs_content)
answer = llm.invoke(formatted_prompt)

# 格式化输出答案
print("=" * 80)
print("🤖 LangChain RAG 智能问答系统 (Ollama本地版本)")
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

# 使用说明：
# 1. 安装Ollama: https://ollama.ai/
# 2. 下载模型: ollama pull qwen2.5:7b
# 3. 启动Ollama服务: ollama serve
# 4. 运行此脚本
#
# 常用模型推荐：
# - qwen2.5:7b (通用中文模型，平衡效果和速度)
# - llama3.1:8b (英文为主，支持中文)
# - mistral:7b (轻量级模型，速度快)
# - codellama:7b (代码专用模型)
