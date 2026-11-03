# 科技全域态势 · 影响力 Tab 三项缺陷修复（INFLUENCE-FIX-L01）

> 状态：待 `human:李伟` 批准 → 执行 → 停本地等人工验收（**严禁 commit/push**）
> 关联：`SITUATION-ENT-D3-L01`（mock Provider 基础设施）、`mock-ledger.md`
> 用户原话（2026-11-01）：「影响力那个计算有问题 首先没有跟筛选条件变动 其次只有企业和组织结构 再有影响力的值是错的」

## 一、缺陷与根因（已核实代码位置）

| # | 现象 | 根因 | 位置 |
|---|---|---|---|
| 1 | 换筛选条件数据不动 | 机构卡**完全不吃** `enabledFactorKeys` / 地域 / 关键词 / 年份；企业卡被要素范围挡掉后只剩机构卡，「怎么筛都不动」 | `SituationController.influence` L1024-1036；`buildInstitutionInfluenceCard` L1523-1564 |
| 2 | 只有企业 + 组织机构两类 | 后端只装配这两张卡；demo 有 5 类（技术产出[论文/期刊/专利]、企业、科研机构、专家、服务项目） | `influence` L1000-1036；demo `data.js` `influenceFactorCards` |
| 3 | 影响力值错 | ①机构卡 `averageScore` 实为 Top50 湾区机构**平均论文数**（截图 56379.0）被渲染成「平均影响力」；②`count=null` 被前端 `Number(x ?? 0)` 渲染成「对象数量 0」；③公式注释是 demo 的复合公式 `clamp(基础分×地域系数×领域系数×时间修正)`，后端从未实现 | 后端 L1557；前端 `InfluenceTab.vue` L171-174 / L179 / L183 |

## 二、口径调研结论（决定实现方式）

### 2.1 xlsx 核查（`指标入库详情-合并-20261028-三系统.xlsx`）

五类对象级影响力指标**均已登记**（技术专题系统 / 科技展示系统 / 科技专题算法库 三 sheet 均有命中）：

| 对象 | 指标ID | 数据支持度 | 源表（节选） |
|---|---|---|---|
| 论文 | `M_INNOV_PAPER_INFLUENCE` | 部分支持 | dwd_en_paper; dwd_zh_paper; dwd_zh_paper_citation |
| 期刊 | `M_INNOV_JOURNAL_INFLUENCE` | 部分支持 | dwd_en_journal; dwd_zh_journal |
| 专利 | `M_INNOV_PATENT_INFLUENCE` | 部分支持 | dwd_patent; dwd_patent_cited |
| 会议 | `M_INNOV_CONFERENCE_INFLUENCE` | **完全不支持** | dwd_conference_* |
| 项目/课题 | `M_INNOV_PROJECT_INFLUENCE` | 部分支持 | dwd_zh_project; dwd_zh_project_output |
| 企业 | `M_INNOV_ENTERPRISE_INFLUENCE` | 部分支持 | dwd_org_*; dwd_patent; dwd_patent_transfer |
| 科研机构 | `M_INNOV_ORG_INFLUENCE` | 部分支持 | dwd_patent; dwd_zh_paper; dwd_research_institute_base_info |
| 专家 | `M_INNOV_SCHOLAR_INFLUENCE` | **完全转换支持** | dwd_scholar; dwd_scholar_papers |
| 服务机构 | `M_SVC_ORG_TECH_SCORE` | 部分支持 | dwd_patent; dwd_org_stock_finance_info |

**结论：指标定义"有"，但**（a）全部依赖 dwd 层，display BFF 无直连通道；（b）无对应算法服务 / 结果面已上线。

### 2.2 算法侧统一口径（唯一真源）

`metrics/calc-logic/INNOV/*INFLUENCE*.md` 五份独立文档共用同一范式：

```
原始计数 → P99.9 缩尾 → log1p → 组内 min-max → ×100 → 多维加权/等权
```

- 论文：`S = 100·(0.7·norm(C) + 0.3·norm(IF))`，IF 整列缺测 → 按缺测重归一退化为 `S=100·norm(C)`
- 科研机构：加权度 = `0.6923·专利数 + 0.3077·论文数`（原 0.45/0.20 再归一），log1p + min-max，×100；实算 312 家 4.25–81.18
- 企业：科创/成果转化/产业带动三维，P99.9 缩尾 + log1p + min-max 等权 ×100
- 专家：h_index / citation_nums / paper_nums 三列 log1p + min-max 等权 ×100

**因此不需要"自造归一化"，直接按官方范式实现**；机构卡当前可用的只有论文维（专利维无通道）→ 按论文文档 §5.2「缺测维重归一」规则退化到单维 `S=100·norm(log1p(paper_count))`，并在 `source` 声明专利维未接入。

## 三、实现方案（决策已定，无需再选）

### 3.1 后端 `SituationController.java`

**(A) 通用要素范围判定** — 抽出 `factorInScope(Map params, String factorKey)`（复用 `enterpriseInScope` 的 `enabledFactorKeys` 解析；空/null = 不限）。

**(B) 机构卡纳入筛选** — 改 `buildInstitutionInfluenceCard` 调用侧（L1024-1036）：
1. 仅当 `factorInScope(params,"institution")` 才出卡；
2. 地域：单选城市时传 `city = 深圳`（用 `GBA_SHOW_CITIES` 把「深圳市」→「深圳」）；未选城市时传 `cities = GBA_SHOW_CITIES`（py `carrier-list` 原生支持 `cities` 列表，后缀「市」自动 rstrip）；
3. 排序 `sort_by = "paper_count"`，`limit = INFLUENCE_ITEM_LIMIT`（有地域过滤后不再需要放大取样）；
4. 关键词：`searchTerm` 非空时在**结果侧** `name.contains` 过滤（py 不支持机构名过滤，`source` 声明"关键词仅过滤榜单内"）；命中 0 条 → 不出卡（前端走空态）；
5. 年份：py 不支持 → **不伪造**，`source` 明写「机构榜不支持时间范围筛选」；
6. 领域 `selectedFieldValues`：机构表无领域列 → 不参与，明写。

**(C) 数值口径修正（机构卡）**
- 新增 `institutionScore(paperCount, minLog, maxLog)`：`100·(log1p(v)-minLog)/(maxLog-minLog)`，全组相同取 50（与官方「全组相同取 0.5」一致）；
- `items[].score` = 归一化 0–100 分；`items[].rawValue` = paper_count 原值（可追溯）；
- `card.averageScore` = 榜单内归一化分均值（0–100）；`card.metricLabel = "相对影响力分"`；
- `card.count` 保持 `null`（纽约无统计源）→ 前端显示「—」；
- `card.countNote = "湾区机构总数无统计源（久新仅全国/全球年度口径），此处仅榜单 Top-N"`；
- `card.caliberNote` = 官方范式 + 缺测维声明；
- `card.mock` 不设（真实源）。

**(D) 补齐 5 类卡**
`influence` 装配顺序：`technologyOutput` → `enterprise` → `institution` → `scholar` → `service`。
- `technologyOutput` / `scholar` / `service` 由 `SituationMockProvider` 出卡（`mock/mockReason/mockVersion`）；
- 每张 mock 卡必须**随筛选条件变化**：`SituationMockProvider.influenceCard(key, scopeKey)` 用 `scopeKey`（city+district+term+startYear+endYear+enabled 的确定性签名）做种子缩放（**禁 `Math.random`**，同输入同输出），并在 `source` 明写「示例值按筛选签名确定性缩放，非真实检索」；
- `technologyOutput` 含 `subFactors = [paper, journal, patent]`，结构对齐 demo（`count` / `averageScore` / `items[]`）。

**(E) 契约字段修正**
- `defaultFactorType`：改为 `cards.get(0).factorType`（当前硬编码 `enterprise`，企业不在范围时会指向不存在的卡）；
- `totalCount` / `totalDefinition`：count 为 null 的卡不计入；文案改为「各要素可分析对象数之和（含 mock 口径，企业与机构为不同口径）」；
- 每张卡新增 `metricLabel`（「平均影响力」/「相对影响力分」）、`countNote`、`caliberNote`。

### 3.2 `SituationMockProvider.java`

新增（保持"单一集中模块"）：
```java
public Map<String,Object> influenceCard(String factorKey, String scopeKey)          // scholar / service
public Map<String,Object> technologyOutputCard(String scopeKey)                     // 含 3 个子类
private double scaledSeed(double seed, String scopeKey)                             // 确定性缩放
```
种子冻结自 `demo-ui-science/src/data.js` `influenceFactorCards`（技术产出 4787200/92.4、论文 2960000/91.8、期刊 7200/87.6、专利 1820000/94.2、专家 248000/84.9、服务 6200/81.2），`MOCK_VERSION` 升为 `influence-v1`，`MOCK_REASON` 增补影响力专用原因（引用 xlsx 指标ID + "算法服务未上线"）。

### 3.3 前端 `InfluenceTab.vue`

1. **卡头口径**：`平均影响力` → `{{ card.metricLabel ?? '平均影响力' }}`（L162）；
2. **对象数量**：`count == null ? '—' : count.toLocaleString()`（L179）；`countNote` 在 metrics 下方一行小字（L179-185 内新增 `<p class="influence-count-note">`）；
3. **公式注释**：删掉虚假复合公式（L171-174），改渲染后端 `caliberNote`：
   ```
   {{ selectedCard.caliberNote }} 当前来源：{{ selectedCard.source }}
   ```
4. **scope strip**：`(dataset?.totalCount ?? 0)` → null 显示 `—`（L141）；
5. **子类表头**：`平均影响力` → `{{ selectedSubFactor?.metricLabel ?? '平均影响力' }}`（L191）；
6. **mock 角标**：卡 tab + detail 处挂 `<MockBadge v-if="card.mock" :reason="card.mockReason" :version="card.mockVersion" />`（组件自身 `v-if="isReviewFeatureEnabled()"` 自闸 → 评审关闭 DOM 零泄漏）。

### 3.4 `src/types/situation.ts`

`InfluenceItem` 新增可选字段：`metricLabel?: string`、`countNote?: string`、`caliberNote?: string`、`rawValue?: number`、`mock?: boolean`、`mockReason?: string`、`mockVersion?: string`。

## 四、明确不做（防扩写）

- 不实现真实论文/专利/期刊/专家/服务项目影响力算法（需算法服务 + dwd 通道，另立任务）；
- 不把机构经纬度当对象点位（久新为城市质心）；
- 不改 `enterprise_score` 占位评分来源（正式 `M_INNOV_ENTERPRISE_INFLUENCE` 未上线）；
- 不动 D3 已完成的期刊/会议要素级 mock 逻辑。

## 五、验收标准

### 5.1 后端自检（`http://localhost:7099/v1/situation/influence`）
1. 全域无筛选 → `cards.length = 5`，`defaultFactorType = "technologyOutput"`；
2. `regionPaths=[[city-cluster,gba,shenzhen]]` → 企业卡 `count` 显著小于全域；机构卡 items 全部 `深圳市`；
3. `enabledFactorKeys=["paper"]` → 不含 `institution` 卡（要素范围生效）；
4. `searchTerm=清华` → 机构卡消失（榜单内无匹配）；
5. 机构卡：`count == null`，`averageScore ∈ (0,100]`，`items[0].score == 100`（榜单内 min-max），`source` 含「log1p / min-max」与「专利维未接入」；
6. 三张 mock 卡均含 `mock=true / mockReason / mockVersion`；同参数二次调用值完全一致（确定性）；
7. 换 `timeRange` → mock 卡值变化（证明随筛选联动）。

### 5.2 前端三绿
- `npm run type-check`（0 error）；`npm run build`（built）；
- `:3000` 页面实跑：切筛选 → 数值/卡片变化；机构卡「对象数量」显示「—」+ 口径说明；公式注释无虚假复合公式；
- 评审关闭回归：`REVIEW_FEATURE.enabled=false` 时 DOM 无 `mock` / 角标（验后恢复 true 并 `git diff` 确认为空）。

### 5.3 闸门
- 改动停本地，**不 commit / 不 push**，等 `human:李伟` 人工验收。

## 六、文档回写

1. `agent-delivery/agent-handoffs/科技发展态势-TS/mock-ledger.md`：追加影响力 3 行（technologyOutput / scholar / service），字段：页签 / 要素 / mock 值 / 真实源指标ID / 缺口原因 / 接替条件；
2. 新建 `INFLUENCE-FIX-L01.md`：mock 点清单 + 「机构卡归一化待改真实口径（专利维接入后按 0.6923/0.3077）」；
3. `task-registry.yaml` + `WBS.md`：登记本单 `status: integration`。
