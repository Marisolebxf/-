# ALGO-POLICY-fullset —— 政策算法全集实现 + 实跑证据

> 任务：POLICY-PROTO-L04（Epic: E-POLICY-PROTOTYPE）｜ 角色：algorithm-agent ｜ 日期：2026-06-23
> 仓：`demo-algo-ent-analysis`（POC，可直推 main）｜ 产物：自包含包 `polan/`（未触碰企业 `entan/`）
> 上游真源：`data/政策域数据库设计(v1).md` + `metrics/cfg_metric-POLICY-seed.yaml`
> 验收核心：**政策算法全集逐个实际跑通并产出 ADS** —— 已在本地 SQLite 后端真实执行（见 §3）。

---

## 1. 范围与实现（与算法全集逐条对照）

### 1.1 polan 包结构

```
polan/
├── __init__.py
├── common/{__init__,config,db,nebula}.py     # PG/SQLite 双后端，本地零依赖可跑
├── mockgen/generate.py                       # dwd.policy_base_info Mock（seed=42）
├── basic/indicators.py                       # 5 类基础指标
├── graph/{entity,nebula_loader}.py           # NER + RE + Nebula(gkx_policy) 灌入
├── eval/{_util,focus,intensity,effect,gap,opportunity,layout}.py   # 6 深度模型
├── text/{parse,match,simulate}.py            # 文本解析/匹配推送/效果推演
└── models/registry.py                        # 政策模型注册（element=POLICY）
scripts/{schema_policy_ads.sql, run_all_policy.py, verify_policy.py}
conf/{settings_policy.yaml, cfg_model_registry.yaml(11 POLICY 模型)}
api/policy_routes.py（/v1/policy/**，已 include 进 api/main.py）
docs/{政策算法demo详细设计文档.md, 政策实体识别构建过程.md}
```

### 1.2 算法全集实现对照

| 类别 | 要求 | 实现 | 产出表 | 实跑行数 |
|------|------|------|--------|----------|
| 基础指标①级别分布 | ✅ | basic/indicators.py | ads_policy_level_dist | 6 |
| 基础指标②类型分布 | ✅ | 同上（QPOL-01 临时 ext1） | ads_policy_type_dist | 5 |
| 基础指标③时序(量+增长+连续性) | ✅ | 同上（环比/连续性已实现） | ads_policy_timeseries | 9 |
| 基础指标④全国分布(按省) | ✅ | 同上 | ads_policy_national_dist | 31 |
| 基础指标⑤深圳分布(按区) | ✅ | 同上 | ads_policy_sz_dist | 9 |
| 实体图谱 NER | ✅ | graph/entity.py | ads_policy_entity | 7517 |
| 实体图谱 RE（4 边） | ✅ | graph/entity.py | policy_graph_node/edge | 806 / 3726 |
| 图谱灌入 Nebula(gkx_policy) | ✅(兜底) | graph/nebula_loader.py | space gkx_policy（本地跳过，镜像兜底） | — |
| 深度①焦点识别 | ✅ | eval/focus.py | ads_policy_focus(policy 行) | 600 |
| 深度②力度评估 | ✅ | eval/intensity.py | ads_policy_intensity + metric_timeseries | 631 / 62 |
| 深度③效果评估 | ✅ | eval/effect.py | ads_policy_effect(region_effect) | 31 |
| 深度④短板识别 | ✅ | eval/gap.py | ads_policy_effect(region_gap) | 31 |
| 深度⑤机遇识别 | ✅ | eval/opportunity.py | ads_policy_focus(region 行) | 31 |
| 深度⑥布局推荐 | ✅ | eval/layout.py | ads_policy_effect(region_layout) | 31 |
| 文本①解析 | ✅ | text/parse.py | ads_policy_text_parse | 600 |
| 文本②匹配推送 | ✅ | text/match.py | ads_policy_match | 144 |
| 文本③效果推演仿真 | ✅ | text/simulate.py | ads_policy_simulate | 36 |
| 模型注册 | ✅ | models/registry.py | gkx_cfg.cfg_model_registry | 13(含 11 POLICY) |

> 说明：`ads_policy_focus`=631（600 政策焦点行 + 31 区域机遇行）；`ads_policy_intensity`=631（600 政策力度 + 31 省级）；
> `ads_policy_effect`=93（31 效果 + 31 短板 + 31 布局）；`ads_policy_metric_timeseries`=93（三维 + 落地实效）。

---

## 2. cfg_metric 🔧 项 formula 实现对照

| metric_id | seed 状态 | polan 实现 formula | 文件 |
|-----------|-----------|--------------------|------|
| M_POLICY_TIMESERIES | 🔧 | 发布量=按年 COUNT；环比=(本期-上期)/上期×100；连续性=连续非空期/总期×100 | basic/indicators.py |
| M_POLICY_VALIDITY_RATE | 🔧 | COUNT(status=1 AND (expire 空 或 >=today))/COUNT(*)×100 | basic/indicators.py |
| M_POLICY_INDUSTRY_COVERAGE | 🔧 | DISTINCT 覆盖产业/全产业×100（省级） | eval/intensity.py |
| M_POLICY_RELATION_DEGREE | 🔧 | gkx_policy 加权度中心性（support/apply_to/regulate/cite 边权和）归一 | graph + eval/focus.py |
| M_POLICY_FOCUS_INDEX | 🔧 | 加权(关键词热度,要素完整度,层级)（权重 QPOL-02 待甲方，临时 0.4/0.35/0.25） | eval/focus.py |
| M_POLICY_INTENSITY_SCORE | 🔧 | 加权(效果,覆盖,成本)三维 | eval/intensity.py |
| M_POLICY_EFFECT_SCORE | 🔧 | 加权(执行效果实算, 社会经济⚠️待采购, 环境⚠️待采购) | eval/effect.py |
| M_POLICY_SHORTBOARD_COUNT | 🔧 | COUNT(覆盖盲区 + 失效超阈 + 力度不足) | eval/gap.py |
| M_POLICY_OPPORTUNITY_COUNT | 🔧 | COUNT(均值(关注度,影响力,稳定性)≥阈值) 按省 | eval/opportunity.py |
| M_POLICY_LAYOUT_REC_COUNT | 🔧 | COUNT(融合机遇+短板优先级≥阈值) | eval/layout.py |
| M_POLICY_INDUSTRY_FIT | 🔧 | 覆盖产业/全产业相似度（QPOL-03 临时） | eval/intensity.py |
| M_POLICY_INTENSITY_INDEX | ⚠️ | 省级=单政策力度均值×数量因子（QPOL-02 待甲方） | eval/intensity.py |
| M_POLICY_SUPPORT_STRENGTH | ⚠️ | 加权(扶持档位,层级,数量) → metric_timeseries | eval/intensity.py |
| M_POLICY_TYPE_DIST | ⚠️ | QPOL-01 临时取 ext1(topic_type) 归类 | basic/indicators.py |
| M_POLICY_IMPLEMENTATION_EFFECT | 🔧 | 执行率+受益+反馈代理（⚠️待采购） → metric_timeseries | eval/effect.py |
| M_POLICY_LEVEL_DIST / _TOTAL_COUNT / _NATIONAL_DIST / _SZ_DIST | ✅ | 直接聚合 | basic/indicators.py |

> 全部 19 条 M_POLICY_* 均有产出落点（4 条 ✅ 直接聚合、12 条 🔧 已实现 formula、3 条 ⚠️ 临时默认口径并标注 pending）。

---

## 3. 实跑证据

### 3.1 run_all_policy 日志摘录（SQLite 后端，PYTHONIOENCODING=utf-8）

```
===== polan 政策算法全流水线启动（DB 后端=sqlite） =====
[Schema 初始化]            0.01s
[模型注册 seed]            seeded=13
[Mock 贴源] 政策=600 层级分布={国际:27, 市级:266, 省级:137, 国家级:56, 区县级:114}
[A 基础指标] A1级别=6(总政策=600,全局时效=80.83%) A2类型=5 A3时序=9 A4全国=31省 A5深圳=9区
[B NER/RE]  NER 实体=7517 图节点=806 图边=3726 边类型={support:1894, apply_to:834, regulate:600, cite:398}
[B+ Nebula]  未启用，跳过；图谱已在 PG/SQLite 镜像可用
[C1 焦点]    600 条（Top focus=97.82 rel=1.58）
[C2 力度]    单政策=600 省级=31 三维=62（力度榜首 广东省 idx=115.0 覆盖=100%）
[C3 效果]    31 区域（社会/环境维度待采购 Mock 代理）
[C4 短板]    31 区域，短板合计=40 项
[C5 机遇]    31 区域，机遇政策合计=541 条（阈值≥60）
[C6 布局]    31 区域，布局建议合计=68 条（优先级≥55）
[D1 文本解析] 600 条
[D2 匹配推送] 主体=18 匹配记录=144（每主体 Top≤8）
[D3 效果推演] 36 条（12 省 × 3 情景）
===== 全流水线完成，总耗时 1.0s =====
```

> 完整日志：`demo-algo-ent-analysis/data/run_all_policy.log`、校验：`data/verify_policy.log`。
> **幂等验证**：连续两次运行各 ADS 表行数完全一致（truncate + 批量 insert）。

### 3.2 各 ADS 表行数（verify_policy.py）

| 表 | 行数 | 表 | 行数 |
|----|------|----|------|
| dwd.policy_base_info | 600 | ads_policy_focus | 631 |
| ads_policy_level_dist | 6 | ads_policy_intensity | 631 |
| ads_policy_type_dist | 5 | ads_policy_effect | 93 |
| ads_policy_timeseries | 9 | ads_policy_metric_timeseries | 93 |
| ads_policy_national_dist | 31 | ads_policy_entity | 7517 |
| ads_policy_sz_dist | 9 | policy_graph_node / edge | 806 / 3726 |
| ads_policy_text_parse | 600 | ads_policy_match | 144 |
| ads_policy_simulate | 36 | cfg_model_registry | 13 |

### 3.3 关键样例

- **级别分布**：国家级 9.33% / 省级 22.83% / 市级 44.33% / 区县级 19% / 国际 4.5%（金字塔合理）；全局时效 80.83%。
- **时序**：2022→2023 增长 67.24%，近年陡增（2026=139）；连续性 100%。
- **全国 Top5**：广东 75 / 江苏 55 / 北京 55 / 浙江 41 / 上海 40。
- **力度榜**：广东 idx=115.0、江苏 103.16、北京 86.13（产业覆盖 100%）。
- **布局推荐样例**（新疆，5 条）：`{补短板, 新材料, 优先级69.5, "新材料产业政策覆盖缺失，建议出台专项扶持政策"}` 等。
- **效果推演**：广东「扶持力度+40%」基线 115.0 → 推演 140.3（+22%）。
- **匹配推送**（华芯生物 Top3）：高端装备相关政策 match_score=75.0。

### 3.4 API 实跑（standalone TestClient）

```
GET /internal/policy/models/registry  → count=11 source=db
GET /v1/policy/metrics                 → headline{total=600, validity=80.83, provinces=31, nodes=806, edges=3726}
GET /v1/policy/indicators              → keys=[level,type,timeseries,national,sz]
GET /v1/policy/analysis/intensity      → count=3
GET /v1/policy/graph?center=POL202500010 → source=sqlite, 子图返回
GET /v1/policy/simulate?scope_code=440000 → 3 条
```

---

## 4. 产物清单

- 代码：`polan/`（17 模块）、`api/policy_routes.py`、`scripts/{run_all_policy,verify_policy}.py`
- DDL：`scripts/schema_policy_ads.sql`（PG 方言，对齐 DB 设计）
- 配置：`conf/settings_policy.yaml`、`conf/cfg_model_registry.yaml`（11 POLICY 模型，替换原 3 个 E7 占位）
- 文档：`docs/政策算法demo详细设计文档.md`、`docs/政策实体识别构建过程.md`
- 日志：`data/run_all_policy.log`、`data/verify_policy.log`
- 本 handoff

---

## 5. 架构合规自检（§2 十条相关项）

| # | 铁律 | 自检 |
|---|------|------|
| 1 | 算法只在 Python | ✅ polan 全 Python；Java/前端不含算法 |
| 2 | 调用链前端→Java→Python | ✅ `/v1/policy/**` + `/internal/policy/**` 供 Java |
| 3 | 图谱 NebulaGraph(gkx_policy) 禁 Neo4j | ✅ space gkx_policy 7 tag/4 edge；不可用 PG/SQLite 镜像兜底 + API 自动回退 |
| 7 | Java 只读 ADS / 不写算法 / 不直连 nGQL | ✅ 全部结果落 gkx_ads.*；图谱经 Python 灌 Nebula |
| 8 | 标准表先行 + Mock | ✅ ADS 先行 + `mock_20260623` 前缀 |
| 10 | 数据血缘 8 件套 | ✅ 每张 ADS 带 metric_id；模型注册 cfg_model_registry（含 evaluation 元数据） |
| 模型注册 | 注册到 cfg_model_registry | ✅ 11 条 POLICY 模型（NER/RE/6 深度/3 文本），engine 可插拔(rule→bert/llm) |

---

## 6. 阻塞与风险（数据缺口 / 兜底说明）

| 项 | 描述 | 当前处理 | 责任 |
|----|------|----------|------|
| QPOL-01 类型口径 | 政策"类型"一级分类规则未定 | 临时取 ext1(topic_type)，ext 标 pending；上线前需甲方确认 | PM→甲方 |
| QPOL-02 推演参数 | 力度/效果/焦点/短板/机遇/布局/三维 权重阈值未定 | 规则基线经验权重（settings_policy.yaml weights），全部标 is_mock + pending；可配置 | 算法 lead+甲方 |
| QPOL-03 匹配规则 | 关联度/产业适配/匹配相似度规则未定 | 临时共现/特征重合规则 | 算法 lead+甲方 |
| 效果/落地数据缺口 | 执行监测/宏观经济/社会发展数据无 ODS 来源 | effect/impl 的社会·环境维度用受控随机代理（seed 固定），ext 标 data_gap=待采购 | PM+数据 lead |
| Nebula 可用性 | 本地无 Nebula（192.168.88.43:9669 不可达/未配） | nebula_loader 安全跳过；图谱在 PG/SQLite 镜像 policy_graph_node/edge，API 自动回退；有环境时 set POLAN_NEBULA_ENABLED=1 即灌入 | 算法/运维 |
| 后端形态 | 本地用 SQLite 验证全链路 | 默认 sqlite 保证零依赖真跑；生产 set POLAN_DB_BACKEND=pg 切 PostgreSQL（同 entan 库形态，DDL 单一 spec 生成，schema_policy_ads.sql 为 PG 交付物） | 算法/data |
| 深度字段格式 | elements/keypoints/factors/pedigree 真源结构待确认 | Mock 用 JSON/分隔符；生产解析规范待 data-agent + 供方确认，schema 不变 | data-agent |

---

## 7. 一句话总结

`polan` 自包含包（common 双后端 / 5 基础指标 / NER+RE 图谱 / 6 深度模型 / 3 文本处理 / 模型注册 / Mock）已落地；
`python scripts/run_all_policy.py` 在本地 SQLite 后端**全 15 步真实跑通**（总耗时 ~1s，幂等可重跑）；
ADS 产出：政策 600、级别 6、类型 5、时序 9、全国 31、深圳 9、焦点/机遇 631、力度 631、效果/短板/布局 93、三维 93、NER 7517、图谱 806 节点/3726 边、文本解析 600、匹配 144、推演 36、模型注册 13(含 11 POLICY)；
对外端点：`/v1/policy/{indicators,metrics,graph,analysis/{modelId},text/parse,match,simulate}` + `/internal/policy/models/registry`（响应 {code,msg,data}）。
