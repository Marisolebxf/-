# M_TALENT_DEEP_163_1（M_TALENT_DEEP_163_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_163_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_163_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_163_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DEEP_163_1 |
| 指标名称 | M_TALENT_DEEP_163_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才洞察页「产业力指数 + 企业榜 + 深圳切片」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DEEP_163_1.md` |

## 口径定义

深圳 95,600 行企业底册中，77,529 家有专利申请人记录、合计 1,300,219 件（占全表 2,939,895 件的 44.23%），59,645 家有 IPC 小类覆盖（76.93%），两维可全量打分；第三维媒体声量受「1,668,414 行新闻表按名称计数」的算力限制，只能对专利 TOP60 取数（58 家命中），且无去重、无情感，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_163_1.md` §二（M_TALENT_DEEP_163_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_important_news_info`
- `dwd_org_industry_product_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：企业影响力（专利件数）与产业覆盖度（IPC 小类数）在 77,529 家深圳企业上可算，两维相关系数 0.78；但媒体知名度只能在专利 TOP60 的 58 家上取数（新闻表 1,668,414 行按名称计数需逐名过滤，全池 7.7 万家不可行），且新闻条数含转载/重复、无情感与去重，只能作头部相对声量；IPC 缓存覆盖 76.93%、深大等机构口径偏低 → 部分支持。
- **基期声明**：专利件数是 `dwd_patent` 全表按申请人聚合的结果，而该表只有 2021—2026 的申请年，因此这是「2021 年起可观测窗口」的累计，不是企业生涯专利总量；2026 为残年（全表 74,810 件），计入但未单独拆年。2017—2020 表中零行（陷阱 3.13），不进分母、不按 0 摊入。IPC 覆盖数与新闻条数同为当前快照截面，不做年度增速。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_163_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_163_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_163_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

