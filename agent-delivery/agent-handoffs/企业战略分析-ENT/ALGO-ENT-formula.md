# Algorithm handoff：ALGO-ENT-formula

- 时间：2026-06-18
- 角色：algorithm-agent（Python 算法实现臂）
- 仓库：`ent-analysis-demo`（NebulaGraph 真源 space `entan`，POC main 直推）
- 分支/提交：`main` · commit **`3e8a41a`**（**已 commit，未 push**，留 coordinator/人工确认）
- 输入真源：`agent-delivery/metrics/cfg_metric-ENT-seed.yaml`（30 条 `pending_algorithm`）
- 命名：按已会签**方案 B**，企业域全部 `M_ENT_*`（Q009 已 v1.1.0 注册助记码 ENT）

---

## 1. 范围与实现（30 条核心 `pending_algorithm`）

全部 30 条 formula 占位 → 可运行 Python 算法骨架，自测跑通。对照如下（均 ✅）：

| 分组 | metric_id | 算法 | 状态 |
|---|---|---|---|
| 评分 | M_ENT_TECH_POWER_SCORE | 5 维 minmax+加权（复用 C1 口径） | ✅ |
| 评分 | M_ENT_BUSINESS_POWER_SCORE | 6 维 minmax+加权（复用 C2 口径） | ✅ |
| 评分 | M_ENT_COMPETITIVENESS_SCORE | 技术力×W1 + 商业力×W2 | ✅ |
| 评分 | M_ENT_INNOVATION_INDEX | 专利/投入/人才/转化/资质 5 因子加权 | ✅ |
| 排名 | M_ENT_TECH_RANK | 竞技排名（同分并列） | ✅ |
| 排名 | M_ENT_COMPETITIVENESS_RANK | 竞技排名 | ✅ |
| 短板 | M_ENT_SHORTBOARD_COUNT | 维度 vs 行业基准分位 + 阈值计数 | ✅ |
| 空间 | M_ENT_REGIONAL_DENSITY | 企业数 / 面积或单位GDP | ✅ |
| 空间 | M_ENT_AGGLOMERATION_INDEX | 区位熵 LQ / 基尼系数（可切换） | ✅ |
| 空间 | M_ENT_CITY_DENSITY | 对标城市企业密度 | ✅ |
| 空间 | M_ENT_CITY_AVG_TECH_POWER | AVG(tech_score) GROUP BY city | ✅ |
| 领域 | M_ENT_DOMAIN_COVERAGE_BREADTH | 覆盖领域数 / 领域全集 | ✅ |
| 领域 | M_ENT_DOMAIN_COVERAGE_DEPTH | chain_score + 产品/专利贡献加权 | ✅ |
| 领域 | M_ENT_DIVERSIFICATION_INDEX | 领域分布熵（Shannon 归一） | ✅ |
| 供应链 | M_ENT_NODE_CENTRALITY | 图中心性 degree/betweenness/pagerank | ✅（自测 networkx 过渡） |
| 供应链 | M_ENT_CORE_SUPPLIER_COUNT | 关系强度≥阈值计数 | ✅ |
| 供应链 | M_ENT_RELATION_STRENGTH | chain_score 归一 + 共现频次 | ✅ |
| 供应链 | M_ENT_SUPPLY_CHAIN_RISK | 网络脆弱性(HHI+稀少度) → 高/中/低 | ✅ |
| 推荐 | M_ENT_ATTRACTION_INDEX | 产业相关度/政策/生态 加权 | ✅ |
| 推荐 | M_ENT_CULTIVATION_INDEX | 相关度/政策/成长/创新 加权 | ✅ |
| 推荐 | M_ENT_GROWTH_POTENTIAL | 营收/研发增速+技术壁垒+团队 | ✅ |
| 推荐 | M_ENT_INDUSTRY_MATCH_SCORE | chain_score + 目标产业相似度 | ✅ |
| 推荐 | M_ENT_POLICY_MATCH_SCORE | 企业标签 vs 政策标签匹配占比 | ✅ |
| 诊断 | M_ENT_PAINPOINT_COUNT | 多维阈值偏离命中计数 | ✅ |
| 诊断 | M_ENT_PAINPOINT_SEVERITY | 各维偏离度归一均值 | ✅ |
| 诊断 | M_ENT_PAINPOINT_GAP | 企业值 − 行业最佳分位（按维度） | ✅ |
| 比率 | M_ENT_RD_INVESTMENT_RATIO | rd_investment/revenue*100 | ✅ |
| 比率 | M_ENT_PROFIT_MARGIN | net_profit/operating_revenue*100 | ✅ |
| 比率 | M_ENT_REVENUE_GROWTH_RATE | (本年−上年)/上年*100 | ✅ |
| 比率 | M_ENT_CHAIN_COMPLETENESS | 覆盖环节/全链环节*100 | ✅ |

**合计：30/30 ✅ 全部实现且自测产出**。

### 附（超出 30 条核心，⚠️ 口径待甲方的标签计数骨架，已顺手实现供 data-agent 接力）
- `M_ENT_TYPE_COUNT`(Q010) / `M_ENT_INNOVATIVE_COUNT`(Q011) / `M_ENT_HIGH_TECH_COUNT`(Q010) —
  见 `entan/metrics/derived.py`，标签解析骨架，口径确认后启用。
### 阻塞项
- `M_ENT_MARKET_SHARE`（❌ no_source，种子已标）：ODS 无细分市场规模/竞品数据，**不实现**，
  需 PM 推动采购第三方市场调研数据后再做。

---

## 2. 参数化的待甲方数值项（不 hardcode，全在 `conf/cfg_metric_params.yaml`，标 `pending_client`）

| Q 编号 | 涉及 metric | 参数（团队临时默认） |
|---|---|---|
| **Q014** | TECH/BUSINESS/COMPETITIVENESS/INNOVATION_SCORE、TECH_RANK、COMP_RANK、SHORTBOARD、CITY_AVG_TECH | 各维度权重；竞争力 W1/W2=0.5/0.5；短板基准分位 0.5、阈值 45 |
| **Q015** | ATTRACTION/CULTIVATION/GROWTH/INDUSTRY_MATCH/POLICY_MATCH | 各推荐因子权重；推荐阈值 60 |
| **Q017** | NODE_CENTRALITY/CORE_SUPPLIER/RELATION_STRENGTH/SUPPLY_CHAIN_RISK | 核心供应商强度阈值 0.6；中心性算法 pagerank；风险分级 0.66/0.33 |
| **Q018** | PAINPOINT_COUNT/SEVERITY/GAP | 诊断四维(技术/市场/融资/管理)；严重度阈值 60；行业最佳分位 0.75 |
| Q012 | REGIONAL_DENSITY/AGGLOMERATION_INDEX | 区划精度(默认市级)；密度基准 area；集聚算法 LQ |
| Q013 | DOMAIN_COVERAGE_BREADTH/DEPTH/DIVERSIFICATION | 领域全集大小(默认样本去重)；深度权重 0.6/0.25/0.15 |
| Q016 | CITY_DENSITY | 对标城市集合(默认 北京/上海/苏州/广州/深圳) |

> 上线前甲方书面/纪要确认（升 🟢）后，调整本文件数值并升 model/metric version，无需改算法代码。
> 这些 Q 项均已在 `客户决策清单跟踪表.md` / 对应 DS-XX matrix 由 PM 跟踪，algorithm-agent **未替甲方拍板**（守 §3.8 铁律）。

---

## 3. cfg_model_registry 变更（新建）

新建 `conf/cfg_model_registry.yaml`（D9：metric ↔ model ↔ version 联动）：
- 12 个 model（ENT_WEIGHTED_SCORE / ENT_RANK / ENT_SHORTBOARD / ENT_SPATIAL_DENSITY /
  ENT_AGGLOMERATION / ENT_CITY_AGG / ENT_DOMAIN / ENT_GRAPH_CENTRALITY / ENT_SUPPLYCHAIN /
  ENT_RECOMMEND / ENT_DIAGNOSIS / ENT_RATIO），覆盖 30 条 metric。
- 每 model 带 `version=0.1.0`（与 metric seed_version 0.1.0 联动）、`params_ref`、`pending_ref`、`ads_suggest`。
- `metric_index` 提供 metric_id → model 反查（30 条全覆盖）。

代码侧 `entan/metrics/registry.py` 提供 `model_of()` / `version_of()` / `lineage()`，每个指标结果行
（`metric_row`）都带 `metric_id + model + model_version + is_mock`，可回查血缘。

---

## 4. 自测结果

- 自测：`entan/metrics/tests/test_ent_metrics.py`（mock 数据 `mock_data.py`，seed=20260618，**不依赖 DB / 真实图谱**）。
- `pytest entan/metrics/tests/ -q` → **4 passed**：
  1. `test_all_30_metrics_produced`：30 条全部产出且 metric_id 一致；
  2. `test_metric_value_sanity`：评分 0~100、排名正整数、风险∈{高,中,低}、多元化∈[0,1]；
  3. `test_lineage_registered`：30 条均能回查 model + version=0.1.0；
  4. `test_params_not_hardcoded`：改权重→评分变化（证明权重取自配置非硬编码）。
- `python -m entan.metrics.tests.test_ent_metrics` 打印 30/30 条产出概览（见提交说明）。
- 依赖：networkx + scipy（pagerank）+ numpy + pyyaml，均已在 `requirements.txt` 列出（本机已 pip 安装验证）。

---

## 5. 给 api-agent 的接口建议（哪些算法产 ADS 表供 Java 只读）

铁律 1/2/7：Java 只读 ADS，不写算法。建议 algorithm-agent 批处理把以下结果落 ADS，
api-agent（`gkxlumen-metrics` / `gkxlumen-topic`）只读：

| 建议 ADS 表 | 承载 metric | 主键/粒度 |
|---|---|---|
| `ads.ent_capability_score` | TECH/BUSINESS/COMP/INNOVATION_SCORE + TECH_RANK/COMP_RANK/SHORTBOARD | enterprise_id |
| `ads.ent_spatial_dist` | REGIONAL_DENSITY/AGGLOMERATION/CITY_DENSITY/CITY_AVG_TECH | region 或 (region,industry) |
| `ads.ent_domain_metric` | DOMAIN_COVERAGE_BREADTH/DEPTH/DIVERSIFICATION | enterprise_id |
| `ads.ent_supplychain_metric` | NODE_CENTRALITY/CORE_SUPPLIER/RELATION_STRENGTH/SUPPLY_CHAIN_RISK | enterprise_id / edge |
| `ads.ent_recommend_score` | ATTRACTION/CULTIVATION/GROWTH/INDUSTRY_MATCH/POLICY_MATCH | enterprise_id |
| `ads.ent_diagnosis` | PAINPOINT_COUNT/SEVERITY/GAP | enterprise_id |
| `ads.ent_ratio_metric` | RD_INVESTMENT_RATIO/PROFIT_MARGIN/REVENUE_GROWTH_RATE/CHAIN_COMPLETENESS | enterprise_id / chain |

- **NODE_CENTRALITY** 生产路径走 **NebulaGraph space=entan**（铁律 3，真源），批处理算完落 `ads.ent_supplychain_metric`；
  本 POC 自测用 networkx 过渡（与 demo 现状一致）。建议 api 响应保留 `source: nebula|pg`。
- 每个 metric 值旁建议 api 暴露 `/metrics/v1/catalog?ids=...` 返回 8 件套 + model/version（D9，供 UI MetricSpecCard）。
- DDL 增删需 data-agent + 架构师评审（algorithm-agent 不擅改 ADS schema，铁律）。

---

## 6. 产物清单

- `conf/cfg_metric_params.yaml`（参数化权重/阈值，pending_client 标注）
- `conf/cfg_model_registry.yaml`（12 model，30 metric 索引）
- `entan/metrics/`：`__init__ / _common / params / registry / scoring / ranking / spatial /
  domain / supplychain / recommend / diagnosis / derived` + `tests/{mock_data, test_ent_metrics}`
- 共 17 文件，1633 行，commit `3e8a41a`（未 push）

---

## 7. 架构合规自检（algorithm.mdc 铁律）

1. 算法只在 Python ✅（无任何 Java 算法）
2. ETL 写 ADS 不覆盖业务库 ✅（仅给落表建议，未动 schema）
3. 图算法用 NebulaGraph ✅（生产真源；自测 networkx 过渡已显式注明，符合 demo 现状）
4. 模型版本化 ✅（cfg_model_registry version 与 metric 联动）
5. OTel instrument ⏳ TODO（仓现有批处理未统一 instrument，留 TODO 不阻塞 POC）
6. 不在算法内写业务规则 ✅（权重/阈值全在 config，标 pending_client）
7. CI 必绿 ⏳（本地 pytest 4 passed；CI 需补 networkx/scipy 已在 requirements）
8. 算法注册 cfg_model_registry ✅
9. ODS 字段不擅自重命名 ✅（沿用 seed/dwd 字段名）

---

## 8. 成本回填（budget-estimate.md）

> task-registry 4 字段建议由 coordinator 按对应 task 行回填；本任务实测如下（单会话估算）：

- `actual_tokens`：≈ 200K（读种子/规约 + 13 源码文件生成 + 自测迭代）
- `model_used`：Claude Opus 4.8（algorithm-agent 会话模型）
- `actual_cost`：≈ $3–4（< $10 阈值，无需复盘）
- `cost_warn`：false

---

## 9. 下一步（建议 coordinator/人工）

1. 人工评审本 commit `3e8a41a` → 确认后由 coordinator 触发 `git push origin main`（POC 仓允许直推）。
2. PM 推进 Q010~Q018 甲方确认；确认后 algorithm-agent 仅调 `cfg_metric_params.yaml` 数值并升 version。
3. api-agent 按 §5 落 ADS 表 + `/metrics/v1/catalog` 接口。
4. 补 NODE_CENTRALITY 的 NebulaGraph 真源批处理（当前仅接入骨架 + networkx 自测）。
5. 补批处理 OTel instrument（铁律 5）。
