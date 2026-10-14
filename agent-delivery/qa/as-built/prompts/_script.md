# 测试脚本编写（第 2 步 · Playwright 可读）

你是 qa-agent。本文件把 **已评审的测试用例** 译成 as-built **测试脚本**（yaml 过程 + locators + fixtures）。禁止改业务仓代码。禁止另起一套与用例冲突的判定。禁止按 A 线功能点或总集 FUNC 表一对一新编脚本。

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

---

## 编号母表闸门（D1/D2，试点 R11+R12 教训）

任务书附带编号母表时，**母表只锁金样 id（P0-01~05）；其余行一律以用例册「自动化用例ID」回填列为唯一基准**：

1. `scripts.yaml` 落笔前，先逐行比对任务书母表 ↔ 用例册回填列；不一致以用例册为准，并在 coverage.md 备注差异、回告派单方。
2. 脚本侧唯一基准 = 用例册回填列 + `scripts.yaml` 的 `func_id`；母表与其冲突时母表让位。
3. 落盘后执行四方一致性机检（`tools/check-run-consistency.py`）：目录名 = result.yaml `case_id` = `func_id` 尾号 = steps.md 标题。

## 编写条款（P1~P6，试点 SEARCH/KEYENT 实勘教训）

| # | 条款 |
|---|------|
| P1 | 步骤文案与现场 locator 不一致时**以实勘为准**；steps.md 与 `as_built_note` 标注差异（如 hero 搜索栏「搜索」vs 文案「查企业」） |
| P2 | **click 后断言必须跨 tick**（分步求值或显式 wait）——React 受控组件 setState 异步，同一次求值内 click+读态会读到旧值假红 |
| P3 | 业务态断言脚本**前置关闭内部评审模式**：右上 persona-menu →「内部评审模式」switch `aria-checked` 置 false（标准前置步骤；开关路径记入 fixtures） |
| P4 | 弹层无 Esc / body-click 关闭路径（如 Arco TriggerPopup 常驻）时，以 DOM `display:none` 收场并在 steps.md 标注——**不判 Fail**，关闭缺失归缺陷单 |
| P5 | 级联分组标题节点 `pointer-events:none` 点击穿透时，**回退父级分组容器点击**；fixtures 记录容器 selector 口径 |
| P6 | （MCP 过渡期）CDP 求值一律**同步单目的**——`Runtime.evaluate + awaitPromise` 对 async IIFE 常返回空对象；async 需求拆多次同步求值。Playwright 正式化后本条自然消除 |

---

## 过程

### 1. 从用例翻译（默认 1:1）

每条人读用例 → 通常 **1** 条脚本。允许 1 用例 N 脚本，仅当：步骤明显互斥（必须 reload）、或金样冒烟需要从全量里抽出子集（金样仍指向同一批用例号）。禁止 1 脚本吞 2 条用例的判定（矩阵会假绿）。

脚本字段见 `schema.md`。`id` 用功能内 `P0-01`…；本功能金样锁定 `P0-01`～`P0-05`（语义跟本页走，不是企业查询那五条）。`entry_id`、`locators`、`steps[].action` 用 schema 枚举。`as_built_note`：现场与用例/USM 不一致时必写。

落盘：

```text
as-built/scripts/{系统}/{模块}/{功能}/
  gold.yaml            # 冒烟 5 条脚本
  scripts.yaml         # includes 金样 + 其余；顶层键 scripts:
  coverage.md          # 【主表】脚本 → 用例
  fixtures/testdata.yaml
```

`coverage.md` 主表列：**脚本 id → 用例编号 → 页面区块/状态 → P → 可见动作**。不要再把 FUNC-000xx 当功能点列主表（可加备注列「第 1 步已覆盖的功能点键」作只读互指）。

**expect 双层格式（X9，用户拍板 2026-10-14）**——每条 expect 用对象而非裸字符串：

```yaml
expect:
  - note: 结果标题出现「智能搜索结果 · 命中 N 家企业」                 # 必填：人话，译自用例预期列
    assert: "await expect(page.getByText('智能搜索结果')).toBeVisible()"  # 尽填：Playwright 原生断言表达式
    manual: true                                                        # 仅写不出机检断言时出现（主观/视觉类）
```

规则：`note` 必填且与用例册预期列对齐（MCP 人工执行照 note 判定，assert 作操作提示）；`assert` 用 Playwright 原生表达式字符串（不发明 DSL），在 runner 的 page/expect 上下文求值；`manual: true` 条目 runner 跳过并标待人工。存量 65 条转换完成前允许裸字符串（runner 按 note 处理并告警），**转换完成后新脚本禁止裸字符串**。

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

本步**不要**建 `runs/`，不要 mkdir 空的 `runs/.../scripts/P0-xx/` 执行目录。

## 交卷

1. yaml / fixtures / full.md / catalog 路径
2. 脚本条数（金样 + 其余 P0/P1）
3. **脚本 → 用例**矩阵（未脚本化清单）
4. 与用例预期的偏差（as_built_note）
