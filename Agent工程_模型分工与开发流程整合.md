# Agent 工程项目：规划机制、模型分工与开发流程（前文整合）

> 以下内容整理自本次聊天前面几轮回答，保留原有建议及其不同阶段的调整，不重新制定方案。

## 一、项目规划机制

对于长期 Agent 工程，不应只依赖一种 Plan。

### L1：技术方向规划 — ChatGPT Chat

**解决 Why / What**

- 为什么要做这个功能？
- 用什么技术路线？
- 是否需要引入新框架？
- 评测体系如何证明方案有效？
- 哪些技术值得作为求职项目亮点？

### L2：工程架构规划 — Codex Plan

**解决 How / Where**

- 阅读真实 Repo
- 明确模块边界和依赖关系
- 确定接口、类、Schema
- 分析现有代码需要修改哪些地方
- 给出实施顺序与验收条件

### L3：编码与执行 — Claude Code + DeepSeek

**解决 Implement / Test**

- 按照计划完成模块
- 运行测试并修复
- 更新文档
- 提交代码
- 生成交付记录

**ChatGPT 用来挑战你的设计思路，Codex 用来理解并设计真实工程，Claude Code 用来高频执行。**

Work 可以在需要跨大量资料完成研究、生成报告或交付成果时使用。单纯基于现有 Repo 规划代码，直接选择 Codex Plan 更合适。

## 二、Codex Plan 与 Claude Code 的交互方式

不要让 Codex 完成 Plan 后，再将整段对话复制给 Claude Code。应该让它们通过仓库文件交接。

**交接流程：**

1. **Codex Plan：** 阅读 Repo → 完成工程设计 → 生成实施计划。
2. **共享设计文档：** `docs/plans/context-manager.md`。
3. **Claude Code + DeepSeek Flash：** 读取计划 → 分阶段实现 → 测试 → 提交。
4. **Codex Review：** 对照原计划检查实现、测试和架构偏差。

### Codex Plan 提示词（前文原文）

```text
请进入 Plan 模式，针对当前 Agent 工程项目进行模块设计。

本次目标：实现 Agent Context Manager。

首先阅读当前代码仓库、AGENTS.md、现有架构文档和测试代码。

要求：
1. 分析目前架构和现有模块的依赖关系。
2. 提出本功能的技术设计方案。
3. 明确需要新增、修改和保持不变的文件。
4. 给出核心接口、数据结构、调用流程。
5. 分析与 Runtime、Memory、RAG 的交互。
6. 给出潜在风险及替代设计。
7. 设计单元测试、集成测试和验收标准。
8. 将实施工作拆分为可独立验收的任务。

请先不要修改业务代码，也不要开始实现。

输出完整实施计划，供我确认后交给另一个 Coding Agent 执行。
```

### Claude Code 接力提示词（前文原文）

```text
请阅读 docs/plans/context-manager.md，并按照其中的实施计划开发。

要求：
- 每次只实现一个 Milestone。
- 不擅自修改已经确定的架构和公共接口。
- 每完成一个 Milestone，运行对应测试。
- 对于计划中没有定义的重大设计问题，停止相关实现并说明原因。
- 更新开发进度文档。
- 不要在未经确认的情况下扩大需求范围。
```

## 三、开发流程每个环节的模型与工具

以下为前文“最终整合：GPT Plus + DeepSeek 的完整分工”原表：

| 项目工作 | 首选模型 | 使用入口 |
|---|---|---|
| Agent 技术原理学习 | GPT-6 Medium | Chat |
| 研究 Context Engineering 策略 | GPT-6 High | Chat |
| 设计 Agent Evaluation 方法论 | GPT-6 High | Chat |
| 重要技术方案交叉验证 | GPT-5.6 Sol | Chat |
| 项目首次整体工程架构 | GPT-6 Astra | Codex Plan |
| 新模块详细设计 | GPT-6.1 Sol High | Codex Plan |
| Runtime 核心状态机首次编码 | GPT-6.1 Sol High | Codex |
| Context Manager 核心算法 | GPT-6.1 Sol High | Codex |
| Evaluation Runner 核心逻辑 | GPT-6.1 Sol High | Codex |
| 普通功能、Adapter、API | DS V4.1 Flash | Claude Code |
| RAG、Memory 常规开发 | DS V4.1 Flash | Claude Code |
| 测试生成、文档整理 | DS Flash / GPT-6 Luna | CC / Codex |
| Flash 遇到较复杂的问题 | DS Flash Max | Claude Code |
| 特定任务需要独立对照 | DS Pro | Claude Code |
| 复杂跨模块 Bug | GPT-6.1 Sol High | Codex |
| 最困难的核心架构问题 | GPT-6 Astra | Codex |
| 每阶段代码独立验收 | GPT-6.1 Sol | Codex |
| 大规模 Agent 评测实验 | DS Flash | 自建程序 |

前文关于 Work 的定位：系统研究 Agent Evaluation 框架和业界实践；阅读、比较多份 Context Engineering 论文；输出评测体系研究报告；根据项目阶段整理技术选型材料；生成比较完整的项目技术总结。

## 四、各编码组合的职责

### CC + DS Flash：高频模块开发者

- RAG Pipeline
- Tool Adapter
- Memory 存储适配
- API、配置、数据模型
- Trace、日志、普通测试
- 已经完成设计的模块功能扩展

**适用条件：** 已有明确方案，编码工作量大，但技术不确定性低；Codex Plan 已经给出清晰的接口、文件修改范围和验收测试；Flash 不需要重新决定系统架构。

### CC + DS Pro：可选的复杂任务执行者

- Flash 连续两次修复同一问题仍无法通过测试
- 多个工具调用之间出现异常状态
- RAG 检索结果正确但最终答案持续出现偏差
- 上下文压缩之后 Agent 遗失关键约束
- 某个 Agent 任务偶尔成功、偶尔失败，需要分析执行轨迹
- 涉及多个模块、但已有清晰设计约束的复杂 Bug

**后续调整：** 不建议默认认为 Pro 一定强于新版 Flash。只有实际测试发现它在某些复杂任务上成功率更高时，才将相应任务交给 Pro。复杂任务先尝试 CC + DS V4.1 Flash Max；仍无法解决时使用 Codex + GPT 进行独立分析。

### Codex + GPT：核心工程开发者

- 整体架构和模块设计
- Agent Runtime 核心实现
- Context Manager 的核心接口
- Evaluation Runner 的核心执行逻辑
- 并发、状态一致性和跨模块重构
- 关键代码 Review

**适用条件：** 代码一旦写错，会影响多个模块、评测可信度或未来架构扩展。Codex 应当主动承担某些关键模块的首次实现，而不是每次都等 Flash 和 Pro 失败。

### Flash 任务准入检查

1. 任务已有明确的接口、输入输出及验收标准。
2. 修改范围相对独立，不需要重新设计核心架构。
3. 可以通过自动化测试验证主要结果。
4. 失败后能够方便地回滚，不会破坏其他模块。

满足四项：直接交给 CC + Flash；满足两三项：先补充设计或测试约束；不足两项：优先交给 Codex Plan。

## 五、Context Manager 示例：完整协作流程

1. **Codex Plan：** 阅读整个仓库，确定模块边界、接口、状态流转和验收标准。
2. **Codex 编码：** 实现 Context Manager 的核心逻辑、关键接口及边界测试。
3. **CC + Flash：** 完成 Token Counter、Compression Adapter、配置、持久化、日志等周边模块。
4. **CC + Flash：** 补充单元测试、集成测试，执行回归。
5. **Codex Review：** 检查是否符合最初的架构设计，尤其关注模块间契约和异常边界。

前文另一例中补充了：**CC + Pro** 可用于分析上下文压缩导致约束丢失等复杂异常；**CC + Flash** 随后完成普通回归测试。

## 六、编码组合的时间分配

前文曾给出以下初期建议，注明“不是 Token 比例，也不是费用比例”：

| 组合 | 建议编码工作时间占比 |
|---|---:|
| CC + DS Flash | 65% |
| CC + DS Pro | 15% |
| Codex + GPT | 20% |

**后续调整（前文原意）：** 不应该把 Flash 承担 65%–80% 的编码工作作为硬性目标。更合理的是按照工程风险分配任务，而不是预先规定 Flash 必须写多少代码。Codex 主导工程，Flash 承担高频实现。DS Pro 是可选补充，不必强行使用。

## 七、Codex 内部模型的职责

以下为前文 GPT Plus 模型分工中的内容，实际可选模型以用户 Codex 模型选择器为准。

### GPT-6.1 Sol：Codex 主力

推荐思考强度：High；普通任务 Medium。

- 项目整体架构的 Plan
- 复杂模块详细设计
- 核心状态机首次编码
- Context Manager 核心逻辑
- Agent Evaluation Runner
- 关键接口及跨模块重构
- Milestone 完成后的独立代码审查

### GPT-6 Luna：轻量任务

推荐思考强度：Medium。

- 单元测试补充
- 简单 Bug 修复
- 类型声明、代码整理
- CI 配置调整
- README、接口文档更新
- 有明确设计约束的小范围代码修改

### GPT-6 Astra：重要任务预留

- 首次确定整个 Agent Runtime 的关键工程架构
- 多 Agent 并发和任务隔离设计
- 复杂状态一致性问题
- 关键评测逻辑的系统性检查
- 重大重构前的方案评审
- Sol 无法解决且影响面很大的工程问题

### GPT-6 Sol：备用模型

如果 Codex 暂时没有开放 6.1，使用 GPT-6 Sol 承担上述核心工程任务。

### ChatGPT Chat 模型

- **GPT-6 Instant：** Java/Python 语法、命令、概念解释、简单代码讨论。
- **GPT-6 Medium：** 模块功能需求、实现思路、Agent 技术原理、技术文档解释。
- **GPT-6 High：** Runtime 架构取舍、Context Engineering 策略、Evaluation 方法论、多 Agent 并发设计。
- **GPT-5.6 Sol：** 重要架构方案的独立审查、反方观点与技术风险分析。

## 八、Codex 额度分配

前文先后给出过两个额度方案。

### 方案 A：按工作类型

| 工作类型 | 目标额度比例 |
|---|---:|
| Plan 与详细设计 | 40% |
| 核心模块编码 | 35% |
| Review 与疑难修复 | 25% |

### 方案 B：按模型与用途（后续版本）

| 模型与用途 | 目标额度比例 |
|---|---:|
| GPT-6.1 Sol：Plan + 核心编码 | 45% |
| GPT-6.1 Sol：Review / Bug | 20% |
| GPT-6 Astra：重要任务预留 | 10% |
| GPT-6 Luna / 弹性余量 | 25% |

**前文说明：** 这是人为设定的额度预算目标，而不是官方模型之间可以精确换算的积分比例。应根据 Usage 页面显示的实际剩余额度调整。

**额度不足时：**

| Codex 剩余额度 | 应对策略 |
|---|---|
| 充足 | 正常承担 Plan、核心编码、Review |
| 剩余较少 | 优先保障架构设计与关键代码 |
| 接近耗尽 | Flash 继续开发已规划的独立任务 |
| 已耗尽 | 暂缓高风险架构修改，继续普通开发与测试 |

不要让 Codex 每天对 Flash 生成的普通代码进行完整仓库级 Review；比较合理的是在每个 Milestone 结束后进行一次关键变更审查。

## 九、前文最终建议

- **Codex 是项目的核心工程开发工具，** 不是仅用于规划和审查。
- **DeepSeek Flash 是高性价比的模块开发主力，** 承担大量有明确边界的任务。
- **DeepSeek Pro 是可选补充，** 不必为了构建三级模型体系而强行使用。
- **ChatGPT 主要承担技术研究、架构思辨和评测方法论设计。**

**GPT-6 High（技术思辨）+ GPT-6.1 Sol（工程设计和关键实现）+ DS Flash（高频编码）。**

