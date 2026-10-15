---
task_id: CHAIN-METRIC-COVER-STAT-L01
task_type: definition
owner: agent:data-agent
supervisor: human:徐滕强
status: ready_to_sign
date: 2026-10-15
ponytail: full（GKX 护栏优先；定义任务产物完整性优先于缩代码）
---

# CHAIN-METRIC-COVER-STAT-L01 Handoff

> 产业链域 STAT/COMPUTE 指标口径全覆盖：40 条逐一拍板、实核落盘。监管人 human:徐滕强 全程逐条确认，无一条未经拍板落盘。

## 1. 范围与实现

**范围**：`cfg_metric-CHAIN-seed.yaml` 99 条中 `algorithm_type ∈ {STAT, COMPUTE}` 的全部 40 条（对照任务定义：CHAIN STAT/COMPUTE 口径定义全覆盖）。

**交付**：38 条升 v0.2.0（seed 口径 + 公式 + 矩阵行 + calc-logic MD 三件套），2 条维持 OPEN（T0-X 注册轨，范围外排除）。

### 1.1 处置分布（38 条 v0.2.0）

| 处置模式 | 条数 | 明细 |
|---|---|---|
| 直数/聚合口径（现网可执行 SQL） | 24 | 市场规模/增长率、企业/新增企业/机构/全球区域/全国区域/总数、深圳企业/机构/区域、产品、专利、投融资、资讯、REG 生态等 |
| 读表口径（ADS v2 metric_fact/dist 直读，等模型灌数） | 10 | 瓶颈 3 条、SZ 问题、布局推荐、优势排名、情感占比等 |
| 三段式（临时出数 + 正式完整保留 + 切换条件） | 2 | HOT_NEWS_COUNT（临时全量代热点）、CONCENTRATION_INDEX（临时 HHI+融资额份额） |
| 锁定待值集（公式结构定，枚举占位） | 2 | SZ_KEY_NODE_COVERAGE、HIGH_VALUE_RATIO（共用 GAP-CHAIN-IMPORTANCE-ENUM） |
| 挂起（无好临时方案，决策卡交唐绍祖） | 1 | INTERNATIONALIZATION_INDEX（QC 号待开） |

**未动 2 条**（范围外，维持 v0.1.0 OPEN）：`M_CHAIN_BASE_95_1`（ALGO-CHAIN-BASE-95 建模任务）、`M_CHAIN_CHOKE_LINK_COUNT`（TOPIC-DIAG-017）——均 GAP-ALGO-TYPE-UNSIGNED 注册轨，唐绍祖未签，动即越权。

## 2. 关键拍板记录（human:徐滕强，2026-10-13 ~ 10-14）

| 日期 | 拍板 | 影响条目 |
|---|---|---|
| 10-14 | STAT 口径=读表口径：读表 SQL 定即口径全定；模型卡未冻结只影响何时有数不进口径 | 瓶颈组 5 条 + ADVANTAGE_RANK + SENTIMENT |
| 10-14 | L1 归一口径（B 方案）：REG_ECOSYSTEM 同构家族统一 COALESCE(parent_node_id,node_id) 折 L1 | SZ_COMPLETENESS、KEY_NODE_COVERAGE、HIGH_VALUE_RATIO |
| 10-14 | 表体系纠正：DWD 现行=v5、ADS 现行=v2 配套；旧 chain_*（DWD 7 张/ADS 8 表）全废止禁引用 | 全部 source_tables 重写 |
| 10-14 | 有目标表先基于表结构定版，无数据不挡口径 | ADVANTAGE_RANK、瓶颈组 |
| 10-14 | HOT_NEWS 三段式：临时全量代热点 + UI 不体现临时标注 | HOT_NEWS_COUNT |
| 10-14 | 临时方案可以错但正式口径必须完整保留不污染 | CONCENTRATION_INDEX |
| 10-14 | INTERNATIONALIZATION 无好临时方案，直接挂起 | INTERNATIONALIZATION_INDEX |
| 10-14 | LAYOUT_RECOMMEND 方案A：统计对象=单链发展方案条数（贴 demo 页面语义） | LAYOUT_RECOMMEND_COUNT |

## 3. 产物清单

| 文件 | 变更 |
|---|---|
| `agent-delivery/metrics/registry/cfg_metric-CHAIN-seed.yaml` | 38 条 v0.1.0→v0.2.0（definition/formula/source_tables/calc_logic_ref/pending_cosign 全重写） |
| `agent-delivery/metrics/registry/metric-readiness-matrix-CHAIN.yaml` | 新增/更新 38 行（d1/d3/d4/lifecycle 如实标注，挂起条 d1=draft/d3=none/blocked） |
| `agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_*.md` | 新建/重写 38 份计算逻辑说明（含废弃表禁用声明、禁止冒充项、解挂条件） |

全部文件纯 CRLF（lone LF=0 校验通过），YAML 解析通过。

## 4. 新增缺口登记（4 个）

| 编号 | 内容 | 责任方 | 解锁条目 |
|---|---|---|---|
| GAP-CHAIN-HEAT-SCORE | NLP 热度打分管线落 heat_score | 算法侧 | HOT_NEWS_COUNT 正式口径 |
| GAP-CHAIN-SENTIMENT | NLP 情感标注（建议与 heat_score 同管线一次产出） | 算法侧 | NEWS_SENTIMENT_RATIO |
| GAP-CHAIN-IMPORTANCE-ENUM | importance_level 值域字典 + 标注层级（问供应方，一次问清双解锁） | 数据侧→供应方 | SZ_KEY_NODE_COVERAGE、HIGH_VALUE_RATIO |
| QC-NEW-INTERNATIONALIZATION | 国际化因子集/权重决策项（**待开号**，建议并入 QC02 组） | PM→客户决策清单 | INTERNATIONALIZATION_INDEX |

## 5. 验收证据

- 逐条拍板记录见本 handoff §2 + 会话全程（监管人在线确认每一条后才落盘）
- YAML/CRLF 校验脚本输出：38 条 v0.2.0、矩阵行各恰好 1 次、lone LF=0
- 实核数据库：demo_gkxlumenx_{ods,dwd,ads}（公网 MCP 连接，表结构/行数/值分布均有查询记录）

## 6. 架构合规自检

- ✅ §2.1 算法只在 Python：COMPUTE 条目全部挂起/决策卡交算法侧，未替拍
- ✅ §2.10 D9 数据血缘：38 条 8 件套齐（algorithm_type/源表/版本/calc_logic_ref），无终态 8 件套卡死叶（挂起条如实 draft/blocked）
- ✅ §3.1 决策不外包：所有口径拍板均 human:徐滕强 逐条确认；QC 项未替甲方拍
- ✅ §3.8 业务口径甲方拍板：QC01/02/04/08/09 全程维持 🟡 未动
- ✅ 无伪造：所有现网 0 行/字段缺失如实 NULL/none/blocked，无临时数冒充正式

## 7. 遗留待办（移交，非本批）

1. **唐绍祖会签**：38 条 v0.2.0 formula（pending_cosign 已逐条标注）
2. **QC 号开设**：QC-NEW-INTERNATIONALIZATION 入客户决策清单跟踪表
3. **供应方题单**：追加 importance_level 值域字典 + 标注层级
4. **NLP 管线任务**：heat_score + sentiment 双标注（可并一条管线一次产出）
5. REG 系 9 条（d1=draft/lc=open）：10-13 已定版口径，矩阵 d1/d3 与 seed v0.2.0 的对齐刷新待下批（本轮聚焦 40 条收口，REG 矩阵行状态滞后是已知项）

## 8. cost

- actual_tokens: ~850k（含探库、38 条三件套读写、逐条确认往返）
- model_used: glm-5.3
- actual_cost: ~$6.2
- cost_warn: false（< $10 阈值）
