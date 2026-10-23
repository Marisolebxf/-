# 服务链完整度（M_SVC_SZ_CHAIN_COMPLETENESS）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_CHAIN_COMPLETENESS.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_CHAIN_COMPLETENESS.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_CHAIN_COMPLETENESS_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_SZ_CHAIN_COMPLETENESS |
| 指标名称 | 服务链完整度 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 科技信息展示系统·产业服务链分析·深圳对比页（当前诚实排除，不画完整度柱） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_SZ_CHAIN_COMPLETENESS.md` |

## 口径定义

服务链完整度的分子是「已覆盖的关键环节数」、分母是「全部关键环节数」，而两库既没有「机构×环节」的成员记录（结构缺），也没有任何一行环节事实（数据缺）；公式本身还未签（算法缺）。三层同时缺失，属结构与数据均不具备可算闭环，故判 **完全不支持**，并按要求留下四条否定性探针。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_CHAIN_COMPLETENESS.md` §二（M_SVC_SZ_CHAIN_COMPLETENESS.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：完整度公式未签（Q-SVCCHAIN-04 / 唐绍祖），calc-logic 0.2.0 明确「本件不做真数、不写可执行公式」；计算所需的「机构×服务链六环节服务记录」（SVC-P0-3）在 gkx 与 live 均不存在（gkx 280 表 0 张 svc_*；live 13 张 svc_* 表 0 行）。分子（某机构在某环节提供过服务）与分母（关键环节全集）两端都无结构承载，属结构与数据双缺。经营范围词表派生的六站代理在城市级恒满 6/6、在 12 个产业上恒为 5/6（distinct=1、零方差），既无区分度，又被 calc-logic 明令禁止冒充完整度，不能把档位抬到部分支持。故判完全不支持，官方值置 null。
- **基期声明**：本件是截面（当期环节覆盖），无年度序列，不使用基期年份；future 若要出「完整度时间序列」，需要机构×环节成员表带生效期，当前两库均无此字段。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_CHAIN_COMPLETENESS.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_CHAIN_COMPLETENESS.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_CHAIN_COMPLETENESS_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版（演示态）
- 2026-08-28: 侯佳伟 1A 挂起
- 2026-10-13: 0.2.0 挂起身份落 seed；明确轴若用覆盖则只认服务六环节、禁产业链；不写可执行公式
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

