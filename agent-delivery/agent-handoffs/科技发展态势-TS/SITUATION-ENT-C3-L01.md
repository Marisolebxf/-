# SITUATION-ENT-C3-L01 · `POST /v1/situation/influence` 实现（enterprise_score 占位）

> **任务**：科技全域态势·企业维度跑通 C3 叶（U1/U2）——element 只读榜单端点 + display 聚合端点
> **角色**：`agent:api-agent` · 监管人：`human:李伟`（长任务授权，授权句已生效）
> **状态**：`backlog → claimed → in_progress → integration`（AV-1 目标态，待人工签收）
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md) · 契约 **v1.2** [SITUATION-ENT-API-CONTRACT-01.md](./SITUATION-ENT-API-CONTRACT-01.md) §2
> **倚前端叶**：[C1 点位](./SITUATION-ENT-C1-L01.md) / [C2 接线](./SITUATION-ENT-C2-L01.md)（均 integration）
> **挂接**：WBS §4.3（WBS-05-18-04） · 2026-10-27

---

## 一、⚠️ 先说一个契约修正（本叶最重要的产出之一）

契约 **v1.1 §2 把 `/influence` 响应写成了 `{count, averageScore, items[]}`**，与冻结的 `types/situation.ts` **不一致**——真实类型是 `InfluenceDataset`：

```
{ analyzableFactorCount, cards[]: InfluenceCard, defaultFactorType, totalCount }
InfluenceCard = { factorType, factorLabel, count, averageScore, rank, rankScope, source, items: InfluenceItem[] }
InfluenceItem = { factorType, name, score, rank, rankScope, regionKey }
```

按 U5「lumen 现实现为真源」，本叶**以 `types/situation.ts` 为准重写契约 §2 并 bump 到 v1.2**。**教训：契约草案若靠人脑简化现有类型，必错——应直接核 TS 定义。**（前端结构仍零改动。）

派生字段语义也按 demo `buildInfluenceAnalysisDataset` 实现：`analyzableFactorCount = cards.length`、`totalCount = Σ card.count`、`defaultFactorType = 最高分卡的 factorType`。

## 二、交付内容

### 2.1 element 侧：`GET /v1/element/enterprise/influence`（`@Inner`）

参数 `limit`（默认 50，硬顶 200）/ `city` / `district` / `name`（企业名模糊）。
返回：`{ scoredCount:int, averageScore:number|null, records[]:{ rank:int, name, score, regionKey }, total:int }`。

- 榜：Top-N `score_total DESC` + `org_id` 兜底稳定排序；`score` 保留 1 位小数（对齐 demo 语义，**数值真实**）
- `scoredCount` / `averageScore` 与榜单**用同一套 args 与同一个 filter**（口径必须一致，否则 count 与 items 打架）
- 无名 / 无分不进榜；[aggregate] 为空时 `averageScore` 出 `null`（未知≠0）
- **只在确有数据源的维度上过滤**：城市 / 区县 / 企业名。时间（注册年份）与领域维度分数表无落筛列，**不过滤**且不假装已过滤

### 2.2 display 侧：`POST /v1/situation/influence`

装配 `InfluenceDataset`（单张企业卡），Feign `enterpriseInfluence(limit, city, district, name)`（`@NoToken` ↔ `@Inner` 配对）。

**过滤器支持矩阵（诚实声明，写在 javadoc 与契约 §2）**

| 入参 | 生效 | 依据 |
|---|---|---|
| `searchTerm` | ✅ | 企业名 LIKE |
| `activeRegionKey` | ✅ 部分 | 以「市」结尾→城市；「区/县」结尾→区县；其余值忽略 |
| `enabledFactorKeys` | ✅ | 非空且不含 `enterprise` → 企业出局（空 cards，非降级） |
| `timeRange` / `selectedFieldValues` / `regionPaths` | ❌ 未应用 | 分数表无对应落筛列 |

**其余 10 要素不生成空卡**（count=0 的空卡会造出空 UI 区块）——与 `/map` factorItems「11 个 chips 全列出、其余 0」的约定不同，按 cards 结构语义处理。

## 三、自测证据（本地 element :7082 + display :7099）

### 3.1 display 六用例（2026-10-27 18:0x，请求体 `charset=utf-8`）

| 用例 | HTTP | cards | count | avg | items | total | default |
|---|---|---|---|---|---|---|---|
| `{}` 默认 | 200 | 1 | **189,115** | **37.78** | 50 | 189,115 | enterprise |
| `activeRegionKey=深圳市` | 200 | 1 | **95,600** | 37.47 | 50 | 95,600 | enterprise |
| `activeRegionKey=南山区` | 200 | 1 | **16,039** | 37.78 | 50 | 16,039 | enterprise |
| `searchTerm=京泉华` | 200 | 1 | **2** | 55.67 | 2 | 2 | enterprise |
| `enabledFactorKeys=["paper"]` | 200 | **0** | — | — | — | 0 | null |
| `enabledFactorKeys=["enterprise"]` | 200 | 1 | 189,115 | 37.78 | 50 | 189,115 | enterprise |

- Top-N 与 A0 / C1 基线一致（京泉华 70.3 / 宝鹰建设 69.7 / 东莞捷荣 68.0）。
- 深圳 95,600 与直连库计数**完全一致**；区县与姓名过滤均与 SQL 侧结果对齐（element 单独自测同时覆盖）。
- 原始 JSON 类型核对：`"analyzableFactorCount":1`、`"totalCount":189115`、`"count":189115`、`"averageScore":37.78`、`"rank":1`、`"score":70.3` —— **全为数字未被转成字符串**。

### 3.2 降级演练（停 `gkxlumen-element`，最终产物包）

```
DEGRADED HTTP=200 cards=0 analyzable=0 total=0 default=null
```
结构完整、诚实空态、不 5xx（分区降级铁律）。

### 3.3 单测

element 模块既有 `EnterprisePointsAssemblerTest` **7/7 绿**（本叶未新增测试的说明见 §五）。

## 四、过程中发现并修正的真实缺陷

1. **漏传参数导致 500**：聚合查询写成 `dao.one(sql)` 少了 `args.toArray()` → 任何带过滤参数的请求都是 500（`No value specified for parameter 1`）。
   **只有不带默认参数的路径是绿的**——这正是「Happy Path 自测通过 = 真通过」的错觉：单测比例为极例起到的作用反而是**暴露**它。修复后三种过滤全部 200，并在注释里写明「聚合与榜单必须同 args 同 filter，否则 count 与 items 口径打架，比报错更难发现」。
2. **PowerShell 5.1 请求体编码坑**：默认按 ASCII 发 JSON body → 中文变 `??`，表现为「城市/区县/搜索过滤全部为空」。加 `ContentType 'application/json; charset=utf-8'` 后正常。**这是自测工具的坑，不是产品 bug**，但极易被误判为后端不过滤——已记为 D1 走查前置提示。

## 五、给 D1（前端切换）的输入

1. **响应即 `InfluenceDataset`**：**api 层无需做结构映射**，`defineApi<SituationInfluenceParams, InfluenceDataset>` 直接可用；mock 与 real 两侧形状一致。
2. **`defaultFactorType` 可能为 `null`**（无数据 / 被过滤掉 / 降级），前端若有 `cards[0].factorType` 的默认值假设，需在 api 层兜底（不动视图）。
3. **未生效的过滤器要如实告知用户**：`timeRange` / `selectedFieldValues` / `regionPaths` **后端未过滤**（数据源无落筛列）。前端若展示「已按时间/领域筛选」会误导——建议在 api 层记录，或走查时作为**已知缺口**接受（不假装过滤是底线）。
4. **其余 10 要素无卡**：影响力 Tab 只会看到企业一张卡，这是诚实结果（不像 demo 那样十来张卡）。
5. **占位口径**写在 `source` 字段里随数据返回：「企业评分表 enterprise_score（占位，正式影响力算法未上线）」，`M_INNOV_ENTERPRISE_INFLUENCE` 的 D4 保持 mock 不翻转。
6. **自测提示**：用 curl/Postman 发中文 body 时注意 UTF-8 编码，否则会误判「过滤不生效」。

## 六、本叶改动清单（git）

| 文件 | 类型 | 说明 |
|---|---|---|
| `gkxlumen-element/src/main/java/.../EnterpriseController.java` | 改 | 新增 `/influence` 端点（占位口径 javadoc + `numifyCount`），修复漏传 args 缺陷 |
| `gkxlumen-display/src/main/java/.../feign/RemoteElementClient.java` | 改 | 新增 `enterpriseInfluence`（`@NoToken`） |
| `gkxlumen-display/src/main/java/.../controller/SituationController.java` | 改 | 新增 `POST /influence` + `buildInfluenceCards` / `enterpriseInScope` / `toNum` + 常量（含 `ENTERPRISE_INFLUENCE_SOURCE` 占位声明） |
| `SITUATION-ENT-API-CONTRACT-01.md` | 改 | **bump v1.2**：纠正 influence 响应结构 + 过滤器支持矩阵 |

> ⚠️ 工作区仍有前序任务未提交改动，`gkxlumen-element/pom.xml`（C1 的 surefire）、C1/C2 文件亦未 commit；按人工验收闸门**全部停本地**。

## 七、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 150k（估，含 500 根因排查与重启轮询） |
| model_used | auto（CodeBuddy） |
| actual_cost | ≈ $1.1（估） |
| cost_warn | green（<$10） |

ponytail: full（默认 / 城市 / 区县 / 搜索 / 要素过滤 / 降级 6 组全跑并与直连 SQL 交叉核对计数；500 缺陷追到根因并加回归注释，未绕过）
