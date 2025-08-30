"""
错别字纠错练习短文批量生成器模型客户端
支持兼容OpenAI接口的各种模型
"""

import os
from typing import Dict, Any
from openai import OpenAI
from config import MODEL_CONFIG


class ModelClient:
    """模型客户端类，支持兼容OpenAI接口的各种模型"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化模型客户端

        Args:
            config: 模型配置，如果为None则使用默认配置
        """
        self.config = config or MODEL_CONFIG
        self.client = OpenAI(
            base_url=self.config["base_url"],
            api_key=self.config["api_key"]
        )

    def generate_text(self, prompt: str) -> str:
        """
        生成文本

        Args:
            prompt: 提示词

        Returns:
            生成的文本内容
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"模型调用失败: {e}")
            return ""

    def update_config(self, **kwargs):
        """
        更新模型配置

        Args:
            **kwargs: 要更新的配置项
        """
        self.config.update(kwargs)
        # 如果更新了base_url或api_key，重新创建客户端
        if "base_url" in kwargs or "api_key" in kwargs:
            self.client = OpenAI(
                base_url=self.config["base_url"],
                api_key=self.config["api_key"]
            )
