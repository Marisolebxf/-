# TS 聚合方案 · 产业铺底（科技全域态势 · M1 数据聚合落库方案）

- **来源**：`agent-delivery/工程过程/02-策划与监控/02-智树工作计划/02-进度/05-展示系统集成工作计划.md` §1「科技发展态势」→ 子目标 1-科技全域态势 → 工作明细第 1 行「**聚合方案：产业铺底，按区域、时间聚合各科创要素（排除政策）**」
- **负责人**：`human:李伟` · **截止**：2026-10-15
- **状态**：草案（§2 源与责任人未落实，对应计划表「对端」栏为空）
- **关联**：
  - 下游接口契约 → `agent-delivery/agent-handoffs/科技发展态势-TS/API-TS-M1.md`（本方案定义"数据怎么生"，契约定义"接口怎么取"）
  - 上游规划 → `agent-delivery/agent-handoffs/科技发展态势-TS/TS-模块开发规划与任务拆分.md` §4 M1 / §5 `BE-TS-S02`
  - ADS 命名与读写铁律参照 → `agent-delivery/data/data-design/产业链/产业链-ADS表设计-原型与Handoff驱动(v2).md` §1/§3
  - 架构铁律 → `agent-delivery/architecture-baseline.md` §2 D3（只读 ADS）/ D4（`app_user` 家族可写）/ D7（Mock 先行，Python 写 ADS）
- **口径真源**：`repos/demo-ui-science/src/data.js`（`factorItems` L250 / `sharedMapRegions` L335）、`src/mapObjectDetail.js` L3–L24（11 要素与对象类型字典）

> ⚠️ 本方案只定义**聚合口径与落库骨架**，不含 SQL/ETL 实现；实际写数归 Python / 数据侧（D7）。§2 中凡标「**待定**」者，均为计划表未填对端人，**不编造责任人**。

---

## 1. 产业铺底骨架

### 1.1 三面读模型（先于表清单）

```text
┌─────────────────────────── 前端（M1 科技全域态势）──────────────────────────┐
│  图层统计 KPI ｜ 地图落点/热力 ｜ 对象详情 L6 ｜ 科创事件时间轴 ｜ 实时监控卡   │
└───────────────┬──────────────────────────────────┬────────────────────────┘
                │                                  │
                ▼                                  ▼
        Java 展示聚合层                          算法结果（带 metric_id，D9）
        /display/v1/** 只读 ADS                  Python 写 ADS，Java 只读
                │
                ▼
        ┌─────────────────────────────────────────────────────┐
        │  ADS 标准表 · 库 `gkxlumenx_ads`（demo `demo_gkxlumenx_ads`）
        │  ┌── 产业铺底底表（骨架，本方案新增）──────────────┐
        │  │   产业 × 区域 × 时间 三层键                     │
        │  └───────────────────┬────────────────────────────┘
        │                      ▼  各科创要素按同键挂靠
        │   要素统计 / 对象落点 / 对象指标 / 事件 / 舆情（§4）
        └─────────────────────────────────────────────────────┘
```

**"产业铺底"的定义**：以**产业维度**作为全域态势的底层骨架（业务键复用产业链域现成的 `industry_id` / `chain_id` / `node_id`，INB 原文），把 11 类科创要素按同一套 `(产业, 区域, 时间)` 键聚合挂靠到骨架上；**政策不在聚合范围**（政策归科技政策跟踪模块，负责人 `human:淮政玮`）。

### 1.2 骨架三维

| 维 | 取值 | 真源 |
|---|---|---|
| **产业** | `industry_id` / `chain_id` / `node_id`（产业链域 INB 业务键，直接复用） | 产业链 DWD v5 / Q053 |
| **区域** | 全球 / 湾区（11 城）/ 深圳（福田·光明·坪山三区）三级 | demo `sharedMapRegions` L335 + `data.js` L346；计划 §1「全球、湾区、深圳三个层级」 |
| **时间** | **日 / 周 / 月 / 季 / 年** 五档（与页面筛选同枚举） | demo `App.jsx` L399–L405 `eventTimeGranularityOptions`（逐字：day 日 / week 周 / month 月 / quarter 季 / year 年） |

### 1.3 底表建议

| 表 | 说明 | 备注 |
|---|---|---|
| `tech_situation_industry_base` | 产业铺底底表：`industry_id, chain_id, node_id, region_key, year, quarter, month` + 该骨架下要素计数汇总 | 表名前缀**待数据侧定名**（§5 U3；本稿沿用 `API-TS-M1.md` §9.1 的 `ts_`/`tech_situation_` 家族风格，不另起一套） |

公共列与命名（照搬产业链 v2 §3，保持全库一致）：不加 `ads_` 前缀；物理主键 `id BIGINT AUTO_INCREMENT`；公共列 `calc_batch_id` / `data_version` / `is_deleted` / `created_time` / `updated_time`；模型派生行可回链 `run_id` / `result_id` / `metric_id` / `metric_version`。

---

## 2. 要素源缺口排查表

> 用途：**拿去催对端责任人**。计划表「对端」栏为空的行，来源与责任人均未落实，逐项标「待定」。

| # | 要素 | 计划表对应行 | 源在哪 | 谁提供 | 是否已知 | 落表建议（§4） | 风险 |
|---|---|---|---|---|---|---|---|
| 1 | 企业 | 「企业、服务机构聚合」（截止**未填**，指标「待填写」） | **自有**（我方库 / 产业链域企业资产） | **我方：`human:李伟`** | **是** | `ts_object` | 仅截止时间未填 |
| 2 | 服务机构 | 同上 | **自有**（我方库） | **我方：`human:李伟`** | **是** | `ts_object` | 截止时间未填；与产业链 `M_SVC_*` 的复用关系待定 |
| 3 | 专家学者（人才） | 「人才（专家学者）、科研机构、论文、专利」截止 **2026-10-31** | 久新提供相关 SQL 或算法，智谱按此从 ADS 读分析结果 | **久新-？**（计划表原文即写问号） | 否 | `ts_object` / `ts_object_metric` | **对端责任人未落人**（最紧的阻塞） |
| 4 | 科研机构 | 同上 | 同上 | **久新-？** | 否 | `ts_object` | 同上 |
| 5 | 论文 | 同上 | 同上 | **久新-？** | 否 | `ts_factor_stat` | 同上 |
| 6 | 专利 | 同上 | 同上 | **久新-？** | 否 | `ts_factor_stat` | 同上 |
| 7 | 会议（顶会） | 「顶会聚合」（截止**未填**） | **待定** | **待定** | 否 | `ts_factor_stat` | 无时间无责任人 |
| 8 | 项目 | 「项目聚合」（截止**未填**） | **待定** | **待定** | 否 | `ts_factor_stat` | 无时间无责任人 |
| 9 | 成果 | 「成果聚合」（截止**未填**） | **待定** | **待定** | 否 | `ts_factor_stat` | 无时间无责任人 |
| 10 | 课题 | **计划表未列此行** | **待定** | **待定** | 否 | `ts_factor_stat` | ⚠️ **覆盖缺口**：demo 11 要素含"课题"，计划 6 行聚合未点名 |
| 11 | 期刊 | **计划表未列此行** | **待定** | **待定** | 否 | `ts_factor_stat` | ⚠️ **覆盖缺口**：同上 |
| — | 事件（科创事件） | 「事件聚合」（截止**未填**） | 三方库导入（D3），数据工厂映射走 ADS | `DATA-TS-S01`（归属由 `human:徐腾强` 定） | 否 | `ts_event` / `ts_opinion` | 三方源上线时点未定 |
| — | **政策** | — | **排除**（不聚合） | — | — | — | 政策归科技政策跟踪，负责人 `human:淮政玮` |

**排查结论（3 类缺口）**

1. **责任人缺口**：12 行要素相关中，**2 行已落实**（企业、服务机构 = 我方自有，责任人 `human:李伟`）；其余 **10 行**「谁提供」仍待定——人才/科研机构/论文/专利组原文写的就是 `久新-？`（连名字都没落），顶会/项目/成果/课题/期刊 5 行 + 事件 1 行则无责任人。
2. **时间缺口**：除人才组（10-31）外，5 组聚合的截止时间为空。
3. **覆盖缺口**：demo 11 要素里的 **课题、期刊** 在计划表 6 行聚合中未被点名——要么并入"论文/项目"组，要么补行，**须在催办时一并确认**。

---

## 3. 要素聚合口径矩阵

> 每个要素回答三问：**源 → 聚合键 → 落表**。源未落实处留空（不编）。

| 要素 | 聚合键 | 时间粒度 | 落表 | 对接口（`API-TS-M1.md`） |
|---|---|---|---|---|
| 企业 / 园区 / 机构 / 高校实验室 / 学者 / 服务机构 | `object_id × region_key` | 快照 + 年 | `ts_object` | §3.2 地域与对象落点 |
| 论文 / 专利 / 期刊 / 课题 / 项目 / 成果 / 会议 | `factor_key × region_key × bucket` | 日/周/月/季/年 预聚合 | `ts_factor_stat` | §3.1 要素图层与统计 / §3.3 检索 |
| 对象指标（创新指数 / 论文数 / 专利数 / 转化金额） | `object_id × metric_key × year` | 年 | `ts_object_metric` | §3.4 详情 metrics / trend |
| 科创事件 | `event_id × date × （聚合到）region_key` | 日/周/月/季/年 五档 | `ts_event` | §3.5 事件列表与详情 |
| 舆情明细（供事件聚合） | `opinion_id × event_id` | 日 | `ts_opinion` | §3.5 聚合 |
| 实时监控三口径（数量 / 占比 / 增长） | `factor_key × time_window` | 滚动窗口 | 由 `ts_factor_stat` 派生 | §3.6 实时监控（D2 轮询） |

**聚合语义（三层一致，禁前端自算正式值）**

- 计数口径：`要素 key × region_key × time` 的**去重计数**；占比 = 该要素在本 region 内占比；增长 = 相邻时间窗环比。
- 正式值只读已发布 ADS；前端**禁**自算正式占比/增长（对齐产业链 v2 §1 铁律），演示口径必须带 🧪 MockBadge。
- 排除政策要素；排除 demo `data.js` 的演示硬编码（`factorItems.count`、`sharedMapRegions.detail` 按 `rank` 线性推导）——**禁直接灌库**，须由 Python 按标准表写 Mock。

---

## 4. ADS 落库表清单

复用 `API-TS-M1.md` §9.1 已出的 5 域建议清单，本方案**只加产业铺底底表**，不另起表名体系：

| # | 域 | 表 | 关键字段 | 消费接口 | D3 就绪度 |
|---|---|---|---|---|---|
| — | **产业铺底（本方案新增）** | `tech_situation_industry_base` | `industry_id, chain_id, node_id, region_key, year, quarter, month` | 全部（骨架） | 项目内结构 |
| 1 | 科创要素 | `ts_factor_stat` | `factor_key, region_scope, year, cnt, source_code` | §3.1 / §3.3 | 部分待映射 |
| 2 | 载体/对象 | `ts_object` | `object_id, object_type, name, lng, lat, region_key, factor_key, heat_level, warning_level` | §3.2 / §3.4 | 项目内结构 |
| 3 | 指标 | `ts_object_metric` | `object_id, metric_key, metric_id, year, value, unit` | §3.4 metrics / trend | 对齐 `/metrics/v1/catalog` |
| 4 | 事件 | `ts_event` | `event_id, date, time_granularity, event_type, importance_level, title, text, lng, lat, source_name, original_url` | §3.5 | **D3 三方源映射待定** |
| 5 | 舆情 | `ts_opinion` | `opinion_id, event_id, source, publish_at, influence, sentiment, url` | §3.5 聚合 | **D3 待定** |

**读写与发布**：写方 = Python / 指标引擎（D7）；Java 只读已发布批次（D3）；库 `gkxlumenx_ads`（demo `demo_gkxlumenx_ads`）；Mock 先行走 Python 按本清单写数，**禁 Java / 前端造数**。

---

## 5. 待定与责任人

| # | 待定 | 归属 | 动作 |
|---|---|---|---|
| P0 | 企业 / 服务机构**自有源定表**（§2 已落实为我方负责） | `human:李伟` | 定"自有"取自哪套资产，回填 §3/§4 —— **不依赖任何对端，可立即推进**。候选：企业 → E1 域（`gkxlumen-topic-enterprise` + `demo-algo-ent-analysis`，`system-wbs.yaml` 已挂 display_pages「1.1 科技全域态势-企业图层」）；机构 → E3 域（`gkxlumen-topic-org`，Python 待建）。⚠️ 服务机构域 Owner 为 `human:侯佳伟`（`02-进度.md`），"我方负责"与此若不一致，须先对齐 |
| P1 | 其余 10 行要素源与责任人（§2） | **待落实** | 李伟催办：久新侧对接人（人才/机构/论文/专利）+ 顶会/项目/成果 3 组 + 事件（`DATA-TS-S01`） |
| P2 | 课题 / 期刊是否补行（§2 覆盖缺口） | `human:李伟` × `human:徐腾强` | 催办时一并定 |
| P3 | 产业铺底底表定名与字段（`tech_situation_industry_base`） | 数据侧 | 与 `API-TS-M1.md` U3 同步定稿 |
| P4 | 区域三级清单与深圳三区是否扩展 | `human:孔东`（前端口径） | 对齐 `API-TS-M1.md` U8 |
| P5 | 事件/舆情三方源上线时点 | `DATA-TS-S01` | 随三方库 |
| P6 | 本方案需否并入 `BE-TS-S02`（ADS 标准表落库） | `human:徐腾强` | M0 评审一并定 |

---

## 6. 下一步

1. **今天**：两条并行——① **P0 立即做**：企业 / 服务机构是我方自有，先把这两类的"源表 → 聚合键 → 落表"在 §3/§4 落定，**不等任何对端**；② 拿 §2 排查表催办 P1/P2（其余 10 行源未落人，不定则方案只能停在草案）。
2. 责任人落实后：回填 §2/§3，把 §1.3 + §4 表清单交数据侧出 DDL（转 `BE-TS-S02`）。
3. M0 评审时与 `API-TS-M1.md` 一并过：本方案 U3/U4/U6/U8 与契约同项合并裁决，**不另立一套未决项**。
