# TOPIC-ALGO-GAP-L01 · 专题差集计数

> 任务：`TOPIC-ALGO-GAP-L01` · 日期：2026-08-22 · **Round 17**（METRIC-OPEN-LOOP 指针返工）  
> 对照：SRS 05（97 叶）+ B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*`  
> A1 双表未交，`A1需规ID` / `A1指标叶ID` 一律空，交卷后回填。  
> yaml 为机器真源。根目录半成品 xlsx 未覆盖。

## 两套计数（必须分开）

| 口径 | 旧版（Round 17 前） | Round 17 后 | 说明 |
|------|---------------------|-------------|------|
| **缺 OPEN 叶**（catalog `metric_open_status=missing`） | **11 页** | **0** | 只改指针 + 分类。语义层已挂上。 |
| **库 missing**（列 11，功能要了、算法库未覆盖） | **7** | **7（未改）** | 禁止把库缺口改成 mapped。 |

缺 OPEN 叶 ≠ 库缺口。OPEN 存在不把 `missing` 改 `mapped`。

## 总览（列 11，库差集）

| 口径 | 条数 |
|------|------|
| 页面包 | 20 |
| 清单行 | **250** |
| **missing（主交付 / 库未覆盖）** | **7** |
| mapped | 171 |
| third_party | 10 |
| other_system | 39 |
| n/a_ops | 23 |
| 语义欠账（口径/公式/分项，不进 missing） | 111 |

## 按模块（列 11）

| 模块 | 页 | mapped | missing | third_party | other_system | n/a_ops |
|------|----|--------|---------|-------------|--------------|---------|
| 产业链分析 | 全景/诊断/区域/深圳 | 66 | 4 | 0 | 1 | 1 |
| 产业服务链分析 | 机构/生态/招引/门户 | 31 | 0 | 0 | 4 | 2 |
| 政策分析 | E7-POLICY | 12 | 1 | 0 | 2 | 4 |
| 综合智能分析 | 父索引+活力/要素/协同 | 19 | 2 | 0 | 5 | 0 |
| 企业分析 | TOPIC-ENT-05 | 14 | 0 | 0 | 1 | 2 |
| 技术链分析 | TOPIC-TECH-05 | 4 | 0 | 9 | 1 | 1 |
| 科研机构分析 | TOPIC-ORG-05 | 10 | 0 | 1 | 5 | 1 |
| 人才分析 | TOPIC-TALENT-05 | 15 | 0 | 0 | 3 | 1 |
| 数据查询 | TOPIC-QUERY | 0 | 0 | 0 | 7 | 7 |
| 运营管理 | TOPIC-OPS | 0 | 0 | 0 | 0 | 4 |
| 数据需求 | TOPIC-DATAREQ | 0 | 0 | 0 | 10 | 0 |

## missing 主清单（7，库未覆盖，Round 17 未改）

| page_id | metric_id | 主项 |
|---------|-----------|------|
| CHAIN-TOPIC-PANORAMA | `M_CHAIN_PRODUCT_COUNT` | 产业链关联产品数 |
| CHAIN-TOPIC-PANORAMA | `M_CHAIN_PATENT_COUNT` | 产业链关联专利数 |
| CHAIN-TOPIC-DIAGNOSIS | （无正式 ID） | 环节健康度 |
| CHAIN-TOPIC-SHENZHEN | （无正式 ID，IC-36） | 全球成功案例匹配 |
| E7-POLICY | `M_POLICY_INDUSTRY_FIT` | 产业适配性 |
| SYNTH-ELEMENT | `M_SYNTH_ELEM_CONTRIB` | 要素贡献度与影响路径 |
| SYNTH-COLLAB | `M_SYNTH_COLLAB_OUTPUT_CORR` | 协同—创新产出关联结果 |

未发明 `M_*` 写入 seed。B 轨已有 ID 未打 missing。SVCCHAIN 29 `M_SVC_*` 仍 mapped。

## OPEN 指针（Round 17 相对旧版）

旧版 catalog `metric_open_status: missing` → 本轮 `present`（11 页）：

| page_id | 指针 | task |
|---------|------|------|
| SVCCHAIN-ORG-ANALYSIS / ECOSYSTEM / RECOMMEND / PORTAL | `…/E7-产业服务链分析/METRIC-OPEN-SVCCHAIN-核对记录.md` | `SVCCHAIN-METRIC-OPEN-L01` |
| TOPIC-ENT-05 | `…/METRIC-OPEN-TOPIC-ENT-核对记录.md`（仅 `TEMP_TOPIC_ENT_*`；禁 `M_ENT_*` / `ENT-MOD-*`） | `TOPIC-ENT-METRIC-OPEN-L01` |
| TOPIC-TECH-05 | `…/METRIC-OPEN-TOPIC-TECH-核对记录.md` | `TOPIC-TECH-METRIC-OPEN-L01` |
| TOPIC-ORG-05 | `…/METRIC-OPEN-TOPIC-ORG-核对记录.md` | `TOPIC-ORG-METRIC-OPEN-L01` |
| TOPIC-TALENT-05 | `…/METRIC-OPEN-TOPIC-TALENT-核对记录.md`（不混 DS-13～16） | `TOPIC-TALENT-METRIC-OPEN-L01` |
| TOPIC-QUERY | `…/METRIC-OPEN-TOPIC-QUERY-核对记录.md` | `TOPIC-QUERY-METRIC-OPEN-L01` |
| E7-POLICY | `…/METRIC-OPEN-E7-DS10-12-核对记录.md`；**已删**「勿误用」 | `POLICY-METRIC-OPEN-L01` |
| SYNTH-REGION | **父索引** `metric_open_role: parent_index`；`metric_open: null`；三兄弟路径不变 | 不另建叶 |

本轮 **补** `metric_open_status: present`（原先已有 path、缺 status）：

- `CHAIN-TOPIC-*`（已有 CHAIN OPEN，禁止 missing）
- `SYNTH-VITALITY` / `ELEMENT` / `COLLAB`

保持不算缺 OPEN：

- `TOPIC-OPS` = `n/a_ops`
- `TOPIC-DATAREQ` = `other_system`
- `E-ZHIKU` = 专题 catalog **n/a**（未新增 `TOPIC-ZHIKU`；留给 Round 18 展示 catalog）

展示 catalog **未动**。
