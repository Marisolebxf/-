# 全球成功案例匹配（M_CHAIN_GLOBAL_CASE_MATCH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GLOBAL_CASE_MATCH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_CASE_MATCH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_CASE_MATCH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_GLOBAL_CASE_MATCH |
| 指标名称 | 全球成功案例匹配 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链对标／全球案例 |
| 更新频率 | 年度 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 链路对标页「全球案例」卡片、产业链招商参考｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_GLOBAL_CASE_MATCH.md` |

## 口径定义

全库 280 张表无任何案例库：7 张 case 表全是司法/破产案件，外资名录无产业结构，专利国家码只到国别；案例、链映射、成功判据三件全缺，判完全不支持。

## 计算逻辑说明

```text
match(本地链, 全球案例) = 产业结构余弦相似度 × 成功判据过滤；本件缺案例库与成功判据
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GLOBAL_CASE_MATCH.md` §二（M_CHAIN_GLOBAL_CASE_MATCH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_forg_research_org_info`
- `dwd_opt_judicial_case_detail`
- `dwd_org_bankruptcy_public_cases`
- `dwd_patent`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：全库没有案例库（280 张表里 case/benchmark 类为 0），唯一境外实体是外资企业名录 6 张各 2 万行，但它与链标签零重叠（extid/name/orgid 三项命中均为 0），挂不上任何一条链；「成功」没有判据表，案例级营收/份额/增速序列都不存在。案例库、链归属、成功判据三项全缺，无法闭环，判完全不支持。
- **基期声明**：没有案例库就没有案例年份；本件不产出任何年度序列，used/missing 为空表示「无时间维可挂」，不是「缺年补 0」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GLOBAL_CASE_MATCH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_CASE_MATCH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_CASE_MATCH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

