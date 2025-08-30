"""
测试RAG基础模块
验证重构后的代码是否正常工作
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_rag_base():
    """测试RAG基础模块的基本功能"""
    print("🧪 开始测试RAG基础模块...")

    try:
        # 导入公共RAG基础模块
        from rag_base import setup_rag_pipeline

        print("✅ 成功导入rag_base模块")

        # 测试基本功能
        print("\n🚀 测试RAG管道设置...")
        rag_base = setup_rag_pipeline(
            urls=["https://zh.wikipedia.org/wiki/深度求索"],
            chunk_size=500,  # 使用较小的chunk_size进行快速测试
            chunk_overlap=100,
            model_name="BAAI/bge-small-zh",
            device="cpu"
        )

        print("✅ RAG管道设置成功")

        # 测试搜索功能
        print("\n🔍 测试文档搜索功能...")
        test_query = "DeepSeek"
        results = rag_base.search_documents(test_query, k=2)

        if results:
            print(f"✅ 搜索成功，找到 {len(results)} 个相关文档")

            # 测试上下文获取
            context = rag_base.get_docs_content(results)
            print(f"✅ 上下文获取成功，长度: {len(context)} 字符")

            # 显示第一个结果的前100个字符
            if results[0].page_content:
                preview = results[0].page_content[:100]
                print(f"📄 第一个结果预览: {preview}...")
        else:
            print("⚠️ 搜索未返回结果")

        print("\n🎉 所有测试通过！RAG基础模块工作正常。")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """测试RAG基础模块的各个组件"""
    print("\n🔧 测试各个组件...")

    try:
        from rag_base import RAGBase

        # 创建实例
        rag = RAGBase(chunk_size=300, chunk_overlap=50)
        print("✅ RAGBase实例创建成功")

        # 测试文档加载
        print("🌐 测试文档加载...")
        docs = rag.load_documents_from_web(["https://zh.wikipedia.org/wiki/深度求索"])
        print(f"✅ 文档加载成功，共 {len(docs)} 个文档")

        # 测试文档分割
        print("✂️ 测试文档分割...")
        splits = rag.split_documents(docs)
        print(f"✅ 文档分割成功，共 {len(splits)} 个块")

        # 测试嵌入模型设置
        print("🔤 测试嵌入模型设置...")
        rag.setup_embeddings("BAAI/bge-small-zh", "cpu")
        print("✅ 嵌入模型设置成功")

        # 测试向量存储设置
        print("🗄️ 测试向量存储设置...")
        rag.setup_vector_store()
        print("✅ 向量存储设置成功")

        # 测试搜索
        print("🔍 测试搜索功能...")
        search_results = rag.search_documents("DeepSeek", k=1)
        print(f"✅ 搜索功能正常，返回 {len(search_results)} 个结果")

        print("\n🎉 所有组件测试通过！")
        return True

    except Exception as e:
        print(f"❌ 组件测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 RAG基础模块测试")
    print("=" * 60)

    # 运行测试
    test1_passed = test_rag_base()
    test2_passed = test_individual_components()

    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    print(f"整体功能测试: {'✅ 通过' if test1_passed else '❌ 失败'}")
    print(f"组件功能测试: {'✅ 通过' if test2_passed else '❌ 失败'}")

    if test1_passed and test2_passed:
        print("\n🎉 所有测试通过！重构成功！")
    else:
        print("\n⚠️ 部分测试失败，请检查代码")

    print("=" * 60)
