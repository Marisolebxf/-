# SITUATION-ENT-C4/C5-L01 · 筛选参数贯通 + 聚类分析真实数据接入

> **触发**：走查反馈「筛选框没有和接口数据挂钩，聚类分析没数据展示」（2026-10-27）
> **角色**：`agent:frontend-agent`（兼处理 api 侧改动，监管人 `human:李伟`）
> **状态**：`integration`（待人工签收）
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md) · 倚 Z1–Z4 / A0–D1（均已完成）
> **日期**：2026-10-27

---

## 一、用户反馈与根因

| 现象 | 根因（查出来的，不是猜的） |
|---|---|
| **筛选框改了，数据不动** | display 的 `/map`、/overview **完全不消费入参**：始终是 `enterpriseOverview()` / `enterpriseRegions(30)`（无参调用），甚至 `scopeLabel` 写死「全量样本」、`fieldScopeLabel` 写死「不限领域」；只有 `/influence` 名题目鼎把地域/关键词用上了 |
| **聚类分析没数据** | `/cluster` 端点**根本不存在**——D1 叶把它标成「未上线」并用 `optional()` 收成诚实空态。所以不是 bug，是**没做** |

## 二、改了什么（4 仓文件 + 2 仓各若干）

### 后端（lumen-svc-platform）
- **element `EnterpriseController`**
  - 新增统一过滤构造器 **`appendScope(alias, city, district, name, startYear, endYear)`**（所有区块共用，防止「总量过滤、明细不过滤」口径打架）
  - `/overview`、`/regions`、`/districts`、`/trend`、`/points`、`/influence` 全部接入该过滤
  - 新增 **`/v1/element/enterprise/cluster`**（聚类原始数据源）
- **display `RemoteElementClient`** 同步上述入参；**`SituationController`**
  - 新增 **`Scope` 记录 + `scopeOf()` 翻译层**：前端 `regionPaths / searchTerm / timeRange` → 后端 city / district / name / 注册年区间
  - `/map`：`chips 计数 / 区域气泡 / 对象点位` 参与筛选；**地域级联选项不参与**（见下）
  - `/overview`：`scopeLabel` 现按真实生效维度计算；`fieldScopeLabel` 在勾了领域时明说「未参与筛选」
  - 新增 **`POST /v1/situation/cluster`**

### 前端（lumen-ui-science-pc）
- `types/situation.ts`：`SituationMapParams` 增加 `searchTerm / timeRange / selectedFieldValues / enabledFactorKeys`；`SituationOverviewParams` 增加 `searchTerm`
- `views/situation/overview/index.vue`：地图 watch 依赖加入 关键词/年份/领域/要素并重传参；总览 watch 加入关键词
- `api/situation/index.ts`：`fetchSituationCluster` 从 `optional()` 空态改回真实 `post()`（端点已上线）

## 三、一个关键取舍（请验收人裁定是否接受）

**地域级联选项不随筛选收缩**。原因：若下拉里的市/区随关键词一起被过滤掉，用户就再也点不回别的区域（导航被自己的筛选吃掉）。所以 `/map` 里为「级联选项」单发一次无过滤查询，而计数/气泡/点位走有过滤查询。**一句话：导航要稳，数据要准。**

## 四、诚实边界（这次格外重要：差点用了假数据）

聚类四个维度里，**只有三个有真数据源**：

| 维度 | 数据源 | 说明 |
|---|---|---|
| influence 影响力 | `ads.enterprise_score.score_total` | 占位口径，与 `/influence` 同源 |
| conversion 转化潜力 | `ads.tech_power.transfer_score` | 独立信号（18.9w 行里仅 1 行与 score 巧合相等） |
| collaboration 合作密度 | `ads.tech_power.cooperation_score` | 独立信号（42 行巧合） |
| **growth 增长指数** | **无** | `revenue_growth_rate` **整列 NULL**（18.9w 行实测非空数 = 0）→ 该桶返回**空 items + emptyReason**，绝不补 0 |

**排掉的坑（值得写进教材）**：`ads.enterprise_centrality.centrality_norm` 与 `pagerank_score` 看起来很像「网络/合作」指标，但实测 **逐行等于 `score_total`**（pagerank 就是 score/100）——拿它们当第二维度，会让四个维度退化成一个。**所以宁可不看数据先用心地查，也不要图省事。

**不参与筛选（已写进报错文案/UI 文案）**：
- **学科领域**：企业主表没有 domain 列，领域只在聚合表 `domain_dist` → 两表无法交叉筛选。勾了就在 `fieldScopeLabel` 上明说「已选领域未参与筛选」
- **日/周/月/季粒度**：数据只有注册年粒度
- **多选地域**：当前只用首项（多选需 OR/IN 改造，未做即不假装支持）

## 五、自测记录

**地图筛选（/map，企业 count / 区域数 / 点位 / 级联）**

| 入参 | 企业 count | regions | points | cascade |
|---|---|---|---|---|
| 无 | 189,115 | 30 | 100 | 30 |
| 深圳市 | **95,600**（= A0 基线） | 1 | 100 | 30 |
| searchTerm=腾讯 | 19 | 2 | 19 | 30 |
| 2025–2026 | 3,183（= 库 Year 分布 122+3,061） | 4 | 100 | 30 |
| 深圳市 + 2025–2026 | 1,564 | 1 | 100 | 30 |

**影响力 /influence**：深圳 95,600（avg 37.47）→ 深圳+2020–2026 **23,837**（与库 join 计数**完全一致**）→ 仅年份 51,809

**聚类 /cluster**：`scopedItems=200`，四桶 = 高影响力 200（Top 70.3）/ 高增长 **0（附 emptyReason）**/ 高转化率 200（Top 96.5）/ 高合作密度 200（Top 100）

**页面实跑**（playwright + 内部 mock 登录）：聚类页签已渲染真数据与供拖动排序，散点 `x/y` 由 min-max 归一化（x=合作密度、y=影响力，随真值单调）；要素比较仍是诚实空态（端点未上线，属已知缺口）

## 六、过程中修掉的**我自己写的**真 bug

`appendScope` 追加的 SQL 片段**没有尾空格** → 下游直接拼 `ORDER BY` 拼成 `?ORDER BY` → SQL 语法错误 → element 500 → **display 的分区降级把它悄悄吞成了空数组**。特征很阴：**无过滤用例全绿，只有传了过滤参数才炸**。已在 helper 上用注释钉住「每个片段必须以空格结尾」。
> 教训（建议上升为通用）：**任何「下游容灾 try/catch」都要假设它会掩盖真实故障**——这次要不是核对「库里 3,166 行 vs 接口 0 条」，一个 500 就当空态蒙过去了。

## 七、遗留 / 待你裁定

1. **KPI 区「独角兽企业 167 家」重复 5 张卡**（走查原就记的观察项）：后端 `factorCards=5`，取数与去重在视图/组装层，**不在本轮边界内**，需孔东侧确认
2. **要素比较**（`/compare`）端点仍未上线 → 仍是空态；要做的话是下一个独立叶（需要「要素 × 年度」真实序列）
3. **改动停本地未 commit**（叠在 A0–D1 未提交改动之上），走查通过后我再按叶分仓 commit
4. `tech_power` 五个分维值域 0–100、均值 49.58，**形态疑似统一分布的占位值**（同 `enterprise_score` 处境）：UI 已标「占位口径（模型输出待核验）」，建议 E��侧确认这些模型是否已上线

## 八、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 300k（估） |
| model_used | auto（CodeBuddy） |
| actual_cost | ≈ $2.2（估） |
| cost_warn | green |

ponytail: full（四个聚类维度逐个查到列级填充率、排除两份「看起来像但是假」的网络指标；带参数的 SQL 拼接 bug 是自测量与库量级不符才揪出来的，不是靠眼瞧）
