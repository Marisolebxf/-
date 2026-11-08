# TA-L2-DS13 供数侧修复方案（8 条部分可演 → 收口）

| 项 | 值 |
|---|---|
| 页面 | DS-13 全球领域人才态势（seq 243–265） |
| 触发 | R1 判定 2026-11-09：15 可演 / **8 部分可演** / 0 待开发完成 |
| 目标 | 把 243/244/250/253/256/258/259/265 的供数缺口收口，解除 ⚠️ 恢复 ✅ |
| 代码真源 | `repos/lumen-topic-py/gkx_show_service/talent_datasets.py`（行号见各条） |
| 数据源 | 久新 Doris（`ads_*` 252 表 / schema 9.14.0） |
| 硬约束 | 不补 0、不推断、不生成文案；缺测保持空数组/空态；覆盖率不达标不解除 ⚠️ |

## 0. 分类结论（先分工，再动手）

| 类型 | 含义 | 条目 | 谁能做 |
|---|---|---|---|
| **S 类 · 服务侧可算** | 库里有源，只是没算/没映射（改 Python 即可） | W1-2S（学历枚举归一）、W2-1 W2-2 W2-3、W3-1 W3-2、W4-3 W4-4、W5-1 | TA 后端（无需久新） |
| **D 类 · 久新需补采/补发布** | 库里无字段或无数据，必须上游补 | W1-1（无工程节点）、W1-2D（degree 回填）、W1-3（分类覆盖 7.9%）、W3-3 W3-4、W4-2（项目表无级别/经费 + 仅覆盖 15 人） | 久新 + TA 后端 |
| **— 已排除** | 探针证实无需修 | ~~W4-1 专利~~（6/15 人已有 19 条） | — |

## 0.1 探针结论（2026-11-09 只读实测，直连久新 Doris）

| 探针 | 结果 | 影响判定 |
|---|---|---|
| P1 `talent_classification` 节点 | 青年人才 6,918 / 专家 900 / 领军人才 100；**无「工程」节点**；分类覆盖 7,918 / 100,000 = **7.9%** | W1-1、W1-3 确认为 D 类 |
| P2 `ads_talent_experience.degree` | 非空 **25,516 人 / 48,652 行（25.5%）**；写法极不统一：`PhD` 7,857、`Ph.D.` 3,302、`Bachelor` 2,281、`Master` 2,094、`Ph.D` 1,864、`Doctor` 1,194、`PHD` 379、`master` 283、`bachelor` 402、`博士` 187 … | W1-2 主因是**大小写敏感匹配**（S 类），绝对覆盖率 25.5% 才是 D 类 |
| P3 `ads_talent_patent` | 全库 85,069 条 / 6,490 人；MVP 15 人 **6 人有 19 条**，接口返回 1/4/3/1/4/6 | **撤回**「专利全 0」，W4-1 关闭 |
| P3-3 `ads_talent_project` | MVP 15 人 9,685 条关系；表为 MVP 衍生关系表（`project_mvp_talent_relation_v1`） | 项目关系仅覆盖 15 人 |
| P4 `DESC ads_talent_project` | 列仅 `relation_type / investigator_role_codes / funded_paper_count / first|latest_evidence_year` 等，**无级别/类型/经费字段** | W4-2 确认为 D 类 |

> 探针脚本：`%TEMP%\gkx_ds13_probes.py`（单连接 + 5 次退避重试）。执行前因 `test2` 连接数超限（limit 10 / current 39，来自本地 show-py 线程本地连接）被拒，停止本地 show-py（8082）后释放，探针跑通。

## 1. W1 · 分类与学历覆盖（对应 243 / 244）

### W1-1 工程人才维恒 0（D 类，已确认）
- 探针：`talent_classification` 只有「青年人才 / 专家 / 领军人才」三个节点，**全库无「工程」类分类**。
- 结论：`engineer` 恒 0 是真实「无此分类」，非映射 bug；页面必须走空态，禁止补 0。
- 处置：久新在 taxonomy 3.x 增「工程人才」节点并回填；TA 后端届时在 `_talent_types()`（`talent_datasets.py:120-140`）补 `elif "工程" in name`（约 3 行）。
- 验收：`regions[].breakdown.types.engineer` 合计 > 0 才解除 ⚠️。

### W1-2 学历分布只统计到 401 人（S 类主因，**W1-2S 已实施 2026-11-09**）
- 探针：`ads_talent_experience.degree` 非空 **25,516 人 / 48,652 行（10 万主档的 25.5%）**，样本充足；但取值大小写与写法极不统一（见 §0.1）。
- 根因（S 类）：`_DEGREE_PATTERNS`（`talent_datasets.py:45-56`）用小写关键词 + `degree LIKE %s`（L59-71）**大小写敏感**，`PhD` / `Ph.D.` / `Master` / `Bachelor` / `PHD` / `doctor` 等主流写法全部落空，只剩 `博士` 等少数命中 → 博士只算出 401。
- 修法 S（P0，服务侧已落地）：`_degree_level_sql()` 改 `LOWER(degree) LIKE %s`；模式补 `ph d` / `d.phil` / `dr.` / `md` / `m.d` / `m.a` / `m.ed`。**未加裸 `ms` / `bs` / `ba`**——无分隔符的双字母关键词会误伤（如 `Systems` 含 `ms`、`mathematics` 含 `ma`），故只收带点号写法，避免把学士误升硕士。
- 实测（2026-11-09 本地 8082，同一 SQL 新旧 CASE 对跑）：全库有学历 25,516 人，档位人数 **旧 3/2/1/未识别 = 1,093 / 397 / 408 / 23,618 → 新 = 21,688 / 1,561 / 624 / 1,643**；global dataset 24 城市 `breakdown.education` **doctor 401 → 7,537、master 179 → 680、bachelor 233 → 341**（`types` 与其余字段无变化）；四端点 200（region 575.6KB / profile 380.4KB / recommend 508.9KB 命中缓存）。
- 修法 D（P1，久新）：`degree` 回填到全量主档（当前 25.5%）。
- 验收：归一化后 24 城市 `breakdown.education` 三项合计 ≥ 该城市「有学历证据人才」的 90%（实测 24 城三档合计 8,558，`phdRatio` 由医生数/有学历证据人数得出，北京 0.8777）；页面标注「ORCID 自报口径，覆盖 N 人」；绝对覆盖率随 D 类回填提升，不宣称 100%。
- ⚠️ 口径提示：`PhD student` / `PhD candidate` / `Postdoctoral` 等原文本同样命中博士档（沿用旧口径未收窄），若客户要求「已获学位」口径需另立判定（D 类）。

### W1-3 人才类型覆盖不足（D 类，已确认）
- 探针：分类覆盖 **7,918 / 100,000 = 7.9%**；现状 `types` 合计 3,254 / `value` 19,102 ≈ 17%。
- 处置：久新扩 `talent_classification` 覆盖（目标 ≥60%）与海外标签口径；TA 后端不加兜底。
- 验收：`types` 合计 / `value` ≥ 60%，否则 243/244 维持 ⚠️。

### W1-4 产业级联缺二级层级（C 类）
- 现象：`regions[].industries` 是一级平铺字符串数组，页面要求「一级产业 → 二级产业」级联。
- 处置：契约 v1.5 明确 `industryTree`（或 `regions[].industryTree`）结构；久新提供产业两级分类与「城市 × 二级行业」计数。
- 验收：级联选二级后点位/KPI 有命中；无命中显示空态（不回落一级）。

## 2. W2 · 顶尖机构洞察（对应 250，**全部 S 类**）

| 子项 | 现状 | 修法 | 验收 |
|---|---|---|---|
| W2-1 关联专家空（0/20） | `talent_datasets.py` 把 `rep_rows` 过滤成 `tid in mvp_ids and tid in talent_ins` → 只有 15 名富画像人才，几乎落不到 20 家机构 | **已实施 2026-11-09**：改为「Top20 机构在册人才 × `h_index` 降序取 Top3」，`h_index` 为 0/空者不入代表 | 实测 **20/20 机构非空、合计 60 人**（每人 ≤3，`field` 有中文标签） |
| W2-2 核心成果空（0/20） | 硬编码 `[]` | **已实施 2026-11-09**（口径修正）：库里**没有机构级成果表**（`ads_institution_research_achievement` 等均不存在），且前端 `TalentTopInstitution.coreAchievements` 是 **`string[]`** 纯文本渲染（`InstitutionDetailDrawer`）→ 用「`ads_institution_yearly_metrics` 2025 年论文 + 同比」与「`ads_institution_discipline_profile` Top1 学科论文/人才」两条**可核对事实**，不写生成式文案 | 实测 **20/20 机构非空、每机构 2 条**；结构化条目（title/venue/citedBy）需前端改类型，暂缓 |
| W2-3 学历结构只有博士 | 仅聚合 `degree='博士'` 得 `doctorCount` | **未做（阻塞前端）**：前端 `TalentTopInstitution` 只有 `doctorCount/phdRatio`，**无 `education` 三档字段**，后端出数也不会渲染；需前端加字段 + 抽屉渲染后同批做 | 三档均有字段；机构详情抽屉三档可渲染 |
| ⚠️ 机构专利数为采样值 | `topInstitutions[].patents` 取自 `ads_institution_patent`，实测 **2,861 家机构恰为 20 条**（该表每机构最多存 20 条） | 页面显示的「专利 20 件」是**截断值，不是真实总量**；本轮未修，建单 **G-DS13-07**（久新补全量专利或改走 `ads_institution_profile` 聚合列——该表无 `patent_count`） | 机构专利数 ≤ 真实值且不出现大面积同值 20 |

## 3. W3 · 最新动态（对应 253 / 256）

### W3-1 三类型（S 类）
- 现状：`talent_datasets.py:638-656` `type` 硬编码 `media`，数据只取 `_media_feed()`（`ads_talent_media_report` 30 条）。
- 修法：新增统一活动流组装，四型并列（`media` 保留）：

| type | 数据源 | 字段映射 |
|---|---|---|
| `academic` 学术发布 | `ads_talent_research_achievement`（MVP 15 人共 232 篇） | title / year / venue / cited_by_count / fulltext_url |
| `position` 职位变动 | `ads_talent_experience`（start_year + position + institution + is_current） | 取近 3 年异动，title 为「机构·职位」 |
| `project` 创新项目 | `ads_talent_project` | title / year / 资助方 |
| `media` 媒体报道 | `ads_talent_media_report`（现状） | 保持 |

- 验收：`activityFeed[].type` distinct ≥ 4；页面类型筛选每型有点位，且条数与后端计数一致。
- ⚠️ **枚举与前端不一致（2026-11-09 核源码）**：前端筛选下拉是 `paper / job / project / award / event`（`fieldConfig.ts` 的 `activityTypeOptions`），**没有** `media`，也没有 `academic/position`。后端若按上表枚举出数，用户在下拉里选任何类型都筛不到。开工前必须先把枚举改成前端这 5 类（media 只能并进 `event`/`award` 或由前端新增筛选位）→ 归入「契约先定」批次，本轮**不做**。

### W3-2 来源字段（C 类 + S 类）
- 现状：`summary=publisher`、`detail=canonical_url`，无规范来源字段；253 要求「来源」。
- 修法：契约增 `source`（机构/期刊名）与 `sourceUrl`（可校验链接）；缺失留空串，页面显「来源待核」。
- 验收：`source` 非空率 ≥ 90%（media/academic），`sourceUrl` 可 200 访问或为空。

### W3-3 时间精度不足（D 类）
- 现象：`research_achievement` 只有 `year`，`experience` 只有 `start_year`；无法支撑 256 的「近一周 / 近一月」。
- 处置：久新补 `published_at`（论文）与 `event_date`（异动）到日粒度。
- 验收：`activityFeed` 中 30 日内事件 ≥ 5 条且带完整日期；否则 256 维持「1–6 月播放器」口径，不宣称为周/月窗。

### W3-4 媒体流时新性（D 类）
- 现象：30 条，最新 2026-02-12，距演示日 2026-11-09 已 9 个月。
- 处置：久新日更采集（`source_confirmed` 门槛保持），目标近 30 日 ≥ 5 条。
- 验收：`max(published_at)` 距当日 ≤ 30 天。

## 4. W4 · 成果与影响力（对应 258 / 259）

### W4-1 专利计数（**已排除，不修**）
- 探针：`ads_talent_patent` 全库 85,069 条 / 6,490 人；MVP 15 人中 **6 人有专利共 19 条**，接口实际返回 `patents.total` = 1 / 4 / 3 / 1 / 4 / 6（其余 9 人为真实 0）。
- 结论：原「专利全 0」判断有误并撤回；258 的专利部分已可演，不建缺口（用例 258 行已同步更正）。

### W4-2 项目分项全 0（D 类，已确认）
- 探针：`DESC ads_talent_project` **无 `project_level` / `project_type` / `funding_amount` 字段**，只有 `relation_type`、`investigator_role_codes`、`funded_paper_count`、`first/latest_evidence_year`；且该表是 MVP 衍生关系表（`metric_definition_version=project_mvp_talent_relation_v1`、`match_method=mvp_funded_paper_authorship`），**项目关系只覆盖 15 人**。
- 处置：久新在项目主表补「级别 / 类型 / 经费」字段并发布 10 万人级项目关系；TA 后端 `talent_datasets.py:1507-1508` 再补聚合映射。
- 验收：`projects.national + international ≤ total` 且 > 0；非 MVP 人才也有项目关系（覆盖 ≥60%）。

### W4-3 学科热度 `fieldHotness`（S 类，纯计算，**已实施 2026-11-09**）
- 现状（修前）：硬编码 0。
- 实现（口径按可用数据收敛）：`ads_talent_yearly_discipline` 按 `field_id` 聚合「人才年度学科论文量」→ 增速 =（2024–2025 均值 / 2019–2021 均值 − 1）→ 全 26 个学科内取**分位**（0 最低、1 最高）。人才 `fieldHotness` = 其论文最多学科的分位。
- ⚠️ **量纲更正**：前端按 **0–1 小数**使用（`ProfileBasicPanel` 里 `fieldHotness × 100` 显示），mock 也是 0.62–0.95；原方案写的「映射 0–100」有误，已改。
- 实测：15 人取值 **0.28 / 0.32 / 0.48 … 0.96，13 个不同值**，非全 0 且有区分度。

### W4-4 热点契合度 `hotspotAlignment`（S 类，纯计算，**已实施 2026-11-09**）
- 实现：`100 × Σ(本人该学科论文占比 × 该学科热度分位)`；无年度学科记录者置 0（NO_DATA，不臆造）。
- 实测：15 人 **43.5 – 83.2**，分项可解释（「研究领域越贴近全库增长最快的学科，分越高」）。
- 验收：同 W4-3；tooltip 给口径，不给百分比进度。

### W4-5 `ifAvg`（暂不修）
- 无期刊影响因子源，维持 0 并在分项行标「无源」，本轮不纳入。

## 5. W5 · 国际合作表（对应 265，S 类，**已实施 2026-11-09**）

- 现状（修前）：`internationalCoop` 硬编码 `[]`；`overseasVisits/overseasExchanges` 无源（期望即空态，不修）。
- 实现：`ads_talent_collaborator` JOIN 合作者现机构 `ads_institution_profile` 取 `country_code / country_name`，**过滤 `CN` 与空国别**（空国别 1,513 条合作者关系无法断言境外，丢弃不猜），按国家聚合：
  - `country` 取机构国名，缺名回落国家码（如 `US`）；`project` 只写「论文合作」这一事实类型（无项目实体源，不编项目名）；`role` = 「共同作者」；`org` = 该国合著最多的 2 家机构；`period` = 首末合作年；`outcome` = 合著/合作项目/共同专利的**事实计数**
  - 每人按合著数降序取 6 行
- 实测：**15/15 人有行、合计 90 行**（每人 5–6 行；样例：US「合著论文 196 篇 · University of Pennsylvania / Duke University · 2015-2025」）。
- 验收：15 人中 ≥10 人有 ≥1 条；无则空态；不得用国内合作顶替。

## 6. 契约 v1.5 增补项（C 类，先定后写）

| 字段 | 变更 |
|---|---|
| `activityFeed[].type` | 固定枚举 **`paper / job / project / award / event`**（对齐前端 `activityTypeOptions`；原稿 `academic/position/media` 与前端不匹配，作废） |
| `activityFeed[].source` / `sourceUrl` | 新增；缺失空串 |
| `topInstitutions[].coreAchievements` | **维持 `string[]`**（前端纯文本渲染），内容为可核对事实统计；结构化条目（title/year/venue/citedBy）作为 v1.6 可选，需前端改类型 |
| `topInstitutions[].education` | 新增 doctor/master/bachelor 三档（前端类型需同步加，否则不渲染） |
| `topInstitutions[].patents` | 明确为**全量**口径（现为 `ads_institution_patent` 每机构 ≤20 条采样，见 G-DS13-07） |
| `regions[].industryTree` | 新增两级产业树（或明确保持平铺并取消级联要求，需产品裁定） |
| `talents[].patents/projects` 分项 | 明确 national/international/fundingWan 的统计口径 |
| `talents[].internationalCoop` | 已定（2026-11-09 实施）：`country / project / role / org / period / outcome`，境外 = 合作者机构 `country_code` 非空且 ≠ `CN` |

## 7. 排期与依赖

| 批次 | 条目 | 依赖 | 解除行 |
|---|---|---|---|
| **P0（服务侧，无需久新）** | ~~W1-2S~~、~~W2-1~~、~~W2-2~~、~~W4-3~~、~~W4-4~~、~~W5-1~~（**6 项均已完成 2026-11-09 本地验证，待发版**）；阻塞：W2-3（前端无 `education` 字段）、W3-1（枚举与前端不匹配 + 无日/月粒度）、W3-2（前端无来源列） | 契约 v1.5 字段形状确认（W2-3 / W3-1 / W3-2 需前端同批） | 250、258（项目分项除外）、259、265；243 学历口径随 W1-2S 发版生效 |
| **P1（久新配合）** | W1-1、W1-3、W1-2D、W3-3、W3-4、W4-2 | 久新 taxonomy/degree/日期/项目字段 | 243、244、256、258 |
| **P2（产品裁定）** | W1-4 产业级联；W4-5 暂不修 | 产品确认是否保留级联要求 | 244 |

## 8. 统一复验脚本（每项修完跑一次）

```powershell
$t=(Get-Content "$env:USERPROFILE\.gkx\display-loop-token" -Raw).Trim()
$h=@{Authorization="Bearer $t";systemCode="display"}
$g=(Invoke-WebRequest "https://edu.itic-sci.com/tid/api/display/v1/talent/global/dataset" -Headers $h).Content|ConvertFrom-Json
$p=(Invoke-WebRequest "https://edu.itic-sci.com/tid/api/display/v1/talent/profile/dataset" -Headers $h).Content|ConvertFrom-Json
# 断言示例
$g.data.regions | ForEach-Object { $_.breakdown.types.engineer } | Measure-Object -Sum
($g.data.activityFeed | Group-Object type | ForEach-Object { "$($_.Name)x$($_.Count)" })
$g.data.topInstitutions | Where-Object { $_.representatives.Count -gt 0 } | Measure-Object
$g.data.topInstitutions | Where-Object { $_.coreAchievements.Count -gt 0 } | Measure-Object
$p.data.talents | Where-Object { $_.internationalCoop.Count -gt 0 } | Measure-Object
$p.data.talents | ForEach-Object { $_.academicInfluence.fieldHotness } | Measure-Object -Minimum -Maximum
```

> 注：文档落盘（本方案）后，DS-13 用例文末「缺口建单 G-DS13-01~06」为本方案的编号映射来源；修复交付时按 §8 断言回填用例「数据情况」列，达标才从 ⚠️ 改 ✅。
