# T07 入图验收总表 · 对账口径（KG-COMPLY-T07-LEDGER）

- 作者：唐绍祖
- 日期：2026-11-12
- 适用：`KG-COMPLY-LOAD-T07`（建议执行人 李周）、以及所有需要引用「入图了多少条」的场合
- 数据时点：**2026-11-12 15:00–15:30 全部由我本人在 `demo_gkx_chain` 现场只读实测**，不引用任何交付自述
- 前置：[T02 对账护栏](./KG-COMPLY-LOAD-T02-对账护栏-cooperate三端点分组.md)、[T03 裁定](./KG-COMPLY-LOAD-T03-裁定-人才与机构四条关系.md)、T05 空态实测、各任务验收记录

---

## 一、一句话说清这份文件干什么

**24 条必须关系，现在每条到底在图里有多少条、是谁灌的、哪些是本来就该是 0。** 表里的数字可以直接抄进总账，但对账时必须按本文第三节的分组规则分组，否则数出来的总数对应不上任何一条关系。

---

## 二、24 行总表（2026-11-12 实测）

「本期状态」三档，含义：
- **新建** = 本期由 T02/T03/T04 灌入；
- **存量已满足** = 图里本来就有，本期只核对不重灌；
- **空态** = 本期本该 0（无源 / 与别的编号同源重复 / 端点类型不符），**不是漏做**。

| M | 边型 | 端点方向 | 本期状态 | 实测条数 | 写入方 | 批号 |
|---|---|---|---|---:|---|---|
| M01 | `cooperate` | `person`→`person` | 新建 | **2,525,789** | T03 宋飞扬 | `comply-2026-11-11-t03` |
| M02 | `cooperate` | `research`→`research` | 新建 | **3,442,271** | T02 陈芸飞 | `comply-20261111-t02` |
| M03 | `cooperate` | `person`→`research` | 空态（端点 100% 企业） | **0** | — | — |
| M04 | `belong` | `person`→`research` | 新建 | **72,099** | T03 宋飞扬 | `comply-2026-11-11-t03` |
| M05 | `belong` | `research`→`research` | 空态 | **0** | — | — |
| M06 | `cite` | `paper`→`paper` | 空态（无源） | **0** | — | — |
| M07 | `participate` | `person`→`project` | 空态（无源） | **0** | — | — |
| M08 | `participate` | `research`→`project` | 新建 | **17,426** | T04 韩梦蕊 | `comply-20261112-t04-4` |
| M09 | `author_of` | `person`→`patent` | 新建 | **85,069** | T04 韩梦蕊 | `comply-20261112-t04-2` |
| M10 | `publish` | 见 L03 | 空态 | **0** | — | — |
| M11 | `policy_relate` | 见 L03 | 空态 | **0** | — | — |
| M12 | `policy_apply_to` | 见 L03 | 空态 | **0** | — | — |
| M13 | `policy_apply_to` | 见 L03 | 空态 | **0** | — | — |
| M14 | `policy_apply_to` | 见 L03 | 空态 | **0** | — | — |
| M15 | `depends_on` | `segment`→`segment` | 存量已满足 | **1,073** | 历史 | 无 |
| M16 | `cite` | 见 L03 | 空态 | **0** | — | — |
| M17 | `participates` | `enterprise`→`segment` | 存量已满足 | **178,731** | 历史 | 无 |
| M18 | `participates` | `institution`→`segment` | 空态 | **0** | — | — |
| M19 | `research_coop` | `research`→`research` | 空态（与 M02 同源重复） | **0** | — | — |
| M20 | `talent_coop` | `person`→`person` | 空态（与 M01 同源重复） | **0** | — | — |
| M21 | `service_provide` | 见 L03 | 空态 | **0** | — | — |
| M22 | `cooperate` | `enterprise`→`enterprise` | **有数据形态不可用（501）** | **94,824** | 历史 | 无 |
| M23 | `supply` | 见 L03 | 空态 | **0** | — | — |
| M24 | `parent_sub` | 见 L03 | 空态 | **0** | — | — |

**已能供数（8 条有真实行数）**：M01、M02、M04、M08、M09、M15、M17，外加 M22（有数据但形态不可用，必须单标 501）。
**空态（16 条）**：M03、M05、M06、M07、M10–M14、M16、M18–M21、M23、M24。

> M03 的特殊性：它**不是「无源」**，源表有 202,795 行——但 8,784 个机构 100% 是 `company`，是人才-企业合作，端点类型对不上 M03 的定义。写总表时必须写「有源但端点不符」，不能写「无源」，否则会被误读成数据缺失。

---

## 三、对账必须先分组（否则总数对不上任何一条）

### 3.1 `cooperate` 一个边型装了四条 M 关系

| 端点组合 | 对应 | 条数 |
|---|---|---:|
| `person`→`person` | M01 | 2,525,789 |
| `research`→`research` | M02 | 3,442,271 |
| `enterprise`→`enterprise` | M22 | 94,824 |
| `person`→`research` | M03 | 0 |
| | **合计** | **6,062,884** |

**禁止**写「`cooperate` 共 6,062,884 条」充当任何一条关系的成果。对账必须四行分组。

### 3.2 `participates` 里混着一条**不属于任何 M 关系**的存量

| 端点组合 | 归属 | 条数 |
|---|---|---:|
| `enterprise`→`segment` | M17 | 178,731 |
| `institution`→`segment` | M18 | 0 |
| `institution`→`institution` | **不属 M17/M18**（T06 的处理对象） | 34,769 |
| | **合计** | **213,500** |

这 34,769 条是历史混装数据，语义与 M17/M18 都不符。**总表里不能把它塞进 M17 或 M18**，必须单列在「未映射存量」区（见第五节）。这也是 T02 任务卡明确禁止「把 `institution`→`institution` 的 `participates` 记成 M02/M19」的原因。

### 3.3 `participate` 和 `participates` 是两个不同的边型

只差一个 `s`，含义完全不同：

| 边型 | 对应 | 条数 | 业务含义 |
|---|---|---:|---|
| `participate`（单数） | M07/M08 | 0 / 17,426 | **科研机构参与项目** |
| `participates`（复数） | M17/M18 | 178,731 / 0 | **企业归属产业链环节** |

用错一个字母，会把「机构参与项目」和「企业归属环节」混成一笔账。写 SQL/nGQL 时请放大核对。

### 3.4 `cite` 同时是 M06 和 M16

`cite` 一个边型覆盖两条 M 关系：**M06 技术→技术（论文→论文）**、**M16 政策→政策**。以
`KG-7ELEM-BUILD-REQ-L03` 的 M 表为准（M16 行写明 `policy→policy`、「新建，不并进 M06」）。当前两者均为 0
（T05 实测 `cite` 全库 0 条）。若将来只建了其中一条，**必须按端点 Tag 拆分**，不能整体写一个数。

> 勘误（2026-11-12 唐绍祖）：本节原写「M16 论文→专利」，与 L03 不符，已按 L03 改正。李周 T07 送审稿
> 「M16 政策引用政策」的写法是对的。

---

## 四、查询模板（可原样复跑，已避开全表扫描）

### 4.1 铁律：按 Tag 锚定 + 用 `CONTAINS` 筛批号

图库 `10.50.75.136:9669` 已触发内存高水位（`Used memory hits the high watermark(0.800000)`），**不带 Tag 锚定的全表扫描会被拒**（实测 `MATCH ()-[e:cooperate]->()` 73 秒被拒、`sum(e.weight)` 518 秒被拒）。

### 4.2 24 行总表的取数语句

```
-- M01
MATCH (a:person)-[e:cooperate]->(b:person) RETURN count(e);
-- M02
MATCH (a:research)-[e:cooperate]->(b:research) RETURN count(e);
-- M03
MATCH (a:person)-[e:cooperate]->(b:research) RETURN count(e);
-- M22
MATCH (a:enterprise)-[e:cooperate]->(b:enterprise) RETURN count(e);
-- M04
MATCH (a:person)-[e:belong]->(b:research) RETURN count(e);
-- M05
MATCH (a:research)-[e:belong]->(b:research) RETURN count(e);
-- M08
MATCH (a:research)-[e:participate]->(b:project) RETURN count(e);
-- M09
MATCH (a:person)-[e:author_of]->(b:patent) RETURN count(e);
-- M15
MATCH (a:segment)-[e:depends_on]->(b:segment) RETURN count(e);
-- M17
MATCH (a:enterprise)-[e:participates]->(b:segment) RETURN count(e);
-- M18
MATCH (a:institution)-[e:participates]->(b:segment) RETURN count(e);
-- M03 之外的 16 条空态：直接数边型
MATCH ()-[e:publish]->() RETURN count(e);
MATCH ()-[e:policy_relate]->() RETURN count(e);
MATCH ()-[e:policy_apply_to]->() RETURN count(e);
MATCH ()-[e:cite]->() RETURN count(e);
MATCH ()-[e:research_coop]->() RETURN count(e);
MATCH ()-[e:talent_coop]->() RETURN count(e);
MATCH ()-[e:service_provide]->() RETURN count(e);
MATCH ()-[e:supply]->() RETURN count(e);
MATCH ()-[e:parent_sub]->() RETURN count(e);
```

### 4.3 批号覆盖率的写法

```
-- 正确（T02 的 props 里 batch 不在 JSON 首位）
MATCH (a:research)-[e:cooperate]->(b:research)
WHERE e.props CONTAINS "comply-20261111-t02"
RETURN count(e);

-- 错误（会返回 0，因为 T03 的 props 才是 batch 打头）
MATCH (a:research)-[e:cooperate]->(b:research)
WHERE e.props STARTS WITH "{\"batch\":\"comply-20261111-t02\","
RETURN count(e);
```

**原因**：T03 的 `props` 是 `{"batch":...}`（batch 在首位），T02 的是 `{"first_year":...,"match_method":"coauthor","batch":"comply-20261111-t02",...}`（batch 在中间）。**不要假设键序**，一律用 `CONTAINS`。

---

## 五、全空间边数口径核对（证明总表没有遗漏）

因为全表扫描被内存水位拒，只能**逐边型累加**。26 种边型全部实测：

### 5.1 M 关系覆盖的边

| 边型 | 条数 |
|---|---:|
| `cooperate`（M01+M02+M03+M22） | 6,062,884 |
| `participates`（M17+M18+未映射 34,769） | 213,500 |
| `author_of`（M09） | 85,069 |
| `belong`（M04+M05） | 72,099 |
| `participate`（M07+M08） | 17,426 |
| `depends_on`（M15） | 1,073 |
| `cite` / `publish` / `policy_relate` / `policy_apply_to` / `research_coop` / `talent_coop` / `service_provide` / `supply` / `parent_sub` | 0 |
| **小计** | **6,452,051** |

### 5.2 不属 M01–M24 的历史存量

| 边型 | 条数 | 说明 |
|---|---:|---|
| `apply_to` | 10,957 | 与 `support` 端点对 100% 重合，T06 待裁「停读一条」 |
| `support` | 10,957 | 同上（抽样 30 对双向各 30/30 可对应） |
| `belongs_to` | 359 | T06 对象 |
| `regulate` | 0 | — |
| `supplies` | 0 | — |
| **小计** | **22,273** | |

### 5.3 tech 层（T08/T09 用的技术点层，与 M01–M24 无关）

| 边型 | 条数 |
|---|---:|
| `tech_rel` | 541,428 |
| `tech_has_patent` | 172,644 |
| `tech_has_person` | 111,578 |
| `tech_has_paper` | 108,337 |
| `tech_has_institution` | 51,000 |
| `tech_path_step` | 35,018 |
| **小计** | **1,020,005** |

### 5.4 加总

```
6,452,051（M 关系）
+   22,273（未映射历史存量）
+1,020,005（tech 层）
= 7,494,329（全空间边总数）
```

**用途**：如果哪天有人质疑「总表只写了 xxx 条，库里明明更多」，用这张分解表可以逐笔对上——差额全部有归属，没有「下落不明的边」。

---

## 六、禁止写法（逐条都有实测理由）

| 禁止 | 后果 |
|---|---|
| `MATCH ()-[e:cooperate]->() RETURN count(e)` 当某条 M 的成果 | 得 6,062,884，M01/M02/M22 三笔混成一笔 |
| 用 `cooperate` 全量当 M02 分母 | 3,442,271 / 6,062,884 = 56.8%，无意义 |
| 把 `institution`→`institution` 的 34,769 条记进 M17 或 M18 | M17 会虚增 19.5% |
| 把 `participate` 与 `participates` 当同一条 | M08 与 M17 混账 |
| 用 `props STARTS WITH "{\"batch\":..."` 测覆盖率 | T02 的会返回 0，误判「没打批号」 |
| 用全表扫算总和 | 内存水位拒服务，脚本直接挂 |
| 把 M03 写成「无源」 | 实际有 202,795 行源，只是端点类型不符 |
| 把 M22 的 94,824 条记成「可用」 | 形态不可用，必须标 501 |
| 把空态行标成「可用」或填非 0 | 违反 T07 DoD 明令 |

---

## 七、已知数据质量问题（写总表时要加脚注）

| 问题 | 影响 | 状态 |
|---|---|---|
| `tech_point.weighted_degree` 与当前边不自洽 | 428 度榜整榜、432 综合榜 25% 分项 | 已记录（[T02/T09 验收 §四](./KG-COMPLY-ACCEPT-T02-T09-技术验收记录.md)），待 tech 层归属方定口径重算 |
| M08 / M09 的 `weight` 全为 1.0 | 无强弱信息，前端不能按 weight 渲染粗细 | 已记录（[T04 验收 §四](./KG-COMPLY-ACCEPT-T04-技术验收记录.md)），属设计选择 |
| M02 的 `weight` 总和 14,715,117 未独立复核 | 无法证明 weight 累加无误 | 全量 `sum(e.weight)` 被内存水位拒，待环境恢复补验 |
| `apply_to` 与 `support` 完全重复 | 读两张表会双计 | T06 处理中（已备开局事实：各 10,957、端点对重合） |

---

## 八、验收判据（T07 怎么算通过）

总表提交时逐条检查：

1. **24 行齐全**，编号 M01–M24 不缺号、不重号；
2. **有真实行数的 8 行**，数字与本文第二节一致（允许因后续新灌而变，但必须附新批号与验收记录）；
3. **16 个空态行必须写 0**，并各附一句理由（无源 / 同源重复 / 端点类型不符）；
4. **M22 单标「有数据形态不可用（501）」**，不得与可用行混排；
5. **`cooperate` 四行分组**、`participates` 三层分组，不得出现边型总量当关系量；
6. **每行标批号**（存量写「无」），新灌行必须能在图里用 `CONTAINS` 复现；
7. **附本文第五节的边数分解表**，证明总表之外没有下落不明的边。

---

## 九、建议的对账表模板（交 T07 直接填）

| M | 关系描述 | 边型 | 端点 | 本期状态 | 应灌 | 实灌 | 跳过 | 批号 | 复现语句 |
|---|---|---|---|---|---:|---:|---:|---|---|
| M01 | 人才-人才合作 | `cooperate` | person→person | 新建 | 2,525,789 | 2,525,789 | 0 | `comply-2026-11-11-t03` | 见 §4.2 |
| … | | | | | | | | | |

「跳过」列来自各任务 handoff 的跳过计数（我本次只核了终态条数，没有逐任务核对跳过明细，该列需执行方补）。
