"""
RAG基础模块 - 公共功能
包含文档加载、文本分块、信息嵌入、向量存储等通用功能
可以被不同的RAG实现方案复用
"""

import os
from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document


class RAGBase:
    """RAG基础类，提供通用的文档处理和向量化功能"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        初始化RAG基础类

        Args:
            chunk_size: 每个文本块的最大字符数
            chunk_overlap: 相邻文本块之间的重叠字符数
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = None
        self.vector_store = None
        self.all_splits = []

    def load_documents_from_web(self, urls: List[str]) -> List[Document]:
        """
        从网页加载文档

        Args:
            urls: 要爬取的网页URL列表

        Returns:
            Document对象列表
        """
        print(f"🌐 正在从 {len(urls)} 个网页加载文档...")
        loader = WebBaseLoader(web_paths=urls)
        docs = loader.load()
        print(f"✅ 成功加载 {len(docs)} 个文档")
        return docs

    def load_documents_from_files(self, file_paths: List[str]) -> List[Document]:
        """
        从本地文件加载文档（预留接口，可根据需要扩展）

        Args:
            file_paths: 本地文件路径列表

        Returns:
            Document对象列表
        """
        # TODO: 实现本地文件加载功能
        # 可以支持PDF、TXT、DOC等格式
        raise NotImplementedError("本地文件加载功能待实现")

    def split_documents(self, docs: List[Document]) -> List[Document]:
        """
        导入递归字符文本分割器，用于将长文本切分成小块

        Args:
            docs: 原始文档列表

        Returns:
            分割后的文档块列表
        """
        print(f"✂️ 正在将 {len(docs)} 个文档分割成小块...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, # 每个文本块的最大字符数（平衡内容完整性和处理效率）
            chunk_overlap=self.chunk_overlap, # 相邻文本块之间的重叠字符数（确保信息不丢失）
        )
        # 将加载的文本分割成多个小块，便于向量化和检索
        self.all_splits = text_splitter.split_documents(docs)
        print(f"✅ 成功分割成 {len(self.all_splits)} 个文本块")
        return self.all_splits

    def setup_embeddings(self, model_name: str = "BAAI/bge-small-zh", device: str = "cpu") -> None:
        """
        设置嵌入模型
        BAAI/bge-small-zh模型，这是一个专门针对中文优化的嵌入模型
        model_kwargs指定使用CPU进行计算，适合没有GPU的环境
        encode_kwargs中的normalize_embeddings=True确保嵌入向量被归一化，提高检索精度
        Args:
            model_name: 嵌入模型名称
            device: 计算设备 ("cpu" 或 "cuda")
        """
        print(f"🔤 正在初始化嵌入模型: {model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name, # 中文嵌入模型，体积小但效果良好
            model_kwargs={"device": device}, # 使用CPU设备进行计算（可改为"cuda"使用GPU）
            encode_kwargs={"normalize_embeddings": True} # 启用向量归一化，提升相似度计算准确性
        )
        print(f"✅ 嵌入模型初始化完成，使用设备: {device}")

    def setup_vector_store(self) -> None:
        """
        设置向量存储
        导入内存向量存储，用于存储和检索文档向量
        """
        if self.embeddings is None:
            raise ValueError("请先调用 setup_embeddings() 设置嵌入模型")

        print("🗄️ 正在初始化向量存储...")
        self.vector_store = InMemoryVectorStore(self.embeddings)

        # 这一步会将所有文档块转换为向量并存储在内存中，用于后续的相似性搜索
        if self.all_splits:
            self.vector_store.add_documents(self.all_splits)
            print(f"✅ 向量存储初始化完成，已添加 {len(self.all_splits)} 个文档块")
        else:
            print("⚠️ 警告：没有文档块可以添加到向量存储中")

    def search_documents(self, query: str, k: int = 3) -> List[Document]:
        """
        在向量存储中搜索相关文档

        Args:
            query: 搜索查询
            k: 返回的文档数量

        Returns:
            相关文档列表
        """
        if self.vector_store is None:
            raise ValueError("请先调用 setup_vector_store() 设置向量存储")

        return self.vector_store.similarity_search(query, k=k)

    def get_docs_content(self, docs: List[Document]) -> str:
        """
        将文档列表转换为上下文字符串

        Args:
            docs: 文档列表

        Returns:
            拼接后的上下文字符串
        """
        return "\n\n".join(doc.page_content for doc in docs)

    def setup_complete_pipeline(self, urls: List[str] = None,
                               model_name: str = "BAAI/bge-small-zh",
                               device: str = "cpu") -> None:
        """
        一键设置完整的RAG管道

        Args:
            urls: 网页URL列表
            model_name: 嵌入模型名称
            device: 计算设备
        """
        if urls:
            # 加载文档
            docs = self.load_documents_from_web(urls)

            # 分割文档
            self.split_documents(docs)

        # 设置嵌入模型
        self.setup_embeddings(model_name, device)

        # 设置向量存储
        self.setup_vector_store()

        print("🎉 RAG管道设置完成！")


# 便捷函数：快速创建RAG基础实例
def create_rag_base(chunk_size: int = 1000, chunk_overlap: int = 200) -> RAGBase:
    """
    快速创建RAG基础实例

    Args:
        chunk_size: 文本块大小
        chunk_overlap: 文本块重叠

    Returns:
        RAGBase实例
    """
    return RAGBase(chunk_size, chunk_overlap)


# 便捷函数：一键设置完整的RAG管道
def setup_rag_pipeline(urls: List[str],
                       chunk_size: int = 1000,
                       chunk_overlap: int = 200,
                       model_name: str = "BAAI/bge-small-zh",
                       device: str = "cpu") -> RAGBase:
    """
    一键设置完整的RAG管道

    Args:
        urls: 网页URL列表
        chunk_size: 文本块大小
        chunk_overlap: 文本块重叠
        model_name: 嵌入模型名称
        device: 计算设备

    Returns:
        配置完成的RAGBase实例
    """
    rag_base = create_rag_base(chunk_size, chunk_overlap)
    rag_base.setup_complete_pipeline(urls, model_name, device)
    return rag_base
