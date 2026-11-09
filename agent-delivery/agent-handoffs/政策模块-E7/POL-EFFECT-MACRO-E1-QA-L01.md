# POL-EFFECT-MACRO-E1-QA-L01 · 落地实效宏观代理：E1 金路径冒烟

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §3 · 前序：[`POL-EFFECT-MACRO-E0-DEVOPS-L01.md`](./POL-EFFECT-MACRO-E0-DEVOPS-L01.md)
> 日期：2026-11-09 · 类型：tech_task · Epic：`E-POLICY-PDR` · 故事：`US-E7-POL-04`
> 证据目录：`evidence/POL-EFFECT-MACRO-E1-QA-L01/`（脚本 + 截图 + 响应体 + 网络日志，约 2MB）。该目录被 `.gitignore` 第 50 行忽略，**仅在 QA 本机工作区（hzw）**，未入 git；关键数据已摘录进本文。本叶**未改任何业务代码**。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | QA 只测已发布页，不写业务代码。脚本用 playwright-core 直跑，未加依赖进业务仓。 |

## 结论

**金路径 4 条全过（PASS）**。建议推进 `ready_to_sign`。另记 **1 条非本管线缺陷（C1，分析指纹对短码产业恒同）**，不挡本叶，需 coordinator 另派前端 bugfix。

- 测试对象：lumen 前端 `http://10.50.69.111:30892`（`gkx-lumen-topic:112afa6e`），算法中台 `http://10.50.69.111:30889`（demo-ui-system-test `41d757a`）。
- D12：lumen 会话全部 `/api/*` 打 `30892`，无 `demo-*` host；全程无 5xx（见 `run*-net.txt`）。
- 前置核对：`lumen-algo-py` Pipeline #4365 **无法查询状态**（GitLab 需登录，无凭据）。侧证：本叶 3 次强制重跑 + 中台 3 次试算全部 200 且结果一致，健康体 `GET :30892/api/policy/topic/v1/policy/health` 200 `degraded=false`；落地实效走 `entan-py`，不经被 #4365 滚动的 `lumen-platform-algo-py`。未遇到滚动窗口失败。

## 金路径结果

| # | 故事 | 路由 | 判定 | 实际现象 | 证据 |
|---|------|------|------|----------|------|
| 1 | US-E7-POL-04 | lumen `/policy/recommendation` 深圳结果板 | **PASS** | 强制「重新分析」产出新任务 `POLICY-20261109-007`（集成电路）。`cards.effect`：`computable=true`、`score=78.5836`，`ext.caliber=macro_outcome_proxy`、`indicator_count=8`、`whitelist_version=macro-eff-v1`、`source_tables=[gkx.dwd_macro_index_data]`、`city_scores` 四城、`period_used`、`proxy_notes`；`frozen_cards.effect` 同带 ext。卡内可见「口径：宏观结果面代理，不等于政策启动率、兑现率或满意度（待甲方确认）。参与指标 8 项。」；`track_a_status=partial_gapfill`，页面写「正本三维补空诊断分 72.7658，仅作诊断，未并入本分」，**无综合分**。 | `run2-result.png` · `run2-effect-card.json` · `run2-bodies.json` · `run2-result-body.txt` · POST Create trace `21080bc9c8517061bb1304a3dca5e382` · result GET trace `2ca588f0912ff1195a870a0bbc27a389` |
| 2 | 同上 | 对比城市分 | **PASS** | 页内无「切换城市」控件，以截面列表验证：上海 30.3062 / 北京 48.5023 / 广州 41.101 / 深圳 78.5836，四城各不同，非常量，且 `0≤score≤100`。取数期按城展示且声明「非同期比较」。参与指标数按规则为 8（GDP 因「参与城 2 < 3」剔除，写入 `proxy_notes`），**未硬断言 9、未硬断言分数**。换产业强制重跑 `-008`（软件与信息服务）实效仍 78.5836，符合城市级宏观口径（与产业无关）。 | `run4-sw-force-*` · POST trace `efe339c6ba7559c9fb25080495a08fd1` |
| 3 | 算法中台 | demo-ui-system-test `/#/policy/effect` | **PASS** | 顶部「落地实效 · 宏观结果面代理（macro_outcome_proxy）」区块：「⚠️ 待甲方确认（QPOL-02）」tag + 口径说明（白名单 macro-eff-v1、四城截面归一等权、不等于启动率/兑现率/满意度、正本三维仍不可算不以 0 代替、期次未对齐）。进页自动请求 `GET /api/policy/v1/policy/effect/macro` 200，页面深圳试算分 78.58 与接口 `city_scores.深圳=78.5836` 一致；点「重新试算」再发一次请求（trace `67e22eb3c800637db2b823cdfb28db40`），分数仍真读真算、无写死。 | `mid-effect.png` · `mid-effect-body.txt` · `mid-macro-bodies.txt` · 进页 macro trace `017fd29e5c484f429c9cd2e4e09435ff` |
| 4 | 回归 | 深圳页支持力度 / 适配性 | **PASS（本管线未改坏）** | 三张固定卡 + 仪表盘柱图布局完整。支持力度：同日预发布任务 `-001` 与新任务 `-007` 完全一致（分 33.5585、名次 5、条数 879、层级 0.4653、档位 4、「非资金强度」说明）。适配性：锚点随产业变化（集成电路 命中 45 分 9.044；软件与信息服务 命中 0 → 页面「不可算：无命中」，未写 0）。 | `run2-result.png` · `run4-sw-force-result-body.txt` |

### 与总控字面期望的两处对照说明

1. **⚠️ 语义**：已发布结果板上「待确认」以**文字**体现（口径句「（待甲方确认）」）。`PendingBadge` 的 ⚠️ 图标与 `M_POLICY_*` / `macro-eff-v1` 等技术键按设计受评审层门控，非评审模式 DOM 里不出现（`dom-check.json`：`metric_id=false`、`whitelist=false`、`source=false`、无「综合」字样）。判定为符合 FE handoff 设计，非缺项。
2. **「期望未发生=红」未触发**：首轮点「开始分析」**没有**新建任务，而是被「当天已成功直接复用」带到 00:30 的旧任务 `-001`（E0 之前算的，`effect` 只有 72.7658、无 `ext`）。已改用「重新分析」强制重跑才得到金路径数据，见下条风险。

## 非本管线缺陷（记录，建议另派）

### D-E1-01 · C1 · 分析指纹对短码 L0 产业恒同，当天复用返回别的产业结果

- 步骤：配置页选 集群「新一代信息技术」→ 产业「软件与信息服务」→「开始分析」（未强制）。
- 期望：新建或复用**该产业**的任务。
- 现象：同日 3 个不同产业（人工智能 `-001`、集成电路 `-007`、软件与信息服务 `-008`）的 `analysis_fp` 全是 `dcd99c2d530c1341c4ccc2005c59700dcccf23cfce6b74842a2e98aafdb987de`。不强制时点「软件与信息服务」直接打开 `-007`：页头写「分析对象：软件与信息服务」，适配性却是「锚点 集成电路 命中 45」。**静默张冠李戴。**
- 怀疑层：前端。`PolicyAnalysisConfigPage.vue` `fingerprintArgs()` 的 `industryVid = toPolicyGraphVid(industryId)`，map 短码 L0（`INB1303` 等，不足 INB+6 位）算不出 VID → `policyAnalysisFingerprintInput` 的 `objectKey` 为空串，所有短码 L0 共用一个指纹。提交体用的是 `industrySubmitFields()`（`chain:`+短码），与指纹口径不一致。
- 复现 trace：复用打开 `-007` 的 `GET result` `b0ff1e1085c4c53de82c82d0c307b11c`（run3）。
- 影响：不影响本叶实效金路径（实效是城市级，与产业无关）；影响适配性准确性与「当天复用」。**建议** coordinator 派 `frontend` bugfix：指纹的 objectKey 与提交体的 `industry_vid` 同源（含短码 L0）。
- 与本管线关系：非本管线引入（`-001` 在 E0 前已存在同指纹），不阻塞 E1。

### 风险 R-E1-01 · 当天旧任务不带 ext

E0 之前算出的同指纹任务被复用时，实效卡只有分、没有口径声明和城市分（FE 对缺 ext 的处理正确：不造声明）。演示/验收前请用「重新分析」重跑，或依赖次日自然失效。

### 观察 O-E1-01 · 支持力度档位说明含 `QPOL-02` 字样

非评审模式正文可见「档位 4。截面金额均值临时分位，QPOL-02」，来自 Python 返回的 `tier.reason`，早于本管线。D9 要求关评审模式零泄漏 `Q0xx`。非本叶范围，记一条供 data/algorithm 收口。

## 测试方法与限制（诚实声明）

- 工具：Playwright（chromium 1.51，headless）直点已发布前端；业务接口全部真实请求，**未代理 POST 改判**，创建任务是 UI 点「开始分析 / 重新分析」。
- **鉴权桩**：发布版已关 mock 登录（`VITE_ENABLE_MOCK_AUTH=false`），QA 无真实 SSO 账号。脚本只对 `GET /api/admin/get-permission-info` 返回一个最小菜单（政策分析下 4 项）并剥掉 Authorization，使路由守卫放行。其余接口一律真实。不是业务 mock，但不覆盖真实 SSO 登录与按钮权限。
- 算法中台登录页自带 demo 默认账号（页面公示），用该账号登录。
- 创建了 2 个新任务：`POLICY-20261109-007`、`POLICY-20261109-008`（测试数据，user=guest）。
- 复跑：`NODE_PATH=<含 playwright-core@1.51.0 的 node_modules> FORCE_RERUN=1 node gold1.cjs`；`node gold3.cjs`；`node dom-check.cjs`。

## 修改内容

无业务仓代码变更。仅新增本 handoff 与证据目录。

## 测试结果

4 / 4 PASS（见上表）。5xx 0 次，D12 命中 `demo-*` 0 次（`run*-net.txt`）。

## 遗留风险

1. D-E1-01 / R-E1-01 如上。
2. #4365 状态无法核实（侧证见结论）。
3. 鉴权桩未覆盖真实 SSO。
4. `GKX_ODS_MYSQL_*` 仍走 yaml 默认（E0 已记，非本叶）。

## CI/CD

- 分支：未改业务仓；未触发业务仓 CI。
- 部署：lumen-ui-topic `112afa6e`（:30892）· demo-ui-system-test `41d757a`（:30889）· `gkxlumen-entan-py-api:1847cd9d`（E0 实测）。
- 编排仓：本 handoff 推 `origin/dev`。

## 可观测性

- 关键 traceId：POST Create `21080bc9c8517061bb1304a3dca5e382`；result GET `2ca588f0912ff1195a870a0bbc27a389`；中台 macro `017fd29e5c484f429c9cd2e4e09435ff`；强制重跑 `-008` `efe339c6ba7559c9fb25080495a08fd1`。全部 200，未失败故无需 Tempo 抄录。

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ QA 未改代码；分数均来自 Python 返回 |
| 2 调用链 | ✅ lumen 前端→Java（topicAsync）→Python；中台走 demo 既有 `/policy/v1/**` 范式 |
| 3 Nebula | ✅ 不涉及 |
| 4 可观测 | ✅ 全程 `X-Trace-Id` |
| 5 CI/CD | N/A（本叶不改业务仓） |
| 6 demo 只读 merge | ✅ 无 merge |
| 9 D8 / 10 D9 / 11 D10 | ✅ 待确认以文字声明 + 评审层门控；无综合分；不伪造 0（见 O-E1-01 例外） |
| 12 D12 | ✅ lumen 会话无 `demo-*` 请求；中台为 demo 沙箱，独立会话 |
| 16 D18 | ✅ 无写死 mock 分，真读真算 |

## cost（回填 registry）

| 字段 | 值 |
|---|---|
| actual_tokens | 约 230000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 1.2 |
| cost_warn | green |
| 说明 | source: session_estimate |

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/POL-EFFECT-MACRO-E1-QA-L01.md`（本文件）
- `agent-delivery/agent-handoffs/政策模块-E7/evidence/POL-EFFECT-MACRO-E1-QA-L01/`（gold1/gold3/dom-check 脚本、截图、响应体、网络日志）
