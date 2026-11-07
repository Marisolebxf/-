# SVCCHAIN 合规演示用例整理 + 数据条件填充 + LOOP 执行编排 · 长任务总控（无人值守）

> **日期**：2026-11-07
> **授权人**：`human:徐滕强`（本管线监管人；用户本轮原话「创建一个长任务……执行时可自行分解为多个子智能体并行完成」= 总控一次授权，**后续认领不必再问**）
> **规约**：`agent-delivery/长任务执行规约.md`；`claim_type=coordinator_dispatch`；`lock_hours=24`
> **规程**：`agent-delivery/产品实现规程.md` §6.4（合规演示用例）+ §6.5（演示样本循环 LOOP）；样例 = `05-展示系统集成/合规演示用例/` 与 `编排计划/` 科技政策跟踪全套（2026-11-07 同日已完成）
> **一句话目标**：按最新规程整理**产业服务链分析**全部子模块（服务机构分析 7.1–7.3 / 服务链生态 7.4·7.5·7.8 / 机构招引培育 7.6·7.7 / 门户专题服务 §33，需规序号以 bid 真源清点）的**合规演示用例**与各域 **LOOP 执行编排计划**；调研当前 demo 库数据情况，**逐条**为覆盖表填充可支持的输入/选择条件；数据无法支持的行写 `覆盖不到` 并写明缺哪类数据。不遗漏、不造假。

---

## 0. 规程口径（执行 agent 必读）

| 术语 | 本管线含义 | 真源 |
|---|---|---|
| 合规演示用例 | §6.4 两块结构：**覆盖表**（需规每条一行，8 列：需规位置/界面/输入或选择/触发/接口地址/按界面值填好的请求/期望输出/数据情况）+ **一条主路径**（可演行串成一次演示，条件不另排列组合） | `产品实现规程.md` §6.4；金样 `05-展示系统集成/合规演示用例/POL-L2-DS10-QRY-合规演示用例.md` |
| 数据情况 | 每行只能写：`可演` / `覆盖不到`+缺哪类数据 / `设计无资源`。参数值来自界面输入真源；现有数据演不到的行写 `覆盖不到`，**不编假结果** | §6.4；POL 样例 202 行 |
| LOOP 执行编排计划 | §6.5 每域一份：常驻验收单建议 ID、先决条件、纯后端 token 熔断（`~/.gkx/topic-loop-token` + `systemCode: topic`）、一轮四步（探测→只读库+调接口→对照→缺口分类 DATA/QUERY/ALGO/ENV）、每轮最多三张子任务、同缺口两轮不进则停 | §6.5；金样 `编排计划/POL-L2-DS10-QRY-LOOP计划.md` |
| 数据情况调研 | demo 库 SVC 域表逐表行数、维度覆盖、`is_mock`、批次状态；**只读 SELECT**；**不打开页面、不探测接口**（接口可达性属 LOOP 轮次内动作，本管线不做） | §6.4 查库节；本总控 §3 |
| 明确缺口 | `覆盖不到` 行引用既有缺口真源（`Q-SVCCHAIN-01~06`、`Q-SVC-011`、as-built `GAP-SVC-*`），**不新造编号**；确属新缺口才登记并交叉引用 | `客户决策清单跟踪表.md`；各域 USM 开放项 |

**禁止**：为凑用例编造数值；把 `d4=mock` 行写成真值；把 `覆盖不到` 改成 `可演`「好看」；建 `*-DEMO-ACCEPT-LOOP` 验收单（等人说「按 LOOP 跑」才建，§6.5.2）；跑 LOOP 轮次；写正式 `gkxlumenx_*`；改业务仓代码。

## 1. 已拍板（执行 agent 不回问）

1. **模块范围** = 产业服务链分析 4 域全部子模块：服务机构分析（7.1–7.3，6 三级项）/ 服务链生态（7.4/7.5/7.8，6 三级项）/ 机构招引培育（7.6/7.7，4 三级项）/ 门户专题服务（bid §1.1.1.1.1.1.1.33，序号 97–104，8 编号项）。需规真源 = `bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.7 + §33；五件套 = `agent-handoffs/产品整体定义/E7-产业服务链分析/{ORG-ANALYSIS|ECOSYSTEM|RECOMMEND|PORTAL}/`（USM/IA/Wireframe/UX-SPEC/TRACE）。条目矩阵清点基准 **24 条**（16+8），M1 逐条核对，多退少补须在 handoff 写明依据。
2. **条件枚举真源** = `repos/demo-ui-topic` 服务域（svc）页面与 API 封装（检索条件、对比篮 `service_org`、Job 任务键 analysisType、门户产业/区域筛选）；as-built 实勘脚本 `qa/as-built/scripts/KJZTFWXT/service/*/cases/*.yaml` 的 locators/路由为第二参照。禁止臆造条件值。
3. **用例覆盖基准** = 需规条目 100% 落覆盖表行（一行不缺）；每行输入/请求必须基于 M2 实查数据填**真实可填值**（照 POL 金样：写出具体参数值、预期首条记录、排序与计数）。`覆盖不到` 的行同样落行，期望列写「不编」。
4. **数据调研范围** = demo 库（`10.50.11.76`，账号走既有 database-mcp 分组，只读）：`demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` / `demo_gkxlumenx_ai` 及服务域业务库，以 `search_schema` 实查 svc/service/institution/org 相关表为准；对照 `metrics/registry/metric-readiness-matrix-SVC.yaml`（29 条 `M_SVC_*` 现 `d4=mock`）逐指标核对源表。**禁止**写任何表；SELECT 失败 2 次 → 该表记「调查受阻」继续下一张，不空转。
5. **过渡标识**：涉及 mock/演示态的期望输出必须带标识（MockBadge / 演示规则判定声明 / `is_mock=1`），与 as-built 实勘记录口径一致；不得当正式业务结论。
6. **缺口处理**：`覆盖不到` 行 → 引用既有 Q/GAP 编号（含 2026-11-06 新登记 `Q-SVC-011` 招引/培育推荐产业切片缺 3 条 L0 链挂链数据）；新缺口登记进 M4 总表并交叉引用，不重复建编号。**不派** DATA/QUERY/ALGO 修数单（那是 LOOP 轮次内动作）。
7. **产物落点**：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/`（新目录）：`产业服务链分析-索引.md`、`SVCCHAIN-需规条目矩阵.md`、`SVC-数据调研-20261107.md`、`SVC-ORG-合规演示用例.md`、`SVC-ECO-合规演示用例.md`、`SVC-REC-合规演示用例.md`、`SVC-PT-合规演示用例.md`、`SVCCHAIN-缺口登记总表.md`；`…/03-专题系统集成/编排计划/`（新目录）：`SVC-ORG-LOOP计划.md`、`SVC-ECO-LOOP计划.md`、`SVC-REC-LOOP计划.md`、`SVC-PT-LOOP计划.md`。
8. **cicd: skip**（纯编排仓文档）；不改 `metrics/registry/` seed；历史集成测试记录（`05-展示系统集成/测试用例/` 等）保持原文件不改写。
9. **升级人**：结构歧义 / 需规清点争议 → `human:李伟`；用例期望 / 授权变更 → 本总控授权人。
10. **签收**：`ready_to_sign→done` 由 coordinator 以 `actor=human:徐滕强` 代签（本总控授权），可积压不挡主链。签收 GDF/KG 类门禁脚本不适用本管线（无 WORKPACK/GRAPH-LOAD 单）。

## 2. 段 / 叶表（M0–M4）

| 段 | task-id | agent | 仓 | 产物 | 依赖门 |
|---|---|---|---|---|---|
| M0 | `SVCCHAIN-DC-CTL-L01` | coordinator-agent | gkx-orchestration | 本总控 + MCP 建单 + push | — |
| M1 | `SVCCHAIN-DC-M1-USM-L01` | product-agent | gkx-orchestration | `SVCCHAIN-需规条目矩阵.md`：24 条需规逐条 = 序号/需规名/界面(路由)/USM 引用/入口动作/条件枚举锚点；含「另发现」须 handoff 说明 | M0 |
| M2 | `SVCCHAIN-DC-M2-DB-L01` | data-agent | gkx-orchestration | `SVC-数据调研-20261107.md`：逐库 search_schema 清单 → SVC 域表逐表行数/维度分布/is_mock/批次/调查受阻标记；`M_SVC_*` 源表对照 | M0（与 M1 并行） |
| M3a | `SVCCHAIN-DC-M3-ORG-L01` | doc-agent | gkx-orchestration | `SVC-ORG-合规演示用例.md`（7.1–7.3 覆盖表+主路径+调度核对）+ `SVC-ORG-LOOP计划.md` | M1 + M2 |
| M3b | `SVCCHAIN-DC-M3-ECO-L01` | doc-agent | gkx-orchestration | `SVC-ECO-合规演示用例.md`（7.4/7.5/7.8）+ `SVC-ECO-LOOP计划.md` | M1 + M2 |
| M3c | `SVCCHAIN-DC-M3-REC-L01` | doc-agent | gkx-orchestration | `SVC-REC-合规演示用例.md`（7.6/7.7）+ `SVC-REC-LOOP计划.md` | M1 + M2 |
| M3d | `SVCCHAIN-DC-M3-PT-L01` | doc-agent | gkx-orchestration | `SVC-PT-合规演示用例.md`（§33 序 97–104）+ `SVC-PT-LOOP计划.md` | M1 + M2 |
| M4 | `SVCCHAIN-DC-M4-GAP-L01` | doc-agent | gkx-orchestration | `产业服务链分析-索引.md`（各域可演/覆盖不到/设计无资源计数）+ `SVCCHAIN-缺口登记总表.md`（既有引用 vs 新登记归并） | M3a–d |

DAG：

```text
M0 ─┬─ M1 ─┬─ M3a ─┐
    └─ M2 ─┴─ M3b ─┼─ M4
              M3c ─┤
              M3d ─┘
```

M1 与 M2 并行；M3 四叶并行（产物路径互斥，禁止两叶改同一文件）；同仓无代码冲突。

## 3. 数据调研清单（M2 必须逐表覆盖，表名以 search_schema 实查为准）

| 库 | 查什么 | 输出 |
|---|---|---|
| `demo_gkxlumenx_dwd` | svc/service/institution/org 相关表：机构主数据、领域/环节挂接、新增动态、投融资 | 逐表行数、关键维度分布、最新批次 |
| `demo_gkxlumenx_ads` | svc 域 ADS 面：覆盖度/深度/热度/技术力/榜单/门户统计 | 同上 + `is_mock` 行数 |
| `demo_gkxlumenx_ai` | svc 分析结果面：链路/瓶颈/图谱/推荐计算产物、Job 快照 | 同上 + 批次状态 |
| `gkxlumenx_topic_svc`（或实查同名业务库） | 检索历史/收藏/对比篮 `service_org` / Job 记录 | 行数 + 样例键值 |
| `gkxlumenx_gapfill` | `gapfill_svc_*` 前缀表 | 行数 + 覆盖键 |
| readiness 对照 | `metric-readiness-matrix-SVC.yaml` 全部 `M_SVC_*` 的源表列 | 每指标 D4 状态 + 源表实查行数 |

每表输出：总行数、按关键维度（领域/环节/区域/年份）分布、最新批次与状态、`is_mock=1` 行数、覆盖缺口（哪个维度组合 0 行）。禁止展开全量明细。

## 4. 用例编号与 LOOP 常驻验收单（M1 定稿，M3 消费）

- 覆盖表行键 = **需规序号**（7.1.1 … 7.8.2 / 97 … 104），不另造 CASE 编号（对齐 POL 金样按序号落行）。
- LOOP 常驻验收单建议 ID：`SVC-ORG-DEMO-ACCEPT-LOOP` / `SVC-ECO-…` / `SVC-REC-…` / `SVC-PT-…`（§6.5.2；**本管线只写进计划，不建单**）。
- 每份 LOOP 计划必含：用例路径、库表清单（引用 M2）、token 文件与 `systemCode: topic` 约定、一轮四步、缺口分类表（DATA/QUERY/ALGO/ENV）、每轮≤3 张、同缺口两轮停、报告 handoff 路径 `agent-handoffs/E7-产业服务链分析/{验收单ID}.md`（只追加）、状态行「覆盖已齐，未执行。等人说『按 LOOP 跑』」。

## 5. 无人值守规则

1. 已拍板不回问；结构歧义该叶 blocked + 升级 `human:李伟`，同段其它叶继续。
2. 只读 demo 库；MCP 建单/改状态后立即 commit + push registry（多会话保护；push 被拒 → `git pull --no-rebase` 后重试一次，仍拒则稍后重试，禁止 force）。
3. 每叶 handoff：`agent-handoffs/E7-产业服务链分析/{task-id}.md`，含 `ponytail:` 行 + cost 四字段 + 架构合规自检（D12 不触业务仓 ✅ / 只读库 ✅ / 不造数 ✅）。
4. 编排仓 commit 带 `[agent:<role>]`，`origin/dev` 直推；untracked 的他人文件不碰、不 add。
5. cost：单叶 >$10 停叶复盘 / >$20 hard stop。

## 6. 段完成定义

- M1 完成时：矩阵覆盖需规条目 24/24（或多/少有 handoff 依据），每条都有界面路由 + 条件枚举锚点。
- M2 完成时：§3 清单逐库逐表落行，零「整库跳过」；每表有行数证据；受阻表有标记。
- M3 完成时：本域覆盖表每条需规一行零缺；`可演` 行的请求参数值 = 界面输入真源值且引用实查数据；`覆盖不到` 行写明缺哪类数据并引用缺口编号；主路径只串可演行；LOOP 计划含 §4 全要素且**不建单不跑**。
- M4 完成时：索引计数 = 四域调度核对合计；缺口总表 `覆盖不到` 行数 = 四域合计；每条缺口有既有引用或新登记编号，无重复编号；无修数单被创建。
