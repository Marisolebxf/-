# 飞书缺陷修复运行账本

> 状态：P0 评审修订版
> 建立日期：2026-11-10
> 适用范围：飞书项目中由当前用户认领并修复的缺陷
> 控制入口：`feishu-bugfix`（Codex / Cursor 只做适配，不另建第二套流程）

## 定位

本目录保存每个缺陷的**执行真相**，用于回答：

- 当前缺陷处于哪个阶段；
- AI 为什么做出这个判断；
- 是否已经获得人工授权；
- 改了什么、验证了什么、还有哪些风险；
- 是否已经提测、部署和验收。

三个真相源职责分离：

| 真相源 | 职责 |
|---|---|
| 飞书项目 | 业务状态、负责人、验收结论 |
| `bugfix-runs/<auto_number>-<work_item_id>/` | 本次执行阶段、授权、证据和下一步 |
| GitLab | 分支、commit、diff、MR、Pipeline 和部署结果 |

## 使用体验

普通同事只需要：

1. 发起处理或确认目标缺陷；
2. 发送 `【进入开发】`；
3. 发送 `【提测】`；
4. 完成一次业务验收。

状态机、JSON、证据索引、哈希、报告生成和飞书写回均由 Agent 内部完成。普通缺陷不要求手工填写模板。

对外只展示：

```text
已认领 → 待进入开发 → 修复中 → 待提测 → 待验收 → 完成
                              └→ 受阻
```

## 与现有主仓规约的关系

- 遵守各业务仓的 `AGENTS.md`。
- 仓库路由优先引用 `agent-delivery/repo-registry.yaml`，不重复维护另一份仓库清单。
- `【进入开发】`授权改代码、推送独立 `fix/*` 分支和创建 Draft MR；`.cursor/rules/fe-manual-confirm-push.mdc` 在实施时补充该映射。
- `【提测】`授权集成分支合并和 dev 部署；P0 不授权生产部署。
- S 级缺陷不创建长任务；M/L 级或跨仓缺陷才接入 `task-registry.yaml`、task MCP 和 worktree 体系。
- 不替代 `长任务执行规约.md` 的段 E、C1–C6 分类和 QA 闭环。

## 目录结构

### S 级

```text
bugfix-runs/
  README.md
  P0-DESIGN.md
  _templates/
  <auto_number>-<work_item_id>/
    state.json
    report.md
    evidence/
```

### M/L 级

沿用 S 级结构。M 级信息默认合并进 `report.md`；L 级或复杂评审才按需增加 `plan.md` 和 `review-report.md`。

运行目录包含截图、日志和临时证据，P0 实施时应将真实运行目录加入 `.gitignore`。需要长期留档的最终报告，经脱敏后再关联到现有 handoff、QA 记录或飞书评论。

## P0 边界

包含：

- 单缺陷内部状态机和对外简化状态；
- 两个精确人工门；
- S/M/L 风险分级；
- 自动生成的统一报告和证据；
- 数据/Mock 策略；
- 内部状态校验器；
- Codex / Cursor 共用语义。

不包含：

- 自研 Agent Runtime；
- 自动轮询飞书；
- Webhook、队列和常驻 Runner；
- lease TTL、心跳和无人值守恢复；
- 自动合并或绕过人工验收；
- 生产自动部署；
- 对所有缺陷强制启用长任务和净室评审。

详细设计见 [`P0-DESIGN.md`](P0-DESIGN.md)。
