# 深圳企业清单与链中角色（M_ENT_SZ_LIST_TOPIC）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SZ_LIST_TOPIC.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_LIST_TOPIC.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_LIST_TOPIC_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_SZ_LIST_TOPIC |
| 指标名称 | 深圳企业清单与链中角色 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 专题企业 / TOPIC-ENT-05 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 专题页「深圳上链企业清单」表 + 选链筛选｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_SZ_LIST_TOPIC.md` |

## 口径定义

深圳 12 条产业链上共 92,930 家企业可列，占全国同链企业 1,714,457 家的 5.42%；但「链中角色（上/中/下游）」这一列在 gkx 无字段，只能给到一级环节，故判部分支持。

## 计算逻辑说明

```text
members = {(credit_code, chain_code, l1_code) | credit_code[2:6]=4403 AND chain_code != null}
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SZ_LIST_TOPIC.md` §二（M_ENT_SZ_LIST_TOPIC.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`
- `dwd_bid_base_out_bak_20260911`
- `dwd_bid_base_out_bak_20260923`
- `dwd_forg_executive_info`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：深圳键与链归属都可等价实现（深圳 92,930 家与已交付链企业快照逐项对上），但 calc-logic 要求的角色字段 node_stage（上/中/下游）在 gkx 全库 0 字段，链树只有目录层级与环节名，不能推出上中下游 → 清单可出、角色不可出。
- **基期声明**：本件是链属快照的截面清单（dwd_org_industry_tags 为当前态，无年度分区），不涉及多期基期；快照抓取日 2026-10-22/23。不把缺失年份按 0 摊入任何分母。
- **复现实测耗时**：约 0.3 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SZ_LIST_TOPIC.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_LIST_TOPIC.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_LIST_TOPIC_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

