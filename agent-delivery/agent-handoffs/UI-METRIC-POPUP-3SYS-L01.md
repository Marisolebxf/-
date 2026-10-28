# UI-METRIC-POPUP-3SYS-L01 · 三系统评审模式指标弹窗升级

> 2026-10-28。status: ready_to_sign。
> 依据：入库查实任务「20261021 指标入库与四大系统落地查实」§四 补救清单第 5 项（查实正本见 `agent-delivery/agent-handoffs/指标算法库上线/METRIC-SRS-GAP-L01/产物/20261027三系统兼容升级/` 附带报告，原调研区为本地工作区不入仓）。
> 数据基准：20261027 批 573 份指标 md，**正本已实物化入仓**：`agent-delivery/agent-handoffs/指标算法库上线/METRIC-SRS-GAP-L01/产物/20261027三系统兼容升级/第三方库指标计算过程/`（8 件 `_ZT`/`_ZS` 拆分件在内）。

## 交付物

| 项 | 内容 | 位置 / commit |
|---|---|---|
| 编译器 | `gen_popup_info.py`（573 md → 四区块 JSON） | 同上入仓目录（输入源已切至入仓正本，本地工作区不再依赖） |
| 中台产物 | `metricPopupInfo.generated.ts`（565 keys，原 ID） | `demo-ui-system-test/src/views/shared/` |
| 专题产物 | 同上（6 族 `_ZT` 优先映射原 key） | `demo-ui-topic/src/app/mock/enterprise/` |
| 展示产物 | `metricPopupInfo.generated.js`（ESM，`_ZS` 优先） | `demo-ui-science/src/` |
| 中台 UI | 三弹窗 + `MetricPopupBlocks` + 合并层 124 命中 | `1c34a1d`（dev） |
| 专题 UI | MetricSpecCard 三区块 + verdict_20261027 36/70 | `dab369f`（dev） |
| 展示 UI | 三套弹窗 + 共享组件 + 契约测试 | `7619afc`（dev） |
| 验收 | Playwright 28/28 断言 100% PASS | `e2e_trackd-run12-final.log` + `e2e_shots/`（7 截图，均已随编译器入上述目录） |

## 四区块口径

1. **req_overview 需规概述** = md「## 摘要」前 2-3 句 +「一、需求定义概述」业务概括（句净化工程语言；兜底 seed definition）。非空率 100%。
2. **calc_logic 计算逻辑** = 「二、计算过程」2.1/2.4 各 1-2 句；24 件无此章用「二、依赖性质裁定/五、方法对照」承载；兜底 seed formula。非空率 100%。
3. **references 参考文献** = 逐条 {text,url,group}；组序 国家机关(1792) → 国内其他(335) → 外刊(787)，共 2914 条；死链 1/内部条目 67/占位 9 过滤。
4. **support 支持度** = md 头部「数据支持度」四档 + 四判定摘要（有则录，无则空，不伪造）。

## DoD 核验

- [x] 三仓 `npm run build` 0 error
- [x] 三仓既有契约测试绿（science `metricCatalogConsistency.test.mjs` 含 mirror↔popup 名称比对新增断言）
- [x] Playwright 28/28：三新区块存在且非空、展开收起可用、组序正确、0 console error / 0 pageerror（过滤存量 antd deprecation 与 dev 无后端噪音）、弹窗无溢出错位（截图核验）
- [x] 生成物 0 处 `local-workspace` 路径字符串
- [x] 三仓 push dev（`9ce9e6f` / `5d4a984` / `4a233e5`），origin/dev 已含任务 commit
- [ ] CI 绿（推送后流水线结果见 GitLab；本单 push 时点 CI 触发中）

## 遗留（不属本单）

- science mirror ↔ 20261027 批名称漂移 52/140（seed 链路 owner 对齐后重生成 mirror，本单已 warn 清单化）。
- 中台 8/132 help 指标不在 565 基线（UI 演示/衍生件，无调研数据属预期）。
- 专题 64 个存量测试失败与 HEAD 基线逐字节一致（design:check 等，非本单引入）。
