# FE-TS-10B · handoff

- 任务：`FE-TS-10B`（implementation · 维护管理图层与数据源前端接线）
- 日期：2026-11-06 · 监管：`human:刘剑锋` · 认领：`agent:frontend-agent`
- 状态：代码已推 feat 分支 + MR !2 待合入 dev；maintain 测试/type-check/build 三绿。**未联调**（等 BE MR !2 合入 + DDL 执行），不标 done
- 分支：`lumen-ui-science-pc` `feat/m10-maintain-wiring`（b263c0b）· MR：`/-/merge_requests/2`

## 实现内容（7 文件，+619/-59）

| 文件 | 变更 |
|---|---|
| `types/maintain.ts` | +服务端 DTO 五型（ServerLayer/LayerGroup/Datasource/FactorDisplay/ProbeResult，对齐契约） |
| `api/situation/maintain.ts` | **全量重写**：`/display/v1/situation/maintain/**` 四组资源 + probe 双轨（10 个 defineApi）；信封解析（40001/40401/40901/50101→MaintainApiError）；图层中文名↔layerCode 翻译收本层；页面行 id 统一服务端数字 id；`fetchMaintainMeta` 降级为兜底（real 抛「已废弃」，mock 返图/实体演示种子） |
| `mock/modules/maintain.ts` + `register.ts` | 新 10 个 mock 命中绑定（demo 纯函数透传，演示态语义完整保留含「至少留一组」） |
| `LayerSourcePanel.vue` | 写操作全 async 经双轨 api（`apply()` 统一出口 + busy 防抖）；**填报型 probe 禁用按钮**（契约 §4.1）；组名改失焦提交（防每键一次 PUT）；probe/409 错误行内 notice |
| `stores/factorDisplay.ts` | **服务端化**：`syncFromServer()`（真源 cfg_factor_display→覆盖层；失败回退 localStorage）；`upsert/reset/resetAll` real 轨 fire-and-forget PUT；localStorage 降级为只读回退缓存+成功镜像 |
| `index.vue` | 分区1 改 `loadMaintainState`（四组资源）；图/实体分区仍 meta 演示态（34–40/41–47 范围外）；挂载时 `syncFromServer()` |

## 差异表六项落地对账（API 分册 §0）

| 差异项 | 落点 |
|---|---|
| meta 废弃拆 4 组 | api 层 `fetchMaintainMeta` 降级兜底 + `loadMaintainState` 等 10 函数 |
| targetLayer 中文→code | api 层 `LAYER_CODE_NAME/NAME_CODE` 双向翻译，面板/表单仍用中文枚举零感知 |
| lastSync 列 | real 行恒 `'-'`（组装器写死，契约无同步动作） |
| testStatus | real 行恒 `未测`；probe 结果即时写行（`通过(123ms)`）+ notice；不持久化 |
| 删组 409 | api 层 catch 409 → 「组下仍有数据源，请先改挂」 |
| 至少留一组 | real 轨无拦截（契约显式放弃）；mock 轨保留 demo 语义 |

## 验证

- `node --experimental-strip-types src/views/situation/maintain/maintain.test.mjs`：ok（demo 三状态机 35 断言不回归）
- `pnpm type-check`：✅（修 5 处：MaintainSeq 导源/模板 state.value 误用/factorName 空串/索引 undefined/meta 泛型）
- `pnpm build`：✅ 51s built
- 本仓无 `design:check` 脚本（那是 demo-ui-topic 仓关卡），对等关卡=type-check+build 已过

## 偏离与遗留

- 双轨语义边界：mock 轨完整保留 demo 演示态（含至少留一组、假延迟 probe、localStorage 真源）；real 轨按契约。USE_MOCK 切换即换轨，页面零改动
- **联调依赖**：BE MR !2（lumen-svc-platform）合入 + `9x_gkxlumenx_cms_tech_maintain_config.sql` 执行 + 网关 `/display/**` 路由核验（已有）+ 登录态。联调走查（含 M1 图例联动）待环境就绪
- `updateLayersEnabled`/`loadLayers` 已导出但面板未用——留给 M1 地图接线（overview 消费 layers/factor-display）时启用
- `.env.development` 本地改动未提交（含个人开关，遵循 FE-TS-10A 同款纪律）

## 架构合规自检

| 项 | 状态 |
|---|---|
| 不重做页面结构（maintain 布局零改动） | ✅ 仅 script 与既有模板行为点 |
| 契约=API 分册（路径/DTO/错误码） | ✅ 四组资源+probe 逐端点对齐 |
| D12 无 demo 依赖 | ✅ mock 轨是仓内冻结种子非运行时依赖 |
| 双轨（USE_MOCK） | ✅ 演示态语义与 demo 冻结一致 |

## cost

- actual_tokens: ~70k
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$1
- cost_warn: green
