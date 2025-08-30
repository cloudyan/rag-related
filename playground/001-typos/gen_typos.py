"""
错别字纠错练习短文批量生成器
Python 3.8+
重构版本：支持多种练习模式，配置化管理
"""

import os
import json
import random
from datetime import datetime
from typing import List, Dict, Any

from config import (
    DEFAULT_CONFIG, GRADES, THEMES,
    EXERCISE_MODES, ENV_CONFIG, GRADE_DEFAULT_VALUES
)
from prompts import PROMPT_TEMPLATES
from model_client import ModelClient
from print_module import ExercisePrinter
from typo_database import is_valid_typo, is_ambiguous_sentence, get_typo_suggestions
import re


class ExerciseGenerator:
    """练习生成器类"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化练习生成器

        Args:
            config: 配置参数，如果为None则使用默认配置
        """
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.model_client = ModelClient()

        # 验证配置
        self._validate_config()

    def _validate_config(self):
        """验证配置参数"""
        if self.config["grade"] not in GRADES:
            print(f"警告：年级 '{self.config['grade']}' 不在支持列表中，使用默认年级")
            self.config["grade"] = DEFAULT_CONFIG["grade"]

        if self.config["mode"] not in EXERCISE_MODES:
            print(f"警告：模式 '{self.config['mode']}' 不支持，使用默认模式")
            self.config["mode"] = DEFAULT_CONFIG["mode"]

        # 简化配置优先级系统
        grade = self.config["grade"]

        # 1. 字数配置：环境变量 > 年级默认值
        if self.config["exercise_length"] is None:
            if ENV_CONFIG["exercise_length"]:
                # 环境变量设置了字数
                env_length = int(ENV_CONFIG["exercise_length"])
                self.config["exercise_length"] = env_length
                print(f"✅ 使用环境变量设置的字数: {env_length}")
            else:
                # 环境变量未设置，使用年级默认值
                self.config["exercise_length"] = GRADE_DEFAULT_VALUES[grade]["exercise_length"]
                print(f"📚 使用{grade}默认字数: {self.config['exercise_length']}")

        # 2. 错误数量配置：环境变量 > 年级默认值
        if self.config["error_count"] is None:
            if ENV_CONFIG["error_count"]:
                # 环境变量设置了错误数量
                env_count = int(ENV_CONFIG["error_count"])
                self.config["error_count"] = env_count
                print(f"✅ 使用环境变量设置的错误数量: {env_count}")
            else:
                # 环境变量未设置，使用年级默认值
                self.config["error_count"] = GRADE_DEFAULT_VALUES[grade]["error_count"]
                print(f"📚 使用{grade}默认错误数量: {self.config['error_count']}")

        # 3. 显示配置信息（仅供参考，不强制限制）
        if grade in GRADE_DEFAULT_VALUES:
            default_length = GRADE_DEFAULT_VALUES[grade]["exercise_length"]
            default_error_count = GRADE_DEFAULT_VALUES[grade]["error_count"]

            # 计算建议范围（上下浮动10%左右）
            length_range = f"{int(default_length * 0.9)}-{int(default_length * 1.1)}"
            error_range = f"{int(default_error_count * 0.8)}-{int(default_error_count * 1.2)}"

            print(f"💡 {grade}建议范围：字数{length_range}字，错误数量{error_range}个（仅供参考）")

    def _get_random_theme(self) -> str:
        """获取随机主题"""
        return random.choice(THEMES)

    def _get_prompt_template(self) -> str:
        """获取提示词模板"""
        mode = self.config["mode"]
        if mode not in PROMPT_TEMPLATES:
            print(f"警告：模式 '{mode}' 的提示词模板不存在，使用错别字模式")
            mode = "misspelling"
        return PROMPT_TEMPLATES[mode]

    def generate_exercises(self) -> List[str]:
        """
        生成练习短文

        Returns:
            生成的练习短文列表
        """
        # 处理主题配置
        theme = self.config["theme"]
        if theme == "random":
            theme = self._get_random_theme()

        # 获取提示词模板
        prompt_template = self._get_prompt_template()

                # 格式化提示词
        prompt = prompt_template.format(
            grade=self.config["grade"],
            length=self.config["exercise_length"],
            theme=theme,
            count=self.config["error_count"],
            num=self.config["exercise_count"]
        )

        print(f"正在生成 {self.config['exercise_count']} 篇{EXERCISE_MODES[self.config['mode']]}...")
        print(f"年级: {self.config['grade']}, 主题: {theme}, 字数: {self.config['exercise_length']}, 错误数量: {self.config['error_count']}")

        # 调用模型生成
        raw_content = self.model_client.generate_text(prompt)

        if not raw_content:
            print("模型生成失败，返回空列表")
            return []

                # 按"---"分割多篇文章
        articles = [a.strip() for a in raw_content.split("---") if a.strip()]

        # 如果生成的文章数量不足，尝试按空行分割
        if len(articles) < self.config["exercise_count"]:
            articles = [a.strip() for a in raw_content.split("\n\n") if a.strip()]

        # 如果还是不够，尝试按行分割
        if len(articles) < self.config["exercise_count"]:
            articles = [a.strip() for a in raw_content.split("\n") if a.strip() and len(a.strip()) > 10]

        # 对每篇文章进行核对检查
        validated_articles = []
        for article in articles[:self.config["exercise_count"]]:
            corrected_article, problems = self._validate_exercise_content(article)
            if problems:
                print(f"\n🔍 练习内容核对检查发现问题：")
                for problem in problems:
                    print(f"  {problem}")
                print(f"💡 建议：检查并修正这些问题，避免误导学生")
            else:
                print(f"✅ 练习内容核对检查通过")

            # 自动修正练习内容，过滤掉无错的纠正
            corrected_article = self._auto_correct_exercise(corrected_article)
            validated_articles.append(corrected_article)

        return validated_articles

    def _validate_exercise_content(self, exercise: str) -> tuple[str, list[str]]:
        """
        核对检查练习内容，避免歧义和多语义句子

        Args:
            exercise: 练习内容

        Returns:
            (修正后的练习内容, 问题说明列表)
        """
        problems = []
        corrected_exercise = exercise

        # 1. 检查答案格式是否正确
        answer_match = re.search(r'答案：\n(.*?)(?:\n|$)', exercise, re.DOTALL)
        if not answer_match:
            problems.append("❌ 缺少答案部分")
            return corrected_exercise, problems

        answer_text = answer_match.group(1)

        # 2. 检查每个答案的合理性
        corrections = re.findall(r'([^，\s]+)\s*->\s*([^，\s]+)', answer_text)

        for wrong, correct in corrections:
            # 检查是否真的是错别字
            if not self._is_valid_correction(wrong, correct):
                problems.append(f"⚠️ 可疑的纠正：'{wrong}' -> '{correct}' 可能不是错别字")

        # 3. 检查句子是否有歧义
        body_text = self._extract_body_text(exercise)
        ambiguous_sentences = self._check_ambiguous_sentences(body_text)
        if ambiguous_sentences:
            problems.extend([f"⚠️ 歧义句子：{s}" for s in ambiguous_sentences])

        # 4. 检查错别字数量是否匹配
        expected_count = self.config["error_count"]
        actual_count = len(corrections)
        if actual_count != expected_count:
            problems.append(f"❌ 错别字数量不匹配：期望{expected_count}个，实际{actual_count}个")

        return corrected_exercise, problems

    def _is_valid_correction(self, wrong: str, correct: str) -> bool:
        """
        检查纠正是否合理

        Args:
            wrong: 错误字
            correct: 正确字

        Returns:
            是否合理的纠正
        """
        return is_valid_typo(wrong, correct)

    def _extract_body_text(self, exercise: str) -> str:
        """提取练习正文部分"""
        lines = exercise.split('\n')
        body_start = -1
        body_end = -1

        for i, line in enumerate(lines):
            if "共有" in line and "个错别字" in line:
                body_end = i
                break

        # 找到正文开始（跳过标题和空行）
        for i in range(len(lines)):
            if lines[i].strip() and "共有" not in lines[i]:
                if i > 0 and not lines[i-1].strip():  # 前面有空行
                    body_start = i
                    break

        if body_start != -1 and body_end != -1:
            return '\n'.join(lines[body_start:body_end])
        return ""

    def _check_ambiguous_sentences(self, body_text: str) -> list[str]:
        """
        检查是否有歧义句子

        Args:
            body_text: 正文内容

        Returns:
            歧义句子列表
        """
        ambiguous = []
        lines = body_text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 检查可能的多语义句子
            if self._is_ambiguous_sentence(line):
                ambiguous.append(line)

        return ambiguous

    def _is_ambiguous_sentence(self, sentence: str) -> bool:
        """检查单个句子是否有歧义"""
        return is_ambiguous_sentence(sentence)

    def _auto_correct_exercise(self, exercise: str) -> str:
        """
        自动修正练习内容，过滤掉无错的纠正，修正错别字数量

        Args:
            exercise: 原始练习内容

        Returns:
            修正后的练习内容
        """
        # 提取答案部分
        answer_match = re.search(r'答案：\n(.*?)(?:\n|$)', exercise, re.DOTALL)
        if not answer_match:
            return exercise

        answer_text = answer_match.group(1)

        # 解析所有纠正
        corrections = re.findall(r'([^，\s]+)\s*->\s*([^，\s]+)', answer_text)

        # 过滤有效的错别字纠正
        valid_corrections = []
        for wrong, correct in corrections:
            # 跳过明显的无效纠正
            if "无错" in correct or wrong == correct:
                continue
            # 跳过格式错误的纠正
            if "（应为" in correct or "（无错" in correct:
                continue
            # 保留其他纠正（让用户判断）
            valid_corrections.append((wrong, correct))

        # 重新构建答案部分
        if valid_corrections:
            new_answer = "答案：\n" + "，".join([f"{wrong} -> {correct}" for wrong, correct in valid_corrections])
        else:
            new_answer = "答案：\n无错别字"

        # 更新错别字数量提示
        actual_count = len(valid_corrections)
        exercise = re.sub(r'共有\d+个错别字', f'共有{actual_count}个错别字', exercise)
        exercise = re.sub(r'已找到：\(0/\d+\)', f'已找到：(0/{actual_count})', exercise)

        # 替换答案部分
        exercise = re.sub(r'答案：\n.*?(?:\n|$)', new_answer, exercise, flags=re.DOTALL)

        return exercise

    def save_exercises(self, exercises: List[str], filename: str = None) -> str:
        """
        保存练习到文件

        Args:
            exercises: 练习列表
            filename: 文件名，如果为None则自动生成

        Returns:
            保存的文件路径
        """
        # 确保 dist 目录存在
        dist_dir = "dist"
        os.makedirs(dist_dir, exist_ok=True)

        if not filename:
            mode_name = EXERCISE_MODES[self.config["mode"]]
            theme = self.config["theme"]
            if theme == "random":
                theme = "随机主题"
            filename = f"{mode_name}_{self.config['grade']}_{theme}.json"

        # 构建完整的文件路径
        filepath = os.path.join(dist_dir, filename)

        # 保存为JSON格式
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "config": self.config,
                "exercises": exercises,
                "generated_at": str(datetime.now())
            }, f, ensure_ascii=False, indent=2)

        print(f"已保存到: {filepath}")
        return filepath

    def print_exercises(self, exercises: List[str]):
        """打印练习内容"""
        mode_name = EXERCISE_MODES[self.config["mode"]]
        print(f"\n=== 生成的{self.config['exercise_count']}篇{mode_name} ===")

        for idx, exercise in enumerate(exercises, 1):
            print(f"\n----- 第 {idx} 篇 -----")
            print(exercise)
            print("-" * 30)

        print(f"\n💡 提示：每篇练习都包含了答案，方便家长参考。")
        print(f"📝 打印时答案会自动分离，练习内容在上方，答案在下方。")


def main():
    """主函数"""
    # 创建生成器实例
    generator = ExerciseGenerator()

    # 生成练习
    exercises = generator.generate_exercises()

    if not exercises:
        print("生成失败，请检查配置和模型连接")
        return

    # 保存到文件
    generator.save_exercises(exercises)

    # 打印内容
    generator.print_exercises(exercises)


if __name__ == "__main__":
    main()
