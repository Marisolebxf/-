# 企业总数（M_ENT_TOTAL_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TOTAL_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TOTAL_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TOTAL_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_TOTAL_COUNT |
| 指标名称 | 企业总数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 二级模块 | 企业总览 |
| 三级模块 | 企业整体概况 |
| 更新频率 | 日 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业分析·企业总览「企业总数」卡｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_TOTAL_COUNT.md` |

## 口径定义

按 2026-08-27 calc-logic 的「国内 ∪ 国外主档」口径，gkx 上可以跑通并给出 **209,116** 家：国内主档 189,116 家、国外主档 20,000 家、两侧 `org_id` 零重叠；但国外主档只有 GB 19,832、US 159、CA 9 三个国家，7,365 行名称为字面空值、7,457 行无外部注册码，属**国别样本档**而不是全球名录。国内侧本身是「广东底册」（广东 188,776 家，占 99.82%），所以 209,116 只能作「库内可见企业数」，不能作「全国企业总数」对外发布，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TOTAL_COUNT.md` §二（M_ENT_TOTAL_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_chain_dtl`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：国内主档完整可算（189,116 家、189,116 个 org_id/信用码），但国外主档 gkx.dwd_forg_base_info 只有 20,000 行、3 个国家（GB 19,832 / US 159 / CA 9），其中 7,365 行 name_en 为字面 'null'，属样本性主档而非全球企业名录；『全球企业总数』的国外维无法闭合。
- **基期声明**：截面计数，无年度序列；基期不适用（库内成立年跨 1900—2026，但本指标不按年摊分母，故 used/missing 均为空）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TOTAL_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TOTAL_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TOTAL_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

