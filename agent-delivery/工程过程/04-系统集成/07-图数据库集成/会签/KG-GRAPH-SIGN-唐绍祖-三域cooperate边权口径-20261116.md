# 会签 · 三域 `cooperate` 边权口径裁定（ALGO / 唐绍祖，2026-11-16）

| 项 | 内容 |
|---|---|
| 会签事项 | ① 淮政玮 11-13 18:25「全量属性聚合线上不允许」的技术确认；② 我在 11-16 答复里承诺会签的「人才侧强度口径」；③ 与之同源的科研机构、企业侧边权口径 |
| 会签人 | 唐绍祖（ALGO / 技术验收 + 算法口径） |
| 会签状态 | **已签**（本文即会签件；需淮政玮、白鑫凤、宋飞扬知会确认，见 §六） |
| 依据 | T02 对账（已签收）、T09-S1 加权度（已签收）、T12 契约（已签收）；2026-11-16 现场只读实测 |
| 实测方式 | 只读连 `10.50.75.136:9669` / `demo_gkx_chain`，只做 `MATCH ... RETURN`，未写任何点边、未改任何配置 |

---

## 一、一句话结论

**`cooperate` 一条边型下压着三批语义完全不同的边，`weight` 在三批里各是不同东西（篇数 / 类型等级 / 全零），所以「全图 `sum(weight)`」无业务含义，淮政玮的判断成立；同时人才侧真正可用的强度字段不是 `weight` 而是 `co_paper_count`，且该边的 `props.weight_field` 声明与实际取值不一致，属需登记的缺陷。**

---

## 二、三条口径裁定（本次会签的正式结论）

### 2.1 M01 人才→人才：强度 = `co_paper_count`，`weight` 与 `collaboration_score` 禁用

| 实测项（11-16） | 结果 |
|---|---|
| 边数 | **2,525,789**（13.3 秒） |
| `weight` 取值 | 抽样 3,000/3,000 **全为 0.0**；分组求和 **0** |
| `props.collaboration_score` | 抽样 **3,000/3,000 全为 null** |
| `props.weight_field` | 声明为 **`"collaboration_score"`**，而该字段全空 |
| `props.co_paper_count` | 抽样仅 2/3,000 为 null，**有值**（样本合计 154,606） |
| `props.co_patent_count` | 2,997/3,000 为 null（几乎无值） |
| `props.co_project_count` | 3,000/3,000 全 null |

**裁定**
1. 人才侧合作强度**本期一律用 `props.co_paper_count`**（合著篇数，可复算、可排序）；
2. `weight` **不得**用于加权度、排序、连线粗细、榜单单列——它全 0，用则全部并列；
3. `collaboration_score` 本期**为空壳**，任何接口不得以它为字段名对外（对外若需「强度」字样，注明口径为合著篇数）；
4. `weight_field` 声明与实际不符，记为**数据缺陷 D-1**（见 §四），不阻塞本期，但必须在 COVER-01 后的下一批修。

### 2.2 M02 科研机构→科研机构：`weight` 是「合著篇数」，不是「合作强度」

| 实测项（11-16） | 结果 |
|---|---|
| 边数 | **3,442,271**（15.1 秒） |
| `weight` 总和 | **14,715,117**（与 T02 报数完全一致） |
| `weight` vs `co_paper_count_total` | 抽样 300/300 **逐条相等** |
| `props.strength_by_year` | 有值，例：`{"2023": 0.047619}`、`{"2022": 0.071429, "2025": 0.028571}` |
| `props.strength_note` | **"normalized separately each year; do not compare across years"**（逐年分别归一，禁跨年比较） |
| `props.undirected` / `canonical_order` | 有值（无向、端点已规范化排序） |

**裁定**
1. **14,715,117 的正确称法是「机构对合著篇数总量」，不是「全库合作强度」**。M02 对账口径不变，继续用它；
2. 需要「强度」语义时，只能用 `props.strength_by_year` 的**分年值**，且**禁止跨年相加、禁止跨年比较**（边自带的 `strength_note` 已写明）；
3. `weight` 可跨年累加（因为是篇数计数），这一点与 2) 不冲突，但表述必须分开，避免把「篇数」说成「强度」。

### 2.3 M22 企业→企业（存量）：`weight` 是合作类型**等级**（序数），禁止求和

| 实测项（11-16） | 结果 |
|---|---|
| 边数 | 94,824 |
| `weight` 取值样本 | 8.0（props `{"coop":"战略合作"}`）、7.0（`{"coop":"技术许可"}`） |
| `props` 键 | 仅 `coop` 一个；无 `weight_field`、无分年强度 |

**裁定**：这是**序数标签**（类型编号），不是可加量。**禁止求和、禁止算加权度、禁止当连续值画粗细或排序**。若要对外展示，按 `coop` 文字值分类呈现。

---

## 三、与淮政玮质询的对接

我没改他的结论，只把边界划清：

| 淮政玮原话 | 我的确认 |
|---|---|
| 「这条语句没有实际应用吧」 | **确认**：线上 12 个端点（428–432、435、437 读归档；400–407 带 Tag 锚定且子图 ≤500；41 走 M10 R1 单实体邻域；404/405/407/436 是 501）**无一依赖全图 `sum`**。但它是 T02 的对账语句，非凭空造数；11-13 复跑时漏了端点锚定才把三批混成 15,142,250 |
| 「正常线上接口里不允许这种全量属性聚合」 | **确认，但限定为**：无 Tag/端点锚定、无结果上限、无超时保护的**在线**全图聚合。分组加权（428 `weight_sum_incident`、M02 篇数）是签收口径，属**离线预计算 + 接口读归档**，不在此列 |

**红线原文（建议进 SDD §5，我这边签字同意）**

> ① 禁止上线任何无锚定、无上限、无超时保护的全图属性聚合（`sum` / `properties` / `collect` 类）。
> ② 对账类全图聚合允许，但须：按端点分组锚定、非业务时段执行、大批量灌数前先重启释放累积内存、结果只落文档不入接口。
> ③ 分组加权（428 加权度 `weight_sum_incident`、M02 机构对合著篇数）为一等公民口径，走离线预计算，不得因本红线删除或降级。

---

## 四、登记缺陷（本期不修，但必须挂账）

**D-1 · 人才合作边 `weight_field` 声明与实际不符**

- 现象：`props.weight_field = "collaboration_score"`，但 `collaboration_score` 3,000 抽样全 null；`weight` 全 0；真正有值的是 `co_paper_count`。
- 影响：任何按 `weight_field` 取强度的通用代码，在人才域会拿到全 0（不报错、静默全并列），比报错更难发现。
- 处置：本期口径按 §2.1 走 `co_paper_count`；下一批（COVER-01 之后）由白鑫凤确认是「源表 `ads_talent_collaborator` 未给分」还是「灌数漏字段」，再决定补分或改 `weight_field` 声明。
- 责任：白鑫凤（数据面确认）、唐绍祖（口径复核）。

**D-2 · `co_patent_count` / `co_project_count` 几乎全空**

- 现象：抽样 `co_patent_count` 2,997/3,000 null、`co_project_count` 3,000/3,000 null。
- 影响：人才侧目前**只能算合著论文强度**，专利/项目合作强度不可用。
- 处置：对外文案不得出现「专利合作强度」「项目合作强度」；接口对这两维返回 `availability=missing`，不返回假 0。

---

## 五、对下游的具体要求（会签生效即约束）

| 下游 | 要求 |
|---|---|
| `KG-GRAPH-RECALC-02`（韩梦蕊，监管 我） | 榜单与加权度**一律不得用人才侧 `weight`**；若出人才侧强度榜，取 `co_paper_count`，字段名与 `meta.formula` 写明；M02 篇数 14,715,117 只作对账，不作「强度」对外 |
| `KG-GRAPH-TRIPLE-03`（宋飞扬） | `PERSON_RE_NEIGHBORS` / `PERSON_RE_SUBGRAPH` 的边宽/强度取 `co_paper_count`；`PERSON_GRAPH_BROWSE`（浏览与排序）不得按 `weight` 排序；`RESEARCH_RE_NEIGHBORS` / `RESEARCH_RE_SUBGRAPH` 若展示强度，取 `strength_by_year` 并标注年份，禁跨年合并 |
| `KG-GRAPH-API-04`（李周） | 423/428 一类加权度只针对技术点层 `tech_*` 边，**不涉及**人才/机构 `cooperate`，本期不受影响；若将来扩到人才层，须回本文取口径 |
| 前端展示 | 企业侧连线粗细不得按 `weight`（序数）；机构侧不得把 14,715,117 当「总强度」展示 |
| SDD §5 | 收录 §三 红线三条 |

---

## 六、会签栏

| 角色 | 人 | 意见 | 状态 |
|---|---|---|---|
| ALGO / 技术验收 | 唐绍祖 | 三条口径确认，红线同意，D-1/D-2 挂账 | ✅ 已签（2026-11-16） |
| 大项目架构师 | 淮政玮 | 确认红线原文进 SDD §5；D-1 派给白鑫凤 | ⬜ 待确认 |
| 数据面（M01/M02 交付方） | 白鑫凤 | 确认 D-1 成因（源表无分 or 漏灌） | ⬜ 待确认 |
| TRIPLE-03 执行人 | 宋飞扬 | 按 §五 实现 110/111、114/115 | ⬜ 待知会 |

---

## 七、实测记录（可原样复跑）

```bash
# 三批边数（11-16 实测，全表 count 已恢复可用）
nebula-console -addr 10.50.75.136 -port 9669 -u root -p trsadmin -e \
  'USE demo_gkx_chain; MATCH (a:person)-[e:cooperate]->(b:person) RETURN count(e)'      # 2,525,789 / 13.3s
nebula-console ... 'USE demo_gkx_chain; MATCH (a:research)-[e:cooperate]->(b:research) RETURN count(e)'  # 3,442,271 / 15.1s

# 分组 weight 总和（必须带端点锚定，禁无锚定全表）
# person     → 0
# enterprise → 427,133
# research   → 14,715,117

# 属性抽样（LIMIT 有界，禁止全表拉 props）
# person   : weight 全 0；weight_field=collaboration_score（全空）；co_paper_count 有值
# research : weight == co_paper_count_total（300/300）；strength_by_year 分年归一
# enterprise: props 仅 {"coop": "战略合作" | "技术许可"}
```

**风险提示**：上述 `RETURN e.props LIMIT n` 属有界抽样（n ≤ 3000，耗时 20–27 秒）。**不要去掉 `LIMIT` 或改成无锚定聚合**——11-13 已验证，一条无锚定全图属性聚合会把实例打到 80% 水位并退出，4 小时 9 分不自愈。
