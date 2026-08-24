# TOPIC-ALGO-GAP-L02 · 专题差集计数（A1 回填）

> 任务：`TOPIC-ALGO-GAP-L02` · 日期：2026-08-24  
> 底稿：`TOPIC-ALGO-GAP-L01` Round 17（不覆盖）  
> 对照真源：A1 表1 `ALGO-LIB-METRIC-DEPS-L01-requirements.yaml`（97 叶）+ 表2 `ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`（101 条：11 `M_*` + 90 `TEMP_ALGO_*`）  
> yaml 为机器真源。未覆盖根目录半成品 xlsx。未开工展示叶。

## 两套计数（必须分开）

| 口径 | L01 Round 17 | L02 | 说明 |
|------|----------------|-----|------|
| **缺 OPEN 叶**（catalog `metric_open_status=missing`） | **0** | **0（未回滚）** | 只加 A1 字段，不改指针。 |
| **库 missing**（列 11） | **7** | **7** | A1 97 叶仍无专叶覆盖；未改 mapped。 |

缺 OPEN 叶 ≠ 库缺口。OPEN 存在不把 `missing` 改 `mapped`。

## 总览（列 11，库差集）

| 口径 | 条数 |
|------|------|
| 页面包 | 20 |
| 清单行 | **250** |
| **missing（主交付 / 库未覆盖）** | **7** |
| mapped | 171（全部已填 A1需规ID / A1指标叶ID） |
| third_party | 10（9 条已填 A1 ID；1 条无对应叶，ID 空） |
| other_system | 39 |
| n/a_ops | 23 |
| 语义欠账 | 111 |

## 改判定行清单

**无。** missing 7→7。禁止用全景/基础指标/瓶颈/协同叶顶替下列专核缺口。

## missing 主清单（7，维持）

| row_id | page_id | metric_id | 主项 | A1 复判 |
|---------|-----------|-----------|------|---------|
| TOPIC-PAN-006 | CHAIN-TOPIC-PANORAMA | `M_CHAIN_PRODUCT_COUNT` | 产业链关联产品数 | 表1 无产品计数专叶；BASE-95 / DEEP-117 不顶替 |
| TOPIC-PAN-007 | CHAIN-TOPIC-PANORAMA | `M_CHAIN_PATENT_COUNT` | 产业链关联专利数 | 无链级专利计数专叶；不映射技术链维 |
| TOPIC-DIAG-018 | CHAIN-TOPIC-DIAGNOSIS | （无正式 ID） | 环节健康度 | DEEP-125 瓶颈五维 ≠ 环节健康度 |
| TOPIC-SZ-016 | CHAIN-TOPIC-SHENZHEN | （无正式 ID） | 全球成功案例匹配 | 16 叶无成功案例叶 |
| TOPIC-POL-005 | E7-POLICY | `M_POLICY_INDUSTRY_FIT` | 产业适配性 | 政策 9 叶无适配性评估；禁止用 185/力度/效果顶替 |
| TOPIC-ELEM-009 | SYNTH-ELEMENT | `M_SYNTH_ELEM_CONTRIB` | 要素贡献度与影响路径 | 187–190 非贡献路径；191/116 不顶替 |
| TOPIC-COL-006 | SYNTH-COLLAB | `M_SYNTH_COLLAB_OUTPUT_CORR` | 协同—创新产出关联结果 | 191 未列产出相关 |

未发明 `M_*` 写入 seed。列 14 不含 `TEMP_ALGO_*`。

## mapped 回填（171）

| 方法 | 条数 | 说明 |
|------|------|------|
| 页面 `algo_lib_leaf` → 表1 `requirement_title` | 多数 | SRS 05 临时底换成表1/表2 |
| `row_override` | 4 | TOPIC-SZ-011～014 深圳四维对比 → `ALGO-CHAIN-DEEP-118`（页面无 leaf，B 轨已 mapped） |
| `05_seq` | 1 | TOPIC-ENT-002 → `ALGO-ENT-BASE-97` |
| `text_title` | 1 | TOPIC-ENT-007 `#深圳企业竞争力水平分析模型` → `ALGO-ENT-DEEP-141` |
| `reuse_same_metric_id` | 2 | 门户 PT-006 / PT-012 复用 ORG-ANALYSIS 已填 A1 ID |

A1 表2 正式 `M_*` 仅 11 条（全企业维）。产业链/政策/服务/综合等 mapped 行的 **A1指标叶ID** 多为 `TEMP_ALGO_*`（未入 seed）。列 14 保留语义层 / B 轨已有 `M_CHAIN_*` / `M_SVC_*` 等。

完整回填表：`TOPIC-ALGO-GAP-L02.xlsx` sheet「回填清单」；机器日志 `metrics/request/_work/TOPIC-ALGO-GAP-L02-fill-log.csv`。

## third_party 未填 A1（1）

| row_id | 主项 | 原因 |
|--------|------|------|
| TOPIC-RORG-012 | 科研机构技术力评价与对比 | 表1 科研机构 10 叶无技术力对比专叶；禁止改挂服务机构 174–179 |

## OPEN 指针

Round 17 `metric_open_status=present` **未改**（catalog 18 present；TOPIC-OPS=`n/a_ops`；TOPIC-DATAREQ=`other_system`）。未新增 `TOPIC-ZHIKU`。展示 catalog 未动。

## 按模块（列 11，与 L01 相同）

| 模块 | mapped | missing | third_party | other_system | n/a_ops |
|------|--------|---------|-------------|--------------|---------|
| 产业链分析 | 66 | 4 | 0 | 1 | 1 |
| 产业服务链分析 | 31 | 0 | 0 | 4 | 2 |
| 政策分析 | 12 | 1 | 0 | 2 | 4 |
| 综合智能分析 | 19 | 2 | 0 | 5 | 0 |
| 企业分析 | 14 | 0 | 0 | 1 | 2 |
| 技术链分析 | 4 | 0 | 9 | 1 | 1 |
| 科研机构分析 | 10 | 0 | 1 | 5 | 1 |
| 人才分析 | 15 | 0 | 0 | 3 | 1 |
| 数据查询 | 0 | 0 | 0 | 7 | 7 |
| 运营管理 | 0 | 0 | 0 | 0 | 4 |
| 数据需求 | 0 | 0 | 0 | 10 | 0 |
