# As-built 脚本编排手册（FUNC ↔ scripts 1:1）

> **当前波（2026-10-19）**：专题用例册已对照重写。脚本按**现行用例号**重写，不沿用旧 `P0-*.yaml`。  
> **环境**：`https://edu.itic-sci.com/tts/svcz/`（路径前缀 /tts/svcz/）。禁止再写内网 `http://10.50.69.111:30892/`、`http://10.50.69.111:30888/` 或 `http://111.198.38.90:50892/`。  
> **路径**：`fixtures.base_url` = 上址；步骤 `goto` 写应用内相对路径，由 runner 拼成 `base_url + target`。  
> **路由真源**：`catalog/KJZTFWXT.yaml` 该 `entry_id` 的 `path`（有 `fixtures/entry-seed.yaml` 时以其 `catalog_path` 为准）。**禁止**用探针猜到的 URL 覆盖 catalog（教训：企业查询曾误写成 `/development/search`）。  
> **单条写法**：[`prompts/_script.md`](prompts/_script.md)。双档 / expect 双层仍读 [`retro/20261014-batch32-method-patch.md`](retro/20261014-batch32-method-patch.md) + [`schema.md`](schema.md)。  
> **下文 §2～§8** 是上一波「补齐缺口 + 写验分离」的记录。和文首冲突时，以文首为准。

---

## 重写波（现行）

父控只派单和改编排表。不写 yaml，不跑 `run-scripts`，不判断步骤对错，不把前置改写成点击。父控把该行的路由、前置、测试步骤、预期原样抄进子提示词。一条现行用例一个子 agent：写点击前只读 `repos/lumen-ui-topic` 里本条路由对应的一个页面文件 → 只按测试步骤写点击 → 只用 `run-scripts.mjs` 无头试跑（默认 `headless=true`）→ 红了只读 `steps.md`「失败时主区文字」，第二次可改失败的那条 assert，或按这段文字补上缺的一次点击。禁止第 3 次。禁止 IDE / MCP 浏览器，禁止有头 Chromium，禁止 `--headless false`，禁止 `survey-page` 或自写探针。登录和关评审由 runner 做。

旧脚本放弃。`func_id` 即使还能对上旧号或保留号，也不要改旧文件，不要把它的 assert 抄进新文件。新文件：

```text
as-built/scripts/KJZTFWXT/{script_rel}/cases/FUNC-xxxxx.yaml
```

`id` 与文件名相同（`FUNC-xxxxx`）。`func_id` 写完整用例号 `ZNFWJQ-KJZTFWXT-v1.0-FUNC-xxxxx`。试跑用 `--only FUNC-xxxxx`（runner 按文件 id 查找，不要求先写进 `index.all`）。子 agent **不要改** `index.yaml`、`coverage.md`、别的 case、catalog。

### 编排表

`as-built/script-rewrite-ledger-KJZTFWXT.csv`

| 列 | 谁改 | 含义 |
|----|------|------|
| `func_id` | 生成时固定 | 现行主表用例号 |
| `entry_id` / `script_rel` / `case_md` | 生成时固定 | 入口、脚本目录、用例册 |
| `status` | 父 | `pending` / `running` / `pass` / `fail` / `blocked` |
| `run_dir` | 父按子交卷抄入 | 试跑目录 |
| `note` | 父按子交卷抄一行 | 失败原因或写不出的原因，不展开步骤 |

中断后续跑：只读这张表。`pending` 和 `fail` 可以再派；`running` 若对话已死，改回 `pending` 再派。`pass` 不重派。不要用 `script-backfill-queue-*.md` 当本波派单表（那份会把旧脚本当成已覆盖）。

### 并发

同时 **6** 个子 agent。每条会起一个无头 Chromium，6 路大约占 2～3GB 内存，本机还能留给父对话。不要开到 20：浏览器和登录会话会互相拖慢，失败会变成环境红。某一路连续因超时失败，先降到 4，不要加并发。

同一 `script_rel` 可以并行，因为子 agent 只新增自己的 `FUNC-xxxxx.yaml`。

### Playwright 执行环境（父控先查，子 agent 不装）

试跑依赖 nvm 的 **Node v24**、`as-built/tools` 里的 `playwright`，以及本机已下载的 Chromium。新 shell 默认没有 `node`。这些只由**父控在派单前检查并修好一次**。子 agent 并行 `npm install` / `npx playwright install` 会抢下载、把同一条环境故障写成多条用例红。

检查与修复的命令以下面 Kickoff 的【Playwright】为准。未打印 `playwright-ok` 不得派子 agent。子 agent 只允许 `nvm use 24` 后调用已经装好的 `run-scripts.mjs`；起不来就 `blocked`，`note=ENV-PLAYWRIGHT`，把环境交回父控。

### 入口 seed · 路由闸门 · 点状复勘（2026-10-20）

批量慢、路由漂，根因多半是子 agent **边写边全页探、用探针 URL 覆盖 catalog**。本波强制：

| 机制 | 谁维护 | 子 agent 怎么用 |
|------|--------|-----------------|
| **入口 seed** | 父控按入口建一次，并把字段抄进每条子提示词 | 子 agent 不打开 seed。`goto` / `waitForURL` 只用提示词里的 `catalog_path` |
| **路由闸门** | seed 内 `catalog_path` + `forbidden_paths` | 落盘前自检：脚本里不得出现 `forbidden_paths`；`testdata.route` = `catalog_path` |
| **点状核对** | 子 agent 不另开浏览器 | 按钮名、列名、chip 以父控抄来的步骤原文和试跑 `steps.md`「失败时主区文字」为准。禁止为核对再开 IDE / 有头浏览器 |

`entry-seed.yaml` 最小字段：

```yaml
entry_id: ent-search
catalog_path: /enterprise/enterprise-search   # = catalog.path，唯一深链真源
menu_path: [企业分析, 企业查询]
menu_leaf: 企业查询
sibling_for_sidebar_entry: /enterprise/attraction  # 「侧栏进入」类：先 goto 兄弟页再点菜单
forbidden_paths:
  - /development/search
  - /enterprise-center/overview
```

规则：

1. **深链用例**：`goto` / `testdata.route` = `catalog_path`。
2. **侧栏进入用例**：`goto sibling_for_sidebar_entry`，再点 `menu_leaf`；`waitForURL` 仍对 `catalog_path`。
3. 探针 URL ≠ `catalog_path`：只写 `as_built_note`，**禁止**把脚本路由改成探针值。
4. 某入口还没有 seed：父控从 `catalog/KJZTFWXT.yaml` 抄 `path` / `menu_path` 写入 seed（仅当文件不存在），再把字段抄进子提示词。子 agent 不打开 catalog，不改已有 `catalog_path`。
5. 参考样例：`scripts/KJZTFWXT/enterprise/search/fixtures/entry-seed.yaml`。

### 回炉

子 agent **自己**把本条改成 `fail` 或 `blocked`（见下「自己落表」）。父不改脚本。

- 环境缺口（`ENV-`、D3、现场无数据、条数不够、按钮不可达，且脚本已落盘）：子 agent 直接写 `blocked`，父不要回炉。
- 脚本本身写错（路由、空断言、可重试超时）：同一条最多回炉 1 次，提示词带上 `note`。第二次仍是环境缺口就改 `blocked`。

写不出稳定断言：`status=blocked`，`note` 写缺什么。不算 pass。

### 循环为什么会停（2026-10-20）

父控一轮回复结束、且没有在飞的子 agent 时，没有人再唤醒它。两次实停都是这个：

1. 落完表后写「下一批从某某起，说继续再派」，本轮没有调用子 agent。
2. 给子 agent 加了 `no ledger`。子 agent 已经交卷，表仍是 `running`，父控对话又没写下一条回复，槽就永远满着。

提示词挡不住系统注入的 “no follow-up needed”。父控把 `running=0` 说成「无需再改表」就会结束本轮，即使 `pending` 还有一千多条。原先用来在对话结束时自动补派的 `.cursor/hooks/rewrite-loop-stop.py` 已删除：它只认旧父控对话，路径也写死在另一台机器上，开关文件不存在，实际不会触发。

对策在 [`prompts/rewrite-wave-parent.md`](prompts/rewrite-wave-parent.md)：

- 子 agent 交卷前**自己改自己那一行**（文件锁，只动本条）。父控死了，表也不会停在 `running`。
- 父控每次回复的**最后一个动作**必须是派子 agent（待派>0 且未满父控文件里的并发）。禁止用进度小结收尾。系统若说 “no follow-up needed”：只要待派>0，就还有后续，必须派。

### 0. 父控与子 agent 提示词

全文在文件里，对话里不要再贴一份。

| 角色 | 文件 | 用法 |
|------|------|------|
| 父控 | [`prompts/rewrite-wave-parent.md`](prompts/rewrite-wave-parent.md) | 新对话只说：读取并执行该文件 |
| 子 agent | [`prompts/rewrite-wave-child.md`](prompts/rewrite-wave-child.md) | 父控从【身份】起整份下发，只替换【】 |

本波的并发 3、只派还没有 yaml 的 pending、无头探活、子提示词要填的路由 / 前置 / 步骤 / 预期，以父控文件为准。它覆盖本节「同时 6 个」和「fail 可再派」。子 agent 不读本 playbook。

---

## 1. 问题定义与口径

| 口径 | 含义 | 真源 |
|------|------|------|
| **FUNC 条数** | 人读用例主表行（`ZNFWJQ-…-FUNC-xxxxx`） | `qa/test-cases/{系统}/**/FUNC-*-用例.md` |
| **脚本条数** | `cases/*.yaml` 文件数 | `qa/as-built/scripts/{系统}/**/cases/` |
| **缺口 GAP** | 有 FUNC、无 `func_id` 命中脚本 | `tools/gap-func-vs-scripts.py` |
| **回炉 REWORK** | 已有 `cases/*.yaml` 但结构半成品/漂移 | `tools/health-cases.py`（`--write` 时自动跑） |
| **派单队列** | REWORK ∪ GAP，去重，回炉优先 | `script-backfill-queue-{系统}.md` |
| **金样 A** | `index.yaml` → `gold:` | 已绿的不重写；补齐波默认**不扩 gold**，除非缺 A 或 A 红 |
| **全量 B** | `all:` / 其余 cases | 本手册主战场 |

**与 BATCH32 金样铺开的关系**：入口金样父验绿（如 34/34·167）≠ 用例 1:1。金样收口后用本手册做 **B 档补齐**；不要再开「只写 5 条冒烟」的派单。

**目标态**：对本系统 live catalog 入口，`脚本条数 ≥ 本轮要自动化的 FUNC 条数`；未自动化须在 `coverage.md` 声明原因 + ticket（计入 skip 配额，见 method-patch §2）。

---

## 2. 角色、粒度与并发（上一波，重写波不沿用）

> 重写波的角色和并发见文首。本节留下只为对照旧补齐波。

### 2.0 粒度铁律（与 BATCH32 R2/R3 相同）

| 子任务类型 | 粒度 | 说明 |
|------------|------|------|
| **写/改脚本** | **1 Task = 1 CASE_ID = 1 FUNC_ID** | 只允许一个 CASE/FUNC；交卷后停止 |
| **独立验收** | **1 Task = 1 CASE_ID** | 新会话；不改业务脚本（只读 + 机跑）；交卷停 |
| **模块闸门** | 1 Task = 1 入口 | 只写 `env-gate.json` + scout；**零** cases |

**明确禁止（常见偷懒）：**

1. 「补齐 `svc-xxx` 全部缺口」→ 一个子 agent  
2. 「本入口缺 18 条，你一并写完」→ 一个子 agent  
3. 写稿子交卷后自行读 gap 续写下一条  
4. **谁写谁验收**（同一 Task / 同一子会话既改 yaml 又报验收绿）  
5. 父自己跑 `run-scripts` 当正式验收（占上下文；正式验收只派 §5.3）

父发现写稿子改了 **>1** 个 `cases/*.yaml` → **判违规**，按条重派。

### 2.1 角色（三角色）

| 角色 | 做 | 不做 |
|------|----|------|
| **父 agent** | `--write` 刷 queue；派写稿 / 派验收 / 记红回炉；批量挂 catalog；进度一行 | **不写** cases；**不跑**正式验收机跑；不吞缺口 |
| **写稿子 agent** | 实勘；写/改唯一 `cases/【CASE_ID】.yaml`；必要时改 index.all / coverage **该行**；可选 `--only` **自检**后交卷 | 不验收定案；不改其他 case；不改 catalog；不续条 |
| **验收子 agent** | 只读检查双层 expect / A 零 skip / index 含 id；**串行** `--only 【CASE_ID】`；交卷 pass/fail+run 路径 | **禁止改** cases（红了只报因，由父派 §5.2 回炉）；禁止顺带验下一条 |

**隔离**：验收 Task 的 `【CASE_ID】` 必须对应**已交卷**的写稿；派验收时注明写稿 Task/会话 id（若有），且验收必须是**新开**子 agent。

### 2.2 并发

- 写稿并发 **≤4**（不同 CASE_ID）；**同功能目录写手 ≤1**。  
- **验收并发 = 1**（全局串行一个 `run-scripts`，避免抢浏览器/端口/runs）。  
- 流水线建议：写稿可并行；每条写稿一交卷，父就把该条排进验收串行队列（不必等 4 条写齐）。  
- 提示词 §5.2 / §5.3 **自包含**；禁止「详见父对话」。

---

## 3. 标准流水线（每个有缺口的入口）

```text
① 父：--write 刷新 queue（REWORK∪GAP）
② 若 env-gate 过期/缺失 → 派 §5.1 闸门（每入口最多一次）
③ 父：按 queue 每行派 §5.2 写稿 Task（≤4 并发；同目录写手 ≤1）
④ 写稿子：写本条；可选 --only 自检；交卷停（自检绿 ≠ 验收绿）
⑤ 父：写稿一交卷 → 立刻派 §5.3 独立验收 Task（验收串行，同时只 1 个）
⑥ 验收子：只读检查 + --only；交卷 pass/fail；**不改 yaml**
⑦ 父：pass → 记完成；fail → 派 §5.2 回炉（新写稿 Task）→ 再 §5.3
⑧ 父：批量挂 catalog（若需）；阶段性 --write；收口见 §6
```

### 3.1 脚本 id 分配

1. 已有 `cases/P0-xx.yaml` 且 `func_id` 对上 → **不改 id**。
2. 新增：在本功能已用 id 后续号（`P0-` / `P1-` 前缀跟用例优先级列习惯，**前缀≠优先级真源**；优先级以用例册为准，见 `_script.md` 编号母表闸门）。
3. 金样 `gold:` 列表：**默认保持不动**；新脚本进 `all:` 与 B 档。仅当金样缺条/坏条时父单独开「金样回炉」小单。

### 3.2 环境闸门（写结果态前）

沿用 method-patch §3。`overall=fail` 时：只写配置/空态/门控；结果态进 B + `allow_skip` + ticket，或 coverage 标「本轮不自动化」。**禁止**为凑条数写假绿结果态。

### 3.3 skip 配额（入口级）

- A/`gold`：**零** `allow_skip`。
- 全量：`allow_skip` 条数 / 本入口脚本总数 **≤ 25%**，且每条有 `ticket`。
- 超阈：砍脚本改「不自动化」登记，或修环境后再写——禁止裸 skip 堆高覆盖率。

---

## 4. 缺口 + 健康扫描（可重复）

```bash
# 在 gkx-orchestration 根（推荐：一次刷三份）
python3 agent-delivery/qa/as-built/tools/gap-func-vs-scripts.py --system KJZTFWXT --write
# → script-backfill-gap-KJZTFWXT.md
# → script-backfill-health-KJZTFWXT.md
# → script-backfill-queue-KJZTFWXT.md   ← 父派单只认这份

# 只要缺口、不跑健康：
python3 agent-delivery/qa/as-built/tools/gap-func-vs-scripts.py --system KJZTFWXT --write --no-health

# 只跑健康：
python3 agent-delivery/qa/as-built/tools/health-cases.py --system KJZTFWXT --write
```

### 4.0 gap 规则

- 按内置 FUNC 册↔脚本目录映射对齐。
- FUNC 行 = 主表首列 `ZNFWJQ-…-FUNC-`。
- 已覆盖判定：`cases/*.yaml` 的 `func_id` 命中。
- **盲区**：文件已在且 `func_id` 对上，但 YAML 半截 / 无 expect / index 漂移 → gap=0，须靠 health。

### 4.1 续跑 / 中断恢复（health）

任务中断后再开对话：**不要**只信旧 gap 条数。必须 `--write` 刷新 queue。

| health reason（摘要） | 含义 | 处置 |
|----------------------|------|------|
| `TOO_SHORT` / `NO_ID` / `NO_FUNC_ID` / `NO_EXPECT` / `EXPECT_EMPTY` / `EMPTY_ASSERT` | 半成品或空 expect | REWORK · §5.2 |
| `EXPECT_NO_NOTE` / `EXPECT_NOTE_NO_ASSERT` | expect 块缺双层键（兼容 0 缩进 `- note:`） | REWORK · 补 note/assert |
| `TRUNCATED_EOF` / `ODD_QUOTE_LAST_LINE` | 写入中断截断 | REWORK |
| `INDEX_ALL_MISSING_FILE` / `INDEX_GOLD_MISSING_FILE` | index 有、磁盘无 | 补文件或改 index |
| `DISK_NOT_IN_INDEX_ALL` | 磁盘有、index.all 无 | 写入 all: 或删文件 |
| `A_SKIP` | A 档 allow_skip | 去 skip 或移出 gold |
| `WIP_MARK` | 顶层 WIP/incomplete | 完成或删标记 |

> 存量 **裸字符串 expect**（仅 `- "…"`）不进 REWORK（白名单）；改动该文件时须顺手转双层（见 `_script.md`）。

**父派单顺序**：queue 表 `REWORK` → `GAP`；完成一批再 `--write`。

**每次开波 / 中断续跑 / 收口必须重跑**；勿死记「153」「72」——以最新 queue 为准。

---

## 5. 子任务提示词模板

### 5.1 模块闸门（每入口最多一次）

```text
【身份】qa-agent。父波：脚本补齐（见 script-backfill-playbook.md）。仅模块闸门。
工作根：/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
【任务】entry=【ENTRY】 目录=agent-delivery/qa/as-built/scripts/KJZTFWXT/【DIR】/
路由：【PATH】
1) 无头 survey-page.mjs（及必要二次探针）→ fixtures/scout/
2) 写/更新 env-gate.json（overall + gates + tickets）
3) 交卷：overall、tickets、结果态是否可写；停止
禁止：改 cases、改 catalog、有头浏览器、全量跑批、git
```

### 5.2 单用例写稿（强制单条 · 非验收）

父填充时：`【CASE_ID】` / `【FUNC_ID】` 各只出现**一个**具体值。本 Task **不是验收**。

```text
【身份】qa-agent 写稿。父波：脚本补齐 · 严格一用例一脚本（本 Task 只写下面这一条，不验收定案）。
工作根：/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
必读：qa/as-built/prompts/_script.md · schema.md · method-patch（双档/expect 双层/cases-v1）
【本 Task 唯一对象】CASE_ID=【CASE_ID】  FUNC_ID=【FUNC_ID】  kind=【GAP|REWORK】
【范围】只允许改：
  - agent-delivery/qa/as-built/scripts/KJZTFWXT/【DIR】/cases/【CASE_ID】.yaml
  - 同目录 index.yaml 仅把【CASE_ID】写入 all:（默认不动 gold:）
  - coverage.md 仅【CASE_ID】那一行；fixtures 仅本条需要时
【蓝本】用例册【CASE_MD】中【FUNC_ID】那一行
【闸门】fixtures/scout/env-gate.json overall=【OVERALL】
【做法】
1) 读预期列 → expect 双层（note+assert）
2) 无头实勘；locator 以实勘为准
3) （可选自检）node …/run-scripts.mjs …/【DIR】 --only 【CASE_ID】——自检结果只写入交卷说明，**不算正式验收**
4) 交卷：改动路径、自检 verdict（若有）、偏差级 D1–D4；**立即停止**
硬禁止：改其他 case；自称「验收通过」；读 queue 续条；catalog；有头浏览器；全量跑批；业务仓。
```

### 5.3 独立验收（强制单条 · 禁止改稿）

父在**写稿已交卷**后派发；必须**新开**子 agent；同时全局只跑 1 个验收 Task。

```text
【身份】qa-agent 验收（独立会话）。父波：脚本补齐 · 本 Task 只验收下面这一条，禁止改 yaml。
工作根：/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
【本 Task 唯一对象】CASE_ID=【CASE_ID】  FUNC_ID=【FUNC_ID】  DIR=【DIR】
写稿交卷摘要：【WRITER_NOTE】（路径/自检结果；勿信任为终态）
【只读检查】
1) cases/【CASE_ID】.yaml：expect 双层 note+assert；无截断；A/gold 零 allow_skip
2) index.yaml 的 all:（及若在 gold:）含【CASE_ID】；coverage 有该行
【机跑】（本 Task 唯一允许的写盘 = runs/ 下本次 run）
  node agent-delivery/qa/as-built/tools/run-scripts.mjs agent-delivery/qa/as-built/scripts/KJZTFWXT/【DIR】 --only 【CASE_ID】
【交卷】
- pass：verdict=pass；run 目录；检查清单勾选
- fail：verdict=fail；红因（C1–C6 / 脚本问题）；**不要改 cases**——停，等父派 §5.2 回炉
硬禁止：修改任何 cases/*.yaml / index / coverage；验收第二条；有头浏览器；全量跑批；业务仓。
```

---

## 6. 收口 DoD

重写波以编排表为准：

- [ ] `script-rewrite-ledger-KJZTFWXT.csv` 中无 `pending` / `running` / `fail`
- [ ] 每条 `pass` 的 `run_dir` 非空；`blocked` 有一行原因
- [ ] 抽查：`cases/FUNC-xxxxx.yaml` 的 `func_id` 等于表里的用例号
- [ ] 某入口全部 pass 之后，再把该目录 `index.all` 收成这些 `FUNC-xxxxx`（此时再删或移走旧 `P0`/`P1` 文件）。收口前不要改 `index.all`，避免全量跑混进旧脚本

上一波补齐 DoD（queue / 独立验收子）不用于本波。

---

## 7. 以后有了新用例怎么续

1. 用例册按 `_case.md` 增行并取号。  
2. `python3 …/gap-func-vs-scripts.py --system KJZTFWXT --write`。  
3. 按 **queue** 表派单（不是只看 gap）。  
4. **不要**新开编排文档；复制 §0 Kickoff 即可。

跨系统：先有 catalog live + FUNC 册 + 脚本根目录映射（工具内或 `--map`）；环境 URL 以该系统 as-built README 为准。

---

## 8. 文件索引

| 文件 | 职责 |
|------|------|
| **本手册** | 补齐编排、父/子、Kickoff、续跑、DoD |
| `prompts/_script.md` | 单条脚本写法 |
| `retro/20261014-batch32-method-patch.md` | 双档、skip、闸门、探针 |
| `tools/gap-func-vs-scripts.py` | 缺口机检；`--write` 附带 health + queue |
| `tools/health-cases.py` | 半成品 / index 漂移健康扫描 |
| `script-backfill-queue-{系统}.md` | **派单主表**（REWORK∪GAP） |
| `script-backfill-gap-{系统}.md` | 缺口快照 |
| `script-backfill-health-{系统}.md` | 健康扫描明细 |
| `catalog/{系统}.yaml` | 入口台账（仅父改挂载） |

---

## 9. 当前波提示（KJZTFWXT）

- 现行用例主表约 1579 行。编排表与之对齐，状态全是 `pending` 表示还没写新脚本。
- 旧 `cases/P0-*.yaml` 留在目录里，重写波不读、不改、不回炉。
- 中断后续跑：打开 `script-rewrite-ledger-KJZTFWXT.csv`。`running` 且没有 `result.yaml` 的改回 `pending`；已有 verdict 的按 verdict 补记。再按文首 Kickoff 派。不要在子 agent 提示词里写 `no ledger`。
- 环境只认 `https://edu.itic-sci.com/tts/svcz/`（路径前缀 /tts/svcz/；内网 `10.50.69.111:30892`、`10.50.69.111:30888`、`111.198.38.90:50892` 不作现行基址）。
