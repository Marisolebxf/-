# 商业力得分（M_ENT_BUSINESS_POWER_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_BUSINESS_POWER_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_BUSINESS_POWER_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_BUSINESS_POWER_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_BUSINESS_POWER_SCORE |
| 指标名称 | 商业力得分 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·企业分析「企业商业力评估对比分析」页面（评分/排名/雷达对比）｜ **数据支持度**：**部分支持**｜ wanghui：true（王惠定义过，§五必含对照） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_BUSINESS_POWER_SCORE.md` |

## 口径定义

live ADS `biz_power` 120 行为样例级（org 与主档 JOIN=0）→ 非完全直接支持；六维中**市场（营收填充 2,095/90,926=2.3%）、品牌（声量可算但荣誉语义待核）、技术合作（专利可解析但专家人月无字段）三维为「低覆盖或半缺」**，**产品/产业链覆盖率/关键环节参与度三维依赖的 `dwd_org_industry_chain_dtl` 在 gkx 与 live 均不存在**，另有 4 个王惠标注待建字段——「始终有部分依赖维不闭合」→ **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_BUSINESS_POWER_SCORE.md` §二（M_ENT_BUSINESS_POWER_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `ads_ent_business_score`
- `dwd_industry_chain_info`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_important_news_info`
- `dwd_org_industry_chain_dtl`
- `dwd_org_industry_tags`
- `dwd_org_org_product_info`
- `dwd_org_tech_tag`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：六维中：市场维财务填充率低（2095/90,926，2.3%）；产品/产业链覆盖/关键环节三维依赖的 dwd_org_industry_chain_dtl 在 gkx（及 live）均不存在（gkx industry_chain_info=1,273 仅链定义，无企业×节点关联）；品牌维资讯 1,668,414 行可算声量、tech_tag 202,424 待核荣誉语义；技术合作维专利 2,939,895 行可解析联合申请、外部专家人月无字段。4 个待建字段 + 1 张关键表缺失 → 始终有依赖维不闭合 → 部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_BUSINESS_POWER_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_BUSINESS_POWER_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_BUSINESS_POWER_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

