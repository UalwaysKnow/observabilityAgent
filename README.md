# observabilityAgent

面向故障诊断的 Agent 工程化个人项目，重点建设轨迹级评测与 Context Engineering 能力。

当前阶段：Python 工程骨架，已提供最小 HTTP 存活检查与开发检查配置。Agent 与实验环境仍待实现。计划在 3—5 个月内逐步迭代，方案随实验结果持续更新。

## 本地开发

使用 Python 3.11 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)。uv 可通过 `brew install uv` 安装。

在仓库根目录执行：

```bash
uv sync --locked
uv run --locked uvicorn observability_agent.api.app:create_app --factory --reload
```

访问 `http://127.0.0.1:8000/healthz`，预期返回 `{"status":"ok"}`。接口文档在 `http://127.0.0.1:8000/docs`。当前启动不需要模型密钥或数据库。

如需自定义配置，复制 `.env.example` 为 `.env` 并修改；环境变量优先于文件。PyCharm 解释器选择本仓库的 `.venv/bin/python`。

## 开发检查

```bash
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest
uv build
```

需要格式化时使用 `uv run ruff format .`。新增依赖使用 `uv add 包名`，开发依赖使用 `uv add --dev 包名`，并提交更新后的 `pyproject.toml` 和 `uv.lock`。

## 项目文档

- [项目方案 v0.2（持续讨论稿）](docs/project-plan.md)：业务场景、数据来源、基线 Agent、评测与上下文策略、复杂度设计及迭代路线。
- [开发骨架与提交边界](docs/development.md)：工程选择、模块职责与下一步开发顺序。
- [项目协作规则](AGENTS.md)

本仓库是该个人项目的开发根目录。后续方案、代码、实验结果和讨论记录均在此维护。
