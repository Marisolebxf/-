# 项目 DWD / ADS 表结构（非指标）对 ODS 底层支撑（2026-08-24 本地）

> 承接早上已取消的 `ENT-DATA-SUPPORT-CONCLUSION-L01`。  
> **本文件只评表结构能不能从 ODS 喂出来**，不评王惠 60 个 `metric_id`、不评 8 件套。  
> DWD 预聚合 KPI 表（`enterprise_region_summary` 等）视为指标层，**本轮排除**。  
> 不入库、不建注册表任务。

## 0. 范围与证据

| 项 | 值 |
|---|---|
| 目标结构真源 | `stores/mysql/dwd-entity.md` / `dwd-risk.md` / `ads.md` + Mapping v1.2 |
| ODS 探测 | `demo_gkxlumenx_ods`（MCP，2026-08-24） |
| 正式 DWD/ADS | `gkxlumenx_dwd` 连接超时，**不以现网灌数行数为 A/B 依据** |
| Mapping | `企业域-ETL-Mapping明细-源表到DWD.md` v1.2 |

三类仍用早上口径：

- **A** 目标表有设计，ODS 有对应表且当前样例有有效行（表自身能映射）
- **B** 目标表有设计，ODS 有表/字段，但空、全删、或跨表对不上同一批企业
- **C** 目标表有设计，ODS 缺表或缺该业务对象的独立关系/维度

`join_sparse`：源表可以是 A，目标若强依赖回连主档则降为 B。

---

## 1. 一页结论

项目 DWD 工商/风险/国外 + ADS 算法结果面，**不是**“ODS 166 张表到了就能灌”：

1. **国内主档、高管、财务、资讯、招聘、上市、招投标、融资/投资、子公司、9 类风险事件：ODS 有表有数，结构可支撑 Mapping 起草。**
2. **产业链企业上链表、真实供应链、合作、创新载体、基金项目：目标 DWD 有表，ODS 没有合格对象源。**
3. **专利有主表，企业专利明细只能名称回连；产业标签 2 万行仅约 6 条信用代码命中主档。**
4. **国外 6 张 `enterprise_forg_*`：主体/股东/高管/产品空；年报财务有数但无主档，构不成实体链。**
5. **ADS 全部没有 ODS 1:1 源表。** 能写的前提是 DWD 实体/事件已按同 cohort 灌入；图中心性、短板分位、招引培育所需链位，ODS 现在撑不住。
6. **Mapping 有语义错位**：股东被映射进 `enterprise_supply_chain`；`dwd_org_sc_info` 实际是证照/资质字段，不是供应关系。

---

## 2. DWD 工商/实体（21 张国内）

对照 `dwd-entity.md`。指标预聚合不进本表。

> **2026-09-02 补记**：新增国内表 `enterprise_shareholder`（源 `dwd_org_shareholder_info`，两库已建空表）。股东**不再**洗进 `enterprise_supply_chain`。清单真源改认 `dwd-entity.md`（现 23 项含 `patent_org_rel`）。下文仍是 2026-08-24 当时分类，不回溯改写。

| 目标表 | ODS 源（Mapping / 实际） | 三类 | 说明 |
|---|---|---|---|
| `enterprise_base` | `dwd_org_base_info`（4 万有效） | **A** | 主档字段可拆；`external_id`→信用代码 |
| `enterprise_extra` | 主档 + `dwd_org_org_product_info` + `dwd_org_stock_base` | **A** | 经营/上市补字段 |
| `enterprise_executive` | `dwd_org_executive_info`（4 万） | **A** | 直接映射 |
| `enterprise_news` | `dwd_org_important_news_info` | **A** | |
| `enterprise_finance_history` | `dwd_org_annual_financial_info` + 上市财务 | **A** | 单位/年度仍待 Mapping 冻结，表级 A |
| `enterprise_financing` | `dwd_org_financing_info` | **A** | |
| `enterprise_invest` | `dwd_org_invest_info` | **A** | 回连主档稀疏 → 当关联事实用是 B |
| `enterprise_parent_subsidiary` | `dwd_org_subsidiary_info` | **A** | |
| `enterprise_recruit` | `dwd_org_recruit_info` | **A** | |
| `enterprise_bid` | `dwd_bid_win_candidate_out` + `dwd_bid_base_out` | **A** | 代理/标的物 Mapping 明确不进企业域 |
| `enterprise_history_name` | `dwd_org_changerecord_info` 滤名称变更 | **A** | |
| `enterprise_tag` | 设计写 `dwd_org_tag_info`；ODS 实表 **`dwd_org_tech_tag`** | **B** | 别名未冻；有数但不能当已冻结源 |
| `enterprise_patent_detail` | `dwd_patent` 名称 JOIN 主档 | **B** | 专利表 A；企业对不上 |
| `enterprise_patent_history` | 专利按年 COUNT | — | 预聚合，本轮不评 |
| `enterprise_industry_chain` | 设计要 `dwd_org_industry_chain_dtl`；ODS **无此表** | **C** | 仅有链字典 + `dwd_org_industry_tags`（2 万行、**信用代码命中主档 6**）；无 `node_id` 明细 |
| `enterprise_industry_product` | `dwd_org_industry_product_tags` | **B** | 表在，**0 行** |
| `enterprise_supply_chain` | Mapping 用股东表充投资方；无供应关系源 | **C** | `dwd_org_sc_info` 是证照（company/credit/type/name/code），不是供应链 |
| `enterprise_cooperation` | Mapping 未列源 | **C** | ODS 无合作关系表 |
| `enterprise_innovation_carrier` | Mapping 未列源 | **C** | ODS 无载体表 |
| `enterprise_fund_project` | 金融 `dwd_fund_*` / 产业基金，非企业承担项目 | **C** | 对象不对，不能硬映射 |
| `enterprise_chain_patent` | 专利 × 链位 | **C** | 链位源缺失，无法上链 |

国外 6 张：

| 目标表 | ODS | 三类 |
|---|---|---|
| `enterprise_forg_base` / `_extra` | `dwd_forg_base_info` **0 行** | **B** |
| `enterprise_forg_executive` | `dwd_forg_executive_info` 0 | **B** |
| `enterprise_forg_invest` | `dwd_forg_shareholder_info` 0 | **B** |
| `enterprise_forg_finance_history` | `dwd_foreign_org_annual_financial_info` 有数 | **B** | 无主档，孤立财务 |
| `enterprise_forg_parent_subsidiary` | 承诺 `dwd_forg_subsidiary_info` / 实表 `dwd_agg_subsidiary_info` 0 | **B** |

高校/科研 ODS 有样例或有效行 0，**不在这 6 张企业国外实体表 Mapping 内**，不计入本轮 A。

港澳台 3 表 ODS 有数；Mapping **本期暂不映射**，目标 DWD 无对应 `enterprise_*` 表 → 不算项目 DWD 结构债，算范围外。

---

## 3. DWD 风险明细（非 `enterprise_risk_summary`）

`dwd-risk.md`：18 张主表 + 6 张 party。汇总长/宽表冲突仍在，**汇总表本轮不评**。

| ODS 有且有数（可直接映射起草） | 目标 |
|---|---|
| `dwd_org_company_abnormal` | `risk_abnormal` |
| `dwd_org_company_punish` | `risk_punishment` |
| `dwd_org_company_illegal` | `risk_illegal` |
| `dwd_org_risk_tax_punish` | `risk_tax_punish` |
| `dwd_org_opt_judicial_case` | `risk_judicial_case` |
| `dwd_org_risk_shixin` | `risk_dishonest` |
| `dwd_org_risk_zhixing` | `risk_executed` |
| `dwd_org_bankruptcy_public_cases` + `_list` | `risk_bankruptcy` + `_party` |

以上 **A（事件表）**。

设计有、本基线 ODS **未见对等表**（限高、诉讼、立案、开庭、公告、股权冻结/出质、终本、动产抵押、司法拍卖及对应 party）：**C**。  
不能用 9 类已到事件去填这 10 张空设计。

---

## 4. ADS 契约面（`ads.md`，非指标 ID）

ADS **禁止**从 ODS 直灌。评的是：以当前 ODS→DWD 原料，这张结果表**有没有计算输入**。

| ADS 表 | 依赖的非指标原料 | 三类 | 说明 |
|---|---|---|---|
| `enterprise_score` | 主档 + 财务 + 专利/标签 | **B** | 输入表多数存在；专利/标签回连不够，不能验收分 |
| `enterprise_ranking` | 同上 | **B** | 随评分 |
| `enterprise_diagnosis` | 企业指标 + **同行分位基准** | **C** | ODS/DWD 无行业 P25/P75 层 |
| `enterprise_centrality` | 供应/股权图 | **C** | 无真实供应边；股东当供应链是错映射 |
| `realdata_key_enterprise` | 主档 ± 标签规则 | **B** | 主档 A；标签别名/回连未闭合 |
| `realdata_enterprise_type_dist` | 主档 `org_type`/`tech_tag` | **B** | 类型枚举待冻；科技标签回连弱 |
| `realdata_enterprise_news_stat` | 资讯明细 | **A** | 可 COUNT；不是 8 件套 |
| `realdata_enterprise_risk` | 风险事件 | **B** | 事件 A；结果表与 ORM 宽表冲突，不能装 |
| `realdata_policy_metrics` | 政策主表有数 | **C** | 缺企业–政策稳定关系 |
| `realdata_chain_news_stat` | `dwd_industry_chain_news_info` | **A** | 链资讯可聚合；不解决企业上链 |
| `graph_node` / `graph_edge` | Nebula 旁路 | **C** | 不是 ODS 表 |

---

## 5. Mapping 已声明「暂不映射」且本轮保持

高校、科研机构、并购、港澳台、招标代理/标的物：ODS 部分有数，**项目 DWD 无承接表或明确范围外**。  
有数 ≠ 要进企业 DWD。并购若产品要事件表，属于 **C（目标缺表）**，需另开设计，不是 ODS 缺数。

---

## 6. 能不能 Mapping

| 动作 | 结论 |
|---|---|
| 国内 A 类实体/事件 **起草** Mapping | **可以**（与早上业务表结论一致） |
| 用产业标签灌 `enterprise_industry_chain` | **不可以**当正式链位；6/20000 回连，且无节点明细 |
| 用股东灌 `enterprise_supply_chain` | **不可以**当供应关系 |
| 国外 6 表正式灌数 | **不可以** |
| ADS 当 ODS 贴源 | **禁止** |
| 正式冻结 / 生产装数 | **仍先裁 C01/C02/C09/C10 等结构冲突** |

---

## 7. 相对早上那份结论多了什么

早上评的是 **供应方承诺表（三方也叫 dwd_*）** 自己能不能用。  
本文件评的是 **项目库表**（`enterprise_*` / `risk_*` / ADS）对 ODS 有没有落点。

多出来的缺口几乎都在「目标有表、源不对或没有」：

- 上链、供应、合作、载体、企业项目、链专利  
- 约 10 张司法扩展风险表  
- ADS 诊断/中心性/政策企业关系  

不是指标公式问题。
