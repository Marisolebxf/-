# As-built 脚本补齐编排手册（FUNC ↔ scripts 1:1）

> **定位**：B 线第 2 步「用例已齐、脚本缺口」时的**三角色编排真源**（父只编排；写稿子 ≠ 验收子；禁止谁写谁验）。  
> **不替代**：单条写法仍读 [`prompts/_script.md`](prompts/_script.md)；双档/闸门/探针仍读 [`retro/20261014-batch32-method-patch.md`](retro/20261014-batch32-method-patch.md) + [`schema.md`](schema.md)。  
> **适用**：专题 `KJZTFWXT` 当前波（补齐相对 774 的缺口）；以后用例册增删后**同一流程**再跑 gap 工具即可续派。展示/算法库环境锁定后可复用本手册（改系统码与 catalog）。

---

## 0. 新对话 Kickoff（整段复制到父 agent）

```text
【身份】qa-agent 父控（只编排与记账；不写 cases、不跑验收机跑，省上下文）。
【工作根】/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
【必读（按序）】
1) agent-delivery/qa/as-built/script-backfill-playbook.md（全文 · 尤其 §2 三角色 + §5.2/§5.3）
2) agent-delivery/qa/as-built/prompts/_script.md
3) agent-delivery/qa/as-built/retro/20261014-batch32-method-patch.md
4) agent-delivery/qa/as-built/schema.md
【目标】FUNC 册 ↔ as-built 脚本 1:1（缺补齐 + 半成品回炉）；以扫描工具最新输出为准。
【第一步 · 必跑】
  python3 agent-delivery/qa/as-built/tools/gap-func-vs-scripts.py --system KJZTFWXT --write
  读 script-backfill-queue-KJZTFWXT.md（派单主表）及 health/gap 附件。
【三角色】
- 写稿子 agent（§5.2）：一次 1 条；可自跑 --only 作交卷前自检，**自检 verdict 不算验收**。
- 验收子 agent（§5.3）：**独立新会话**；与写稿者不得为同一 Task；一次 1 条；串行（同时只 1 个验收在飞）。
- 父：派写 → 收写稿交卷 → 另派验收 → 收验收交卷；红则派 §5.2 回炉（换写手或同模板重开均可，仍禁止写手自验）。
【续跑铁律】有文件 ≠ 完成；queue 刷新后再派；REWORK 优先于 GAP。
【粒度】写/验收各 1 Task=1 CASE_ID；禁止整入口大包；闸门例外见 §5.1。
【并发】写稿 ≤4（同目录写手 ≤1）；**验收串行 =1**。
【强度】ponytail full。【禁止】父写 cases / 父跑 run-scripts 验收；有头浏览器；子改 catalog；全量刷分；git push（除非人类要求）。
【进度】每批写+验后 --write；收口 §6。
开干：queue 前 ≤4 行派写稿 Task；每条写稿交卷后立刻派独立验收 Task（验收队列串行，不要等写满 4 条再验）。
```

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

## 2. 角色、粒度与并发

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

入口级：

- [ ] queue 该入口无待办；本波每条均有**独立验收子** pass（非写稿自检）
- [ ] `gap=0` 或豁免+ticket；`health` 该入口 0
- [ ] `index.all` ↔ disk 一致；B skip≤25%+ticket；A 零 skip
- [ ] catalog 已挂（父）；用例册自动化列已回填

系统级：

- [ ] queue 长度 0（或仅豁免说明）
- [ ] handoff：FUNC/脚本总数、独立验收 pass 数、豁免条数；注明「验收均独立子 agent、写手未自验定案」

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

- 金样铺开已收口（BATCH32 R3）。补齐波以 **`--write` 刷新后的 queue** 为准。  
- 中断续跑：先 `--write`，先清 `REWORK`，再补 `GAP`。  
- 顺手：catalog 未挂的入口由父批量挂；薄包补 `coverage.md` / `testdata.yaml`。
