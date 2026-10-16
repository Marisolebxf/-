# 功能测试工作总索引（命令路由）

> **用途**：人说一句「执行某某系统的某某工作」时，父 agent **先读本文件**，再按表跳转规约与 Kickoff。  
> **范围**：仅 **FUNC 功能测试**（兼容/集成/性能/安全另见 `perf-baseline.md` 等）。  
> **系统码**：专题 `KJZTFWXT` · 展示 `KJXXZSXT` · 算法库 `SDWJSF/KJZTFWSFK`（目录名用 `-`）。  
> **不替代**：单步写法仍以 `as-built/prompts/_*.md` 为真源；本文件只做**路由 + 启动词 + 就绪门**。

---

## 0. 一句话怎么用

1. 解析命令 → 对照 **§1 命令路由表** 得到阶段码（S1～S5）。  
2. 查 **§2 系统就绪门**（展示环境未锁则停，先补 catalog/env）。  
3. 打开该阶段「必读」；把 **§3 Kickoff** 整段贴进新对话（改系统码/入口）。  
4. 进度与产物路径见路由表「产物」列。

---

## 1. 命令路由表（功能测试五阶段）

| 阶段 | 人话命令（同义） | 成熟度 | 必读（按序） | 产物 | 编排补充 |
|------|------------------|--------|--------------|------|----------|
| **S1 用例编写** | 执行{系统}的用例编写，按 B 线 | ✅ 专题已跑通；展示未开 | ① `as-built/prompts/_case.md` ② `qa-test-case-spec.md` ③ `templates/test-case-template.md` ④ `code-registry.yaml`（取号）⑤ 该系统 A 线 `total-set/{系统}/` 仅作覆盖矩阵对照 | `test-cases/{系统}/**/FUNC-*-用例.md` + `coverage-fp.md` | catalog 建入口；B 线现场起稿，**禁止**按 A 线功能点一对一灌用例 |
| **S2 脚本编写** | 执行{系统}的用例脚本编写（含补齐缺口） | ✅ 专题金样+补齐手册；展示未开 | ① `_script.md` ② `schema.md` ③ `retro/20261014-batch32-method-patch.md` ④ 有缺口时 `script-backfill-playbook.md` | `as-built/scripts/{系统}/…/index.yaml` + `cases/*.yaml` + `coverage.md` + `fixtures/` | 三角色：闸门→写稿子(≤4)→**独立验收子串行**；禁止谁写谁验；父不跑机跑；子不改 catalog |
| **S3 脚本执行** | 执行{系统}的用例脚本执行（冒烟/全量/回归） | ✅ 批量编排已建 | ① **`as-built/script-batch-run-playbook.md`** ② `_result.md` ③ `schema.md` §4.2 ④ `tools/run-scripts.mjs` + `aggregate-wave-results.py` | 波次目录 `as-built/runs/{日}-50892-{wave}/`（**不入库**）+ **强制** `results.xlsx` + `EXEC-SUMMARY.md`；正式轮次再拷 `test-records/` + `evidence/` | 三种模式 smoke/full/regress；串行机跑；结束后必须派 Excel+总结两个子任务；禁止改脚本充绿 |
| **S4 用例交付合并** | 执行{系统}的用例交付文档合并，按 B 线合并 A 线，用例可拆分，需覆盖所有功能点 | 🟡 骨架已建；专题已出 **B∪A** 约 886 行；未覆盖/政策等仍缺口 | ① **`case-delivery-playbook.md`** ② `_submit.md` ③ `scripts/_gen_zt_delivery_func_ab_merge.py` ④ `delivery/…/ab-merge-manifest.md` ⑤ `delivery/README.md` | `delivery/{系统}/6.…_测试用例.xlsx` + manifest | 未覆盖不投影；全覆盖须先消缺口或豁免；专题默认一键重跑 |
| **S5 可交付测试记录** | 根据脚本执行结果+用例交付文档，生成可交付测试记录 | 🟡 骨架已建（Kickoff/列映射/DoD）；导出脚本与 Bug 渠道待补 | ① **`record-delivery-playbook.md`** ② `templates/test-record-template.md` ③ `delivery/README.md` 清检单 ④ S3 正式 `test-records/R{n}` + 6.x 用例簿 | `delivery/{系统}/7.…_测试记录.xlsx` + `test-records/` 工作稿 | 输入=正式轮次非调通 runs；是否通过仅通过/不通过；阻塞跳过须先消化 |

**专题 vs 展示**：上表方法论**跨系统共用**；换系统 = 换系统码、catalog、env、取号段。展示当前 **catalog=`placeholder`、env 未锁**（`as-built/catalog/index.yaml`）——S1～S3 开干前必须先锁环境并填 catalog。

---

## 2. 系统就绪门

| 系统 | catalog | 环境 | S1～S3 | S4～S5 |
|------|---------|------|--------|--------|
| `KJZTFWXT` 专题 | active · 50892 | ✅ `http://111.198.38.90:50892/` | 可执行 | S4 骨架+已有 B∪A（886）见 `case-delivery-playbook.md`；S5 见 `record-delivery-playbook.md` |
| `KJXXZSXT` 展示 | placeholder · env=null | ❌ 未锁 | **先**：定已发布 URL + 填 `catalog/KJXXZSXT.yaml` live 入口 + `catalog/index.yaml` locked_env | 用例/脚本齐后方可 |
| `SDWJSF-KJZTFWSFK` 算法库 | placeholder · 多 `no_ui` | 无独立用户前端 | 以 API/算法验收为主，不套本表 UI B 线 | 另议 |

---

## 3. Kickoff 模板（复制后改【】）

### S1 · B 线用例编写

```text
【身份】qa-agent。阶段 S1·B 线用例编写。总索引：qa/func-test-playbook-index.md
【系统】【SYSTEM=KJXXZSXT|KJZTFWXT】
【工作根】…/gkx-orchestration
【必读】as-built/prompts/_case.md → qa-test-case-spec.md → templates/test-case-template.md → code-registry 取号
【做法】现场（已发布前端）勘察 → 按页面场景写 FUNC 册；覆盖矩阵对照 total-set/【SYSTEM】/；未覆盖允许登记，禁止按功能点一对一灌用例
【产物】test-cases/【SYSTEM】/…/FUNC-*-用例.md + coverage-fp.md
【禁止】改业务仓；A 线灌用例；未锁 env 时对展示硬开
开干：先确认 §2 就绪门，再按 catalog 入口清单逐模块派子任务（建议一模块一子会话）。
```

### S2 · 脚本编写 / 补齐

```text
【身份】qa-agent 父控。阶段 S2。总索引：qa/func-test-playbook-index.md
【系统】【SYSTEM】
【必读】_script.md → schema.md → method-patch；若补缺口再读 script-backfill-playbook.md
【第一步】python3 qa/as-built/tools/gap-func-vs-scripts.py --system 【SYSTEM】 --write（专题已支持；展示需先有映射）
【执行】闸门一次 → 写稿子一用例（≤4）→ 独立验收子串行 --only（禁止谁写谁验；父不跑机跑）详见 script-backfill-playbook §2/§5
【禁止】有头浏览器；子改 catalog；全量刷分入库 runs；改业务仓
```

### S3 · 脚本执行（冒烟 / 全量 / 回归）

> 完整 Kickoff 与强制子任务见 **`as-built/script-batch-run-playbook.md` §0**（勿在本索引复制第二份长文）。

```text
【身份】qa-agent 父控。阶段 S3。总索引：qa/func-test-playbook-index.md
【必读】as-built/script-batch-run-playbook.md（全文）→ _result.md → schema.md §4.2
【系统】【SYSTEM=KJZTFWXT】 环境：http://111.198.38.90:50892/
【模式】【smoke | full | regress】  波次：as-built/runs/【YYYYMMDD】-50892-【WAVE_ID】/
【执行】父串行 run-scripts.mjs，一律 --run-dir $WAVE/<功能短名>（多功能禁止共用 run-dir）
【收口必须派两个子 Task】A Excel（aggregate-wave-results.py → results.xlsx）B EXEC-SUMMARY.md
【禁止】改脚本充绿；并行多个 run-scripts；localhost；缺 A/B 宣称完成
```

### S4 · 用例交付（B 合并 A / 覆盖功能点）

> 完整 Kickoff / 列口径 / DoD：[`case-delivery-playbook.md`](case-delivery-playbook.md)。

```text
【身份】qa-agent 父控。阶段 S4。总索引：qa/func-test-playbook-index.md
【必读】qa/case-delivery-playbook.md → as-built/prompts/_submit.md → delivery/README.md
【系统】【SYSTEM=KJZTFWXT】 模式【full-regen|module-patch】
【产物】delivery/【SYSTEM】/6.…_测试用例.xlsx + ab-merge-manifest.md
【专题重跑】python3 agent-delivery/scripts/_gen_zt_delivery_func_ab_merge.py
【禁止】未覆盖造行；场景全文充多行；为投影行新写脚本
```

### S5 · 可交付测试记录

> 完整 Kickoff / 列映射 / DoD：[`record-delivery-playbook.md`](record-delivery-playbook.md) §1～§6。

```text
【身份】qa-agent 父控。阶段 S5。总索引：qa/func-test-playbook-index.md
【必读】qa/record-delivery-playbook.md → templates/test-record-template.md → delivery/README.md 清检单
【系统】【SYSTEM】 正式轮次 R【n】
【输入】test-records/【SYSTEM】/R【n】/ + evidence + delivery/【SYSTEM】/6.…测试用例.xlsx
【产物】delivery/【SYSTEM】/7.…_测试记录.xlsx
【禁止】调通 runs 充交付；是否通过写跳过/阻塞；臆造 BUG 号
```

---

## 4. S4 口径说明（B∪A 与现行 `_submit`）

| 项 | `_submit.md` 现行 | 你描述的「B 合并 A、覆盖所有功能点」 |
|----|-------------------|--------------------------------------|
| 未覆盖功能点 | **不投影** | 必须先 **S1 补场景** 或 PM 签字豁免，再投影 |
| 行粒度 | 一已覆盖功能点一行（场景切点） | 同左；允许为覆盖而 **拆** 场景/投影行 |
| 专题已做 | 多为 **仅 B 线** 交付 Excel（A 列可空） | 展示若要求全覆盖，开单时写明「须合 A」并验收矩阵 0 未覆盖（或豁免表） |

S4 稳定后可把「合 A 检查清单」升格进 `_submit.md` 附录；未升格前以本 § 为准。

---

## 5. 文档地图（按目录）

```text
qa/
  func-test-playbook-index.md     ← 本文件（命令路由）
  case-delivery-playbook.md       ← S4 用例交付合并编排（骨架）
  record-delivery-playbook.md     ← S5 可交付测试记录编排（骨架）
  README.md                       ← 工作区总览（偏目录说明）
  qa-test-case-spec.md            ← 编号/主表列规范
  perf-baseline.md                ← 性能（非本表）
  as-built/
    prompts/_case|_script|_result|_submit.md
    script-backfill-playbook.md   ← S2 缺口补齐编排
    script-batch-run-playbook.md  ← S3 批量执行（冒烟/全量/回归 + Excel/总结）
    schema.md · catalog/ · scripts/ · tools/
  test-cases/ · test-records/ · evidence/
  total-set/                      ← A 线功能点
  delivery/                       ← 6/7/8 交付成品
templates/test-case|test-record|test-retest-template.md
```

相关 handoff（样板，非永远最新）：`agent-handoffs/QA/QA-ASBUILT-SCRIPT-BATCH32-*`（S2 金样）、`QA-KJZTFWXT-BLINE-DELIVERY-EXCEL-*`（S4 B 线）、`QA-KJZTFWXT-BLINE-CASE-*`（S1 粒度）。

---

## 6. 维护

- 新阶段 playbook（如 S5）落盘后：**只改本索引一行**，勿再散落多处 Kickoff。  
- 新系统：先 `catalog/index.yaml` + env，再复制 Kickoff 换系统码。  
- 与 `qa/README.md`：README 管「目录有什么」；**本文件管「命令怎么干」**。
