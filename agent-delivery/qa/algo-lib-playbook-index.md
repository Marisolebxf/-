# 科技专题服务算法库 · QA 工作总索引（命令路由）

> **用途**：人说「执行算法库的某某工作」时，父 agent **先读本文件**，再按表跳转对应 playbook 与 Kickoff。  
> **系统码**：`SDWJSF/KJZTFWSFK`（编号内 `/`）；目录名 **`SDWJSF-KJZTFWSFK`**。  
> **环境**：联调台 `https://edu.itic-sci.com/dma/algovwz/`（`50897` 已停用）。catalog 见 `as-built/catalog/SDWJSF-KJZTFWSFK.yaml`。  
> **不替代**：各阶段细则以链接的 playbook / 原则 / `prompts/_*.md` 为真源；本文件只做 **路由 + 父/子分工 + 启动词**。

---

## 0. 一句话怎么用

1. 解析命令 → 对照 **§1 命令路由表** 得到阶段码（**A 线** F0～F4 · **B 线** S1～S5）。  
2. 查 **§2 就绪门**（catalog SHA、原则版本、金样闸门）。  
3. **A 线**：打开 `fp-split-by-api-playbook.md`；父控 **§3**、子 agent **§4**。  
4. **B 线**：打开 [`algo-lib-api-case-playbook.md`](algo-lib-api-case-playbook.md)；父控 **§5**、子 agent **§6**。  
5. A 线所有拆表/写 work·review **只在子 agent**；B 线按 catalog 页派子写 FUNC 册。第三轮规则在 api-case playbook **§长任务返工**。

---

## 1. 命令路由表

### A 线 · 功能点拆分（by-api v0.2.1，对外唯一交付）

| 阶段 | 人话命令（同义） | 成熟度 | 任务说明（必读） | 产物 | 父控做什么 |
|------|------------------|--------|------------------|------|------------|
| **F0 准备** | 算法库 by-api 准备 / 刷新 catalog / 生成提示词 | ✅ | ① 本索引 ② [`fp-split-by-api-playbook.md`](total-set/SDWJSF-KJZTFWSFK/fp-split-by-api-playbook.md) §F0 ③ 原则 **0.2.1** ④ `fp-split-by-api-run/00-control.md` | `_catalog-snapshot.md`、`_l6-to-catalog-map.yaml`、`prompts/L01–L60.md`、`01-task-list.md` | 跑 snapshot 脚本；跑 `_gen_kjztfwalgo_fp_by_api_prompts.py`；**不**写 work |
| **F1 金样 L01** | 算法库功能点拆分 L01 / 产业链基础指标金样 | ✅ 提示词可生成 | playbook §F1 + `prompts/L01.md` + 原则 0.2.1 | `work/L01.md`、`review/L01.md` | **派 1 个子 agent**；人确认通过后改队列 `L01=done`、开 F2 |
| **F2 金样 L13** | 算法库功能点拆分 L13 / 图谱 API 金样 | 🟡 须产出图谱 endpoint 封闭清单 | playbook §F2 + `prompts/L13.md` + 4A | `work/L13.md`、`review/L13.md`、`memo/L13-graph-endpoint-closure.md`（建议） | 派 1 个子 agent；人确认后开 F3 |
| **F3 并行六级** | 算法库功能点拆分全量 / 派 L02–L60 | 闸门：F1+F2 已过 | playbook §F3 + `01-task-list.md` + 各 `prompts/Lxx.md` | 每路 `work/Lxx.md` + `review/Lxx.md` | **每六级 1 子 agent**（建议每批 ≤4～8 路）；父不代写表 |
| **F4 合表** | 算法库 by-api 合表 / 校验 3c | 🔴 校验脚本待建 | playbook §F4 + 原则 §四（12a 扩展列） | `6.…_功能点拆分-by-api_v1.xlsx` | 父跑校验绿后派子或脚本合表；禁止覆盖 v2 需规 xlsx |

- **任务 ID（拟）**：`QA-KJZTFWALGO-FP-BY-API-L01`（MCP 待 PM 补建）。  
- **需规 v2 合表**：`fp-split-run/` → **内部对照**，不是算法库对外交付（原则 #1）。  
- **旧 by-api 0.1**：`fp-split-by-api-run-v0-202609/` 只读。

### B 线 · 接口向测试（本系统专用 playbook）

| 阶段 | 人话命令（同义） | 成熟度 | 任务说明（必读） | 产物 | 父控做什么 |
|------|------------------|--------|------------------|------|------------|
| **S1 用例编写** | 算法库用例编写 / 第三轮 FUNC 重写 / B 线 S1 | ✅ 可开 | ① [`algo-lib-api-case-playbook.md`](algo-lib-api-case-playbook.md) **§编写方法论 + §长任务返工** ② §S1 ③ `qa-test-case-spec.md` ④ `code-registry` 的 **`next_seq.FUNC`** ⑤ `_case.md` 仅文字红线 ⑥ `01-task-list.md` + `_l6-to-catalog-map.yaml` | `FUNC-*-用例.md` + `coverage-fp.md`（删同目录旧 API 册） | 按 catalog 页派子；验收 §细则 I |
| **S2 脚本** | 算法库测试脚本 / 金样已写 | 🟡 截图已放行，可按页编写 | playbook §S2 | `as-built/scripts/SDWJSF-KJZTFWSFK/basic/chain-basic/` | 2026-10-22 人已看金样截图。先补本页 FUNC-00003、00005–00023，再按页派。00001、00004 保持失败 |
| **S3 执行** | 算法库冒烟/全量 | 🔴 未开 | playbook §S3 | `as-built/runs/*-algovwz-*` | 金样截图已看。全库执行等脚本按页落盘后再开波次 |
| **S4 交付用例簿** | 算法库 6.x 测试用例 | ✅ 已出表（2026-10-20，FUNC-00001～01500） | playbook §S4 | `delivery/SDWJSF-KJZTFWSFK/6.国际科技信息中心项目_科技专题服务算法库_测试用例.xlsx` | 不重出，除非用例册又改 |
| **S5 测试记录** | 算法库 7.x 测试记录 | 🟡 骨架 | playbook §S5 + `record-delivery-playbook.md` | 同上 | 待 S3 正式轮次 |

专题/展示 B 线仍走 [`func-test-playbook-index.md`](func-test-playbook-index.md)；**算法库 B 线不要**套用其 S1「页面区块」Kickoff。

---

## 2. 就绪门

| 检查项 | A 线 | B 线 |
|--------|------|------|
| 原则版本 | `科技专题服务算法库-功能点拆分原则-by-api.md` = **0.2.1** | 同左（矩阵对照） |
| catalog | `fp-split-by-api-run/_catalog-snapshot.md` 与 map 一致 | `as-built/catalog/SDWJSF-KJZTFWSFK.yaml`；执行环境 **algovwz** |
| 金样闸门 | **L01、L13** 人确认前 F3 **禁止** | S1 **无**硬依赖合表；建议首册金样 `chain.basic`（与 L01 对齐） |
| 子 agent | 只写本六级 `work`+`review` | 只写本 `catalog_page_id` 一册 API + 本页 coverage |
| 并发 | F3 分批；本机会话 ≤20 | 按 catalog 页分批派 S1 |

---

## 3. 父控 Kickoff · A 线（复制后改阶段）

```text
【身份】qa-agent 父控（调度/归纳，不写六级功能点表）
【总索引】agent-delivery/qa/algo-lib-playbook-index.md
【阶段】【F0|F1|F2|F3|F4】算法库 A 线 by-api 功能点拆分
【任务说明】agent-delivery/qa/total-set/SDWJSF-KJZTFWSFK/fp-split-by-api-playbook.md
【原则】…/科技专题服务算法库-功能点拆分原则-by-api.md（0.2.1）
【控制面】…/fp-split-by-api-run/00-control.md + 01-task-list.md
【系统】SDWJSF/KJZTFWSFK · 工作根 ${GKX_ROOT}/gkx-orchestration

【父控职责】
- 读索引与 playbook，维护 01-task-list / 00-control 状态
- 按闸门派子 agent（F1=L01，F2=L13，F3=每六级一条 prompts/Lxx.md）
- 验收：review 通过、条数一致、4A/3c/7b 自检项；归纳全库行数
- 禁止：父对话自己写 work/Lxx.md 功能点表；禁止脚本批量改 60 份 work

【本回合】（示例 F1）
- 派 1 个子 agent，Kickoff 用本索引 §4，Lxx=L01
- 子完成后你检查 review，更新队列，向人汇报是否可进 F2

开干：先读 00-control 当前阶段，再执行。
```

---

## 4. 子 agent Kickoff · A 线（每六级一条，复制后改 Lxx）

```text
【身份】qa-agent 执行子（只做一条六级）
【总索引】agent-delivery/qa/algo-lib-playbook-index.md
【任务说明】agent-delivery/qa/total-set/SDWJSF-KJZTFWSFK/fp-split-by-api-playbook.md §子 agent
【原则】…/科技专题服务算法库-功能点拆分原则-by-api.md（0.2.1）
【本六级提示词】…/fp-split-by-api-run/prompts/L【xx】.md（全文必读，按其中需规+catalog 拆）

【Lxx】L【xx】
【只产出】
1. …/fp-split-by-api-run/work/L【xx】.md
2. …/fp-split-by-api-run/review/L【xx】.md
（L13 另附 memo/L13-graph-endpoint-closure.md 若提示词要求）

【表列】主列 + GKX 扩展列：endpoint_id、METHOD、path、field_key、catalog_status（12a）
【禁止】读 lumen-algo-* / demo-algo-* 实现；读 fp-split-by-api-run-v0-202609 当答案抄；改其它 Lxx；合表；派子任务

开干：读完 prompts/L【xx】.md 后只拆本六级，落盘 work+review。
```

---

## 5. 父控 Kickoff · B 线 S1（用户只开父对话 · 复制本段即可）

> 用户**不**手贴子 Kickoff。父控用 **Task 子 agent**（或 Background Agent）派单；§6 为**嵌入派单描述**的子任务包模板，由父控填入 `catalog_page_id` 后整段传给子 agent。

```text
【身份】qa-agent 父控（本会话只调度/验收/归纳，不亲自写整册用例表）
【总索引】agent-delivery/qa/algo-lib-playbook-index.md
【阶段】S1·算法库用例第三轮（页面操作 + FUNC）
【任务说明】agent-delivery/qa/algo-lib-api-case-playbook.md §长任务返工
【工作根】${GKX_ROOT}/gkx-orchestration
【系统】SDWJSF/KJZTFWSFK
【环境】https://edu.itic-sci.com/dma/algovwz/（50897 已停用，禁止写入步骤）
【文档真源】repos/lumen-ui-algo-apiview/src/catalog/*.json
【需规层级】fp-split-by-api-run/01-task-list.md + _l6-to-catalog-map.yaml

【父控必读】algo-lib-api-case-playbook **§编写方法论 + §编写细则 + §长任务返工** → §S1 → qa-test-case-spec → code-registry 的 next_seq.FUNC

【本回合】第三轮。API-00001～02210 全部作废不复用。89 个在用 catalog 页全部重写为 FUNC 册。新号从 FUNC-00001 起。父控按「该页现有用例条数 + 2」预分配闭区间（多出的 2 条给接口信息清单和算法测试清单）。本会话内自己循环派批，不要再套 /loop。不合 A 线。全部页完成后父控重出工作区 Excel 和 delivery 模板 Excel。

【父控流程】
1. 读 §长任务返工。不要把 run-log 旧批次的 89/89 当成已完成。
2. 每批最多 4 个 Task，每任务 1 个 catalog 页；任务描述用 §6，并带上 FUNC 闭区间。
3. 验收 §编写细则 I：步骤是页面操作；模块列是三至六级或「待挂需规」；测试内容含「验证」和「检查」；功能点无自行添加的 A1/A2；0 条登录/401 用例；正向预期含 sampleResponse 字段；反向每参数 1 条；另有接口信息、算法测试各 1 条清单用例。不合格只返工 1 次，仍不合格则跳过。
4. 连续 2 批全跳过，或 catalog JSON 读不到，则停机。不要问人。
5. 全部页清空后，父控重出两份 Excel：工作区 `科技专题服务算法库-API测试用例.xlsx` 与 `delivery/SDWJSF-KJZTFWSFK/6.国际科技信息中心项目_科技专题服务算法库_测试用例.xlsx`。按客户模板 17 列从 FUNC 册搬入，仍不合 A 线。然后输出总表并停止。

【父控禁止】自己写用例表；浏览器 MCP / Playwright / curl；读 lumen-algo-py、demo-algo-*；改 A 线 work；取 API 号；复用 API-00001～02210。

开干：从 FUNC-00001 切第一批号段，派 4 页。chain.basic 放在第一批，作为风格样例。
```

---

## 6. 子任务包 · B 线 S1（由父控嵌入 Task 描述，用户不直接粘贴）

父控复制下框，替换【】后作为 **单个子 agent 的 Task 全文**：

```text
【身份】qa-agent 执行子（隔离上下文；只做一页 catalog）
【派单来源】父控 S1 第三轮批次【批次名，如 金样-chain.basic】
【任务说明】agent-delivery/qa/algo-lib-api-case-playbook.md §编写细则（全文）+ §长任务返工 + §S1
【工作根】${GKX_ROOT}/gkx-orchestration
【环境】https://edu.itic-sci.com/dma/algovwz/（步骤按此写，禁止打开页面，禁止写 50897）

【文档】repos/lumen-ui-algo-apiview/src/catalog/*.json 中 catalog_page_id=【如 chain.basic】
【需规】01-task-list.md 的五级/六级；_l6-to-catalog-map.yaml。无六级则功能项和子功能项都写「待挂需规」。一页多个六级时按 endpoint 归属拆开
【页】功能点 = endpoints[].title，去掉自行添加的「A数字 」前缀
【编号】只用父控 FUNC 闭区间【起-止】。禁止任何 API- 号
【A 线】fp-split-by-api-run/work/【如 L01】.md 只做覆盖矩阵，不代替接口文档，禁止 field 一行一用例

【产物】test-cases/SDWJSF-KJZTFWSFK/…/FUNC-【页】-用例.md 与 coverage-fp.md
【填写完整相对路径】
写完后删除同目录 API-*-用例.md

【写法】
- 功能模块=算法工具库；子功能模块=科技专题服务算法库；功能项=五级；子功能项=六级；页面=页标题；功能点=下拉标题
- 场景写在备注：场景=主流程 / 备选-参数组合 / 异常-入参-缺{参数}
- 测试内容：「验证{功能点}功能，检查{本条要确认的事}」
- 步骤：侧栏进入页面 → 下拉选择接口 → 按附录组合填参 → 点击调用。登录只写前置条件
- 每个 title 至少 1 条主流程。正向覆盖合法参数组合，预期逐字段写 sampleResponse。反向每个参数 1 条，预期写该参数的错误说明。status=unavailable 同样写，备注注明未交付
- 另写 2 条，不点击调用：场景=接口信息-清单、场景=算法测试-清单。核对页头或下拉的接口数量、名称、method 和 path；切换一个接口后这三项跟着变，其它区域只要求正常刷新，不逐字段核对。只有 1 个接口时不切换
【禁止】登录用例、Token、401、424、预期只写 HTTP 4xx；步骤写 GET/POST；打开 algovwz/50897；浏览器 MCP；Playwright；读 lumen-algo-py / demo-algo-*；改其它页和 A 线 work；自行添加 A1、A2。

【交卷】接口数、主流程条数、反向条数、清单是否恰好 2 条、功能点是否都能搜到且无 A 序号、抽 1 条步骤是否为页面操作。

开干：只读该页 catalog JSON 和对应六级，按号段写入 FUNC 册。
```

---

## 7. 文档地图

```text
qa/
  algo-lib-playbook-index.md          ← 本文件（算法库 QA 总路由 A+B）
  algo-lib-api-case-playbook.md       ← B 线 S1～S5 编排真源
  func-test-playbook-index.md         ← 专题/展示 B 线；算法库仅跳转本索引
  total-set/SDWJSF-KJZTFWSFK/
    科技专题服务算法库-功能点拆分原则-by-api.md
    fp-split-by-api-playbook.md       ← A 线 F0～F4
    fp-split-by-api-run/
  test-cases/SDWJSF-KJZTFWSFK/        ← B 线 S1（第三轮 FUNC-*；金样 chain.basic）
  as-built/catalog/SDWJSF-KJZTFWSFK.yaml
```

---

## 8. 维护

- 新 **A** 线阶段：先写 `fp-split-by-api-playbook.md`，再在本索引 §1 增一行。  
- 新 **B** 线阶段或 S2/S3 落地：先写 `algo-lib-api-case-playbook.md`，再改 §1 B 线表。  
- **禁止**在 `func-test-playbook-index.md` 维护算法库 API 向长文 Kickoff。
