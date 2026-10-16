# 专题服务门户 脚本→用例 覆盖表（2026-10-14 BATCH32 回炉 · svc-portal · r3；2026-10-15 P0-06 补齐）

蓝本 = `qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCPORTAL-专题服务门户/FUNC-专题服务门户-用例.md` v2.0（01306~01327，22 条）。
闸门 = `fixtures/scout/env-gate.json`（overall=**pass**，无头 `_env-gate-probe.mjs`）。
方法论 = `as-built/retro/20261014-batch32-method-patch.md`。
回修依据 = `runs/20261014-50892-portal-r3-runner/`（P0-07 strict×2；P0-04 step-click 超时 + 排行 heading 超时）。
P0-06 补齐 = `runs/20261015-50892-portal-p006-r2/`（verdict=**n/a**，skip 证据链见 scripts/P0-06/observed.yaml + fixtures/scout/probe-p006*.json/png）。

| 汇总 | 值 |
|------|-----|
| A 档金样 | **5**：`P0-01,P0-07,P0-08,P0-10,P0-09` · **零 allow_skip** |
| B 档机检 | **12**（含降档 P0-04 与新写 P0-06）· skip 1 条（P0-06 挂 ENV 票） |
| 机检合计 | **17** · skip 占比 **1/17 ≈ 5.9% ≤25%** |
| 本轮不自动化 | **5**（条条有 ticket） |
| catalog | **未改** |

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 档(A/B) | 页面区块/状态 | P | skip ticket | 可见动作 |
|---------|----------|---------|---------------|---|-------------|---------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01306 | A | 入口·路由/页头/五 Tab | P0 | — | goto /service-portal |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01307 | A | 五 Tab 互斥切回 | P0 | — | 轮切四 Tab→概况（heading 限 main） |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01308 | A | 筛选·链初始禁用 | P0 | — | 点产业链 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01310 | A | 概况·KPI+三区块 | P0 | — | 默认态核对 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01309 | A | 筛选·产业级联解锁 | P0 | — | 选产业→展链（r3 替入） |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01314 | B | 区域·两级视图+排行 | P0 | — | evaluate 进 region-map（r3 自 A 降） |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01311 | B | 概况·三图表+规模空态 | P0 | — | 览三区块 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01312 | B | 产业分布·六类+环节空 | P0 | — | 选产业→切 Tab |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01316 | B | 技术能力·口径+诚实空榜 | P0 | — | 切技术能力 Tab |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01318 | B | 深圳·右上分流+四区壳 | P0 | — | 点页头按钮 |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01319 | B | 深圳·重点机构墙空态 | P0 | — | 滚动重点板块 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01321 | B | 筛选·共用重算持久化 | P0 | — | 换产业+切 Tab+reload |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01313 | B | 产业分布·环节下钻开抽屉 | P0 | `ENV-SVC-PORTAL-STAGE-EMPTY`（n/a，r2） | 深链选产业→点环节卡→点机构名（环节区诚实空 skip；stages 到位后实跑） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01315 | B | 区域·圆点点选联动列表高亮 | P0 | `ENV-SVC-PORTAL-MAP-NO-COORD`（n/a，写稿自检） | 深链 region-map→点圆点→核梯度/图例/列表高亮（圆点诚实空 skip；坐标到位后实跑） |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01317 | B | 技术能力·前三金银铜+在库不足诚实标注 | P0 | `ENV-SVC-PORTAL-TECH-RANK-EMPTY`（n/a，写稿自检） | 深链 capability-rank→核前三配色/第4普通色+在库标注（榜诚实空 skip；有入榜后实跑） |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01320 | B | 深圳·重点机构详情抽屉四板块 | P0 | `ENV-SVC-PORTAL-KEY-ORG-EMPTY`（n/a，写稿自检） | 深链 shenzhen→点重点机构卡→核抽屉四板块依序（墙诚实空 skip；有卡后实跑） |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01323 | B | 深圳·机构参数分享恢复 | P1 | `ENV-SVC-PORTAL-KEY-ORG-EMPTY`（n/a，写稿自检） | 点卡写 ?org=→深链复进开抽屉→关闭清参回焦（墙诚实空 skip；有卡后实跑） |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01326 | B | 筛选·无映射产业空态不回落 | P1 | `ENV-SVC-PORTAL-NO-UNMAPPED-CLUSTER`（n/a，写稿自检） | 扫十五集群找无链映射→核「无相关产业数据」+产业不回落（本轮均有链 skip；有无映射后实跑） |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01322 | B | 技术能力·产业切换 | P1 | — | 切换产业下拉 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01324 | B | 评审·角标+追溯 | P1 | — | 开评审→点角标 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01325 | B | 评审·未登记+零泄漏 | P1 | — | 关评审→五 Tab 扫 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01327 | B | 异常·非法机构参 | P1 | — | goto 非法 orgId |

## 本轮不自动化（原 allow_skip → 声明 + ticket）

| 用例编号 | 原脚本 | 原因 | ticket |
|----------|--------|------|--------|
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01320 | P0-06（旧占位）→ **P0-13 已脚本化** | 重点机构墙诚实空，无法开抽屉；2026-10-15 落盘 P0-13（allow_skip n/a） | `ENV-SVC-PORTAL-KEY-ORG-EMPTY` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01315 | P0-12（旧占位）→ **P0-11 已脚本化** | 地图无坐标，圆点不可点；2026-10-15 落盘 P0-11（allow_skip n/a） | `ENV-SVC-PORTAL-MAP-NO-COORD` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01317 | P0-13（旧占位）→ **P0-12 已脚本化** | 技术力榜诚实空，无法验金银铜；2026-10-15 落盘 P0-12（allow_skip n/a） | `ENV-SVC-PORTAL-TECH-RANK-EMPTY` / `Q060` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01323 | P1-02（旧占位）→ **P0-17 已脚本化** | 重点机构墙诚实空，无法点卡写参分享；2026-10-15 落盘 P0-17（allow_skip n/a） | `ENV-SVC-PORTAL-KEY-ORG-EMPTY` |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01326 | P1-05（旧占位）→ **P0-18 已脚本化** | 十五集群均有链，未见「无相关产业数据」；2026-10-15 落盘 P0-18（allow_skip n/a） | `ENV-SVC-PORTAL-NO-UNMAPPED-CLUSTER` |

> 2026-10-15 更新：01313（环节下钻）已由 P0-06 脚本化（skip n/a 挂 `ENV-SVC-PORTAL-STAGE-EMPTY`，见主表）；01315（圆点点选）已由 P0-11 脚本化（skip n/a 挂 `ENV-SVC-PORTAL-MAP-NO-COORD`，见主表；用例册列旧占位 P0-12）；01320（重点机构抽屉四板块）已由 **P0-13** 脚本化（skip n/a 挂 `ENV-SVC-PORTAL-KEY-ORG-EMPTY`，见主表；用例册列旧占位 P0-06 撞号已让位）。注意：用例册 01317 行仍写自动化 ID=P0-13（BATCH32 占位）——实档为 P0-12，需父 agent 回填列。

## r3 回修纪要

| id | 动作 |
|----|------|
| P0-07 | `getByRole('heading')` → `locator('main').getByRole(..., { exact: true })`；先等 URL |
| P0-04 | 移出金样→B；step 改 evaluate（runner 无 portal tab 词表）；排行 `main`+exact |
| P0-09 | 升入金样（筛选级联，与已绿 P0-08 同闸门 G3） |

## as-built 偏差（D1/D2）

| 脚本 | 用例 | 级 | 偏差 |
|------|------|----|------|
| P0-10 | 01310 | **D1** | 「覆盖产业领域数」→「环节合计（可重复计）」 |
| P0-04 | 01314 | **D1** | 「全球分布/全国分布」→「全球视图/全国视图」 |
| P0-14 | 01318 | **D1** | 深圳 KPI as-built 文案 |
| P0-03 | 01312 | **D2** | 六类/环节/热力三区，非单链路图 |
| P1-01 | 01322 | **D2** | 共用产业下拉，非独立 chip |
| P0-06 | 01313 | **D2 前瞻**（源码静读未实证） | 环节卡点击=跳分析侧（openStage→/service/chain-analysis?workspace=chain&segment=…），未见「展开代表机构列表」承载；stages 到位后实跑按 D3-SVCPORTAL-STAGE-DRILL-MISSING 或 D2 归票（详见 cases/P0-06.yaml as_built_note ②） |

## 2026-10-15 P0-06 补齐纪要（脚本补齐波）

- **r2 实跑**：verdict=**n/a**（allow_skip 命中 `.svc-portal-stage-card` 5s 不可见）；证据链 `fixtures/scout/probe-p006{,b,c,d}.json` + 4 张截图 + `runs/20261015-50892-portal-p006-r2/scripts/P0-06/observed.yaml`；ticket `ENV-SVC-PORTAL-STAGE-EMPTY`。
- **落局**：④ 环节区诚实空——POST industry-distribution 双参 stages=[]（接口 200、六类 6 行有数=链路通），环境数据债非页面缺陷。
- **⚠ 存量隐患回报（父 agent 处置）**：portal/ 存量 16 条 case（P0-01~05、P0-07~16、P1-*）steps/expect 列表为**列 0 缩进**（2026-10-14 20:21 批量重写所致），runner 极简 YAML 解析器**静默截断** → `runs/20261014-50892-portal-r3-runner`（20:22 波）pass 条均为「0 项机检断言通过」假绿、steps.md 空；19:24/19:28 两波（2 空格缩进期）为真跑。修复=存量 case 转列 2 空格缩进 + 金样重验；本波按铁律未改前作。chain-graph/sz/rec-cultivate 等入口无此问题。

## 2026-10-15 存量缩进修复 + 金样重验纪要（修复波）

- **修复**：16 条存量 case（P0-01~05、P0-07~10、P0-14~16、P1-01/03/04/06）`preconditions`/`steps`/`expect` 列表项**列 0 → 2 空格**（2026-10-14 20:21 批量重写所致缩进缺陷；蓝本 P0-06 未动）。脚本级自检：修复前后逐行内容（strip 前导空格）完全相等，diff 为纯缩进+结构行变化。
- **附带必要修复（2 处，超出纯缩进，如实记录）**：P0-02/P0-10 各一条 `assert` 为 YAML 单引号标量内嵌 JS 单引号（`''heading''`）——同源批量重写损坏，`--check` 编译必炸；按最小等价改 JS 字符串单引号→双引号（语义不变），否则金样 P0-10 重验必然假红。
- **假绿波标注**：`runs/20261014-50892-portal-r3-runner`（20:22 波）pass 条均为「0 项机检断言通过」、steps.md 空——**该波 pass 判定作废**，以本轮重验波为准。
- **--check**：17 条（含 P0-06）assert 编译错误 **0**；每条解析出真实 steps(1~2)/expect(2~4)。
- **金样重验**：`runs/20261015-50892-portal-gold-reverify`（--only P0-01,P0-07,P0-08,P0-10,P0-09，headless，baseline=假绿波）→ **5/5 pass，每条 3 项机检断言通过**（真断言），steps.md 非空、逐条 ✓、截图 2 张/条；COMPARISON 与假绿波 verdict 5/5 一致（pass↔pass，本轮补齐断言证据）。
- **B 档非金样 11 条**：只修缩进不重跑（铁律）；--check 全量已覆盖编译校验。

## 2026-10-15 P0-17 补齐纪要（脚本补齐波 · FUNC-01323）

- **落盘**：`cases/P0-17.yaml`（B 档，allow_skip + `ENV-SVC-PORTAL-KEY-ORG-EMPTY`）；`index.yaml` all 增 P0-17（未动 gold）；参数名 as-built=`org`（D1）。
- **无头探针**：`fixtures/scout/_probe-p017.mjs` → `probe-p017.json`（card=0、empty、?org=org-live-1 toast 清参）。
- **写稿自检**：见交卷说明（不算正式验收）。

## 2026-10-15 P0-18 补齐纪要（脚本补齐波 · FUNC-01326）

- **落盘**：`cases/P0-18.yaml`（B 档，allow_skip + `ENV-SVC-PORTAL-NO-UNMAPPED-CLUSTER`）；`index.yaml` all 增 P0-18（未动 gold）；筛条 locator=nth(0/1)（D1）。
- **无头探针**：`fixtures/scout/_probe-p018.mjs` + `_probe-p018b.mjs` → `probe-p018.json` / `probe-p018b.json`（15 集群；INB1804 未来空间链=深海矿产；无「无相关产业数据」）。
- **偏差**：D4 环境债（无无映射集群）；D2 前瞻（空态文案未落地，见 case as_built_note）。
- **写稿自检**：见交卷说明（不算正式验收）。

## 父验收金样 ids

```
P0-01,P0-07,P0-08,P0-10,P0-09
```
