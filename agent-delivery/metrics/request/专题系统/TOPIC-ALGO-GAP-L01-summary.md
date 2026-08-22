# TOPIC-ALGO-GAP-L01 · 专题差集计数

> 任务：`TOPIC-ALGO-GAP-L01` · 日期：2026-08-22 · 对照：SRS 05（97 叶）+ B 轨 63 `M_CHAIN_*` / 29 `M_SVC_*`  
> A1 双表未交，`A1需规ID` / `A1指标叶ID` 一律空，交卷后回填。

## 总览

| 口径 | 条数 |
|------|------|
| 页面包 | 20 |
| 清单行 | **250** |
| **missing（主交付）** | **7** |
| mapped | 171 |
| third_party | 10 |
| other_system | 39 |
| n/a_ops | 23 |
| 语义欠账（不进 missing） | 111 |

## 按模块

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

## missing 主清单（7）

| page_id | metric_id | 主项 |
|---------|-----------|------|
| CHAIN-TOPIC-PANORAMA | `M_CHAIN_PRODUCT_COUNT` | 产业链关联产品数 |
| CHAIN-TOPIC-PANORAMA | `M_CHAIN_PATENT_COUNT` | 产业链关联专利数 |
| CHAIN-TOPIC-DIAGNOSIS | （无正式 ID） | 环节健康度 |
| CHAIN-TOPIC-SHENZHEN | （无正式 ID，IC-36） | 全球成功案例匹配 |
| E7-POLICY | `M_POLICY_INDUSTRY_FIT` | 产业适配性 |
| SYNTH-ELEMENT | `M_SYNTH_ELEM_CONTRIB` | 要素贡献度与影响路径 |
| SYNTH-COLLAB | `M_SYNTH_COLLAB_OUTPUT_CORR` | 协同—创新产出关联结果 |

未发明 `M_*` 写入 seed。B 轨已有 ID 未打 missing。
