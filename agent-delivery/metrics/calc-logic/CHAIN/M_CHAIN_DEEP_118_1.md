# 深圳产业链模型构建（M_CHAIN_DEEP_118_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_118_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_118_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_118_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_118_1 |
| 指标名称 | 深圳产业链模型构建 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链总览／深圳视图 |
| 更新频率 | 建议月更 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「深圳切片」页签、区域产业链看板、深圳产业链地图｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEEP_118_1.md` |

## 口径定义

四类原料齐备，12 条链的深圳切片当日可出（企业 136,326 人次、K 节点覆盖 82.5%、载体 1,030 家），但企业挂链与 K 覆盖都是弱归属，故判部分支持。

## 计算逻辑说明

```text
深圳切片 = 链内企业 ∩ city like '深圳%'；K 节点覆盖 = 深圳企业名 token 命中环节名；载体 = 深圳高校/院所计数
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_118_1.md` §二（M_CHAIN_DEEP_118_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_heis_info`
- `dwd_org_industry_tags`
- `dwd_research_institute_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三张深圳切片结果面都不存在，但切片所需的四类原料在 gkx 齐备且量足：深圳标签行 116,017、12 链深圳企业可逐链汇总、K 节点树 1,273 节点且已有 coverage 计算（90/90 等）、深圳高校与院所可按 city 直接数出。切片是可现在加工的，故不判完全不支持；但链归属靠多标签表、K 覆盖靠企业名 token，两项都是弱归属，切片只能作「分布画像」不能作「环节强度」结论，故判部分支持。
- **基期声明**：本件是截面切片（当前时点的企业/载体分布），不做年度序列，故无基期年份；标签表与底册均为当前快照，不含历史版本，无法回溯往年切片。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_118_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_118_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_118_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

