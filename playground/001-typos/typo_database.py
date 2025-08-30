"""
错别字数据库
包含常见的错别字组合，用于核对检查
"""

# 常见错别字组合（错误字 -> 正确字）
COMMON_TYPOS = {
    # 时间相关
    "昨田": "昨天", "今晨": "今天", "清辰": "清晨", "下五": "下午",

    # 地点相关
    "海弯": "海湾", "海宾": "海边", "海分": "海风", "公圆": "公园",
    "沙摊": "沙滩", "山角": "山脚", "山角下": "山脚下", "秋里": "秋林",

    # 物品相关
    "书饱": "书包", "产子": "铲子", "贝克": "贝壳", "扇壳": "扇贝",
    "小栏子": "小篮子", "小胶鞋": "小胶鞋", "金市": "金币",

    # 动作相关
    "扒着": "爬着", "爬倒": "爬到", "初发": "出发", "钩好": "勾好",
    "曲爬山": "去爬山", "过九": "过久", "爬倒": "爬到", "约号": "约好",
    "趣": "去", "起船": "起床", "检": "捡", "跳午": "跳舞",

    # 形容词相关
    "狠快": "很快", "狠多": "很多", "狠累": "很累", "狠开新": "很开心",
    "丰井": "风景", "漂良": "漂亮", "小欣": "小心", "开森": "开心",

    # 其他常见错别字
    "朋有": "朋友", "迷臧": "迷藏", "再树后": "在树后", "草从": "草丛",
    "发见": "发现", "约订": "约定", "伙半": "伙伴", "风争": "风筝",
    "剪只": "剪纸", "糊只": "糊纸", "装示": "装饰", "小和": "小河",
    "依就": "依旧", "笑哈哈": "笑哈哈", "家们": "家门", "佛过": "拂过",
    "脸旁": "脸庞", "很斗": "很多", "山披": "山坡", "小草莓": "小草莓",
    "火球": "火球", "伸受": "伸手", "兴奋": "兴奋", "象": "像",
    "飞午": "飞舞", "经": "径", "记念": "纪念", "从": "丛"
}

# 歧义句子模式（可能有多重含义的句子）
AMBIGUOUS_PATTERNS = [
    r'浪花亲我的脚',      # 亲可以是亲吻或轻抚
    r'它怕羞',            # 怕羞可以是害羞或怕羞
    r'像妈妈的手',        # 可以是比喻或描述
    r'疼得我直跳脚',      # 跳脚可以是动作或表达
]

# 无效纠正（不是真正的错别字）
INVALID_CORRECTIONS = [
    ("贴画", "贴画（无错，不计）"),
    ("草", "草（无错，不计）"),
    ("扎", "扎（无错，不计）"),
    ("跳脚", "跳脚（无错，不计）"),
    ("兴", "兴（无错，不计）"),
    ("踏", "踏（无错，不计）"),
    ("挂", "挂（无错，不计）"),
    ("火", "火（无错，不计）"),
    ("小", "小（无错，不计）"),
    ("眼泪", "眼泪"),
    ("夹", "夹"),
    ("蟹", "螃"),
    ("捡到", "拾到"),
    ("放进", "装到"),
    ("礼", "礼物"),
    ("疼了", "痛了"),
    ("吹吹", "呼呼"),
    ("开", "高"),
    ("脸", "脸")
]

def is_valid_typo(wrong: str, correct: str) -> bool:
    """
    检查是否是有效的错别字组合

    Args:
        wrong: 错误字
        correct: 正确字

    Returns:
        是否是有效的错别字
    """
    # 检查常见错别字
    if wrong in COMMON_TYPOS and COMMON_TYPOS[wrong] == correct:
        return True

    # 检查无效纠正
    if (wrong, correct) in INVALID_CORRECTIONS:
        return False

    # 检查是否是相同字
    if wrong == correct:
        return False

    # 检查是否是明显的错别字（字形相似或音近）
    if len(wrong) == len(correct) == 1:
        # 简单的相似性检查
        if wrong != correct and (wrong in correct or correct in wrong):
            return True

    return False

def get_typo_suggestions(wrong: str) -> list[str]:
    """
    获取错别字的建议纠正

    Args:
        wrong: 错误字

    Returns:
        建议的纠正列表
    """
    suggestions = []

    # 从常见错别字中查找
    if wrong in COMMON_TYPOS:
        suggestions.append(COMMON_TYPOS[wrong])

    # 从无效纠正中查找
    for invalid_wrong, invalid_correct in INVALID_CORRECTIONS:
        if invalid_wrong == wrong:
            suggestions.append(invalid_correct)

    return suggestions

def is_ambiguous_sentence(sentence: str) -> bool:
    """
    检查句子是否有歧义

    Args:
        sentence: 句子

    Returns:
        是否有歧义
    """
    import re

    for pattern in AMBIGUOUS_PATTERNS:
        if re.search(pattern, sentence):
            return True

    return False
