#!/usr/bin/env python3
"""
双版面功能测试脚本
测试方格纸模板生成器和打印模块的A4横放双版面功能
"""

import os
from grid_paper_template import GridPaperTemplate
from print_module import ExercisePrinter


def test_grid_template():
    """测试方格纸模板生成器"""
    print("🧪 测试方格纸模板生成器...")

    template = GridPaperTemplate()

    # 测试基础模板
    print("📄 生成基础双版面模板...")
    basic_template = template.create_dual_panel_template("dist/test_basic_template.pdf")
    print(f"✅ 基础模板生成成功: {basic_template}")

    # 测试示例模板
    print("📝 生成带示例文字的双版面模板...")
    sample_template = template.create_sample_template("dist/test_sample_template.pdf")
    print(f"✅ 示例模板生成成功: {sample_template}")

    return True


def test_print_module():
    """测试打印模块"""
    print("\n🧪 测试打印模块...")

    printer = ExercisePrinter()

    # 创建测试练习数据
    test_exercises = [
        """春游

春天来了，小草绿了
花儿开了，小鸟叫了
我们一起去春游，看到
了美丽的风景，呼吸着
新鲜的空气，心情很好
春天真是一个美好的季
节，我们都很喜欢春天
希望春天能多停留一会
儿。

共有8个错别字，已找到：(0/8)

答案：
春游 -> 春游，小草 -> 小草，花儿 -> 花儿，小鸟 -> 小鸟，我们 -> 我们，美丽 -> 美丽，新鲜 -> 新鲜，春天 -> 春天""",

        """爬山

昨天我合同学约好
今天一起去爬山，一大
早我们就初发了，一路
上有说有笑很快就到了
山角下，爬山的人很多
没过多久我们就爬到了
山顶，山顶的风景很
美，爬山很累但我们很
开心。

共有7个错别字，已找到：(0/7)

答案：
合 -> 和，初 -> 出，山角 -> 山脚，爬 -> 爬，风景 -> 风景，累 -> 累，开心 -> 开心"""
    ]

    test_config = {
        "grade": "三年级",
        "theme": "测试主题",
        "mode": "misspelling"
    }

    # 生成测试PDF
    print("🖨️ 生成测试双版面PDF...")
    test_pdf = printer.create_exercise_pdf(test_exercises, test_config, "dist/test_dual_panel.pdf")
    print(f"✅ 测试PDF生成成功: {test_pdf}")

    return True


def main():
    """主函数"""
    print("🚀 A4横放双版面功能测试开始")
    print("=" * 50)
    print("设计规格：")
    print("- A4横放：297mm × 210mm")
    print("- 左右各一个32k版面：130mm × 184mm")
    print("- 每个版面：10行10列，内部竖向排版")
    print("- 行间距：半格高度，无方格")
    print("- 底部预留成绩区空间")
    print("=" * 50)

    # 确保输出目录存在
    os.makedirs("dist", exist_ok=True)

    try:
        # 测试方格纸模板生成器
        if test_grid_template():
            print("✅ 方格纸模板生成器测试通过")
        else:
            print("❌ 方格纸模板生成器测试失败")
            return

        # 测试打印模块
        if test_print_module():
            print("✅ 打印模块测试通过")
        else:
            print("❌ 打印模块测试失败")
            return

        print("\n🎉 所有测试通过！")
        print("\n📁 生成的文件：")
        print("  - dist/test_basic_template.pdf (基础双版面模板)")
        print("  - dist/test_sample_template.pdf (示例双版面模板)")
        print("  - dist/test_dual_panel.pdf (测试双版面练习纸)")

        print("\n💡 使用说明：")
        print("  1. 打印时选择A4横放")
        print("  2. 左右各一个32k版面")
        print("  3. 每个版面内部竖向排版（10行10列）")
        print("  4. 行间距半格高度，无方格")
        print("  5. 底部预留成绩区空间")

        print("\n🎯 布局特点：")
        print("  - 版面1（左侧）：练习一")
        print("  - 版面2（右侧）：练习二")
        print("  - 中间间距：20mm（对折线位置）")
        print("  - 成绩区：底部预留空间，无方格")

    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
