# 人才产研结构对比（M_TALENT_UI_IR_SPLIT）

> **类型**：RATIO（结构占比）｜ **域**：科技人才态势·全球领域人才态势｜ **UI 挂载**：科技信息展示系统 → 全球领域人才态势 → 分布洞察视图·产研对比分析（ECharts 分组柱图，系列「科研」「产业」，`InsightPanel.jsx` / `DistributionInsightView.jsx`）
> **数据支持度**：**部分支持**｜ **公式定义人**：仿王惠（SRS 有叶有名，未给学术/产业判定口径）｜ **口径归属**：SRS 叶「产研对比分析」有名无口径
> **复现脚本**：`code/M_TALENT_UI_IR_SPLIT.py`｜ **产物**：`code/M_TALENT_UI_IR_SPLIT_out.json`
> **四判定摘要**：直接结构 = 无（无现成产研分类结果面）；直接数据 = 无；依赖结构 = 是（履历/高校/院所表链齐全）；依赖数据 = 部分（产业侧无机构类型字典，只能减法代理）
> **数据源口径**：本件支持度按「开发库 + 三方库（gkx，183.240.141.251:3318 只读）」评估，仅排除 `demo_*`；live 库（111.198.38.90:34306）本件未用到，库存行数真源为 `_work_gkx21/GKX_INVENTORY.json`。

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 两库均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库与三方库（gkx）**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别（`gkx` 或 `gkxlumenx_*`），只写「开发库」视为未调研三方库，闸门判 FAIL。

**本件判定：部分支持。** 学术侧依赖链（学者→在任履历→机构名→高校表/院所表）在 gkx 结构完整、数据量足（高校 20,000 行、院所表 JOIN 命中 61 人）；产业侧没有机构类型字典字段可直分，只能「在任有机构名池 − 学术侧」的减法代理，误差方向明确但不可消除 → 部分支持。升档触发器见 §1.6。

## 摘要

SRS 叶「产研对比分析」（seq 251）要求展示学术界与产业界人才分布对比，但两份需求真源均未给出计算口径；UI 在 `InsightPanel.jsx:131` 用双柱分组图呈现（系列「科研」「产业」），数据来自 `data.js:1161` 的硬编码 mock。本件以「在任履历机构名是否命中高校/院所表」推测定义学术侧，用减法代理产业侧，实跑 gkx：在任且有机构名学者 **17,668** 人中，学术 **8,499**（48.1039%）、产业代理 **9,169**（51.8961%）、产业/学术比值 **1.0788**。学术链路可复现性高，产业代理是主要降档原因。

## 一、需求定义概述

### 1.1 所属功能模块

科技人才态势 → 全球领域人才态势 → 分布洞察视图（洞察分析面板：华人占比 / 地区分布 / **产研对比** / 热点流入流出）。所属四级功能为 1.1.1.1.4.3 科技人才态势（SRS excel_rows 246–332）。

### 1.2 为什么需要本指标

人才工作从「有多少」进阶到「在什么部门干活」：学术界与产业界的分布对比回答区域创新体系「研究型人才与开发型人才的配比」，是引进决策（挖学术骨干还是产业专家）与政策评估（产研融合政策是否起效）的共同输入。UI 把它放在洞察面板，与华人占比、地区分布并列，构成「Who（华人）— Where（地区）— Which sector（产研）」的洞察三联。

### 1.3 需求文档是否给出定义方法

**需求文档没给出定义方法。** SRS 叶「产研对比分析」（seq 251，excel_row 254）原文只要求「展示学术界与产业界人才分布对比」；主需求文档《科技信息展示系统和科技专题服务系统.md》检索「产研对比」0 命中。学术界/产业界如何判定（按现职机构类型？按论文署名？双重身份算谁？）没有任何说明，本件走推测定义路径。

### 1.4 类似指标权威方法可行性分析概要

官方统计口径中，国家统计局《中国科技统计年鉴》将 R&D 人员按「企业 / 研究与开发机构 / 高等学校」三大执行部门分组（2023 年公报口径成熟稳定，R1）；科技部《中国科技人才发展报告（2020）》同样按部门分析人才布局并指出「科技人才整体加速向东部聚集」（R2）。方法论补强：学界对机构类型归属的标准做法是从履历/论文的机构署名标准化后映射到机构类型（机构名标准化是公认难点，R3）。本件数据侧对应：履历机构名 → 高校表/院所表精确等值，与官方「执行部门」三分法同构，但库内缺「企业」字典只能减法。方法族对照见附录 C。结论：可行，产业侧精度受字典缺失限制，须降档交付。完整版见附录 C。

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/talent-trend/components/InsightPanel.jsx:131` — `irOption` 系列 `name: '科研'`（`:136` data: irSplit.research）与 `name: '产业'`（`:148` data: irSplit.industry）双柱；x 轴 labels = 5 个技术领域（人工智能/生物医药/新材料/通信技术/高端制造）。
- mock 源：`repos/demo-ui-science/src/pages/talent-trend/data.js:1161` — `generateIrSplit()` 返回 `industry: [45, 32, 28, 35, 40]`、`research: [55, 68, 72, 65, 60]`（5 领域硬编码随机值）。
- SRS：`bid-reference/srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md` seq 251（excel_row 254）——「产研对比分析」。

### 1.6 推测原意与推测定义

**推测定义（非甲方闭合口径）**：以学者最近在任履历的机构类型判定其属于学术界或产业界，报告两集合人数与占比。

- 学术侧：$A = \{s : \exists\, \text{在任履历},\ \text{org\_name\_en} \in \text{高校表} \cup \text{院所表}\}$；
- 产业侧（代理）：$I = \{s : \text{在任且 org\_name\_en 非空}\} \setminus A$；
- 展示口径：$p_A = |A|/(|A|+|I|)$，$p_I = |I|/(|A|+|I|)$，比值 $r = |I|/|A|$。

**降档/升档触发器（写死）**：库内若上线「机构类型字典」（企业/院所/高校三分类，含统一社会信用代码映射），产业侧按字典直分 → 升「完全转换支持」；若甲方认定按「论文署名活跃部门」判定，需另建论文级机构类型推断件，与本件并列、不替换。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md` |
| 所属四级功能 | 1.1.1.1.4.3 科技人才态势（excel_rows 246–332，87 叶） |
| 所属页面 | 1.1.1.1.4.3.1 全球领域人才态势（23 叶，excel_rows 246–268） |
| 本件最近叶 | 产研对比分析（seq 251，excel_row 254） |
| 相邻叶 | 华人占比分析（seq 248 → CHINESE_RATIO 件）/ 人才分布信息查看（seq 243 → DENSITY_TIERS 件）/ 人才迁徙情况展示（seq 252 → MIGRATION_FLOW 件） |
| 本件性质 | 洞察面板数字位（有名无口径）；批 2 五件组之一 |

## 二、计算过程

### 2.1 装载与规模校验

以 `_gkxdb.py` 为唯一入口连接 gkx，`SET NAMES utf8mb4` 后先对账规模：主档 `dwd_scholar` = 21,316（与批 1 及 `GKX_INVENTORY.json` 零漂移）；在任履历学者 17,723（83.1441%，快照键复核）。**collation 归一必须做**：`dwd_forg_university_org_info.name_std` 与 `dwd_scholar_work_experience.org_name_en` collation 不同，直接等值报 1267 错误，两列均 `CONVERT(... USING utf8mb4) COLLATE utf8mb4_general_ci` 后比较（20261021 轮踩坑，共享快照有记录）。

### 2.2 口径池：在任且有机构名

分母池取「在任（`is_current=1`）且 `org_name_en` 非空非空串」的 distinct 学者 = **17,668**。比在任全量 17,723 少 55 人（机构名缺失），这 55 人无法做任何机构类型判定，从两桶中同时排除——分子分母同池（B3 纪律），不允许出现「产业分母含无机构名者」的混基。

### 2.3 学术侧：高校与院所两跳

高校表精确等值命中 **8,438** 人；院所表 `dwd_research_institute_base_info` 以 `name_en = org_name_en` 同法 JOIN 命中 **61** 人。两表名称空间按构造不相交（高校名 vs 院所名），学术合计 $A = 8{,}438 + 61 = 8{,}499$。

```sql
-- 学术侧（高校）
SELECT COUNT(DISTINCT we.scholar_id)
FROM gkx.dwd_scholar_work_experience we
JOIN gkx.dwd_forg_university_org_info u
  ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci
     = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
WHERE we.is_current = 1 AND we.org_name_en IS NOT NULL;
-- → 8438

-- 学术侧（院所）
SELECT COUNT(DISTINCT we.scholar_id)
FROM gkx.dwd_scholar_work_experience we
JOIN gkx.dwd_research_institute_base_info i
  ON CONVERT(i.name_en USING utf8mb4) COLLATE utf8mb4_general_ci
     = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci
WHERE we.is_current = 1 AND we.org_name_en IS NOT NULL;
-- → 61
```

### 2.4 产业侧：减法代理

$I = 17{,}668 - 8{,}499 = 9{,}169$。误差方向（披露）：把「非高校非院所」全部记为产业，其中混有未收录院所与事业单位；但由于高校/院所收录以名称精确等值为准，**误差单向**（只会高估产业、不会高估学术），对「学术占比不超过一半」这一量级结论稳健。

### 2.5 派生比（全部落产物）

$p_A = 8{,}499/17{,}668 = 48.1039\%$；$p_I = 9{,}169/17{,}668 = 51.8961\%$；$r = 9{,}169/8{,}499 = 1.0788$（产业每 1 名对应学术 0.927 名）。另披露口径池相对主档的在任覆盖率 $17{,}723/21{,}316 = 83.1441\%$（快照键复核）。

### 2.6 确定性声明

全部为确定性 SQL 聚合（COUNT/等值 JOIN），无采样、无随机、无 hash 序依赖；同库同数据重跑逐位一致（B5）。两表 JOIN 的 collation 归一为幂等操作。

### 2.7 复现代码结果展示

- 代码：`code/M_TALENT_UI_IR_SPLIT.py`（运行 `python3 code/M_TALENT_UI_IR_SPLIT.py`，退出码 0，落 `_out.json`）。
- 结果：`facts = {scholar_total: 21316, current_exp_scholars: 17723, current_exp_with_org_name: 17668, academic_university_scholars: 8438, institute_matched_scholars: 61, industry_scholars_proxy: 9169, academic_total_used: 8499}`；derived 四键见 §2.5。
- 解读：学术/产业接近对半、产业略多（$r=1.079$），与我国 R&D 人员执行部门结构（企业占比过半，R1）方向一致——代理面虽然粗，量级不背离官方结构。
- **需求符合性评审**：SRS 叶要求「展示学术界与产业界人才分布对比」——本件交付双桶人数+占比+比值，满足「对比」的功能形态；未满足点：UI 的 x 轴是 5 个技术领域（领域内双柱），本件只交付全量不分领域版；领域维需要学者-领域映射（`dwd_scholar_talent_flag` 与主档仅 8.72% 交集，P4.3 断裂），列入 §四 缺口。

## 三、数据支撑情况

| 依赖维 | 库表（gkx） | 行数 | 支撑判定 |
|---|---|---:|---|
| 学者主档 | `dwd_scholar` | 21,316 | 结构+数据足（`gkx`） |
| 在任履历 | `dwd_scholar_work_experience`（is_current=1） | 21,515 段 / 17,723 人 | 结构+数据足（`gkx`） |
| 高校字典 | `dwd_forg_university_org_info` | 20,000 | 结构+数据足（`gkx`） |
| 院所字典 | `dwd_research_institute_base_info` | 见库存 | 可 JOIN（命中 61 人），字段 `name_en`（`gkx`） |
| 机构类型字典（企业侧） | — | — | **无承载**（absence_probe，`gkx`） |
| 学者-领域映射（UI 领域维） | `dwd_scholar_talent_flag` 与主档交集 | 1,858（8.72%） | 不足（P4.3 断裂，`gkx`） |

## 四、数据缺失情况

1. **机构类型字典缺失**（产业侧只能减法代理）：建议甲方提供统一机构类型字典或企业名录映射表；到位后同一脚本改字典直分，升档。
2. **领域维断裂**：UI 的 5 领域分组柱在本库无法真实出数（学者属性宇宙与主档仅 8.72% 交集）；可先上全量双柱版，领域维等属性库与主档对齐后补。
3. 可构建但存在缺口，不构成「无法构建」。

## 参考文献

1. 2023年全国科技经费投入统计公报[EB/OL]. 国家统计局、科学技术部、财政部. https://www.stats.gov.cn/sj/zxfb/202410/t20241002_1956810.html （R1，2026-10-31 WebSearch 核验可达）
2. 《中国科技人才发展报告2020》发布[EB/OL]. 中华人民共和国科学技术部. https://www.most.gov.cn/kjbgz/202109/t20210907_176742.html （R2，2026-10-31 WebSearch 核验可达）
3. External collaboration patterns of research institutions using shared publications in the Web of Science[EB/OL]. Information Development / Emerald. https://doi.org/10.1108/00330331311313753 （R3，2026-10-31 WebSearch 核验可达）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技人才态势/全球领域人才态势.md》seq 251（excel_row 254）叶名「产研对比分析」：要求展示学术界与产业界人才分布对比（功能性表述，无口径无公式）。

《科技信息展示系统和科技专题服务系统.md》（bid-reference 正本）检索记录：「产研对比」0 命中；「学术界」/「产业界」未以指标形式出现。

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 产研对比 | 主需求文档 | 0 |
| 产研对比分析 | SRS 全球领域人才态势.md | 1（叶名，无口径） |
| 学术界 / 产业界 | 主需求文档 | 0（指标语境） |

## 附录 B 历史库表探测证据

- 共享快照：`code/_snapshots/_shared_probe_talent_20261030_out.json`（批 1 建档，本件复用口径复核键；本件在任池 17,723 为 `is_current=1` distinct 口径，与快照 20,028 的「非空履历」口径不同，正文已分列）。
- 本件产物：`code/M_TALENT_UI_IR_SPLIT_out.json`（20261031 实跑）。

### B.2 本件产物逐键清单

| 产物键 | 类型 | 值 | 正文引用 |
|---|---|---|---|
| `facts.scholar_total` | 计数 | 21,316 | §2.1 |
| `facts.current_exp_scholars` | 计数 | 17,723 | §2.1/§2.5 |
| `facts.current_exp_with_org_name` | 计数 | 17,668 | §2.2/§2.5 |
| `facts.academic_university_scholars` | 计数 | 8,438 | §2.3 |
| `facts.institute_matched_scholars` | 计数 | 61 | §2.3 |
| `facts.academic_total_used` | 计数 | 8,499 | §2.3/§2.4 |
| `facts.industry_scholars_proxy` | 计数 | 9,169 | §2.4/§2.5 |
| `derived.academic_share_of_named_current_pct` | 派生比 | 48.1039 | §2.5 |
| `derived.industry_share_of_named_current_pct` | 派生比 | 51.8961 | §2.5 |
| `derived.industry_per_academic_ratio` | 派生比 | 1.0788 | §2.5 |
| `derived.current_exp_share_pct` | 派生比 | 83.1441 | §2.5 |
| `absence_probe` | 负证据 | （空数组——机构字典缺失以 §3 表格呈现；院所表 name_en JOIN 成功） | §3 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 判定依据 | 本库承载 | 贴合度 |
|---|---|---|---|---|
| 执行部门三分法（企业/机构/高校） | 国家统计局 R&D 统计（R1） | 现职单位类型 | 高校/院所字典有；企业字典无 | 高（学术侧）/中（产业侧代理） |
| 部门人才布局监测 | 科技部人才报告（R2） | 部门统计调查 | 无调查数据 | 中（方向对齐） |
| 机构署名标准化→类型映射 | R3（WoS 机构协作模式） | 机构名标准化 | 名称精确等值（弱版） | 高 |

### C.2 数据矩阵

| 依赖 | 行数 | 质量 | 缺口 |
|---|---:|---|---|
| `dwd_scholar` | 21,316 | status 单峰 | 无现职类型字段 |
| 在任履历 | 21,515 段 | org_name_en 段级覆盖 | 非高校院所不可直分 |
| 高校表 | 20,000 | country/name_std | — |
| 院所表 | 见库存 | name_en | 收录偏少（命中 61） |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v1（即期） | 全量双桶占比+比值（本件） | 无 |
| v2 | 产业侧字典直分（升档） | 机构类型字典 |
| v3 | 5 领域分组柱（UI 完整形态） | 学者属性库与主档对齐 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 产业桶混入未收录院所 | 中 | 披露误差方向；字典上线复算 |
| 领域维缺失与 UI 形态不一致 | 中 | 先上全量版并脚注披露 |
| mock 双柱读数（55/68/72…）与真实占比差异大 | 高 | UI 联调前对齐（预期行为非故障） |

### C.5 总判

**部分支持**：学术侧三条件齐；产业侧依赖字典缺失只能代理。升档触发器（机构类型字典）写在 §1.6。

## 附录 D　复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_TALENT_UI_IR_SPLIT.py` | 退出码 0，落 `_out.json` |
| 数据入口 | `_gkxdb.py` | demo_* 直接 raise |
| 判档闸 | `gate_check.py --dir 第三方库指标计算过程` | PASS |
| 正文产物一致 | `audit_md_vs_out.py --dir 同上 --max-miss 0` | miss = 0 |
| 判档一致 | `audit_verdict_enum.py` | MD 四档 = out 判档 |
| 派生还原 | `audit_derived_arith.py` | 4 键全还原 |
| mock 残留检查 | `rg "generateIrSplit" repos/demo-ui-science/src` | 正式版替换后无 KPI 引用 |

---

## 久新库回填记录（2026-11-01，jiuxin_warehouse 探针，只读实测）

> 触发：2026-11-01 三源铁律（开发库非 demo_* + gkx + 久新）落地后的缺口复查。
> 缺口族：机构类型｜回填判定：**部分回填**。

**实测事实**：
1. ads_institution_profile（83,745 行）+ ads_institution_type 字典表存在（科研机构组共 10 张 ads_institution_* 表）；人才侧 ads_talent_industry_activity（397,964 行）按 CN_GB4754 产业门类给学者产业活动计数

**对档位与数据源的影响**：产业侧「无机构类型字典可直分」的缺口可由 ads_institution_type + ads_institution_profile 补齐；学术/产业拆分可叠加久新 institutional 维度交叉验证（gkx 侧高校/院所 JOIN 命中面保留）。

**新增数据源**：`jiuxin_warehouse.gkx_technology_analysis_dev.ads_institution_profile, ads_institution_type, ads_talent_industry_activity`（只读；探针产物 `_phase2_jiuxin_probe2_out.json`）

**原则**：本段为追加记录，原正文判档、复现数字与 gkx 侧事实一律保留；后续如切换主数据源须重跑复现脚本并更新判档。
