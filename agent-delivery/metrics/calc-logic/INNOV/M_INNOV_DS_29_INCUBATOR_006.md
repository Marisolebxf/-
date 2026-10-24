# 影响力评价（孵化/众创载体）（M_INNOV_DS_29_INCUBATOR_006）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_29_INCUBATOR_006.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_29_INCUBATOR_006.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_29_INCUBATOR_006_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_29_INCUBATOR_006 |
| 指标名称 | 影响力评价（孵化/众创载体） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技专题服务系统） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统 → 科技专题内容运营中心 → 服务机构管理 → 孵化载体影响力评价 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_29_INCUBATOR_006.md` |

## 口径定义

开发库无「载体影响力评分」结果面 → 非完全直接支持；三维中**创新产出维**与**在孵规模维**可由 `dwd_org_subsidiary_info` + `dwd_patent` + `dwd_zh_author` 直接算出（已实测 **184 家**载体入集、73 家可测在孵规模、38 家有专利产出；名称含关键词但无资质标签的 81 家只登记不评分）；但**服务能力维**王惠要求「高企子公司数 + 载体高企标记」，子公司 `org_id` 与机构名录属不同 ID 命名空间（JOIN 命中 0），只能退化为「载体自身高企标签」，且载体池仅 184 家（限广东四市）→ **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_29_INCUBATOR_006.md` §二（M_INNOV_DS_29_INCUBATOR_006.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_author`
- `dwd_en_paper`
- `dwd_org_base_info`
- `dwd_org_subsidiary_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：载体可入集 184 家（仅取科技企业孵化器/众创空间真实资质标签，名称关键词命中但无标签的 81 家只登记不评分），创新产出维与高企服务能力维可直接算；但在孵规模维仅 73 家（39.7%）能以名称对齐子公司表，且子公司侧无法回连企业名录做高企核验；王惠口径的三维中一维（在孵规模）覆盖不足、一维（高企覆盖）语义被削弱（仅载体自身标签）→ 判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_29_INCUBATOR_006.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_29_INCUBATOR_006.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_29_INCUBATOR_006_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

