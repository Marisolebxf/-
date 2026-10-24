# 潜在科技发展方向预警（M_INNOV_DS_09_COMPREHENSIVE_008）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_COMPREHENSIVE_008.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_COMPREHENSIVE_008.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_COMPREHENSIVE_008_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_09_COMPREHENSIVE_008 |
| 指标名称 | 潜在科技发展方向预警 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统·科技发展态势·科技发展规划·综合发展规划（ |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·科技发展态势·科技发展规划·综合发展规划（SRS 序号 184） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_09_COMPREHENSIVE_008.md` |

## 口径定义

六源中专利与产业两源在 2021–2026 全覆盖且可直接算增速；论文源因关键词表仅覆盖 0.79% 而降级为题名匹配；政策源的 `keywords/theme` 为字面 `'NULL'`（真实值 0/2 行），只能退为题名匹配；项目源有真实关键词但覆盖止于 2021；人才源 `fields` 为英文短语，与中文 IPC 锚点无法对齐，**完全不可算** → **部分支持**。（20261021 改源版：六源全部改读三方库 `gkx`，不再连本项目自建 `ods` 面；算法与窗口未改。）

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_COMPREHENSIVE_008.md` §二（M_INNOV_DS_09_COMPREHENSIVE_008.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`
- `dwd_scholar`
- `dwd_scholar_research_direction`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠六源中，专利与产业两源（IPC4 申请量、IPC4 活跃申请人）在 2021-2026 全覆盖、可直接算增速；论文与政策两源可借助方向锚点以题名匹配近似；项目源有真实关键词与立项年可命中；但 ①政策 keywords/theme 为字面 'NULL'（按 UPPER(TRIM()) 口径复核，真实值仍为 0/20,000 与 2/20,000），只能退为题名匹配；②论文关键词表 gkx.dwd_zh_paper_classification 与论文主表 JOIN 仅命中 799 篇（0.79%），论文维只能退为题名匹配；③人才源 gkx.dwd_scholar_research_direction 的 fields 为英文短语，无法与中文 IPC 锚点对齐，本批次完全无法计算。六源少一源、两源降级为代理，故判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_COMPREHENSIVE_008.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_COMPREHENSIVE_008.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_COMPREHENSIVE_008_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

