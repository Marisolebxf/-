# 后加工 · 圈定与指标

列的落点在 `09`。这里只写谁进池、怎么分类、指标怎么计。  
**2026-11-04** round1 答复已落地（`GDF-SVC-WORKPACK-R1A-L01`）。

规则与 [`svc_rule_demo_kw_v1.md`](../../../../data-design/storage/SVC/seeds/svc_rule_demo_kw_v1.md) 相同，不改词。规则号 `svc_rule_demo_kw_v1.1`，2026-08-20 按规则 A 拍板，是项目临时词典。第 1 节的词是写圈定池之前就有的输入。第 2 节的指标在圈定池写下之后才算，结果进 ADS，不回写词表。`org_type` 不参与。不读高校表、科研院所表。

## 1. 谁进池

1. 行业、行业分层、行业代码、经营范围（`dwd_org_org_product_info.main_activities`）里有字时，满足任一即进池：一级行业等于「科学研究和技术服务业」；或一级行业含「金融」；或行业 / 经营范围命中下面的分类叶子；或命中「咨询」「广告」。
2. 这些文本都空：只看 `name_cn` 是否命中名称收紧词。光杆「投资」「咨询」「广告」「银行」「基金」「保险」不够进池。
3. ~~进池不足 10 家改为过滤后全部机构进池~~ **已取消（Q9）**。命中多少入多少；0 行则诚实空池，下游不写。
4. 分类从紧，顺序 `FINANCE`、`IP`、`HR`、`MKT`、`CONSULT`、`INNOV`，先命中先得。对不上就空，不补成某一类。一级行业是「科学研究和技术服务业」只说明可以进池，不能单凭这一句记成 `INNOV`。

有行业时：

| 类 | 行业侧子串 |
|----|------------|
| FINANCE | 一级行业含「金融」；或投资与资产、货币金融、资本市场、保险、证券、非金融机构支付 |
| IP | 知识产权 |
| HR | 人力资源、劳务派遣、职业中介 |
| MKT | 广告业、广告服务、会展、会议展览、市场调查、市场营销 |
| CONSULT | 管理咨询、规划咨询、商务咨询、科技咨询、社会经济咨询、咨询与调查 |
| INNOV | 检验检测、检测认证、质检、技术推广、研究和试验、科技推广、技术转移、孵化、中试、计量认证 |

行业串里只有裸「咨询」「广告」或「投资」：进池，候选为空。

没有行业文本时，名称词同时决定进池和分类：

| 类 | 名称子串 |
|----|----------|
| FINANCE | 科技金融、创业投资、风险投资、融资担保、知识产权质押、小额贷款、小贷、创投、风投 |
| IP | 知识产权、专利代理、商标代理、版权代理、知产 |
| HR | 人力资源、人才服务、劳务派遣、猎头、招聘 |
| MKT | 市场营销、市场推广、会展 |
| CONSULT | 管理咨询、规划咨询 |
| INNOV | 检验检测、检测认证、技术转移、研发服务、科技服务、孵化器、众创、中试、计量认证、综合科技 |

不用光杆「服务」。

## 2. 基础指标

人口是本批圈定机构。属性从 ODS 主表读。

| 标识 | 怎么算 |
|------|--------|
| A1 `M_SVC_INDUSTRY_LAYOUT` | **两维写进同一 `category` 列（维持现网，不加前缀）**：①六类候选各计一次（英文码 `FINANCE`…`INNOV`，空候选单独一档）；②另有 `industry` 时再按行业原文计，`industry` 空则用 `industry_l2_name`。两列都没有就只留六类档。`value` 是机构数。有 `org_size` 才写入 `ext`。不用国民经济代码当六类。读侧用六类枚举集合拆两维 |
| A2 `M_SVC_ORG_CNT` | 源上没有国家列。中文名是按国家计数，这里降成省。`geo_level` 写 `province`。`region_name` 用 `province`。空省不进分布，记到 `ext`。`org_count` 是圈定人口 |
| A3 `M_SVC_INVEST_Y` | 只用本批事件里 `event_date` 有值的行。`period` 是年份。`value` 是当年 `amount` 之和。金额空的不加入，也不当成 0，并在 `ext` 记下这条取舍。没有这样的行，序列就是 0 行。投资行没有业务日，不进这里 |
| A4 `M_SVC_NEW_CNT`、`M_SVC_ORG_NEW_COUNT` | 两条同一套按年计数，各写各的标识。`period` 先取 `incorporation_date` 的年，没有再取 `incorporation_year`。两个都空就跳过。`value` 是机构数 |
| A5 `M_SVC_SZ_SCALE` | `city` 为「深圳」或「深圳市」的机构数（存量截面）。`period` 固定 **`all`**；`slice_key` 固定 **`city`**（切片标签，不是城市名 / regionId）；`ext.filter=city` |
| A6 `M_SVC_SZ_DISTRICT` | 城市过滤同 A5。`geo_level` 为 `sz_district`。`region_name` 用主表 `area`。无 `area` 则该条 0 行，不从地址拆区县，不做 `district` 回退 |

下面这些标识点过名，没有可执行的算法。不写，也不补 0：

`M_SVC_ORG_TOTAL`、`M_SVC_PT_GLOBAL_TOTAL`、`M_SVC_PT_GLOBAL_TYPE_DIST`、`M_SVC_PT_REGION_ORG`、`M_SVC_PT_GLOBAL_SCALE_DIST`、`M_SVC_PT_SZ_TOTAL`、`M_SVC_SZ_COMPARE_METRIC`、`M_SVC_PT_SZ_TYPE_DIST`、`M_SVC_PT_SZ_REGION_ORG`。
