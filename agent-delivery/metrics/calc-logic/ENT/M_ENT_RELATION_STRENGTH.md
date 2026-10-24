# 关系强度（M_ENT_RELATION_STRENGTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RELATION_STRENGTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RELATION_STRENGTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RELATION_STRENGTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_RELATION_STRENGTH |
| 指标名称 | 关系强度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 月度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业关系图谱边权着色、企业详情页「对外投资」列表的强度标签 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_RELATION_STRENGTH.md` |

## 口径定义

关系强度在 calc-logic 里是「一条边 + 一个档」，主口径只看投资金额落在哪个区间，两条辅证用来「作证」。gkx 里主口径的源表与金额都在，档位当场可切；但两条辅证各自对应的表一张都没有。也就是说：**能算出主档，但算不出 calc-logic 要求的「三源互证」**。按四档定义，这属于「始终有部分依赖维度无法得到足够数据」，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RELATION_STRENGTH.md` §二（M_ENT_RELATION_STRENGTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：关系强度在 calc-logic 里是「一条边 + 一个档」，主口径只看投资金额落在哪个区间，两条辅证用来「作证」。gkx 里主口径的源表与金额都在，档位当场可切；但两条辅证各自对应的表一张都没有。也就是说：**能算出主档，但算不出 calc-logic 要求的「三源互证」**。按四档定义，这属于「始终有部分依赖维度无法得到足够数据」，判**部分支持**。
- **基期声明**：截面件：投资边无统一发布年度键（仅有 created_time/updated_time），不做年度序列、不把缺失年摊 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RELATION_STRENGTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RELATION_STRENGTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RELATION_STRENGTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

