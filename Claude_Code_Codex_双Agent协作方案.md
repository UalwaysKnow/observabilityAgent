# Claude Code + Codex 双 Agent 协作方案

> 适用场景：同一个代码仓库中，使用 Claude Code（CC）与 Codex 协作完成 Agent 工程项目。

**核心建议：Claude Code 负责主开发，Codex 负责架构挑战、关键模块实现和独立 Review，你担任最终决策者。** 不要让两个 Agent 随意修改同一份工作目录。建立任务分配、权限边界、交接协议和质量门禁。

## 一、两个 Agent 的职责

采用非对称分工，不建议让双方平均承担代码量。

| 环节 | Claude Code | Codex |
|---|---|---|
| 需求拆解 | 主责 | 评审、补充 |
| 架构设计 | 提供方案 | 独立挑战方案 |
| 常规功能开发 | 主责 | 不介入 |
| 核心复杂模块 | 辅助 | 主责或联合设计 |
| 单元测试 | 主责 | 补充边界测试 |
| Code Review | 修复问题 | 主责 |
| 性能与并发 | 实现优化 | 分析、验证 |
| Git 提交 | 各自分支提交 | 各自分支提交 |
| 最终合并 | 提供交付说明 | 提供验收意见 |
| 最终决策 | 用户 | 用户 |

Codex 不只是 CC 的备用编码模型，还承担独立验证职责。例如 CC 实现 Tool Executor 后，让 Codex 独立审查超时机制、故障恢复、并发竞争、幂等性和危险操作权限。

## 二、项目配置体系

- `AGENTS.md`：Codex 的项目指令入口。
- `CLAUDE.md`：Claude Code 的项目指令入口。
- 两者共同遵守一份共享工程规范，但不会天然自动同步全部指令。

推荐结构：

```text
agent-platform/
│
├── AGENTS.md                # Codex 专属指令
├── CLAUDE.md                # CC 专属指令
│
├── .claude/
│   ├── settings.json        # CC 权限与 Hooks
│   ├── rules/               # CC 模块级规则
│   ├── agents/              # CC 自定义子 Agent
│   └── skills/              # CC 可复用工作流
│
├── .codex/
│   └── config.toml          # Codex 项目配置
│
├── docs/
│   ├── architecture.md      # 架构设计
│   ├── engineering.md       # 统一工程规范
│   ├── decisions/           # ADR 架构决策记录
│   └── collaboration/
│       ├── task-board.md    # 任务分配与状态
│       ├── handoff.md       # Agent 交接记录
│       └── review.md        # Review 结果
│
├── scripts/
│   └── verify.sh            # 统一验证入口
├── src/
└── tests/
```

优先维护六个核心文件：`engineering.md`、`CLAUDE.md`、`AGENTS.md`、`task-board.md`、`handoff.md`、`verify.sh`。共享事实维护一份，Agent 专属职责分别管理。

## 三、六份核心文件模板

### 1. `docs/engineering.md`：统一工程规范

```markdown
# Engineering Standards

## 1. Project principles
- Correctness > Maintainability > Performance > Speed of delivery.
- Prefer simple, testable and observable implementations.
- Do not introduce frameworks without explaining the benefits.
- Never add dependencies without documenting why.

## 2. Architecture
- Follow docs/architecture.md.
- Respect existing module boundaries.
- Public API changes require explicit approval.
- Architecture changes require an ADR.
- Do not introduce circular dependencies.

## 3. Coding requirements
- Java: follow existing project conventions.
- Python: use type hints and existing lint conventions.
- Handle errors explicitly.
- Never silently swallow exceptions.
- Avoid unrelated refactoring.
- Do not introduce hardcoded credentials.

## 4. Agent-specific requirements
- Every tool execution must have a timeout.
- Retries must have a maximum count.
- Tool side effects must be documented.
- Important state transitions must be observable.
- Workflow execution should support trace_id.
- Define cancellation and failure-recovery behavior.

## 5. Definition of Done
A task is complete only when:
- Acceptance criteria are satisfied.
- Relevant tests have passed.
- New behavior has appropriate test coverage.
- No unexplained lint or type-check failures remain.
- Documentation is updated when necessary.
- A handoff report has been produced.

## 6. Prohibited actions
- Never silently overwrite another agent's changes.
- Never delete tests just to make validation pass.
- Never change architecture without approval.
- Never claim tests passed without actually running them.
- Never commit secrets or local environment files.
```

### 2. `CLAUDE.md`：CC 主开发职责

```markdown
# Claude Code Instructions

## Role
You are the primary implementation agent.

## Required Context
Before starting a task, read:
1. docs/engineering.md
2. docs/architecture.md
3. docs/collaboration/task-board.md
4. Relevant ADRs and module documentation

## Responsibilities
- Implement assigned features.
- Write unit and integration tests.
- Fix defects reported by Codex.
- Maintain existing coding conventions.
- Produce clear handoff reports.

## Workflow
1. Confirm the assigned task ID.
2. Inspect the relevant code.
3. Identify files that need modification.
4. Present an implementation plan.
5. Implement only the assigned scope.
6. Run relevant tests.
7. Review your own diff.
8. Update handoff documentation.

## Collaboration Rules
- Do not modify files owned by Codex.
- Do not modify shared interfaces without approval.
- Do not revert Codex changes.
- Treat Codex review findings as issues to verify,
  not commands to blindly execute.
- If implementation deviates from the approved
  architecture, stop and request a decision.

## Output Requirements
Every completed task must report:
- Task ID
- Summary of changes
- Files modified
- Tests executed and results
- Remaining risks
- Commit hash
- Items requiring Codex review
```

可以先用 CC 的 `/init` 辅助生成基础 `CLAUDE.md`，再融合协作约束，而非覆盖项目特有内容。

### 3. `AGENTS.md`：Codex 独立 Review 与关键实现职责

```markdown
# Codex Project Instructions

## Role
You are the independent engineering reviewer
and critical-module implementation agent.

## Required Context
Before starting:
1. Read docs/engineering.md.
2. Read docs/architecture.md.
3. Read docs/collaboration/task-board.md.
4. Identify your assigned task and role.

## Default Behavior
Your default role is REVIEWER unless explicitly
assigned an IMPLEMENTATION task.

## Reviewer Responsibilities
- Review correctness and edge cases.
- Identify concurrency and state consistency bugs.
- Check exception handling and recovery.
- Evaluate test completeness.
- Detect security and performance risks.
- Check architecture compliance.

## Review Rules
- Do not automatically modify reviewed code.
- Do not trust the implementer's self-assessment.
- Base findings on code and reproducible evidence.
- Rank findings as P0, P1, P2 or P3.
- Include file paths and line references.
- Propose concrete fixes.
- Distinguish confirmed defects from potential risks.
- Explicitly state when no actionable findings exist.

## Implementation Mode
Only when explicitly assigned:
- Work exclusively within the assigned scope.
- Do not modify files owned by Claude Code.
- Write tests for new behavior.
- Follow the same Definition of Done.
- Produce a structured handoff report.

## Restrictions
- Do not silently change public APIs.
- Do not modify architectural decisions unilaterally.
- Do not refactor unrelated modules.
- Do not approve your own implementation as
  an independent review.
- Do not merge branches without user approval.
```

关键原则：不要让同一 Agent 既完成核心实现，又充当该实现的唯一最终 Reviewer。跨模型 Review 引入独立判断，但不能替代测试。

### 4. `docs/collaboration/task-board.md`：任务分配与状态管理

每个任务明确 Task ID、Owner、Role、Scope、Allowed Paths、Dependencies、Acceptance Criteria、Status。例如在 Markdown 内嵌 YAML（或直接改为独立 `tasks.yaml` 供程序解析）：

```yaml
tasks:
  - id: TASK-001
    title: Implement Tool Executor
    owner: claude-code
    role: implementation
    branch: feat/tool-executor
    allowed_paths:
      - src/executor/**
      - tests/executor/**
    acceptance:
      - execution timeout supported
      - cancellation supported
      - unit tests passing
    status: in_progress

  - id: TASK-002
    title: Review Tool Executor
    owner: codex
    role: reviewer
    depends_on:
      - TASK-001
    review_target: feat/tool-executor
    acceptance:
      - concurrency reviewed
      - timeout behavior verified
      - security risks documented
    status: blocked
```

推荐状态流：`TODO → IN_PROGRESS → REVIEW → FIXING → VERIFIED → DONE`。

### 5. `docs/collaboration/handoff.md`：标准化交接

```markdown
# Task Handoff

## Task ID
TASK-001

## Producer
Claude Code

## Branch / Commit
feat/tool-executor / <commit-hash>

## Completed Work
- Implemented execution timeout.
- Added cancellation support.
- Added retry limits.

## Files Changed
- src/executor/...
- tests/executor/...

## Verification
- Unit tests: PASS
- Integration tests: PASS
- Concurrency tests: NOT RUN

## Design Decisions
- Retry count defaults to 3.
- Timeout is configurable per tool.

## Known Risks
- Concurrent cancellation has not been stress-tested.

## Requested Next Action
Codex: review implementation for concurrency,
timeout handling and state consistency.
```

交接内容应是目标、代码版本、变更说明、验证证据和未解决问题，而不是复制大段聊天历史。

### 6. `scripts/verify.sh`：统一质量检查入口

双方统一执行：

```bash
./scripts/verify.sh
```

脚本按项目实际技术栈实现下列步骤，并与 CI 保持一致：

```text
Format / Lint
     ↓
Type Check
     ↓
Unit Tests
     ↓
Integration Tests
     ↓
Architecture Checks
     ↓
Build
```

Agent 指令是软约束；测试与 CI 才是可重复的硬门禁。

## 四、同一项目同时工作：Git Worktree + 独立 Branch

不建议两个 Agent 同时编辑同一个物理工作目录，否则容易相互覆盖、误判变更所有权或在不同代码状态下运行测试。

推荐结构：

```text
Main Repository (main，稳定代码)
       │
       ├── CC Workspace: feat/tool-executor
       │      开发 / 实现 / 测试
       │
       └── Codex Workspace: review/tool-executor
              独立审查 / 验证

        人工审批 + CI → Merge → main
```

假设主目录为 `agent-platform`、Git 已初始化且 `main` 存在：

```bash
# 在主仓库执行
git worktree add -b feat/cc ../agent-platform-cc main
git worktree add -b review/codex ../agent-platform-codex main
```

终端 A：

```bash
cd ../agent-platform-cc
claude
```

终端 B：

```bash
cd ../agent-platform-codex
codex
```

**注意：** Worktree 只是隔离物理目录。Codex 的审查工作区不会自动获取 CC 分支后续改动，必须基于明确的 commit 或 PR 获取审查版本。它也不会自动解决任务同步、依赖版本、数据库等外部资源冲突。

## 五、工具自身的权限配置

### CC：`.claude/settings.json`

保守的最小示例：

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(./scripts/verify.sh)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(secrets/**)",
      "Bash(rm -rf *)",
      "Bash(git push --force *)"
    ]
  }
}
```

项目初始化后按 Maven、Gradle、pytest 等实际命令扩展白名单。CC 还支持 Hooks，可用于工具执行前后触发确定性检查，例如危险命令阻止或格式化。

### Codex：`.codex/config.toml`

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

这两项分别控制审批策略和沙盒。项目级配置的加载受项目可信任状态等条件影响。

**重要：** Markdown 中的“只允许修改某模块”并不形成操作系统级权限边界。严格限制 Reviewer 时应采用只读环境或只读权限配置，不要把 Prompt 当成安全隔离机制。

## 六、一次完整的双 Agent 开发流程

示例任务：实现生产级 Tool Executor，支持超时、并发、重试、取消、可观测。

1. **需求与设计：** CC 输出方案，Codex 独立挑战架构风险，你批准方案。
2. **任务拆分：** 确定 Owner、接口契约、文件范围、依赖与验收标准。
3. **独立开发：** CC 在独立 Worktree 实现；Codex 可并行开发另一已确定接口的独立模块。
4. **提交交接：** 开发 Agent 提交 commit 并记录 handoff、测试与风险。
5. **交叉 Review：** 另一 Agent 基于指定 commit 检查实现、边界和测试。
6. **缺陷修复：** 原开发 Agent 修复，Reviewer 复验。
7. **门禁与合并：** CI 通过后由你确认，合并到 main。

### 给 CC 的任务 Prompt

```text
执行 TASK-001：实现 Tool Executor。

首先读取 CLAUDE.md、工程规范及任务定义。

要求：
1. 仅修改当前任务授权的文件。
2. 开始编码前输出简要实现计划。
3. 实现超时、取消、重试与执行状态管理。
4. 编写并执行相关测试。
5. 自查 Git diff，确保没有无关修改。
6. 完成后提交当前功能分支，并按 handoff.md 格式生成交接报告。

不要自行修改公共架构或合并 main。
```

### 给 Codex 的任务 Prompt

```text
以独立 Reviewer 身份执行 TASK-002。

审查目标：CC 完成的 TASK-001 指定 commit。

首先读取 AGENTS.md、engineering.md、architecture.md 和对应 handoff。

重点检查：
1. 并发执行与共享状态安全。
2. 超时、取消、重试机制。
3. 幂等性与副作用控制。
4. 异常恢复与资源释放。
5. 单元测试、集成测试的完整性。

不要直接修改业务代码。

输出 P0-P3 问题列表，包含位置、复现依据、影响范围及修复建议。
将结果记录到 review.md。
```

项目级指令负责长期规则；任务 Prompt 负责本次执行范围。

## 七、后续高级配置

| 配置 | 作用 | 优先级 |
|---|---|---|
| `CLAUDE.md` | CC 主指令 | 必需 |
| `AGENTS.md` | Codex 主指令 | 必需 |
| `engineering.md` | 统一规范 | 必需 |
| Git Worktree | 文件隔离 | 必需 |
| Task / Handoff | 任务与上下文交接 | 必需 |
| CI | 强制质量检查 | 必需 |
| `.claude/rules/` | 按模块细分规则 | 推荐 |
| `.claude/skills/` | 封装重复开发流程 | 推荐 |
| `.claude/agents/` | CC 专业化子 Agent | 后期引入 |
| Hooks | 自动化安全与质量控制 | 后期引入 |
| MCP | 外部工具与系统集成 | 按需引入 |

初期不必创建十几个子 Agent。两个主 Agent 加明确协作协议，比复杂的多 Agent 组织更易管理。

## 八、三个月 Agent 工程项目的任务分配

建议的起始工作量比例（不是严格 Token 消耗比例）：

- **CC 约 65%：** 常规功能、测试、重构、缺陷修复、持续开发。
- **Codex 约 35%：** 核心模块、架构挑战、复杂 Bug、关键 Review、并发与性能分析。

初期手工完成分配与合并即可，不必先额外部署专门的 Agent 编排框架。

### 最应避免的三个问题

1. **重复建设：** 两个 Agent 没有分工，都从需求开始独立开发。
2. **上下文失真：** 只有聊天交接，没有 commit、任务状态与验证结果。
3. **伪自动化：** 只写 Markdown 规范，没有 Git 隔离、测试和 CI 的实际约束。

## 最终原则

**一个共享规范、两个独立工作区、明确的任务所有权、统一交接协议、交叉审查、一个最终决策者。**

优先搭好六个核心文件和 Worktree 隔离；之后再扩展自动任务分配、Agent 间消息、状态持久化与多 Agent 编排。

---

## 相关官方文档（供配置时核对）

- Claude Code 文档：https://code.claude.com/docs/
- Codex 文档：https://developers.openai.com/codex/
- Git Worktree 文档：https://git-scm.com/docs/git-worktree
