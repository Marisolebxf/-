# SYNTH L2 · 要素册 — 区域创新要素分析（ARCH/DATA/API/METRIC 合并册）

- 日期：2026-11-05（v1.0.6：三方会签意见落盘；v1.0.5 会签退回。当前 8 张改落 ADS；四维不计入本期、不记已覆盖；删规划句）
- 状态：**DRAFT，第一轮退回后改稿，待复审**
- 上游：总册 §2.2/§11（v1.0.5-draft）；需求真源 SRS 136–138；类型/层次/领域同核 `M_SYNTH_187_1`–`M_SYNTH_189_1`，综合 `M_SYNTH_190_1`。这四项不顶替序号 137 的四维打分
- 现状衔接：FE ELEM 三页已联调中（`LUMEN-INTEL-FE-ELEM`）；后端未建——本册即要素后端实现依据。**FE 非终态**：四维区块（`ElementsWorkbenchView.vue` 386–）设计态=缺失态+红问号（137② blocked）；现网若仍挂演示快照属待清差距，见 §7。

## 1. ARCH（流程与落点）

```text
lumen-ui-topic 要素三页（在途，差距见 §6）
  → gateway → gkxlumen-topic（快照）/ topic-async（任务）
  → GET /topic/v1/synth/elements/batch-snapshot
  → POST /topicAsync/topic/v1/analysis/tasks → POST /internal/v1/synth/jobs/execute
  → entan-py 装包
       指标结果：读 demo_gkxlumenx_ads / gkxlumenx_ads 的 synth_elem_*（当前 8 张；succeeded 最新批）
       要素全景：真实 DWD 汇聚（装包内聚合，无表）
       四维：本期不读表。evaluationDimensions=[] + reason=metric_not_registered
```

- 同核：`M_SYNTH_ELEM_INDEX` ≡ `M_SYNTH_190_1`；类型 ≡ `M_SYNTH_187_1`；层次 ≡ `M_SYNTH_188_1`；领域 ≡ `M_SYNTH_189_1`。同核只算一处。
- 贡献路径优先已有 SPEC `M_SYNTH_ELEM_CONTRIB`；E-02 未闭禁因果表述。
- **序号 137 四维 = 本期不覆盖**：`M_SYNTH_ELEM_FOUR_DIM_SCORE` 未注册、公式未定稿 → **不建表、不灌数、不出数**，不计入当前 8 张，不写成设计落位齐，不写成照册可满足需规。类型/层次/领域不能顶替这四维。FE 四维区块只显示缺失态+红问号。
  - 以后若要做，须先由 `human:唐绍祖` 定稿五要素并完成注册，再新建 ADS 表 `synth_elem_four_dim_score`。候选方向只供其参考，本册不写表结构、不当实现依据。

## 2. DATA（表 · 每表四项）

库：`demo_gkxlumenx_ads` / `gkxlumenx_ads`。灌数方 entan-py。读取：`GET /topic/v1/synth/elements/batch-snapshot`，装包只读下列 8 张。公共列见总册 §11.2。

**当前必建 8 张**

| 表 | 业务粒度（一行=） | 唯一键（`uk_` 基础=region+compare+window+batch） | 写入方式 | 读批 |
|---|---|---|---|---|
| `synth_elem_index` | 区域×对比×窗 综合指数 | 基础键 | 实算/预填整批 | succeeded 最新单行 |
| `synth_elem_type_score` | 基础 × 要素类型（七类）× **指标（INDEX/SCORE 两行）** | `+ (metric_id, type_code)` | 同上 | 同批 ≤14 行 |
| `synth_elem_level_score` | 基础 × 结构层次（七结构）× **指标（INDEX/SCORE）** | `+ (metric_id, level_code)` | 同上 | 同批 ≤14 行 |
| `synth_elem_domain_score` | 基础 × 产业领域 | `+ (domain_code)` | 同上 | 同批 N 行 |
| `synth_elem_indicator` | 基础 × 分项 | `+ (indicator_code)` | 同上 | 同批 N 行 |
| `synth_elem_weight` | 基础 × 透镜 × 维度 × `weight_profile_code`（本期只有 `EQUAL`） | `+ (lens_code, dim_code, weight_profile_code)` | 预填 `is_mock=1`。没有行就 null+reason。装包不得直接填 1/3 | 同批 N 行 |
| `synth_elem_contrib` | 基础 × 要素×靶点 | `+ (element_code, target_code)` | 实算优先（已有 SPEC） | 同批 N 行；空 → 列表空 |
| `synth_elem_rank` | 对比范围每城市 | `+ (rank_city_code)` | 同上 | 同批全城市 |

> type/level 唯一键说明：INDEX 与 SCORE 是同一类型维下两个 metric_id，故唯一键必须含 `metric_id`，一行=一个 metric_id 的一个值（`value_num` 装指数，`value_json` 可装得分明细），**不再一行承载两个 id**。
> 本期权重方案只有 `EQUAL`。seed 把等权行写入 `synth_elem_weight`。装包只读已灌行。

**要素全景（136）：无表，装包真实 DWD 汇聚（v0.4 用户裁定）**

| 项 | 值 |
|---|---|
| 落点 | **无表**：DWD 有实数，Python 装包时真实聚合查询，不做 gapfill、不建结果表 |
| 粒度 | 装包返回 `panorama[]`：要素类型（企业/机构/人才/资金/空间）× 计数 × 关键明细 TopN（按稳定 ID=org_id 等源侧主键去重） |
| 聚合口径 | 各要素类型计数 SQL 与明细字段在装包函数内实现，引用 `calc-logic` 源表清单；禁随机数、禁 0 填充 |
| **DTO 契约（`panorama[]`）** | 每元素：`{element_type(企业/机构/人才/资金/空间), total_count, top_n:[{id,name,key_metric,value}]}`；请求参数：`page_size`（TopN，默认 10）、`element_types`（缺省全部）；响应带 `total_count`。本期只有 TopN 与 `total_count` |
| 挂载 | `ElementResult.panorama[]`（需在 MOCK-INV 契约同步登记——实现时回写） |
| 性能 | 首版直接查 DWD；若默认三元组查询超时，再议缓存表（另裁定，本册不预支） |
| 消费方 | 要素全景卡（136）、装包前置校验 |

预填范围：默认三元组。本期 DDL 只有上面 8 张 ADS 表。`synth_elem_four_dim_score` 不在本脚本。

## 3. API（参数/异常/空态）

- 快照 `GET /topic/v1/synth/elements/batch-snapshot?region=&compare=&window=&page_size=&element_types=`：200 同构 `ElementResult`（MOCK-INV §1）**+ `panorama[]`（本册 §2 DTO；`page_size` 默认 10、`element_types` 缺省全部——判定为扩展快照 API，不新增独立路由；MOCK-INV 回写列入实现单）**；404 非默认三元组；缺数据 200+null/reason。
- 任务：`analysisType=region_innovation_elements`（`POST /topicAsync/topic/v1/analysis/tasks`）；Java Adapter → Python `POST /internal/v1/synth/jobs/execute`。
- `evaluationDimensions`：固定 `[]` + `reason='metric_not_registered'`。序号 137 四维本期不出数。
- 报告：**前端基于真实快照渲染出 PDF**（同协同册 §3.3 模式，复用既有渲染能力）；`*_report` 任务键 v1 不依赖。
- 五阶段文案逐字用 MOCK-INV §2 要素行；三透镜 URL 参数沿用 FE。

## 4. METRIC（挂接/就绪度）

| metric_id | D1 | D4 | 落表 |
|---|---|---|---|
| `M_SYNTH_ELEM_INDEX` | aligned | mock | `synth_elem_index` |
| `M_SYNTH_ELEM_TYPE_INDEX` / `M_SYNTH_ELEM_TYPE_SCORE` | aligned | mock | `synth_elem_type_score` |
| `M_SYNTH_ELEM_LEVEL_INDEX` / `M_SYNTH_ELEM_LEVEL_SCORE` | aligned | mock | `synth_elem_level_score` |
| `M_SYNTH_ELEM_DOMAIN_INDEX` | aligned | mock | `synth_elem_domain_score` |
| `M_SYNTH_ELEM_INDICATOR` | aligned | mock | `synth_elem_indicator` |
| `M_SYNTH_ELEM_WEIGHT` | aligned | mock | `synth_elem_weight` |
| `M_SYNTH_ELEM_CONTRIB` | aligned | mock | `synth_elem_contrib` |
| `M_SYNTH_ELEM_RANK` | aligned | mock | `synth_elem_rank` |
| `M_SYNTH_ELEM_FOUR_DIM_SCORE` | 未注册 | — | 本期无表。接口只回 `[]`+`reason=metric_not_registered`。不顶替 187–189 |

开放项 `Q-SYNTH-02 / E-01 / E-02` 🟡 不拍板；口径引用 `calc-logic/SYNTH/*.md`。D4 改 live：实算成功后 data-agent 逐条登记批次。

## 5. 观测与可追溯

- FE 埋点 `synth_elem_*`；装包日志记 batch_id/缺行数；不可变 `snapshotId`（含 `calc_batch_id`）可回查；`cache_key` 仅作条件最新索引；表 COMMENT 登记血缘。

## 6. 验收条件

1. 快照/任务契约同 §3；`evaluationDimensions` 恒为 `[]`+`reason='metric_not_registered'`（137② blocked 回归项；解锁四步完成后方可断言切换）。
2. 缺行 null+reason+confidence。权重无行时不得填 1/3。
3. 只读 succeeded 批（自检断言）；重跑新批不覆盖。
4. 三透镜/贡献路径/排名区块各有表供给；**四维区块在 137② 解锁前不接任何数据源**（页面缺失态+红问号，验收=确认无演示数据泄漏）；无「表建了无图消费」或「图有块无表供」。
5. 五阶段文案逐字一致。

## 7. 页面差距审计（FE ELEM 现状 vs 需规，v0.3 新增）

| 需规模块 | FE 现状（实码核对） | 差距 | 改造项 |
|---|---|---|---|
| 136 全景汇聚 | 页面无独立全景区（要素以三透镜呈现） | 需规要求"形成要素全景数据库"的可视消费 | 工作台加「要素全景」Tab 或卡片（读快照 `panorama[]`=装包真实 DWD 汇聚，禁演示 fixture；分类筛选+统计卡）——**新增模块**，产品确认形态 |
| 137① 类型/层次/领域评价 | 三透镜 Tab 已有 | 无 | — |
| 137 四维打分 | 区块已有，现挂演示快照 | 本期不覆盖 | 去掉演示快照。验收=缺失态+红问号。本期不接表 |
| 138 贡献路径 | 贡献列表已有 | 接真表 | `contributions[]` 接 `synth_elem_contrib` |

## 8. 实现单/文件边界（并行分配）

| 动作 | 仓/文件 | 归属 |
|---|---|---|
| 当前 8 张 ADS DDL + 预填（index/type/level/domain/indicator/weight/contrib/rank）。全景无表。四维不在本脚本 | `lumen-algo-py/scripts/mysql/synth_elem.sql` + seed | data/算法并行线 2 |
| 装包（elements 分支；四维固定 `[]+reason`；只读 8 张 ADS） | `vendor/entan-py` | 线 2 |
| Java 白名单+Adapter elements 键 | `lumen-svc-platform` gkxlumen-topic-async-service（扩 `LUMEN-INTEL-BE-1` 或新认领） | 线 2 api |
| FE 四维接线 + 全景模块新增 | `lumen-ui-topic` ElementsWorkbench 等 | 线 2 前端（§7 改造项） |

## 9. 会签

| 角色 | 状态 |
|---|---|
| 架构 | 已签-架构（2026-11-05）：**可签**。当前 8 张 ADS + 四维不建表不出数（`[]`+`reason=metric_not_registered`）、全景 DWD 真查无表，符合 D18/D16 边界；137② 诚实 blocked 不记已覆盖。保留意见 AR-8（全景 DWD 聚合性能首版直查、超时再议缓存另裁定——建议预约定 timeout 阈值）与待确认 TC-3 见 `agent-delivery/agent-handoffs/LUMEN-INTEL-SDD-SIGNOFF-L01.md`，不挡签 |
| 算法 | 已签-算法（2026-11-05）：**可签**（137② METRIC-OPEN 注册：唐绍祖牵头，仍为独立外部依赖）。装包读表与 calc-logic 一致性核对通过：要素等权（`EQUAL` 1/3×3）由 seed 灌 `synth_elem_weight`（`is_mock=1`），装包只读已灌行、缺行 null+reason 禁直接填 1/3；三透镜同核 `M_SYNTH_ELEM_INDEX`≡`M_SYNTH_190_1`、类型/层次/领域 ≡`M_SYNTH_187_1`–`189_1` 只算一处、贡献路径优先已有 SPEC `M_SYNTH_ELEM_CONTRIB` 且 E-02 未闭禁因果，符合算法规约。137② 本期不建表不灌数不出数（`evaluationDimensions=[]`+`reason=metric_not_registered`）、187–189 不顶替四维——合规，不触碰唐绍祖锁定闭包，不涉 -合规/-合理 成对改名；候选方向仅供其参考。**保留意见**：①METRIC-OPEN 定稿（公式五要素）解锁前四维区块不得接任何数据源；②全景聚合口径（计数 SQL+明细 TopN 按稳定 ID 去重）在装包函数内实现、引用 calc-logic 源表清单，禁随机数禁 0 填充 |
| 数据 | 已签-数据（2026-11-05）：**可签**。DDL 清单核对通过：要素 8 张 ADS（index/type_score/level_score/domain_score/indicator/weight/contrib/rank）落 `demo_gkxlumenx_ads`/`gkxlumenx_ads`，唯一键基础=region+compare+window+`calc_batch_id`、type/level 另含 `metric_id`+`type_code`/`level_code`（INDEX 与 SCORE 同表不碰撞），公共列与血缘 COMMENT 齐；`synth_elem_four_dim_score` 不在本期 DDL。全景无表（真实 DWD 汇聚，用户裁定不走 gapfill）符合 D16 边界——未在 `gkxlumenx_gapfill` 新造表；预填 `is_mock=1`。**保留意见**：①AR-4 批次清理建议（按 `calc_batch_created_at` 保留最近 3 批、保护 batch_meta 引用批）适用本册 8 表，DDL 单落地时写入任务定义，不另开表；②全景 DWD 直查性能须按 AR-8 预约定 timeout，避免首屏拖慢 |
| 产品 | 未签（产品行见总册会签表：TC-3 136 全景模块形态待确认不挡会签、超时降级可接受；Q-SYNTH-02/E-01/E-02 🟡 角标策略同总册） |

## 10. 修订

| 版本 | 日期 | 说明 |
|---|---|---|
| v0.1 | 2026-11-04 | 首版骨架 |
| v0.2 | 2026-11-04 | 评审修复：每表四项、137② 决议+决策人+API 契约、权重缺行不套等权、快照表四项、观测/验收、文件边界 |
| v0.3 | 2026-11-04 | 第二轮审核修复：137② 升方案 A（METRIC-OPEN 注册+建表，过渡期可追溯推导演示行，不返回裸 []）；panorama 移 `gkxlumenx_gapfill` 且唯一键补条件上下文；权重口径实核 calc-logic（等权 1/3×3 主口径，`weight_source='calc_logic_placeholder'`）；报告=前端真快照渲染 PDF；新增 §7 页面差距审计（136 全景模块=FE 待新增项） |
| v0.4 | 2026-11-04 | 第三轮收敛：panorama 撤 gapfill 改真实 DWD 汇聚（DWD 有实数，用户裁定）；DDL 收敛为 9 张 `_ai` 指标结果表 |
| v0.6 | 2026-11-04 | 第五轮审核收敛：137② 改 blocked（不建 gapfill 表不出数，解锁四步定义）；panorama 补 DTO 契约（panorama[] 结构/page_size/element_types/total_count，首版 TopN 不深分页） |
| v1.0 | 2026-11-05 | 对齐总册 v1.0-draft：清「四维过渡推导 / panorama 演示行 / placeholder_equal」残留；权重码统一 `EQUAL`；头部版本对齐 |
| v1.0.2 | 2026-11-05 | P2：实现清单改为「当前 8 张 + 解锁后第 9 张四维」 |
| v1.0.4 | 2026-11-05 | 观测：`snapshotId` 不可变含批次；`cache_key` 条件最新索引（对齐总册 v1.0.4） |
| v1.0.5 | 2026-11-05 | 会签退回：8 张改落 ADS；删「DDL 9 张」、page_token、未来官方权重、缺行填 1/3；137② 不记已覆盖 |
| v1.0.6 | 2026-11-05 | 三方会签意见落盘：算法可签（等权装包/同核只算一处合规，137② METRIC-OPEN 仍为外部依赖）；数据可签（8 张 DDL 清单/唯一键/gapfill 边界齐、AR-4 清理建议适用）；产品行指向总册（TC-3 确认不挡会签） |

