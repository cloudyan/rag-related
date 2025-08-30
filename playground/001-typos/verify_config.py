"""
配置验证脚本 - 展示重构后的配置变量
"""

from config import DEFAULT_CONFIG, EXERCISE_LENGTH_RANGES, ERROR_COUNT_RANGES


def show_config():
    """显示当前配置"""
    print("🔧 当前配置信息")
    print("=" * 50)

    print(f"📚 年级: {DEFAULT_CONFIG['grade']}")
    print(f"🎨 主题: {DEFAULT_CONFIG['theme']}")
    print(f"📝 练习字数: {DEFAULT_CONFIG['exercise_length']}字")
    print(f"❌ 错误数量: {DEFAULT_CONFIG['error_count']}个")
    print(f"📖 练习篇数: {DEFAULT_CONFIG['exercise_count']}篇")
    print(f"🎯 练习模式: {DEFAULT_CONFIG['mode']}")

    print("\n📊 年级配置范围")
    print("-" * 30)

    grade = DEFAULT_CONFIG['grade']
    if grade in EXERCISE_LENGTH_RANGES:
        min_len, max_len = EXERCISE_LENGTH_RANGES[grade]
        print(f"📏 {grade}练习字数范围: {min_len}-{max_len}字")

    if grade in ERROR_COUNT_RANGES:
        min_count, max_count = ERROR_COUNT_RANGES[grade]
        print(f"❌ {grade}错误数量范围: {min_count}-{max_count}个")

    print("\n✅ 配置变量重构完成！")
    print("💡 现在变量名更加语义化，易于理解和使用")


def show_environment_vars():
    """显示环境变量配置示例"""
    print("\n🌍 环境变量配置示例")
    print("=" * 50)

    print("""# 在 .env 文件中配置：
DEFAULT_GRADE=二年级
DEFAULT_THEME=random
DEFAULT_EXERCISE_LENGTH=60      # 每篇练习的字数
DEFAULT_ERROR_COUNT=5           # 每篇练习的错误数量
DEFAULT_EXERCISE_COUNT=5        # 要生成的练习篇数
DEFAULT_MODE=misspelling        # 练习模式
""")

    print("💡 提示：")
    print("1. DEFAULT_EXERCISE_LENGTH: 控制每篇练习的字数")
    print("2. DEFAULT_ERROR_COUNT: 控制每篇练习的错误数量")
    print("3. DEFAULT_EXERCISE_COUNT: 控制要生成多少篇练习")


if __name__ == "__main__":
    show_config()
    show_environment_vars()
