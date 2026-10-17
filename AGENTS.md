# Codex 项目指令

## 项目与必读资料

- 使用中文。项目重点是可恢复的 Agent Runtime、Context Engineering 和 Evaluation Harness，以 K8s 故障诊断与沙箱运维任务验证。
- 工作根目录是**当前 worktree 的 Git 根目录**，通过 `git rev-parse --show-toplevel` 确认。方案、代码和实验记录在本仓库维护，不放入社招求职目录，也不返回另一个工作区编辑。
- 开始任务先阅读 `README.md`、`docs/engineering.md`、`docs/architecture.md`、`docs/collaboration/README.md`，再查任务看板和当前任务卡。
- 总体范围以 `docs/project-roadmap.md` 为准；早期 `docs/project-plan.md` 和根目录讨论记录仅作参考。按任务需要读取 ADR 和模块设计，不将历史建议视为用户已确认的设计。

## Codex 职责与角色

- 负责关键模块设计和实现、架构挑战、复杂问题及独立 Review。CC 负责日常开发，用户负责最终决策和合并。
- 根据用户当前指令和任务卡确定 `implementation` 或 `reviewer` 角色；明确安排实现时直接实现，不默认退回仅审查。
- 仅修改当前任务范围；已有授权范围内的接口变更按计划执行。新增重大架构问题先记录并请求决策，同时继续不受影响的工作。
- Reviewer 检查指定 base/head commit，记录证据、影响和可执行修复建议；不自动修改被审业务代码。
- 区分确认缺陷与待验证风险；按 P0—P3 排序，无可行动发现时明确说明审查范围和验证局限。
- 自查不等于独立 Review。Codex 实现的任务由 CC 或用户安排的其他独立 Reviewer 审查。

## 协作边界

- 遵循共享工程规范中的验证、交接、提交和版本绑定规则，不覆盖他人的未提交改动。
- 不将未运行的检查写成通过，不把工作目录、任务卡或 Markdown 规则宣称为操作系统权限隔离。
- 未经当前用户消息明确要求，不主动启动 deep-research、工作流或子 Agent；联网需要时直接检索和阅读来源。
- 提交、推送、合并依用户授权范围执行；未获得授权时保留可审查改动和交接记录。
