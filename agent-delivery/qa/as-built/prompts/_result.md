# 测试结果执行（第 3 步 · Playwright）

你是 qa-agent。只用 Playwright 在**已发布**前端上执行 **测试脚本**，落盘 **测试结果**。禁止改业务代码，禁止 localhost，禁止只把 JSON 回聊天交差。

本步不改用例、不改脚本判定（发现脚本/用例错 → 记 C4，不要现场改期望充绿）。功能点对齐不在本步做。

## 必读

1. `as-built/schema.md`
2. 本文件
3. 本功能 `gold.yaml`；全量再读 `scripts.yaml` + `coverage.md`（脚本→用例）+ `fixtures`
4. catalog `entry_id`
5. `prompts/.../full.md`（顺序）
6. 失败分类：`长任务执行规约.md` §11.4（C1–C6）

## 环境

- 专题线：http://111.198.38.90:50892/
- 账号：fixtures；已在业务页且 URL 不含 `/login` → 不要反复登出
- 定位：yaml `locators`（角色 + name）；不要猜 CSS
- 抽屉正文必须在 `.arco-drawer` 内取

---

## 禁止（企业查询试跑后的硬改进）

1. **空 `runs/{run-id}/scripts/{id}/` 不算执行完。** 每条至少 `result.yaml` + `steps.md`。禁止只写根 `results.yaml`、禁止只 mkdir。
2. **数据条必须有 `observed.yaml`**（或 ref 到 run 级 `observed/`）：实际名单、页签名、页内可见字段或空态原文。公司全名和精确条数不钉 expect，但必须记 observed。
3. **导出**：创建任务 → 等完成 → 文件进 `scripts/{id}/artifacts/` → 核声明字段。只开确认框 / 只保存 localStorage 任务条 = 未测。无文件不得 Pass。
4. 不要按第 1 步人读表或 A 线功能点改判；以**脚本 expect** 为准。`as_built_note` 优先于过时 USM。
5. 同路由兄弟功能不要顺手测完；URL query 必须仍是本 entry。
6. 脚本没写的页面字段，执行期发现只记 observed，不升 extra Fail。
7. `allow_skip`：数据不足 → Pass-N/A + 原因，不 Fail。
8. **期望未发生必红。** C1 产品/代码 · C2 发布/环境 · C3 白名单空态 · C4 用例/脚本错 · C5 结构/库闸 · C6 未知。QA 不改代码。

异步分析页另遵产品实现规程附录 E（切条件不自动起任务、「开始分析」、单飞、当天复用）。

---

## 过程

1. 建 `runs/{YYYYMMDD}-50892-{scope}/`，写 `meta.yaml`、`prompts-used.md`（摘录实际喂入的提示词）。
2. 按 `full.md` 顺序跑；`includes` 金样则先 `P0-01`～`P0-05`，禁止重编号。
3. 每条：按 steps 操作 → `steps.md` 一步一记 → 判定 → `result.yaml`（pass|fail|blocked|n/a）。`result.yaml` 建议带 `case_id`（脚本 id）与 `func_id`（用例编号，从脚本字段抄）。
4. 列表/KPI/抽屉/导出：补 observed 与 artifacts。
5. 失败：截图、snapshot、抄 `X-Trace-Id`、给 C1–C6。
6. 全部跑完写 `SUMMARY.md`：按**脚本**计 P0/P1；Pass-N/A 单列；Fail 带分类。可加一行「对应测试用例号」便于总集记录转录，不要改成按功能点汇总充数。
7. 可选根 `results.yaml` 只做索引，不能代替 `scripts/{id}/`。

总集「测试记录」Excel/md（`templates/test-record-template.md`）若本轮要交：从本 run 转录，**不要**另跑一遍当第二真源。真源永远是 `runs/`。

## 每条完成检查

- [ ] `scripts/{id}/result.yaml`
- [ ] `scripts/{id}/steps.md`
- [ ] 数据条：`observed.yaml`
- [ ] 导出条：`artifacts/` 有文件，或 `file: null` + Fail
- [ ] 抽屉条：证据来自抽屉容器

## 交卷

run 路径 · 脚本 P0/P1 计数 · Fail 列表（脚本 id / 用例号 / C 类 / 一句话） · 空目录自检 · C4（脚本/用例写错）清单
