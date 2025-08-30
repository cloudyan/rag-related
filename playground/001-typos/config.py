"""
错别字纠错练习短文批量生成器配置文件
"""

import os
from typing import List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 模型配置
MODEL_CONFIG = {
    "model": os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
    "base_url": os.getenv("OPENAI_BASE_URL"),
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("MAX_TOKENS", "2000"))
}

# 练习模式配置
EXERCISE_MODES = {
    "misspelling": "错别字纠错练习",
    "word_usage": "用词不当纠错练习"
}

# 年级配置
GRADES = [
    "一年级", "二年级", "三年级", "四年级", "五年级", "六年级"
]

# 主题配置
THEMES = [
    "春游", "秋游", "动物园", "游乐园", "图书馆", "博物馆",
    "公园", "海边", "山上", "农场", "学校", "家庭", "朋友"
]

# 默认配置
DEFAULT_CONFIG = {
    "grade": os.getenv("DEFAULT_GRADE", "二年级"), # 年级
    "theme": os.getenv("DEFAULT_THEME", "random"),  # random 表示随机选择
    "exercise_length": None,  # 每篇练习的字数（None表示使用年级默认值）
    "error_count": None,      # 每篇练习的错误数量（None表示使用年级默认值）
    "exercise_count": int(os.getenv("DEFAULT_EXERCISE_COUNT", "2")), # 要生成的练习篇数
    "mode": os.getenv("DEFAULT_MODE", "misspelling") # 练习模式
}

# 环境变量配置（高优先级，但会被年级范围限制）
ENV_CONFIG = {
    "exercise_length": os.getenv("DEFAULT_EXERCISE_LENGTH"),
    "error_count": os.getenv("DEFAULT_ERROR_COUNT"),
}

# 年级默认值配置（参考基准，可上下浮动10%左右）
GRADE_DEFAULT_VALUES = {
    "一年级": {"exercise_length": 40, "error_count": 4},
    "二年级": {"exercise_length": 65, "error_count": 5},
    "三年级": {"exercise_length": 100, "error_count": 6},
    "四年级": {"exercise_length": 125, "error_count": 8},
    "五年级": {"exercise_length": 160, "error_count": 10},
    "六年级": {"exercise_length": 200, "error_count": 12},
}
