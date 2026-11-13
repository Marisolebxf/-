# S-lite 最小合规清单（S 级缺陷）

> 原则：可以让流程轻，但不能无痕。每项都是最低留痕，不允许“修完直接推”。

## 开工

- [ ] `init` 创建 run（`auto_number`、`work_item_id`、`claim_id`）
- [ ] 飞书 claim：`[agent-claim]` 评论 + `claim_comment_ref`
- [ ] `diagnosis.requirement_refs`：具体需规文件 + 条款/序号
- [ ] 变更范围与非目标

## 开发与验证

- [ ] 专用 fix 分支 + commit SHA
- [ ] `fix` 验证：报告的行为已修复
- [ ] `regression` 验证：相邻行为未破坏
- [ ] 证据落盘（命令/退出码/stdout/commit/environment）

## 提测

- [ ] 精确口令 `提测`
- [ ] `ship` gate 绑定候选 SHA + diff/verification/review hash
- [ ] pipeline + deploy 终态（candidate 已包含）
- [ ] `record-ship-package`

## 验收（不得跳过）

- [ ] 精确口令 `验收通过`
- [ ] `finalize-acceptance --message 验收通过 --current-status IN PROGRESS`
- [ ] `get_transitable_states` + `get_transition_required`
- [ ] `transition_state` → `RESOLVED`（必填字段按 references/feishu-transition-recipe.md）
- [ ] `record-acceptance(mode=chat_exact, current_status=RESOLVED)`
- [ ] `advance --to RESOLVED`
- [ ] 飞书验收总结评论
- [ ] `render-report`

## 禁止

- 禁止无 run、无 claim、无需求锚点直接改代码
- 禁止跳过 `提测`/`验收通过` gate
- 禁止收到 `验收通过` 后只汇报流水线、不迁移状态
- 禁止在迁移失败时声称“已关闭”
