# 企业分类型匹配数量（M_ENT_TYPE_MATCH_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_MATCH_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_MATCH_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_MATCH_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_TYPE_MATCH_COUNT |
| 指标名称 | 企业分类型匹配数量 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 二级模块 | 重点企业类型分析 |
| 三级模块 | 类型与区域分析 |
| 更新频率 | 日 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业分析·类型与区域分析「匹配企业总数」卡｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_TYPE_MATCH_COUNT.md` |

## 口径定义

按「所选产业 ∩ 所选类型」的国内去重口径，gkx 上可以给出 12 链 × 6 类的完整矩阵：严格链属 28,031 家，高企 12,776、专精特新 8,410、小巨人 1,399、外资 2,214、小微 19,785、上市 1,178。矩阵的每一格都能复算，且 12 条链的链属数相加正好等于 28,031（一家只挂一条链，无重复计数）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_MATCH_COUNT.md` §二（M_ENT_TYPE_MATCH_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_chain_dtl`
- `dwd_org_industry_tags`
- `dwd_org_stock_base`
- `dwd_org_tech_tag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：12 条战略链真链属 28,031 家在底册内，与六类资质同源可交，链×类型矩阵 12×6 全部有数；但产业侧只有『链属』没有『非链属但属该产业』，标签表 7,015 家只挂顶层链无细分链被排除，且链标签来自 dwd_org_industry_tags 单一表、无第二来源校验，故判部分支持。
- **基期声明**：截面交叉计数，无年度序列；不设基期

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_MATCH_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_MATCH_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_MATCH_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

