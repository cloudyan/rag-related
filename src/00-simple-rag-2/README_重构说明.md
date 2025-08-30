# RAG代码重构说明

## 重构目标
将三个RAG实现文件中重复的前四步（文档加载、文本分块、信息嵌入、向量存储）提取到公共模块中，提高代码复用性和可维护性。

## 重构后的文件结构

### 1. `rag_base.py` - 公共RAG基础模块
- **功能**: 提供所有RAG实现共享的基础功能
- **包含**:
  - 文档加载（网页、预留本地文件接口）
  - 文本分块
  - 信息嵌入模型设置
  - 向量存储管理
  - 文档搜索
  - 一键设置完整管道

### 2. `01_langchain_deepseek.py` - DeepSeek版本
- **功能**: 使用DeepSeek API的LangChain RAG实现
- **特点**: 调用云端API，需要API密钥
- **代码行数**: 从154行减少到约80行

### 3. `02_langchain_ollama.py` - Ollama本地版本
- **功能**: 使用本地Ollama模型的LangChain RAG实现
- **特点**: 完全本地化，保护数据隐私
- **代码行数**: 从166行减少到约90行

### 4. `03_langgraph_deepseek.py` - LangGraph版本
- **功能**: 使用LangGraph构建的RAG工作流
- **特点**: 图状执行流程，支持复杂工作流
- **代码行数**: 从180行减少到约110行

## 重构优势

### 1. 代码复用
- 消除了约60-70行重复代码
- 三个文件共享相同的文档处理逻辑
- 新功能只需在公共模块中实现一次

### 2. 维护性提升
- 文档处理逻辑集中管理
- 参数配置统一化
- 错误处理标准化

### 3. 扩展性增强
- 新增RAG实现只需关注LLM调用部分
- 支持不同的文档源（网页、本地文件等）
- 支持不同的嵌入模型和向量存储

### 4. 使用便利性
- 提供一键设置函数 `setup_rag_pipeline()`
- 支持自定义参数配置
- 提供详细的进度提示

## 使用方法

### 基本用法
```python
from rag_base import setup_rag_pipeline

# 一键设置完整RAG管道
rag_base = setup_rag_pipeline(
    urls=["https://example.com"],
    chunk_size=1000,
    chunk_overlap=200,
    model_name="BAAI/bge-small-zh",
    device="cpu"
)

# 搜索文档
docs = rag_base.search_documents("你的问题", k=3)

# 获取上下文
context = rag_base.get_docs_content(docs)
```

### 高级用法
```python
from rag_base import RAGBase

# 创建自定义实例
rag = RAGBase(chunk_size=500, chunk_overlap=100)

# 分步设置
rag.load_documents_from_web(["https://example.com"])
rag.split_documents(docs)
rag.setup_embeddings("BAAI/bge-large-zh", "cuda")
rag.setup_vector_store()
```

## 新增功能

### 1. 进度提示
- 🌐 文档加载进度
- ✂️ 文本分割进度
- 🔤 嵌入模型初始化
- 🗄️ 向量存储设置
- 🎉 完成提示

### 2. 错误处理
- 参数验证
- 依赖检查
- 友好的错误信息

### 3. 扩展接口
- 预留本地文件加载接口
- 支持不同嵌入模型
- 支持GPU/CPU设备选择

## 依赖要求

所有文件都需要以下依赖：
```bash
pip install langchain-community langchain-text-splitters langchain-huggingface langchain-core
```

特定版本还需要：
- DeepSeek版本: `pip install langchain-deepseek`
- Ollama版本: `pip install langchain-ollama`
- LangGraph版本: `pip install langgraph`

## 未来扩展

### 1. 文档源扩展
- PDF文档支持
- Word文档支持
- 数据库连接支持

### 2. 向量存储扩展
- ChromaDB支持
- Pinecone支持
- Weaviate支持

### 3. 嵌入模型扩展
- OpenAI嵌入
- Cohere嵌入
- 本地嵌入模型

## 总结

通过这次重构，我们成功地将三个RAG实现文件中的重复代码提取到了公共模块中，实现了：
- **代码行数减少**: 总体减少约40-50%
- **维护成本降低**: 核心逻辑集中管理
- **开发效率提升**: 新功能快速实现
- **代码质量提高**: 结构清晰，职责分离

这种模块化设计为后续的RAG系统扩展奠定了良好的基础。
