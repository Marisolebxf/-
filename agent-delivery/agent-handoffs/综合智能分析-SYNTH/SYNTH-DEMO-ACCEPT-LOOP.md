# SYNTH-DEMO-ACCEPT-LOOP Handoff — 综合智能分析演示实例反复验收（常驻验收单）

- **任务**：`SYNTH-DEMO-ACCEPT-LOOP`（产品实现规程 §6.5.2 验收单；tech_task / qa-agent）
- **监管**：`supervised_by=human:徐滕强`（§6.5.7 当次会话真人；`done` 操作人以 registry 闸门为准）
- **仓**：gkx-orchestration（registry only；本单不改业务代码、不写库）
- **强度**：ponytail: full
- **日期**：2026-11-07

## 运行 2026-11-07（R1 探测误判 + R2 更正后批量对照）

### R1（19:58–20:16）：路由误判（已撤回）

用 `/tts/svcz/api/enterprise/**` 与 `/tts/lumen/api/**` 两面探测 SYNTH 均 404 → 误判「网关剥前缀错配」（当时做了完整分层诊断：服务直打 svc 7092 带 `/topic/v1` 前缀 200 数据正确，该诊断结论本身正确，但把它错误外推到「线上无正确入口」）。**监管人 20:30 澄清「线上明明可以调通」后复核出正确入口**（见 R2 X1）。教训记录：**线上入口以监管人给的现网请求为锚做路由枚举，不做「两面皆 404 = 无入口」外推**。

### R2（20:30–20:45）：正确路由确认 + 批量样本对照（全 PASS）

**正确入口**：`https://edu.itic-sci.com/tts/svcz/api/topic/**topic**/v1/synth/**`（`/api` + 服务段 `topic` + 完整 `/topic/v1` 路径；实测 X1 200）

| 用例 | 请求要点 | 结果 | 判定 |
|---|---|---|---|
| VIT-01 默认秒开 | 3y 默认三元组 | 200；`snap:mock_20261106_vit_seed_index_main`；index=75.15；dims 4 / indicators 12 / ranks 4 | ✅ |
| VIT-02 EQUAL 档 | `weight_profile=EQUAL` | 200；`snap:..._equal`；index=75.00 ≠ INDEX_MAIN 75.15（指纹隔离） | ✅ |
| VIT-11 非法档 | `weight_profile=INVALID_X` | **400 `WEIGHT_PROFILE_INVALID`**（reason 逐字命中，不回落） | ✅ |
| VIT-16 活力趋势 | 3y 快照 `trend` 字段 | `[2022, 2023, 2024]` 三年度 | ✅ |
| ELEM-01 默认秒开 | 3y | 200；`batch:深圳市\|...\|mock_20261107_elem_delivery_3y`；compositeIndex=77.68；fourDim 4 / typeScores 7 / contributions 8 / ranks 4 | ✅ |
| ELEM-12 要素趋势 | 3y `trend` 字段 | `[2022, 2023, 2024]` —— **矩阵 gap 已被下午修复单闭合**（原判「要素无历史年行」过时） | ✅（矩阵待增量更新） |
| ELEM-02 要素 1y | 1y 窗 | **200** `mock_20261107_elem_delivery_1y` —— 矩阵 gap 过时（原判 404） | ✅（矩阵待更新） |
| ELEM-03 要素 5y | 5y 窗 | **200** `mock_20261107_elem_delivery_5y` | ✅（矩阵待更新） |
| ELEM-04 广州换城 | 广州 3y | 200 `batch:广州市\|...` | ✅ |
| COLLAB-01 协同默认 | 3y | 200；`batch:...\|gapfill_transitional`；**8 节点 / 9 边 / 1 集群 / 2 孤立**（与调研一致）；relationInput {jointPatent:3, project:3, talentFlow:3}；ranks 4 城；effectEval status=ok r=0.9909；strategies 2 条 | ✅ |
| COLLAB-02 广州协同 | 广州 3y | 200；6 节点（batch_meta latest 命中，不串深圳批） | ✅ |
| COLLAB-08 产业筛选 | graph API | 200；8 节点 / 9 边；产业 {人工智能, 智能制造, 生物医药} | ✅ |
| COLLAB-17 坏快照 | `snapshotId=task:never_exists` | **404 `SNAPSHOT_NOT_FOUND`**（不回落最新批） | ✅（语义等价拦截：未指定 meta 的 snapshot 走 not_found；`batch_meta_missing` 为 meta 行存在但快照缺批的分支，复测时用历史快照 ID 再验） |
| VIT-03 活力 5y | 5y 窗 | **404 `SNAPSHOT_NOT_FOUND`** —— ⚠️ 但库内 1y/5y 行已在（60 行/窗，`mock_20261106_vit_seed_*_5y` 均 succeeded） | ❌ **QUERY 缺口** |
| VIT-04 活力 1y | 1y 窗 | 404（同上） | ❌ QUERY（并入 Q1） |

### 缺口单（QUERY 类 ×1）

- `SYNTH-DEMO-ACCEPT-LOOP-Q1`（ready，api-agent）：活力 1y/5y 行在+succeeded+键面同款但拣不中（要素同结构可 200 对照成立）→ 疑似 latestCalcBatchId/快照解析未纳入新窗批。**修后复测 VIT-04/05/09/15。**

### 矩阵过时项（增量更新待办，M3 增补轮）

- gap 5 条中：VIT-04/05/09 → 改 QUERY 缺口（Q1，数据已在库）；ELEM-12 → **已闭合**（趋势有数）；ELEM-02/03 → **已闭合**（1y/5y 200）
- VIT-15 失败态触发器随 VIT-05 状态变化需重新设计（1y/5y 将有数后，「失败态」需另寻触发路径或降级为可选演示）

### 环境与令牌

- 令牌：监管人提供 curl 提取 access_token → 写入 `~/.gkx/topic-loop-token`（600 权限；不进 git / handoff / 日志正文）
- 锚点探测：`POST /tts/svcz/api/enterprise/topic/v1/recommend`（监管人提供的现网请求）→ **HTTP 200**，令牌有效、网关前缀可用

### 探测（§6.5.3）+ 分层诊断（根因定位）

| # | 层 | URL | 结果 |
|---|---|---|---|
| 1 | 域名网关（企业专题面） | `GET /tts/svcz/api/enterprise/topic/v1/synth/vitality/batch-snapshot` | 404 `path=/topic/v1/...`（demo 面网关，非本服务） |
| 2 | 域名网关（lumen 面） | `GET /tts/lumen/api/topic/v1/synth/vitality/batch-snapshot` | 404 `path=/v1/synth/...`（**网关剥 `/topic` 转发**） |
| 3 | NodePort 30895 直打 | `GET /topic/v1/synth/vitality/batch-snapshot` | 404 `path=/v1/synth/...`（同上，证实网关剥前缀行为） |
| 4 | **服务直打 svc 7092** | `GET /topic/v1/synth/vitality/batch-snapshot` | **HTTP 200 + 快照数据正确**（`snapshotId=snap:mock_20261106_vit_seed_index_main`，`cache_key=深圳\|全国重点城市\|最近3年\|INDEX_MAIN`） |

**根因**：`gkxlumen-platform-topic` 服务按**完整 `/topic/v1` 前缀**注册映射（直打 200 验证）；lumen 网关按**剥 `/topic` 前缀**转发（StripPrefix）→ 服务收到 `/v1/synth/**` 无此映射 → 404。服务与数据全正常，纯网关-服务路由前缀错配。

**修复二选一（监管人裁决）**：
- **方案 A（devops）**：网关为 `gkxlumen-platform-topic` 的路由改为不剥前缀（保留 `/topic/**` 直转）——注意需评估其他已按剥前缀工作的 topic 接口（#102–#109 任务链等）兼容性
- **方案 B（api）**：服务侧按网关契约把 controller 映射改发布为 `/v1/**`（Java `gkxlumen-topic` `server.servlet.context-path` 或 controller 调整）

> 运行注记：第 2/3 步属 ENV 分层诊断（同意图探测 2 次 + 变路径对照 1 次，未超熔断纪律）；第 4 步命中前按「服务内部真实映射」假设验证，非重复探测。

### 处置（按规程，未越线）

- 验收单 → `blocked`（note 只写映射不存在事实 + 已通知监管人）；**不建子任务、不开第二轮**
- LOOP 计划状态行已回写（「最近一轮：R1 探测 / 退出=ENV」）
- 同意图探测合计 2 次，未第三次猜路由（熔断纪律）

### 给监管人的路由澄清选项（下一轮开工前二选一确认）

1. 现网尚未发布 `gkxlumen-topic` SYNTH 路由（demo 库数据在、K8s dev 服务在、但 `edu.itic-sci.com` 网关未挂该服务/路径）
2. 网关前缀另有其值（既非 `/tts/svcz/api/enterprise` 也非 `/tts/lumen/api`）

澄清后由监管人重说「按 LOOP 跑」，验收单再转回执行。

## 架构合规自检

- ✅ 纯后端两段制（只读探测）；未写任何库；未建缺口子任务（ENV 类不建单）
- ✅ 令牌未写入 git/handoff/日志；探测合计 2 次未空转
- ✅ 未把 404 改写成通过；未把 ENV 归入 DATA/QUERY/ALGO

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 30000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.04 |
| cost_warn | green |

## ponytail

ponytail: full——单 handoff 复用验收单生命周期；探测记录即运行记录，不另建运行日志文件。
