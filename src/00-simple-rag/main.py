import os
import re
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def clean_text(text):
    """清理文本内容，去除多余的空白和HTML标签"""
    # 去除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 去除HTML标签残留
    text = re.sub(r'<[^>]+>', '', text)
    # 去除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fff\-\.\,\!\?\(\)]', '', text)
    # 去除开头和结尾的空白
    text = text.strip()
    return text


def get_meaningful_preview(text, max_length=200):
    """获取有意义的文本预览"""
    # 清理文本
    cleaned_text = clean_text(text)

    # 如果清理后文本太短，尝试获取更多内容
    if len(cleaned_text) < 50:
        # 查找第一个包含中文的段落
        lines = text.split('\n')
        for line in lines:
            line_cleaned = clean_text(line)
            if len(line_cleaned) > 20 and any('\u4e00' <= char <= '\u9fff' for char in line_cleaned):
                return line_cleaned[:max_length]

    return cleaned_text[:max_length]



# 如果你想要更干净的文本，可以考虑使用专门的维基百科加载器：
# from langchain_community.document_loaders import WikipediaLoader

# loader = WikipediaLoader(query="深度求索", lang="zh")
# docs = loader.load()



def test_langchain_deepseek():
    """测试 LangChain DeepSeek RAG 系统的基本功能"""
    print("🧪 开始测试 LangChain DeepSeek RAG 系统...")

    try:
        # 1. 加载文档
        print("📚 步骤1: 加载文档...")
        from langchain_community.document_loaders import WebBaseLoader

        # 创建网页加载器实例，指定要爬取的URL
        loader = WebBaseLoader(web_paths=("https://zh.wikipedia.org/wiki/深度求索",))  # 深度求索的维基百科页面
        docs = loader.load()  # 执行加载操作，返回Document对象列表
        print(f"✅ 成功加载 {len(docs)} 个文档")

        # 2. 文本分块
        # 导入递归字符文本分割器，用于将长文本切分成小块
        print("✂️ 步骤2: 文本分块...")
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        # 创建文本分割器实例
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # 每个文本块的最大字符数（平衡内容完整性和处理效率）
            chunk_overlap=200,  # 相邻文本块之间的重叠字符数（确保信息不丢失）
        )
        # 将加载的文本分割成多个小块，便于向量化和检索
        all_splits = text_splitter.split_documents(docs)
        print(f"✅ 成功分割成 {len(all_splits)} 个文本块")

        # 3. 显示有意义的文本块预览
        if all_splits:
            print("\n📖 文本块预览:")

            # 显示前3个有意义的文本块
            meaningful_count = 0
            for i, split in enumerate(all_splits):
                if meaningful_count >= 3:
                    break

                preview = get_meaningful_preview(split.page_content)
                if len(preview) > 30:  # 只显示有意义的文本块
                    meaningful_count += 1
                    print(f"\n片段 {meaningful_count}:")
                    print(f"   {preview}...")
                    print(f"   原始长度: {len(split.page_content)} 字符")

        # 4. 返回处理结果
        return all_splits

    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("Simple RAG 系统测试")
    print("=" * 60)

    # 测试基本功能
    result = test_langchain_deepseek()

    if result:
        print(f"\n✅ 测试完成！共处理 {len(result)} 个文本块")
    else:
        print("\n❌ 测试失败")

    print("=" * 60)


# uv run python main.py

if __name__ == "__main__":
    main()
