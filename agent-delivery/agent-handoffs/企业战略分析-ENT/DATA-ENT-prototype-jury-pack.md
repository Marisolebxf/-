# 企业分析原型需求确认 · 数据/算法陪审包

| 属性 | 内容 |
|------|------|
| 文档编号 | DATA-ENT-JURY-v1 |
| 版本 | v1.0.0 |
| 作者 | data-agent（供算法/数据工程师发起评审） |
| 日期 | 2026-06-19 |
| 评审范围 | **第一轮：分析层 E-20~E-30**（bid §1.1.1.2.4.2.3 共 10 子功能） |
| 原型真源 | `topic_demo` 分支 `feat/ent-elements-build`（见 `ENT-delivery-summary.md`） |
| 指标真源 | `metrics/cfg_metric-ENT-seed.yaml`（49 条 `M_ENT_*`） |
| 决策跟踪 | `客户决策清单跟踪表.md` §2.4（Q010~Q019） |

> **用途**：配合 PM + UE 组织甲方原型评审会；数据/算法工程师在会中讲解「页面数字能否落地、哪些是 Mock、哪些需甲方拍板」。  
> **不替代**：UE 的交互/视觉确认、PM 的范围守门、甲方的最终签字。

---

## 1. 发给 PM / UE / coordinator 的协作请求（可复制）

**收件人**：PM（主）、UE/UI lead（原型演示）  
**抄送**：coordinator-agent（登记 task-registry）

**主题**：ENT-REQ-CONFIRM-01 · 企业分析原型需求确认会（E-20~E-30）

**正文**：

> 算法/数据侧已整理「原型陪审包」（本文档），请求安排 **60~90 分钟** 甲方原型评审会，目标：
>
> 1. 确认分析层 9 页路由/功能范围是否与 bid 一致（E-20~E-30）
> 2. 对 Q010~Q019 共 10 项业务口径做甲方确认或书面认可临时默认
> 3. 每页给出「确认 / 待改 / 暂缓」三态，写入会议纪要
>
> **会前材料**：本文档 + `ENT-functional-design-v2.md` + demo2 原型链接  
> **会中角色**：UE 讲交互 · PM 记决策 · 数据/算法讲指标可行性  
> **会后产出**：更新 `客户决策清单跟踪表.md` + `agent-handoffs/ENT-req-confirm-{date}.md`

**建议登记 task-registry 条目**：

```yaml
- id: ENT-REQ-CONFIRM-01
  title: 企业分析原型需求确认（E-20~E-30）
  agent: pm
  collaborators: [ue-lead, data-lead, algorithm-lead]
  dependencies: [ENT-UX-v2, ENT-FE-as-built]
  dod:
    - 甲方纪要或书面确认 Q010~Q019
    - 客户决策清单跟踪表 §2.4 更新
    - 每页 E-XX 三态签字
  status: pending
```

---

## 2. 原型访问与演示路径

| 层级 | 路由 | E-XX | 演示要点 |
|------|------|------|----------|
| P0 概述 | `/enterprise/overview` | E-20 | KPI 卡片 + 趋势 + 下钻入口 |
| P1 类型 | `/enterprise/type-distribution` | E-21 | 7 类 type_dim × 区域地图 |
| P2 领域 | `/enterprise/domain-distribution` | E-22 | 产业链覆盖广/深 |
| P3 能力 | `/enterprise/capability` | E-23/E-24 | 技术力/商业力 Tab |
| P5 深圳 | `/enterprise/status-analysis` | E-25 | 深圳切片 + 城市对标 |
| P6 引育 | `/enterprise/recommendation` | E-26/E-27 | 招引/培育 Tab |
| P8 供应链 | `/enterprise/supply-chain` | E-28 | 关系图 + 风险 |
| P9 痛难点 | `/enterprise/pain-points` | E-29 | 四维诊断 |
| P10 竞争力 | `/enterprise/competitiveness` | E-30 | 综合得分 + 排名 |

> Wave 0 全部统计数字为 **Mock**（🧪 MockBadge）；评审重点是 **功能范围 + 口径 + 交互**，不是数值真实性。  
> 原型部署：demo2 沙箱（push 后约 2–3 min 生效）`https://skxrules.unicomcn.tech:30999/`；若分支未 push，请 UE 本地 `topic_demo` 演示。

---

## 3. 逐页陪审表（页面 → 指标 → 数据状态 → 必问问题）

**图例**：✅ ODS 可直接聚合 · 🔧 需算法/规则 · ⚠️ 口径待甲方 · ❌ 无数据源

### P0 · 企业分析概述（E-20）`/enterprise/overview`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方（1 句） |
|-----------|--------|----------|---------|------------------|
| M_ENT_TOTAL_COUNT | 企业总数 | ✅ | — | 统计对象是否=要素库全量有效企业？ |
| M_ENT_INNOVATIVE_COUNT | 创新型企业数 | ⚠️ | **Q011** | 「创新型企业」= 高企∪专精特新∪瞪羚∪独角兽 是否认可？ |
| M_ENT_NEW_COUNT_Y | 历年新增 | ✅ | — | 按 `registration_date` 逐年计数是否 OK？ |
| M_ENT_AVG_RD_INVESTMENT | 平均研发投入 | ✅ | — | 仅统计有研发数据的企业是否 OK？ |
| M_ENT_PATENT_TOTAL | 专利总量 | ✅ | — | 用 ODS 预聚合授权数求和是否 OK？ |
| M_ENT_HIGH_TECH_COUNT | 高企数量 | ⚠️ | **Q010** | 高企判定：资质标签解析规则是否认可？ |

**页面级确认**：驾驶舱 KPI 组合是否满足 bid「企业分析概述」？下钻到 P1/P2 的链路是否符合预期？

**临时默认（Q011）**：四类资质标签并集去重。

---

### P1 · 重点企业类型分析（E-21）`/enterprise/type-distribution`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_TYPE_MATCH_COUNT | 匹配企业总数 | ✅ | — | 产业+类型筛选逻辑是否符合业务？ |
| M_ENT_TYPE_COUNT | 各类型企业数 | ⚠️ | **Q010** | 7 类 type_dim 判定规则是否认可？ |
| M_ENT_TYPE_RATIO | 类型占比 | ✅ | 依赖 Q010 | — |
| M_ENT_REGIONAL_COUNT | 区域企业数 | ⚠️ | **Q012** | 区划下钻到**市**还是**区县**？ |
| M_ENT_REGIONAL_DENSITY | 区域密度 | 🔧 | **Q012** | 密度分母：面积 / GDP / 其他？ |
| M_ENT_AGGLOMERATION_INDEX | 集聚指数 | 🔧 | **Q012** | 集聚算法（区位熵/基尼）是否接受？ |

**type_dim 枚举（需确认）**：`foreign` / `high_tech` / `sme` / `listed` / `little_giant` / `gazelle` / `unicorn`

**临时默认（Q010）**：按 `is_foreign/is_high_tech/is_sme/is_listed` + 荣誉标签解析专精特新/瞪羚/独角兽。  
**临时默认（Q012）**：下钻到市级；密度分母暂用面积（待补维表）。

---

### P2 · 领域分布分析（E-22）`/enterprise/domain-distribution`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_DOMAIN_COVERAGE_COUNT | 覆盖领域数 | ✅ | — | 按产业链名称去重计数是否 OK？ |
| M_ENT_DOMAIN_COVERAGE_BREADTH | 覆盖广度 | 🔧 | **Q013** | 广度 = 覆盖数/领域全集，全集如何定义？ |
| M_ENT_DOMAIN_COVERAGE_DEPTH | 参与深度 | 🔧 | **Q013** | 深度是否用 chain_score + 产品/专利加权？ |
| M_ENT_DIVERSIFICATION_INDEX | 多元化指数 | 🔧 | **Q013** | 领域分布熵是否作为多元化指标？ |

**临时默认（Q013）**：全集取 `dwd_industry_chain_info`；深度 = chain_score + 产品/专利贡献加权。

---

### P3 · 能力评估（E-23 技术力 + E-24 商业力）`/enterprise/capability`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_TECH_POWER_SCORE | 技术力评分 | 🔧 | **Q014** | 指标库构成与权重（专利 25% 等）是否认可？ |
| M_ENT_BUSINESS_POWER_SCORE | 商业力评分 | 🔧 | **Q014** | 商业力指标库与权重是否认可？ |
| M_ENT_TECH_RANK | 技术力排名 | 🔧 | Q014 | — |
| M_ENT_PATENT_GRANT_COUNT | 专利授权数 | ✅ | — | — |
| M_ENT_RD_INVESTMENT_RATIO | 研发投入占比 | 🔧 | — | — |
| M_ENT_REVENUE_LATEST | 营收 | ✅ | — | — |
| M_ENT_REVENUE_GROWTH_RATE | 营收增长率 | 🔧 | — | — |
| M_ENT_PROFIT_MARGIN | 利润率 | 🔧 | — | — |
| M_ENT_MARKET_SHARE | 市场份额 | ❌ | **Q019** | **无 ODS 来源**：采购市调 / 页面降级 / 下架？ |

**页面级确认**：E-23/E-24 合并 Tab 承载是否接受？（叶子功能点不变，符合 ±10%）

**临时默认（Q014）**：沿用原型默认权重表（见 wireframe P3）。  
**临时默认（Q019）**：UI 标 ❌ 无来源，算法不实现，待采购决策。

---

### P5 · 深圳企业现状（E-25）`/enterprise/status-analysis`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_SZ_COUNT | 深圳企业数 | ✅ | — | `headquarters_city='深圳'` 筛选是否 OK？ |
| M_ENT_CITY_AVG_TECH_POWER | 城市平均技术力 | 🔧 | Q014 | — |
| M_ENT_CITY_DENSITY | 企业密度 | 🔧 | **Q016** | 对标城市默认集合是否认可？ |
| M_ENT_CHAIN_COMPLETENESS | 产业链完整度 | 🔧 | — | 覆盖环节/全链环节定义是否 OK？ |
| M_ENT_SZ_CHAIN_POSITION | 链中角色 | ✅ | — | 上/中/下游取自 ODS 是否 OK？ |
| M_ENT_KEY_NODE_COUNT | 重点环节企业数 | ✅ | — | — |

**临时默认（Q016）**：对标城市 = 北京 / 上海 / 苏州 / 广州。

---

### P6 · 招引/培育推荐（E-26/E-27）`/enterprise/recommendation`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_ATTRACTION_INDEX | 招引推荐指数 | 🔧 | **Q015** | 招引指数权重（产业/政策/生态）是否认可？ |
| M_ENT_CULTIVATION_INDEX | 培育推荐指数 | 🔧 | **Q015** | 培育指数权重（相关/政策/成长/创新）是否认可？ |
| M_ENT_GROWTH_POTENTIAL | 成长潜力 | 🔧 | Q015 | — |
| M_ENT_INDUSTRY_MATCH_SCORE | 产业匹配度 | 🔧 | Q015 | — |
| M_ENT_POLICY_MATCH_SCORE | 政策匹配度 | 🔧 | Q015 | 跨政策域引用是否接受？ |
| M_ENT_RECOMMEND_COUNT | 推荐企业数 | ✅ | Q015 | 推荐阈值如何定？ |

**临时默认（Q015）**：各维度等权；阈值待算法 lead 建议 + 甲方确认。

---

### P8 · 供应链关系（E-28）`/enterprise/supply-chain`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_SUPPLIER_COUNT | 供应商数量 | ✅ | — | 上游关系计数口径是否 OK？ |
| M_ENT_CORE_SUPPLIER_COUNT | 核心供应商数 | 🔧 | **Q017** | 核心供应商 chain_score 阈值？ |
| M_ENT_NODE_CENTRALITY | 节点中心性 | 🔧 | Q017 | NebulaGraph 中心性算法是否接受？ |
| M_ENT_SUPPLY_CHAIN_RISK | 断链风险等级 | 🔧 | **Q017** | 高/中/低评级规则是否认可？ |
| M_ENT_RELATION_STRENGTH | 关系强度 | 🔧 | Q017 | — |

**临时默认（Q017）**：核心供应商 = chain_score ≥ P75；风险 = 网络脆弱性 + 风险表综合。

---

### P9 · 痛难点分析（E-29）`/enterprise/pain-points`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_PAINPOINT_COUNT | 痛难点总数 | 🔧 | **Q018** | 诊断维度：技术/市场/融资/管理 四维是否 OK？ |
| M_ENT_PAINPOINT_SEVERITY | 严重度 | 🔧 | Q018 | 各维度阈值如何定？ |
| M_ENT_PAINPOINT_GAP | 与行业最佳差距 | 🔧 | Q018 | 行业基准来源？ |

**临时默认（Q018）**：四维诊断 + 团队阈值占位；依赖后续专家知识库。

---

### P10 · 竞争力分析（E-30）`/enterprise/competitiveness`

| metric_id | 中文名 | 数据状态 | 决策 ID | 必问甲方 |
|-----------|--------|----------|---------|----------|
| M_ENT_COMPETITIVENESS_SCORE | 综合竞争力 | 🔧 | **Q014** | W1×技术力 + W2×商业力，W1/W2 取值？ |
| M_ENT_COMPETITIVENESS_RANK | 竞争力排名 | 🔧 | Q014 | — |
| M_ENT_SHORTBOARD_COUNT | 短板维度数 | 🔧 | Q014 | 低于行业基准的维度如何定义？ |
| M_ENT_INNOVATION_INDEX | 创新能力指数 | 🔧 | Q014 | 创新指数指标库是否认可？ |

---

## 4. 决策项速查表（Q010~Q019 · 评审会必过）

| ID | 标题 | 影响页面 | 团队临时默认 | 评审结论（现场填） |
|----|------|----------|--------------|-------------------|
| Q010 | 企业类型判定规则 | E-20/E-21 | 标签解析 is_* 字段 | ☐ 确认默认 ☐ 修改：____ ☐ 暂缓 |
| Q011 | 创新型企业口径 | E-20 | 四类资质并集 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q012 | 区划精度 + 密度分母 | E-21 | 到市级；密度/面积 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q013 | 领域广/深口径 | E-22 | chain_score 加权 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q014 | 评分权重体系 | E-23/24/30 | 原型默认权重 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q015 | 招引/培育权重阈值 | E-26/27 | 等权 + 阈值待定 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q016 | 对标城市集合 | E-25 | 北上苏广 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q017 | 供应链核心/风险规则 | E-28 | P75 + 综合评级 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q018 | 痛难点维度阈值 | E-29 | 四维 + 占位阈值 | ☐ 确认 ☐ 修改 ☐ 暂缓 |
| Q019 | 市场份额无来源 | E-24 | 不实现 + UI 标注 | ☐ 采购 ☐ 降级 ☐ 下架 |

> 甲方未当场拍板时：PM 可按 playbook §4 发送「T+3 工作日未回复视为认可临时默认」函。

---

## 5. 指标数据可行性汇总（49 条）

| 状态 | 数量 | 含义 | 评审策略 |
|------|------|------|----------|
| ✅ | 14 | ODS 可直接聚合 | 快速过，确认口径即可 |
| 🔧 | 30 | 需算法/规则 | 确认是否接受算法方案方向 |
| ⚠️ | 4 | 口径待甲方 | **必须 Q010/Q011/Q012 + TYPE_COUNT** |
| ❌ | 1 | 无来源 | **必须 Q019 决策** |

**数据工程师会后动作**（🟢 确认后）：
- 更新 `cfg_metric-ENT-seed.yaml` definition/formula
- 补登 `data-source-mapping-registry.yaml`
- 调整 ETL 中 `enterprise_code` 去重（统一业务主键）

**算法工程师会后动作**（🟢 确认后）：
- 更新 `ALGO-ENT-formula.md` 权重/阈值
- 实现 `conf/cfg_metric_params.yaml` 参数化
- Q019 若下架则从 capability 页移除 `M_ENT_MARKET_SHARE`

---

## 6. 建议议程（90 分钟）

| 时段 | 内容 | 负责人 |
|------|------|--------|
| 0–10 min | 范围说明：E-20~E-30 + Mock 标注 | PM |
| 10–25 min | P0/P1/P2 演示 + Q010/Q011/Q012/Q013 | UE + 数据 |
| 25–40 min | P3/P5 演示 + Q014/Q016/Q019 | UE + 算法 |
| 40–55 min | P6/P8 演示 + Q015/Q017 | UE + 算法 |
| 55–70 min | P9/P10 演示 + Q018/Q014 | UE + 算法 |
| 70–85 min | 决策项逐条确认（§4 表格） | PM |
| 85–90 min | 页面三态签字 + 后续计划 | PM |

---

## 7. 页面签收表（PM 现场填写）

| E-XX | 路由 | 功能范围 | 交互/视觉 | 数据口径 | 综合结论 |
|------|------|----------|-----------|----------|----------|
| E-20 | /enterprise/overview | ☐确认 ☐待改 ☐暂缓 | ☐ | ☐ | |
| E-21 | /enterprise/type-distribution | ☐ | ☐ | ☐ | |
| E-22 | /enterprise/domain-distribution | ☐ | ☐ | ☐ | |
| E-23/24 | /enterprise/capability | ☐ | ☐ | ☐ | |
| E-25 | /enterprise/status-analysis | ☐ | ☐ | ☐ | |
| E-26/27 | /enterprise/recommendation | ☐ | ☐ | ☐ | |
| E-28 | /enterprise/supply-chain | ☐ | ☐ | ☐ | |
| E-29 | /enterprise/pain-points | ☐ | ☐ | ☐ | |
| E-30 | /enterprise/competitiveness | ☐ | ☐ | ☐ | |

**甲方签字/纪要链接**：________________  
**会议日期**：________________

---

## 8. 第二轮预告（可选，不在本次会议范围）

门户层 E-31~E-35（`/development/*`）+ 明星企业 CMS（E-37，**Q020** 待登记）建议单独安排第二轮，避免首轮过载。

---

## 9. 引用文档

| 文档 | 路径 |
|------|------|
| 交付总册 | `agent-handoffs/企业战略分析-ENT/ENT-delivery-summary.md` |
| 功能设计 FDS | `topic_demo/docs/ia/enterprise/ENT-functional-design-v2.md` |
| Wireframe | `topic_demo/docs/ia/enterprise/ENT-wireframe.md` |
| 企业域 DB 设计 | `data/企业域数据库设计(v1).md` |
| ODS→DWD 映射 | `data/企业相关-ODS到DWD字段映射分析报告(v2).md` |
| 指标种子 | `metrics/cfg_metric-ENT-seed.yaml` |
| 决策跟踪 | `客户决策清单跟踪表.md` §2.4 |
| 验收台账 | `acceptance-catalog/catalog-topic-enterprise.yaml` |

---

**维护**：评审会后由 PM 归档纪要；data/algorithm 按 🟢 项更新 cfg_metric 与 formula handoff。
