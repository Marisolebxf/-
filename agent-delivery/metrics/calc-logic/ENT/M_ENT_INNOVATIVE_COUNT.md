# 创新型企业数（M_ENT_INNOVATIVE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INNOVATIVE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATIVE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATIVE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_INNOVATIVE_COUNT |
| 指标名称 | 创新型企业数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | ENT（企业分析） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 企业分析 → 重点企业分析 → 类型与区域分析 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_INNOVATIVE_COUNT.md` |

## 口径定义

{'unit': '家企业', 'dedupe_key': 'org_id', 'families': [{'label': '创新型中小企业', 'match': '创新型中小企业', 'n_org': 16864}, {'label': '专精特新中小企业', 'match': '专精特新中小企业', 'n_org': 14830}, {'label': '专精特新小巨人', 'match': '专精特新小巨人', 'n_org': 2006}, {'label': '制造业单项冠军', 'match': '单项冠军', 'n_org': 686}], 'rule': '四类标签任一命中即计入，一企多牌只计一次'}

> 一句话口径（源件 §0.3）：库内没有「创新型企业数」现成结果面（live `ads` 侧无同名指标表），但依赖表 `gkx.dwd_org_tech_tag` 结构完整、202,424 行、32,322 家机构，四类名单标签全部命中，且 `org_id` 与 18.9 万行底册的主键匹配率 **99.997%**，城市维可直接落表——结构与数据双满足，属**完全转换支持**。本档位与 `code/M_ENT_INNOVATIVE_COUNT_out.json` 的 `support_judgment` 字段一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INNOVATIVE_COUNT.md` §二（M_ENT_INNOVATIVE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：库内没有「创新型企业数」现成结果面（live `ads` 侧无同名指标表），但依赖表 `gkx.dwd_org_tech_tag` 结构完整、202,424 行、32,322 家机构，四类名单标签全部命中，且 `org_id` 与 18.9 万行底册的主键匹配率 **99.997%**，城市维可直接落表——结构与数据双满足，属**完全转换支持**。本档位与 `code/M_ENT_INNOVATIVE_COUNT_out.json` 的 `support_judgment` 字段一致。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.2 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INNOVATIVE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATIVE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATIVE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

