# KG-COMPLY-LOAD-T01 · 缺口清单修正说明（致白鑫凤）

| 项 | 内容 |
|---|---|
| 收件人 | 燕大 · 白鑫凤 |
| 发件人 | 唐绍祖（ALGO） |
| 日期 | 2026-11-09 |
| 对应交付 | `T01-缺口清单-交付版 (5).md`（2026-11-09） |
| 评审结论 | **核对结果认可，范围与数量都对；第 6 节补建语句需修正后再报 DBA** |
| 内部评审记录 | [会签/KG-COMPLY-LOAD-T01-REVIEW-ALGO.md](./会签/KG-COMPLY-LOAD-T01-REVIEW-ALGO.md) |

---

## 一、你的核对结果，我复核过，全部一致

我用只读会话连 `10.50.75.136:9669` / `demo_gkx_chain`，独立重跑了一遍，你和我的实测完全对得上：

| 复核项 | 实测 | 你的清单 |
|---|---|---|
| Tag 总数 / 缺 Tag | 10 个 / 缺 5 个（`research` `paper` `patent` `project` `person`） | 一致 |
| 缺 Edge | 11 种 | 一致 |
| `cooperate` / `participates` / `depends_on` | 94,824 / 213,500 / 1,073 | 一致 |
| `cite` / `supplies` | 0 / 0 条 | 一致 |

**两点你比我准，已按你的结果回修我方文档：**

1. **缺的是 11 种边，不是 10 种**——我派单里漏了 `publish`（M10，科研机构→政策）。你的清单是对的，`KG-COMPLY-SDD-L01` 已改成 11 种。
2. **`parent_sub` 缺失 ≠ 代码没实现**——「代码侧已实现写图」不等于「空间里已有结构」，这个区分写得好，请保留原话，避免被误读成我方虚报。

另外，`cite` / `supplies` 实测各 0 条、`supply` 与 `supplies` 名称与属性都不同不能等价替代、统计未覆盖技术点层因此不认定全图无漂移——**这几条判断都对，口径保持。**

**范围完整性已确认**：15 种边型覆盖 M01–M24 全部 24 条必须关系，无遗漏、无重复，《详细设计说明书》的「T01 预期缺口」表已补上这张对应表，T01 的范围可以据此结项。

---

## 二、第 6 节 16 条补建语句：先别报 DBA（P0）

### 问题

5 个 Tag + 11 种 Edge 现在是**空属性写法**（括号里没有任何字段）：

```sql
CREATE TAG  IF NOT EXISTS research ();     -- 没有 name / weight / props
CREATE EDGE IF NOT EXISTS belong ();       -- 没有 weight / props
```

建完之后，每批入图要写的批号 `props.batch` **物理上无处可落**。

### 为什么这不是「后续再定」的设计问题

《详细设计说明书》的「全清单共同前提」表已明确规定：每条边带 `weight` / `props`（JSON 含 `batch`），每批入图带 `props.batch` 用于对账。空属性结构没有 `props` 列，这条纪律**无法执行**，下游会连锁断掉：

| 任务 | 断点 |
|---|---|
| T02–T04 入图 | 写不进批号，批号纪律失效 |
| T07 对账单 | 无法按批次比对源表行数，验收没有凭据 |
| T05 / T06 | 无法区分批次，`apply_to` / `support` 双灌这类问题无法定位 |
| T08–T10 | 边没有 `weight`，加权与强度排序静默退化 |

**这是基准 `KG-7ELEM-SCHEMA-DDL-L01` 自身的缺项**，不是你的疏漏——你是照基准抄的，抄得没错。

### 旁证：前人已经踩过同一个坑

现网 `cooperate` 实测带 `props` + `weight`，`participates` 实测带 `props` + `chain_role` + `chain_score` + `participation_depth`，而基准对这两种边的定义也是空括号。说明实际写入时**必须**有 `props`，历史上是用「图内多列」绕过去的——就是你清单第 3 节记为「属性漂移」的那两处。

**所以：那不是脏数据，是正确的自救。** 你清单第 8 节第 2 问问得好。

---

## 三、请按这个版本改第 6 节（可直接替换）

属性名与我们已定的结构文档对齐；业务属性一律进 `props` JSON（不逐项升列），`first_year` 按已签收口径不新建。

```sql
USE demo_gkx_chain;

-- Tag（5 个：name 供展示，业务属性进 props）
CREATE TAG IF NOT EXISTS research (name string, props string);
CREATE TAG IF NOT EXISTS person   (name string, props string);
CREATE TAG IF NOT EXISTS paper    (name string, props string);
CREATE TAG IF NOT EXISTS patent   (name string, props string);
CREATE TAG IF NOT EXISTS project  (name string, props string);

-- Edge（11 种：weight 供加权，props 承载 batch / 来源 / 置信度）
CREATE EDGE IF NOT EXISTS belong          (weight double, props string);
CREATE EDGE IF NOT EXISTS participate     (weight double, props string);
CREATE EDGE IF NOT EXISTS author_of       (weight double, props string);
CREATE EDGE IF NOT EXISTS publish         (weight double, props string);
CREATE EDGE IF NOT EXISTS policy_relate   (weight double, props string);
CREATE EDGE IF NOT EXISTS policy_apply_to (weight double, props string);
CREATE EDGE IF NOT EXISTS research_coop   (weight double, props string);
CREATE EDGE IF NOT EXISTS talent_coop     (weight double, props string);
CREATE EDGE IF NOT EXISTS service_provide (weight double, props string);
CREATE EDGE IF NOT EXISTS supply          (weight double, props string);
CREATE EDGE IF NOT EXISTS parent_sub      (weight double, props string);
```

**两个特意没有做的事，请不要替我加上：**

1. **不加 `first_year`**——存量 24+6 边型实测全库都没有这个字段，徐滕强 2026-11-09 已签收「本期不强制新建，避免 DDL 膨胀拖期」，需要时另立一项走同一通道。
2. **不加任何 `ALTER EDGE`**——`cite` / `cooperate` / `depends_on` 本来就有 `weight` + `props`，`participates` 用 `chain_score` 作强度（已签收的 M17 例外），四个存量边都不必改结构。

> 上面 16 条 `CREATE` 仍属 DDL，走同一条通道：
> 唐绍祖确认内容 → 报徐滕强 → 项目组授权 DBA 执行。唐绍祖只做内容确认，不是 DDL 授权人。

---

## 四、还差两列，补齐后 T01 才算完整

SDD 的 T01 核对表规定四列：**Tag / Edge / VID / 端点方向**。你交了前两列（质量很好），还缺：

1. **VID 前缀抽查**：`ent:` / `seg:` / `inst:` / `person:` / `paper:` / `patent:` / `proj:` / `policy:` / `svc:` / `tp:` 各抽 20 条；
2. **边端点与方向抽样**：已存在的 15 种边各抽 20 条，核对起点/终点 Tag 对与方向。

> 你清单里把这项记为「属 T06」，属理解偏差：**抽样核对在 T01**，T06 做的是语义重合度比对。两件事不冲突，但别互相等。

其中两项顺带是 T06 的输入，请一并拆清：

- `depends_on` 1,073 条是否全部为 `segment → segment`（M15）；
- `participates` 213,500 条按端点拆分：`enterprise → segment`（M17 可用）与 `institution → institution`（服务公司关联，不属 M02/M19）各多少。

---

## 五、你清单第 8 节的四个问题，逐条答复

| # | 你的问题 | 答复 |
|---|---|---|
| 1 | 16 条补建语句是否认可 | **结构名与数量认可，属性定义不认可**。按本文第三部分「请按这个版本改」替换后再报。空属性版本不得提交 DBA |
| 2 | 第 3 节两处属性漂移保留还是处理 | **保留现状，不处理**。多出的列正是写入所需，删除有数据风险，`IF NOT EXISTS` 与之不冲突。**明令不要重建这两种边**（重建会丢列丢数据） |
| 3 | `supply` / `supplies` 怎么处理 | **采纳你的建议**：`supplies` 保留不动、按基准新建 `supply`。补两点：① `supplies` 实测 **0 条**，不存在迁移负担；② 两者同义并存有双写风险，请在最终清单写明「**M23 只写/只读 `supply`，`supplies` 停用**」，与 `apply_to` / `support` 同口径 |
| 4 | 空属性 Tag/Edge 的业务属性存哪、`props.batch` 怎么落 | **不是待定项，是 DDL 缺项**。按 `props` 字符串（JSON）承载，批号落 `props.batch`。`props` 列为空则批号无处落，复验必然不通过。处置见本文第三部分 |

---

## 六、下一步（按序）

1. 按本文第三部分产出**带属性的补建语句**（**16 条 `CREATE`**：5 Tag + 11 Edge，**不含任何 `ALTER`**），替换清单第 6 节；
2. 补齐本文第四部分说的两列（VID 前缀 + 端点方向抽样），与缺口清单同版提交；
3. 交唐绍祖确认内容 → 报徐滕强 → 项目组授权 DBA 执行；
4. DBA 执行后，重跑同一核对脚本（含 VID 与端点抽样）提交证据；
5. 复验通过后 T01 关闭，T02–T04 解阻；等待期 T05 / T08 / T09 / T10 / T14 可并行。

> **T01 不因「补建语句执行完毕」自动认定通过**，以复验证据为准——你原文这句写得对，保留。

---

## 七、我方文档已同步回修

| 文件 | 修改 |
|---|---|
| 《详细设计说明书》的全清单共同前提 | 新增「结构补建（DDL）属性底线」：空属性结构一律不可用 |
| `KG-COMPLY-SDD-L01` T01 预期缺口 | 边型 10 → **11**，补 `publish`（M10），补 15 边型 ↔ 24 M 关系对应表 |
| `KG-COMPLY-SDD-L01` T01 话术与验收 | 补「待补清单 DDL 须逐条核对属性，空属性结构不得提交 DBA」 |

> 基准 `KG-7ELEM-SCHEMA-DDL-L01` 的同类空括号写法也应修订，属已签收基线，
> 由本次评审提出、经内容确认后更新，不由 ALGO 单方改写。
