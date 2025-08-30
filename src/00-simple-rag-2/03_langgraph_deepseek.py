"""
LangGraph RAG智能问答系统
使用LangGraph构建检索增强生成(RAG)工作流
包含文档检索和答案生成两个步骤的图状执行流程
"""

import os
from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 调试：检查环境变量是否正确加载
api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"API Key loaded: {'YES' if api_key else 'NO'}")
print(f"API Key length: {len(api_key) if api_key else 0}")

# log 里的 LangSmith 是 LangChain 官方提供的应用监控和调试平台，用于：
# 追踪 LLM 调用，监控应用性能，调试提示词，分析模型响应
# 不影响功能：这只是一个警告，不会阻止你的 RAG 系统运行

# 导入公共RAG基础模块
from rag_base import setup_rag_pipeline

# 使用公共模块设置RAG管道
print("🚀 开始设置RAG管道...")
rag_base = setup_rag_pipeline(
    urls=["https://zh.wikipedia.org/wiki/深度求索"],  # 指定要爬取的网页URL列表
    chunk_size=1000,      # 每个文本块的最大字符数
    chunk_overlap=200,    # 相邻文本块之间的重叠字符数，确保信息连贯性
    model_name="BAAI/bge-small-zh",  # 使用bge-small-zh中文嵌入模型
    device="cpu"          # 指定使用CPU运行（可改为'cuda'使用GPU）
)

# 定义RAG提示词
# 从LangChain Hub拉取预定义的RAG提示词模板
from langchain import hub

prompt = hub.pull("rlm/rag-prompt")  # 获取标准的RAG提示词模板

# 定义应用状态
# 使用TypedDict定义LangGraph工作流中的状态结构
class State(TypedDict):
    """
    LangGraph状态定义

    Attributes:
        question: 用户输入的问题字符串
        context: 检索到的相关文档列表
        answer: 生成的答案字符串
    """
    question: str              # 用户提出的问题
    context: List[Document]    # 从向量存储中检索到的相关文档
    answer: str               # 大语言模型生成的最终答案

# 定义检索步骤
def retrieve(state: State) -> dict:
    """
    检索步骤：根据问题从向量存储中检索相关文档

    Args:
        state: 当前状态，包含用户问题

    Returns:
        dict: 包含检索到的文档的字典，键为"context"
    """
    # 使用相似度搜索检索与问题最相关的文档
    retrieved_docs = rag_base.search_documents(state["question"])
    return {"context": retrieved_docs}  # 返回检索结果，更新状态中的context字段

# 定义生成步骤
def generate(state: State) -> dict:
    """
    生成步骤：基于检索到的文档和问题生成答案

    Args:
        state: 当前状态，包含问题和检索到的上下文文档

    Returns:
        dict: 包含生成答案的字典，键为"answer"
    """
    # 导入DeepSeek聊天模型
    from langchain_deepseek import ChatDeepSeek

    # 初始化DeepSeek大语言模型
    llm = ChatDeepSeek(
        model="deepseek-chat",                      # 使用deepseek-chat模型
        temperature=0.7,                            # 控制生成文本的随机性(0-1，越高越随机)
        max_tokens=2048,                           # 最大生成token数量
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),     # 从环境变量获取API密钥
    )

    # 将检索到的文档内容拼接成上下文字符串
    docs_content = rag_base.get_docs_content(state["context"])

    # 使用提示词模板格式化问题和上下文
    messages = prompt.invoke({
        "question": state["question"],
        "context": docs_content
    })

    # 调用大语言模型生成答案
    response = llm.invoke(messages)
    return {"answer": response.content}  # 返回生成的答案，更新状态中的answer字段

# 构建和编译应用
# 使用LangGraph构建包含检索和生成步骤的工作流图
from langgraph.graph import START, StateGraph

# 创建状态图并定义执行流程
graph = (
    StateGraph(State)                          # 创建状态图，指定状态类型
    .add_sequence([retrieve, generate])        # 添加顺序执行的节点序列：先检索，后生成
    .add_edge(START, "retrieve")              # 添加从开始节点到检索节点的边
    .compile()                                # 编译图，生成可执行的工作流
)

# 运行查询
# 执行完整的RAG工作流：问题 -> 检索 -> 生成 -> 答案
question = "DeepSeek有哪些核心技术？"      # 定义要查询的问题
response = graph.invoke({"question": question})  # 调用图执行器，传入初始状态

# 格式化输出结果
print("=" * 80)
print("🤖 LangGraph RAG 智能问答系统")
print("=" * 80)
print(f"📝 问题: {question}")
print("-" * 80)
print("💡 答案:")
print(response["answer"])
print("-" * 80)
print(f"📚 检索到的文档数量: {len(response.get('context', []))}")
print("=" * 80)
