# COLLAB-002：统一验证入口与 CI

- 原计划 Owner：Claude Code
- 本轮 Owner / 实际执行者：Codex（用户授权整份方案落地）
- 角色：implementation
- 独立 Reviewer：Claude Code（待执行；Codex 自查不算独立 Review）
- 状态：IN_PROGRESS
- 基线：`fcc1c29464b31b5fd6a4758cfb8bf7d1e3b992b4`
- 工作区 / 分支：当前主仓库工作目录 / main，未提交
- 依赖：COLLAB-001 提供规范和记录格式

## 范围与验收

允许修改：`scripts/verify.sh`、CI 工作流、验证脚本测试、现有骨架测试的准确命名；说明和交接由对应文档任务集成。

- [x] 本地与 CI 共用一个入口。
- [x] 脚本定位自身工作区；覆盖根目录、子目录和带空格路径。
- [x] 失败保留退出码并停止后续步骤；缺少 uv 提示明确。
- [x] 完整真实脚本验证通过，证据写入交接。
- [ ] 共享基线提交与 CC 独立 Review。
- [ ] 远端 CI 与用户验收。

## 交付与下一步

交接见 [本轮记录](../handoffs/COLLAB-002-working-tree.md)。2026-10-17 完整脚本通过：Ruff、mypy、7 项测试、sdist/wheel 构建、锁定运行依赖安装及仓库外导入与应用创建检查。未调用实际模型或修改用户 API 配置。实现仍待提交与 CC 独立 Review。
