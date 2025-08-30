# 错别字纠错练习短文批量生成器

非 uv 项目转为 uv 管理

```bash
# 1. 生成 pyproject.toml（只写依赖，不写构建后端）
uv init --no-package --name legacy_project .

# 2. 把 requirements.in/requirements.txt 里的包搬进来
uv add -r requirements.txt

# 3. 生成锁文件
uv lock
```

后续用 `uv sync` / `uv add` / `uv lock` 即可

```bash
# 执行
cd playground/001-typos
conda activate rag

uv sync  # 安装依赖
uv python gen_typos.py  # 运行脚本

# 1. 生成包含答案的练习
uv run gen_typos.py
# 2. 生成PDF（答案自动分离，双版面设计）
uv run print_module.py
# 3. 生成方格纸模板
uv run grid_paper_template.py
# 4. 测试完整功能
uv run test_with_answers.py
```

## 功能特性

- 🎯 **多种练习模式**：支持错别字纠错练习和用词不当纠错练习
- ⚙️ **配置化管理**：所有参数都可通过环境变量配置
- 🤖 **模型兼容**：支持所有兼容OpenAI接口的模型
- 📚 **年级适配**：根据年级自动调整字数和错误数量
- 🎨 **主题丰富**：内置多种主题，支持随机选择
- 💾 **智能保存**：自动生成有意义的文件名
- 📄 **双版面设计**：A4横放双版面方格纸，适合对折打印
- 🖨️ **专业打印**：自动生成PDF，答案分离，便于教学使用

## 文件结构

```
playground/001-typos/
├── config.py              # 配置文件
├── prompts.py             # 提示词模板
├── model_client.py        # 模型客户端
├── gen_typos.py          # 主程序
├── print_module.py        # 打印模块（双版面设计）
├── grid_paper_template.py # 方格纸模板生成器
├── typo_database.py       # 错别字数据库
├── README.md              # 说明文档
├── README_双版面设计.md   # 双版面设计说明
└── docs/                  # 配置说明文档
```

## 环境配置

复制以下内容到 `.env` 文件：

```bash
# 模型配置
MODEL_NAME=gpt-3.5-turbo
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your-api-key-here

# 模型参数
TEMPERATURE=0.7
MAX_TOKENS=2000

# 默认练习配置
DEFAULT_GRADE=二年级
DEFAULT_THEME=random
DEFAULT_EXERCISE_LENGTH=65
DEFAULT_ERROR_COUNT=5
DEFAULT_EXERCISE_COUNT=2
DEFAULT_MODE=misspelling
```

## 支持的模型

### 1. OpenAI官方
```bash
MODEL_NAME=gpt-3.5-turbo
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 2. DeepSeek
```bash
MODEL_NAME=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

### 3. 智谱AI
```bash
MODEL_NAME=glm-4
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

### 4. 魔搭社区 modelscope
```bash
MODEL_NAME=glm-4
OPENAI_BASE_URL=https://api-inference.modelscope.cn/v1
```

### 5. 本地Ollama
```bash
MODEL_NAME=qwen2.5:7b
OPENAI_BASE_URL=http://localhost:11434/v1
```

## 练习模式

### 错别字纠错练习模式 (`misspelling`)
- 生成包含错别字的短文
- 错别字为字形或音近错字
- 适合基础语文练习

### 用词不当纠错练习模式 (`word_usage`)
- 生成包含用词不当的短文
- 包括词语搭配不当、使用错误等
- 适合进阶语文练习

## 年级配置

系统会根据年级提供参考基准，可上下浮动10%左右：

| 年级 | 建议字数 | 建议错误数量 | 说明 |
|------|----------|--------------|------|
| 一年级 | 40字 | 4个 | 字数36-44字，错误3-5个 |
| 二年级 | 65字 | 5个 | 字数59-72字，错误4-6个 |
| 三年级 | 100字 | 6个 | 字数90-110字，错误5-7个 |
| 四年级 | 125字 | 8个 | 字数113-138字，错误6-10个 |
| 五年级 | 160字 | 10个 | 字数144-176字，错误8-12个 |
| 六年级 | 200字 | 12个 | 字数180-220字，错误10-14个 |

> 💡 **注意**：以上数字仅供参考基准，系统不会强制限制。你可以通过环境变量灵活调整。

## 使用方法

### 1. 基本使用
```bash
uv python gen_typos.py
```

### 2. 自定义配置
```python
from gen_typos import ExerciseGenerator

# 自定义配置
config = {
    "grade": "三年级",
    "theme": "动物园",
    "exercise_length": 100,
    "error_count": 6,
    "exercise_count": 3,
    "mode": "word_usage"
}

generator = ExerciseGenerator(config)
exercises = generator.generate_exercises()
```

### 3. 批量生成不同配置
```python
configs = [
    {"grade": "二年级", "mode": "misspelling"},
    {"grade": "四年级", "mode": "word_usage"},
    {"grade": "六年级", "theme": "图书馆"}
]

for config in configs:
    generator = ExerciseGenerator(config)
    exercises = generator.generate_exercises()
    generator.save_exercises(exercises)
```

## 输出格式

生成的练习会保存为JSON格式，包含：
- 配置信息
- 练习内容
- 生成时间

文件名格式：`{练习模式}_{年级}_{主题}.json`

## 双版面设计

### 🎯 设计特点
- **A4横放**：210mm × 297mm，适合对折打印
- **双版面**：左右各一个32k版面，每版面10行10列
- **答案分离**：答案在版面下方，便于家长参考
- **专业打印**：自动生成PDF，支持批量打印

### 📱 使用方法
1. **生成练习**：`uv run gen_typos.py`
2. **生成PDF**：`uv run print_module.py`
3. **生成模板**：`uv run grid_paper_template.py`

### 🖨️ 打印说明
- 选择A4横放打印
- 打印完成后沿中线对折
- 每个版面适合一篇练习短文
- 底部预留空间可用于手写答案

> 📖 **详细说明**：查看 [README_双版面设计.md](README_双版面设计.md) 了解完整设计细节

## 依赖安装

```bash
uv add openai python-dotenv
```

## 注意事项

1. 确保API密钥有效且有足够额度
2. 主题设置为`random`时会随机选择主题
3. 系统会自动验证配置参数的有效性
4. 生成的练习会自动按年级调整难度
5. 支持自定义保存文件名

## 📚 相关文档

- [README_重构说明.md](README_重构说明.md) - 重构过程说明
- [README_双版面设计.md](README_双版面设计.md) - 双版面方格纸设计说明
- [CONFIG_PRIORITY.md](docs/CONFIG_PRIORITY.md) - 配置系统完整说明（优先级设计 + 变量重构）
- [README_核对检查.md](README_核对检查.md) - 内容验证和自动修正功能说明
