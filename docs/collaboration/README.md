# Codex 与 Claude Code 长期协作指南

执行依据：[整体规划](../project-roadmap.md)、[共享工程规范](../engineering.md)、[当前与目标架构](../architecture.md)。原始参考为 [双 Agent 讨论记录](../../Claude_Code_Codex_双Agent协作方案.md)。本文将讨论中的建议落实为本项目操作约定，不自动启用讨论示例里的配置或工作流。

## 分工

| 工作 | 主负责人 | 独立审查 |
|---|---|---|
| 日常功能、Adapter、MCP 工具、API、常规 RAG、测试与文档 | CC | Codex |
| Runtime、Context、Evaluation 关键设计与实现、复杂跨模块问题 | Codex | CC |
| 任务分配、重要设计决策、最终验收与合并 | 用户 | 两个 Agent 提供证据 |

以上是默认分工，用户当前任务授权可调整 Owner。自查不等于独立 Review；不会将同一 Agent 换会话后的自查冒充交叉审查。

## 指令与文档入口

Codex 读取根目录 `AGENTS.md`，CC 读取 `CLAUDE.md` 并导入共享工程规范。两个入口保存各自职责，共享事实在工程规范、架构和任务卡中维护。

- [任务索引](task-board.md)：只索引，不复制任务状态。
- [任务卡模板](task-template.md)：保存唯一任务状态与范围。
- [交接模板](handoff.md)：复制成独立交接记录。
- [Review 模板](review.md)：复制成绑定 base/head 的独立报告。
- [ADR 索引与模板](../decisions/README.md)：记录重要设计决策。

`tasks/<任务编号>.md` 保存任务卡；`handoffs/<任务编号>-<实现短SHA>.md` 和 `reviews/<任务编号>-<实现短SHA>.md` 保存版本化记录。未提交的本轮草稿使用 `working-tree` 后缀，SHA 标为待补充，不进入已审查状态。

## 先建立共享基线

整体规划、原始讨论资料与协作基础已于 2026-10-17 纳入实现基线 `cfffc33db7606070b0fccb1bd07f81ec6dd3a068`。创建工作区前仍应检查共享改动已提交；`git worktree add` 只检出提交，不携带主目录未提交和未跟踪文件。

本轮交付协作文件与启动指南。创建工作区和跨工具演练的验收状态单独记录，不能因文档已生成就标记已完成。

## 一次性创建两个工作区

在主仓库执行，先检查现状，确认共享文件已纳入基线、目标目录尚不存在：

```bash
git status --short
git worktree list
git worktree add --detach ../observabilityAgent-cc main
git worktree add --detach ../observabilityAgent-codex main
```

三个目录是主仓库、CC 工作区和 Codex 工作区。既有工作区适合当前任务时直接复用；不可覆盖现有目录或为切换目标而丢弃改动。

在每个工作区根目录分别安装自己的依赖：

```bash
uv sync --locked
```

`.venv`、`.env` 与运行产物不共享。服务从所在工作区根目录启动；如需本地配置，由用户在各自目录维护，不把密钥复制进交接文件。后续数据库、Compose 项目和端口通过任务配置分配，当前尚未实现这些资源。

两个终端分别从主仓库目录出发启动工具：

```bash
# 终端 A
cd ../observabilityAgent-cc
claude
```

```bash
# 终端 B
cd ../observabilityAgent-codex
codex
```

也可在 Codex 应用中打开对应 worktree。开始任务时让工具说明当前 Git 根目录、HEAD、任务编号和角色，并确认已经读取对应指令与共享规范；不要在未指定任务时让两者各自规划同一个实现。

## 领取与实现任务

用户或指定的集成任务维护看板索引和任务分配，Owner 维护自己的任务卡。不要让两个 Agent 同时编辑同一任务卡或公共看板。

开始时确认 Git 根目录、工作区是否干净、任务 Owner、依赖与基线。下面是命名示例，任务编号和基线应替换为任务卡里的实际值：

```bash
git rev-parse --show-toplevel
git status --short
git switch -c task/EXAMPLE-001-cc <base_sha>
```

实现只覆盖任务卡允许的路径，明确的接口变更按已授权方案执行。遇到新的重大设计问题，记录 ADR 草案并提交用户决策，继续不受影响的工作。

任务状态流：`TODO → IN_PROGRESS → REVIEW → FIXING／VERIFIED → DONE`。阻塞使用 `BLOCKED`，记录原因和恢复到哪个状态。

## 指定版本交接与 Review

1. 实现者运行检查、自查差异。用户已授权提交时创建实现 commit；否则保留改动并明确标注“待提交”，不伪造 SHA。
2. 取得实现 SHA 后，按交接模板记录 base/head、修改、验证、风险和请求。交接文档可以在后续文档提交中引用实现 SHA，避免提交哈希自引用。
3. Reviewer 确认自己的工作区干净，检出完整实现 SHA：`git switch --detach <head_sha>`；用 `git diff <base_sha> <head_sha>` 审查，不对移动中的分支名给出无限期结论。
4. Reviewer 使用 Review 模板记录确认缺陷、待验证风险、实际检查和结论。报告与目标 SHA 对应；Reviewer 不自动修改被审业务代码。
5. 需要通过 Git 传递报告时，在该版本上创建 `review/<任务编号>-<短SHA>` 分支；用户授权后仅提交报告。实现者按明确的报告提交引入报告，避免顺便合并另一任务的业务改动。
6. 实现者修复并产生新实现 SHA 后，更新交接和审查目标。业务、依赖、配置或验收行为变化必须复验；单纯交接或索引文档变更单独说明。
7. 无未解决阻断项且验收证据齐全时进入 VERIFIED；经用户确认合并并运行集成检查后进入 DONE。主线变化引起冲突或行为改变时重新验证。

本地 worktree 共用 Git 对象，提交后可按 SHA 查找；远程工作环境需显式传输分支或提交。文件、任务状态、依赖安装和外部资源都不会自动同步。

## 验证入口与记录

```bash
./scripts/verify.sh
# 从 src 子目录执行时：
../scripts/verify.sh
```

脚本定位自身所在工作区，安装锁定依赖并执行检查、测试、构建及仓库外 wheel 安装验证。缺少 uv、网络或依赖时保留失败记录；脚本不会跳过错误或自动改写格式。

验收应区分：应用工厂/ASGI 请求、真实服务进程、lifespan、外部服务连接。当前仅实现前两者中的工厂/请求检查，不宣称完整启动过程已验证。

## 最小协作演练（基线提交后执行）

领取一个独立的小任务 → Owner 在自己的 worktree 实现 → 记录实现 SHA 与交接 → 另一 Agent 检出该版本 Review → Owner 处理发现 → 新版本复验 → 用户确认合并。

记录两个工作区路径和实际 HEAD、双方工具/角色、检查命令、发现和最终结果。若没有发现，不人为制造缺陷；修复流程可在后续真实发现中验证并记录未覆盖项。尚未调用 CC 或完成 Review 时必须写“待执行”。

## 权限与后续扩展

`.claude/settings.json` 和 `.codex/config.toml` 控制各自工具配置，其具体行为以安装版本和实际生效环境为准。本轮保留已有权限配置，不从讨论示例直接复制白名单或审批策略；不读取或更改个人模型密钥。

任务范围和 Markdown 是行为约定，不是文件系统强制隔离。需要严格只读 Reviewer 时另行配置受限环境。`.claude/rules/`、子 Agent、Skills、Hooks 等待出现明确需求后处理；未经当前用户消息明确要求，不主动启用自动工作流、deep-research 或子 Agent。

本机目前未在 PATH 中找到 uv，日常使用需先安装与 CI 一致的版本。开发工具的模型选择与运行时模型调用分别管理。

参考：[Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[Claude Code 项目记忆](https://code.claude.com/docs/en/memory)、[Git worktree](https://git-scm.com/docs/git-worktree)、[HTTPX ASGI transport](https://www.python-httpx.org/advanced/transports/)。
