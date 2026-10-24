# 热点区域自动识别与预警（M_INNOV_DS_27_SPATIO_003）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_27_SPATIO_003.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_003.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_003_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_27_SPATIO_003 |
| 指标名称 | 热点区域自动识别与预警 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技时空演进展示） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技成果展示 → 科技时空演进展示 → 全球研究主体地域时空分布展示 → 热点区域自动识别与预警 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_27_SPATIO_003.md` |

## 口径定义

开发库无「热点区域/预警等级」结果面 → 非完全直接支持；区县级**专利**信号结构齐全、可对齐率 72.68%（2021-2024 共 176.2 万件落区县），可现算出密度、热点与预警分级；但王惠口径中的**论文**信号在区县级几乎全失配（20.94%，且窗口内仅 339 条作者-单位实例）、**项目**信号对齐 18.59%，两维实质缺失 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_27_SPATIO_003.md` §二（M_INNOV_DS_27_SPATIO_003.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_en_author`
- `dwd_en_paper`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_research_institute_base_info`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：区县级专利信号可建（2021-2024 专利申请人名与机构名录精确对齐 72.68%），热点识别与预警分级可跑通；但论文信号仅 20.944% 可对齐到机构（论文语料为全国高校院所，机构名录以广东企业为主），项目信号对齐 18.59%，故王惠口径中的「论文/项目」两维在区县级实际缺失，密度退化为专利主导 → 判部分支持。
- **基期声明**：由产物中实际出现的年度键反推：used=[2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_27_SPATIO_003.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_003.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_003_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

