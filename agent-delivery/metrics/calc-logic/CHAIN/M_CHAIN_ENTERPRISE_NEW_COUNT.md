# 新增关联企业数（M_CHAIN_ENTERPRISE_NEW_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_ENTERPRISE_NEW_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_NEW_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_NEW_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_ENTERPRISE_NEW_COUNT |
| 指标名称 | 新增关联企业数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 二级模块 | 产业链全景 / 全景概览 |
| 更新频率 | 日 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_ENTERPRISE_NEW_COUNT.md` |

## 口径定义

官方口径要求“该年首次挂链企业数”，时间轴是 `first_link_date`；gkx 既没有这张明细表，也没有这个字段，`created_time` 全表 2,283,762 行只有 1 个取值（2026-08-27 11:08:26），无法分年。因此本件判 **完全不支持**，交付值是“不可得”，不是“0 家”；同时给出“当年成立且当前在链”的代理观察 3,627 家（2021—2025），仅用于说明缺口量级，不充作指标。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_ENTERPRISE_NEW_COUNT.md` §二（M_CHAIN_ENTERPRISE_NEW_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：本件回答“每年有多少家企业第一次挂上产业链”。官方口径在 2026-10-14 已拍板：按 `first_link_date` 取每年最早挂链时间，按 `org_id` 去重，退出后重挂不计。
- **基期声明**：官方口径以 first_link_date 分年，该字段不存在，无法确定基期；代理观察用成立年 2021—2025（2026 仅 5 家，作残年单列，不进取数窗口）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_ENTERPRISE_NEW_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_NEW_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_NEW_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-14: 0.2.0 新建口径钉死（首挂年归集 + 重挂不计 + 分链链内首挂）；开 CHAIN-P0-5；临时方案入运营注记。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

