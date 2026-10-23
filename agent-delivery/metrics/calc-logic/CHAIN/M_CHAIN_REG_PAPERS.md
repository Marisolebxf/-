# 高校论文（区域）（M_CHAIN_REG_PAPERS）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_PAPERS.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PAPERS.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PAPERS_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_PAPERS |
| 指标名称 | 高校论文（区域） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN（产业链区域指数） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链区域指数 → 学术生态竞争力 → 区域论文数 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_PAPERS.md` |

## 口径定义

论文表能提供作者机构、标题、学科分类，但没有产业链字段，机构也没有链码；把机构落城后覆盖 40.68%，再用标题与学科关键词代理链归属只能命中 11.76%，且 2024 年单年占全表 32.09%（采集批次偏斜）→ 区域维基本闭合、链维是文本代理 → **部分支持**。本档位与 `code/M_CHAIN_REG_PAPERS_out.json` 的 `support_judgment.data_support_level` 一致。

## 计算逻辑说明

```text
Papers(c,r)=Σ_p 1{机构(p)∩r≠∅ ∧ chain_token(p)=c}，一篇可命中多条链
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_PAPERS.md` §二（M_CHAIN_REG_PAPERS.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：区域维闭合：100,900 篇中文论文的作者机构串 100% 非空，41,044 篇（40.68%）至少 1 位作者机构可落到 4 市，高校论文 77,712 篇（77.02%）；链维只能靠标题/分类关键词代理，命中 11,866 篇（11.76%），48 个链×城单元 44/48 非零，但 4 个单元为 0 且论文数区间 0—978 跨三个数量级。因为论文表没有任何产业链字段、机构也没有链码，链归属是文本代理而非数据字段，且 2024 年论文占全表 32.09%（采集偏斜），不能当作年度趋势，故判部分支持。
- **基期声明**：由产物中实际出现的年度键反推：used=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 0.06 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_PAPERS.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PAPERS.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PAPERS_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

