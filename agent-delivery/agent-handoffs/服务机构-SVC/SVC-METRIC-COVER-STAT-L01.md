# SVC-METRIC-COVER-STAT-L01 · 产业服务链 STAT 21 条口径重裁（一条一过，分三批）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强`（主对话逐条拍板，AI 执笔） |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（definition 定义类任务） |

## 问题清单

- 18 条 MODEL / 3 条 GRAPH 不在本单范围（DoD 约束，未动）。
- `dwd_service_org`（50 行）确认为废弃 demo mock，主档统一改挂 `dwd_org_base_info`（189,116 行；深圳切片 95,600；圈定池∩深圳真数 **14,033**）。
- 环节轴历史冲突：算法侧曾把环节源写成产业链 `industry_link_code`（产业链节点）；CT-SVC-PT-01 / Q-SVCCHAIN-08 明确服务六环节≠产业链节点，两套口径不可互换。16/17/20 三条已按服务六环节锁死并写禁项。

## 修改内容（三批 21 条，改前 → 改后）

### 批1（Seq 1–7，机构池基础）

| Seq | ID | 改前 | 改后 | 一句话口径 |
|---|---|---|---|---|
| 1 | M_SVC_ORG_TOTAL | v0.1.0 演示态 | **v0.2.0** | 圈定池 `svc_org_circle` COUNT(*)=43,296；fact 35,411 / series 35,410（无成立日差 1） |
| 2 | M_SVC_ORG_SELECTED_COUNT | v1 演示 | **v0.3.0 retired** | 勾选家数是 UI 状态非指标；页面可显 N、不挂 ⓘ、不灌 ADS |
| 3 | M_SVC_ORG_NEW_COUNT | v1 演示 | **v0.2.1** | series 相邻年差（侯佳伟 3A）；缺成立年只进 fact 不进 series；1 家无成立日→末年 35,410 |
| 4 | M_SVC_ORG_TECH_SCORE | 未动（MODEL，不在范围） | 未动 | — |
| 5 | M_SVC_ORG_MARKET_HEAT | 未动（MODEL） | 未动 | — |
| 6 | M_SVC_GRAPH_* | 未动（GRAPH） | 未动 | — |
| 7 | M_SVC_ORG_COVERAGE_DEPTH | 未动（MODEL） | 未动 | — |

> 批1 说明：DoD 原注「ORG_TOTAL 已落」属实；SELECTED/NEW/TECH/HEAT/DEPTH 按范围裁剪，MODEL/GRAPH 未进本单。

### 批2（Seq 8–14，平台维度）

| Seq | ID | 改前 | 改后 | 一句话口径 |
|---|---|---|---|---|
| 8 | M_SVC_PT_GLOBAL_TOTAL | v0.1.0 | **v0.2.0** | 国内格 COUNT(*) 可执行；全球格挂 Q-SVCCHAIN-07（海外/港澳台无源） |
| 9 | M_SVC_PT_GLOBAL_TYPE_DIST | v0.1.0 | **v0.2.0** | 高校/院所恒 0（本体不属服务机构口径）；企业=池内其余；判型 JOIN heis/research_institute |
| 10 | M_SVC_PT_GLOBAL_SCALE_DIST | v0.1.0 | **v0.2.0** | 四档 [0,50)/[50,200)/[200,500)/[500,+]；人数优先→注册资本兜底→未分档残档；偏差登记 Q-SVCCHAIN-06 |
| 11 | M_SVC_PT_SZ_TOTAL | v0.1.0 | **v0.2.1** | city 经 `dwd_org_base_info` JOIN；深圳真数 14,033；数随池联动不写死 |
| 12 | M_SVC_PT_SZ_TYPE_DIST | v0.1.0 | **v0.2.1** | 企业=14,033、高校/院所=0（同第 11 条 JOIN 口径）；单色环如实 |
| 13 | M_SVC_PT_SZ_REGION_ORG | v0.1.0 | **v0.2.1** | 标准十区字典全集常显；空 `area` 单列「未分配」5 家；南山 3,655…大鹏 0 |
| 14 | M_SVC_PT_SZ_FIELD_DIST | v0.1.0 | **v0.2.0** | 15 集群全集常显；五跳链 circle→base_info→ent_industry_chain→chain→map→cluster；无上链→未分配 14,033；D3=none 如实 |

### 批3（Seq 15–21，链路与对比）

| Seq | ID | 改前 | 改后 | 一句话口径 |
|---|---|---|---|---|
| 15 | M_SVC_PT_CHAIN_NODE_ORG | v0.1.0 | **v0.2.0** | 预统计宽表 15×6=90 格（产业轴=15 集群 × 环节轴=六站）；「选定产业」=查询层下钻不进口径 |
| 16 | M_SVC_CHAIN_SEGMENT_AVG_DEPTH | v1 演示 | **v0.2.0 draft** | 六环节 AVG(depth) 目标口径；双缺口（成员表 SVC-P0-3 + 深度分 Q-02）；不写 metric: 引用防继承 MODEL 错轴 |
| 17 | M_SVC_CHAIN_SEGMENT_ORG_COUNT | v1 演示 | **v0.2.0 aligned** | 六环节 COUNT(DISTINCT org_id)；0 家返回 0 不伪造；缺口 SVC-P0-3 |
| 18 | M_SVC_ORG_COVERAGE_BREADTH | v0.1.0 自建表 | **v0.3.1 aligned** | 对齐 M_ENT_DOMAIN_COVERAGE_COUNT：circle→上链→L0→cluster_map；无上链=0；不挂 Q-08 |
| 19 | M_SVC_REC_CANDIDATE_CNT | v0.2.0 挂 STAT | **v0.3.0 retired** | 推荐「共 N 家」= results.length 实时集非指标；作废 08-28 侯佳伟 1B 口径；不建表不灌 ADS |
| 20 | M_SVC_SZ_CHAIN_COMPLETENESS | v1 演示 | **v0.2.0 draft 挂起** | 公式未签（Q-04/唐绍祖）+环节无源；对比页诚实排除不画柱；轴若用覆盖只认服务六环节 |
| 21 | M_SVC_SZ_COMPARE_METRIC | v1 演示 | **v0.2.0 aligned 部分闭合** | 多格面板：仅深圳×服务机构数 live（同第 11 条 14,033）；外市/技术力/密度不灌，fixture+🧪⚠️ |

**最终分布**：锁口径 17 条 / 挂起 2 条（16、20）/ 废止 2 条（2、19）；MODEL 3 条 + GRAPH 3 条未动（范围外）。

### registry 层同步

- `cfg_metric-SVC-seed.yaml`：21 条 definition/formula/source_tables/version/is_mock/pending_ref 全量重写（+328/−255 行）
- `metric-readiness-matrix-SVC.yaml`：D1/D2/D3/D4 四维 + d1_note 逐条对齐；**未把任何甲方黄项改绿**，D3 未升 full、D4 未升 live
- `calc-logic/SVC/`：19 个 md 重写 + 2 新增（`M_SVC_BASE_101_1.md`、`M_SVC_TYPE_DIST_QUERY.md`，算法轨封面叶，随本批一并落盘）
- 纯 CRLF 纪律保持（两 YAML 孤 LF=0，Ruby YAML 解析通过）

## 测试结果

- YAML 解析：`cfg_metric-SVC-seed.yaml`（43 条）、`metric-readiness-matrix-SVC.yaml` 均通过
- CRLF：两文件孤 LF = 0
- 真数锚点（live MySQL 实查）：池 43,296 / 深圳 14,033 / 十区分布（南山 3,655…大鹏 0 + 未分配 5）/ 主档 189,116（深圳 95,600）
- 一致性：每条 seed ↔ 矩阵 ↔ calc-logic 三方版本号、口径、缺口描述一致

## 遗留风险

- D1 多条仍 draft（待甲方 Q-SVCCHAIN-06/07 签认），**签认前不得升 aligned**
- Seq 16/20 解挂条件：唐绍祖公式定义卡 + 供方交付机构×环节成员表（SVC-P0-3）
- Seq 18 上链灌 INB 与 ENT 同闸；Q068 15 集群目录仍黄
- 深圳真数随圈定池批次浮动，页面禁止写死 14,033

## CI/CD（必填）

- 分支：`dev`（gkx-orchestration 无业务 CI）
- commit：`3a9bf38c` 已推 origin/dev（2026-10-14 经确认后推送）
- pipeline / K8s / dev URL：N/A（纯定义文档仓）

## Cost（2026-10-15 补填）

- actual_tokens: ~500k（估算，含探库、21 条一条一过、三方落盘）
- model_used: glm-5.3
- actual_cost: ~$3.7
- cost_warn: false（< $10 阈值）

## 涉及文件

- `agent-delivery/metrics/registry/cfg_metric-SVC-seed.yaml`
- `agent-delivery/metrics/registry/metric-readiness-matrix-SVC.yaml`
- `agent-delivery/metrics/registry/export/指标与数据开发进度.xlsx`（进度导出随批刷新）
- `agent-delivery/metrics/calc-logic/SVC/*.md`（19 改 + 2 增）
- `agent-delivery/metrics/request/专题系统/CHAIN-SVC-COVER-STAT-定义分流-20261012.md`（定义分流依据）
