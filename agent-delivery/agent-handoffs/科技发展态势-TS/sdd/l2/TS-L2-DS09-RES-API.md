# TS-L2-DS09-RES-API · 研究领域分析 · 后台接口设计

> **任务**：`TS-L2-DS09-RES-API`（definition，不写业务代码）
> **日期**：2026-11-06 · **作者**：agent:zcode 会话代跑 api-agent（子智能体链路故障，主会话按授权链代写；监管人 `human:王梓真`）
> **状态**：草案，待四角色会签 · **硬依赖**：`sdd/l2/TS-L2-DS09-RES-ARCH.md` 已落盘（与其冲突时改本分册不改调用链）
> **约定沿袭**：OV/KEY 两组分册——信封 R\<T\>（code 0 / 401 / 403 / 500，**本页禁 501**）、各块按 sort_no ASC、空块带 empty_reasons、列名以 RES-DATA 分册 DDL 为终准、文案/阈值/模板由表行携带（Java 不硬编码）

---

## 1. 端点总表（本二级 1 读端点 + 1 既有导出复用）

| 方法 | 服务内路径 | 网关路径 | 需规叶 | 消费表 | 读/写 |
|---|---|---|---|---|---|
| GET | `/v1/situation/planning/research-analysis` | `/display/v1/situation/planning/research-analysis` | 191–196 全部 | `ts_plan_research_*` 11 表 + KEY 组 `ts_plan_key_area_plan`（196 只读引用） | 读 |
| POST（既有） | `/v1/situation/export/jobs` | `/display/v1/situation/export/jobs` | 195 报告下载 | M1 §3.8 导出任务中心（`content_key=planning-research-intelligence`，建议值） | 写（建任务，既有端点零新增） |

复用 OV 组 `PlanningController`（U1 裁定：统一 `planning` 前缀单 Controller，本页只加 `researchAnalysis()` 方法，零新路由）。Query：**无**（本页一次取全 + FE 本地筛选联动，沿 KEY 先例；领域/主体/时间窗/规则档位切换均为 FE 状态，复算系数由 time_factor/overlap_rule 表行下发）。

## 2. 响应 DTO 定稿（平铺 12 块，块名与 ARCH §0/§6 逐字对齐）

```json
{
  "code": 0,
  "data": {
    "fields": [
      { "field_key": "ai", "field_label": "人工智能", "sort_no": 1 }
    ],
    "companies": [
      { "company_id": "C-TARGET", "name": "深圳先进技术研究院", "role": "target", "color": null,
        "level_tag": null, "metric_id": null, "empty_reasons": null },
      { "company_id": "C-01", "name": "华为技术", "role": "compare", "color": "#1f6feb",
        "level_tag": "S", "metric_id": "M_INNOV_RES_CI_LEVEL" }
    ],
    "overlap_matrix": [
      { "company_a": "深圳先进技术研究院", "company_b": "华为技术",
        "overlap_score": 72, "level": "high",
        "related_fields": ["人工智能", "集成电路"], "metric_id": "M_INNOV_RES_OVERLAP" }
    ],
    "overlap_rules": [
      { "rule_key": "strict", "label": "严格规则", "prompt": "…", "threshold_high": 75,
        "threshold_medium": 60, "threshold_low": 59, "rule_source": "…", "scope_text": "…" }
    ],
    "time_scopes": [
      { "scope_key": "1y", "scope_label": "近1年", "factor": 0.82, "sort_no": 1 }
    ],
    "level_cards": [
      { "grade_key": "lead", "grade_label": "领先级", "description": "…",
        "threshold_low": 80, "patent": 2100, "papers": 3200, "top_papers": 180,
        "score": 92, "metric_id": "M_INNOV_RES_GRADE" }
    ],
    "overlap_benchmarks": [
      { "name": "华为技术有限公司", "score": 82, "metric_id": "M_INNOV_RES_OVERLAP" }
    ],
    "competing_enterprises": [
      { "company_id": "C-01", "name": "华为技术", "level_tag": "S",
        "avg_overlap": 63.5, "pairs": [
          { "counterpart": "腾讯科技", "overlap_score": 58, "source_tag": "overlap" },
          { "counterpart": "阿里巴巴", "overlap_score": null, "source_tag": "empty",
            "empty_reason": "no_seed_pair" }
        ], "metric_id": "M_INNOV_RES_CI_COMPARE" }
    ],
    "graph": {
      "truncated": false, "node_count": 14, "edge_count": 13, "follow_up": null,
      "categories": [
        { "category_key": "enterprise", "category_label": "企业" },
        { "category_key": "institution", "category_label": "机构" },
        { "category_key": "tech_field", "category_label": "技术领域" },
        { "category_key": "literature", "category_label": "文献" },
        { "category_key": "patent", "category_label": "专利" }
      ],
      "nodes": [ { "node_id": "N-01", "node_name": "深圳先进技术研究院", "category_key": "institution",
                   "symbol_size": 46, "x": 320, "y": 300 } ],
      "edges": [ { "edge_id": "E-01", "source": "N-01", "target": "N-02", "relation": "关联" } ]
    },
    "intelligence_rows": [
      { "row_id": 1, "field": "AI大模型", "competition": "领先布局", "priority": "高",
        "evidence": "…", "regional_insight": "…", "action": "…", "plan_id": "a", "metric_id": null }
    ],
    "report_export": { "content_key": "planning-research-intelligence", "default_format": "doc",
                       "template_source": "ts_plan_research_report_template" },
    "strategy_advice": { "mode": "derived",
                         "sections": ["tech_route", "resource_config", "cooperation"],
                         "plan_source": "key-area plans", "metric_id": null },
    "caliber_note": "重叠度真值对 6/15；无真值对显示空（演示算法哈希已废弃）；阈值与档位为建议值待 M0 终冻",
    "metric_ids": ["M_INNOV_RES_OVERLAP", "M_INNOV_RES_GRADE", "M_INNOV_RES_CI_LEVEL", "M_INNOV_RES_CI_COMPARE"]
  }
}
```

逐字段说明与来源列（列名**以 RES-DATA 分册 DDL 为终准**）：

| 块 | 来源表 | 说明 |
|---|---|---|
| fields | `ts_plan_research_field`（5 行） | 领域字典（ResearchTab L53 常量表行化） |
| companies | `ts_plan_research_company`（7 行） | 目标主体 1（role=target，level/color NULL）+ 六企 6（role=compare；level_tag S/S/A/A/A/B 挂 CI_LEVEL 草稿） |
| overlap_matrix | `ts_plan_research_overlap`（6 行） | **真值对**（值域 45–72）；15 对中 9 对无行 → FE 矩阵对应格显空「—」，接口不造值（G-B4） |
| overlap_rules | `ts_plan_research_overlap_rule`（3 行） | strict 75/60/59 · balanced 70/55/54 · wide 65/50/49（逐字表行下发） |
| time_scopes | `ts_plan_research_time_factor`（3 行） | 近1年 0.82 / 近3年 1 / 近5年 1.12（筛选下拉 + 复算系数双职责） |
| level_cards | `ts_plan_research_grade`（4 行） | 四档逐字（lead 92 / advantage 76 / catching 58 / potential 34）+ threshold_low 80/65/45/0（**U3 建议值，标 draft 待 M0**） |
| overlap_benchmarks | `ts_plan_research_overlap_benchmark`（3 行） | 华为 82 / 腾讯 67 / 大疆 48（gauge 兜底 + 196 合作机会拼接源） |
| competing_enterprises | company + overlap 行，Java 现算 | 每企 avg_overlap = 该企全部**有值对**均值（确定性现算，非 mock 非模型）；pairs.source_tag ∈ overlap\|empty；metric_id=CI_COMPARE 草稿 |
| graph | graph_node（14）/ graph_edge（13） | 见 §3 U9 降级；categories 定名取实义（demo「专家」名实不符勘误，专家类留位不灌） |
| intelligence_rows | `ts_plan_research_insight`（4 行） | 195 报告列表 + 196 三节派生源（plan_id a/b/c/b） |
| report_export | `ts_plan_research_report_template`（6 行）元数据 | 下载建任务 `POST /v1/situation/export/jobs`（body 含 content_key + 行筛选参数），响应 `job_id` 回填 `report_ref`；模板文案表行携带（含 {target}/{compare}/{field} 占位符），Java/Python 不硬编码 |
| strategy_advice | 派生块（G-B3 方案 A） | 无新表；tech_route=insight 行 action/regional_insight、resource_config=insight.plan_id→KEY 方案行 resourceGap/expectedEffect、cooperation=benchmark 行拼接；三节文案 FE 按模板渲染，接口只下发 mode/sections/plan_source |

`caliber_note`：**物理行源 = `ts_plan_research_report_template` 的 rendered 侧或 `ts_plan_research_grade` 侧不适用**——本页为整页级口径说明，落 `ts_plan_research_report_template` 增 1 行 `section_key=page_caliber` 模板行携带（RES-DATA 分册落列，避免 Java 硬编码）。

## 3. U3 / U9 落册

- **U3（四档标签 + 阈值）**：标签与阈值由 `level_cards` 块下发（字典行，Java/FE 不硬编码）；`threshold_low` 80/65/45/0 为**建议值**，响应字段带 `"draft": true` 语义（由表行 draft 列携带）；「自定义阈值」V1 = overlap_rules 三档预设下拉（读面），无 PUT 写面。
- **U9（图谱降级）**：graph 块常带 `truncated / node_count / edge_count / follow_up` 四字段——节点 ≤100 且边 ≤300 时 `truncated=false` 全量下发；超限时 graph 块只返 `{ "truncated": true, "node_count": N, "edge_count": M, "follow_up": "M2 §3.1" }`（**不下发 nodes/edges**），FE 跳转/懒加载 M2 §3.1 图谱接口。阈值常量由 `report_template` 的 `section_key=graph_limit` 模板行携带（100/300），非 Java 硬编码。

## 4. G-B4 与 193 现算语义

- **G-B4（哈希废弃）**：`overlap_matrix` 只含 6 真值对；FE `getDeterministicOverlap` / `getPairOverlapCompute` 哈希兜底分支在接线单**移除**（model 文件属接线文件族，.vue 零改动——ARCH §5 已列，需会签确认）；无值对显「—（暂无重叠数据）」。复算口径（领域匹配 ×1.08/×0.96 + time_factor 系数）保留为 FE 确定性计算，系数全部来自 time_factor/overlap_rule 表行。
- **193 象限现算**：`competing_enterprises.avg_overlap` = 表行有值对均值（算式：`AVG(overlap_score) OVER 有值对`，Java 内存计算，可复现可断言）；四象限轴线标签与象限名为 FE 既有呈现，接口不下发。

## 5. metric_id 回填规则（M1 纪律沿袭）

- 回填值**逐字取四条草稿号**：overlap_matrix/overlap_benchmark→`M_INNOV_RES_OVERLAP`、level_cards→`M_INNOV_RES_GRADE`、companies.level_tag→`M_INNOV_RES_CI_LEVEL`、competing_enterprises→`M_INNOV_RES_CI_COMPARE`；fields/graph/intelligence_rows/report_export/strategy_advice 恒 NULL；顶层 `metric_ids` 四条去重。
- **禁取** Q010–Q019 / QPOL-* / Q-TINDEX-01；**禁点** `M_SYNTH_COLLAB_*` / `M_SVC_GRAPH_*` / `M_ENT_*` / `M_CHAIN_*` 伪 8 件套；全部标注「赋号草稿·未签·pending 唐绍祖」。
- 回填时点 = 批 4 冻结由 `BE-TS-CONTRACT-02` 落契约正文；物理行源 = 各表 metric_id 列（RES-DATA 落列）。

## 6. FE 接线差异清单（拼装层 + model 兜底，.vue 零改动）

| # | 改造点 | 文件 |
|---|---|---|
| 1 | dataset 中 Tab3 相关字段改为从 `research-analysis` 端点响应组装（12 块映射到既有 dataset 键：companies/overlapMatrix/overlapRuleProfiles/researchLevelCards/researchOverlapBenchmarks/researchGraphNodes/regionalPlanningInsightRows/timeScope…） | `src/api/situation/techDevelopmentPlan.ts` |
| 2 | **移除** `getDeterministicOverlap` 与 `getPairOverlapCompute` 的哈希兜底分支；无值对显空；复算系数改读响应块 | `src/models/techDevelopmentPlanModel.ts`（接线文件族，ARCH §5） |
| 3 | 195 下载改走导出任务中心（建任务 → job_id → 轮询取文件），废弃 FE Blob `downloadHtmlAsWord`；PDF 沿浏览器打印 | 同上两文件族 |
| 4 | 196 战略 Modal 数据源改 strategy_advice 派生块 + intelligence_rows.plan_id → plans 映射 | 同上 |
| 5 | graph 图例文案对齐 categories 下发（页面 DOM 零改动优先，仅数据侧） | model 层 |

## 7. 契约 §3.8 改约 delta（供批 4 冻结单列）

1. graph 边界「6 节点 6 边」→「实测 14 节点 13 星型边 + U9 truncated 降级字段」；2. `fields` 单行混排（field_key+research_grade+overlap_score）→ 拆 fields/level_cards/overlap_matrix 三块；3. `competing_enterprises.intelligence_level/score` → level_tag/avg_overlap（现算）+ pairs 明细；4. `intelligence_report` 单对象 → intelligence_rows（4 行）+ report_export（content_key=planning-research-intelligence）；5. 新增 strategy_advice 派生块（G-B3 方案 A）；6. 契约 §4 表 #6：`ts_plan_research_field` 沿用改形（领域字典 5 行）、`ts_plan_compete_intel` 弃用、拆 11 表；7. 新增 overlap_rules/time_scopes/overlap_benchmarks 三块；8. caliber_note 整页口径由模板行携带。

## 8. 合规自检

调用链前端→Java REST→只读 ADS ✅（无 Python 运行时依赖）；**本页禁 501** ✅（错误码仅 401/403/500，无模型未注册话术）；D18 ✅（全部读表、文案/阈值/模板表行携带、无直返 mock、9 空对不造值）；诚实标注 ✅（caliber_note/draft 阈值/empty_reasons）；导出不另造通道 ✅（M1 §3.8 既有端点）。

## 9. 会签重点（请四角色裁定）

1. **G-B3 方案 A**（strategy_advice 并入响应）终板；2. **G-B4 model 文件改动边界**（.vue 零改动、model 属接线文件族）；3. 契约 delta 8 条；4. U3 阈值 draft 语义 / U9 truncated 字段设计；5. `competing_enterprises.avg_overlap` 现算口径（有值对均值）。
