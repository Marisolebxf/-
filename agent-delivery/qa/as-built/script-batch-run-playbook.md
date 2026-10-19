# As-built 用例脚本批量执行手册（S3）

> **定位**：B 线第 3 步——对已落盘脚本做**冒烟 / 全量 / 回归**机跑，并强制产出波次 Excel 清单 + 执行总结。  
> **不替代**：单条判定铁律仍读 [`prompts/_result.md`](prompts/_result.md)；落盘形状见 [`schema.md`](schema.md) §4；失败分类 C1–C6 见 `长任务执行规约.md` §11.4。  
> **总路由**：[`../func-test-playbook-index.md`](../func-test-playbook-index.md) 阶段 **S3**。  
> **与 S5 区别**：本手册 Excel = **本波执行工作清单**（便于收结果）；客户交付「测试记录」簿见 [`../record-delivery-playbook.md`](../record-delivery-playbook.md)（S5），禁止把调通垃圾当交付。

---

## 0. 开跑前须知（其它问题）

| # | 点 | 处理 |
|---|----|------|
| 1 | `as-built/runs/` **被 gitignore** | 波次结果默认只在本地；正式轮次须另拷摘要到 `test-records/{系统}/R{n}/` + 失败图 `evidence/`（见 §7）。**禁止** `--run-dir` 指向 `qa/runs/`（历史误用目录，已废弃） |
| 2 | 脚本缺口未补完 | 「全量」= **已有脚本全跑**，≠ FUNC 册 774。开跑前跑 `gap-func-vs-scripts.py`，WAVE.md 写明缺口数 |
| 3 | 多功能 `P0-01` 撞名 | 必须波次父目录 + **每功能一子目录**（`schema.md` §4.2）；禁止多功能共用一个 `--run-dir` |
| 4 | runner 串行 | 同时只跑 **1** 个 `run-scripts.mjs`（浏览器/账号互扰）；父可排队多入口，勿并行机跑 |
| 5 | `allow_skip` / `manual` | → `n/a` / `pending_manual`，**不算 Fail**；Excel「通过情况」单独取值 |
| 6 | 闸门 fail 入口 | 仍可跑；结果多为配置/空态或 n/a；总结里单列「环境债」 |
| 7 | fail_class 常为 C6 | runner 默认偏 C6；**汇总子任务**须按 `actual` 重判 C1–C6 并填严重程度（§6.2） |
| 8 | Bug 提交方式待定 | Excel「BUG编号」允许空；若本波人工取号，写 `bug-registry.yaml` 后再回填 |
| 9 | 与写脚本波混淆 | 本波**禁止**改 `cases/*.yaml` 期望充绿；脚本错 → C4，另开 S2 回炉 |

---

## 1. 新对话 Kickoff（整段复制到父 agent）

```text
【身份】qa-agent 父控。阶段 S3·脚本批量执行。
【总索引】agent-delivery/qa/func-test-playbook-index.md
【必读】agent-delivery/qa/as-built/script-batch-run-playbook.md（全文）
         → prompts/_result.md → schema.md §4.2
【工作根】/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
【系统】【SYSTEM=KJZTFWXT】 环境：http://10.50.69.111:30888/（禁止 localhost）
【模式】【smoke | full | regress】
  - smoke：每个 live 入口只跑 index.yaml 的 gold:
  - full：每个 live 入口跑 index.all（或全部 cases）
  - regress：仅跑清单【LIST_FILE 或 下方 IDS】
【波次目录】agent-delivery/qa/as-built/runs/【YYYYMMDD】-30888-【WAVE_ID】/
【第一步】mkdir 波次目录；写 WAVE.md（模式/范围/缺口快照一行）；跑 gap 工具备忘
【执行】父按入口串行调用 run-scripts.mjs，一律 --run-dir $WAVE/<功能短名>
【结束后强制两个子 Task（缺一不算收口）】
  A) 汇总 Excel：手册 §5.1 模板 → 跑 tools/aggregate-wave-results.py --wave $WAVE --write
     再人工/子任务补严重程度重判与 BUG 列
  B) 执行总结：手册 §5.2 模板 → 写出 $WAVE/EXEC-SUMMARY.md（含 bug 清单，编号可空）
【禁止】改业务仓；改脚本期望充绿；有头浏览器；并行多个 run-scripts；多功能共用 run-dir
【强度】ponytail full
开干：确认模式与 WAVE_ID 后从 catalog live 入口队列第一条开始串行机跑。
```

---

## 2. 三种执行模式

| 模式 | 人话 | 每入口选哪些脚本 | 典型用途 |
|------|------|------------------|----------|
| **smoke** | 冒烟 | 仅 `index.yaml` → `gold:`（无 gold 则跳过并记 WAVE 风险） | 发版后快速看红 |
| **full** | 系统全量 | `index.all`；若无 `all` 则该目录全部 `cases/*.yaml` | 专题整库回归 |
| **regress** | 指定回归 | 人给定：`entry_id` + `CASE_ID` 列表（文件或 Kickoff 内嵌） | 修缺陷后复测 |

### 2.1 回归清单文件格式（推荐）

路径示例：`$WAVE/regress-list.yaml`

```yaml
system: KJZTFWXT
items:
  - entry: ent-search
    dir: enterprise/search          # 相对 scripts/KJZTFWXT/
    ids: [P0-01, P0-05, P1-11]
  - entry: svc-portal
    dir: service/portal
    ids: [P0-01, P0-07]
```

### 2.2 入口队列来源

- 默认：`catalog/{系统}.yaml` 中 `status: live` 且磁盘存在 `scripts/.../index.yaml`。  
- smoke/full：按 catalog 顺序；regress：只跑清单出现的 entry。  
- 无脚本目录：记入 WAVE「未执行」表，不假装 pass。

---

## 3. 波次目录与机跑命令

```text
runs/{YYYYMMDD}-{env}-{wave-id}/
  WAVE.md                 # 模式、环境、范围、缺口、开始结束时间
  regress-list.yaml       # 仅 regress
  enterprise-search/      # 每功能一层（短名 = 路径 basename 或模块-功能）
    meta.yaml · SUMMARY.md · scripts/{CASE_ID}/result.yaml …
  service-portal/
  …
  results.xlsx            # 子任务 A 产出（或 .csv）
  EXEC-SUMMARY.md         # 子任务 B 产出
  aggregate-raw.json      # 工具中间态（可选）
```

```bash
# 在 as-built/tools 下；WAVE 换成实际波次绝对/相对路径
WAVE=../runs/20261015-50892-smoke-r1
mkdir -p "$WAVE"

# 单入口示例（smoke = 把 gold ids 填进 --only）
node run-scripts.mjs ../scripts/KJZTFWXT/enterprise/search \
  --run-dir "$WAVE/enterprise-search" \
  --only P0-01,P0-02,P0-03,P0-04,P0-05

# full：不加 --only（跑 index.all / 全部 cases）
node run-scripts.mjs ../scripts/KJZTFWXT/enterprise/search \
  --run-dir "$WAVE/enterprise-search"
```

父负责：从各入口 `index.yaml` 解析 gold/all → 拼 `--only` → **串行**执行 → 更新 WAVE.md 进度行。

---

## 4. 角色与子任务

| 角色 | 职责 |
|------|------|
| **父** | 建波次；串行机跑；维护 WAVE.md 进度；**必须**派齐 §5 两个子 Task；仲裁 C 类争议 |
| **子·机跑**（可选） | 仅当父把「单入口机跑」外包时：只跑一个 `--run-dir`，不改脚本，交 SUMMARY 路径 |
| **子·Excel（必须）** | §5.1：聚合成 `results.xlsx` |
| **子·总结（必须）** | §5.2：写 `EXEC-SUMMARY.md` |

机跑本身**不需要**大模型（纯 `run-scripts.mjs`）。父可用 LLM 编排排队；判定以 runner 的 `result.yaml` 为准。

---

## 5. 结束后强制子任务模板

### 5.1 子任务 A · 结果 Excel 清单

```text
【身份】qa-agent。S3 波次收口 · 子任务 A·Excel 汇总（必须）。
工作根：…/gkx-orchestration
【输入】波次目录【WAVE=绝对路径】
【必读】as-built/script-batch-run-playbook.md §6
【做法】
1) python3 agent-delivery/qa/as-built/tools/aggregate-wave-results.py --wave 【WAVE】 --write --casebook-scope bline-only
2) 打开生成的 results.xlsx：按 §6.2 对 Fail/Blocked 行重填「失败分类」「严重程度」；BUG编号按 §6.3（可空）
3) 交卷：results.xlsx 路径、行数、Fail 行数；停止（不要改 cases/、不要重跑浏览器）
```

**Excel 最低列（顺序固定）：**

| 列 | 说明 |
|----|------|
| 用例编号 | `func_id`（`ZNFWJQ-…-FUNC-xxxxx`） |
| 用例描述 | 脚本 `title`；缺则从用例册标题补 |
| 脚本ID | `P0-01` 等 |
| 功能入口 | catalog `entries[].title` 中文名（由 `meta.yaml` 的 `feature` 反查；无则回退 run 子目录名） |
| 通过情况 | `通过` / `不通过` / `跳过` / `阻塞` / `待人工`（§6.1 映射） |
| 失败原因 | `result.actual` 摘要；通过可空 |
| 失败分类 | `C1`–`C6` 写成 **`编号-名称`**（如 `C6-未知/待分诊`）；非失败可空 |
| 严重程度 | §6.2；非失败可空 |
| BUG编号 | 有则 `BUG-ZNFWJQ-…`；待定则空 |
| 证据路径 | 从 **`runs/`** 起：`runs/{波次名}/{功能子目录}/scripts/{脚本ID}/`（`aggregate-wave-results.py` 自动拼） |
| traceId | 若有 |

### 5.2 子任务 B · 执行总结 + Bug 清单

```text
【身份】qa-agent。S3 波次收口 · 子任务 B·执行总结（必须）。
工作根：…/gkx-orchestration
【输入】【WAVE】+ 已生成的 results.xlsx（若 A 未完成则先等 A）
【产物】【WAVE】/EXEC-SUMMARY.md，结构见手册 §6.4
【要求】
- 总览：计划/执行/通过/不通过/跳过/阻塞/待人工
- 按模块失败热点；环境债（闸门 fail、n/a 票）单独一节
- Bug 清单表：标题、关联用例编号、失败分类、严重程度、BUG编号（可空）、建议责任层
- 明确：本文件≠客户交付测试记录（S5）；runs 默认不入库
交卷后停止。
```

---

## 6. 判定与列映射

### 6.1 verdict → 通过情况

| `result.yaml` verdict | 通过情况 |
|----------------------|----------|
| `pass` | 通过 |
| `fail` | 不通过 |
| `n/a` | 跳过 |
| `blocked` | 阻塞 |
| 含 `pending_manual` 且无 fail | 待人工 |

### 6.2 严重程度（汇总时填写）

Excel **失败分类**列用 **`编号-名称`**（工具默认输出；人工重判时保持同格式）：

| 编号 | Excel 取值示例 | 严重程度 | 含义（摘要） |
|------|----------------|----------|--------------|
| C1 | `C1-产品/代码缺陷` | 高 | 产品/代码缺陷 |
| C2 | `C2-发布/环境` | 中 | 发布/环境 |
| C3 | `C3-白名单空态` | — | 白名单空态（通常不应进 Fail） |
| C4 | `C4-用例/脚本错` | 中 | 用例/脚本错 → 开 S2 回炉，不改产品充绿 |
| C5 | `C5-结构/库闸` | 阻塞 | 结构/库闸 |
| C6 | `C6-未知/待分诊` | 高 | 未知/待分诊 |

并列取更停：C5 > C6 > C4 > C2 > C1（与长任务规约一致）。

### 6.3 BUG 编号

- 提交方式**待定**：默认空。  
- 若本波要占号：先改 `qa/bug-registry.yaml` 取号，再回填 Excel + EXEC-SUMMARY。  
- 禁止臆造 BUG 号。

### 6.4 EXEC-SUMMARY.md 骨架

```markdown
# 执行总结 · {wave-id}

## 1. 范围
- 系统 / 模式 / 环境 / 波次目录
- 脚本缺口备忘（gap 工具一行）

## 2. 结果总览
| 通过情况 | 条数 |
| 通过 | |
| 不通过 | |
| 跳过 | |
| 阻塞 | |
| 待人工 | |

## 3. 不通过清单（热点）
| 用例编号 | 脚本ID | 入口 | 分类 | 严重程度 | 原因摘要 |

## 4. Bug 清单
| BUG编号 | 标题 | 用例编号 | 分类 | 严重程度 | 状态 |
（编号可空，标题必填）

## 5. 环境与债务
闸门 fail / 高 n/a 入口 …

## 6. 结论与下一步
总体：通过 / 不通过 / 有条件通过；建议 S2 回炉 / 缺陷跟进 / S5 交付…
```

---

## 7. 正式轮次（可选升级）

调通/日常 smoke：只保留 WAVE 本地即可。

**正式 R{n} 轮次**额外：

1. 将 `EXEC-SUMMARY.md` + `results.xlsx` 拷到 `test-records/{系统}/R{n}/`  
2. Fail 关键截图拷到 `evidence/{系统}/R{n}/`  
3. 不在此步生成客户交付「7.测试记录.xlsx」（那是 **S5**）

---

## 8. 收口 DoD

- [ ] 波次下每个计划入口均有功能子目录 + `SUMMARY.md`（或 WAVE 标明跳过原因）  
- [ ] **子任务 A** 已产出 `results.xlsx`（列齐全）  
- [ ] **子任务 B** 已产出 `EXEC-SUMMARY.md`  
- [ ] 未改脚本期望充绿；C4 已登记回炉意向  
- [ ] WAVE.md 写明结束时间与命令摘录  

---

## 9. 文件索引

| 文件 | 职责 |
|------|------|
| **本手册** | S3 批量执行编排 + Kickoff + 强制子任务 |
| `prompts/_result.md` | 单条执行铁律 / 截图 / C 类 |
| `schema.md` §4.2 | 波次目录形状 |
| `tools/run-scripts.mjs` | 机跑 |
| `tools/aggregate-wave-results.py` | 波次 → Excel/JSON |
| `../func-test-playbook-index.md` | 命令总路由 S3 |
| `script-backfill-playbook.md` | S2 缺口补齐（本波不写脚本） |
