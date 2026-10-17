# 当前架构与目标架构

本文区分实现事实与设计目标。计划与排期以 [整体规划](project-roadmap.md) 为准；重要变更记录在 [ADR 索引](decisions/README.md)。

## 当前实现

现有代码位于 `src/observability_agent/`，只有配置模块和 FastAPI 应用工厂。`/healthz` 返回进程存活响应；没有模型、数据库或工具连接。

已有 pytest 检查配置优先级、非法环境配置和 ASGI 请求。`httpx.ASGITransport` 不自动执行 lifespan，因此这些检查不等同于服务启动和关闭流程验证。

已有 Python 包配置、uv 锁文件、Ruff/mypy 及 CI。统一验证脚本将构建后的 wheel 在仓库外隔离安装。当前未实现 Runtime、Context、Evaluation、Memory、RAG、MCP 或离线业务入口。

## 目标依赖方向（随业务任务落地）

```text
HTTP / CLI / Worker → 任务执行用例 → Runtime
                                     ├── Context Policy → Memory / RAG
                                     ├── Tool Engine
                                     └── Model Gateway

任务执行产生标准轨迹 → Evaluation + 评测端黄金依据 → 实验报告
```

各模块通过明确的输入输出交互。Context 需要模型摘要时也可调用 Model Gateway，不通过 HTTP 或工具引擎绕行。

| 模块 | 责任与边界 |
|---|---|
| 任务与轨迹契约 | Agent 可见任务、证据、状态和事件，可序列化；保持与 HTTP 和 LangGraph 解耦 |
| Runtime | LangGraph/ReAct、执行控制、Checkpoint、恢复；调用上下文策略和工具，输出事件 |
| Context Policy | 按预算选择任务状态、历史、证据与检索结果；支持裁剪、摘要和结构化笔记 |
| Tool Engine | MCP/工具适配、参数校验、超时、重试、执行日志和实际幂等语义 |
| Model Gateway | 统一模型调用、用量、错误和结构化输出，支持切换后端 |
| Memory / RAG | 记忆的更新与隔离、知识检索及来源引用；保留原始证据回取能力 |
| Evaluation | 批量实验、确定性规则和 Judge；读取独立答案、版本化结果与失败分类 |
| HTTP / CLI / Worker | 转换输入输出、调度用例；核心能力不通过 HTTP 绕行调用 |

首个业务切片是“一个可信任务包 → 按条件查询快照 → 多步 Agent → 执行轨迹 → 独立评分”。先明确该切片契约，再按真实实现建立模块目录。

## 骨架审查结论

保留 src 布局、uv 锁定和现有开发工具。HTTP 骨架不作为业务架构已验证的依据；当前无 lifespan，未来管理模型连接或数据库资源时增加相应生命周期验证。

当前配置按工作目录寻找 `.env`，通过每个工作区从根目录启动明确来源。后续 CLI/Worker 的配置传递在对应任务中设计。

统一脚本与 CI 保持一致；构建成功后还要验证分发包可以独立安装。已跟踪的 IDE 配置从版本控制移除，本机文件保留。
