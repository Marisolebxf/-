# 可视化行业分布（GAP-RECRUIT-METRIC-04）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-04.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-04.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-04_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | GAP-RECRUIT-METRIC-04 |
| 指标名称 | 可视化行业分布 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业培育 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 培育企业推荐分析（E-27，wireframe 第 6 列）｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/GAP-RECRUIT-METRIC-04.md` |

## 口径定义

无现成「可视化行业分布」结果表（live `enterprise_industry_distribution` 0 行）→ 非完全直接支持；深圳企业主档 95,600 家 + GB/T 四级行业字段（非空 98.8%）**结构齐全且行量充足**，脚本已现转出 98 个二级行业桶的完整分布数据集（Top1 占比 26.3%、Top5 占 64.3%，分布非退化）→ **完全转换支持**；正式统计口径（对象集合/分类层级）待甲方闭合（ER-B10）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-04.md` §二（GAP-RECRUIT-METRIC-04.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：深圳企业 95600 家、行业桶 98 个（二级），Top1 行业占比 26.33%（分布非退化）；live enterprise_industry_distribution=0（无现成结果面）。GROUP BY 现转即可出图表数据集；正式口径（对象集合/分类层级）待甲方闭合（ER-B10）。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/GAP-RECRUIT-METRIC-04.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-04.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/GAP-RECRUIT-METRIC-04_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

