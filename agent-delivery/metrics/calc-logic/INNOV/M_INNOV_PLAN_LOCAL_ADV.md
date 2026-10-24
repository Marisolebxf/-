# 地方优势方向（M_INNOV_PLAN_LOCAL_ADV）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_LOCAL_ADV.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_LOCAL_ADV.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_LOCAL_ADV_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_LOCAL_ADV |
| 指标名称 | 地方优势方向 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技发展规划页「全球热点技术捕捉」——属地技术方向比较优势视图 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PLAN_LOCAL_ADV.md` |

## 口径定义

无「地方优势方向」现成表 → 非完全直接支持；专利维可算，但**参照池不是全国、更不是全球**，而是「可回连申请人底册的国内专利池」，且底册本身深圳占 50.5% → LQ 绝对值被结构性抬高，判**部分支持**。

## 计算逻辑说明

```text
{'lq': 'LQ_d=(L_d/L_total)/(A_d/A_total)', 'composite': 'LQ_comp=几何平均(可得维)', 'normalize': 'LQ_norm=LQ_comp/0.7508（截面几何均值）', 'threshold': 'LQ_norm>1 优势；≥1.5 强优势；仅专利单维 LQ>1 作对照'}
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_LOCAL_ADV.md` §二（M_INNOV_PLAN_LOCAL_ADV.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：448 类方向可算出非退化 LQ（专利/申请人/论文三维），但需求要求的「与全球水平对比」在本库没有全球分母（现有分母是国内专利池，深圳占池 4 成以上是名称宇宙的结构性偏高）；创新资源维只能用活跃申请人代理，论文维依赖 Top-1 22.14% 的术语桥
- **基期声明**：专利/申请人/论文均取 2021—2024（dwd_patent 的 apdt_year 只有 2021—2026，2017—2020 零行）；LQ 是同期份额比，不跨期，但不得把缺失年按 0 摊入任何趋势分母。
- **复现实测耗时**：约 26.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_LOCAL_ADV.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_LOCAL_ADV.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_LOCAL_ADV_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

