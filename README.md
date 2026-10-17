# observabilityAgent

面向 K8s 故障诊断和沙箱运维任务的 Agent 工程化个人项目，重点建设可恢复的 Agent Runtime、Context Engineering 和 Evaluation Harness。

当前阶段：Python 工程骨架，已提供最小 HTTP 存活检查与开发检查配置。Agent 与实验环境仍待实现。整体规划为 12 周、标准投入 225 小时，第 13 周可作缓冲；每阶段任务和验收标准见项目整体规划。

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

本地与 CI 共用一个入口；脚本会定位自身所在工作区，可从项目内任意目录调用：

```bash
./scripts/verify.sh
# 在 src 子目录中：
../scripts/verify.sh
```

依次执行锁定依赖安装、Ruff、mypy、pytest、构建及仓库外 wheel 安装检查；需要可用的 uv 和依赖下载网络。CI 固定 uv 0.12.23，本地优先保持一致。验证脚本不调用模型 API，也不自动改写格式。

需要格式化时使用 `uv run ruff format .`。新增依赖使用 `uv add 包名`，开发依赖使用 `uv add --dev 包名`，并提交更新后的 `pyproject.toml` 和 `uv.lock`。

## 双 Agent 协作

CC 负责日常开发，Codex 负责关键实现与独立 Review，用户负责最终决策和合并。按 [协作指南](docs/collaboration/README.md) 在独立 worktree 中执行任务，交接绑定具体 commit。任务分配可由用户当前指令调整。

两个指令入口分别是 [AGENTS.md](AGENTS.md) 和 [CLAUDE.md](CLAUDE.md)，共同遵循 [共享工程规范](docs/engineering.md)。当前仅建立协作基础，两个工作区与跨工具演练须在共享基线提交后执行，尚未完成独立 CC Review。

## 项目文档

- [项目整体规划 v1.0](docs/project-roadmap.md)：当前执行基准，包含 12 周排期、阶段任务、验收标准、实验和开发工具分工。
- [早期技术方案 v0.2（历史参考）](docs/project-plan.md)：保留早期业务场景、数据来源与技术讨论；冲突内容以整体规划为准。
- [开发骨架与提交边界](docs/development.md)：工程选择、模块职责与下一步开发顺序。
- [系统架构设计 v1.0](docs/architecture.md)：总体架构、模块边界、数据流、恢复、上下文与评测；[Word 阅读版](docs/architecture-design-v1.0.docx)。
- [架构复审记录](docs/architecture-review-2026-10-17.md)：完整性核对、边界歧义与修订建议。
- [架构讨论原文归档](docs/discussions/2026-10-17-architecture-discussion-verbatim.md)：保留消息原文、时间戳与选项问答。
- [协作任务索引](docs/collaboration/task-board.md)
- [架构决策记录](docs/decisions/README.md)
- [三个月项目规划讨论记录](agent_project_plan_3months.md)
- [模型分工与开发流程讨论记录](Agent工程_模型分工与开发流程整合.md)
- [双 Agent 协作讨论记录](Claude_Code_Codex_双Agent协作方案.md)
- [项目协作规则](AGENTS.md)

本仓库是该个人项目的开发根目录。后续方案、代码、实验结果和讨论记录均在此维护。
