# 产业服务链（服务机构施工）· 停机转交包

> **日期**：2026-08-18  
> **交接点头**：`human:淮政玮`（项目负责人）→ **接收人 / 后续总控授权人**：`human:侯佳伟`  
> **效力**：施工合同草案。侯佳伟在新总控写明「后续认领不必再问」之前，**禁止** coordinator 按旧 DAG 继续派 C/D/E。  
> **本文件不是授权句**。旧总控 `DEMO-SVC-ABCD-长任务总控.md` / `DEMO-SVC-FULL-底座后全量-长任务总控.md` 的「不必再问」**待侯佳伟落盘废止句后失效**。  
> **规约**：[`长任务执行规约.md`](../../长任务执行规约.md) v1.13 · 失败可逆 = `git revert` 正向提交，**禁止 force**。

---

## 0. 淮政玮已拍板（2026-08-18）

| # | 议题 | 决定 |
|---|------|------|
| 1 | 回退范围 | **范围 3**：停派 + 按路径 `git revert` SVC 提交 + 清 Demo SVC 切片 + 停 K8s 本模块 |
| 2 | S1–S4 | **不保留** `agent-delivery/data/data-design/storage/SVC/` |
| 3 | 共用仓 | **只 revert SVC 路径**；产业链 `LUMEN-CHAIN-*` / `storage/CHAIN` / `gkxlumen-topic-chain` **不动** |
| 4 | 重跑 A 主路径 | **ODS → SVC DWD**（`entan.svcseed` 升主路径）；24 家 fixture `seed_svc_demo_mock.py` 降旁路，不得再当 A 退出门 |

分类：整条已授权长任务作废 → **新长任务总控**（不是缺陷包、不是兼容扩展迷你链）。  
ODS→DWD 抽边界写进**新 A**，不要单独先开变更总控。

---

## 0.1 跨机（侯佳伟在另一台电脑）

ABORT / revert / 清库 **只在侯佳伟那台机器做**。淮政玮这台会话不代跑，避免两机同时改同一 `origin/dev`。

| 真源 | 说明 |
|------|------|
| GitLab `origin/dev` | 两机唯一共享工作区。侯佳伟开工：各仓 `git pull --rebase origin/dev` |
| 本转交包 | 路径 `agent-handoffs/服务机构-SVC/DEMO-SVC-停机转交-侯佳伟.md`。淮政玮已 push `origin/dev`；侯佳伟 `git pull --rebase origin/dev` 即可读 | |
| `storage/SVC` | **已在** `origin/dev`（S1–S4 他那边看得到）。范围 3 = 他删目录并 push |
| 本机未推送改动 | 淮政玮工作区另有：`pipeline-demo-mock` 等 as-built 改写、`DEMO-SVC-A-RECLOSE-L01.md`、`task-registry.yaml` 本地 diff。**不要**把半成品 registry yaml 提交给他；看板以 MCP / 飞书为准 |
| Cursor / MCP | 各开各的会话。他本机 `supervised_by=human:侯佳伟`，锁 24h；不要远程占用他的 lock |
| Demo 库 / K8s | 共用环境。清 `demo_*`、停 `topic-svc` 只需做一次，在他机器执行 |

淮政玮侧只负责把转交包推进 `origin/dev`。ABORT / revert / 清库等他拉到后再在他自己电脑开。

---

## 1. 转交边界（谁管什么）

| 仍归侯佳伟 | 不随本包转走 |
|------------|----------------|
| E7 施工长任务停机、revert、Demo 清数、新 A–E 重跑 | **产业链** `E-CHAIN-PROTOTYPE` / `LUMEN-CHAIN-*` |
| 新总控授权人、全部新叶 `supervised_by=human:侯佳伟` | **产品定义五件套** `产品整体定义/E7-产业服务链分析/`（USM/TRACE/IA；施工只消费） |
| 看板废作：`DEMO-SVC-*` / `LUMEN-SVC-*` 施工叶 | `demo-ui-topic` 已评审原型（对标真源，D12 禁 merge） |
| | 展示系统 `FE-DISPLAY-SVC-ECO-ALIGN-L01` |
| | 平台基建 `PY-LUMEN-TOPIC-PY-PORT-L01` / topic-py CI（整仓迁仓） |
| | 签收权：`ready_to_sign → done` 仍是 `human:淮政玮`（chore 除外） |

`TOPIC-SVCCHAIN-R1/R2/R2B/R2C` = 定义/原型闭环，**默认不废作、不 revert**。若侯佳伟认为与 lumen 施工缠死，另开一句写进新总控。

---

## 2. 停机顺序（有 ID 才能动手）

```text
落盘「停机总控」（侯佳伟授权句 + 废止旧两张总控）
  → MCP 建 DEMO-SVC-ABORT-L01（chore，ready）
  → 认领 24h · coordinator_dispatch · supervised_by=human:侯佳伟
     ① 旧叶写入废作（blocked / needs-revision + note；不删 registry、不倒填 ready）
     ② 按仓路径 git revert → push origin/dev（禁 force）
     ③ TRUNCATE 仅 demo_gkxlumenx_dwd/ads 的 service_org* / svc_* ；禁正式 gkxlumenx_*
     ④ 编排仓删除 storage/SVC/，改 storage/README.md 去掉 SVC 行
     ⑤ Helm/网关停 topic-svc；K8s 不再发 gkxlumen-topic-svc（CHAIN 发布门不动）
  → ABORT 达 integration 后，才能开「新长任务总控」A 段
```

同仓同时只一张 coding。`lumen-ui-topic` / `lumen-svc-platform` 若 CHAIN 仍占坑，**先等 CHAIN 叶交或串行**，禁止整仓 reset。

---

## 3. 废作清单（不要派、不要当 depends_on）

旧 ID **保留在 registry** 作审计。新 DAG 必须用新 ID。

### 3.1 旧总控与厚包（文档）

- `DEMO-SVC-ABCD-长任务总控.md`（2026-08-17 · 侯佳伟「不必再问」）
- `DEMO-SVC-FULL-底座后全量-长任务总控.md`（2026-08-18 Gate-0/1）
- 段总派单 A/B/C/D/E、`DEMO-SVC-CD-细叶拆单.md`、`DEMO-SVC-GATE1-全量派单.md`

### 3.2 A

| ID | 现状态 | 处理 |
|----|--------|------|
| `DEMO-SVC-SEED-ODS-L01` | needs-revision | 废作 |
| `DEMO-SVC-SEED-MOCK-L01` | needs-revision | 废作 |
| `DEMO-SVC-SEED-MOCK-ENRICH-L01` | needs-revision | 废作 |
| `DEMO-SVC-A-RECLOSE-L01` | integration | 废作（fixture 闸门，不得给新 C 开闸） |
| `DEMO-SVC-BASE-GATE0-L01` | ready_to_sign | 废作（不倒填；签收可积压） |

S1–S4 本地 handoff（registry 无单，删目录即可）：`ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01`、`DATA-SVC-STORAGE-S2/S3/S4-L01`、`DATA-SVC-STORAGE-DDL-L01`。

### 3.3 B

`DEMO-SVC-PY-MIDDLE-BOOT/SEARCH/TASK-L01`、`DEMO-SVC-PY-SVCAN-BOOT/MODELS/WIRE-L01`、`DEMO-SVC-PY-PORTAL-AGG-L01`（多为 integration）→ 废作。

### 3.4 C 厚包 + 路径细叶

厚包 `LUMEN-SVC-JAVA-FACADE/JOB-L01`、`JAVA-JOB-WHITELIST`、`JAVA-PORTAL-EXT`、`C1-FACADE-TEST-FIX` → 废作。  
细叶（现 backlog，**不要升 ready**）：

`LUMEN-SVC-JAVA-API-SEARCH-ORGS-L01` · `PROFILE-GET` · `PORTAL-OVERVIEW/RANKING/INDUSTRY/REGION/SZ/KEYORG` · `TASK-CREATE/GET/RESULT/EVENTS` · `ECO-GRAPH` · `REC-LIST`

重跑时按 v1.13 **新 ID** 一路径一叶；不要复活这些 ID 当主链。

### 3.5 D 厚包 + 故事细叶

厚包 `FE-ENTRY/WORKSPACE`、视觉 C1、`SEARCH-REPLICA-C2`、`PORTAL-FULL`、`ANALYSIS-FULL`、`PORTAL-VISUAL`、`ANALYSIS-VISUAL` → 废作。  
细叶 backlog 同 C：`FE-SHELL` · `WAITVIEW` · `FE-US-PT-*` · `FE-US-ORG-*` · `FE-US-ECO-*` · `FE-US-REC-*` —— 停派；新总控用新 ID 或改挂新 A 退出门后再用。

### 3.6 E（旧 `ready_to_sign` ≠ 本轮完成）

`LUMEN-SVC-E-DEVOPS-L01` · `E-QA-SMOKE-L01` · `E-DEVOPS-GATEWAY-SVC-C1` · `E-FULL-SMOKE-L01` → 废作。闸4 后必须 **新 E0/E1**。

---

## 4. 按仓 revert 路径（只 SVC，禁整仓回点）

操作：`git log --oneline -- <path>` 列出提交 → `git revert <sha>`（冲突则拆文件）。**禁止** `reset --hard` + force。commit 带 `[agent:devops-agent]` 或 `[human:侯佳伟]`。

| 仓 | 动 | 勿动 |
|----|----|------|
| `gkx-orchestration` | 删 `data-design/storage/SVC/`；改 `storage/README.md` 去掉 SVC；旧 `data-design/服务机构/` 去掉指向 storage/SVC 的「现行入口」横幅（可留历史对照） | `storage/ENT` · `storage/CHAIN` · 产品定义 E7 |
| `demo-algo-ent-analysis` | `entan/svcseed.py` · `api/svc_routes.py` · `scripts/seed_svc_demo_mock.py` · `scripts/apply_svc_demo_ddl.py` · `scripts/run_svc_ods_reconcile.py` · `test_svc_ods_reconcile.py` | ENT 主体 / `dwd_org_base_info` / 非 SVC 脚本 |
| `lumen-topic-py` | 整包 `gkx_svc_service/` · `tests/test_gkx_svc_*.py` · 相关 CI/K8s 清单（若只挂 svc） | `gkx_search_service` · `gkx_ai_*`。注意：BOOT 叶曾写 `feat/svc-middle-boot`，先核 `origin/dev` 是否已合入 |
| `lumen-algo-py` | `lumen_algo_service/views/svcan.py` · `tests/test_svcan_boot.py`；`main.py` 去掉 svcan include | `views/chain.py` 及产业链 Job |
| `lumen-svc-platform` | **整模块** `gkxlumen-topic-svc/`；父 POM module；Helm `topic-svc`；`configs/gkxlumen-topic-svc-biz-dev.yml`；gateway `/svc/**`；`db/9x_*_topic_svc.sql`；CI `backend:image:topic-svc` / `deploy:topic-svc`；async-service **仅 SVC Job 白名单键** | `gkxlumen-topic-chain` · ENT 门面 · 网关其它 Path |
| `lumen-ui-topic` | `src/views/service-portal/**` · `src/views/service-center/ServiceOrg*` · `OrgProfileDrawer` · `ServiceRecommendPage`（E7 招引）· `src/api/svc/**` · `utils/serviceOrgSearchModel.ts`；`router/menu.ts` / `routes.ts` **只删 SVC 路由** | 产业链页（产业查询/全景/诊断等）· CHAIN 皮肤提交。`ServiceChainAnalysisPage.vue` 属 E7 服务链生态，随本长任务一起退 |

Demo 库（ABORT 子步骤，只 `demo_*`）：

```text
demo_gkxlumenx_dwd.service_org*
demo_gkxlumenx_ads.svc_*
```

**禁止** DROP `demo_gkxlumenx_ods` 的 33 张约定表；**禁止** 写正式 `gkxlumenx_*`。

---

## 5. 重跑 DAG（ABORT 完成后再开；新 ID）

切法从第一天按规约 v1.13。总控授权人 `human:侯佳伟`。

```text
A1  ODS 33 表核对（复用脚本可以，新 task-id）
A2  ODS → SVC DWD 抽取（升 svcseed；禁 SELECT enterprise_*；禁复制 dwd_org_base_info 全列）
A3  A 退出门 live 证据（只认 A2，不认 fixture 24 家）
B   lumen-topic-py /internal/gkx-svc 按能力叶 + lumen-algo-py svcan
C   一 REST 路径一叶（新 ID；可对照旧细叶清单，勿复活旧 ID）
D   一 USM 故事一叶 + SHELL + WAITVIEW；同仓默认 CHAIN P0 D 先于本模块
E   闸4 后新 E0/E1；金路径必须真实 US-SVC-* ；旧 E ready_to_sign 不算完成
```

A2 硬约束（写进新总控「已拍板不回问」）：

- 共用 `demo_gkxlumenx_ods`，不新建 ODS 实例  
- 圈定 Demo 临时规则 `svc_rule_demo_kw_v1`（`name_cn` + `industry_l*_name`）；Q-SVC-010 🟡 不伪闭合 live  
- 机构主体权威在 ENT；禁止 SVC 平行 `svc_org_base` / 复制 `dwd_org_base_info`  
- fixture 24 家仅旁路，不得当退出门

---

## 6. 侯佳伟开工时建议的第一句授权（可贴进新停机总控头）

> 授权：`human:侯佳伟`。废止 `DEMO-SVC-ABCD-长任务总控` 与 `DEMO-SVC-FULL-底座后全量-长任务总控` 的「不必再问」。  
> 按本转交包范围 3 执行 `DEMO-SVC-ABORT-L01`；后续认领不必再问聊天。  
> 完成后再开新 A–E 总控（ODS→SVC DWD）。禁止 force push。

建议 MCP 首叶（侯佳伟确认后建，本转交会话**未建**）：

| 字段 | 值 |
|------|-----|
| id | `DEMO-SVC-ABORT-L01` |
| title | 服务机构施工停机：废作旧 DAG + 按路径 revert + 清 Demo SVC 切片 |
| agent | `devops-agent`（清库可拆 `data-agent` 子叶） |
| epic | `E7-产业服务链分析` |
| task_type | `chore` |
| repo | `gkx-orchestration`（跨仓；touched_files 列 §4） |
| supervised_by | `human:侯佳伟` |
| status | `ready`（无 depends_on） |

---

## 7. 本转交包未做（避免无授权动手）

- 转交包已随淮政玮 push 进入 `origin/dev`  
- 未 MCP 建 `ABORT` / 未把旧叶标废作（侯佳伟做）  
- 未 `git revert`、未 TRUNCATE、未改 K8s  

淮政玮本机 **停驱、不代 ABORT**。侯佳伟：`pull` 到本文件 → 复制 §6 授权句 → 建停机总控 → 在他自己的 Cursor 认领 ABORT → 再重跑。
