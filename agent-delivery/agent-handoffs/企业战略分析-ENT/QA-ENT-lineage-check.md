# QA Handoff：企业域 metric_id 贯穿一致性核验（设计期 / Wave 0）

- 时间：2026-06-18
- 角色：qa-agent（QA + 测试架构师 / 只读核验）
- 范围：企业分析（战略分析）Wave 0 全链路产物 metric_id 贯穿一致性
- 核验类型：**设计期 metric_id 贯穿核验**（Mock 阶段无真实数据，做"跨制品一致性 + 8 件套完整性 + 命名合规 + 验收覆盖"核验，**替代** `data-lineage-policy §7.6` 的「UI→API→ADS→DWD→ODS」4 段真实数据核验）
- ⚠️ **真实 4 段链路核验待 Wave 1 数据接入后补做**（Wave 0 全部 `is_mock=true`，无真实 DB 可查；本次未连任何 DB）
- 核验依据：`data-lineage-policy.md` §2（8 件套）/§3.2.1（v1.1.0 命名）/§7.6（qa 职责）
- 核验对象（commit / 路径）：
  - 设计：`topic_demo/docs/ia/enterprise/ENT-wireframe.md`（49 metric_id 汇总 + 9 页字段表）
  - 数据：`agent-delivery/metrics/registry/cfg_metric-ENT-seed.yaml`（49 条 8 件套，commit `b4bf381` 未 push）
  - 算法：`ent-analysis-demo/conf/cfg_model_registry.yaml` + `entan/metrics/registry.py`（30 条 model 映射）
  - API：`agent-delivery/agent-handoffs/企业战略分析-ENT/API-ENT-metrics-catalog.md`（catalog + 14 ✅ 端点 + 35 待接）
  - 决策：`客户决策清单跟踪表.md` Q009~Q018
  - UI：`topic_demo/src/app/pages/enterprise/Enterprise{Type,Domain}Distribution.tsx`（commit `bc16e5a` 未 push）

---

## 一、7 项核验结论表

| # | 核验项 | 结论 | 证据摘要 |
|---|--------|------|----------|
| 1 | metric_id 集合一致性 | ✅ | wireframe 枚举 49 ↔ 种子 49 ↔ 算法 30(🔧) ↔ API 14✅+35待接=49，总数与分组自洽，30 条算法集与种子 🔧 集**逐条相等**（详见 §二） |
| 2 | 命名合规（`M_ENT_*` / 无 `M_E1_*`） | ✅ | 全仓实际 metric_id 100% `M_ENT_*`（49+30+UI 引用），`M_E1_` 仅出现在 4 处**说明性文字**（讨论废弃别名），无任何实际指标使用；符合 policy v1.1.0 §3.2.1 |
| 3 | 8 件套完整性（抽样 9 条覆盖 ✅/🔧/⚠️/❌） | ✅ | 抽样 9 条 8 字段全齐，占位标注规范（`pending_algorithm`/`pending_data_lead`/`no_source`/`Q0xx` 引用齐备）；轻微：⚠️ 项 definition 偏短（<50 字，ARCH 已记 Wave 1 整改） |
| 4 | 算法↔种子联动 + pytest | ✅ | `cfg_model_registry.metric_index` 30 条全部带 model+version(0.1.0) 联动，与种子 30 🔧 完全对应；`pytest entan/metrics/tests/ -q` → **4 passed in 1.77s** |
| 5 | 验收覆盖闭环（10 子功能↔E-20~E-30↔metric_id） | ✅ | bid §1.1.1.2.4.2.3.1~.10（10 子功能）+ E-20 概述 → E-20~E-30（11 验收单元）；种子 49 条 `bid_ref`+`acceptance_unit_id` 两列齐备，E-20~E-30 全覆盖，可双向追溯 |
| 6 | UI 占位（ⓘ / 🧪 / ⚠️） | ✅ | 2 个新页 KPI 旁 `MetricLineageBadge`：ⓘ(title 暴露 metric_id+口径) + 🧪 MockBadge + ⚠️(口径待甲方)，引用 metric_id 均为合法 `M_ENT_*` 且与种子一致 |
| 7 | 阻塞/风险清单 + 影响 | ⚠️ | 9 项业务口径 🟡(Q010~Q018) 阻塞上线移除 ⚠️ 角标；MARKET_SHARE(❌/K-O7) 无来源；2 处文档陈旧漂移（详见 §六、§七）。真实 4 段核验待 Wave 1 |

> **综合：6 项 ✅ + 1 项 ⚠️（均为待办/陈旧文案，非硬性不一致）。设计期贯穿一致性达标。**

---

## 二、metric_id 集合一致性（核验项 1 详证）

### 2.1 总数与状态分布

| 制品 | 计数 | 备注 |
|------|------|------|
| wireframe 9 页"本页 metric_id 清单"枚举合计 | **49** | 6+6+4+9+6+6+5+3+4=49 |
| wireframe 文末汇总叙述 | "~45" | ⚠️ **叙述漂移**：文末写"共 ~45 个"，实际枚举 49（见 §六-1） |
| 种子 `cfg_metric-ENT-seed.yaml` `total_metrics` | **49** | `mapping_status` 实测 ✅14 / 🔧30 / ⚠️4 / ❌1 = 49，与文件自带footer一致 |
| 算法 `metric_index` | **30** | 对应 30 条 `pending_algorithm`（🔧） |
| API `/catalog` 待接清单 | **35** | =49−14；分解 30🔧+4⚠️+1❌=35 ✅ |
| API ✅ 直接聚合端点 | **14** | 14+35=49 ✅ |

### 2.2 算法 30 条 ↔ 种子 30 🔧 ——逐条相等（无遗漏 / 无拼写漂移）

`metric_index` 30 个 key 与种子 `mapping_status:🔧` 的 30 条 metric_id 集合**完全相同**（评分×4 / 排名×2 / 短板×1 / 空间密度×2 / 集聚×1 / 城市聚合×1 / 领域×3 / 中心性×1 / 供应链×3 / 推荐×5 / 诊断×3 / 比率派生×4 = 30）。每条均落到 11 个 model（`ENT_WEIGHTED_SCORE`/`ENT_RANK`/`ENT_SHORTBOARD`/`ENT_SPATIAL_DENSITY`/`ENT_AGGLOMERATION`/`ENT_CITY_AGG`/`ENT_DOMAIN`/`ENT_GRAPH_CENTRALITY`/`ENT_SUPPLYCHAIN`/`ENT_RECOMMEND`/`ENT_DIAGNOSIS`/`ENT_RATIO`）之一，version 均 0.1.0。

### 2.3 14 条 ✅ ↔ 种子 ✅ 核对

种子 14 条 ✅：TOTAL_COUNT / NEW_COUNT_Y / AVG_RD_INVESTMENT / PATENT_TOTAL / TYPE_MATCH_COUNT / TYPE_RATIO / DOMAIN_COVERAGE_COUNT / PATENT_GRANT_COUNT / REVENUE_LATEST / SZ_COUNT / SZ_CHAIN_POSITION / KEY_NODE_COUNT / RECOMMEND_COUNT / SUPPLIER_COUNT —— 与 API §3 的 14 端点 metric_id **逐条相等** ✅。

---

## 三、命名合规（核验项 2 详证）

- 实际 metric_id：种子 49 + 算法 30 + UI 引用（M_ENT_TYPE_MATCH_COUNT / M_ENT_TYPE_RATIO / M_ENT_REGIONAL_COUNT / M_ENT_REGIONAL_DENSITY / M_ENT_AGGLOMERATION_INDEX / M_ENT_DOMAIN_COVERAGE_COUNT / M_ENT_DIVERSIFICATION_INDEX / M_ENT_DOMAIN_COVERAGE_DEPTH）—— **全部 `M_ENT_*`**。
- `M_E1_` 全仓扫描命中 4 处，**均为说明性文字**（非 metric_id 取值）：
  - `topic_demo/docs/ia/enterprise/README.md:62`（开放项 K-O1 描述）
  - `ARCH-ENT-milestone-review.md:22,26`（Q009 拍板建议）
  - `DATA-ENT-metric-seed.md:40`（命名前提说明）
  - `cfg_metric-ENT-seed.yaml:11`（header 注释）
- `ent-analysis-demo`（conf/yaml + entan/metrics/*.py）扫描 `M_E1_` → **0 命中**。
- 结论：符合 policy v1.1.0 §3.2.1（ENT 现行助记码，E1 已降为废弃别名）✅。

---

## 四、8 件套完整性抽样（核验项 3 详证）

抽样 9 条（覆盖 ✅/🔧/⚠️/❌ 四类），8 字段 = metric_id / metric_name_zh / definition / formula / source_tables / source_systems / update_freq / version：

| metric_id | 状态 | 8 字段 | 占位标注 |
|-----------|------|--------|----------|
| M_ENT_TOTAL_COUNT | ✅ | 齐全 | 无占位，公式可执行 |
| M_ENT_PATENT_TOTAL | ✅ | 齐全 | 无占位 |
| M_ENT_INNOVATIVE_COUNT | ⚠️ | 齐全 | `definition_status:pending_data_lead` + `pending_ref:Q011` ✅ |
| M_ENT_HIGH_TECH_COUNT | ⚠️ | 齐全 | Q010 ✅ |
| M_ENT_TYPE_COUNT | ⚠️ | 齐全 | Q010 ✅ |
| M_ENT_REGIONAL_COUNT | ⚠️ | 齐全 | Q012 ✅ |
| M_ENT_TECH_POWER_SCORE | 🔧 | 齐全 | `formula:pending_algorithm` + Q014 ✅ |
| M_ENT_NODE_CENTRALITY | 🔧 | 齐全 | `pending_algorithm` + NebulaGraph 真源标注 ✅ |
| M_ENT_MARKET_SHARE | ❌ | 齐全 | `source_tables:[]` 空 + `source_status:no_source` ✅ |

- 全 49 条均带 `source_systems:["Mock @ batch=mock_20260618"]` + `is_mock:true`（符合 §FAQ Q5）。
- **轻微问题（非阻塞，Wave 1 整改，ARCH 已记）**：① ⚠️ 项 definition 偏短（<policy 要求的 50 字）；② `source_tables` 把 ADS/DWD 混写为字符串、缺 DWS 层、ADS 复用 `dwd.enterprise` 而非独立 `ads_*` 表名。

---

## 五、算法↔种子联动 + pytest（核验项 4 详证）

- `registry.py` 提供 `model_of()` / `version_of()` / `lineage()`，从 `cfg_model_registry.yaml` 反查 model+version，metric↔model version 同步起步 0.1.0。
- 30 条 `metric_index` 全部带 `pending_ref`（Q012~Q018，比率类无 pending），可追溯甲方决策。
- 回归：`cd ent-analysis-demo && python -m pytest entan/metrics/tests/ -q` → **`4 passed in 1.77s`** ✅（与基线一致）。

---

## 六、不一致 / 漂移项清单

| # | 等级 | 项 | 位置 | 描述 | 建议 |
|---|------|----|------|------|------|
| 1 | ⚠️ 轻微 | wireframe 汇总叙述漂移 | `ENT-wireframe.md:418` | 文末写"共 ~45 个 metric_id"，实际 9 页枚举 = 49，与种子 49 不符（叙述近似值，非清单错误） | 文案改"49 个"以消歧 |
| 2 | ⚠️ 轻微 | Q009 已会签但文案陈旧 | 种子 `:10-13,28` / README `:62` / `DATA-ENT-metric-seed.md:40` | Q009 已 🟢 会签（方案 B，2026-06-18），policy 已 bump v1.1.0；但上述 3 处仍写"待 architect 拍板/统一"（K-O1 视为开放） | 同步为"Q009 已会签，K-O1 关闭"；命名本身已合规无需改名 |
| 3 | ⚠️ 轻微 | API §4 CHAIN_COMPLETENESS 重复归类 | `API-ENT-metrics-catalog.md:79,80` | CHAIN_COMPLETENESS（种子 🔧）同时列入"口径待甲方计数"行与"链/环节派生"行；且前者本应只含 4 个 ⚠️ 项 | 仅保留"链/环节派生"归类 |
| 4 | ⚠️ 待补登 | MARKET_SHARE(K-O7) 未入中央决策表 | `客户决策清单跟踪表.md` | 中央表扫描无 MARKET_SHARE / K-O7（仅在 UX/ARCH handoff 出现）；ARCH §四.4 已建议补登 | PM 补登 K-O7（采购/降级/下架）到中央跟踪表 |

> 以上 4 项均为**文案陈旧 / 归类瑕疵 / 登记遗漏**，不构成 metric_id 集合或命名的硬性不一致；核验项 1/2 仍判 ✅。

---

## 七、阻塞 / 风险清单（核验项 7）

### 7.1 业务口径阻塞（🟡 待甲方，阻塞"上线移除 ⚠️ 角标"）

| 决策项 | 影响 metric_id | 验收单元 | 上线影响 |
|--------|----------------|----------|----------|
| Q010 | TYPE_COUNT / TYPE_RATIO / HIGH_TECH_COUNT | E-20/E-21 | 企业类型/高企口径未定，类型分析数字不可对甲方定稿 |
| Q011 | INNOVATIVE_COUNT | E-20 | 创新型企业并集口径未定 |
| Q012 | REGIONAL_COUNT / REGIONAL_DENSITY | E-21 | 行政区划下钻精度未定（临时到市级） |
| Q013 | DOMAIN_COVERAGE_BREADTH/DEPTH / DIVERSIFICATION_INDEX | E-22 | 覆盖广度/深度口径未定 |
| Q014 | TECH/BUSINESS/COMPETITIVENESS_SCORE 等 8 项 | E-23/E-24/E-30 | 评分权重未定（可参数化先实现骨架，数值待注入） |
| Q015 | ATTRACTION/CULTIVATION_INDEX 等 5 项 | E-26/E-27 | 推荐阈值/权重未定 |
| Q016 | CITY_DENSITY / CITY_AVG_TECH_POWER | E-25 | 对标城市集合未定 |
| Q017 | CORE_SUPPLIER_COUNT / SUPPLY_CHAIN_RISK 等 | E-28 | 核心供应商阈值/断链评级未定 |
| Q018 | PAINPOINT_COUNT/SEVERITY/GAP | E-29 | 诊断维度/阈值未定（依赖专家知识库） |

> 全部按"团队临时默认值"先跑（标 🟡），UI 已加 ⚠️"待甲方确认"角标；上线前须升 🟢。

### 7.2 无来源风险（❌）

- **M_ENT_MARKET_SHARE**（E-24）：ODS 要素库无市场规模/竞品数据，`no_source`。影响范围仅 1 条；需采购市场调研数据或下架/降级。**且未登记中央决策表（K-O7）→ 须补登**。

### 7.3 真实数据核验缺口（Wave 0 固有）

- Wave 0 全 Mock，**policy §7.6 的「UI→API→ADS→DWD→ODS」4 段真实链路核验本期无法执行**（无真实 DB）。本报告以设计期贯穿一致性替代。
- blocker 抽样真实值核验、性能基线（P95<500ms）、视觉回归基线 —— **均待 Wave 1 数据 + lumen 复刻后补做**。

---

## 八、Go / No-Go

**结论：GO（设计期贯穿一致性达标，带待办）**

- ✅ 可继续推进：algorithm-agent 参数化实现 30 条 🔧 formula、api-agent 接 14 条 ✅ ADS 端点 —— 设计期 metric_id 骨架自洽、命名合规、8 件套齐全、算法回归绿、验收闭环。
- 📌 上线前必办（移除 ⚠️ / 进入 Wave 1 前）：
  1. PM 推动 Q010~Q018 甲方书面确认 → 🟡 升 🟢，UI 移除 ⚠️ 角标；
  2. MARKET_SHARE(K-O7) 补登中央决策表 + 采购/降级/下架决策；
  3. 文案同步：wireframe 汇总改 49、种子/README/DATA-handoff 同步 Q009 已会签、API §4 去重 CHAIN_COMPLETENESS；
  4. Wave 1 数据接入后补做 policy §7.6 真实 4 段链路核验 + 8 件套 definition 补足 ≥50 字 + source_tables 补 DWS 层 / 正式 ADS 表名；
  5. 性能基线 + 视觉回归基线（lumen 复刻后）。

---

## 九、架构合规自检（公约 §2，与 architect-agent 联签项）

| 铁律 | 自检 |
|------|------|
| 1 算法只在 Python | ✅ 30 🔧 全部落 `ent-analysis-demo` Python，Java(API) 仅 SQL 级聚合 |
| 7 共享聚合核心 / 只读 ADS | ✅ API catalog 定位聚合核心，全 `ent_*` 只读 |
| 8 数据策略 ADS 先行 + Mock | ✅ Wave 0 全 Mock，字段按 ODS/DWD 口径占位 |
| 9 D8 前端规范 | 🟡 topic_demo 原型按派单豁免（保留旧栈），lumen 复刻执行 Arco |
| 10 D9 数据血缘 8 件套 | ✅ 49 条齐全；UI ⓘ/🧪/⚠️ 占位在位，完整 MetricSpecCard 留 lumen |

---

## 十、成本回填（budget-estimate.md）

| 字段 | 值 |
|------|----|
| actual_tokens | ~95k（读 policy/qa.mdc + 5 制品片段 + 4 handoff + pytest + UI 占位 grep） |
| model_used | Claude Opus 4.8（cursor agent） |
| actual_cost | ~$3.5（< $10 阈值，无需复盘） |
| cost_warn | false |
