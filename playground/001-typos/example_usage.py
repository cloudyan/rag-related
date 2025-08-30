"""
错别字纠错练习短文批量生成器使用示例
展示不同配置和模式的使用方法
"""

from gen_typos import ExerciseGenerator


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")

    # 使用默认配置
    generator = ExerciseGenerator()
    exercises = generator.generate_exercises()

    if exercises:
        generator.save_exercises(exercises)
        generator.print_exercises(exercises)


def example_custom_config():
    """自定义配置示例"""
    print("\n=== 自定义配置示例 ===")

    # 自定义配置：三年级用词不当练习
    config = {
        "grade": "三年级",
        "theme": "动物园",
        "length": 100,
        "count": 6,
        "num": 3,
        "mode": "word_usage"
    }

    generator = ExerciseGenerator(config)
    exercises = generator.generate_exercises()

    if exercises:
        generator.save_exercises(exercises)
        generator.print_exercises(exercises)


def example_batch_generation():
    """批量生成示例"""
    print("\n=== 批量生成示例 ===")

    # 不同配置的练习
    configs = [
        {
            "grade": "一年级",
            "mode": "misspelling",
            "theme": "春游",
            "num": 2
        },
        {
            "grade": "四年级",
            "mode": "word_usage",
            "theme": "图书馆",
            "num": 2
        },
        {
            "grade": "六年级",
            "mode": "misspelling",
            "theme": "博物馆",
            "num": 2
        }
    ]

    for i, config in enumerate(configs, 1):
        print(f"\n--- 生成第 {i} 组练习 ---")
        generator = ExerciseGenerator(config)
        exercises = generator.generate_exercises()

        if exercises:
            filename = generator.save_exercises(exercises, f"batch_{i}.json")
            print(f"第 {i} 组练习已保存到: {filename}")


def example_theme_random():
    """随机主题示例"""
    print("\n=== 随机主题示例 ===")

    # 使用随机主题
    config = {
        "grade": "二年级",
        "theme": "random",  # 随机选择主题
        "mode": "misspelling",
        "num": 3
    }

    generator = ExerciseGenerator(config)
    exercises = generator.generate_exercises()

    if exercises:
        generator.save_exercises(exercises)
        generator.print_exercises(exercises)


if __name__ == "__main__":
    print("错别字纠错练习短文批量生成器 - 使用示例")
    print("=" * 50)

    try:
        # 运行各种示例
        example_basic_usage()
        example_custom_config()
        example_batch_generation()
        example_theme_random()

        print("\n所有示例执行完成！")

    except Exception as e:
        print(f"执行示例时出错: {e}")
        print("请检查环境配置和模型连接")
