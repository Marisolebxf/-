# 重点企业总数（M_ENT_KEY_TOTAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEY_TOTAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEY_TOTAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEY_TOTAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEY_TOTAL |
| 指标名称 | 重点企业总数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统·企业整体概况「重点企业」读数（算法库 bid §1.1.1.2.4.2.3）；KEYPANO 8 件套的名单母体｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_KEY_TOTAL.md` |

## 口径定义

无现成名单面（且 calc-logic 明令 demo 87 行不算接通）→ 非完全直接支持；真源 gkx 294 万专利行**结构+当前量均足**，阈值口径（≥50 件）分桶聚合已两轮实跑出 6,917 家非退化名单 → **完全转换支持**；阈值 N=50 是团队临时值（Q038🟡）不改变「可构建」判定，只标注口径未闭合。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEY_TOTAL.md` §二（M_ENT_KEY_TOTAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_base_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：专利阈值口径现算成功：dwd_patent 294 万按第一当前受让人聚合，≥50 件的去重受让人 6,917 家（分布 {'50-99': 4093, '100-499': 2398, '500-1999': 330, '2000+': 96}；头部 79,089 件）。受让人→org_id 映射为 ETL 对齐步骤（名称归一），结构+当前量+现转成功 → 完全转换支持。（Q038 阈值 50 仍🟡临时值；技术交易额版搁置不影响本判定。）
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEY_TOTAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEY_TOTAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEY_TOTAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

