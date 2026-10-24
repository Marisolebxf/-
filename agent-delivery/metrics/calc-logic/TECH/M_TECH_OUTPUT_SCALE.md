# 技术规模（M_TECH_OUTPUT_SCALE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_OUTPUT_SCALE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_OUTPUT_SCALE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_OUTPUT_SCALE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_OUTPUT_SCALE |
| 指标名称 | 技术规模 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | TECH（技术点体系 / DS-03 技术发展跟踪） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术点气泡图（大小维）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_OUTPUT_SCALE.md` |

## 口径定义

seed 把「技术规模」定义为「成果 + 应用体量」，并明文禁止用论文量、专利量、技术交易额冒充；本库**应用侧四类承载（产品/产值/装机/交易额）全缺**，成果侧只有专利与论文两类且都在禁止之列——因此本文只能交付**专利体量代理**并改名，判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_OUTPUT_SCALE.md` §二（M_TECH_OUTPUT_SCALE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_transfer`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：成果侧可算：378 个技术点中 366 个有专利体量，合计 2380595 件，CR10 27.9%、HHI 150.0，分布非退化（{'S1 超大（≥2万件）': 25, 'S2 大（5千–2万）': 83, 'S3 中（1千–5千）': 164, 'S4 小（200–1千）': 94, 'S5 长尾（<200）': 0}）。但 seed 定义的「应用体量」四类承载（产品/产值/装机/交易额）全部缺失，且 seed 明文禁止以专利量冒名——故只能判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 2.07 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_OUTPUT_SCALE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_OUTPUT_SCALE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_OUTPUT_SCALE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

