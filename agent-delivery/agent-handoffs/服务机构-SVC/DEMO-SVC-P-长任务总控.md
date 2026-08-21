# 服务机构施工 · 阶段 P（产品）长任务总控

> **日期**：2026-08-21  
> **授权**：`human:淮政玮`（签收 `DEMO-SVC-LAB-GATE-L01` = done 后单独授权）  
> **本管线监管**：`human:侯佳伟`（**后续认领不必再问**）  
> **签收**：`ready_to_sign → done` 仍是 `human:淮政玮`  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **锁**：`lock_hours=24` · `claim_type=coordinator_dispatch` · `supervised_by=human:侯佳伟`  
> **前置**：阶段 F 退出门 [`DEMO-SVC-LAB-GATE-L01`](./DEMO-SVC-LAB-GATE-L01.md) = done；切法 A [`formula-freeze-cut-a.md`](../../data/data-design/storage/SVC/formula-freeze-cut-a.md)  
> **与 F 的关系**：不是把 F 总控 DAG 自动续过来。本文件才是 P 的授权真源。

---

## 0. 授权句（本机落盘 · 2026-08-21）

> 授权：`human:侯佳伟`。`human:淮政玮` 2026-08-21 签收 F-GATE 后同意开启阶段 P 长任务。  
> **后续认领不必再问聊天。** 禁止 force。签收仍 `human:淮政玮`。  
> 消费切法 A：一张 `demo_gkx_chain` 双滤镜、关系链双密度并排、短板/技术力对象=机构、引入/培育名单=机构、关联主体一跳复用 ENT hang。  
> Q060 / Q062 / Q063 / Q-SVC-010 / Q-SVCCHAIN-03 不因本总控变绿。

---

## 1. 一句话

50892 产品段：换引擎不换表，把 F 已冻结的公式接到正式调用链（前端 → Java REST → Python `/internal/*`）。  
F 积压（GRAPH 内网投影、十模型页、S2–S4）不挡本总控开工。

---

## 2. 段/叶表（侯佳伟落盘补齐后再派第一张 coding 单）

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| B | `lumen-algo-py` | `origin/dev` | （侯佳伟补 ID） | 消费切法 A；禁 Neo4j；禁写正式 `gkxlumenx_*` 无闸门 |
| C | `lumen-svc-platform` | `origin/dev` | （侯佳伟补 ID · 一 REST 路径一叶） | 前端只调本仓 |
| D | `lumen-ui-topic` | `origin/dev` | （侯佳伟补 ID · 实施权威故事一叶） | 复刻五维；`USE_MOCK=false` 禁 fixture |
| E | devops + qa | K8s `dev` | E0 发布门 · E1 金路径 | 只认 50892 已发布前端 |

金路径表、废作清单、调用链细节由侯佳伟按规约 §4.1 补进本文件后再 `coordinator_dispatch`。未补段/叶 **禁止** 无 ID 改 lumen 四仓。

---

## 3. 已拍板（不回问）

| # | 项 | 决定 |
|---|-----|------|
| 1 | 切法 | 只消费 F-GATE 切法 A，不另起一套公式 |
| 2 | 调用链 | 前端 → Java → Python `/internal/*`；50892 不直连 demo / 50100 |
| 3 | D12 | 对照 demo 可读后重写；禁止 merge `demo-*` |
| 4 | 黄灯 | 待核验保留；禁止本总控改绿 |
| 5 | git | `origin/dev` 直推；禁止 force |

结构歧义升级 `human:侯佳伟`。环境卡点微信 `human:淮政玮`。
