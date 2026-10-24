# 技术基础能力分析（M_TECH_BASE_96_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_BASE_96_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_BASE_96_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_BASE_96_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_BASE_96_1 |
| 指标名称 | 技术基础能力分析 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术／技术基础 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 技术基础能力页的 11 个卡片（论文 4 张、专利 4 张、交易 2 张、资讯 1 张） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_BASE_96_1.md` |

## 口径定义

11 维里 3 维直接、4 维代理、4 维无源。代理维能出数但口径降级，无源维连降级都不能，因此既有可交付内容、又始终补不齐，按 §〇 落**部分支持**，不上抬到「完全转换支持」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_BASE_96_1.md` §二（M_TECH_BASE_96_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`
- `dwd_deal`
- `dwd_industry_chain_news_info`
- `dwd_patent`
- `dwd_patent_transfer`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：11 子指标中专利计数与深圳/区域专利维可直接出数（主分类 IPC4 2,420,915 件、2024 深圳 275,908 件），论文维只能给「学科上界 + 机构代理」两套降级读数；前沿机构质量维因影响因子列缺失、download_num 整列 0、论文级被引 ID 不通而不可算；技术交易额两维无技术合同登记表（dwd_deal 10 行无金额、dwd_patent_transfer 无成交价、dwd_bid_base_out 是招投标买方口径），技术动态资讯维无技术域标签。始终存在无法补齐的依赖维，故落部分支持，不抬档。
- **基期声明**：专利窗口 2021—2026（dwd_patent.apdt_year 仅此六年，2017—2020 零行，不补 0、不摊入分母）；2026 为残年（69,747 件，约为 2025 的 20.4%），只做端点披露、不用于增速。论文侧 cover_year_start 跨 2001—2026，但学科标注那 20,048 篇没有年份字段，故论文不做域×年双轴序列。城市专利分布窗口为 2021—2024（缓存决定的四年）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_BASE_96_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_BASE_96_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_BASE_96_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

