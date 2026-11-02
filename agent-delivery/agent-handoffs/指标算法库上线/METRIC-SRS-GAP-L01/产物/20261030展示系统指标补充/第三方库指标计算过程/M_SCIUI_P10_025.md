# M_SCIUI_P10_025 科研主体时空流动路径追踪 —— 指标信息 MD

> **类型**：简单统计类｜ **域**：科技成果展示·时空演进 New·科研活动流动与协同网络·主体路径（`SpaceTimeEvolutionNewPage.jsx:1374`）｜ **UI 挂载**：科技信息展示系统 → 创新载体孵化载体 New（时空演进页）→ SectionCard「科研主体时空流动路径追踪」（主体选择器+世界地图路线+迁移明细）
> **数据支持度**：**部分支持**｜ **公式定义人**：无（轨迹口径无定义；主体=机构或研究团队而三源机构静态单址、团队无实体——仅学者维轨迹承载）｜ **口径归属**：SRS 正名功能叶（序号 509）；UI 区块同名挂载 :1374
> **复现脚本**：`code/M_SCIUI_P10_025.py`（薄壳实算，共享探针 `code/_shared_s308_laneb_probe.py`）｜ **产物**：`code/M_SCIUI_P10_025_out.json`
> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**
> **四判定摘要**：直接结构=无（无「主体×轨迹站点」现成面）；直接数据=无；依赖结构=部分（学者维双向轨迹：experience 地理时序+event 学科变迁 281,117 行；机构维静态单址 0 迁移、团队维无实体表）；依赖数据=部分（示例地理路线 18 站/学科路线 10 跳实算落产物；机构/团队整体迁移不可算）
> **数据源口径**：本件支持度按「开发库 live（10.50.11.76:3306，gkxlumenx_*，禁 demo_*/_devdb）+ 三方库（gkx，183.240.141.251:3318 只读）+ 久新库（jiuxin，Doris 47.93.119.170:29030）」三源评估。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源中存在数据量充分的相关表/字段，仅需口径转换/间接计算（无额外数据采集）即可产出本指标 |
| **部分支持** | 三源中存在部分可复用表/字段，**只可计算本指标的部分子项**（或关键维度缺失） |
| **完全不支持** | 三源均无承载，需新建数据链路/外部接入 |

**本件判定：部分支持。** 降档根因是「主体两维从缺」：SRS 509 主体=机构或研究团队——机构维经历表机构粒度多城市聚合=0（`ads_institution_profile` 83,745 行静态单址无迁移历史）；团队维三源无实体表（mock 6 团队纯编造）；学者维轨迹双向齐备（`ads_talent_experience` 140,887 行 25,434 多城市学者 + `ads_talent_mobility_event` RESEARCH_FIELD_CHANGE 281,117 行学科变迁）。主体三分维仅学者维可承载，机构/团队整体迁移关键维度缺失，判部分支持。

### 批次通用纪律摘要（S3-08 批共用）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键（附录 B 对照表） |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实 |
| B3 | 同基相除/相减 | 事件类型占比=同表分子分母（94.2% 注记） |
| B4 | 负结论带探针 | 机构 0 迁移/团队无表/轨迹词族 0 命中留证 |
| B5 | 确定性 | 事件序列按 event_year 排序；站点按 start_year |
| B6 | 闸门自身被闸 | 不自跑闸门；派单方统一跑 |
| B7 | 产物只由脚本产出 | 薄壳实算脚本重跑产出 |
| B8 | 回执不复收 | 实算读数可重跑复验 |
| B9 | 单位/日期陷阱 | start_year 可 NULL（COALESCE 排尾部）；is_current 无结束年 |
| B10 | 口径裁定保守交付 | 三主体维并列（学者可算/机构从缺/团队从缺），触发器写死 §1.6 |
| 基期三键 | base_years_used/missing/note | 产物全键 |

### 判档自检三问（本件 = 部分支持）

| 问 | 答 | 证据 |
|---|---|---|
| 判定轴存在吗？ | 部分 | 学者维轨迹双面有；机构/团队维无 |
| 代理轴可信吗？ | 部分 | 学者经历时序可绘制路线；机构聚合=0 城市迁移 |
| 子盘能撑多少？ | 一维 | 学者粒度地理+学科双路线可切真；机构/团队整体迁移全 mock |

## 摘要

「科研主体时空流动路径追踪」是时空演进 New 页协同网络区 SectionCard（`SpaceTimeEvolutionNewPage.jsx:1374`）：Select 主体选择器（`RESEARCH_SUBJECTS` 16 项：10 机构/载体+6 团队）+ `WorldEvolutionMap` route 线（`:1390`）+ 迁移路线明细列表（`:1397-1415`，末站红框标注）。mock 侧仅 6 团队带 `trajectory`（3-4 站年份+城市+事由，`mockData.js:81-139`），机构/载体项 `getSubjectRoute` 返回空数组——**UI 自身即只对团队型主体画线**。数据侧判定：**部分支持**——SRS 509 需规「用户选择机构或研究团队，支持基于时间轴自动绘制其地理迁移和学科变迁路线」。机构维：经历表机构粒度多城市聚合=0（机构无地理迁移承载，profile 静态单址）；团队维：三源无团队实体表；学者维：`ads_talent_experience`（140,887 行）按 start_year 排序即得地理迁移路线（示例 18 站：Paderborn 1991→…→Munich 2020~），`ads_talent_mobility_event` RESEARCH_FIELD_CHANGE（281,117 行）按 event_year 排序即得学科变迁路线（示例 10 跳：Chemistry→…→2025）——「地理迁移和学科变迁」双语义在学者粒度全通。主体三分维仅一维齐备，判部分支持。

- 需求判定：**SRS 正名功能叶**（序号 509，excel_row 512；UI 区块同名挂载）。
- 复现状态：薄壳实算已跑通；轨迹承载量+双示例路线落产物。
- 档位结论：**部分支持**（学者维轨迹双面齐备，机构/团队整体迁移从缺）。
- 关键事实：25,434 名多城市学者（27,458 多机构）可作轨迹候选主体；机构多城市数=0——机构作为「主体」无迁移可画。
- 升档路径：团队实体表入库（课题/项目团队维）或机构历史地址面 → 三维齐备升完全转换支持。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统 → 科技成果展示 → 时空演进展示（New 页族）→ 科研活动流动与协同网络可视化 → SectionCard「科研主体时空流动路径追踪」（`SpaceTimeEvolutionNewPage.jsx:1374`，extra=主体 Select 宽 260）。`:1380` 选择器 options=RESEARCH_SUBJECTS.map（label=`name（type）`）；`:1390` WorldEvolutionMap `route={{stops: subjectRoute}}` showHeat=false focus=routeFocus（自动跟随末站）；`:1397-1415` 迁移路线明细（每站 Tag 年份+城市名+事由，末站 1.5px 红框红 Tag）。数据链：`:562-563` `subject = RESEARCH_SUBJECTS.find(id)` + `subjectRoute = useMemo(getSubjectRoute(subject, year))`；`mockData.js:464-478` `getSubjectRoute`：`subject.trajectory.filter(stop.year<=year).map(city 坐标+note)`——无 trajectory 属性的主体（10 机构/载体）返回 `[]`。

mock 主体清单（`mockData.js:81-139`）：sub-01~10 机构/载体（斯坦福 HAI、MIT 合成生物中心、深圳湾实验室等，仅城市+主题+成立年，无轨迹）；sub-11~16 团队（深智大模型团队 4 站/量子材料联合团队 3 站/合成生物创业团队 3 站/固态电池攻关团队 3 站/EDA 软件核心团队 3 站/商业航天动力团队 3 站）。

### 1.2 为什么需要本指标

主体路径回答「这个机构/团队从哪里来、到哪里去、学科怎么转」：地理迁移线=资源整合轨迹（SRS 509 需规原文「实现科研协同和资源整合可视化掌控」）；学科变迁线=转型预警（传统学科→交叉前沿）。时间轴播放可追踪路径推进（`:1397`「时间轴播放可追踪路径推进」），为科技主管部门把握主体演化提供个体粒度证据。

### 1.3 需求文档是否给出定义方法

**三份说明书未给出该指标的计算方法。**SRS 序号 509 需规描述给出功能行为（选主体+时间轴+地理迁移和学科变迁双路线+导出），但无：主体的界定口径（机构/团队/是否含领军人才个人）、迁移事件的判定规则（地址变更 vs 任职变更）、学科变迁的粒度（领域/子领域/主题）。

### 1.4 类似指标权威方法可行性分析概要

权威口径方法族（完整版指向附录 C）：①OECD 科学家流动测量（个体履历法：机构时序→迁移线，与 experience 面同构）；②NSF Survey of Doctorate Recipients（机构变更事件计数，与 WORK_TO_WORK 事件同构）；③欧盟 Horizon Europe 机构参与轨迹（机构粒度项目参与时序——本库无此面，机构迁移无权威代理）。①②原料在库（experience+event 双面物化），③无承载。完整版见附录 C。

### 1.5 引用来源

1. OECD. Handbook on Measuring the Mobility of Scientists（履历法轨迹）. https://www.oecd.org/sti/sci-tech/
2. NSF. Survey of Doctorate Recipients（机构变更事件）. https://www.nsf.gov/statistics/srvydoctoratework/
3. European Commission. Horizon Europe Participation Data（机构参与轨迹）. https://erc.europa.eu/

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

- **口径 A（学者维轨迹，已实现）**：地理迁移路线 = experience 按 talent_id 过滤、start_year 排序的站点序列（city×institution×年份）；学科变迁路线 = RESEARCH_FIELD_CHANGE 事件按 event_year 排序（from_field→to_field）。
- **口径 B（机构维迁移，从缺）**：机构历史地址时序——profile 静态单址、经历表机构粒度多城市聚合=0，无承载。
- **口径 C（团队维迁移，从缺）**：团队实体表三源无（mock 6 团队纯编造）。
- **降档触发器**：若 UI 主体选择器强约束仅机构/团队两类（不含学者），则本件降完全不支持（两维均零承载）。
- **升档触发器**：团队实体表入库（课题成员组队面）或机构历史地址面（工商变更/迁址记录）→ 三维齐备升完全转换支持。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技成果展示/科技时空演进展示.md` |
| 所属四级功能 | 1.1.1.1.4.6 科技成果展示（域）|
| 所属页面 | 时空演进 New（创新载体孵化载体 New 页族）|
| 本件叶 | 序号 509 科研主体时空流动路径追踪（SRS 正名叶；UI 区块 :1374 同名挂载）|
| 相近叶 | 序号 507 科技人员流动动态可视化（P10_022/023，同根三面）；序号 510 科学家与团队协作网络分析（同组邻叶）|
| UI 容器 | `SpaceTimeEvolutionNewPage.jsx:1374-1415` SectionCard |

## 二、计算过程

### 2.1 口径裁定（B10 多口径并列）

- **口径 A（学者维轨迹，已实现）**：地理迁移（experience 时序）+学科变迁（RESEARCH_FIELD_CHANGE 流）双路线——本件判档依据（SRS 双语义在此维全通）。
- **口径 B（机构维，从缺）**：机构多城市聚合=0+profile 无历史地址——零承载留证。
- **口径 C（团队维，从缺）**：无实体表——零承载留证。
- **裁定**：A 结构+数据均足；B/C 零承载。三分维一维齐备 → 部分支持。

### 2.2 探针读数实测

```sql
-- 轨迹承载量：多城市/多机构学者（迁移候选主体）
SELECT COUNT(*) FROM (SELECT talent_id FROM ads_talent_experience
  WHERE city IS NOT NULL AND city<>'' GROUP BY talent_id
  HAVING COUNT(DISTINCT city)>=2) t;                       -- 25,434
-- 机构迁移检查：机构粒度多城市聚合（应=0）
SELECT COUNT(*) FROM (SELECT institution_id FROM ads_talent_experience
  WHERE institution_id IS NOT NULL AND institution_id<>''
    AND city IS NOT NULL AND city<>''
  GROUP BY institution_id HAVING COUNT(DISTINCT city)>=2) t;  -- 0
-- 示例地理路线（serial mover）
SELECT start_year, end_year, city, institution_name FROM ads_talent_experience
  WHERE talent_id='tal_a17f...' AND city IS NOT NULL AND city<>''
  ORDER BY COALESCE(start_year, 9999);                      -- 18 站
-- 示例学科路线
SELECT e.event_year, ff.name_en, tf.name_en FROM ads_talent_mobility_event e
  LEFT JOIN ads_discipline_field ff ON e.from_field_id=ff.field_id
  LEFT JOIN ads_discipline_field tf ON e.to_field_id=tf.field_id
  WHERE e.talent_id='tal_e2d7...' AND e.mobility_type='RESEARCH_FIELD_CHANGE'
  ORDER BY e.event_year;                                     -- 10 跳
```

实读：多城市学者 25,434 / 多机构学者 27,458 / 多城市机构 **0**；示例地理路线 18 站（Paderborn 1991→Atlanta 2001→St Louis 2004→Gießen/Giessen 2004-2007→Stanford 2007→Princeton 2007→New Haven 2008→Osnabrück 2008-2011→Berlin 2011-2020→Zurich 2014→Tromsø 2019-2023→Munich 2020~现任）；示例学科路线 10 跳（2016 Chemistry→Agricultural & Biological Sciences 起，至 2025 Biochem→Chemistry）。事件类型分布：RESEARCH_FIELD_CHANGE 281,117（94.2%）/ EDUCATION_TO_WORK 7,991 / WORK_TO_WORK 9,276。

### 2.3 读数落盘与同基核对

轨迹承载量落 `derived[0]`（学者/机构双计数同表分组，B3 同基）；地理路线 18 站落 `derived[1]`；学科路线 10 跳落 `derived[2]`；事件类型分布落 `derived[3]`（94.2%=281,117/298,384 同表分子分母）。mock 16 主体+6 团队轨迹仅作 ui_demo_fallback 披露，不混入真读数。

### 2.4 稳健性与口径敏感性

①start_year 可 NULL（首条经历无起点年，COALESCE 排序尾部）；②同名异写城市（Gießen/Giessen）未归一——路线站点数对归一敏感；③学科型事件占 94.2% 而其 from/to_location 全空（学科变迁不带地理端）——地理+学科双路线须分别取自 experience 与 event 两面再按年拼接；④assignment_confidence 提示部分事件为推断归属；⑤机构维度若以「人才流入流出序列」重定义（机构≠迁移而是人才更替），语义变为 P10_022 净流入面——口径重定义可另立指标不改本件判档。

### 2.5 基期年份可用性

`base_years_used`=[1991, 2025]（示例轨迹起止）；`missing`=[]；轨迹为个体全程时序（无全局基期）；事件面 2000-2025。note 详附录 B。

### 2.6 需求符合性预评

主体选择器可改挂学者（25,434 候选，label=姓名（机构数））+双路线切真（口径 A）；机构/团队选项维持 mock 或下线；「一键导出」为前端功能无数据依赖；学者姓名展示需脱敏/授权评估（个人信息面）。

### 2.7 复现代码结果展示

复现入口 `python3 code/M_SCIUI_P10_025.py`（薄壳直连久新实算：承载量双计数+机构零迁移断言+双示例路线+gkx 履历面行数复核）；产物 `code/M_SCIUI_P10_025_out.json`；关键读数：`derived[0]` 承载量、`derived[1]` 地理路线、`derived[2]` 学科路线、`derived[3]` 事件类型分布。

### 2.8 分步证据对照表

| 步 | MD 论断 | 产物键 |
|---|---|---|
| 1 | experience 140,887 行 / event 298,384 行 | facts.jiuxin_*_table |
| 2 | 多城市学者 25,434 / 多机构 27,458 | derived[0] |
| 3 | 多城市机构=0（机构无迁移） | derived[0].multi_city_institutions |
| 4 | 示例地理路线 18 站 | derived[1] |
| 5 | 示例学科路线 10 跳 | derived[2] |
| 6 | 学科型事件 281,117（94.2%） | derived[3] |
| 7 | gkx 履历面 57,117 行复核 | facts.gkx_scholar_family |
| 8 | 判档 部分支持 | support_judgment |

## 三、数据支撑情况

### 3.1 依赖维总览

| 依赖维 | 承载源 | 状态 |
|---|---|---|
| 学者地理时序（迁移路线） | jiuxin `ads_talent_experience` | **有**（140,887 行；city×institution×起止年） |
| 学科变迁事件流 | jiuxin `ads_talent_mobility_event` | **有**（RESEARCH_FIELD_CHANGE 281,117 行；from/to_field 双端） |
| 学科字典 | jiuxin `ads_discipline_field` | **有**（26 行 OpenAlex 四级领域） |
| 机构地理维 | jiuxin `ads_institution_profile` | **静态单址**（无历史地址——机构迁移零承载） |
| 团队实体面 | 三源 | **无表**（mock 6 团队纯编造） |
| 轨迹现成结果面 | 三源 | **无**（学者维需 experience/event 排序转换——判转换的依据） |
| gkx 履历面 | gkx `dwd_scholar_work_experience` | **备选**（57,117 行；无城市列需机构名关联） |

### 3.2 现场复核清单

UI 链实读：`SpaceTimeEvolutionNewPage.jsx:1374-1415` SectionCard（Select/Map route/明细列表）+ `:562-563` useMemo 链 + `mockData.js:81-139`（16 主体）+ `:464-478`（getSubjectRoute 空 trajectory 返 []）。久新实连复核（本件脚本）：多城市学者 25,434/多机构 27,458/多城市机构 0 断言通过；示例路线 18 站+10 跳断言通过；事件类型三分布断言通过。gkx 实连复核：`dwd_scholar_work_experience` 57,117 行、`dwd_scholar` 21,316 行。共享探针快照 `_snapshots/_shared_s308_laneb_probe_out.json`：trajectory 词族 dev 仅 sys_route_conf（系统路由）/gkx 0 命中/jiuxin 0 命中（表名层），承载在 talent 词族两表。

## 四、数据缺失情况

### 4.1 缺口清单

①机构迁移历史零承载（profile 静态单址，经历表机构粒度 0 多城市——SRS 509 主体半边从缺）；②团队实体表无（课题/项目组队面未入湖——主体另半边从缺）；③城市名归一未做（Gießen/Giessen 异写）；④学科型事件无地理端（双路线须两面拼接）；⑤学者姓名展示的脱敏/授权评估未做（个人信息面）。

### 4.2 修复建议与影响面

短期：主体选择器改挂领军人才/多段履历学者（25,434 候选）+双路线切口径 A 真数。中期：团队实体表入库（课题成员组队面）→ 团队维升档；机构历史地址面（工商变更记录）→ 机构维升档。远期：城市归一字典+双路线拼接物化视图（主体×年份×站点预聚合）。同族联动：P10_022/023 同根三面，本件补齐主体路径维后 507/509 两叶全通。

### 4.3 影响面

主体选择器 16 项中 10 机构/载体项当前 mock（且 UI 自身返空数组不画线）；改挂学者后双路线可全切真；机构/团队两项维持 mock 直至中期能力补齐。

## 参考文献

1. OECD. Handbook on Measuring the Mobility of Scientists. https://www.oecd.org/sti/sci-tech/
2. NSF. Survey of Doctorate Recipients. https://www.nsf.gov/statistics/srvydoctoratework/
3. European Commission. Horizon Europe Participation Data. https://erc.europa.eu/

# 附件

## 附录 A 原始需求原文摘录

- SRS《科技时空演进展示.md》序号 509（excel_row 512，level5=科研活动流动与协同网络可视化）：「用户选择机构或研究团队，支持基于时间轴自动绘制其地理迁移和学科变迁路线。交互式轨迹图和数据明细一键展示、导出，实现科研协同和资源整合可视化掌控。」
- bid_desc（excel_row 500，序号 497，继承行）：「支持按时间要素对论文发布、专利交易、资金与研发进度、科技人员流动等实时动态数据，进行分布展示与流动展示。」
- 检索记录：`rg 科研主体时空流动路径追踪` 三份说明书 → SRS 509 正名命中（UI 区块 :1374 同名）。
- mock 参照（`mockData.js:81-139`）：16 主体（10 机构/载体无轨迹+6 团队 trajectory 3-4 站）。

## 附录 B 本件产物逐键清单（`code/M_SCIUI_P10_025_out.json`）

metric_id/batch=S3-08/ui_evidence（5 条组件行号）/requirement_trace（named_in_srs=true + SRS 锚 509）/facts（ui_mount/ui_subjects/ui_route_builder/ui_mock_note/jiuxin_experience_table/jiuxin_event_table/jiuxin_institution_profile/gkx_scholar_family/dev_table_total=542/gkx_table_count=280/jiuxin_table_count_live=218）/derived[0]（轨迹承载量含机构 0）/derived[1]（示例地理路线 18 站）/derived[2]（示例学科路线 10 跳）/derived[3]（事件类型分布）/absence_probe（三源三条）/support_judgment=部分支持/notes（5 条）/base_years 三键/ctx_refs。

## 附录 C 可行性报告完整版（要点）

方法谱系：OECD 履历法（个体机构时序→迁移线，experience 面同构）→ NSF SDR（机构变更事件，WORK_TO_WORK 同构）→ Horizon Europe 机构参与轨迹（机构粒度——本库无此面）。数据矩阵：experience 140,887 行（25,434 多城市学者）；event 281,117 学科变迁+9,276 职务变迁；机构 0 迁移；团队无表。分期方案：一期主体改挂学者+双路线切真（口径 A）、二期团队实体表+机构地址面（三维齐备升完全转换）、三期物化视图+城市归一。风险登记：学科型事件无地理端（两面拼接）、城市异写、学者姓名脱敏评估、assignment_confidence 推断归属。总判：部分支持（学者维全通、机构/团队维零承载；降档触发器=选择器强约束机构/团队两类）。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_P10_025.py` | 退出码 0，落 `_out.json` |
| 实算复核 | derived[0] 25,434/27,458/0 | 重跑一致 |
| 判档一致 | MD 文首「部分支持」= out.json `support_judgment` | 一致 |
| 负证据 | 机构 0 迁移/团队无表/轨迹词族 0 命中 | 逐一可复验 |
| mock 披露 | 16 主体/6 团队轨迹仅 §1.1 语义描述 | 不参与支持度结论 |
