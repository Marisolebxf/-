# POL-L2-DS10-CMP-PTYPE-FE-L01 · D 波次前端 handoff

- 任务：`POL-L2-DS10-CMP-PTYPE-FE-L01`（`POL-L2-DS10-CMP-PTYPE-FDE` D 波次）
- 认领：`agent:frontend-agent`；监管：`human:淮政玮`
- 强度：ponytail full
- 日期：2026-11-11

## 范围与实现

SRS 216 对标表「政策类型」列 + 218 图交界，数据源 = stats 新增 `policy_types` 块（API 端 `POL-L2-DS10-CMP-PTYPE-API-L01`）：

1. `compareLive.ts`：新增 `PolicyTypeRow` / `mapPolicyTypeRows`（snake 兼容 camel，`items` 逐行映射）/ `policyTypeCellText`（格文案 = `Top文种 件数`，如「通知 32」；无行 → 空串，组件渲染 `—`）。
2. `BenchmarkCompareModal.vue`：
   - `loadLiveStats` 增读 `policy_types`（含 indicators 兜底路径）；
   - `liveFieldValue` 增「政策类型」分支返回文种文案（返回类型放宽 `number | string | null`）；表格行按对象省名取文案；
   - 表头「政策类型」列经 Arco `#th` 插槽挂 `PendingBadge`（`QPOL-01`，评审层自闸，关闭零渲染）；
   - 218 地区视角图轴过滤掉「政策类型」（文种文案非力度量纲），政策视角保持空态——同 SDS 216-PT-4；
   - 打开弹窗复位清单增 `livePolicyTypeRows`。
3. 自检：`FE-POL-CMP-LIVE.test.mjs` 增 8 处断言（映射 / 格文案 / 缺席不造默认 / 组件锚点 mapPolicyTypeRows·policyTypeCellText·PendingBadge·QPOL-01），`node --experimental-strip-types` 全绿；头部运行说明同步。

## 偏离说明

- 218 地区视角「政策类型」不进图轴：L2 ARCH §5.6 写「地区视角图以各省 Top 文种件数为量」，实现按 SDS 216-PT-4 收敛为雷达/柱/热力共用轴只收数值量——文种件数若入轴会与力度指数/覆盖度混纲（雷达轴 max 语义破坏）。SDS 216-PT-4 与 ARCH §5.6 表述需 E 波次对齐时以 SDS 为准（已在 SDS 写明「政策视角保持空态；地区视角以 Top 文种件数为量」——如产品坚持文种件数单独出图，走 FDE 追加，不在本叶混轴）。as-built：图轴不含政策类型。

## 产物清单

- commit `204112d` + `6ed642c`（lumen-ui-science-pc 本地 dev，**待人工确认推送**——fe-manual-confirm-push 规约）
- 3 文件 +96/-12（另 fix +4/-1）

## 验收证据

- `node --experimental-strip-types src/views/policy/panorama/FE-POL-CMP-LIVE.test.mjs` 全绿（本地跑的是纯断言自检，非编译；type-check/build 按「本地不需要编译前端」走远端 CI）。
- 类型防炸：图轴 `get` 收窄 `number | null`（commit `6ed642c`，防 TS2345 重演）。

## 架构合规自检

| 铁律 | 结论 |
|---|---|
| D8 栈 | ✅ Arco `#th` 插槽 + 既有 PendingBadge（无新依赖、无自绘控件） |
| D9 | ✅ 只读消费 `policy_types`；无行 `—`，不造 0；ⓘ/角标不撤 |
| D10/评审层 | ✅ PendingBadge 自闸（useReviewStore），关闭 DOM 零泄漏 |
| I2-12 | ✅ 未加任何自动触发；切条件不自动起任务 |
| D12 | ✅ 只调 `/display/v1/policy/panorama`（既有 panoramaStats），无 demo 直连 |

## cost

- `actual_tokens`: ~95k；`model_used`: glm-5.3-flash；`actual_cost`: ~$0.40；`cost_warn`: 无

ponytail: 复用既有 PendingBadge / blockRecords / mapBenchmarkObjects 模式，未新增公共件；`policyTypeCellText` 一行函数即为格式化边界。
