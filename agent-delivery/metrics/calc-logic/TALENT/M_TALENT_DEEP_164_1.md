# M_TALENT_DEEP_164_1（M_TALENT_DEEP_164_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_164_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_164_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_164_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DEEP_164_1 |
| 指标名称 | M_TALENT_DEEP_164_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才洞察页「外部候选人推荐榜 + 匹配分析卡」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DEEP_164_1.md` |

## 口径定义

外部候选人 20,183 人中，学术力 100% 可算、所属机构专利 17,093 人（84.70%）可算、深圳连接度只有 468 人（2.32%）有任何信号，其中 82 人强于 0.4；需求点名的「产品匹配度」在招聘表与产品标签表都无法落地，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_164_1.md` §二（M_TALENT_DEEP_164_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_product_tags`
- `dwd_org_recruit_info`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_scholar_work_experience`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：学术力（20,183 人全覆盖）、产业力（机构专利 17,105 人 = 84.75%）、深圳连接度（合著 465 人 / 履历 19 人）三维可算，但需求点名的「产品匹配度」没有数据：招聘表只有岗位名与工作地、无技能要求，产品标签表的 credit_code 与机构底册只有 3.5% 交集，无法逐人匹配；深圳连接度有合著信号的人只占 2.30% → 部分支持。
- **基期声明**：截面口径：学术力取生涯累计两列，深圳连接度取全时段合著与履历，不含年度窗口，故无基期年份。合著信号来自中文论文面板（1980—2026），但本件不按年切分、不做增速，2017—2020 不参与任何分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_164_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_164_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_164_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

