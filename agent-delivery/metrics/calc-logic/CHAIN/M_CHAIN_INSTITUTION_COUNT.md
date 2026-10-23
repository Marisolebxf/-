# 关联机构数（M_CHAIN_INSTITUTION_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INSTITUTION_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INSTITUTION_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INSTITUTION_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_INSTITUTION_COUNT |
| 指标名称 | 关联机构数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链总览／创新载体 |
| 更新频率 | 建议年度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「关联机构」计数卡、链内载体年度新增曲线｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_INSTITUTION_COUNT.md` |

## 口径定义

5,575 家机构底册按成立年可数，但链归属只有 134 家（2.4%）能靠名称匹配上，10 条链有值、2 条链为 0，判部分支持。

## 计算逻辑说明

```text
链内机构成立数 = COUNT(DISTINCT 机构) WHERE 机构名命中链上环节名，按成立年 GROUP BY；环比 = 当年/上年-1
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INSTITUTION_COUNT.md` §二（M_CHAIN_INSTITUTION_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_heis_info`
- `dwd_research_institute_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：chain_institution_stat 结果面不存在，但需求要的「每年成立数 + 环比」在两张真实底册上可直接算：院所 2,074 行（1,996 行有成立日期）与高校 3,501 行（带 est_year）都有年份字段，按年 GROUP BY 即可。缺的是链归属：机构表没有任何产业标签，只能靠机构名匹配环节名，命中率 4.2%，因此链级数字是下限。结构与主键齐、年份齐、链维弱，判部分支持。
- **基期声明**：院所成立年取 incorporation_date 的年份（1,996/2,074 有值，78 行空值不进任何年，不摊 0）；高校取 est_year。窗口 2016—2025，2026 为残年（22 家）不入窗口。未命中年份的机构在「未归属」桶，不按比例摊派到链。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INSTITUTION_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INSTITUTION_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INSTITUTION_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

