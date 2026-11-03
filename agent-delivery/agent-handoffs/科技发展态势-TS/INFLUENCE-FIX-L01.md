# INFLUENCE-FIX-L01 · 影响力 Tab 三缺陷修复

> **任务**：科技全域态势 → 影响力 Tab 计算口径修复（用户 2026-11-01 报障）
> **角色**：`agent:api-agent` · 监管人：`human:李伟`
> **状态**：`integration`（改动停本地，**未 commit / 未 push**，待人工验收）
> **规格**：[INFLUENCE-FIX-spec/spec.md](./INFLUENCE-FIX-spec/spec.md)（已批准）· 任务 [tasks.md](./INFLUENCE-FIX-spec/tasks.md)
> **挂接**：WBS §4.3（WBS-05-18-12） · 台账 [mock-ledger.md](./mock-ledger.md)「影响力登记」3 行 · 2026-11-01

---

## 一、报障原文与三缺陷

> 「影响力那个计算有问题　首先没有跟筛选条件变动　其次只有企业和组织结构　再有影响力的值是错的」

| # | 现象 | 根因（原实现） |
|---|---|---|
| 1 | 不改筛选条件 | 机构卡此前**完全不吃** `enabledFactorKeys` / `regionPaths` / `activeRegionKey` / `searchTerm`，只按全库 Top-50 出卡；其余卡也没有统一的要素守门 |
| 2 | 只有企业 / 组织机构两类 | `/influence` 只装配 enterprise + institution 两卡；demo 冻结种子的 5 类卡缺 3 类 |
| 3 | 影响力值是错的 | 机构卡 `averageScore` = **原始论文数均值**（截图 56,379.0），`count` 又被前端 `?? 0` 渲染成「对象数量 0」；卡下还挂着编造的复合公式 `S = clamp(算法基础分 × 地域系数 × 领域系数 × 时间跨度修正, 0–99.9)` |

## 二、口径裁定（用户 2026-11-01 三项回答）

1. **要素范围**：先查 `agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx`——五类对象级影响力指标**均已登记**（`M_INNOV_PAPER_INFLUENCE` / `M_INNOV_JOURNAL_INFLUENCE` / `M_INNOV_PATENT_INFLUENCE` 部分支持、`M_INNOV_CONFERENCE_INFLUENCE` 完全不支持、`M_INNOV_SCHOLAR_INFLUENCE` 完全转换支持、`M_INNOV_ENTERPRISE_INFLUENCE` / `M_INNOV_ORG_INFLUENCE` 部分支持、`M_SVC_ORG_TECH_SCORE` 部分支持），但**全部依赖 dwd 层且对象级算法服务未上线** → 缺的 3 类按用户指示**用 mock 补齐**并登记台账。
2. **机构口径**：算法侧**已有统一范式**（`metrics/calc-logic/INNOV/*INFLUENCE*.md`）：`原始计数 → P99.9 缩尾 → log1p → 组内 min-max → ×100 → 多维加权`；机构加权度 `0.6923·专利数 + 0.3077·论文数`。本环境**专利维无接入通道**，按官方「缺测维按权重重归一」规则**退化为单维**：`log1p(论文数) → 榜单内 min-max → 0–100`，并在 `caliberNote` 如实声明。**不是自造口径**，接真数后按 0.6923/0.3077 加权恢复。
3. **对象数量**：机构总数**无统计源**（久新只给全国/全球年度口径），`count` 返 `null`，前端显示「—」+ 口径说明；**不拿全国 48,444 配湾区 Top-50**。

## 三、改动面（2 仓 4 文件）

| 仓 | 文件 | 改动 |
|---|---|---|
| `lumen-svc-platform` | `gkxlumen-display/.../controller/SituationController.java` | 新增 `factorInScope`（要素守门公共方法，`enterpriseInScope` 委托）；`/influence` 重写为 5 类装配（技术产出 → 企业 → 机构 → 专家 → 服务）；机构请求真实传 `city`/`cities`；`buildInstitutionInfluenceCard` 改归一化 + `rawValue` + `countNote`/`caliberNote`；新增 `inGbaShowCity` / `showCityOf`（久新 `city_name` 不带「市」）；`defaultFactorType` 取首卡；`totalCount` 跳过 null |
| `lumen-svc-platform` | `gkxlumen-display/.../support/SituationMockProvider.java` | 追加 `influenceScopeScale`（筛选签名确定性缩放）/ `technologyOutputCard`（论文・期刊・专利三子类）/ `influenceCard(scholar|service)`；`INFLUENCE_MOCK_VERSION="influence-v1"`、`INFLUENCE_MOCK_REASON` 引用 5 个指标 ID；`baseCard` 分统一 `clampScore`（0–99.9 一位小数） |
| `lumen-ui-science-pc` | `src/types/situation.ts` | `InfluenceItem` 补 `metricLabel` / `rawValue` / `mock*`；`count` 与 `totalCount` 改 `number \| null`；`InfluenceCard` 补 `countNote` / `caliberNote`；`InfluenceDataset` 补 `anyMock` |
| `lumen-ui-science-pc` | `src/views/situation/overview/components/InfluenceTab.vue` | `formatCount`（null → 「—」）/ `metricLabelOf`；删虚假复合公式改渲染 `caliberNote + source`；`countNote` 渲染；卡位与详情挂 `MockBadge`（`@/review`） |

## 四、验证证据

### 4.1 后端（`http://localhost:7099/v1/situation/influence`，7 条）

| # | 输入 | 结果 |
|---|---|---|
| ① | 全域无筛选 | ✅ 5 卡、`defaultFactorType=technologyOutput`、`totalCount=5,093,158`、`anyMock=true`；技术产出 94.5 / 企业 36.6(51,758) / 机构 32.5(—) / 专家 86.6 / 服务 82.8 |
| ② | `regionPaths=[[city-cluster,gba,shenzhen]]` | ✅ 企业 51,758 → **23,837**；机构 items 全为「深圳」（Top1 深圳大学 score=100 raw=21,482）；技术产出 94.5 → **91.7** |
| ③ | `enabledFactorKeys=["paper"]` | ✅ 仅 1 卡 `technologyOutput`（count 2,960,000，子类仅「论文」）；`["institution"]` → 仅机构卡且 default 指它 |
| ④ | `searchTerm=清华` | ✅ 企业 1 家（清华附中湾区学校）、机构 1 家（清华大学伯克利分校深圳研究院）——**机构卡按关键词联动**（py 不支持机构名检索，只能在已取回榜单内过滤，`source` 已声明） |
| ⑤ | 机构卡契约 | ✅ `count=null` + `countNote`；`averageScore=32.5∈(0,100]`；`items[0].score=100`、末位 0.0；`metricLabel="相对影响力分"`；`source` 含「归一化（M_INNOV_ORG_INFLUENCE 范式）」与「专利维未接入」；`caliberNote` 写全 log1p / min-max / 缺测重归一 |
| ⑥ | 同参两次 | ✅ 全卡 `factorType:averageScore` 串完全一致（**幂等，无随机**）；3 张 mock 卡带 `mock=true` / `mockReason` / `mockVersion=influence-v1` |
| ⑦ | `timeRange` 2020–2026 → 2010–2026 | ✅ 技术产出 94.5→**95.5**、专家 86.6→**87.4**、服务 82.8→**83.6** |

编译 / 打包 / 重启：`mvn -o -q -DskipTests -pl gkxlumen-display -am compile|package` exit 0（JDK17 离线）；停 :7099 → 重启 `java -jar --spring.profiles.active=local` → LISTENING。

### 4.2 前端

| # | 验证 | 结果 |
|---|---|---|
| ⑧ | `npm run type-check` | ✅ exit 0（首轮报 `metricLabelOf` 只收 `InfluenceCard`，已放宽为 `InfluenceCard \| InfluenceSubFactor`） |
| ⑨ | `npm run build` | ✅ exit 0（仅既有 unocss / Node 版本告警） |
| ⑩ | :3000 页面实跑 | ✅ 「影响力」Tab 显示 **技术产出 94.5 / 企业 / 科研机构 / 专家**；机构「对象数量 —」+ 口径说明；无虚假复合公式，改为「口径注释」；切地域到深圳市后企业 51,379 → **23,834**（筛选联动生效） |
| ⑪ | 评审关闭零泄漏 | ✅ 结构保证 + 同款 `MockBadge` 根部 `v-if`（D3 同组件已实测过同类回归）；本次未重复改开关 |

## 五、已知限制（如实声明，未作假）

1. ~~服务项目卡当前页面不可达~~ → **已解除（2026-11-01 追加接线）**：服务机构要素在 `/situation/map` `factorItems` 中 `active=true`（`service` 计数 6200 家，来源 `mock` + `mockReason`），并已进 `regions[].layerKeys`；前端 `effectiveFactorKeys` 因此含 `service`。页面默认见 **5 类**（技术产出 / 企业 / 科研机构 / 专家 / 服务项目）。**数值仍是 mock**（CMS `v_cms_svc` 真实计数未接入），台账已登记。
2. **机构榜不支持年份 / 领域**：久新 `carrier-list` 无年份、无领域参数；`caliberNote` 与 `source` 明写「机构榜不支持时间范围与领域筛选」「关键词仅过滤榜单内」。
3. **领域（`selectedFieldValues`）全线不参与**：企业主表无领域列、久新机构表无领域列；技术产出的 mock 缩放**计入**领域（demo 同式），但不改变真实卡范围。
4. ~~页面时间选择器仅开放 2025–2026~~ → **已放开到 2015（2026-11-01 追加修正）**：`DEFAULT_YEARS` 扩为 2015–2026，`years` 改为「静态基准 ∪ 响应年份」（响应只回两年也不再收缩下拉）；请求入参仍只读 store + 静态基准，未引入自激循环。

## 六、mock 点位（详见台账）

[mock-ledger.md](./mock-ledger.md)「影响力登记（2026-11-01，INFLUENCE-FIX-L01）」3 行：`technologyOutputCard`（paper/journal/patent 子类）、`influenceCard("scholar")`、`influenceCard("service")`，均 `mock_version=influence-v1`，含接替条件与清理动作。

## 七、去 mock 接真数路径

1. 对象级影响力算法服务上线（dwd 通道 + `M_INNOV_*_INFLUENCE` 五指标）→ 删 `technologyOutputCard` / `influenceCard` / `TECH_OUTPUT_*` / `SCHOLAR_ITEMS` / `SERVICE_ITEMS`，装配改 Feign。
2. 机构：`M_INNOV_ORG_INFLUENCE` 专利维接入后，按 `0.6923·专利数 + 0.3077·论文数` 加权恢复（当前单维为**缺测重归一**退化）；机构总数统计源到位后 `count` 不再为 null。
3. 服务机构：CMS `v_cms_svc` 接线 → 把 `SituationMockProvider` 的 `service` 计数换成真实 CMS 计数（`/map` `factorItems.service` 的 `source` 同时从 `mock` 改回真实标注）；影响力服务项目卡改调 `M_SVC_ORG_TECH_SCORE` 算法服务（卡已可达，当前数值仍是 mock）。

## 八、Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | mock 集中单一 Provider、契约 `mock/mockReason/mockVersion` 完整；机构分按官方范式（非自造），缺测维如实声明未伪闭合；`count=null` 不以 0 冒充；删编造公式；筛选联动实测（地域/关键词/年份/要素四路）；无随机（同参幂等） |

## 九、Cost（成本四字段）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 120000 |
| actual_tokens | ~210000（xlsx 核查 + 算法口径查证 + 双仓实现 + 编译打包重启 + 7 条端点 + type-check/build + 两次浏览器实跑） |
| model_used | DeepSeek-V4.1-Flash |
| actual_cost | ~$2.2（估算） |
| cost_warn | green（< $5） |

## 十、改动停本地（人工验收闸门）

- 两仓改动**未 commit / 未 push**，停本地等 `human:李伟` 走查。
- 服务状态：display :7099 已用新 jar 重启（含本修复）；前端 :3000 dev 运行中。

## 十一、追加修正（2026-11-01，用户指令「年份放开到2015　服务机构要素接线」）

**1) 年份放开到 2015（前端）** —— `lumen-ui-science-pc/src/views/situation/overview/index.vue`
- `DEFAULT_YEARS`：`2020–2026` → **`2015–2026`**；
- `years`：原来直接返回响应 `timelineData.years`（实测只回 2025/2026），改为**静态基准 ∪ 响应年份**（数值升序去重）；
- 请求入参口径不变：`normalizedTimeRange` 仍只读 `store.timeRange` + 静态基准（**不掺响应派生值**，避免之前 15 秒 99 次请求的自激循环复发）。

**2) 服务机构要素接线（后端）**
- `SituationMockProvider`：`COUNTS` / `UNITS` 增 `service = 6200 家`；新增 `REASONS` 逐要素 mock 原因（`service` 用 `SERVICE_MOCK_REASON`＝CMS `v_cms_svc` 未接，**不套用期刊/会议的 §24.10 文案**）；`metadata()` 按 key 取原因；
- `SituationController`：`MOCK_FACTOR_ORDER` 增 `service`（**关键**：前端 `effectiveFactorKeys` 取 `regions[].layerKeys` ∩ 勾选集，只填 `factorItems` 不填图层 → 要素永远不可达）；`sourceOf` 增 `service` 分支（写明 CMS 真源）；
- `buildFactorItems` 的 mock 覆盖循环自动把 `service` 置 `active=true`、`count=6200`、`source=mock` + `mock` 标记。

**验证证据**
| # | 项 | 结果 |
|---|---|---|
| ① | `mvn -o -q -DskipTests -pl gkxlumen-display -am package` | ✅ exit 0 |
| ② | `/v1/situation/map`（空参） | ✅ `service`：`active=true` / `count=6200` / `source=mock` / `mock=true`；9 个城市的 `layerKeys` 均含 `service` |
| ③ | `/v1/situation/influence`（空参） | ✅ `analyzableFactorCount=5`：技术产出 94.5 / 企业 / 科研机构 32.5 / 专家 86.6 / **服务项目 82.8（6200）** |
| ④ | `/v1/situation/map` + `/influence`（`timeRange=2015–2026`） | ✅ 9 城正常；5 卡；服务项目 count 7192 / 均分 83.6（随年份跨度缩放，证明 2015 入参生效） |
| ⑤ | `npm run type-check` / `npm run build` | ✅ exit 0 |
| ⑥ | :3000 页面实跑 | ✅ 影响力 Tab 出现 **5 个卡 tab**（含「服务项目」）；时间控件「开始年份」下拉**包含并可选 2015** |

> ⚠️ 诚实边界：服务机构**计数 6200 家仍是 mock 种子**（CMS `v_cms_svc` 真实计数端点未接入、本机 CMS 未运行），台账已登记（`mock-ledger.md` D3 新增 1 行 + 改 1 行）。影响力服务项目卡同理（`influence-v1`）。
