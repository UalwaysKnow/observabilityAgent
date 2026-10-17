# 开发骨架与首个开发提交

首个开发提交的验收目标：新环境能安装锁定依赖，导入已安装的包，提供 HTTP 入口，并通过格式、静态检查、应用创建与请求检查和打包检查。现有自动化检查未启动真实 HTTP 进程，也未驱动 lifespan。

建议提交信息：`chore: bootstrap Python project with uv, FastAPI and CI`。

## 工程选择

- 使用 Python 3.11 作为当前开发与 CI 基线，匹配本机现有环境。pyproject 声明最低版本为 3.11，其他版本兼容性需在扩展 CI 后验证。
- 使用 uv 管理虚拟环境与依赖，`pyproject.toml` 声明依赖范围，`uv.lock` 保存解析出的精确版本，二者一起提交。参见 [uv 项目结构](https://docs.astral.sh/uv/concepts/projects/layout/)。
- 使用 `src/observability_agent/` 放置可安装代码，测试通过安装后的包导入，避免依赖仓库根目录或手工修改 `sys.path`。参见 [PyPA 的 src 布局说明](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)。
- FastAPI 使用应用工厂，初始化在创建应用时发生。当前 `/healthz` 只检查进程可响应，后续外部依赖就绪检查另行设计。
- `pydantic-settings` 管理进程配置，环境变量覆盖 `.env`；示例配置可提交，实际 `.env` 忽略。模型配置在实现模型适配时加入。
- Ruff 管理格式与基础静态检查，mypy 检查源码类型，pytest 验证应用创建、请求与配置行为。CI 与本地统一调用 `scripts/verify.sh`。

## 当前目录

以下列出初始骨架；新增协作文件、架构与验证入口见 [协作指南](collaboration/README.md)、[共享工程规范](engineering.md) 和 [架构说明](architecture.md)。

```text
observabilityAgent/
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .gitignore
├── .github/workflows/ci.yml
├── src/observability_agent/
│   ├── __init__.py
│   ├── config.py
│   └── api/
│       ├── __init__.py
│       └── app.py
├── tests/test_bootstrap.py
└── docs/
    ├── project-plan.md
    └── development.md
```

仓库名 `observabilityAgent`、安装包名 `observability-agent`、Python 导入名 `observability_agent` 分别服务于仓库、打包和语言命名习惯。

## 后续模块边界

以下为演进约定，模块在首个真实功能进入时创建：

| 模块 | 责任与依赖方向 |
| --- | --- |
| `contracts/` | Agent 可见任务、证据、可序列化执行事件和结果；保持与 Web 框架及 LangGraph 解耦 |
| `agent/` | LangGraph 状态和 ReAct 循环；调用工具和上下文策略，产生标准事件 |
| `tools/` | MCP 适配与快照查询；执行入参校验、超时处理，返回有来源的结果 |
| `context/` | 从任务、历史和证据构造模型输入；实现完整历史、裁剪、摘要和笔记策略 |
| `evaluation/` | 消费标准轨迹和仅评测端可见的黄金依据，执行规则与 Judge 评分 |
| `datasets/` | 任务包加载、数据划分与版本检查；Agent 输入转换时排除黄金答案 |
| `api/` | HTTP 请求与响应转换；后续离线评测入口可直接调用业务模块 |

Agent 和 Context 模块不得反向依赖 Evaluator 或读取黄金答案。后续可先用普通 Python 函数表达接口，在出现第二个实现时再考虑 Protocol 等抽象。

## 建议的后续提交

1. 任务与轨迹最小契约：一个可人工检查的故障任务包，区分可见证据和黄金依据，验证 JSON 序列化及输入边界。
2. 可查询快照工具：按服务、时间和条件查询固定数据；把同一接口通过 MCP 暴露。
3. 基线 Agent：LangGraph + 一个模型适配器，先跑通一个多步任务，保存执行轨迹；此时加入实际使用的 LangChain/LangGraph 依赖。
4. 最小离线评测：批量运行、规则评分和基线报告，再逐步增加 Judge 与上下文策略实验。

环境接入与数据采集可以同步推进，业务模块围绕第一个任务逐步落地。开发初期每次提交尽量有单一、可验证的结果。

## 本次本地验证

2026-10-06，macOS、Python 3.11.15、uv 0.12.23：

- 已生成 `uv.lock`，使用锁定依赖安装开发环境。
- Ruff 静态检查与格式检查通过；mypy 对 4 个源码文件的严格类型检查通过。
- pytest 的 3 项检查通过且无警告：无模型密钥和外部连接时可创建应用并响应健康请求、环境变量覆盖 `.env`、非法环境配置在创建应用时失败。此记录不包含 lifespan、真实 HTTP 进程或外部服务就绪验证。
- 已构建 sdist 与 wheel，并在仓库之外的隔离环境安装 wheel、成功导入包及创建应用。
- GitHub Actions 工作流已配置；远端 CI 结果须在后续提交推送后确认。

## 统一验证入口（2026-10-17 起）

执行 `./scripts/verify.sh`。脚本定位自身工作区并锁定依赖，完成 Ruff、mypy、pytest，随后在临时目录构建 sdist/wheel，导出锁定运行依赖，创建隔离环境、安装 wheel 并检查应用工厂。

安装包检查在源码目录之外执行，移除 `PYTHONPATH` 并使用 Python 隔离模式，验证导入文件确实来自新环境的 site-packages。它验证可安装性与应用创建，不模拟服务 lifespan。

验证入口的自动化用例使用假 uv 检查工作区定位、带空格路径、失败退出码、提前停止及工具缺失；真实脚本另行验证打包和安装。事实记录见各任务交接，运行记录不会被写成独立 Review。
