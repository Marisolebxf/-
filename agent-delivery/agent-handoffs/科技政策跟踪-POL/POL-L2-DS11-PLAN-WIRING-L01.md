# POL-L2-DS11-PLAN-WIRING-L01 · 推荐方案报告交互展示 · 前端接线 handoff

- 任务：`POL-L2-DS11-PLAN-WIRING-L01`（feature，P1，3 点）
- 仓：`lumen-ui-science-pc`（origin/dev）
- 执行：`agent:frontend-agent`；监管：`human:淮政玮`（2026-11-10 会话「还有很多是空的」报障触发返工）
- 强度：ponytail full
- 上游：`POL-L2-DS11-PLAN-ARCH/API/DATA/GAPFILL-L01`（均 done）；测试接力：`POL-L2-DS11-PLAN-TEST-L01` 阶段二

## 一、报障与根因

用户截图（2026-11-10）：推荐方案 Tab 下「多方案对比展示 / 方案参数自定义模拟 / 实施路径与风险辅助」等大片空态。
根因三层：

1. **信封/键名不匹配**：真轨后端返回 PigX 信封 `{code, data:{records:[…]}}`、列名 camelCase（`schemeName/compareDims/paramBand/evalResult/trendText/archiveNote/nodeName/timeProgress/nodeNote/riskTitle/riskNote/opinionSubject/opinionClass/opinionText/opinionAt`）；旧接线只认 mock 轨 `{items:[…]}` + snake_case → `records` 永远取不到，五叶全空。
2. **`compareDims` 是文本**：表内为「维度：数值」多行 text（如 `财政补助强度：8%\n企业配套比例：1:1.8`），旧代码当已结构化 `compare_items` 消费 → 雷达/KPI 无数据。
3. **230/231 查询参数名错**：前端传 `scheme`，后端 shells 端点收 `@RequestParam("scheme_name")` → 意见/报告恒空。

## 二、修复实现

| 文件 | 变更 |
|---|---|
| `src/views/policy/analysis/schemeRowParse.ts`（新增） | 纯归一层（零 import）：`schemeRowsOf`（records/items/整信封兜底）+ `parseCompareDims`（文本→结构化，首数启发式已 `ponytail:` 注明天花板）+ `compareRowOf/simRowOf/pathRowOf/opinionRowsOf`（camel/snake 双兼容；230 分类闭集 `评价/评论/建议` 外丢弃） |
| `src/views/policy/analysis/schemePlanWiring.ts` | 五叶 load 全部经归一层；229 按 sort_no=id 升序；231 兼容真轨 `{records}` 与 mock 轨 `{schemes}` |
| `src/api/policyEvaluationPlan.ts` | 230/231 real 映射改传 `scheme_name` |
| `src/views/policy/analysis/index.vue` | 下线 demo 种子残留（`simParams/simPreview/filterSchemes/schemeMerit/editModalOpen/t42` 闸门等）；左栏方案卡/228/229/230/231 全部接真轨行；`liveSchemes/canExportSchemes/currentScheme` 由 227 读行派生 |
| `src/views/policy/analysis/schemeRowParse.test.mjs`（新增） | assert 自检 8 断言，形状取自线上实测 |

## 三、线上实测（2026-11-10 22:0x，edu.itic-sci.com/tid/api，Bearer 本机 token，只读 GET/同步 POST）

| 叶 | 请求 | 结果 |
|---|---|---|
| 227 | POST jobs kind=方案对照 | 200，records **4** 方案（人才引育优先/平台攻坚优先…），row0 含全字段 |
| 228 | POST jobs kind=参数模拟 scheme=人才引育优先方案 | 200，records **4** 档（人才规模基准档…） |
| 229 | POST jobs kind=路径与风险 scheme=同上 | 200，records **6** 节点（首节点带 riskTitle/riskNote） |
| 230 | GET shells kind=互动意见 scheme_name=同上 | 200，records **6** 意见 |
| 231 | GET shells kind=方案报告 scheme_name=同上 | 200，records **2** 方案对照行 |

结论：**后端与 gapfill 数据全部就绪**；截图所见空态 = 旧前端未接通（本修复）+ 线上 K8s dev 尚未部署新代码。

## 四、验证证据

- 自检：`node --experimental-strip-types src/views/policy/analysis/schemeRowParse.test.mjs` → **8 passed**（真轨实测形状 + mock 轨双兼容；曾抓住并修复「整信封未解包」边界）
- **本地全量 vue-tsc 未跑完**（>15 分钟挂起，用户裁定「本地忽略编译」后已终止进程）。替代：静态一致性核对——已删符号（`t42/simParams/simPreview/filterSchemes/schemeMerit/editModalOpen/PATH_DATE_SEED/dayjs`）零残留引用；图标 5 枚全有模板引用；`exportPolicyEvalSchemeReport` 与 `analysisExport.ts` 签名对齐；mock 轨 `{items}/{schemes,opinions}` 与归一层兼容。真编译由 CI 门（push → Pipeline）兜底。
- 空态语义（DoD 2）：方案未选 → 228/229/230 空；参数档对不上 → 228 空并回落首档下拉；行不足两行 → 227 对比空；导出无行 → 提示「导出为空」不产文件；采纳/改期/页面新评价不写库（新评价只入浏览器会话数组）。

## 五、偏离说明

- DoD 3 写「pnpm type-check/build 三绿」：本地 vue-tsc 挂起未完成，按用户裁定改「自检绿 + 静态核对 + CI 兜底」。**CI 绿后测试接力单才能进阶段二**，若 CI 红需回本单修。
- `schemeRowsOf` 增加整信封兜底（`data.records`）：超出 API 分册字面（分册假定拦截器已解包），属防御性兼容，测试断言覆盖。

## 六、架构合规自检

- D1 调用链 ✅ 前端只调 `/display/v1/policy/evaluation/**`（网关剥前缀 → gkxlumen-display → Feign gkxlumen-element → gapfill 表），不直连 Python/库
- D9 血缘 ✅ 各叶块保留 MockBadge + ⓘ 位；229 行 metric_id 已在 GAPFILL 单核实（6 行命中 M_POLICY_DS_11_POLICY_EVAL_015）
- D12 隔离 ✅ 只改 lumen-ui-science-pc，未动 demo 仓
- 诚实性 ✅ 不造方案/不造意见/不现算；228/229 行原样展示；230 分类闭集外丢弃
- Git 纪律 ✅ 待 commit 带 `[agent:frontend-agent]`，push origin/dev

## 七、待办与接力

1. **人工确认后 push**（fe-manual-confirm-push 闸门）→ CI 绿 → K8s dev rollout → 用户复验界面（应看到 4 个方案卡：人才引育优先方案等）
2. `POL-L2-DS11-PLAN-TEST-L01` 阶段二：S1–S5b 截图 + TC-01~TC-07 联调实测回填
3. token/口令不进 git（本机 `%USERPROFILE%\.gkx\display-loop-token`）

## 产物清单

- 代码：`schemeRowParse.ts` / `schemeRowParse.test.mjs`（新增），`schemePlanWiring.ts` / `policyEvaluationPlan.ts` / `index.vue`（修改）
- 本 handoff：`agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-PLAN-WIRING-L01.md`
- ponytail: 单文件纯函数归一层 + 8 断言自检；未引入新依赖、未加框架
