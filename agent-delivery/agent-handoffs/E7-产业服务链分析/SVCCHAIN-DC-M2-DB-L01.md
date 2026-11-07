# Handoff — SVCCHAIN-DC-M2-DB-L01

- 日期：2026-11-07
- agent：data-agent；监管人：human:徐滕强；强度：ponytail full
- 产物：
  - `agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVC-数据调研-20261107.md`
- 任务状态：M2 完成，待 coordinator 推进（依据总控 §2：M2 与 M1 并行、M3 消费本产物）

## 范围与实现

- 按总控 §3 清单逐库逐表实查：demo_gkxlumenx_dwd（svc 7 表 + org 弱相关 0 行 8 表点名）、demo_gkxlumenx_ads（svc 面 23 张逐表）、demo_gkxlumenx_ai（39 表全核对，svc=0 如实记录）、svc 业务库（实查 `gkxlumenx_topic_enterprise`，含 svc_compare_basket_item 6 行 + analysis_task svc:analysis:* 8 类）、gkxlumenx_gapfill（svc 3 表全 mock）、readiness 对照（matrix-SVC 51 条 → 去重 21 源表全部命中 demo_gkxlumenx_ods 且非空）。
- 每表输出：总行数 / 关键维度分布（国家·类型·领域·年份·环节·区域·批次）/ 最新批次与状态 / mock 标识 / 覆盖缺口；样例 ≤3 行；无全量明细展开。
- 严格只读：SELECT / SHOW / information_schema；零写操作；未跑 `--apply`；口令/连接串未入档。

## 偏离说明

1. 指定入口连接 `gkxlumenx-dwd-public-rw-mock` 认证被拒（Access denied，2 次即停未探活）→ 改用同分组 `demo-gkxlumenx-ods` 连接（同主机同账号）跨库完成，调研覆盖不受影响。as-built 已记入调研文档 §0/§9。
2. 任务给的 `gkxlumenx_topic_svc` 库不存在 → svc 业务面实际在 `gkxlumenx_topic_enterprise`（实查为准，总控 §3 允许与名单有出入）。
3. svc 模型产物在 ADS 而非 ai 库（ai 库 0 张 svc 表）；`svc_search_history`/`svc_favorite`/`svc_analysis_job` 三表全实例不存在（数据缺口）。

## 关键结论（供 M3 覆盖表引用）

- 数据面最强 = 真实池主档（43,296 家，深圳切片 14,080，九区分布齐全）；最弱 = **全球/海外轴**（仅 150 行种子面板 5 国，境外名录无源 Q-SVCCHAIN-07）。
- 链环节面：六环节堵点表有值但**中试熟化 0 行**；机构×环节成员事实表仍缺（Q-SVCCHAIN-02/04，SVC-P0-3 待供方）。
- 招引/培育：招引榜 50 行全 high 档；培育榜 11-07 15:54 由 50 行切为 3 行（growth_stage 全 NULL），bak 表保留 50 行 proxy 快照。
- **全部 svc 表无 `is_mock` 列**——覆盖表「数据情况」判定用 `data_source='mock*'` / `pending_client_confirm=1` / `q061_pending_client=1` / `rule_version=svc_rule_demo_kw_v1.1` 承载，勿写 is_mock=1（字段不存在）。
- matrix 51 条 D4=mock 全部维持，不改绿；D3=none 3 条属口径层缺口，源表实查非空不改判。

## 架构合规自检

- D12 不触业务仓 ✅（只在编排仓写文档）
- 只读库 ✅（零写操作，SELECT/SHOW/information_schema）
- 不造数 ✅（行数均实测或 information_schema 估算并标 ≈；禁写 is_mock 字段名）
- 不改 metrics/registry seed ✅（matrix 只读消费）
- 不 commit/push ✅（coordinator 统一提交）
- D9 指标口径 ✅（M_SVC_* 只读对照，D4=mock 维持不改绿）
- cicd: skip ✅（纯编排仓文档，无业务 CI 触发）

## 受阻清单

1. 入口连接认证被拒（已绕行，见偏离 1）
2. `gkxlumenx_topic_svc` 不存在（已映射到 `gkxlumenx_topic_enterprise`）
3. svc 检索历史/收藏/独立 Job 表不存在（数据缺口 → M3 对应需规行写「覆盖不到」）
4. svc Job 结果快照不落库（ai 库 0 张 svc 表）

## 调度核对

总控 §3 六行全部落节、零整库跳过；每表行数证据齐；Top10 与关键缺口见调研文档 §7/§8；`覆盖不到` 判据交 M3 按既有 Q/GAP 编号引用，未新造编号；未派任何 DATA/QUERY/ALGO 修数单。

## 验收证据

- 6 库 37 表逐表落行（`SVC-数据调研-20261107.md`）：dwd 7 表 / ads 23 表 / topic_enterprise 2 表 / gapfill 3 表 / 弱相关 2 表；零整库跳过
- readiness 对照：matrix-SVC 51 条 `M_SVC_*` → 21 张去重源表全部命中 `demo_gkxlumenx_ods` 且非空；D4=mock 全部维持
- 受阻 4 项有标记：指定连接认证被拒（绕行 demo-gkxlumenx-ods 入口）/ topic_svc 库不存在（映射 topic_enterprise）/ 检索历史·收藏·Job 快照三表不存在 / Job 结果快照不落库
- registry：evidence/cost 已回填；状态流转 MCP 留痕

## cost

- estimated_tokens: ~55,000（含 21 张表实查与文档产出）
- model_used: glm-5.3-Flash
- actual_cost: ~$0.3（< $10 阈值，无需复盘）
- cost_warn: no

ponytail: full——最小实查集（每表一条聚合查询为主）、复用既有金样体例与既有 Q/GAP 编号、不新增抽象；受 2 次即停铁律约束未做探活。
