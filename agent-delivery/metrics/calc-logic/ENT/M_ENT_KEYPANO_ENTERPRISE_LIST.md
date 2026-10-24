# 企业清单（当前链位）（M_ENT_KEYPANO_ENTERPRISE_LIST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_ENTERPRISE_LIST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_ENTERPRISE_LIST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_ENTERPRISE_LIST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEYPANO_ENTERPRISE_LIST |
| 指标名称 | 企业清单（当前链位） |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 重点企业全景 → 选定产业链与链位后的企业列表 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_KEYPANO_ENTERPRISE_LIST.md` |

## 口径定义

成员表的三块拼图里，**上链边**是最硬的一块：`dwd_org_industry_tags` 2,283,762 行、去重后覆盖全国 31—32 个省级行政区，按 `credit_code` 去脏（2 行非 18 位）后可直接连接。**名单**与**链位**两块都不在库里：前者 280 张表零命中，只能用专利授权≥50 的 4,561 家代理；后者 `dwd_org_industry_tags` 15 个列里没有 `node_stage`，`dwd_industry_chain_info.level` 1,273 行全 0，只能把 41 个一级环节按产业位置手工归到上/中/下游。一块直取、两块自建，按 §〇 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_ENTERPRISE_LIST.md` §二（M_ENT_KEYPANO_ENTERPRISE_LIST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_id`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_important_news_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：成员表结构可算：上链边（dwd_org_industry_tags，2,283,762 行）在，链位可由一级环节码映射，区域/资质只在查询时 JOIN，公式可完整执行，实出 31 个链×链位格、5,196 行成员、2,105 家企业。但两条依赖不可靠：①名单是代理——gkx 280 张表按 keypano/key_/important/focus/star/honor/roster 八个模式扫描只命中 dwd_org_important_news_info（新闻表，非名单），没有「重点企业」名单表，只能用专利授权≥50 的 4,561 家代理；②链位是自建映射——dwd_org_industry_tags 15 列无 node_stage，dwd_industry_chain_info.level 1,273 行全 0，只能把 41 个一级环节手工归到上/中/下游。名单与链位两维都不在库里，故判部分支持，不抬档。
- **基期声明**：截面件：名单按专利授权累计量（>=50）一次性截取，上链关系、链位、区域、资质均无年度键，产物与参数中不存在年份窗口，故 used/missing 均为空。不是「缺年按 0 摊入」的情形，也不得用 created_time 反推年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_ENTERPRISE_LIST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_ENTERPRISE_LIST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_ENTERPRISE_LIST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

