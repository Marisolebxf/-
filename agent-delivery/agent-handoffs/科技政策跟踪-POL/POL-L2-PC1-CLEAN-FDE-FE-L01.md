# POL-L2-PC1-CLEAN-FDE-FE-L01 · 602 清洗页签 · 选择政策与执行

ponytail: full

> 2026-11-10。只改清洗页签。未 push。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时状态已是 in_progress，未再 task-claim。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8/D9/D10、可观测和已有页壳。清洗列表与本批不走 fixture。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机这一步没有走 headroom 压缩。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本叶不改架构图。 |
| 图 diff | 无 |
| 会签态 | 无 |
| 说明 | 界面以说明书「#### 602」和 `602-选择政策-线框.md` 为准。 |

## 问题清单

- 清洗页从「演示政策」单选改成选择政策：智能搜索、按政策 ID、国内/海外多选、执行、清空。
- 没点执行不发本批。执行中锁住勾选、清空和六条开关，执行不能再点。
- 规则启停只在本次打开的页面里，重新进入六条都启用，不落库。
- 页眉库级计数仍走原 `governance/results`，指标仍是 `M_POLICY_TOTAL_COUNT`。结果汇总不进本批，清洗卡不再挂 `M_POLICY_VALIDITY_RATE`。

## 修改内容

仓库 `lumen-ui-science-pc`，分支 `dev`，commit `9bb644c`。未 push。

- `src/views/policy/governance/index.vue`：只改清洗页签。结构化、溯源、指标库仍用原来的单选。
- `src/views/policy/governance/cleanSelect.ts`：空态和本批文案判定。
- `src/api/policy.ts`：新增 `GET /display/v1/policy/governance/clean-candidates` 与 `POST /display/v1/policy/governance/clean-execute`。这两条直接打网关，不进 mock 注册。页眉仍用原 results。
- 可观测：沿用 `request` 的 trace，并补 `clean-search` / `clean-execute` / `clean-clear` / `clean-rule-toggle`。

## 与线框对照

| 线框 | 页面 |
|------|------|
| 条件栏「选择政策」，可多选 | 清洗页卡片标题是选择政策。国内、海外各一块多选，进同一个已选集合 |
| 智能搜索：国内标题、文号或发文部门；海外只按标题 | 搜索框下写明海外只按标题。检索词原样交给候选接口，页面不另用文号去搜海外 |
| 按政策 ID 精确查 | 第二个搜索框，`mode=id`，参数 `policy_id` |
| 表在且当前行为 0：「这一源还没有贴源数据」 | 该源 `status=empty` 才用这句 |
| 表不在或查询失败：「读取失败」 | 整段失败或该源 `read_failed` / 缺块，都写读取失败，不改写成贴源无数 |
| 该 ID 不在贴源 / 这次没搜到 | 按候选块的 status 分句。没搜到不写成该 ID 不存在。已选政策不被这次响应清掉 |
| 已选旁「执行」，未选或执行中不可用 | 按钮在已选标签旁边。未选或执行中禁用 |
| 清空，执行中不可用 | 清空回到未选，规则区和批次明细清空 |
| 改勾选或开关不自动跑 | 只改页面状态。已有本批时标明「还不是最新一次」 |
| 六条规则，重开都启用，执行中开关不可用 | 名称与作用范围写在 `CLEAN_RULES`。停用行仍在，标明停用。不写 sessionStorage |
| 没点执行前无本批判定，不写成功 | 未选时不渲染规则表。未执行时命中列空白，批次明细无行 |
| 点执行才有批次名和条数 | 批次头用执行响应的 `batch.name` / `batch.count` |
| 成功 / 部分 / 失败 | 只在执行响应的 `batch.status` 是这三字时，写到能判定的规则行。读取失败和无加工事实不用这三字 |
| 无加工事实 | 命中留空，不写 0，不写成功 |
| 准确性有演示数则标明演示；没有演示行写「这一条还没有演示数」 | 只展示接口给出的 `demo_hit_count` 或这句。不画表名，不写成已经按原文核过 |
| 执行中 | 批次头写「执行中」。勾选、标签关闭、清空、六条开关、执行都不可用。先不写成功 |
| 页眉不随这一选改口径 | 清洗勾选不再调用 results。页眉件数仍是 `M_POLICY_TOTAL_COUNT` |

## 复刻五维

| # | 结果 |
|---|------|
| V1 | 沿用本页 `demo-policy-pc-pages.css` 与页壳，未另起灰白页 |
| V2 | 不适用。本叶不是检索 Hub，没有新 Hero |
| V3 | 候选行是标题加辅文，横向排在勾选右侧 |
| V4 | 清洗页左选择、右规则和批次，一列一套 |
| V5 | 候选勾选行 `min-width: 0`，标题可换行 |
| V6 | 未检索不写贴源无数；有句才显示对应空态 |
| V7 | 候选不是结果卡网格 |
| R1 | 选择、两源列表、已选、执行、清空、六条规则、批次头、批次明细都在 |
| R2 | 未选、未执行、执行中、贴源无数、ID 不在贴源、未命中、停用、无加工事实、没有演示行、读取失败、陈旧结果都有对应文案或空位 |
| R3 | Arco 输入、多选、开关、按钮、表格、标签。控件沿用本页字号 |
| R4 | 评审仍走页面已有 `@/review` 的 `reviewMode`。本批条数不是指标，不新造 ⓘ。清洗卡不再挂有效率指标。关评审后本叶不写 metric_id |
| R5 | `USE_MOCK=false` 时候选和本批不读 `@/mock`、不用 fixture。两条新接口不走 `defineApi` 的 mock 命中 |

W1–W3 不适用：本叶不是分析工作区，没有关系图，也没有新报告阅读器。

## 测试结果

- `pnpm type-check`（`vue-tsc --build`）退出码 0。
- `node --experimental-strip-types src/views/policy/governance/cleanSelect.test.mjs`：12 组断言通过。
- `node src/views/policy/governance/FE-POL-04A.test.mjs`：22 组断言通过。
- 未在浏览器里对已登录展示页点选。本机这一步没有打开带网关会话的页面。

## 遗留风险

- 未 push。dev 环境还不是这版页面。
- `USE_MOCK=true` 时页眉四张卡仍来自原数据集。清洗卡不再挂 `M_POLICY_VALIDITY_RATE`，但百分比数字仍是原数据集，不进本批。
- results 返回前，页眉仍用页面原有的首屏初值。这是原页面行为，本叶没有改。
- 结构化、溯源、指标库仍是「演示政策」单选。
- 候选和执行依赖 Java 公开读口。接口失败时对应块写「读取失败」，不造 0。

## CI/CD（必填）

- 分支：`dev`
- commit：`9bb644c`（lumen-ui-science-pc）
- pipeline URL / ID：未 push，无新流水线
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未执行
- dev 测试 URL：无

## 可观测性（建议）

- 候选和执行走既有 `request`，响应 trace 仍由拦截器提取。
- 页面另发 `pol-policy-track`：`clean-search`、`clean-execute`、`clean-clear`、`clean-rule-toggle`。
- 未在 dev 抽样 traceId。

## 涉及文件

- `repos/lumen-ui-science-pc/src/views/policy/governance/index.vue`
- `repos/lumen-ui-science-pc/src/views/policy/governance/cleanSelect.ts`
- `repos/lumen-ui-science-pc/src/views/policy/governance/cleanSelect.test.mjs`
- `repos/lumen-ui-science-pc/src/views/policy/governance/FE-POL-04A.test.mjs`
- `repos/lumen-ui-science-pc/src/api/policy.ts`

## 架构合规自检

1. 只调 Java 公开读口，不直连 Python、不直连库。✅
2. 未改图谱。✅
3. 可观测沿用 request 与政策页埋点。✅
4. 未改 CI 配置。✅
5. 未把 demo 合并进 lumen。✅
6. D12：路径在 `/display/v1/policy/` 下。✅
