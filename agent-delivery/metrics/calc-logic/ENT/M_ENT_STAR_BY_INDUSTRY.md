# 明星企业行业分布（M_ENT_STAR_BY_INDUSTRY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_BY_INDUSTRY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BY_INDUSTRY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BY_INDUSTRY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_STAR_BY_INDUSTRY |
| 指标名称 | 明星企业行业分布 |
| 所属域 | ENT（企业分析） |
| 一级模块 | ENT（企业主体） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 智慧服务门户·企业发展·明星企业介绍／重点企业领域统计 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_STAR_BY_INDUSTRY.md` |

## 口径定义

明星企业（代理）= 真实专利授权数≥50 的企业；行业 = gkx.dwd_org_base_info.industry_l1_name/l2_name

> 一句话口径（源件 §0.3）：行业字段本身 100% 覆盖代理名单（4,561/4,561），聚合逻辑可跑通；但**分子（明星名单）是专利阈值代理**、**行业是工商登记行业而非实际业务**、**底册 99.82% 在广东**——三重代理叠加，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_BY_INDUSTRY.md` §二（M_ENT_STAR_BY_INDUSTRY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `ads_ent_star_industry`
- `dwd_id`
- `dwd_org_base_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：行业字段本身 100% 覆盖代理名单（4,561/4,561），聚合逻辑可跑通；但**分子（明星名单）是专利阈值代理**、**行业是工商登记行业而非实际业务**、**底册 99.82% 在广东**——三重代理叠加，故判 **部分支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_BY_INDUSTRY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BY_INDUSTRY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BY_INDUSTRY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

