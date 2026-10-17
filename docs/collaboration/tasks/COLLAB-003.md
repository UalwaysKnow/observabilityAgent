# COLLAB-003：IDE 配置退出版本控制

- 原计划 Owner：Claude Code
- 本轮 Owner / 实际执行者：Codex（用户授权整份方案落地）
- 角色：implementation
- 独立 Reviewer：Claude Code（待执行）
- 状态：IN_PROGRESS
- 基线：`fcc1c29464b31b5fd6a4758cfb8bf7d1e3b992b4`
- 工作区 / 分支：当前主仓库工作目录 / main，索引变更待提交
- 依赖：无

## 范围与验收

允许操作：仅从 Git 索引移除已跟踪的 `.idea` 文件，保留磁盘文件与现有忽略规则。不清理其他用户文件。

- [x] 五个原跟踪文件已从 Git 索引移除。
- [x] 对应本地文件保留。
- [ ] 用户确认提交后，从该基线创建的新 worktree 不包含这些文件。
- [ ] CC 独立 Review 与用户验收。

## 交付与下一步

交接见 [本轮记录](../handoffs/COLLAB-003-working-tree.md)。执行的是 `git rm -r --cached -- .idea`，尚未产生提交；本地 IDE 文件不受删除影响。
