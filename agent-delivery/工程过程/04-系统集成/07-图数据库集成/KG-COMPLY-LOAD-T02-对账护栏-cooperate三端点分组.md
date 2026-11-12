# T02 对账护栏：`cooperate` 边型三端点分组

- 作者：唐绍祖
- 日期：2026-11-12
- 适用：`KG-COMPLY-LOAD-T02` 签收、`KG-COMPLY-LOAD-T07` 总账对账
- 触发原因：`cooperate` 这一种边型，现已同时承载**三种端点组合**的数据，来自三个不同任务、三个不同批次。任何「`cooperate` 一共有多少条」的问法，答案都会把三笔账混成一笔。

---

## 一、为什么必须分组

`cooperate` 在 `demo_gkx_chain` 里只有一个边型名，但库里现在躺着三组语义完全不同的关系：

| 端点组合 | 业务含义 | 对应关系编号 | 写入方 | 批次戳 |
|---|---|---|---|---|
| `enterprise` → `enterprise` | 企业之间的产业链合作 | **M22**（存量） | 历史脚本 | 无（历史数据） |
| `person` → `person` | 人才之间的合著合作 | **M01** | T03（宋飞扬） | `comply-2026-11-11-t03` |
| `research` → `research` | 科研机构之间的合作 | **M02** | T02（陈芸飞） | `comply-20261111-t02` |

**风险**：若 T07 只写「`cooperate` 总计 6,062,884 条」而不分组，读者无法判断 M01、M02、M22 三条关系的分母是否各自达标；若某一条关系的实灌数算多了或算少了，总数上看不出来（三组互相抵消）。更糟的是，如果对账 SQL 用「`cooperate` 全量」当 M02 的分母，会得出 3,442,271 ÷ 6,062,884 = 56.8% 这种毫无意义的结果。

---

## 二、2026-11-12 现场实测

我在 `10.50.75.136:9669` 的 `demo_gkx_chain` 上按端点 Tag 组合逐一计数（每种组合单独锚定 Tag 查询，不走全表扫描）：

| # | 端点组合 | 实测条数 | 应等于 | 判定 |
|---|---|---:|---|---|
| 1 | `enterprise` → `enterprise` | 94,824 | M22 存量 | ✅ 与 T01 基线一致 |
| 2 | `person` → `person` | 2,525,789 | M01 | ✅ 与 T03 交付一致 |
| 3 | `research` → `research` | 3,442,271 | M02 | ✅ 与 T02 交付一致 |
| 4 | `person` → `research` | 0 | M03（本期 0） | ✅ |
| 5 | `research` → `person` | 0 | — | ✅ 无反方向 |
| 6 | `enterprise` → `person` | 0 | — | ✅ |
| 7 | `person` → `enterprise` | 0 | — | ✅ |
| 8 | `enterprise` → `research` | 0 | — | ✅ |
| 9 | `research` → `enterprise` | 0 | — | ✅ |
| | **9 组合合计** | **6,062,884** | — | 与 3 个对角组合之和相等 |

**结论：** `cooperate` 边型被三组数据完全干净地分割，**没有任何跨组合污染**（不存在「人才→机构」被记成 `cooperate` 的情况，也不存在 M03 数据混入 M02）。

### 2.1 补充核验（M02）

| 检查 | 结果 | 判定 |
|---|---|---|
| `research`→`research` 总数 | 3,442,271 | ✅ 与 T02 报数一致 |
| 其中 `props` 含 `comply-20261111-t02` | 3,442,271（100%） | ✅ 无未打戳残留 |
| 非 0 rank（同对重复写） | 0 | ✅ 无覆盖冲突 |
| 反规范方向（`src >= dst`） | 0 | ✅ 无向去重正确 |
| `research` 点总数 | 83,745 | ✅ 未被 T02 重建或冲掉 |

---

## 三、T07 对账的正确写法

**必须按端点 Tag 对分组**，不许用 `cooperate` 全量。推荐三条独立查询（各自走 Tag 索引，不用全表扫）：

```
-- M22 存量
MATCH (a:enterprise)-[e:cooperate]->(b:enterprise) RETURN count(e) AS c;
-- 期望 94824

-- M01（T03）
MATCH (a:person)-[e:cooperate]->(b:person) RETURN count(e) AS c;
-- 期望 2525789

-- M02（T02）
MATCH (a:research)-[e:cooperate]->(b:research) RETURN count(e) AS c;
-- 期望 3442271
```

对账单上写三行，不要写一行合计。

### 3.1 绝不能用的写法

| 错误写法 | 后果 |
|---|---|
| `MATCH ()-[e:cooperate]->() RETURN count(e)` | 得 6,062,884，无法拆到 M01/M02/M22 任何一条 |
| 用 `cooperate` 全量当 M02 分母 | 3,442,271 / 6,062,884 = 56.8%，无意义 |
| 只筛 `props.batch` 不筛端点 | 会同时命中 T02 与 T03 两批（若将来批次命名趋同更危险） |
| 用 `src >= dst` 之外的规则判无向 | 三组各自有自己的规范化约定，不能混用 |

---

## 四、⚠️ props 键序陷阱（本次实测发现）

**T02 与 T03 的 `props` JSON 键序不同，不能复用同一条前缀查询。**

- T03 的 `props` 以 `{"batch":...` 开头，所以 T03 验收时用
  `e.props STARTS WITH "{\"batch\":\"comply-2026-11-11-t03\","` 能正确计数 2,525,789。
- T02 的 `props` **`batch` 键不在首位**，实测样例：

  ```json
  {"first_year":2023,"latest_year":2023,"year_count":1,"co_paper_count_total":1,
   "match_method":"coauthor","batch":"comply-20261111-t02",
   "source_table":"ads_institution_collaboration_yearly", ... }
  ```

  照抄 T03 的 `STARTS WITH "{\"batch\":\"comply-20261111-t02\","` 查询，**返回 0**，会让人误以为 T02 没打批次戳。

**正确写法**（本次实测可用，返回 3,442,271）：

```
MATCH (a:research)-[e:cooperate]->(b:research)
WHERE e.props CONTAINS "comply-20261111-t02"
RETURN count(e) AS c;
```

**长期建议**：T07 及后续批次一律用 `CONTAINS "<批次戳>"` 或解析 JSON 取字段，**禁止假设 `batch` 在 JSON 首位**。T03 那条前缀写法虽然能过，但属偶然依赖键序，不宜推广。

---

## 五、⚠️ 图库内存高水位告警（运维待处理）

本次验收过程中，图库 `10.50.75.136:9669` 多次出现：

```
Used memory hits the high watermark(0.800000) of total system memory.
```

- 表现：连接时通时断（`nc` 探端口始终 OPEN，但 `ConnectionPool.init` 报 `BAD`）；部分大查询直接失败。
- 触发条件：**不带 Tag 锚定的全表扫描**，例如 `MATCH ()-[e:cooperate]->() RETURN count(e)`，以及带 `sum()` / `properties()` 的大范围聚合。
- 已成功的查询：按 Tag 锚定的分组计数（最快 2 秒，最慢 33 秒）。
- 已失败的超时/拒服务查询：`MATCH (a)-[e:cooperate]->(b) RETURN tags(a),tags(b),count(e)`（73 秒拒）、`MATCH (a:research)-[e:cooperate]->(b:research) RETURN e.props LIMIT 1`（20 秒拒）、`sum(e.weight)` 全量聚合（**518 秒后拒**）。

**判断**：T02 灌入 3,442,271 条边后，实例逼近内存上限，全扫描能力已基本丧失。这不影响数据正确性（分组计数全部通过），但影响：

1. **T07 若用全表扫描式对账脚本会直接跑挂**，必须改用 Tag 锚定 + 分组；
2. 后续还有若干任务要灌边，**建议运维（淮哥侧）扩容或调整 `high_watermark` / 内存配额后再继续大批量写入**；
3. M02 的 `weight` 总和（T02 报 **14,715,117**）我本次**未能独立复核**——全量 `sum(e.weight)` 在 518 秒后被内存水位拒绝。该项暂采信 T02 自述，标注为「待内存释放后补验」，不构成签收阻塞，但须记录。

---

## 六、签收建议

T02 报数与我实测在**边数层面完全一致**（3,442,271 / 批次覆盖率 100% / rank 与方向零异常 / `research` 点未被冲掉 / 三组无跨组合污染），技术上具备签收条件。两点需在签发时一并写入对账单：

1. **M02 分母用 3,442,271，不用 6,568,617。** 后者是「合格年度行数」，不是跨年合并后的边数——T02 报告第 26 行已自行说明，此处确认为正式口径。这也再次印证 11-12 在 T03 裁定 §8.4 记下的教训：**涉类型过滤或跨年合并的边数，必须在「唯一对/合并后」层计数，不能按源行数推算**。我 11-11 给的 6,568,617 上限按行数推算，实测 3,442,271，偏差 47.6%，属我方预估口径问题。
2. **`weight` 总和 14,715,117 待补验**，其余项已现场复核通过。

---

## 七、复核命令（可原样复跑）

```bash
# 三组分组计数（务必逐条跑，不要合成一条）
nebula-console -addr 10.50.75.136 -port 9669 -u root -p trsadmin -e 'USE demo_gkx_chain; MATCH (a:enterprise)-[e:cooperate]->(b:enterprise) RETURN count(e)'
nebula-console -addr 10.50.75.136 -port 9669 -u root -p trsadmin -e 'USE demo_gkx_chain; MATCH (a:person)-[e:cooperate]->(b:person) RETURN count(e)'
nebula-console -addr 10.50.75.136 -port 9669 -u root -p trsadmin -e 'USE demo_gkx_chain; MATCH (a:research)-[e:cooperate]->(b:research) RETURN count(e)'

# 批次覆盖率（用 CONTAINS，不要用 STARTS WITH）
nebula-console -addr 10.50.75.136 -port 9669 -u root -p trsadmin -e 'USE demo_gkx_chain; MATCH (a:research)-[e:cooperate]->(b:research) WHERE e.props CONTAINS "comply-20261111-t02" RETURN count(e)'

# 反向与 rank 异常
nebula-console -addr 10.50.75.136 -port 9669 -u root -p trsadmin -e 'USE demo_gkx_chain; MATCH (a:research)-[e:cooperate]->(b:research) RETURN sum(CASE WHEN rank(e)==0 THEN 0 ELSE 1 END), sum(CASE WHEN src(e)<dst(e) THEN 0 ELSE 1 END)'
```
