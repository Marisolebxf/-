# 市场份额（M_ENT_MARKET_SHARE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_MARKET_SHARE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_MARKET_SHARE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_MARKET_SHARE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_MARKET_SHARE |
| 指标名称 | 市场份额 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／企业评价／市场地位 |
| 更新频率 | 年度 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 企业画像「市场份额」卡、行业集中度分析｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2014] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_MARKET_SHARE.md` |

## 口径定义

分子营收只覆盖 0.734% 企业且止于 2014 年，分母（市场规模/产业产值）全库不存在，链内样本试算因分母漂移被否决，判完全不支持。

## 计算逻辑说明

```text
share_i = revenue_i / market_size(产品×区域×年)；本件缺 market_size
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_MARKET_SHARE.md` §二（M_ENT_MARKET_SHARE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_finance_annual`
- `dwd_org_finance_stock`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：市场份额的分母（市场规模/行业产值/第三方市占率）在 gkx 完全没有来源，chain_market 表不存在；分子侧只有 0.73% 的企业有营收（1,388/189,116），且集中在上市公司。分母无源、分子极稀疏，比率不成立。链内样本份额试算已做，但其分母是样本营收而不是市场规模，属构造性偏差，明确否决。故判完全不支持，只写需求与恢复路径。
- **基期声明**：分子基准年取 2014（有效企业最多的年份，752 家）；2025 只有 34 家，属残年，不用它做试算。全期去重 1388 家。年份不是本件的瓶颈，分母缺失才是：即使补齐十年营收，没有市场规模仍然算不出份额，故 base_years_missing 留空而不是列一串年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_MARKET_SHARE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_MARKET_SHARE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_MARKET_SHARE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

