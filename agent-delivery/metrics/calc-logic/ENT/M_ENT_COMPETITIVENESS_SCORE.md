# 综合竞争力分（M_ENT_COMPETITIVENESS_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_COMPETITIVENESS_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_COMPETITIVENESS_SCORE |
| 指标名称 | 综合竞争力分 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·企业分析「企业竞争力分析—个性化竞争力评价与输出」（§1.1.1.2.4.2.3.10.2「计算企业综合竞争力得分」；算法库「深圳企业竞争力水平分析模型」§1.1.1.1.1.1.1.5.1 输出「综合竞争力指数」）... |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_COMPETITIVENESS_SCORE.md` |

## 口径定义

无现成「综合竞争力分」结果面（落表 `ads_ent_competitiveness_score` 待建；现网 `enterprise_score` 120 行为 innov/operate/growth 口径禁顶替）→ 非完全直接支持；九个三级指标的原料集中在 gkx `dwd_org_annual_financial_info`（90,926 行），但六项财务/规模指标填充仅 2.4%—3.5%、研发人员全空、本科及以上学历无字段、市场占有率需行业营收汇总（同样依赖低填充营收）——极值归一化对覆盖面敏感，2—4% 覆盖撑不起全国可比的 min/max，人力资源维两指标一空一无 → **部分支持**（表结构在、原料结构性薄，非无法构建）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_COMPETITIVENESS_SCORE.md` §二（M_ENT_COMPETITIVENESS_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `ads_ent_`
- `ads_ent_competitiveness_score`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_rd_achiev_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维九三级指标原料：gkx 财务表 90926 行中资产>0 2.9%、员工>0 3.5%、营收>0 2.4%、利润非空 2.6%、负债>0 2.6%、财务三要素齐 fin3 2.3%；研发人员 development_employee 全空；本科及以上学历人数无字段（待建）；市场占有率需行业营收汇总（同样依赖低填充营收）。极值归一化对填充量敏感——2-4% 覆盖撑不起全国可比 min/max，人力资源维两指标一空一无 → 部分支持（表结构在、原料结构性薄，非无法构建）。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_COMPETITIVENESS_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

