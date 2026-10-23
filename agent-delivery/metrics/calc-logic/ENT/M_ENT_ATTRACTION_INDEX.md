# 招引推荐指数（M_ENT_ATTRACTION_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_ATTRACTION_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACTION_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACTION_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_ATTRACTION_INDEX |
| 指标名称 | 招引推荐指数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·企业分析「招引企业推荐分析」（§1.1.1.2.4.2.3.6）与算法库「招引企业综合推荐模型」（§1.1.1.1.1.1.1.5.7）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_ATTRACTION_INDEX.md` |

## 口径定义

无现成「招引推荐指数」结果面（live 侧 `enterprise_recommend_summary` 等均未建）→ 非完全直接支持；三维中「深圳连接度」的中心度子项可由投资/股东边代理现算（scored 95,652 节点、50,358 家含深圳连接），但「产业相关度」的产业链融入度依赖 `industry_link_code` 链路码与中国投入产出表（两库皆无；gkx 侧 tags 虽有全量 2,283,762 行、链路码样本填充率高，但与 `dwd_industry_chain_info` 关联实测 0 行，链路码体系不匹配）、「政策匹配度」的 GPT 文本契合层未建、「深圳连接度」的引力模型子项缺人口/GDP/距离数据——**三维中有依赖维始终缺数据** → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_ATTRACTION_INDEX.md` §二（M_ENT_ATTRACTION_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_invest_info`
- `dwd_org_org_product_info`
- `dwd_org_shareholder_info`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维中：产业相关度 tags 已由 gkx 全量承载（2,283,762 行），但链路码与 dwd_industry_chain_info 关联仅 0 行（20 万行样本口径）、投入产出表缺失，产业链融入度仍不可闭合；政策匹配度有政策文本（20,000）与企业文本（45,011）但 GPT 契合层未建（keywords 填充 3000）；深圳连接度可用投资/股东边代理中心度（scored=95652，含深圳连接企业 50358），但引力模型子项缺人口/GDP/距离。始终有依赖维数据不足 → 部分支持。库存自校验：True
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_ATTRACTION_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACTION_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACTION_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

