# SYNTH L2 拆分总览（并行执行索引）

- 日期：2026-11-06（v1.0.6：功能合规过渡。正式结果仍落 ADS；137 过渡结果落 `_ai`，C-05 年化输入落 gapfill）
- 状态：三册四角色均为同意，可进入签收。签收由 human:淮政玮 执行。不另开任务，不改任务状态。

## ADS 实测结论（2026-11-04 实查，评审要求的资产审计先行结论）

2026-11-04 实查：`demo_gkxlumenx_ads` / `gkxlumenx_ads` 没有 synth 活力/要素/协同表。正式结果仍在这两个库里新建 `synth_*`。功能合规例外：137 未注册指标结果落 `_ai.synth_elem_four_dim_score`；C-05 年化输入落 gapfill，不把最终图结果放 gapfill。

## 册清单（落点 = 总册 §11 v1.0.5：ADS。当前必建 = 活力 5 + 要素 8 + 协同指标 4。另有协同空表 cluster、batch_meta、node、edge。四维不建。gapfill 只有活力既有 3 张输入）

| 册 | 覆盖 | 当前 ADS | 不在本期 | 空态 |
|---|---|---|---|---|
| `SYNTH-L2-VIT-AI-TABLES.md` | 活力补册 | 5 张 `synth_vit_*` | — | 权重无行 → null+reason，禁止常量 |
| `SYNTH-L2-ELEM.md` | 要素 | 8 张 ADS + `_ai.synth_elem_four_dim_score` 过渡表 | — | 缺 `_ai` 过渡表才回 `[]+metric_not_registered`；全景查 DWD |
| `SYNTH-L2-COLLAB.md` | 协同 | ADS 结果表 + `gapfill_synth_collab_relation_year/output_year` 年化输入 | — | 有 gapfill 输入则计算图和相关性；无输入才回 `no_year_on_source`；集群仍 `cluster_rule_unclosed` |

库名：`demo_gkxlumenx_ads` / `gkxlumenx_ads`。灌数方 entan-py。接口只读这些表。

## 并行分配（实现期）

| 并行线 | 依据册 | 动作 |
|---|---|---|
| 线1 活力 | VIT 补册 | 5 张 `synth_vit_*` DDL+预填+装包读表 |
| 线2 要素 | ELEM 册 | 8 张 ADS + 全景 DWD 聚合；137 四维 `_ai` 过渡表 |
| 线3 协同 | COLLAB 册 v1.0.10 | ADS 表 + gapfill 年化输入；Python 计算图/网络统计/相关性；集群仍空表。策略 LLM 无表 |

共享约定（公共列、`calc_batch_created_at` 批次排序、`calc_status`、缺行策略、`weight_source`）以总册 §11 为唯一真源；改共享约定必须回总册改。Java Adapter 要素/协同共改 BE-1 时按「同仓一单」协调。

## 治理规则

1. **本目录只拆文档，不拆 WBS 单**；实现单并行启动时按册认领/扩范围（如 `LUMEN-INTEL-BE-1` 扩要素/协同装包与图谱接口）。
2. 各册含：流程、每表四项（粒度/唯一键/写入/读批）、接口参数与异常空态、血缘、观测、验收条件、**页面差距审计**、实现单/文件边界。实现 agent 只读对应分册 + 总册 §11 即可开工。
3. 口径一律引用 `metrics/calc-logic/SYNTH/*.md` 与 `Q-SYNTH-*`；Q-* 升绿只改 calc-logic 与总册。
4. 会签建议：总册先签 → 三册一桌连签。
5. 交付对账（评审线诉求）：`reconciliation/` 三件（9 叶功能覆盖矩阵 / 指标落表矩阵含 ADS 实测列 / 页面区块对账）为下一产出，作为会签附件与拆单输入。

## 修订

| 版本 | 日期 | 说明 |
|---|---|---|
| v0.1 | 2026-11-04 | 首版 |
| v0.2 | 2026-11-04 | 表数修正、深度声明 |
| v0.3 | 2026-11-04 | 对齐总册 v0.5：`_ai` 只留指标/产物表（18），panorama/node/edge 移 gapfill；cluster 归指标结果组；137② 方案 A；FE 差距审计入册；ADS 实测结论（无可复用表、`_ai` 库已存在不新建） |
| v0.4 | 2026-11-04 | 对齐总册 v0.6：strategy 表废止→LLM 实时生成、cluster 口径挂靠保留；panorama 改真实 DWD 汇聚；gapfill 收敛为图事实 2张 |
| v0.5 | 2026-11-04 | 对齐总册 v0.7：137 过渡数据落表方案（后被 v0.6 改 blocked）；gapfill 批次字段统一 `gapfill_batch_id`；权重 `weight_profile_code` |
| v0.6 | 2026-11-04 | 对齐总册 v0.8：`_ai`=**19 张**（5+9+5 按实际清单）；137② 改 blocked（不建表不出数）；panorama DTO 已定；node/edge 行级 metric_id 血缘；协同 5 张口径统一 |
| v1.0 | 2026-11-05 | 对齐总册 v1.0-draft；头部/册清单版本引用统一；标明 18 可建 + planned 第 19 张 |
| v1.0.5 | 2026-11-05 | 四角色退回后：结果与图改落 ADS；137② 与集群不记本期交付 |
| v1.0.6 | 2026-11-06 | 功能合规过渡：137 结果落 `_ai`、C-05 年化输入落 gapfill；正式指标/真源后续对齐 |

