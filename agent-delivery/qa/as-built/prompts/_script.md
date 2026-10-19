# 测试脚本编写（第 2 步 · Playwright 可读）

你是 qa-agent。本文件把 **已评审的测试用例** 译成 as-built **测试脚本**（yaml 过程 + locators + fixtures）。禁止改业务仓代码。禁止另起一套与用例冲突的判定。禁止按 A 线功能点或总集 FUNC 表一对一新编脚本。

专题重写波（2026-10-19）：脚本文件名和 `id` 用用例号 `FUNC-xxxxx`，`func_id` 用完整用例号。不要改旧的 `P0`/`P1` 文件，也不要抄它们的断言。环境 `http://10.50.69.111:30888/`。编排见 `script-backfill-playbook.md` 文首，一条用例一个子 agent。

本步覆盖矩阵的方向是 **脚本 → 用例**（不是脚本 → 功能点）。功能点覆盖已在第 1 步做完。

## 必读

1. 第 1 步产物：`qa/test-cases/.../FUNC-*-用例.md` + 用例对功能点矩阵
2. `as-built/schema.md`、`as-built/README.md`
3. 本文件；功能专属 `full.md` 只补充执行顺序
4. catalog 目标 `entry_id`
5. 指标 ⓘ 仍走 metric-registry MCP

未完成第 1 步（没有人读用例文件）时：**停**。不要倒退成「直接写 yaml 再回头补用例」。企业查询就是这样漏的。

## 禁止

1. 不把 `P0-xx` 写成用例编号；脚本 id 只存在于 as-built yaml。
2. 不把 `func_id` 填成 v8 功能点行。`func_id` = 第 1 步的 **用例编号**（`ZNFWJQ-KJZTFWXT-v1.0-FUNC-xxxxx`）。
3. 看不见的字段不当 expect（与用例预期一致；用例没写的页面字段不要在脚本里加严）。
4. 同一工具条多种结果态：用例有几条，脚本就要覆盖几条，禁止只译其中一条。
5. 导出步骤必须含创建任务 + 等待文件；禁止译成「开确认框取消」。
6. 抽屉断言限定 `.arco-drawer`。
7. 同路由兄弟功能不写进本套脚本。
8. 不要为未覆盖的 A 线功能点「发明」脚本。
9. **收到含编号母表的任务书，禁止直接照抄落笔**（见「编号母表闸门」）。
10. **登录并关闭内部评审模式是 runner 的会话前置**（`ensureBusinessSession`）：每条脚本的步骤开始前执行一次，每次 `goto` 后再执行一次，本条结束后再确认一次。整段测试过程保持关闭，不是写在某条 `assert` 里的检查。单条 `cases/*.yaml` **不要**再写登录或开关步骤。禁止出现「开启内部评审」。评审专有控件不写 `assert`。
11. **禁止空断言当通过。** `assert` 里出现空分支（例如任务变多也什么都不验）= 脚本不合格。`allow_skip` 不能代替用例要的那一个终态；金样（A 档）禁止 `allow_skip`。

---

## 编号母表闸门（D1/D2，试点 R11+R12 教训）

任务书附带编号母表时，**母表只锁金样 id（P0-01~05）；其余行一律以用例册「自动化用例ID」回填列为唯一基准**：

1. `cases/*.yaml`（或存量 `scripts.yaml`）落笔前，先逐行比对任务书母表 ↔ 用例册回填列；不一致以用例册为准，并在 coverage.md 备注差异、回告派单方。
2. 脚本侧唯一基准 = 用例册回填列 + 各条脚本的 `func_id`；母表与其冲突时母表让位。
3. 落盘后执行四方一致性机检（`tools/check-run-consistency.py`）：目录名 = result.yaml `case_id` = `func_id` 尾号 = steps.md 标题。
4. **脚本 id 的 P0/P1 前缀 ≠ 用例册优先级列**：母表顺延可把用例优先级 P2 的条挂到脚本 `P0-13`；coverage 主表「P」列写用例优先级，勿与脚本 id 混读。

## 编写条款（P1~P9，试点 SEARCH/KEYENT + runner 校准教训；P3/P9 于 2026-10-17 收紧）

| # | 条款 |
|---|------|
| P1 | 步骤文案与现场 locator 不一致时**以关评审后的复勘为准**（过程 §0）；steps.md 与 `as_built_note` 标注差异（如 hero 搜索栏「搜索」vs 文案「查企业」） |
| P2 | **click 后断言必须跨 tick**（分步求值或显式 wait）——React 受控组件 setState 异步，同一次求值内 click+读态会读到旧值假红 |
| P3 | **关评审是会话前置，不是断言。** `run-scripts.mjs` 在每条脚本开始、每次 `goto` 之后、本条结束时调用 `ensureBusinessSession`：已登录，且 `aria-label="内部评审模式"` 的 switch 为 `aria-checked="false"`（菜单内有多个 switch，禁止 `first()`）。人设菜单随即关掉，避免挡住主区。yaml 不重复这段操作；若步骤把开关打开，下一次前置会再关掉 |
| P4 | 弹层无 Esc / body-click 关闭路径（如 Arco TriggerPopup 常驻）时，以 DOM `display:none` 收场并在 steps.md 标注——**不判 Fail**，关闭缺失归缺陷单 |
| P5 | 级联分组标题节点 `pointer-events:none` 点击穿透时，**回退父级分组容器点击**；fixtures 记录容器 selector 口径 |
| P6 | **默认按原生 Playwright runner（`tools/run-scripts.mjs`）编写**：机检判定写在 `expect[].assert`（page/expect 上下文）。仅 MCP/CDP 过渡调试时：CDP 求值一律**同步单目的**（`Runtime.evaluate + awaitPromise` 对 async IIFE 常返回空对象；async 拆多次同步求值） |
| P7 | **Arco Select / Cascader 点击目标**：点可见触发器容器（如 `.arco-select-view`、`span.sci-arco-cascader`），**禁止**点宽度为 0 的隐藏 `.arco-select-view-input` / 仅靠 `getByPlaceholder` 点到的隐藏 input（必超时）。下拉选项挂在 `.arco-trigger-popup:visible` |
| P8 | **跨脚本状态隔离**：单 page 顺序跑时，上一条遗留（抽屉开 / 菜单开 / tag 残留）会污染下一条。评审开关由会话前置收回，不必在用例步骤里再关。承接型脚本在 steps 或 assert 自含 `goto` 页面重置，或真实关闭抽屉（`.arco-drawer-close-btn`）；禁止假设「上一条已还原」 |
| P9 | **断言必须落到用例的那一问。** 用例预期是「进入结果且不新增任务」，脚本就不能只判断任务条数变化后留空。写不出稳定 `assert` 时标 `manual: true` 待人工，不得写成空语句或 `allow_skip` 后仍报通过。B 档 `allow_skip` 仅用于数据或环境闸门（须有 `ticket`），跳过的脚本不能计入该用例已验收 |

**steps / locators / assert 分工（runner）**：`tools/run-scripts.mjs` 机跑以 `expect[].assert` 为判定真源；`steps[]` / `locators` 供人读与 MCP 勘察。关键交互（下拉点选、开关、关抽屉）须在 `assert` 内自含可点 selector，或保证 `steps` 的 action 已被 runner 完整实现且与 assert 不打架。优先把操作留在 `steps`、assert 只做判定；避免把整段 try/catch 操作堆进超长 assert（维护成本高）。

---

## 过程

### 0. 复勘（写 locator 之前）

对照用例核对文案和 selector 时，与第 1 步勘察相同：**先关闭内部评审模式，再看页面**。用手开的浏览器时先关，复勘过程中不要打开。用 `tools/survey-page.mjs` 时，探针在抽控件和截图之前关闭。关着看不见的评审挂件（指标说明、Q0xx 角标、需求追溯、评审态模拟下拉）不进 `locators`，也不进 `assert`。

### 1. 从用例翻译（默认 1:1）

每条人读用例 → 通常 **1** 条脚本。允许 1 用例 N 脚本，仅当：步骤明显互斥（必须 reload）、或金样冒烟需要从全量里抽出子集（金样仍指向同一批用例号）。禁止 1 脚本吞 2 条用例的判定（矩阵会假绿）。

脚本字段见 `schema.md`。`id` 用功能内 `P0-01`…；本功能金样锁定 `P0-01`～`P0-05`（语义跟本页走，不是企业查询那五条）。`entry_id`、`locators`、`steps[].action` 用 schema 枚举。`as_built_note`：现场与用例/USM 不一致时必写。

落盘（**新规 cases-v1 · 一用例一文件**）：

```text
as-built/scripts/{系统}/{模块}/{功能}/
  index.yaml             # gold: [P0-01, …]；all: […]（可选）
  cases/P0-01.yaml       # 单文件 = 一条完整脚本对象
  cases/P0-02.yaml
  coverage.md            # 【主表】脚本 → 用例（含档 A/B、skip ticket）
  fixtures/testdata.yaml
  fixtures/scout/env-gate.json
```

禁止再写大包 `scripts.yaml` / `gold.yaml`（存量已拆；漏网可用 `tools/split-scripts-to-cases.py`）。

`coverage.md` 主表列：**脚本 id → 用例编号 → 页面区块/状态 → P → 档(A/B) → 可见动作 / skip ticket**。不要再把 FUNC-000xx 当功能点列主表（可加备注列「第 1 步已覆盖的功能点键」作只读互指）。

**expect 双层格式（X9，用户拍板 2026-10-14）**——每条 expect 用对象而非裸字符串：

```yaml
expect:
  - note: 结果标题出现「智能搜索结果 · 命中 N 家企业」                 # 必填：人话，译自用例预期列
    assert: "await expect(page.getByText('智能搜索结果')).toBeVisible()"  # 尽填：Playwright 原生断言表达式
    manual: true                                                        # 仅写不出机检断言时出现（主观/视觉类）
```

规则：`note` 必填且与用例册预期列对齐（MCP 人工执行照 note 判定，assert 作操作提示）；`assert` 用 Playwright 原生表达式字符串（不发明 DSL），在 runner 的 page/expect 上下文求值；`manual: true` 条目 runner 跳过并标待人工。

**裸字符串存量**：`expect` 禁止新写裸字符串。KEYENT（24）已双层；SEARCH 等若仍有裸串，属存量白名单——改动该功能脚本时须顺手转双层，转完即移出白名单。runner 遇裸串按 note 处理并告警，不得当作新脚本合格标准。

文末暂缓：只放第 1 步已标未覆盖/P2/跨模块的项。看得见却没脚本 = 本步没做完。

### 2. fixtures 与执行顺序提示词

`fixtures/testdata.yaml`：base_url、账号、页面上能点到的默认文案。不要把执行期才出现的公司名单当硬期望。

写 `prompts/{系统}/{模块}/{功能}/full.md`（可选 `gold.md`）：只写推荐执行顺序与易错点。铁律引用 `_result.md`，不要复制相反口径。

catalog 该 entry 补 `scripts` / `gold` / `full_scripts`。禁止改 `id`。

第 1 步用例表的「自动化用例ID」列回填脚本 id（如 `P0-03`）。

### 3. 脚本对用例覆盖矩阵（本步 DoD）

| 用例编号 | 脚本 id | 关系 | 状态 |
|----------|---------|------|------|
| FUNC-00046 | P0-02 | 1:1 | 已脚本化 |
| FUNC-00047 | P0-03, P0-04 | 1:N（reload） | 已脚本化 |
| FUNC-00099 | — | — | **未脚本化**（须补或声明本轮不自动化） |

目标：第 1 步里本轮要自动化的用例，脚本覆盖 **N >= 1**。未脚本化必须写原因（P2 / 无稳定 locator / 依赖人工文件审批）。

本步**不要**建空的 `runs/.../scripts/P0-xx/` 执行目录。BATCH32 铺开叫停后：**金样须可被** `tools/run-scripts.mjs --only …` **机跑**（由父 agent 验收时创建 run；子 agent 仍禁止自己全量跑批刷分）。

### 4. 双档 + 环境闸门 + 一文件一用例（BATCH32 方法论补丁，2026-10-14）

真源：`as-built/retro/20261014-batch32-method-patch.md`。摘要：

- **布局 cases-v1**：`index.yaml` + `cases/{id}.yaml`；新写 / 回炉强制（存量已全量拆）。
- **A 档 smokeable（`index.gold`）**：仅当前环境可绿路径；对应 case **禁止** `allow_skip`。
- **B 档 coverage（其余 cases）**：skip ≤25% 且每条有 `ticket`；超阈砍脚本改「不自动化」。
- 写结果态前必须过环境闸门，证据落 `fixtures/scout/env-gate.json`。
- 子 agent **不改 catalog**；无头探针公约见补丁 §4。

## 交卷

1. `index.yaml` + `cases/*.yaml` / fixtures（含 `scout/env-gate.json`）/ full.md；catalog 路径交给父 agent 挂
2. 脚本条数（金样 A + 其余 B）与 **skip 占比**
3. **脚本 → 用例**矩阵（未脚本化清单 + skip ticket）
4. 与用例预期的偏差（as_built_note，按 D1～D4 分级）

---

## 用例已齐、脚本有缺口时

单条写法仍用本文。**父/子编排、缺口盘点、Kickoff、收口 DoD** 见 [`../script-backfill-playbook.md`](../script-backfill-playbook.md)（勿把编排流程写进本文件）。机检：`../tools/gap-func-vs-scripts.py`。
