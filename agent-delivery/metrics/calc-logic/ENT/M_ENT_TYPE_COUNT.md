# 企业分类型数量（M_ENT_TYPE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_TYPE_COUNT |
| 指标名称 | 企业分类型数量 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 二级模块 | 重点企业类型分析 |
| 三级模块 | 类型与区域分析 |
| 更新频率 | 月度/年度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业分析·类型与区域分析「各类型企业数」六卡｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_TYPE_COUNT.md` |

## 口径定义

六类在 gkx 上都能给出数：高企 27,936、专精特新 14,830、小巨人 2,006、外资 10,417、小微 125,477、上市 1,971，六类求和 182,637（因重叠不可当总数）。但 calc-logic 指定的六码表 `enterprise_tag` 在 gkx 与 live 都不存在，本件只能用「科技标签表 + 主档工商字段」重建六类；其中上市只有 1,971 家、A/B 股仅 975 家，外资是 `org_type` 自由文本关键词且含港澳台，小微有 46,897 家规模未知。六类口径不等权、数据完备度差异大，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_COUNT.md` §二（M_ENT_TYPE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_stock_base`
- `dwd_org_tech_tag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：六类中四类（高企/专精特新/小巨人/小微）表结构+表数据直接可算；外资类 org_type 是工商登记类型自由文本，需关键词口径且含港澳台；上市类底册 listing_status 仅 1,971 家、dwd_org_stock_base 只覆盖 A/B 股 975 家，缺港股/美股/新三板，六类口径不等权，合计不可当『企业总数』使用。
- **基期声明**：截面资质计数，无年度序列；资质本身有授予年（高企 3 年有效），但 gkx 标签表无生效/失效日期列，故不拆年份

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

