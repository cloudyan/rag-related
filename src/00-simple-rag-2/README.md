# 00-simple-rag-2 - 重构后的RAG实现

这是重构后的RAG代码版本，将原来三个文件中的重复代码提取到了公共模块中。

## 📁 文件说明

- `rag_base.py` - 公共RAG基础模块，包含所有共享功能
- `01_langchain_deepseek.py` - 重构后的DeepSeek版本
- `02_langchain_ollama.py` - 重构后的Ollama版本
- `03_langgraph_deepseek.py` - 重构后的LangGraph版本
- `test_rag_base.py` - 测试文件
- `README_重构说明.md` - 详细的重构说明文档

## 🚀 使用方法

### 1. 安装依赖
```bash
pip install langchain-community langchain-text-splitters langchain-huggingface langchain-core
```

### 2. 运行测试
```bash
cd src/00-simple-rag-2
python test_rag_base.py
```

### 3. 运行具体实现
```bash
# DeepSeek版本
python 01_langchain_deepseek.py

# Ollama版本
python 02_langchain_ollama.py

# LangGraph版本
python 03_langgraph_deepseek.py
```

## ✨ 重构优势

- **代码行数减少**: 总体减少40-50%
- **维护成本降低**: 核心逻辑集中管理
- **开发效率提升**: 新功能快速实现
- **代码质量提高**: 结构清晰，职责分离

## 📚 详细说明

请查看 `README_重构说明.md` 文件了解完整的重构细节和使用方法。
