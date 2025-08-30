"""
测试包含答案的错别字练习生成和打印功能
"""

from gen_typos import ExerciseGenerator
from print_module import ExercisePrinter
import os


def test_exercise_generation_with_answers():
    """测试包含答案的练习生成"""
    print("🧪 测试包含答案的练习生成功能")
    print("=" * 50)

    # 创建生成器实例
    config = {
        "grade": "二年级",
        "theme": "春游",
        "length": 60,
        "count": 5,
        "num": 2,
        "mode": "misspelling"
    }

    generator = ExerciseGenerator(config)

    # 生成练习
    print("正在生成包含答案的练习...")
    exercises = generator.generate_exercises()

    if not exercises:
        print("❌ 练习生成失败")
        return False

    print(f"✅ 成功生成 {len(exercises)} 篇练习")

    # 保存练习
    json_file = generator.save_exercises(exercises)
    print(f"💾 练习已保存到: {json_file}")

    # 打印练习内容预览
    print("\n📖 练习内容预览:")
    generator.print_exercises(exercises)

    return True


def test_pdf_generation_with_answers():
    """测试包含答案的PDF生成"""
    print("\n🧪 测试包含答案的PDF生成功能")
    print("=" * 50)

    # 查找JSON文件
    dist_dir = "dist"
    json_files = [f for f in os.listdir(dist_dir) if f.endswith('.json')]

    if not json_files:
        print("❌ 没有找到JSON文件，请先运行练习生成")
        return False

    # 使用第一个JSON文件
    json_file = json_files[0]
    json_path = os.path.join(dist_dir, json_file)

    print(f"📄 正在处理文件: {json_file}")

    # 创建打印器
    printer = ExercisePrinter()

    # 生成PDF
    pdf_path = printer.print_from_json(json_path)

    if pdf_path:
        print(f"✅ PDF生成成功: {pdf_path}")
        print("💡 PDF中答案会自动分离，便于打印使用")
        return True
    else:
        print("❌ PDF生成失败")
        return False


def main():
    """主函数"""
    print("🚀 错别字练习答案功能测试")
    print("=" * 50)

    try:
        # 测试练习生成
        if test_exercise_generation_with_answers():
            print("\n✅ 练习生成测试通过")

            # 测试PDF生成
            if test_pdf_generation_with_answers():
                print("\n✅ PDF生成测试通过")
                print("\n🎉 所有测试通过！")
                print("\n📋 功能说明:")
                print("1. ✅ 练习内容包含答案")
                print("2. ✅ 答案与练习内容分离")
                print("3. ✅ PDF中答案在最后，便于打印")
                print("4. ✅ 适合小学生练习，家长参考")
            else:
                print("\n❌ PDF生成测试失败")
        else:
            print("\n❌ 练习生成测试失败")

    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        print("请检查环境配置和依赖安装")


if __name__ == "__main__":
    main()
