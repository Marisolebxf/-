# KG-COMPLY-SDD-L01 · 会签意见（ALGO 角色）

- **对象**：`KG-COMPLY-SDD-L01-详细设计说明书.md`（origin/dev `dafbc94e`，495 行 / 49,459 字节）+ `agent-handoffs/KG-COMPLY-SDD-L01.md`（2026-11-08 复审修订版）
- **会签角色**：ALGO（算法主责方）
- **会签人**：唐绍祖
- **日期**：2026-11-08
- **监管 / 签收**：`human:徐滕强`（2026-11-06 改派后备注，2026-11-08 明示签收归其名下；本单 DoD 末句已同步改）
- **结论**：**有条件同意**

---

## 0. 一句话结论

**设计骨架、23 条清单、14 条细任务、空间与验收面采用都正确，可以放行；但有 4 项 P0 必须改，否则燕大照单执行会「跑得出过程、得不到结果」——最要紧的是边属性读法写错了，会让中心性、路径、社群三条批次的权重全部静默降级。**

---

## 1. 结论分级

| 级别 | 项数 | 是否阻塞 ready_to_sign |
|---|---:|---|
| **P0 阻塞** | 4 | **是**，改完才能进 `ready_to_sign` |
| P1 建议 | 4 | 否，建议同期修 |
| P2 文字 | 3 | 否，顺手改 |

P0 不改的后果：T08 / T09 / T10 三条算法批次会**跑完、有输出、但权重全丢**，验收时看不出错，事后被质疑要重跑。

---

## 2. P0 项（必须改）

### P0-1 · 边属性读法写错，会让三条算法批次静默降级

#### 2.1.1 SDD 现在的写法

| 位置 | 原文 | 问题 |
|---|---|---|
| §2.1 #1 | 「`tech_point` 点 + `tech_rel` 边（**证据等级在 `props`**，做加权权重）」 | `tech_rel` **没有 `props` 字段**，也没有 `weight` 字段 |
| T08 编排话术 | 「跑 BFS 与 Dijkstra（**权重取 `props.confidence`**）」 | 同上，`props` / `confidence` 都不存在 |

#### 2.1.2 实测：`tech_rel` 的真实字段

```
DESCRIBE EDGE tech_rel
→ relation_type (string) / evidence_level (string)
  relation_confidence_score (double) / direction_status (string)
```

**没有 `weight`，没有 `props`。** 权重来源是 `relation_confidence_score`（实测有值，如 46.78 / 47.83）。

#### 2.1.3 更关键的坑：本引擎的边属性**不能用边名前缀读**

同一个属性，三种写法实测结果（`demo_gkx_chain`，2026-11-08）：

| 写法 | 实测返回 |
|---|---|
| `e.tech_rel.evidence_level` | **`NULL`**（541,428 条全 NULL） |
| `e.evidence_level` | `'LOW'` ✅ |
| `properties(e)` | `{'relation_type': "WEAK_DEPENDENCY", 'evidence_level': "LOW", ...}` ✅ |

**而节点侧约定相反**：`v.tech_point.name_zh` ✅ 有值，`v.name_zh` → `NULL`。

也就是说本图库（TRSGraph，Nebula 协议兼容但非原生 Nebula）：

- **节点**：必须带 Tag 前缀 `v.<tag>.<field>`
- **边**：必须**不带**边名前缀 `e.<field>`，或用 `properties(e)`

> 若照原 Nebula 习惯写 `e.tech_rel.evidence_level`，得到的是全 NULL，且**不报错**。算法会当成「没有证据等级」，权重退化为 1.0，加权路径退化成无权路径——结果照样输出，只是错了。

#### 2.1.4 要求改

1. §2.1 #1 与 T08 的「`props` / `props.confidence`」改为 **`e.evidence_level` / `e.relation_confidence_score`**（或 `properties(e)`）。
2. §5「全清单共同前提」增加一行**引擎读写约定**：

   > 节点属性用 `v.<tag>.<field>`；边属性用 `e.<field>` 或 `properties(e)`，**禁用 `e.<edge_name>.<field>`**（本引擎返回全 NULL 且不报错）。

3. T08 / T09 / T10 的验收判据各加一条：**权重分布自检**——`e.relation_confidence_score` 的空值率必须为 0，否则该批次判不通过。

#### 2.1.5 备注：SDD 里的百分比是对的

§2.2 #2 写「HIGH 15.1% / MEDIUM 16.7% / LOW 68.2%」，我用全量 541,428 条核对：**HIGH 81,623 / MEDIUM 90,377 / LOW 369,428，完全一致**。只是拿到这个数的写法要按上面改。

---

### P0-2 · T01 闸门开局必不过，T02–T04 实际一开始就是 blocked，排期没体现

#### 2.2.1 实测结构缺口

`SHOW TAGS` / `SHOW EDGES` 实测（2026-11-08）：**10 Tag / 15 Edge**。SDD 与 STRUCT 要求 **14 Tag / 30 Edge（24+6）**。

**缺 5 个 Tag**：

| 缺失 Tag | 用途 |
|---|---|
| `research` | 科研机构 |
| `person` | 人才 |
| `paper` | 论文 |
| `patent` | 专利 |
| `project` | 项目 |

**缺 10 条 M 边型**：

| 缺失边型 | 对应 |
|---|---|
| `participate` | M07 / M08 |
| `author_of` | M09 |
| `belong` | M04 |
| `policy_relate` | M11 |
| `policy_apply_to` | M12–M14 |
| `research_coop` | M19 |
| `talent_coop` | M20 |
| `service_provide` | M21 |
| `supply` | M23 |
| `parent_sub` | M24 |

#### 2.2.2 这不是设计错，是排期没写

T01 本来就设计成闸门（「待补清单非空 → T02–T04 blocked」），方向对。问题在于**关键路径没被标出来**：

```
T01（必出待补清单） → DDL 授权 → 补建 → 复验 → T02/T03/T04 才能开工
```

SDD 把 DDL 写成「清单交唐绍祖确认后由 DBA / 授权 DDL 通道补建」。**这一句不能落在我身上**：按本项目库禁改铁律（AGENTS.md §0），我不能对既有图空间执行任何 DDL。DDL 必须走项目组授权的 DBA 通道，我做的是「确认清单内容对不对」，不是「批准建」。

#### 2.2.3 要求改

1. T01 增加一句：**「本清单为预期非空项，实测 10 Tag / 15 Edge，预计缺 5 Tag + 10 M 边型」**，让燕大别有「核验应该全绿」的错误预期。
2. DDL 通道改写成：**「清单经唐绍祖确认内容 → 报 `human:徐滕强` → 项目组授权 DBA 执行 DDL」**，明确我不是 DDL 授权人。
3. §5 清单汇总处加一行**关键路径警示**：T02–T04 工期从 DDL 完成起算，不是从 T01 起算。

---

### P0-3 · T06 按现写法发现不了 `apply_to` / `support` 是同一批数据

#### 2.3.1 SDD 现在的写法

> T06：「对 `apply_to` / `support` / `participates` / `belongs_to` 四条现存边，**各抽 20 条**列端点 Tag 与方向……」

分别抽样看不出问题：两条边各自抽 20 条，端点分布当然都像「政策→链/环节」。

#### 2.3.2 实测：两条边 100% 重合

| 边 | policy→chain | policy→segment |
|---|---:|---:|
| `apply_to` | 1,678 | 9,279 |
| `support` | 1,678 | 9,279 |

连接比对（按「起点+终点」同对）：

```
MATCH (a:policy)-[e1:apply_to]->(b:segment) MATCH (a)-[e2:support]->(b) RETURN count(e1)
→ 9279
```

**9,279 = `apply_to`→segment 的全量，即 100% 重合，不是部分重叠。**

后果：任何按边名统计的算法会把政策覆盖数算成**双倍**。

#### 2.3.3 要求改

T06 编排话术增加一步**跨边重合度比对**：

> 对 `apply_to` 与 `support` 做「起点+终点」同对连接计数，与各自总量比对，给出重合率；重合率 >90% 判为「同批数据双灌」，结论写「建议停读一条」，不写「两条边分别映射」。

---

### P0-4 · `participates` 端点口径写错，把 M17 的有效数据一起否掉了

#### 2.4.1 SDD 现在的写法

| 位置 | 原文 |
|---|---|
| T06 读哪张图 | 「`participates`（**213,500，机构→机构**）」 |
| T02 不做什么 | 「不把现有 `apply_to` / `support` / `participates`（**机构→机构 213,500 条那条**）直接记成 **M12–M18** 已建」 |

#### 2.4.2 实测：213,500 是两种语义拼起来的

| 端点 | 数量 | 对应 |
|---|---:|---|
| `enterprise`→`segment` | **178,731** | **✅ 就是 M17** |
| `institution`→`institution` | **34,769** | ❌ 不属任何 M |

178,731 + 34,769 = 213,500。

也就是说：**213,500 里的 8 成正是 M17 的有效数据**，被「机构→机构 213,500」这一句整体否掉了。陈芸飞照这句话做，会把 M17 判成「不可用」，然后重复灌一遍 17.8 万条边。

另外 `institution` Tag 里装的是**科技创新服务公司**（实测 43,296 个，类型为科技创新服务 29,321 / 服务机构 9,650 / 金融服务 2,062 等），不是科研机构。所以那 34,769 条是**服务公司之间的关联**，不是 M02/M19 的科研机构合作。

#### 2.4.3 要求改

1. T06 读哪张图改为：**「`participates` 共 213,500 条，须按端点拆两层看：`enterprise`→`segment` 178,731（M17 候选，可用）、`institution`→`institution` 34,769（服务公司关联，不属 M02/M19）」**。
2. T02 不做什么的「M12–M18」改为逐条点名：**「不把 `apply_to` / `support` 记成 M12–M14；不把 `institution`→`institution` 的 `participates` 记成 M02 / M19」**（M15 是 `depends_on`，M17 是 `enterprise`→`segment`，与本节无关）。
3. 在 T06 验收判据加一条：**结论必须区分「可映射 / 需改名 / 不得映射」三类，且指明条数**。

---

## 3. P1 项（建议同期改）

### P1-1 · `community_id` 要写明是空字符串，不是 NULL

SDD §2.1 #12 与 T10 都写「全空」，方向对，但缺校验写法。

实测（双路径确认）：

| 写法 | 结果 |
|---|---|
| `v.tech_point.community_id` | `''`（空字符串） |
| `properties(v)` 里的 `community_id` | `""` |
| `WHERE ... IS NOT NULL` | **19,430（全量命中，误报）** |
| `WHERE ... <> ''` | **0** |

**建议**：§2.1 #12 补一句「字段值为空字符串非 NULL，校验须用 `<> ''`，`IS NOT NULL` 会误判为有值」。

### P1-2 · 社群两套口径，需登记一项待定

实测久新源表 `ads_technology_community_member` **19,430 行、1,731 个簇群**（每个技术点一行，已算好归属）。与我方自算 **113 个**差 15 倍。

SDD 直接采用 113（与 ACCEPT 一致，可接受），但没有登记「1,731 那套存在」。验收时容易被问「为什么不用现成的」。

**建议**：§2.2 #4 加一行待定说明：「久新源表已有 1,731 簇群口径，与自算 113 数量差 15 倍，两者不可混用；本期采用自算 113，若业务方改用源表口径须另行指定并重跑」。

### P1-3 · `first_year` 字段全库不存在

§5「全清单共同前提」要求每条边带 `first_year int`。实测 **15 条边没有任何一条有 `first_year` 字段**。

**建议**：并入 P0-2 的 DDL 清单，或本期降级为「有则填，无则不填」并注明需 DDL 才能有。

### P1-4 · `participates` 没有 `weight` 字段

§5 要求「每条边带 `weight double`」。实测 `participates` 字段是 `chain_role` / `participation_depth` / `chain_score` / `props`，**无 `weight`**。

M17 正好落在 `participates` 上，无法满足该通用条款。

**建议**：对 M17 单列例外，写明「M17 用 `chain_score` 作强度，不另加 `weight`」。

---

## 4. P2 项（文字性）

| # | 位置 | 问题 | 改法 |
|---|---|---|---|
| P2-1 | handoff「验收证据」段 | 写「未 commit / 未 push」，但 `dafbc94e`、`689def87` 已推 origin/dev | 改为已推送并附 commit 号 |
| P2-2 | handoff「偏离说明」2、registry note | 写「DoD 字段未改，待徐滕强明确」；2026-11-08 徐滕强已明示签收归其名下 | 已由本次会签同步改登记册 DoD 末句，handoff 需同步 |
| P2-3 | §2.2 #5 与 §2.1 #4 措辞 | 「94,824 条边」是有向数；结果 JSON 的 94,776 是去重无向数 | 加一句「有向 94,824 / 去重无向 94,776，差 48 对互为反向」，避免对账时误判缺口 |

---

## 5. 核对通过的部分（确认无误，不需改）

逐项实测复核，以下全部一致：

| 项 | SDD 写的 | 实测 | 结论 |
|---|---|---|---|
| 技术点规模 | 19,430 点 / 541,428 边 | 19,430 / 541,428 | ✅ |
| Louvain | 113 社群、模块度 0.5198 | JSON 一致 | ✅ |
| 路径 | 10 对、35,018 步 | JSON 一致 | ✅ |
| 证据等级比例 | 15.1 / 16.7 / 68.2 | 81,623 / 90,377 / 369,428 | ✅ 精确一致 |
| 度中心性相关 | 与现算度相关 0.9515 | JSON `pearson 0.9515` | ✅ |
| 紧密/中介采样 | 度数前 1,500 子图、k=300 | JSON scope 一致 | ✅ |
| M22 碎片 | 最大连通片 220/208,394 | JSON 一致 | ✅ |
| M15 依赖网 | 1,073 边、32 层、341 片 | JSON 一致 | ✅ |
| policy / institution 点数 | 20,000 / 43,296 | 实测一致 | ✅ |
| 算法清单条数 | 23 = 17 + 6 | 逐条点算一致 | ✅ |
| 细任务条数 | 14 条 | T01–T14 齐全 | ✅ |
| 执行人分布 | 白2/陈3/宋2/韩2/兰2/李2 + 待定1 | 点算一致 | ✅ |
| 空间采用 | `demo_gkx_chain` 放法 B | 与 STRUCT §4 一致 | ✅ |
| M22 语义 | 必为 501「形态不支持」非空态 | 判定准确 | ✅ |
| T05 空 Tag 口径 | 区分「Tag 有历史数据」与「本期无供数」 | 已采纳修正 | ✅ |
| 路径步差异 | 35,018 vs 47,909 已登记待确认 | 与实测一致 | ✅ |
| 34–40 不做 / 42–47 不验 | — | 与 ACCEPT 一致 | ✅ |

**特别肯定两处**：

1. **M22 的 501 语义区分准确**——「有数据但形态不可用」不等于「暂无数据」，这个区分很多人会写混，SDD 写对了。
2. **T05 已采纳「policy / institution 不是空 Tag」的修正**——说明上一轮反馈被吸收，没有照抄旧结论。

---

## 6. 会签意见（正式表述）

> 同意本单进入 `ready_to_sign`，**前提是 P0-1 至 P0-4 四项改完并回推**。
>
> 理由：设计骨架、清单口径、空间与验收面采用均正确，无需重开 STRUCT / ACCEPT；P0 四项属「照单执行会出错」的执行层错误，不改则燕大六人开工后返工，且返工点在算法侧（我的主责），成本高于现在改文档。
>
> P1 / P2 不阻塞，建议同期修，避免下一轮再来一遍。

### 与 T06 裁定的关系

本次会签与 [`KG-COMPLY-T06-现存边语义裁定.md`](../KG-COMPLY-T06-现存边语义裁定.md) 配套：

- T06 裁定文件给**结论**（哪条边可用、判冗余、需改名）；
- 本会签给**过程要求**（T06 任务该怎么做才能得出这些结论）。

陈芸飞出报告时以 T06 裁定文件为对照基准，不必从零判断。

---

## 7. 复核方法（任何人可重跑）

连 `10.50.75.136:9669`，`USE demo_gkx_chain`，全部只读：

```sql
-- ① 结构缺口
SHOW TAGS;  SHOW EDGES;
DESCRIBE EDGE tech_rel;          -- 无 weight / props，有 evidence_level / relation_confidence_score

-- ② 边属性两种写法差异（本引擎关键陷阱）
MATCH (a)-[e:tech_rel]->(b) RETURN e.tech_rel.evidence_level LIMIT 3;   -- 全 NULL
MATCH (a)-[e:tech_rel]->(b) RETURN e.evidence_level LIMIT 3;            -- 'LOW'
MATCH (a)-[e:tech_rel]->(b) RETURN properties(e) LIMIT 3;               -- 完整

-- ③ 节点侧相反
MATCH (v:tech_point) RETURN v.tech_point.name_zh LIMIT 3;               -- 有值
MATCH (v:tech_point) RETURN v.name_zh LIMIT 3;                          -- 全 NULL

-- ④ community_id 空串非 NULL
MATCH (v:tech_point) WHERE v.tech_point.community_id IS NOT NULL RETURN count(v);  -- 19430（误报）
MATCH (v:tech_point) WHERE v.tech_point.community_id <> '' RETURN count(v);        -- 0

-- ⑤ apply_to / support 重合
MATCH (a:policy)-[e1:apply_to]->(b:segment) MATCH (a)-[e2:support]->(b) RETURN count(e1);  -- 9279

-- ⑥ participates 拆两层
MATCH (a)-[e:participates]->(b) RETURN tags(a)[0], tags(b)[0], count(e);
-- enterprise→segment 178731 / institution→institution 34769
```

---

## 8. 附：本次会签改动的其他文件

| 文件 | 改动 |
|---|---|
| `agent-delivery/task-registry.yaml` | DoD 末句「经唐绍祖确认」改为「经徐滕强确认（2026-11-08 明示）」；note 追加本会签结论与 P0 摘要 |
| `KG-COMPLY-ACCEPT-L01-验收面.md` | 社群口径改为「空字符串非 NULL、校验用 `<> ''`」；补 T06 交叉引用 |
| `KG-COMPLY-STRUCT-L01-结构与空间选定.md` | `policy` / `institution` 由「空 Tag 等供数」改为实测点数与类型说明 |
| `README.md` | 补 T06 裁定与本会签索引 |
