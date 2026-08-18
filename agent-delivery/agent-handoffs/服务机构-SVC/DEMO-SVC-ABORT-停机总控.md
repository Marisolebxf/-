# 产业服务链（SVC）· 停机长任务总控（已授权）

> **日期**：2026-08-18  
> **授权**：`human:侯佳伟`（本管线监管人；后续认领 **不必再问**）  
> **来源**：`human:淮政玮` 转交 + 拍板范围 3（[`DEMO-SVC-停机转交-侯佳伟.md`](./DEMO-SVC-停机转交-侯佳伟.md)）  
> **目标**：停旧 A–E 施工 DAG；按路径 revert SVC；清 Demo SVC 切片；停 `topic-svc`；删 `storage/SVC`。完成后再开新 A（ODS→SVC DWD）。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md) · **禁止 force push**  
> **签收**：`ready_to_sign → done` 仍是 `human:淮政玮`（本叶 `chore` 豁免签收，但仍不替其把旧施工叶标 done）

---

## 0. 授权句（本机落盘 · 2026-08-18）

> 授权：`human:侯佳伟`。废止 `DEMO-SVC-ABCD-长任务总控` 与 `DEMO-SVC-FULL-底座后全量-长任务总控` 的「不必再问」。  
> 按本转交包范围 3 执行 `DEMO-SVC-ABORT-L01`；后续认领不必再问聊天。  
> 完成后再开新 A–E 总控（ODS→SVC DWD）。禁止 force push。

**即日起禁止**按旧两张总控派 C/D/E 或视觉补单。CHAIN 管线不动。

---

## 1. 已拍板不回问

| # | 议题 | 决定 |
|---|------|------|
| 1 | 回退范围 | **范围 3**：停派 + 按路径 `git revert` SVC 提交 + 清 Demo SVC 切片 + 停 K8s 本模块 |
| 2 | S1–S4 | **不保留** `agent-delivery/data/data-design/storage/SVC/` |
| 3 | 共用仓 | **只 revert SVC 路径**；`LUMEN-CHAIN-*` / `storage/CHAIN` / `gkxlumen-topic-chain` **不动** |
| 4 | 重跑 A | **ODS → SVC DWD**（`entan.svcseed` 升主路径）；24 家 fixture 降旁路，不得当 A 退出门 |
| 5 | 库 | 只动 `demo_gkxlumenx_dwd.service_org*` / `demo_gkxlumenx_ads.svc_*`；禁 DROP ODS 33 表；禁写正式 `gkxlumenx_*` |
| 6 | git | `git revert` 正向提交；禁止 `reset --hard` + force；commit `[agent:devops-agent]` 或 `[human:侯佳伟]` |
| 7 | 看板 | 旧 `DEMO-SVC-*` / `LUMEN-SVC-*` 施工叶 **废作留 ID**；新 DAG 必须新 ID |

锁：`lock_hours=24`。`claim_type=coordinator_dispatch`。`supervised_by=human:侯佳伟`。  
升级：结构歧义 → `human:李伟`；环境卡点微信 `human:淮政玮`。

---

## 2. DAG

```text
落盘本总控 ✅
  → DEMO-SVC-ABORT-L01（chore · ⑤已闭合，可关单）
     ① 旧叶废作 ✅（69 叶）
     ② 按仓路径 revert → origin/dev ✅
     ③ TRUNCATE Demo service_org* / svc_* ✅（after=0）
     ④ 删除 storage/SVC/ ✅
     ⑤ 停 topic-svc ✅（values-lumen `enabled: false` · helm:chart 22854 Removing / Terminating；CHAIN 发布门未改）
  → 可开「新长任务总控」A 段（ODS→SVC DWD，新 ID）
```

同仓同时只一张 coding。`lumen-ui-topic` / `lumen-svc-platform` 若 CHAIN 仍占坑，**先等或串行**，禁止整仓 reset。

---

## 3. 本叶

| 字段 | 值 |
|------|-----|
| id | `DEMO-SVC-ABORT-L01` |
| agent | `devops-agent`（① 由 coordinator MCP；清库可拆 `data-agent`） |
| epic | `E7-产业服务链分析` |
| task_type | `chore` |
| repo | `gkx-orchestration`（跨仓；路径见转交包 §4） |
| 路径清单 | 转交包 §4 |

**ABORT 完成前禁止**开新 A–E 总控、禁止派旧 C/D 细叶。

---

## 4. 重跑 A（ABORT 完成后再开；此处只钉口径）

- 共用 `demo_gkxlumenx_ods`，不新建 ODS 实例  
- 圈定 Demo 临时规则 `svc_rule_demo_kw_v1`（`name_cn` + `industry_l*_name`）；Q-SVC-010 🟡 不伪闭合 live  
- 机构主体权威在 ENT；禁止 SVC 平行 `svc_org_base` / 复制 `dwd_org_base_info`  
- fixture 24 家仅旁路，不得当退出门  

切法：A1 ODS 核对 → A2 ODS→SVC DWD → A3 live 退出门（只认 A2）→ 再 B/C/D/E（**新 ID**）。

---

## 5. 废作（文档指针）

旧总控与厚包见转交包 §3。本总控废止：

- `DEMO-SVC-ABCD-长任务总控.md`
- `DEMO-SVC-FULL-底座后全量-长任务总控.md`
