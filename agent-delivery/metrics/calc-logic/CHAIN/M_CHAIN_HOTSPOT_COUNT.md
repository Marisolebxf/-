# 热点/历程事件数（热点领域数）（M_CHAIN_HOTSPOT_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOTSPOT_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_HOTSPOT_COUNT |
| 指标名称 | 热点/历程事件数（热点领域数） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 更新频率 | 周 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_HOTSPOT_COUNT.md` |

## 口径定义

热点领域数 = 在可评估 L1 中，企业增速、投融资热度、专利密度三信号min-max 归一加权后综合分 >= 0.60 的环节去重数；对象是环节，不是资讯条数

> 一句话口径（源件 §0.3）：按“企业增速 + 投融资热度 + 专利密度”三信号、在 28 个达到证据门槛的 L1 环节上做 min-max 加权，综合分 ≥ 0.60 的热点领域是 **2 个**——人工智能/技术层（0.6749）与低空经济/低空制造业（0.6172）；阈值降到 0.55 会变成 3 个、升到 0.65 只剩 1 个，说明“热点数”对自定义阈值高度敏感，判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOTSPOT_COUNT.md` §二（M_CHAIN_HOTSPOT_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`
- `dwd_org_industry_chain_pat_dtl`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件回答“12 条产业链里有哪些环节正在变热”。按 `calc-logic` 的三路信号：企业增速（2021—2025 成立企业占比）、投融资热度（2021—2025 融资事件/可映射企业）、专利密度（累计专利/可映射企业），在 28 个达到证据门槛的 L1 上做 min-max 归一，按 0.34/0.33/0.33 加权，综合分 ≥ 0.60 记为热点。
- **基期声明**：增速与融资取 2021—2025 五年窗口；2026 为残年（链内仅 5 家新成立、融资 238 笔），不进取数窗口；专利为累计存量，不分年

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOTSPOT_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

