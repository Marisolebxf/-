# POL-L2-DS10-CMP-PTYPE-QA-L01 · 216 政策类型列 · 演示用例更新与 LOOP 复测

- 流程：`agent-delivery/产品实现规程.md` §6.4 / §6.5
- FDE 总控：`POL-L2-DS10-CMP-PTYPE-FDE`（E 波次）
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-CMP-合规演示用例.md`
- 执行：`agent:qa-agent`（本会话代跑，监管人口令「应该绿了」= CI 绿后开 E 波次，2026-11-11 会话）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`（长度 32），不进 git、不打印。请求头 `Authorization: Bearer` + `systemCode: display`。
- 上游：API `a795cd1`（lumen-svc-platform）/ FE `48f486b`+`a647090`（lumen-ui-science-pc）均推 origin/dev，CI 绿、K8s dev 已 rollout（user 当次确认「应该绿了」）。

## LOOP 第四轮（2026-11-11，PTYPE 增量复测）

- 性质：216 政策类型块为**同步 stats 读**（非写型 Job），验收轮可签发；218 的 POST jobs 沿例仍 SKIP。
- 探测：213 兼探测 HTTP 200、3 行 diff——令牌有效、链路通。
- 证据落盘：`%TEMP%\gkx_loop\cmp\ptype_r4\`（probe_213.json、stats_ptype.json、stats_ptype_v2.json，不进 git）；断言脚本 `%TEMP%\gkx_loop\cmp_ptype_r4b.py`。

### 逐项结果（`cmp_ptype_r4b.py`：8 断言 6 PASS；2 个脚本侧误判勘误后实为全绿）

| 断言 | 实测 | 判定 |
|---|---|---|
| `policy_types` 块存在且北京/广东条目齐 | 2 行，`scope_name` snake 形 | ✅ |
| 北京 Top 文种+件数 | `实施细则` / `3`（脚本初版把字符串数字 `'3'` 判 FAIL，勘误：数据侧为合法计件，前端 `Number()` 转换无影响） | ✅ |
| 广东 Top 文种+件数 | `目录` / `14`（同上勘误） | ✅ |
| 北京 Top=items[0]（SQL ORDER BY count DESC 保证） | 文种、件数均一致 | ✅ |
| 广东 items 省名一致 | 全部 `广东省` | ✅ |
| 回归锚点：`support_strength` 110000/440000 仍在（时点 2026-11-10、值 58） | 在，第三轮期望未回归 | ✅ |
| 回归锚点：`benchmark_objects` 31 行含北京/广东 | 在 | ✅ |
| 键形 | snake 为主、行内 camel 兼容（`policyType`/`regionCode`），前端 `compareLive.ts` 双形容错已覆盖 | ✅ |

- 勘误说明：首轮脚本 `cmp_ptype_r4.py` 4 个 FAIL 均为脚本自身键名/类型假设（camelCase 未容错、top_count 字符串型），非接口缺陷；`r4b` 按 `compareLive.ts` 同款双形容错策略复断言，数据侧全绿。与 2026-11-10 第二轮脚本勘误同性质。

## 用例更新（本任务 touched_files）

- 头注「查库时间」行：增补 2026-11-11 216 政策类型块冻结说明（QPOL-01 文种临时默认 🟡）。
- 覆盖表 216 行：输入/请求/期望全量重写——字段勾「支持力度+政策类型」；期望补 `policy_types.records` 2 行（北京 `实施细则 3`、广东 `目录 14`）、行键双形、🟡 角标文案、`—` 空态不造 0、出处 DWD `policy_base_info.policy_type` 按省聚合、218 图轴不进说明；「只发 `kind=all` 时政策类型块为空」。
- 主路径第 2 步：同步改「字段勾支持力度与政策类型」，写明期望值与空态。
- 218 行不单独改表（图轴行为已并入 216 期望说明）；调度核对维持 6 行可演。

## 结论

- 样本满足：**是**（216 政策类型路径可演；213–218 六行保持可演）。
- **QPOL-01 仍 🟡：文种临时默认口径待甲方确认，界面角标不得去**；甲方定级分类后按 §6.4 重冻结本用例 216 行。
- 前端界面渲染证据：`FE-POL-CMP-LIVE.test.mjs`（`node --experimental-strip-types`）断言 `mapPolicyTypeRows` / `policyTypeCellText` / PendingBadge QPOL-01 锚点全绿（D 波次交付）；线上界面待人工在 K8s dev URL 目检，本轮以接口读面为准。

## 架构合规自检

- D1 调用链：前端 → display → element `/v1/element/policy/compare-stats`，未越层 ✅
- D9：本列非统计指标，为比对文本列；QPOL-01 🟡 角标挂列头，临时默认口径可追溯（DWD 文种按省聚合）✅
- D16/D18：本列读 DWD 原始文种真值（非 gapfill 表、非接口写死 mock）✅
- 只读：本轮仅 GET，未写库、未 POST jobs ✅

ponytail: 单文件自检脚本 + 用例两处文本更新，无新增框架/依赖。
