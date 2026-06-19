# Data handoff：DATA-ENT-metric-seed

- 时间：2026-06-18
- 角色：data-agent
- 任务：把 ux 设计期 ENT-wireframe 的 `M_ENT_*` metric_id 升级为 cfg_metric 8 件套种子 + 源表映射登记
- 范围：仅企业域（ENT）；不写算法实现；不连 DB

## 产物清单

| # | 文件 | 动作 | 说明 |
|---|------|------|------|
| 1 | `agent-delivery/metrics/cfg_metric-ENT-seed.yaml` | 新建 | 49 条 `M_ENT_*` 8 件套种子（目录新建） |
| 2 | `agent-delivery/data-source-mapping-registry.yaml` | 增补 | 新增 ENT 标准表 5 条（dwd.enterprise / enterprise_industry / enterprise_supply_chain / enterprise_finance_history / gkx_ads.ads_enterprise_score），未删改现有条目 |
| 3 | `agent-delivery/agent-handoffs/企业战略分析-ENT/DATA-ENT-metric-seed.md` | 新建 | 本文件 |

## metric 总数与状态分布

- **metric 总数：49**（wireframe 文末汇总 ~45，实际逐页字段表共 49 个 `M_ENT_*`）
- 映射状态分布（mapping_status，以"头条阻塞"归类）：

| 状态 | 数量 | 含义 | 代表 metric |
|------|------|------|------------|
| ✅ 源可直接聚合且口径清晰 | 14 | 可立即出数 | TOTAL_COUNT / NEW_COUNT_Y / AVG_RD_INVESTMENT / PATENT_TOTAL / TYPE_MATCH_COUNT / TYPE_RATIO / DOMAIN_COVERAGE_COUNT / PATENT_GRANT_COUNT / REVENUE_LATEST / SZ_COUNT / SZ_CHAIN_POSITION / KEY_NODE_COUNT / SUPPLIER_COUNT / RECOMMEND_COUNT |
| 🔧 formula 待 algorithm-agent | 30 | 源有原料、需算法 | 各类 *_SCORE / *_INDEX / *_RANK / 密度 / 增长率 / 利润率 / 供应链中心性等 |
| ⚠️ 口径待甲方确认 | 4 | 源可用、definition pending_data_lead | INNOVATIVE_COUNT(Q011) / HIGH_TECH_COUNT(Q010) / TYPE_COUNT(Q010) / REGIONAL_COUNT(Q012) |
| ❌ 无来源(no_source) | 1 | 需采购第三方数据 | MARKET_SHARE（缺市场规模/竞品数据） |

> 注：多数 🔧 项同时含 `definition_status: pending_data_lead`（口径也待甲方，引用 Q013~Q018）；为避免重复计数，统计时以 formula 待算法为头条状态归入 🔧，业务口径阻塞通过各条 `pending_ref` 标注。涉及口径待甲方的 metric 合计 ~30+，对应开放项 Q010~Q018。

## ODS 真源引用（DWD ← ODS 血缘）

- `dwd.enterprise` ← `dwd_org_reg_info` / `dwd_company_base` / `dwd_org_annual_financial_info` / `dwd_org_stock_base/finance_info` / `dwd_org_rd_achiev_info` / `dwd_org_tag_info` / `dwd_company_honor_tags` / `dwd_company_location_tags`
- `dwd.enterprise_industry` ← `dwd_org_industry_chain_dtl` / `dwd_industry_chain_info` / `dwd_company_industry_tags` / `dwd_industry_code`
- `dwd.enterprise_supply_chain` ← `dwd_industry_chain_info` / `dwd_org_industry_chain_dtl`（+ NebulaGraph）
- `dwd.enterprise_finance_history` ← `dwd_org_annual_financial_info` / `dwd_org_stock_finance_info`
- （以上 ODS 表均为三方要素库命名 `dwd_*`，本项目分层归 ODS 贴源层）

## K-O1 / Q009 命名冲突处置

- data-lineage-policy §3.2 企业要素正式代号为 `E1`（即 `M_E1_*`），派单与 wireframe 统一用 `M_ENT_*`。
- **本次按 `M_ENT_*` 落种子**，文件头加备注 `naming_pending_architect: Q009（ENT vs E1）`，**未擅自改成 E1**。
- 待 architect 拍板 Q009/K-O1 后，由 data-agent 批量改名（metric_id + source mapping 同步）。
- 已在 `客户决策清单跟踪表.md` Q009 行确认登记（🟡 待 architect）。

## 接力清单

### → algorithm-agent（实现 formula，30 条 `pending_algorithm`）
- 评分模型：`M_ENT_TECH_POWER_SCORE` / `M_ENT_BUSINESS_POWER_SCORE` / `M_ENT_COMPETITIVENESS_SCORE` / `M_ENT_INNOVATION_INDEX`（权重待 Q014 甲方确认）
- 排名：`M_ENT_TECH_RANK` / `M_ENT_COMPETITIVENESS_RANK`
- 比率派生：`M_ENT_RD_INVESTMENT_RATIO` / `M_ENT_REVENUE_GROWTH_RATE` / `M_ENT_PROFIT_MARGIN`
- 空间/分布：`M_ENT_REGIONAL_DENSITY` / `M_ENT_AGGLOMERATION_INDEX` / `M_ENT_CITY_DENSITY` / `M_ENT_DIVERSIFICATION_INDEX` / `M_ENT_DOMAIN_COVERAGE_BREADTH/DEPTH` / `M_ENT_CHAIN_COMPLETENESS`
- 推荐/潜力：`M_ENT_ATTRACTION_INDEX` / `M_ENT_CULTIVATION_INDEX` / `M_ENT_GROWTH_POTENTIAL` / `M_ENT_INDUSTRY_MATCH_SCORE` / `M_ENT_POLICY_MATCH_SCORE`
- 图谱（NebulaGraph）：`M_ENT_NODE_CENTRALITY` / `M_ENT_RELATION_STRENGTH` / `M_ENT_SUPPLY_CHAIN_RISK` / `M_ENT_CORE_SUPPLIER_COUNT`
- 诊断模型：`M_ENT_PAINPOINT_COUNT/SEVERITY/GAP` / `M_ENT_SHORTBOARD_COUNT` / `M_ENT_CITY_AVG_TECH_POWER`

### → api-agent（上线读取）
- 14 条 ✅ 可先行接 ADS/DWD 聚合查询联调（计数/均值/直读类）。
- 其余须等 algorithm-agent 产出 `gkx_ads.ads_enterprise_score` 等评分类 ADS 后接入。
- 上线前校验：每个 metric_id 8 件套齐全（D9 铁律：缺则不可上线）。

### → PM（推动甲方确认口径，Q010~Q018）
- Q010 企业类型判定 / Q011 创新型企业口径 / Q012 行政区划精度 / Q013 领域广度深度 / Q014 评分指标库与权重 / Q015 招引培育阈值 / Q016 对标城市集合 / Q017 供应链核心/断链规则 / Q018 痛难点诊断维度。
- Q009 命名（K-O1）→ architect 拍板。

## 架构合规自检（§2 十条）
- ① 算法只在 Python：✅ 本次仅起草 formula 占位 `pending_algorithm`，未写实现
- ⑦ 共享聚合核心：✅ source_tables 走 ODS→DWD→ADS，前端只读 ADS
- ⑧ 数据策略：✅ 标准表先行 + Mock 填充（batch=mock_20260618）
- ⑩ 数据血缘（D9）：✅ 8 件套齐全，is_mock/bid_ref/acceptance_unit_id 已填
- 其余条目本任务不涉及（无前端/Java/CI 变更）

## git
- commit message：`[agent:data-agent] 企业域 M_ENT_* cfg_metric 8件套种子 + 源表映射登记`
- commit hash：`b4bf381`（**未 push**，仅本地 commit；仅 add 种子 + registry 两文件）

## 成本回填
- model_used：Claude Opus 4.8
- actual_tokens：约 90k（精读纪律生效，未整读大文件）
- actual_cost：约 $1.5（< $10 阈值，无需复盘）
- cost_warn：false
