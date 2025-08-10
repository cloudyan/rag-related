## 2025-08-10

- 更新 `RAG开发环境准备.md`：完善依赖安装指南，推荐使用 Conda 管理虚拟环境、uv 安装依赖。
  - 新增 macOS 安装 uv 的步骤与验证命令
  - 新增 Homebrew 安装 uv 方式
  - 新增在 Conda 环境中使用 `uv pip install/sync` 的示例
  - 新增 `--python "$(which python)"` 用于显式指定解释器的可选参数
  - 新增国内镜像（清华）示例参数 `-i https://pypi.tuna.tsinghua.edu.cn/simple`
  - 新增常用操作（升级、列包、本地 venv 可选）
  - 保留 pip 兜底方案
  - 新增平台兼容性说明：macOS 不安装 `triton` 与 `nvidia-*` 包，并给出缓存清理与同步命令

- 更新 `src/00-simple-rag/requirements.txt`：为 `triton` 与全部 `nvidia-*` 依赖添加平台条件，仅在 Linux x86_64 安装，避免 macOS 解析失败。

- 更新 `RAG开发环境准备.md`：补全“运行项目”章节
  - 明确 Conda 环境与 uv 同步依赖的先决步骤
  - 深入说明 `DEEPSEEK_API_KEY` 的配置方式（export 与 .env 差别）
  - Ollama 本地模型准备与运行指引（serve、pull）
  - 三个示例的运行命令与注意事项（LangChain/DeepSeek、LangChain/Ollama、LangGraph/DeepSeek）
  - 常见问题与网络说明
  - 新增“确保正确 Python 版本（Conda 环境绑定）”排查与修复：
    - 使用 `which python`、`python -c ...` 校验
    - `conda init zsh && exec $SHELL` 重新初始化
    - 使用 `conda run -n rag` 与 `uv --python "$(conda run -n rag which python)"` 的稳健运行与安装


