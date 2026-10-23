# 产业链关联产品数（M_CHAIN_PRODUCT_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PRODUCT_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PRODUCT_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PRODUCT_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_PRODUCT_COUNT |
| 指标名称 | 产业链关联产品数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链详情页「产品」区标题（「本链关联 N 个产品」）+ 产品云入口 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_PRODUCT_COUNT.md` |

## 口径定义

产品标签表 `gkx.dwd_org_industry_product_tags` 当日 **80,258 行**，拆项后得 **724,960 个产品条目**、去重 **221,945 个**、覆盖 **78,838 家企业**；但 `INB1209`/`INB1236`/`INB2503` 三条链在 `industry_link_name` 中**零行**（SQL 实测），且产品条目无行业标准编码、同物异名严重 → 覆盖缺 3/12、口径不可跨链比较，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PRODUCT_COUNT.md` §二（M_CHAIN_PRODUCT_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_industry_product_tags`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：产品标签表 80,258 行真实可取，拆项后 9/12 条链有产品；但 INB1209/INB1236/INB2503 在产品表 industry_link_name 中零行（SQL 实测），且产品条目无行业标准编码、同物异名严重、不做归并则不可跨链比较——覆盖与口径两侧都有缺口。
- **基期声明**：口径明确「无时间窗」，产品标签表也没有年份字段，故不设统计期、不做年度序列。
- **复现实测耗时**：约 2.9 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PRODUCT_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PRODUCT_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PRODUCT_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-24: 初版 v0.1.0（表名漂移稿）
- 2026-10-14: v0.2.0 口径重写（human:徐滕强 拍板：直数/等值匹配/无窗口/字面去重）
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

