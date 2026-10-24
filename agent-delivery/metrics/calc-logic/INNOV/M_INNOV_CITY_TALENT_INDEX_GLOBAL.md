# 人才创新指数（全球城市语境）（M_INNOV_CITY_TALENT_INDEX_GLOBAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CITY_TALENT_INDEX_GLOBAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_GLOBAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_GLOBAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_TALENT_INDEX_GLOBAL |
| 指标名称 | 人才创新指数（全球城市语境） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统／科技人才智慧服务／人才创新评估 |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才指数卡、城市对比条 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_CITY_TALENT_INDEX_GLOBAL.md` |

## 口径定义

在 21 个「可锚定学者 ≥200 人」的城市里，深圳以 **71.17** 分排第一，但这个第一几乎全部来自**人均与占比**：规模叶（学者数）只有 **1.45** 分，而上海 77.00、北京（学者 2,841 人）在池内排第 6、总分 **43.48**。把规模叶权重从 0 扫到 1，**w ≥ 0.36 上海反超、w ≥ 0.45 北京反超**——榜首不是数据定的，是权重定的。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CITY_TALENT_INDEX_GLOBAL.md` §二（M_INNOV_CITY_TALENT_INDEX_GLOBAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`
- `dwd_scholar`
- `dwd_scholar_talent_flag`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：在 21 个「可锚定学者 ≥200 人」的城市里，深圳以 **71.17** 分排第一，但这个第一几乎全部来自**人均与占比**：规模叶（学者数）只有 **1.45** 分，而上海 77.00、北京（学者 2,841 人）在池内排第 6、总分 **43.48**。把规模叶权重从 0 扫到 1，**w ≥ 0.36 上海反超、w ≥ 0.45 北京反超**——榜首不是数据定的，是权重定的。
- **基期声明**：论文产出叶取 2021—2023 三年；2017—2020 不进分母，原因是 dwd_patent.apdt_year 这四年零行（DATA_FACTS §3.13），且 2024 年中文论文语料是回填孤峰（32,379 篇，为 2023 年的 4.87 倍），放进窗口会把四城论文组件同时抬高、画出假上行线。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CITY_TALENT_INDEX_GLOBAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_GLOBAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_GLOBAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

