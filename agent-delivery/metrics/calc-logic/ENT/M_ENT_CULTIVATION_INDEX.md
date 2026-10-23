# 培育推荐指数（M_ENT_CULTIVATION_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CULTIVATION_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CULTIVATION_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CULTIVATION_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CULTIVATION_INDEX |
| 指标名称 | 培育推荐指数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·企业分析「培育企业推荐分析」（§1.1.1.2.4.2.3.7）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_CULTIVATION_INDEX.md` |

## 口径定义

本条为**指数本体 MODEL**（三维加权，无现成结果面）；依赖侧三维源表结构全在 gkx（转换入湖可算），但**数据量两维不济**——产业维原料量足可算、政策维缺 GPT 分类模型层、潜力维财务填充 2.4—2.9% 且研发列 `arch_development_am` 全空——三维一可两缺，按 §〇「始终有部分依赖维度数据不足」归**部分支持**（脚本机判一致；先验档「完全转换支持」被实测数据量否决）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CULTIVATION_INDEX.md` §二（M_ENT_CULTIVATION_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_org_product_info`
- `dwd_org_shareholder_info`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维成熟度：①产业相关度原料可算（tags 2283762 行+股东 400286 行图谱边+目录）✅；②政策匹配度缺 GPT 分类框架（政策库 content 96%、企业文本 45011 行 description 71.3%，但行动/话语两型契合的识别模型未建）❌；③企业潜力财务三指标：资产 2.9%、净利润 2.6%、研发投入 arch_development_am 全空、营收 2.4%——低填充+一列空❌。三维一可两缺（GPT 框架未建+财务薄）→ 部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CULTIVATION_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CULTIVATION_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CULTIVATION_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

