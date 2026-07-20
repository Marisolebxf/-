# RFC-003 · 飞书 Bitable Webhook 入站 + 飞书-only 状态纪律

| 字段 | 值 |
|------|------|
| Status | **🟢 Phase C 已实现（2026-07-21）** — Handler 见 `scripts/feishu-bitable-webhook-handler.mjs` + [`feishu-bitable-webhook-handler.md`](../feishu-bitable-webhook-handler.md) |
| Author | coordinator（AI 辅助起草） |
| Created | 2026-07-21 |
| 决策人 | PM（郭万迎）/ 项目负责人（淮政玮） |
| 关联 | `feishu-bitable-integration.md` · `自动派单与确认规约.md` · `dispatch-rules.yaml` · `coordinator-dispatch.mjs` |

---

## 1. 摘要

团队选定 **方案 B：飞书 Bitable 为状态真源 + 自动化 Webhook 入站**。

目标链路：

```text
人在飞书拖状态 / 改认领 / Sprint
        ↓
Bitable 自动化 Webhook（HTTPS POST）
        ↓
feishu-bitable-webhook-handler（待建）
        ↓
单条 inbound → task-registry.yaml
        ↓
status=done → coordinator-dispatch scan
        ↓
pending 队列（定义轨 + 门3 impl-gate3-unlock）
        ↓
PM confirm --approved-by human:{真名}
        ↓
ready + 派单包 + outbound（监管人等 SkipKanbanFields）
```

**不在本 RFC 范围（Phase 1 仍可用）**：`board-sync-watch` 轮询、`update-task-status.ps1` 改 status — Phase 2 逐步弱化为 heartbeat / 应急入口。

---

## 2. 已拍板决策

| # | 决策 | 说明 |
|---|------|------|
| D1 | **方案 B（Webhook）** | 状态变更尽量只在飞书操作；registry 由 inbound 回写 |
| D2 | **门 3 须 confirm** | `*-DG-G3 done` → `impl-gate3-unlock` pending → PM confirm → ready（**已改** `dispatch-rules.yaml`） |
| D3 | **confirm 权限** | 必填 `--approved-by`；校验 `team-roster.yaml`（PM / `can_supervise_agent`） |
| D4 | **confirm 入口 Phase 2** | 仍用终端 `coordinator-dispatch confirm`；飞书「PM 确认」按钮为可选 Phase 3 |

---

## 3. Handler 接口（草案）

### 3.1 路由

```
POST /internal/feishu-bitable/webhook
```

配置真源：`agent-delivery/feishu-bitable.yaml`（新增 `webhook` 段，与 `feishu-project.yaml#webhook` 对齐）。

### 3.2 请求校验

1. 飞书开放平台 **签名校验**（`X-Lark-Signature` + timestamp）
2. 仅接受已配置 `app_token` / `table_id` 的事件
3. 字段映射沿用 inbound 白名单：`status` / `claimed_by` / `sprint_id` / `priority`（见 `feishu-bitable.yaml#inbound`）

### 3.3 处理步骤（单条 record）

```text
1. 解析 record_id → task_id（Bitable「Task ID」列）
2. 映射字段 → registry patch（strict 状态机，非法 transition 拒绝并 audit）
3. git pull --rebase（或乐观锁）→ 写 task-registry.yaml
4. 若 status 变为 done → spawn coordinator-dispatch scan --cause-task {id}
5. 可选 git commit + push（见 §4 OPEN）
6. 返回 200（飞书重试策略友好）
```

### 3.4 与 outbound 边界

| 方向 | 字段 |
|------|------|
| inbound（Webhook / pull） | status、claimed_by、sprint_id、priority |
| outbound（registry → 飞书） | 监管人 supervised_by、Agent、Epic、Token 等 **SkipKanbanFields** |

冲突策略：**registry 为编排真源**；飞书 inbound 只改白名单字段；监管人不从飞书回写。

---

## 4. 部署（OPEN · 待 PM/架构师）

| 选项 | 优点 | 缺点 |
|------|------|------|
| K8s dev 小服务 | 与现有 CI/CD 一致 | 需公网 Ingress / 内网穿透 |
| 编排机常驻 Node | 实现快 | 单点、需 HTTPS 隧道 |
| GitLab CI trigger | 无长驻进程 | 非实时、不适合高频拖卡 |

**推荐**：K8s dev Deployment + Ingress（路径 `/internal/feishu-bitable/webhook`），环境变量注入 `FEISHU_APP_*`、Webhook 密钥。

### OPEN 项

- [x] **O1** 每次 inbound auto `git commit` + push `task-registry.yaml` → **是（默认 true，2026-07-21 PM）**
- [ ] **O2** 是否正式禁止 `update-task-status -Status`（仅保留 heartbeat / 应急）？
- [ ] **O3** Webhook 失败告警通道（飞书群 / coordinator halt）？
- [ ] **O4** 与 `board-sync-watch` 并存窗口期多长？

---

## 5. 派单与 confirm（与 Webhook 衔接）

Webhook **不替代** confirm；只替代「人拖状态 → 写 registry → scan」这一段。

| 触发 | pending trigger | confirm 后 |
|------|-----------------|------------|
| PACK-L01 done | `def-pack-unlock-mo-ux` 等 | METRIC-OPEN / UX → ready |
| DG-G3 done | `impl-gate3-unlock` | 同模块 implementation → ready |

全员操作见 [`自动派单与确认规约.md`](../自动派单与确认规约.md)。

---

## 6. 实施分期

| Phase | 内容 | 状态 |
|-------|------|------|
| **A** | dispatch scan / confirm / 门3 pending | ✅ 2026-07-21 |
| **B** | 本 RFC + feishu-bitable.yaml webhook 段 | 🟡 文档 |
| **C** | Handler 服务 + 飞书自动化配置 | ✅ Handler 已实现；飞书自动化需 PM 配 URL |
| **D** | 弱化 CLI 改 status；watch 仅 outbound/heartbeat | ⬜ 未开始 |

---

## 7. 验收（Phase C DoD）

1. 飞书拖「已完成」→ 30s 内 registry status=done（可 audit）
2. 定义轨 / 门3 done → `pending-dispatch.yaml` 出现对应条目
3. PM `confirm --approved-by` → ready + 派单包 + 飞书监管人列更新
4. 非法状态跳转被拒绝并留 audit 日志
5. 签名校验失败 → 401，不写 registry

---

## 8. 参考命令（Phase A · 当前）

```powershell
cd gkx-orchestration
node scripts/coordinator-dispatch.mjs list
node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:郭万迎
node scripts/coordinator-dispatch.mjs scan --cause-task ENT-MOD-EVAL-DG-G3 --dry-run
```
