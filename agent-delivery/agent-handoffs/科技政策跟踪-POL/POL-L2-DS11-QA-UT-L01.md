# POL-L2-DS11-QA-UT-L01 · 政策分析评价 · 单元测试用例（第一阶段）

- 任务：`POL-L2-DS11-QA-UT-L01`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领：`agent:qa-agent`
- 状态：in_progress（不因本文件改状态）
- 强度：ponytail full
- 阶段：**第一阶段**（用例 + 数据准备验证）。第二阶段（接口与界面验证）待 `POL-L2-DS11-BE-L01` 合入后同任务续做，见文末待办段。

## 0. 依据与口径

| 分册 | 状态 |
|---|---|
| `sdd/l2/POL-L2-DS11-READ-API.md` | 已签收（223 短板/焦点、224、225、226 摘要） |
| `sdd/l2/POL-L2-DS11-VIZ-API.md` | 已签收（219 趋势、220 分区、221、222 模板） |
| `sdd/l2/POL-L2-DS11-PLAN-API.md` | **尚未落盘**（2026-11-03 Glob 全 agent-delivery 无该文件）。方案侧 227–231 以已落盘 `POL-L2-DS11-PLAN-ARCH.md` 第 2/3/4/8 节为对照基准；`kind` 参数名按 VIZ-API 既有先例假定，字段名以 BE 合入时契约为准。PLAN-API 落盘后须复核本文件 §3.5–3.9 与 §4 方案相关行。 |

空态总口径（三分册一致）：**无行则空，HTTP 成功；不造 0、不造默认模板、不返回 501、接口不直接返回 mock**。期望未发生必红。

公共数据事实（QA 已复核库 + 脚本，2026-11-03）：

| 表 | 行数 | 明细 |
|---|---|---|
| `gkxlumenx_gapfill.gapfill_policy_eval_shell` | 7 | entry_kind=解读 ×4（subject_name/conclusion_text/suggestion_text 必填、title/caption_text 必空）、多媒体 ×3（title/caption_text 必填、前三列必空）；**0 模板行**（0 选用行） |
| `gapfill_policy_eval_trend` | 44 | 时间 4 指标×6 年 + 区域 2 指标×6 地区 + 类别 2 指标×4 类 |
| `gapfill_policy_eval_partition` | 41 | 地区×投向 24 + 行业 10 + 目标群体 7 |
| `gapfill_policy_eval_scheme` | 19 | 方案对照 2 + 参数模拟 5 + 路径与风险 6（全部挂 `M_POLICY_DS_11_POLICY_EVAL_015`）+ 互动意见 6 |

二阶段验证不重灌数；仅 UT-02-3 需临时清表、UT-03-3 需临时清模板表，用后按 §1 脚本原样恢复。

## 1. 数据准备验证（已完成 · 2026-11-03）

三个脚本重跑 `--check`，不改脚本。命令（PowerShell，不要用 `&&`）：

```powershell
cd e:\zhipu\gkx-lumen\repos\lumen-algo-py
python scripts/seed_gapfill_policy_eval_shell.py --check
python scripts/seed_gapfill_policy_eval_viz.py --check
python scripts/seed_gapfill_policy_eval_scheme.py --check
```

输出（JSON，ok=true；中文键在 GBK 终端显示乱码，以 exit code 0 与 ok=true 为准）：

| 脚本 | --check 行数 | 预期 | 结论 |
|---|---|---|---|
| `seed_gapfill_policy_eval_shell.py` | 解读 4 + 多媒体 3 = **7** | 7 | PASS |
| `seed_gapfill_policy_eval_viz.py` | trend **44** + partition **41** | 44+41 | PASS |
| `seed_gapfill_policy_eval_scheme.py` | 对照 2 + 模拟 5 + 路径 6 + 意见 6 = **19** | 19 | PASS |

--check 同时覆写 `scripts/mysql/gapfill_policy_eval_*.sql`（脚本内建行为，不视为改脚本）。

恢复命令（临时清表用例用后还原，需 `LUMEN_ALGO_MYSQL_PASSWORD`）：

```powershell
python scripts/seed_gapfill_policy_eval_shell.py --apply
python scripts/seed_gapfill_policy_eval_viz.py --apply
python scripts/seed_gapfill_policy_eval_scheme.py --apply
```

## 2. 用例总览

共 **22 条**，编号 `UT-<模块>-<序号>`：UT-01 counts（3）、UT-02 jobs·解读二键（4）、UT-03 shells·解读/多媒体/模板（3）、UT-04 VIZ 趋势/分区（4）、UT-05 PLAN 方案五叶（5）、UT-06 白名单/种类分界回归（3）。

| 用例 | 资源 | 类型 | 一句话 |
|---|---|---|---|
| UT-01-1 | counts | 主路径 | region_gap 有行返回 shortboard_cnt |
| UT-01-2 | counts | 空态 | 无行不造 0 |
| UT-01-3 | counts | 越界 | 不动 ads 行 |
| UT-02-1 | jobs | 主路径 | policy_focus_ads 走 Job 后读 policy_focus |
| UT-02-2 | jobs | 主路径 | policy_text_parse 只查 summary |
| UT-02-3 | jobs | 空态 | summary 无行返回空、不清条款行 |
| UT-02-4 | jobs | 回归 | 旧键 policy_focus 行为不变 |
| UT-03-1 | shells | 主路径 | 7 行 4+3 分块返回 |
| UT-03-2 | shells | 只读 | 请求后行数/内容不变 |
| UT-03-3 | shells | 空态 | 0 选用行模板区空 |
| UT-04-1 | jobs kind=趋势 | 主路径 | 44 行按维+指标名返回点 |
| UT-04-2 | jobs kind=分区 | 主路径 | 41 行按对象/投向拣行 |
| UT-04-3 | jobs kind=趋势 | 空态 | 维或指标名对不上则图空 |
| UT-04-4 | jobs 趋势/分区 | 同步读表 | 不建任务不调 Python |
| UT-05-1 | jobs 方案对照 | 主路径 | 两方案对照行返回 |
| UT-05-2 | jobs 参数模拟 | 主路径 | 按方案+参数档拣行 |
| UT-05-3 | jobs 路径与风险 | 主路径 | 按方案返回节点与风险 |
| UT-05-4 | shells 互动意见 | 只读 | 读 6 行不插入 |
| UT-05-5 | shells 方案报告 | 生成 | 只从当次行生成 |
| UT-06-1 | jobs | 白名单 | 未放行键空结果不造数 |
| UT-06-2 | jobs | 分界 | kind 与 sub_type 同传整块空 |
| UT-06-3 | jobs/shells | 分界 | 一次请求只一种类 |

未覆盖（属第二阶段界面走查）：221 结构关联（无政策资源、无接口）、222 导出文件生成与操作日志空态的前端表现、切条件不自动起任务的浏览器行为、Job 失败不清空 counts/shells 的页面级表现。

## 3. 用例明细

> 通用前置：经网关 `https://<gw>/display/v1/policy/**` 打 `gkxlumen-display`（第二阶段起做）；单元层先在服务内直测 controller→element 读表逻辑与 Python `jobs/execute` 内部逻辑。「服务日志无 `polan.eval.focus.run`」在单元层以不调用该函数/mocker 断言。

### UT-01 · GET evaluation/counts（READ-API §3）

前置库：`ads.policy_effect`，拣行键 `scope_type='region_gap'`。

#### UT-01-1 短板条数 · region_gap 有行

- 数据准备：`ads.policy_effect` 存在 `scope_type='region_gap'` 行（库现状即有），记录该行 `shortboard_cnt` 值 N。
- 步骤：`GET /display/v1/policy/evaluation/counts`。
- 期望：HTTP 200；短板条数 = N；只统计 `scope_type='region_gap'` 行，其它 scope_type 行不计入。
- FAIL：返回 0 或 501；计入非 region_gap 行；调用 `polan.eval.gap.run`（该 GET 不触发 run）。

#### UT-01-2 短板条数 · 无行空态（不造 0）

- 数据准备：临时移除 `ads.policy_effect` 的 `region_gap` 行（QA 库或回滚态；不动共享 dev 库）。
- 步骤：同上 GET。
- 期望：HTTP 200；计数为空（null/缺省），**不造 0**，不返回 501。
- FAIL：返回 0；返回 501；接口内写死条数。
- 后置：恢复 region_gap 行。

#### UT-01-3 counts 越界不动数据

- 数据准备：同 UT-01-1。
- 步骤：GET 前后各取 `ads.policy_effect` 全行快照。
- 期望：快照完全一致；只读，无写库；`counts` 响应不含 `M_POLICY_OPPORTUNITY_COUNT` 改动（既有机遇读面原样）。
- FAIL：行数或内容变化；机遇读面被改写。

### UT-02 · POST evaluation/jobs（READ-API §4/§6）

前置库：`ads.policy_focus`（`polan.eval.focus.run` 产物，拣行键 `policy_id` 非空）、`ads.policy_text_parse`（拣行键 `summary`）。

#### UT-02-1 policy_focus_ads 主路径

- 数据准备：先由算法侧（或预置）执行 `polan.eval.focus.run` 写入 `ads.policy_focus`；确认存在 `policy_id` 非空行（含 `focus_score`、ext 内 `title`/`explanation`）与 policy_id 为空的机遇行各若干。
- 步骤：`POST /display/v1/policy/evaluation/jobs`，`sub_type=policy_focus_ads`；等待 Job 完成。
- 期望：Job 成功；结果只含 `policy_id` 非空行的 `focus_score`+ext `title`/`explanation`；机遇行（policy_id 空）不出现。
- FAIL：结果含 policy_id 为空行；返回写死指数；返回 `focus-one` 当场计算结果；白名单未放行时伪造数据。
- 附带断言：`run()` 只删 policy_id 非空行再写入，机遇行保留（前后机遇行数一致）。

#### UT-02-2 policy_text_parse 只查 summary

- 数据准备：`ads.policy_text_parse` 存在 summary 非空行；记录全表行数 T（含条款结构化行）。
- 步骤：`POST jobs`，`sub_type=policy_text_parse`；等 Job 完成。
- 期望：结果为 summary 行原样内容；**全表行数仍为 T**——该请求不调用 `polan.text.parse.run`（run 会清空整表，本请求禁止触发）；服务日志无 `polan.text.parse.run`。
- FAIL：返回写死段落；表行数变化；日志出现 parse.run。

#### UT-02-3 policy_text_parse 无 summary 行

- 数据准备：临时清空 `ads.policy_text_parse`（QA 库），确认 0 行。
- 步骤：同上 POST；等 Job 完成。
- 期望：摘要空；HTTP 成功；不返回写死段落、不 501。
- FAIL：返回任何摘要文本；返回 501。
- 后置：恢复表数据。

#### UT-02-4 旧键 policy_focus 回归（行为不变）

- 数据准备：既有 `policy_focus` 白名单路径可用；准备 items/产业或正文入参（既有校验要求）。
- 步骤：`POST jobs`，`sub_type=policy_focus`，带 items（合法入参）；再发一例走产业 VID 校验的请求。
- 期望：行为与合入前一致——仍要求 items、产业或正文，仍走 `harness.dispatch`，产业 VID XOR 校验照旧；新键的例外（不收 items、不走 XOR）**未**扩大到旧键（发不带 items 的 policy_focus 应仍被既有校验拒绝，拒绝方式不变）。
- FAIL：旧键校验被放宽或改道；旧键被改成 `policy_focus_ads` 语义；harness 返回被当成热点看板。

### UT-03 · GET evaluation/shells（READ-API §5 + VIZ-API §6）

前置库：`gkxlumenx_gapfill.gapfill_policy_eval_shell`（拣行键 `entry_kind` 与 `gap_item` 成对；0 模板行）；`gapfill_policy_eval_template`（0 选用行，模板表本身无 seed）。

#### UT-03-1 解读与多媒体行返回

- 数据准备：`seed_gapfill_policy_eval_shell.py --apply` 后库内 7 行：解读 4 + 多媒体 3。
- 步骤：`GET /display/v1/policy/evaluation/shells`（解读条目种类）；再以多媒体条目种类请求。
- 期望：解读块恰 4 条（subject_name、一句结论、一句应用建议），多媒体块恰 3 条（title+一句说明）；两块字段互斥（解读行无 title/caption_text 值，多媒体行无 subject/conclusion/suggestion 值）；不返回视频、动画、PDF、模板字节；点选条件只在已返回行内筛选。
- FAIL：解读块出多媒体行或反之；返回文件字节；查询触发灌数。

#### UT-03-2 shells 只读（意见行不插入）

- 数据准备：同上；另确认 `gapfill_policy_eval_scheme` 意见行 6 条（UT-05-4 共用前置）。
- 步骤：GET shells（含互动意见种类）前后各取 `gapfill_policy_eval_shell` 与 `gapfill_policy_eval_scheme` 快照（行数+内容）。
- 期望：两张表快照一致；互动意见块返回库内已有意见行（≤6），**请求不插入新意见**。
- FAIL：任一表行数或内容变化（=请求插入/更新/删除）。

#### UT-03-3 模板区空态（无默认模板）

- 数据准备：`gapfill_policy_eval_template` 0 选用行（库现状；模板表无灌数脚本，天然空）。
- 步骤：`GET shells`，`kind=模板选用`，template 取任一名。
- 期望：模板区空；HTTP 成功；**不出默认模板**、不返回写死模板、不 501；不读 `gapfill_policy_eval_shell` 充数。
- FAIL：返回任何模板行/默认模板；读壳表填模板区；501。
- 附带断言（同步分支）：不建任务、不进 `gkxlumen-topic-async-service`、不发 SSE。

### UT-04 · POST evaluation/jobs · kind=趋势/分区（VIZ-API §3/§4，同步读表非 Job）

前置库：`gapfill_policy_eval_trend`（拣行键 `switch_dim`+`metric_name`）、`gapfill_policy_eval_partition`（拣行键 `object_kind`，可选 `resource_direction`）。

#### UT-04-1 趋势主路径

- 数据准备：`seed_gapfill_policy_eval_viz.py --apply` 后 trend 44 行。
- 步骤：`POST jobs`，`kind=趋势`，`switch=['时间']`，`metric=['科技政策连续出台数']`；再按维切换发 区域+`研发投入强度`、类别+`科技政策连续出台数` 两例。
- 期望：每次只返回该维该指标的整条序列（时间 6 点 2021–2026；区域 6 点；类别 4 点）；每条序列含重点/波动标记（is_key_point/is_fluctuation 原样）；三维数据不串（时间请求不含区域/类别点）。
- FAIL：返回写死 2020–2026 序列或五维雷达；跨维混点；造默认曲线。

#### UT-04-2 分区主路径

- 数据准备：同上脚本，partition 41 行。
- 步骤：`POST jobs`，`kind=分区`，`subject='地区'`（不带 chart/allocation）；再发 `subject='行业'`、`subject='目标群体'` 两例；再发一例 `subject='地区'` + `allocation='财政资金'`。
- 期望：地区返回 24 行、行业 10 行、目标群体 7 行；不带 chart 时柱/热力用同一批行；带 allocation 只剩该投向行（地区+财政资金 = 6 行）；闭集外图种/投向不收、该图空。
- FAIL：返回演示矩阵；subject 缺省或多选补默认对象；另造城市名单。

#### UT-04-3 趋势空态

- 数据准备：同 UT-04-1。
- 步骤：`switch` 缺省或空；`metric` 缺省或空；`metric` 传表外名（如「弦线密度」）；`switch` 传闭集外维（如「行业」）。四例各发一次。
- 期望：四例全部图空，HTTP 成功，不补默认曲线，不 501。
- FAIL：任何一例返回了曲线/默认对象；501。

#### UT-04-4 趋势/分区为同步读表（不建任务不调 Python）

- 数据准备：同上。
- 步骤：发 UT-04-1/2 全部请求；检查异步任务表（topic-async 任务无新增）、SSE 无发布、服务间无对 Python `/internal/policy/jobs/execute` 调用。
- 期望：不建任务、不进 `gkxlumen-topic-async-service`、不调 Python、不占并发锁；响应即读表结果。
- FAIL：任务表新增记录；出现对 `/internal/policy/jobs/execute` 的调用；发 SSE。

### UT-05 · 方案五叶（PLAN-ARCH §2–§5；PLAN-API 未落盘，参数名按契约合入定稿复核）

前置库：`gapfill_policy_eval_scheme`，拣行键 `row_kind` + `scheme_name`（+`param_band`）；行数据按 §1 脚本。

#### UT-05-1 方案对照（227）

- 数据准备：scheme 19 行在库（对照 2：研发投入加力方案、人才引育优先方案）。
- 步骤：`POST jobs`，种类=方案对照，不选方案（读全部）；再分别指定两方案各发一次。
- 期望：默认返回 2 条对照行（名称、说明、compare_dims、优劣结论、实施建议）；指定方案返回该方案 1 行；雷达/KPI 数值即行上对照值，Java 不补演示分。
- FAIL：返回 demo `policyData.js` 三条常量方案；少于 2 行时仍出对比（当前库 2 行不触发，此断言留边界注记）；501。

#### UT-05-2 参数模拟（228）

- 数据准备：同上（参数模拟 5 行：研发 3 档 + 人才 2 档）。
- 步骤：`POST jobs`，种类=参数模拟，方案=研发投入加力方案 + 参数档=资金规模基准档；再发对不上的组合（方案=人才引育优先方案 + 档=资金规模基准档）；再发缺方案一例。
- 期望：匹配组合返回该行（评估结果、一句趋势、归档说明）；对不上则预览空；缺方案该块空；请求内不现算、不调用 `polan.text.simulate`；采纳不写库。
- FAIL：对不上仍返回数据；弹性公式现算；调用 simulate.run；缺方案补默认方案。

#### UT-05-3 路径与风险（229）

- 数据准备：同上（路径 6 行：两方案各 3 节点，metric_id 全挂 `M_POLICY_DS_11_POLICY_EVAL_015`）。
- 步骤：`POST jobs`，种类=路径与风险，方案=研发投入加力方案；再发方案=不存在方案一例。
- 期望：返回该方案 3 行（节点、时间进度、节点说明、风险标题、风险说明）；行上 metric_id 为 `M_POLICY_DS_11_POLICY_EVAL_015`；不存在方案则路径与风险都空；不读图、不写 nGQL、不返回推演曲线。
- FAIL：返回推演曲线顶替；出现任何 Nebula/nGQL 调用；501。

#### UT-05-4 互动意见只读（230）

- 数据准备：同上（意见 6 行：两方案各 3 条，分类 评价/评论/建议）。
- 步骤：`GET shells`，种类=互动意见，方案=研发投入加力方案；请求前后取 scheme 表快照。
- 期望：返回该方案 3 条意见（主体、分类、正文、时间）；分类只用 评价/评论/建议；**快照一致（请求不插入）**；不选方案则意见列表空。
- FAIL：请求后意见行数变化；出现 评价/评论/建议 之外分类；不选方案仍返回全部。

#### UT-05-5 方案报告只从当次行生成（231）

- 数据准备：同上（对照 2 + 意见 6）。
- 步骤：`GET shells`，种类=方案报告，范围=研发投入加力方案（该方案对照 1 行 + 意见 3 行）；再发范围=不存在方案一例。
- 期望：报告内容只含当次读到的该方案对照行与意见行字段；不存在方案则导出空；响应不内嵌写死 PDF/Word；不写对象存储；不另建报告行。
- FAIL：报告内容含库外文案（对照行/意见行之外的正文）；返回写死文件；写对象存储。

### UT-06 · 白名单与种类分界回归（READ-API §2 + VIZ-API §2/§8）

#### UT-06-1 新键未放行时空结果

- 数据准备：若 BE 合入初期白名单尚未含 `policy_focus_ads`/`policy_text_parse`，此用例在该窗口执行；已放行则跳过并记录。
- 步骤：`POST jobs`，`sub_type=policy_focus_ads`（与 policy_text_parse 各一例）。
- 期望：Job 返回空结果；不返回写死指数/摘要；不放行不造数。
- FAIL：未放行却返回数据（含写死值）。

#### UT-06-2 kind 与 sub_type 同传

- 数据准备：同 UT-04/UT-02。
- 步骤：`POST jobs`，同时带 `kind=趋势` 与 `sub_type=policy_focus_ads`。
- 期望：该块空；不建任务、不读趋势表、不转发异步；HTTP 成功不 501。
- FAIL：建了任务；读了趋势表；转发了异步；501。

#### UT-06-3 一次请求只一种类

- 数据准备：同上。
- 步骤：`POST jobs` 尝试一次同传趋势+分区（或方案对照+参数模拟）；`GET shells` 尝试同传模板选用+解读条目（或互动意见+方案报告）。
- 期望：非法组合不建任务、不读多张表、该块空（按分册分发语义）；趋势与分区必须两次请求。
- FAIL：一次请求同时读 trend 和 partition（或 scheme 多种类混读）；同请求既同步填趋势/分区又转发异步。

## 4. 失败分类与缺陷登记

二阶段执行结果按以下分类登记（缺陷走 gkx-bug-record，KJXXZSXT 系统）：

| 分类 | 判定 | 示例 |
|---|---|---|
| A 违反空态口径 | 无行返回 0/501/写死 mock | UT-01-2 返回 0 |
| B 只读破坏 | 请求导致写库 | UT-03-2 意见行数变化 |
| C 链路越界 | 绕过 element 直连库/Python、浏览器改打 `/topic/v1/policy`、调 demo-* | UT-04-4 出现 `/internal` 调用 |
| D 回归破坏 | 旧键/既有读面行为变化 | UT-02-4 旧键校验放宽 |
| E 数据缺项 | 表行数与 §1 不符（先核对是否被误清） | trend ≠ 44 |

## 5. 第二阶段待办（本轮不做；BE POL-L2-DS11-BE-L01 合入后续做）

1. **接口验证**：经网关调 `/display/v1/policy/evaluation/counts|jobs|shells/**`，跑 §3 全部用例的 HTTP 层（关键路径优先：UT-01-1/2、UT-02-1/2、UT-03-1/2/3、UT-04-1/2、UT-05-1/4）。
2. **界面走查**：K8s dev 前端评价页操作流走查（短板计数 → 焦点 → 解读/多媒体 → 趋势/分区 → 方案五叶），截图存 `agent-delivery/agent-handoffs/科技政策跟踪-POL/screenshots/`（目录不存在则建）。
3. **前端未就绪项**：如实标注「前端未就绪」，不伪造截图。
4. **PLAN-API 复核**：该分册落盘后复核 §3.5–3.9 参数名与 §0 对照基准。
5. 完成后按任务规约回填 evidence/note（联调/测试关键词），状态流转按 registry 流程。

## 6. 架构合规自检

- ✅ 只写用例文档 + 重跑 --check，不改脚本、不改 Java/Python 代码、不碰 lumen-svc-platform
- ✅ 数据事实核对以库与脚本 --check 为准（不造数）
- ✅ 期望未发生必红（各用例 FAIL 行）
- ✅ 缺项表只读断言（UT-03-2/UT-05-4 前后快照）
- ✅ 未把 mock 写成已上线、不改 D4 口径表述
- ⚠️ PLAN-API 未落盘，方案侧以 PLAN-ARCH 对照，已在 §0 声明并留二阶段复核项
