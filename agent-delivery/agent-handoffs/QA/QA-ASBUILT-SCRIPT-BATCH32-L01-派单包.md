# 派单包：QA-ASBUILT-SCRIPT-BATCH32-L01

- **监管**：`human:黄敬洲`
- **执行**：`qa-agent`（子 agent 按模块隔离）
- **状态**：`in_progress`
- **强度**：ponytail full（写脚本；不缩 D8/D9/D10/规约）

## 1. 目标（本阶段）

对 catalog **剩余 32 个 live 入口**编写 as-built **测试脚本**（B 线第 2 步）。

| 做 | 不做 |
|----|------|
| 读已有人读用例 → 译脚本 | 不重写用例册 |
| **无头独立 Chromium 实勘**（`tools/survey-page.mjs`）取 locator 并修订 | **禁止** IDE/`cursor-ide-browser`/`user-playwright` 共享有头浏览器 |
| `gold.yaml` + `scripts.yaml` + `coverage.md` + `fixtures/`（可选 `full.md`） | **禁止** `run-scripts.mjs` 全量跑批 / 新建 `runs/` 执行目录 |
| 回填用例「自动化用例ID」列 | 不改业务仓；金样条数不强制 5 |

## 2. 必读

- `qa/as-built/prompts/_script.md`（含 P1–P8、expect 双层、母表闸门）
- `qa/as-built/schema.md`
- 样板：`qa/as-built/scripts/KJZTFWXT/enterprise/key-type/`（质量参考，勿抄 SEARCH 旧坑）
- 环境：http://111.198.38.90:50892/ · admin / 123456

## 3. 已完成（勿重复）

| entry_id | 脚本目录 |
|----------|----------|
| ent-search | `as-built/scripts/KJZTFWXT/enterprise/search/` |
| ent-key-type | `as-built/scripts/KJZTFWXT/enterprise/key-type/` |

## 4. 剩余 32 清单

### enterprise（9）

| entry_id | 标题 | 用例路径（相对 `qa/test-cases/`） | 建议脚本目录 |
|----------|------|----------------------------------|--------------|
| ent-key-domain | 重点企业领域分析 | `KJZTFWXT/enterprise-企业分析/KEYDOM-重点企业领域分析/FUNC-重点企业领域分析-用例.md` | `scripts/KJZTFWXT/enterprise/key-domain/` |
| ent-eval-tech | 企业技术力评估对比分析 | `…/EVALTECH-企业技术力评估对比分析/…` | `…/enterprise/eval-tech/` |
| ent-eval-business | 企业商业力评估对比分析 | `…/EVALBIZ-…` | `…/enterprise/eval-business/` |
| ent-eval-compete | 企业综合竞争力评估 | `…/EVALCOMP-…` | `…/enterprise/eval-compete/` |
| ent-sz-status | 深圳企业现状分析 | `…/SZSTATUS-…` | `…/enterprise/sz-status/` |
| ent-attract | 招引企业推荐分析 | `…/ATTRACT-…` | `…/enterprise/attract/` |
| ent-cultivate | 培育企业推荐分析 | `…/CULTIVATE-…` | `…/enterprise/cultivate/` |
| ent-supply | 企业供应链关系分析 | `…/SUPPLY-…` | `…/enterprise/supply/` |
| ent-pain | 企业发展痛难点分析 | `…/PAIN-…` | `…/enterprise/pain/` |

### industry-center（11）

| entry_id | 标题 | 建议脚本目录 |
|----------|------|--------------|
| chain-overview | 专题全景 | `scripts/KJZTFWXT/industry-center/overview/` |
| chain-search | 产业查询 | `…/industry-center/search/` |
| chain-panorama | 产业链全景图谱 | `…/panorama/` |
| chain-cycle | 产业周期分析 | `…/cycle/` |
| chain-regional-index | 区域产业指数评价 | `…/regional-index/` |
| chain-key-link | 产业关键环节识别 | `…/key-link/` |
| chain-bottleneck | 产业瓶颈堵点识别 | `…/bottleneck/` |
| chain-sz-compare | 深圳产业情况分析对比 | `…/sz-compare/` |
| chain-sz-dev | 深圳产业发展分析 | `…/sz-dev/` |
| chain-regional-compete | 区域产业竞争力评价 | `…/regional-compete/` |
| chain-maintenance | 维护管理 | `…/maintenance/`（用例=`CHAINMAINT-维护管理`） |

### service（11）

| entry_id | 标题 | 建议脚本目录 |
|----------|------|--------------|
| svc-portal | 专题服务 | `scripts/KJZTFWXT/service/portal/` |
| svc-search | 服务机构查询 | `…/service/search/` |
| svc-org-field | 服务机构产业领域分析 | `…/org-field/` |
| svc-org-trend | 服务机构新增趋势分析 | `…/org-trend/` |
| svc-org-capability | 服务机构技术力评估分析 | `…/org-capability/` |
| svc-chain-shortboard | 服务链短板分析 | `…/chain-shortboard/` |
| svc-chain-graph | 服务链图谱分析 | `…/chain-graph/` |
| svc-rec-attract | 引入服务机构推荐分析 | `…/rec-attract/` |
| svc-rec-cultivate | 培育服务机构推荐分析 | `…/rec-cultivate/` |
| svc-sz | 深圳服务链现状分析 | `…/sz/` |
| svc-maintenance | 维护管理 | `…/maintenance/`（用例=`SVCMAINT-维护管理`） |

### shell（1）

| entry_id | 标题 | 用例 | 建议脚本目录 |
|----------|------|------|--------------|
| shell-compare-basket | 系统对比篮 | `…/COMPARE-对比篮/FUNC-对比篮-用例.md` | `scripts/KJZTFWXT/shell/compare-basket/` |

## 5. 执行纪律

1. **写稿并发 ≤4；实勘用无头独立进程（可并行）**：每人自启 `tools/survey-page.mjs`（headless Chromium），**禁止**共享 IDE/`cursor-ide-browser`/`user-playwright` MCP（会抢焦点）。
2. 同波次模块目录互斥，禁止并行改同一 yaml。
3. 同路由兄弟脚本**只写本 entry**。
4. catalog 补 `scripts`/`gold`/`full_scripts`，**禁止改 entry id**。
5. 完成后 §6 打勾；父任务勿自行 `done`。
6. **子 agent 必须用 §7 提示词模板**。

> **2026-10-14**：W1 四路抢有头浏览器已打断 → 改 **无头探针并行**（`survey-page.mjs` 冒烟通过）。

## 7. 子 agent 提示词模板（强制）

派单时把下方整段复制，只替换 `【】` 占位。禁止只丢一句「去写某某脚本」。

```text
【身份】你是 qa-agent 子执行臂。父单 QA-ASBUILT-SCRIPT-BATCH32-L01，监管 human:黄敬洲。
工作根：/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
只改编排仓 agent-delivery/qa/ 下本模块相关文件。

【唯一任务】为 catalog entry_id=【ENTRY_ID】编写 as-built 测试脚本（B 线第 2 步）。
标题：【TITLE】
路由：【PATH】【QUERY】
人读用例（唯一蓝本）：【CASE_MD 绝对路径】
落盘目录（只许写这里）：【SCRIPTS_DIR】
样板（只读对照，勿抄错 entry）：agent-delivery/qa/as-built/scripts/KJZTFWXT/enterprise/key-type/
规约（必读）：agent-delivery/qa/as-built/prompts/_script.md 、 schema.md

【必须产出】在落盘目录创建/覆写：
1) gold.yaml — 金样冒烟（条数不强制 5；选可测主路径；id 用 P0-01…；func_id=用例编号）
2) scripts.yaml — includes 金样 + 其余；顶层键 scripts:；与用例尽量 1:1
3) coverage.md — 主表：脚本id → 用例编号 → 区块 → P → 可见动作；未脚本化须写原因
4) fixtures/testdata.yaml — base_url=http://111.198.38.90:50892/ 、admin/123456、本页可见默认文案与 selector 口径
5) 可选 prompts/.../full.md — 仅执行顺序与易错点
6) 回填用例册「自动化用例ID」列；catalog KJZTFWXT.yaml 本 entry 补 scripts/gold/full_scripts 路径（禁止改 id）
7) expect 必须双层 {note, assert}；禁止新写裸字符串 expect

【做法（按序，不可跳）】
A. 通读用例册全部用例，列清单（编号/标题/优先级），决定金样子集与全量脚本列表
B. **无头实勘（强制）**：在 `agent-delivery/qa/as-built/tools/` 执行  
   `node survey-page.mjs --path '【PATH_WITH_QUERY】' --out '../scripts/【相对SCRIPTS_DIR】/fixtures/scout'`  
   （浮层入口可加 `--click '对比篮'` 等）。读生成的 scout.md / scout.json / page.png，locator 以实勘为准（P1/P7）。需要二次探测可再跑探针，**不要**开 IDE 浏览器。
C. 按 _script.md P1–P8 写 yaml；业务态断言前关「内部评审模式」（aria-label，勿 first() 盲点）
D. 同路由兄弟功能不要写进本套（本 entry 隔离）
E. 写完自检：每条自动化用例有 ≥1 脚本，或 coverage 声明不自动化原因；func_id 尾号与用例一致
F. 交卷：列产出路径、脚本条数、未脚本化清单、as_built_note 偏差；停止

【允许】
- 读用例 / 规约 / key-type 样板 / catalog
- 运行 `tools/survey-page.mjs`（及同目录下你为二次探测写的一次性 headless 小脚本，产出仍落本模块 fixtures/）
- 写/改本模块 scripts 目录、fixtures、可选 full.md、用例自动化ID列、catalog 本 entry 的 scripts 字段
- 金样条数按可测主路径裁

【禁止 — 违反即失败】
- **禁止** cursor-ide-browser / user-playwright / 任何有头共享 MCP 浏览器
- 禁止 run-scripts.mjs 全量跑批、禁止新建 runs/ 执行目录
- 禁止改业务仓、禁止改其他模块脚本、禁止动 ent-search / ent-key-type
- 禁止重写用例正文（只许回填自动化用例ID列）；禁止改 catalog entry id
- 禁止把 P0-xx 写成用例编号；func_id 必须是 ZNFWJQ-...-FUNC-xxxxx
- 禁止发明用例没有的断言；禁止 1 脚本吞 2 条用例判定
- 禁止 git commit / push / 改 task-registry / 推进父单状态
- 禁止并行改其他 entry；本任务只做【ENTRY_ID】
- 做完就停，不要修 runner、不要改 schema/_script.md
```

## 6. 进度

| 波次 | 模块 | 状态 | 备注 |
|------|------|------|------|
| W1 | ent-key-domain | ✅ 交卷 | 20 条 1:1；P1-04 manual+allow_skip |
| W1 | shell-compare-basket | ✅ 交卷 | 29/30；00510 权限未脚本化；政策 Tab 缺 |
| W1 | chain-search | ✅ 交卷 | 17 条 1:1；P0-11 空搜缺陷预期红；P0-08 allow_skip |
| W1 | svc-search | ✅ 交卷 | 23 条 1:1；示例仅回填等偏差 |
| W1b | ent-eval-tech | ✅ 交卷 | 30 条；预检失败→开始分析禁用 allow_skip |
| W1b | ent-eval-business | ✅ 交卷 | 30 条；预检失败链 allow_skip |
| W1b | ent-eval-compete | ✅ 交卷 | 35 条；结果态 allow_skip |
| W1b | ent-sz-status | ✅ 交卷 | 19 条；无 chip 改下拉验收 |
| W1b | ent-attract | ✅ 交卷 | 25 条；招引候选入口 allow_skip |
| W1b | ent-cultivate | ✅ 交卷 | 28 条；分析失败链 allow_skip |
| W1b | ent-supply | ✅ 交卷 | 24 条；关键节点空等 allow_skip |
| W1b | ent-pain | ✅ 交卷 | 30 条；enterprise 批次已齐 |
| W2 | chain-overview | ✅ 交卷 | 17 条；默认已选三级非空态 |
| W2 | chain-panorama | ✅ 交卷 | 15 条；生物组合可能 INPUT_OBJECT_INVALID |
| W2 | chain-cycle | ✅ 交卷 | 16 条；空对象拦截非置灰 |
| W2 | chain-regional-index | ✅ 交卷 | 16 条；自定义态权重粘滞 allow_skip |
| W2 | chain-key-link | ✅ 交卷 | 23 条；排序控件未见 allow_skip |
| W2 | chain-bottleneck | ✅ 交卷 | 25 条；过程/结果多 allow_skip |
| W2 | chain-sz-compare | ✅ 交卷 | 22 条；开始分析常禁用 allow_skip |
| W2 | chain-sz-dev | ✅ 交卷 | 25 条；单级产业下拉；结果 allow_skip |
| W2 | chain-regional-compete | ✅ R3 金样绿 | 5/5；run regional-compete-r3-runner |
| W2 | chain-maintenance | ✅ 交卷 | 19 条；追溯弹层需 Esc → 待 R3 回炉 |
| W3 | svc-portal | ✅ 交卷 | R1 金样绿 |
| W3 | svc-org-field | ✅ R3 金样绿 | 5/5；run org-field-r3-runner |
| W3 | svc-org-trend | ✅ R3 金样绿 | 5/5；run org-trend-r3-runner |
| — | svc-org-capability | ✅ R3 金样绿 | 闸门 fail→配置 A 4/4；run org-capability-r3-runner |
| — | svc 其余 6 | 🔄 R3 | 未铺：shortboard/graph/rec-attract/rec-cultivate/sz/maintenance |

## 8. 方法论补丁 + 回炉试点（2026-10-14 19:14）

- 真源：`qa/as-built/retro/20261014-batch32-method-patch.md`（双档 A/B、**cases-v1 一用例一文件**、skip 配额、环境闸门、探针公约、catalog 父挂）
- `_script.md` / `schema.md` 已同步；**存量已全量拆 cases-v1**（25/577；catalog 已改挂；runner 仅新布局）
- `_script.md` 已加 §4 摘要指向补丁

| 试点 | entry_id | 状态 | 目标 |
|------|----------|------|------|
| R1 enterprise | ent-eval-tech | ✅ 金样绿 | 5/5；ids P0-01~05；env-gate fail→仅配置/空态；run eval-tech-r3-runner |
| R1 industry | chain-bottleneck | ✅ 金样绿 | 5/5；ids P0-01~05；B skip 3/13≤25%；run bottleneck-r3-runner |
| R1 service | svc-portal | ✅ 金样绿 | 5/5；ids P0-01,07,08,10,09；run portal-r3-runner |

## 9. 回炉波 R2（2026-10-14 20:40）

**策略**：模块闸门一次 → 子 agent **一用例一闭环**（写/实勘/修订/`--only` 试跑）→ 父串行验金样。无头探针；并发写稿 ≤4；金样机跑串行。

| 入口 | entry_id | skip 现状 | 路由 | 阶段 |
|------|----------|-----------|------|------|
| `enterprise/pain` | ent-pain | 25/30≈83% | `/enterprise/risk?workspace=pain-points&tab=pain-points` | ✅ 金样绿 4/4（P0-01,07,11,04） |
| `enterprise/eval-business` | ent-eval-business | 14/30≈47% | `/enterprise/evaluation?workspace=business&mode=business` | ✅ 金样绿 4/4（P0-01~04；env-gate fail→仅配置态） |
| `enterprise/search` | ent-search | 13/41≈32% | `/enterprise/enterprise-search` | ✅ 金样绿 5/5（P0-01~05；run search-r3-runner；P0-05 须开评审才渲 ⓘ） |

**进度快照（每完成一项更新）**：入口父验绿 **3/3** · 金样用例父验通过 **13/13** · R2 收口 · ⏳待派 **0**

**R2 收口注记（2026-10-14 21:34）**：search 父串验 `pass=5`；末条 P0-05 根因 = `MetricSpecCard` 仅 `reviewMode` 渲染且 `trigger=hover`，断言改为开内部评审→evaluate scroll→hover ⓘ→关评审查泄漏。

**本波目标（每入口）**：`env-gate.json` + A 档 3～5 条零 skip 且父验绿；B 档 skip≤25%+ticket（可砍「本轮不自动化」）。cases-v1 已就位，只改 `cases/*.yaml` / `index.yaml` / `coverage.md` / fixtures。

**§7 旧提示词已过时**（仍写 gold.yaml/scripts.yaml）；R2 子派单用下方模板。

### 9.1 模块闸门子任务模板

```text
【身份】qa-agent。父单 QA-ASBUILT-SCRIPT-BATCH32-L01。回炉波 R2 · 仅模块闸门。
工作根：/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
【任务】entry=【ENTRY】 目录=agent-delivery/qa/as-built/scripts/KJZTFWXT/【DIR】/
路由：【PATH】
1) 无头 survey-page.mjs（及必要二次探针）→ fixtures/scout/
2) 写 env-gate.json（overall + gates + tickets）；对照 method-patch §3
3) 读现有 index.yaml gold + cases，建议：保留/降 B/替入金样的 id 列表（只建议，不改脚本）
4) 交卷：overall、tickets、建议金样 ids、禁止进金样的原因；停止
禁止：改 cases 内容、改 catalog、有头浏览器、run-scripts 全量、git
```

### 9.2 单用例回炉模板

```text
【身份】qa-agent。父单 QA-ASBUILT-SCRIPT-BATCH32-L01。R2 · 一用例一脚本。
工作根：同上。只改【DIR】/cases/【CASE_ID】.yaml（必要时 index.yaml 的 gold/all、coverage 该行）。
蓝本用例：【FUNC_ID】（用例册路径【CASE_MD】）
env-gate：已存在 fixtures/scout/env-gate.json（overall=【OVERALL】）——过程/结果态是否可写以闸门为准。
做法：读现有 case → 无头实勘本条路径 → 修订 expect 双层 → node run-scripts.mjs ../scripts/KJZTFWXT/【DIR】 --only 【CASE_ID】 自验
A 档禁止 allow_skip；B 档 skip 必须 ticket。禁止改其他 case、catalog、有头浏览器、全量跑批。交卷列自跑 verdict；停止。
```

## 10. 整单铺开 R3（2026-10-14 21:40 · 方法论生效后续派）

**策略同 R2**：模块闸门一次 → 子 agent 一用例一闭环（≤4 并发）→ 父串行验金样。cases-v1；A 零 skip；B skip≤25%+ticket。禁止有头浏览器 / 全量跑批 / 改业务仓 / git。

### 10.1 已达标（A 金样父验绿 · 6）

| 入口 | 金样 | 来源 |
|------|------|------|
| `enterprise/eval-tech` | 5/5 | R1 |
| `industry-center/bottleneck` | 5/5 | R1 |
| `service/portal` | 5/5 | R1 |
| `enterprise/pain` | 4/4 | R2 |
| `enterprise/eval-business` | 4/4 | R2 |
| `enterprise/search` | 5/5 | R2 |
| `service/org-field` | 5/5 | R3 |
| `service/org-capability` | 4/4 | R3（闸门 fail·仅配置） |
| `industry-center/regional-compete` | 5/5 | R3 |
| `service/org-trend` | 5/5 | R3 |
| `service/chain-shortboard` | 5/5 | R3·W2 |
| `service/chain-graph` | 5/5 | R3·W2（hang 空禁点边） |
| `service/rec-attract` | 5/5 | R3·W2 |
| `service/rec-cultivate` | 5/5 | R3·W2 |
| `service/sz` | 5/5 | R3·W2（结果态走历史） |
| `service/maintenance` | 5/5 | R3·W2（占位壳） |

### 10.2 待办队列

**W0/W2 新写**：✅ 已全部金样父验绿（上表）。

**W1 回炉**：✅ 已并入基线（高 skip 入口已回炉）。

### 10.3 进度快照

入口父验绿 **34/34** · 金样用例父验通过 **167** · **W2 收口** · 六入口金样齐（shortboard/graph/attract/cultivate/sz/maintenance）· 待：catalog 批量挂 scripts/gold（父）· B 档 skip 清理可另开

### 10.4 金样之后：FUNC 1:1 脚本补齐（另开对话）

金样收口 ≠ 774 用例全脚本化。B 档补齐编排真源（含新对话 Kickoff、父/子模板、gap 工具）：

`agent-delivery/qa/as-built/script-backfill-playbook.md`

缺口快照（工具生成）：`agent-delivery/qa/as-built/script-backfill-gap-KJZTFWXT.md`
