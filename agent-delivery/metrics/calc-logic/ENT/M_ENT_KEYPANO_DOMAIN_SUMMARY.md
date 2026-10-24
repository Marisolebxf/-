# 领域摘要（M_ENT_KEYPANO_DOMAIN_SUMMARY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_DOMAIN_SUMMARY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_DOMAIN_SUMMARY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_DOMAIN_SUMMARY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEYPANO_DOMAIN_SUMMARY |
| 指标名称 | 领域摘要 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·重点企业全景（全景页面两支柱之汇总面）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_KEYPANO_DOMAIN_SUMMARY.md` |

## 口径定义

无现成「领域摘要」结果面 → 非完全直接支持；王惠五步法中断在两环——链位归集环断（`chain_info.level` 1,273 行全 0，上/中/下游分组键无从取值）与领域映射环断（库内无关键词→产业链细分领域映射表，王惠 calc-logic 自标「未建」），而文本源环在（专利 294 万且 keywords 填充率 100%、中文论文 100,900 篇+作者单位 23,327 机构，但英文侧仅 1,387 篇、专利摘要表仅 20,000 行）→ 按第 4 档定义归**部分支持**（脚本机判一致）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_DOMAIN_SUMMARY.md` §二（M_ENT_KEYPANO_DOMAIN_SUMMARY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_patent`
- `dwd_patent_abstract`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠五步法逐环实测（三方库 gkx）：①链位归集断——chain_info.level 全 0（分布 [{'level': 0, 'n': 1273}]），上/中/下游分组键无从取值，且 tags×chain_info 关联 0 行（链路码体系不匹配）；②文本源在——专利 2,939,895 行且 keywords 列样本填充率 100.0%，论文 zh 100900 篇 + 作者单位 23327 机构（名称可对齐企业），但英文侧仅 1387 篇、专利摘要表 20000 行；③领域映射断——库内无关键词到产业链细分领域映射表（无），王惠 calc-logic 自标「映射规则表（未建）」。五步中断在 1/3 两环 → 部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_DOMAIN_SUMMARY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_DOMAIN_SUMMARY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_DOMAIN_SUMMARY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

