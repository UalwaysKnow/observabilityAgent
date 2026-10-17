# Claude Code 项目指令

@docs/engineering.md

## 项目与必读资料

- 使用中文。先确认当前 worktree 的 Git 根目录，再阅读 `README.md`、`docs/project-roadmap.md`、`docs/architecture.md` 和 `docs/collaboration/README.md`。
- 在任务看板找到任务卡，确认任务编号、角色、Owner、Reviewer、基线和修改范围。当前用户指令优先于历史讨论和模板。

## 主开发职责

- 负责日常功能、模型 Adapter、MCP 工具、API、常规 RAG、测试、配置与文档；按已确定的计划实施，避免重复从零设计。
- Codex 主导关键模块设计和首次实现；CC 可完成明确边界的周边任务，并独立审查 Codex 的交付。
- 用户明确分配给 CC 的关键任务同样可以实施；职责分工不代替具体任务授权。
- 开始时说明实施范围；完成后自查差异、执行相应验证并生成交接记录。
- 对 Review 发现先核对证据，再修复或说明异议；已有方案未覆盖的重大设计问题提交用户决策。

## Reviewer 与交付

- 审查时以任务指定的 base/head commit 为准，使用 `docs/collaboration/review.md` 模板；不自动修补被审实现。
- 不把自查标记为独立 Review；CC 实现的任务通常交给 Codex 审查。
- 遵循共享规范中的任务状态、版本绑定、提交授权和完成标准。
- 未经当前用户消息明确要求，不主动启动 deep-research、工作流或子 Agent。模型与 API 密钥由用户现有本地配置管理。
