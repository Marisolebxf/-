# SYNTH L2 拆分总览（并行执行索引）

- 日期：2026-11-05（v1.0：对齐总册 v1.0-draft——`_ai` 19 张、137② blocked、panorama DTO、node/edge 行级血缘；FE 差距审计；ADS 实测结论）
- 状态：三册 DRAFT；**前置条件：总册《综合智能分析-系统详细设计说明书.md》（v1.0-draft）四方会签**，会签后本三册方可进入各自会签与实现。

## ADS 实测结论（2026-11-04 实查，评审要求的资产审计先行结论）

对 `demo_gkxlumenx_ads` / `gkxlumenx_ads` 实查：**无任何 synth/活力/要素/协同相关表**（唯一近似 `chain_sz_elements` 属产业链域）。→ 三叶**不存在可复用 ADS 结果表**，全部按本目录新建路径执行；`demo/live` 的 `demo_gkxlumenx_ai` / `gkxlumenx_ai` 库已存在（INNOV 域 `innov_carrier_index`、`innov_scholar_influence`，注释「算法侧灌数，功能侧只读」），本模块沿用该库与命名惯例，**不新建库**。逐指标源表/字段级审计在 `metrics/calc-logic/SYNTH/*.md`（「源表字段/待建表字段」节，VIT 系已点名 `dwd_patent`、`dwd_org_tech_tag` 等实表），落 DDL 前按册引用，不另建总表。

## 册清单（落点口径 = 总册 §11.1/§11.3 v1.0-draft：`_ai` **19 张** = 活力 5 + 要素 9 + 协同 5（cluster 计入）；gapfill 新 2 张图事实（+活力既有 3）；strategy=LLM 实时、panorama=DWD 汇聚，均无表）

| 册 | 覆盖 | `_ai` 表（指标结果/分析产物） | gapfill 表 | blocked 项 | 并行启动条件 |
|---|---|---|---|---|---|
| `SYNTH-L2-VIT-AI-TABLES.md` | 活力补册 | 5 / 0 | （活力既有 3 张输入缺项，DBA 单） | 无 | 总册会签即可并行 |
| `SYNTH-L2-ELEM.md` | 要素全量 | 9（含 137② 正式表，**注册后建**） | 0（panorama=真实 DWD 汇聚无表，DTO 已定） | **137② blocked**：公式细则待算法 Lead 定稿+注册 | 总册会签即可并行（四维单除外） |
| `SYNTH-L2-COLLAB.md` | 协同全量 | **5**（含 cluster 口径挂靠；strategy 无表=LLM 实时生成） | 2（`gapfill_synth_collab_node/edge`） | 图 2 张真值待 C-05（预填演示行可先行） | 指标表可先行；图真值等贴源 |

> 落点裁定（总册 §11.1/§11.3 v1.0-draft）：**`_ai` 只放有指标口径的表（19 张 = 5+9+5，cluster 口径挂靠计入；当前可建 18 + planned 第 19 张四维）**；strategy=装包 LLM 实时生成（无表）；panorama=真实 DWD 汇聚（无表，DTO 已定）；node/edge=gapfill 预填演示行（D16，`gapfill_batch_id`，行级血缘拆 metric_id）。**137② 四维 blocked**：公式未定稿前不建表不出数（注册+定稿后建 `_ai` 表）。页面差距见各册「页面差距审计」节。

## 并行分配（实现期）

| 并行线 | 依据册 | 动作 |
|---|---|---|
| 线1 活力 | VIT 补册 | 5 张 `synth_vit_*` DDL+预填+装包读表 |
| 线2 要素 | ELEM 册 | 9 张 `_ai` DDL+panorama 真实聚合+装包+FE 四维接线（blocked 待注册）/全景模块 |
| 线3 协同 | COLLAB 册 | 5 张 `_ai`+2 张 gapfill 图事实+装包（含 LLM 策略）+图谱查询接口+FE 产业筛选 |

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

