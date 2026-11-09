# KG-COMPLY-LOAD-T01 · 交付评审意见（ALGO / 唐绍祖）

| 项 | 内容 |
|---|---|
| 评审对象 | `T01-缺口清单-交付版 (5).md`（燕大 · 白鑫凤，2026-11-09） |
| 评审依据 | `KG-COMPLY-SDD-L01` §5 T01 闸门 / `KG-7ELEM-SCHEMA-DDL-L01` / `KG-7ELEM-BUILD-REQ-L01` M01–M24 / STRUCT §1 |
| 评审人 | 唐绍祖（ALGO） |
| 日期 | 2026-11-09 |
| 评审结论 | **内容方向认可，结构补建清单不予放行（1 项 P0 + 1 项 P1 补齐后可复验）** |
| 复核方式 | 只读会话连 `10.50.75.136:9669` / `demo_gkx_chain`，独立重跑 `SHOW TAGS` / `SHOW EDGES` / `MATCH count`，未做任何写操作 |

---

## 一、一句话结论

24 条必须关系的范围没有错，白鑫凤的缺口清单**名称与数量都对得上**；
但清单第 6 节的 16 条建表语句里，5 个 Tag 和 11 种 Edge 是**空属性写法**（括号里没有字段），
建完之后每批入图要写的批号 `props.batch` **无处可落**——这不是「后续再定」的设计问题，
是基准 DDL 自身的缺项，必须先补属性再报 DBA。

---

## 二、独立复核结果（与交付一致）

只读复核于 2026-11-09 执行，结果与白鑫凤清单逐项一致：

| 复核项 | ALGO 实测 | 交付清单 | 判定 |
|---|---|---|---|
| Tag 总数 | 10（`chain` / `enterprise` / `institution` / `policy` / `segment` / `tech_institution` / `tech_paper` / `tech_patent` / `tech_person` / `tech_point`） | — | ✅ |
| 缺 Tag | `research` / `paper` / `patent` / `project` / `person`（5 个） | 5 个，同名 | ✅ |
| 缺 Edge | `belong` / `participate` / `author_of` / `publish` / `policy_relate` / `policy_apply_to` / `research_coop` / `talent_coop` / `service_provide` / `supply` / `parent_sub`（11 种） | 11 种，同名 | ✅ |
| `cite` 边数 | 0 | 0 | ✅ |
| `supplies` 边数 | 0 | 0 | ✅ |
| `cooperate` 边数 | 94,824 | 94,824 | ✅ |
| `participates` 边数 | 213,500 | 213,500 | ✅ |
| `depends_on` 边数 | 1,073 | 1,073 | ✅ |

**白鑫凤纠对了 ALGO 的一处错误**：本评审方 `KG-COMPLY-SDD-L01` 首版「T01 预期缺口」写「10 种边型」，
漏了 `publish`（M10，科研机构→政策）。实测确为 11 种，交付清单正确，已回修 SDD（见 §六）。

**15 种边型覆盖 24 条 M 关系**（一种边型对应多条关系，故 15 ≠ 24）：

| Edge | 对应 M 编号 | Edge | 对应 M 编号 |
|---|---|---|---|
| `cooperate` | M01 / M02 / M03 / M22 | `policy_apply_to` | M12 / M13 / M14 |
| `belong` | M04 / M05 | `depends_on` | M15 |
| `cite` | M06 / M16 | `participates` | M17 / M18 |
| `participate` | M07 / M08 | `research_coop` | M19 |
| `author_of` | M09 | `talent_coop` | M20 |
| `publish` | M10 | `service_provide` | M21 |
| `policy_relate` | M11 | `supply` | M23 |
| | | `parent_sub` | M24 |

合计 4+2+2+2+1+1+1+3+1+2+1+1+1+1+1 = **24**，无遗漏、无重复。**清单范围完整，可以此为结项依据。**

---

## 三、P0：空属性结构不得提交 DBA

### 3.1 事实

`KG-7ELEM-SCHEMA-DDL-L01` 现状（原文行号）：

```sql
-- 第 10–18 行：5 个 Tag 全部空属性
CREATE TAG IF NOT EXISTS research ();
CREATE TAG IF NOT EXISTS paper ();
CREATE TAG IF NOT EXISTS patent ();
CREATE TAG IF NOT EXISTS project ();
CREATE TAG IF NOT EXISTS person ();

-- 第 31–34、37–49、52、54–58 行：11 种 Edge 全部空属性
CREATE EDGE IF NOT EXISTS belong ();
CREATE EDGE IF NOT EXISTS participate ();
CREATE EDGE IF NOT EXISTS author_of ();
CREATE EDGE IF NOT EXISTS publish ();
CREATE EDGE IF NOT EXISTS policy_relate ();
CREATE EDGE IF NOT EXISTS policy_apply_to ();
CREATE EDGE IF NOT EXISTS research_coop ();
CREATE EDGE IF NOT EXISTS talent_coop ();
CREATE EDGE IF NOT EXISTS service_provide ();
```

### 3.2 与 SDD 直接冲突

`KG-COMPLY-SDD-L01` §5 共同前提已写明：

- **边属性**：每条边带 `weight double` / `props`（JSON 含 `source_table` `source_record_id` `batch` `confidence` `match_method` `evidence`）；`first_year` 按徐滕强 2026-11-09 签收口径**本期不强制新建**；
- **批号**：每批入图带 `props.batch`，端点缺失跳过并计数，用于对账。

空属性结构没有 `props` 列，上述两条**在物理上无法执行**。按现清单建完，后果是：

| 下游任务 | 断点 |
|---|---|
| T02 / T03 / T04 入图 | 写不进 `props.batch`，批号纪律失效 |
| T07 对账单 | 无法按批次比对源表行数，验收无凭据 |
| T05 / T06 语义对齐 | 无法区分批次，「`apply_to` / `support` 双灌」这类问题无法定位 |
| T08 / T09 / T10 | 边无 `weight`，加权与强度排序静默退化 |

### 3.3 旁证：前人已踩过同一个坑

现网 `cooperate` 实测带 `props` + `weight`，`participates` 实测带 `props` + `chain_role` + `chain_score` + `participation_depth`；
而 `KG-7ELEM-SCHEMA-DDL-L01` 对这两种边的定义是空括号。说明实际写入时**必须**有 `props`，
历史上是用「图内多列」的方式绕过去的——即白鑫凤清单 §3 记为「属性漂移」的那两处。
**结论：漂移是正确方向的自救，不是脏数据。**

### 3.4 处置：属性定义按下列版本补齐后再报 DBA

将白鑫凤清单 §6 的 16 条语句替换为下面 **16 条**（Tag 5 + Edge 11），属性名与 STRUCT §1 对齐；
`first_year` 按 §5 共同前提 ⑲ 口径不新建，**不附带任何 `ALTER EDGE`**：

```sql
USE demo_gkx_chain;

-- Tag（5 个：name 供展示，业务属性一律进 props JSON，不逐项升列）
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

**为什么不加 `first_year`、也不补 `ALTER`**：徐滕强 2026-11-09 已签收口径——存量 24+6 边型实测全库无此字段，
本期不强制新建（避免 DDL 膨胀拖期），需要时走同一授权通道单独立项。
同理，`cite` / `cooperate` / `depends_on` 已有 `weight` + `props`，`participates` 用 `chain_score` 作强度，
**四个存量边都不需要改结构**——原清单若报 `ALTER`，请删掉。

> `ALTER`/`CREATE` 同属 DDL，与 `CREATE` 走同一条通道：
> 唐绍祖确认内容 → 报 `human:徐滕强` → 项目组授权 DBA 执行。
> 唐绍祖只做内容确认，不是 DDL 授权人；编排侧不得自行执行任何 DDL。

---

## 四、P1：T01 验收还差两列

`KG-COMPLY-SDD-L01` T01 的核对表规定四列：**Tag / Edge / VID / 端点方向**。
本次交付覆盖了前两列（且属性逐列比对质量高），后两列未做：

1. **VID 前缀抽查**：`ent:` / `seg:` / `inst:` / `person:` / `paper:` / `patent:` / `proj:` / `policy:` / `svc:` / `tp:` 各抽 20 条；
2. **边端点与方向抽样**：已存在的 15 种边各抽 20 条，核对起点/终点 Tag 对与方向是否合 STRUCT §1.2。
   交付清单把该项记为「属 T06」，属理解偏差——**抽样核对在 T01**，T06 做的是语义重合度比对。

特别需要拆清的两项（同时是 T06 的输入）：

- `depends_on` 1,073 条是否全部为 `segment → segment`（M15）；
- `participates` 213,500 条按端点拆分：`enterprise → segment`（M17 可用）与 `institution → institution`（服务公司关联，不属 M02/M19）各多少。

---

## 五、对交付清单 §8 四个问题的答复

| # | 问题 | 答复 |
|---|---|---|
| 1 | §6 的 16 条补建语句是否认可 | **结构名与数量认可；属性定义不认可**。按 §三 3.4 补齐属性后再报。空属性版本不得提交 DBA |
| 2 | §3 两处属性漂移保留还是处理 | **保留现状，不处理**。多出的列正是写入所需；删除有数据风险；`CREATE ... IF NOT EXISTS` 与之不冲突。**明令不要重建这两种边**（重建会丢列、丢数据） |
| 3 | `supply` / `supplies` 如何处理 | **采纳交付建议**：`supplies` 保留不动，按基准新建 `supply`。补充两点：① `supplies` 实测 **0 条边**，不存在迁移负担；② 两者同义并存有双写风险，须在最终清单写明「**M23 只写 / 只读 `supply`，`supplies` 停用**」，与 `apply_to` / `support` 的处理口径一致 |
| 4 | 空属性 Tag/Edge 的业务属性存哪、`props.batch` 怎么落 | **不是待定项，是 DDL 缺项**。按 `props` 字符串（JSON）承载，批号落 `props.batch`；`props` 列为空则批号无处落，复验必然失败。处置见 §三 3.4 |

### 另外两点提醒（交付清单已写对，请保留原话）

1. `parent_sub` 缺失 ≠ 代码未实现：**代码侧「已实现写图」不等于目标空间「已有结构或数据」**，这个区分要保留，避免被误读为我方虚报。
2. 「统计未覆盖技术点层、未做全量历史对照，不据此认定全图无漂移」——口径正确，保留。

---

## 六、ALGO 侧文档回修（已直接改进正文）

| # | 文件 | 修改 |
|---|---|---|
| 1 | `KG-COMPLY-SDD-L01` T01「预期缺口」 | 边型 10 → **11**，补 `publish`（M10），并补 15 边型 ↔ 24 M 关系完整对应表 |
| 2 | `KG-COMPLY-SDD-L01` §5 共同前提 | 新增「**结构补建（DDL）属性底线**」行：空属性结构一律不可用；Edge 至少 `weight` / `props`、Tag 至少 `name` / `props`；`first_year` 按 ⑲ 口径不强制 |
| 3 | `KG-COMPLY-SDD-L01` T01 话术与验收 | 补「待补清单 DDL 须逐条核对属性定义，空属性结构不得提交 DBA」 |
| 4 | `KG-COMPLY-SDD-L01` 修订记录 | 新增 2026-11-09 条（⑰⑱），指向本文 |

> 基准文件 `KG-7ELEM-SCHEMA-DDL-L01` 本身也应同步修订属性定义。该文件属已签收基线，
> 由本评审提出、经内容确认后更新，不由 ALGO 单方改写。

---

## 七、后续动作与顺序

1. 白鑫凤按 §三 3.4 产出**带属性的补建语句**（16 条 `CREATE`：5 Tag + 11 Edge，**不含 `ALTER`**）；
2. 补 T01 缺的两列（VID 前缀 + 端点方向抽样），与缺口清单同版提交；
3. 唐绍祖确认内容 → 报 `human:徐滕强` → 项目组授权 DBA 执行；
4. DBA 执行后，白鑫凤重跑同一核对脚本（含 VID 与端点抽样）提交证据；
5. 复验通过后 T01 关闭，T02–T04 解阻；T05 / T08 / T09 / T10 / T14 等待期可并行。

**T01 不因「补建语句执行完毕」自动认定通过**，以复验证据为准。
