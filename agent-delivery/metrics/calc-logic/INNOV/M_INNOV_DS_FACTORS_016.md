# 要素聚类分析（M_INNOV_DS_FACTORS_016）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_016.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_016.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_016_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_FACTORS_016 |
| 指标名称 | 要素聚类分析 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技信息展示系统） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科技全域态势 → 要素聚类分析 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_FACTORS_016.md` |

## 口径定义

开发库无「要素聚类」结果面 → 非完全直接支持；`gkx` 侧项目（58,453）、期刊（3,401）、专利（价值维 199 万非空）三类可入集，**会议类实体全库 0 条**（四张出版物表的 `publication_type` 无会议枚举）→ 四类只聚三类；且三类的影响力分本身是降级口径（期刊缺影响指数、专利缺被引维、项目缺参与机构维），K-Means 在「类型独热 + 降级分」上跑出的簇几乎等于类型标签本身 → 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_016.md` §二（M_INNOV_DS_FACTORS_016.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_journal`
- `dwd_en_paper`
- `dwd_en_project`
- `dwd_id`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_zh_journal`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠口径要求会议 / 项目 / 专利 / 期刊四类要素入集，gkx 会议类实体 0 条（publication_type 无会议枚举），四类仅得三类；且专利影响力退化为价值单维、项目参与机构数维退化、期刊影响指数缺测。聚类算法本身可跑通并产出簇标签与规模（K=4，轮廓系数 0.8811），但要素集不完整，故判部分支持。
- **基期声明**：聚类为截面结构分析，输入是库内全量要素特征矩阵，不做逐年切片、不做增速或同比，因此无基期分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_016.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_016.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_016_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

