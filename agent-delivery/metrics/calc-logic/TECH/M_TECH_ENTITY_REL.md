# 实体关联关系网（M_TECH_ENTITY_REL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_REL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_REL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_REL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_ENTITY_REL |
| 指标名称 | 实体关联关系网 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 · 技术评估 · 创新主体关系网络（企业/高校/院所之间的合作、转移、合著关系） ｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_ENTITY_REL.md` |

## 口径定义

「实体关联关系网」在库内**没有结果表**，依赖侧则**部分足、部分缺**：`dwd_patent_transfer`（转移 22,809 行）、`dwd_patent_applicants`（共同申请）、`dwd_zh_paper`（论文合著）三源可现转出 **30,704 个实体节点 / 39,055 条唯一边 / 66,136 条边实例**（转移 27,024、合著 23,756、共申 15,356 实例），度分布 p50=2、p90=4、max=66；但需求所含的**引用边**（`dwd_patent_cited` 仅 0.70%、`cited_by` 多为 `'null'`）、**许可边**（法事件 2/2000）、**诉讼边**（0/2000）均无可用量，**始终缺一类以上关键边**，按四档口径落 **部分支持**（out.json `support_judgment` 同档）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_REL.md` §二（M_TECH_ENTITY_REL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent_applicants`
- `dwd_patent_cited`
- `dwd_patent_transfer`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「实体关联关系网」在库内**没有结果表**，依赖侧则**部分足、部分缺**：`dwd_patent_transfer`（转移 22,809 行）、`dwd_patent_applicants`（共同申请）、`dwd_zh_paper`（论文合著）三源可现转出 **30,704 个实体节点 / 39,055 条唯一边 / 66,136 条边实例**（转移 27,024、合著 23,756、共申 15,356 实例），度分布 p50=2、p90=4、max=66；但需求所含的**引用边**（`dwd_patent_cited` 仅 0.70%、`cited_by` 多为 `'null'`）、**许可边**（法事件 2/2000）、**诉讼边**（0/2000）均无可用量，**始终缺一类以上关键边**，按四档口径落 **部分支持**（out.json `support_judgment` 同档）。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_REL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_REL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_REL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

