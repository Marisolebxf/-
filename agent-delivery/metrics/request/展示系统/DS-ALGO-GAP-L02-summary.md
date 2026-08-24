# DS-ALGO-GAP-L02 · 展示差集计数（A1 回填）

> 任务：`DS-ALGO-GAP-L02` · 日期：2026-08-24  
> 底稿：`DS-ALGO-GAP-L01` Round 18（不覆盖）  
> 对照真源：A1 表1 `ALGO-LIB-METRIC-DEPS-L01-requirements.yaml`（97 叶）+ 表2 `ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`（101：11 `M_*` + 90 `TEMP_ALGO_*`）  
> 消费：`TOPIC-ALGO-GAP-L02` missing **7→7**（不重列）  
> yaml 为机器真源。未覆盖根目录半成品 xlsx。

## 两套计数（必须分开）

| 口径 | L01 Round 18 | L02 | 说明 |
|------|----------------|-----|------|
| **缺 OPEN 叶 · DS-01…09 / E-ZHIKU / DS-10…12** | **0** | **0（未回滚）** | catalog 指针未改。 |
| **缺 OPEN 叶 · DS-13～16** | **4** | **4（仍 missing）** | 未改挂 `TOPIC-TALENT`。 |
| **库 missing 主清单**（列 11，去专题重复） | **70** | **70** | A1 97 叶仍无专叶；未改 mapped。 |
| items 内 missing（含专题 also_in） | 71 | 71 | `M_POLICY_INDUSTRY_FIT` 仅 also_in。 |

缺 OPEN 叶 ≠ 库缺口。OPEN 存在不把 `missing` 改 `mapped`。

## 总览（列 11，库差集）

| 口径 | 条数 |
|------|------|
| 页面包 | **75**（+ FANIN 数据需求 1 行） |
| 清单行 | **930** |
| **missing 主交付（去专题重复）** | **70** |
| items 内 missing（含专题已列） | 71 |
| mapped | 204（全部已填 A1需规ID / A1指标叶ID） |
| third_party | 16（14 条已填 A1 ID；2 条投融资保持空） |
| other_system | 336 |
| n/a_ops | 303 |
| 语义欠账 | 247 |

专题 7 条 missing **不重列**。`M_POLICY_INDUSTRY_FIT`（DS-10，缺口说明含 also_in E7-POLICY）不进主清单。

## 改判定行清单

**无。** missing 70→70。禁止用相邻叶 / 图谱 API / 区域指数顶替下列专核缺口。

## mapped 回填（204）

| 方法 | 条数 | 说明 |
|------|------|------|
| 页面 `algo_lib_leaf` → 表1 `requirement_title` | 多数 | SRS 05 临时底换成表1/表2 |
| `05_seq` | 8 | 取数依据 / note 中的 seq |
| B 轨小节名 → 维基础叶 | 门户 6 条等 | `#产业市场规模` 等不是表1 标题，落到 `ALGO-CHAIN-BASE-95` |

列 14 `metric_id` 保留语义层 / B 轨已有 `M_*`；**不把 `TEMP_ALGO_*` 写入列 14**；不编造正式 `M_*`。

## third_party 未填 A1（2）

| row_id | 主项 | 原因 |
|--------|------|------|
| DS-CHAIN-OV-009 | 投融资总额 | 保持 third_party；缺口说明禁止改 mapped |
| DS-CHAIN-OV-010 | 投融资事件数 | 同上 |

## 按模块（清单行，含 items 内 missing）

| 模块 | 页 | mapped | missing | third_party | other_system | n/a_ops | 合计 |
|------|----|--------|---------|-------------|--------------|---------|------|
| 科技发展态势 | 35 | 52 | 43 | 13 | 89 | 71 | 268 |
| 科技政策跟踪 | 3 | 25 | 3 | 0 | 11 | 17 | 56 |
| 科技人才态势 | 4 | 33 | 6 | 0 | 26 | 27 | 92 |
| 科技成果展示 | 5 | 7 | 5 | 0 | 50 | 28 | 90 |
| 科技知识图谱 | 4 | 8 | 14 | 0 | 13 | 20 | 55 |
| 科技服务全景 | 5 | 0 | 0 | 0 | 34 | 11 | 45 |
| 科技数据资源 | 4 | 0 | 0 | 0 | 45 | 25 | 70 |
| 企业展示 | 13 | 64 | 0 | 1 | 60 | 76 | 201 |
| 新型高端智库 | 1 | 0 | 0 | 0 | 6 | 25 | 31 |
| 智慧服务门户 | 1 | 15 | 0 | 2 | 1 | 3 | 21 |
| 数据资源 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |

## missing 主清单（70，维持）

与 L01 Round 18 主清单相同（改判定行 0）。详见 `DS-ALGO-GAP-L01-summary.md` 同表。未发明 `M_*`。B 轨已有 ID 未打 missing。

## OPEN 指针

Round 18 `metric_open_status` **未改**。DS-13～16 仍 missing。未改挂 `TOPIC-TALENT`。专题 catalog 未动。

## skip（不进清单）

| page_id | 原因 |
|---------|------|
| EDU-ADDON | 教育核增 |
| POLICY-COMPARE-ADDON | 政策对比核增 |
| DS-ANTI-EPIDEMIC | 招标核减 |
| DS-DATAREQ | 一行 other_system 汇总 |
