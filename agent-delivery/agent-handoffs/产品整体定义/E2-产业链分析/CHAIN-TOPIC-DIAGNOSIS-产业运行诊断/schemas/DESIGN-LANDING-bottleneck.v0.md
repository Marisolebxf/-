# 落地设计 · 瓶颈堵点识别（`bottleneck`）v0

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.1-draft |
| 日期 | 2026-08-12 |
| 作者 | `human:李伟`（架构师）+ architect-agent |
| 状态 | 落地设计收口稿；实现以本文 + 待建 GRAPH / Schema / Prompt 为准 |
| 样板依赖 | Runtime 样板键 `key_link`；本键按 ISOMORPH **同构扩展**（同对象、换健康度/角标） |
| Bid | `1.1.1.2.4.2.2.5` 瓶颈堵点及相关算法 `.3.9` |
| 产品真源 | `CHAIN-TOPIC-DIAGNOSIS` 五件套（US-05/06；IA §5.3；Wireframe §6） |
| 词汇决策 | `DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806.md` |
| Runtime 真源 | `../../系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 同构差量 | `../../ISOMORPH-chain-analysis-jobs.v0.md` §3.2 |
| 关键样板对照 | 同目录 `DESIGN-LANDING-key_link.v0.md`、`GRAPH-key_link.v0.md` |

---

## 0. 一句话

> **不换厨房，只换菜谱**：复用 Analysis Job Runtime；  
> 本键新增 `analysis_key=bottleneck` 的 Input draft、五段 Graph、健康图谱 Result、可选成因 Prompt Pack。

口诀：`chain:diagnosis:bottleneck` = 同 `industry_chain` + **健康度确定性** + **规则标瓶颈/卡脖子** + LLM 只写成因/建议。

### 0.1 命名与词汇纪律（全篇强制）

| 术语 | 含义 | 禁止混用 |
| --- | --- | --- |
| `stage_code` | Graph 过程步 | 不得表示健康分档 |
| `stage_key` | 五环节业务键 | 同 key_link |
| L1 `band` | `稳健` / `关注` / `薄弱` | **薄弱 ≠ 瓶颈** |
| L2 瓶颈 | 规则判定角标 | 不得与 L1 并格图例 |
| L2+ 卡脖子 | `瓶颈 ∧ severity=高` | 计数 ⊆ 瓶颈数 |
| 禁词 | **断链** | 本 Tab 任何 UI/字段禁止出现 |
| 维名 | 展示用「**资本**」 | 禁止用「资金」替代 Bid 面 |

---

## 1. 范围与非目标

### 1.1 本落地覆盖

| # | 交付物 | Owner |
| --- | --- | --- |
| A | 注册 `bottleneck` / `task_type` / graph | Java + Python |
| B | Create draft：五维只读包确认 | FE + Java |
| C | Graph `bottleneck.graph.v1` | Python |
| D | Result `chain.bottleneck.result_payload.v1` | Python + Java |
| E | Prompt Pack（成因/建议，可降级） | 算法 |
| F | Tab=`bottleneck` 过程壳 + 结果（图谱+详情+报告入口） | FE |
| G | 切片 S1–S5（§10） | 全栈 |

### 1.2 明确不做（v0）

- 不改 Runtime 状态机；不新造私有 Create 路径  
- 不允许前端伪编辑五维阈值/权重  
- 禁止「断链」语义与文案  
- 不把薄弱节点自动等同瓶颈  
- Progress 灰卡不得冒充「矩阵」正式结果  
- LLM 不得裁定是否瓶颈 / 卡脖子 / 健康分档  

---

## 2. 身份注册（钉死）

| 字段 | 值 |
| --- | --- |
| `analysis_key` | `bottleneck` |
| `task_type` | `chain:diagnosis:bottleneck` |
| `graph_version`（默认） | `bottleneck.graph.v1` |
| `input_schema_version` | `chain.bottleneck.input.v1` |
| `result_schema_version` | `chain.bottleneck.result_payload.v1` |
| `prompt_pack_version` | `bottleneck.annotate.prompts.v1`（可选） |
| 互斥 | 同用户 + 同 `task_type` 仅一条非终态 |
| 路由 | `/industry-center/diagnosis?tab=bottleneck` |
| 菜单兼容 | `workspace=bottleneck` ≡ `tab=bottleneck` |

---

## 3. 与关键样板的差量

| 维度 | `key_link` | `bottleneck`（本键） |
| --- | --- | --- |
| 主对象 | `industry_chain` | **同** |
| 配置 | 三因子只读 | **五维只读**（技术/人才/市场需求/资本/政策） |
| Graph 中段 | structure / score_high_end / annotate | **timeseries / score_health / annotate_bottleneck** |
| 判定 | 高端化 + 关键 | **健康度 + 瓶颈/卡脖子分层** |
| Result | 全链关键标注 | **健康图谱 + 角标 + 成因建议** |
| KPI | 关键环节数 | **瓶颈数 / 最高严重度 / 类型分布 / 卡脖子数** |
| LLM | N4c 格局趋势 | **成因/改进建议清单** |

Runtime / Harness / Snapshot / wait_view：**✅ 直接复用**。

---

## 4. 端到端主路径

```text
对比篮确认 industry_chain
  → Tab=bottleneck 五维只读确认
  → 生成分析 → POST analysis-jobs { analysis_key:"bottleneck", draft }
  → Java 门禁 → Python bottleneck.graph.v1
  → succeeded_wait_view → 显式查看结果
  → 结果：左健康图谱 + 右节点详情 → 诊断报告 SectionPanel → ENT-EXPORT
```

### 4.1 Create body 要点

```json
{
  "client_request_id": "uuid",
  "task_type": "chain:diagnosis:bottleneck",
  "analysis_key": "bottleneck",
  "draft": {
    "object": {
      "object_type": "industry_chain",
      "chain_id": "CHN-IC-001",
      "parent_industry_id": "INB1204",
      "display_name": "集成电路产业链"
    },
    "dimensions": {
      "pack_id": "diag_bottleneck_dims",
      "pack_version": "1.0.0",
      "user_confirmed": true,
      "items": [
        { "dim_key": "tech", "label": "技术", "status": "ready" },
        { "dim_key": "talent", "label": "人才", "status": "ready" },
        { "dim_key": "market_demand", "label": "市场需求", "status": "ready" },
        { "dim_key": "capital", "label": "资本", "status": "ready" },
        { "dim_key": "policy", "label": "政策", "status": "ready" }
      ]
    },
    "ui": { "route_path": "/industry-center/diagnosis", "tab": "bottleneck" }
  }
}
```

**Java 硬门禁**：

1. `object_type=industry_chain`  
2. 五维齐全且 `status=ready`；`user_confirmed=true`  
3. 拒绝阈值/权重 override；拒绝前端 `graph_version`  
4. 同 `task_type` 互斥复用  

---

## 5. Graph · `bottleneck.graph.v1`

| # | stage_code | Bid / Wireframe 可见文案 | LLM？ | 主 Artifact |
| --- | --- | --- | --- | --- |
| 1 | `freeze` | 任务提交与产业链对象冻结 | 否 | `art.context` |
| 2 | `timeseries` | 整合各环节技术/人才/资本/政策等时序数据 | 否 | `art.timeseries_bundle` |
| 3 | `score_health` | 基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度 | 否 | `art.link_health_scores` |
| 4 | `annotate_bottleneck` | 瓶颈智能识别与卡脖子环节归因/改进建议生成 | **建议可 LLM** | `art.bottleneck_bundle` |
| 5 | `validate_assemble` | 结果可信性校验与靶向方案/报告组装 | 否 | `art.result_payload` |

```text
STAGE_LABELS = {
  "freeze": "任务提交与产业链对象冻结",
  "timeseries": "整合各环节技术/人才/资本/政策等时序数据",
  "score_health": "基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度",
  "annotate_bottleneck": "瓶颈智能识别与卡脖子环节归因/改进建议生成",
  "validate_assemble": "结果可信性校验与靶向方案/报告组装",
}
```

过程 Steps **须可见四核心指标词**：技术成熟度 / 人才供给量 / 融资事件 / 政策覆盖率（**不在**结果页链级对齐表复述）。

### 5.3 节点契约（摘要）

#### N1 · `freeze`

核对 object/dimensions/versions；写 `art.context`。失败：`OBJECT_INVALID` / `DIM_PACK_UNAVAILABLE`。

#### N2 · `timeseries`

拉各环节时序事实包。时序未接通 → `honesty.timeseries.mode=replay_snapshot|unavailable`，**允许继续**（V1 可回放）；若五环节骨架缺失 → **硬失败**。

#### N3 · `score_health`（确定性）

| 项 | 内容 |
| --- | --- |
| 做 | 每 `stage_key` 算 `health_score` + L1 `band ∈ {稳健,关注,薄弱}` |
| 禁止 | LLM 改分/改分档 |
| 公式 | `GAP-CHAIN-DIAG-METRICS` 未闭合 → mock + gap_ref |
| 写 | `art.link_health_scores` |

#### N4 · `annotate_bottleneck`

```text
1) 规则：health + 时序特征 → bottlenecks[]（含 severity/type）
2) 规则：is_choke = bottleneck ∧ severity=高（QC04 正式表未出前用临时默认 + honesty）
3) LLM（可选）：成因/改进建议清单；不得改 is_bottleneck / is_choke / band
4) LLM 失败 → 空建议 + honesty.llm=degraded；判定结果仍成功
```

#### N5 · `validate_assemble`

组装 §6；双检不变量。

### 5.5 limits

与 key_link 同级即可；若启用 LLM：`llm_retry_max≥2`，`annotate_bottleneck` 节点超时 ≥120s。

---

## 6. Result Payload

```text
result_schema_version: chain.bottleneck.result_payload.v1
kpi:
  bottleneck_count
  max_severity                 # 最高严重度
  type_distribution            # 类型分布
  choke_link_count             # 卡脖子环节数（⊆ bottleneck_count）
sections:
  health_graph                 # 五节点+边 + band 底色
  link_health[]                # stage_key, health_score, band
  bottlenecks[]                # id, stage_key, severity, type, is_choke, advice_refs
  node_details                 # 点选：是否瓶颈/是否卡脖子 + 成因/建议
honesty / versions / object / metrics_used[]
```

### 6.2 结果页绑定

| UI | 字段 |
| --- | --- |
| 顶栏四 KPI | `kpi.*` |
| 左图谱 | `sections.health_graph` + L1 底色 + L2/L2+ 角标 |
| 右详情 | `sections.node_details`（与左**等高，以右为准**） |
| 图例 | **两行**：健康分档 \| 判定角标；禁止薄弱/瓶颈并格 |
| 报告 | 只读 Result → ENT-EXPORT |

### 6.3 Complete 不变量

1. 五环节齐全  
2. `choke_link_count ≤ bottleneck_count`  
3. 每个 `is_choke=true` 必须 `is_bottleneck=true`  
4. `band=薄弱` **不强制**入 bottlenecks  
5. payload / 文案 **无「断链」**  
6. `object_type=industry_chain` 与 Input 一致  
7. 展示统计带 `metric_id`  

### 6.4 Artifact → Result

| Artifact | Result |
| --- | --- |
| `art.link_health_scores` | `sections.link_health` + `health_graph` 节点属性 |
| `art.bottleneck_bundle.bottlenecks` | `sections.bottlenecks` + kpi 计数 |
| `art.bottleneck_bundle.advice` | `sections.node_details` 建议清单 |
| `art.*.honesty` | `honesty.*` |

---

## 7. Prompt Pack

| Pack ID | 节点 | 输入 | 输出 |
| --- | --- | --- | --- |
| `bottleneck.annotate.prompts.v1` | N4 子步 | 已判定 bottlenecks + 时序摘要 + 健康分 | 成因[] / 改进建议[]（禁改判定布尔） |

---

## 8. 配置与数据依赖

| 依赖 | 缺失策略 |
| --- | --- |
| 链 + 五环节 | **硬失败** |
| 五维包 | Create **硬失败** |
| 时序 ADS | 降级回放 + honesty |
| 健康/瓶颈公式（QC04） | mock/临时默认 + gap |
| LLM | 建议降级，判定不降级假成功 |

开放项：QC04、GAP-CHAIN-DIAG-METRICS、GAP-CHAIN-DIAG-SEMANTICS、DEC 卡脖子临时默认。

---

## 9. 分层职责

同 key_link：FE 不直连 Python；Java 不跑健康算法；Python 不签发 `result_snapshot_id`。

---

## 10. 切片交付（S1–S5）

| Slice | 目标 | 可验出口 |
| --- | --- | --- |
| S1 | 注册 + N1+N5 空跑 | 五段文案；对象门禁；互斥 |
| S2 | +N2 | 时序降级 honesty；五环节骨架 |
| S3 | +N3 | 每节点 band + health_score；四核心词在过程可见 |
| S4 | +N4 规则层 | KPI/角标计数一致；词汇分层校验；禁断链 |
| S5 | +LLM 建议或降级 | 点选详情；报告只读入口 |

建议落地序：ISOMORPH **#1**（紧随 key_link）。

---

## 11. 验收 DoD

- [ ] 五维未确认禁用生成；维名展示「资本」  
- [ ] wait_view 纪律；结果图谱+详情布局符合 Wireframe §6  
- [ ] L1/L2/L2+ 分层正确；薄弱≠瓶颈；卡脖子⊆瓶颈  
- [ ] 无「断链」；LLM 不裁定判定布尔  
- [ ] 未分叉私有 API；算法只在 Python  

---

## 12. 已收口决策

| ID | 决策 |
| --- | --- |
| B1 | 同构 key_link 对象与五环节骨架，换健康/角标语义 |
| B2 | 词汇分层以 DEC-BOTTLENECK-VOCAB 为准 |
| B3 | 卡脖子 = 瓶颈∧severity=高（正式 severity 表待 QC04） |
| B4 | 时序可降级；五环节骨架不可缺 |
| B5 | 统一 analysis-jobs |

---

## 13. 产物清单

| 文件 | 状态 |
| --- | --- |
| `DESIGN-LANDING-bottleneck.v0.md` | **本文件** |
| `GRAPH-bottleneck.v0.md` | 待从 §5 抽出 |
| `chain.bottleneck.input.v1.schema.json` | 待建 |
| `chain.bottleneck.result_payload.v1.schema.json` | 待建 |
| `PROMPT-PACK-bottleneck-annotate.v0.md` | 待建 |
| `openapi-analysis-job.v0.yaml` | 补丁：`BottleneckStageCode` + draft oneOf |

---

## 14. 会签栏

| 角色 | 签字 | 日期 |
| --- | --- | --- |
| 架构师 `human:李伟` | | |
| 架构 Lead `human:徐滕强` | | |
| 体验 Owner `human:高颖` | | |
| PM `human:郭万迎` | | |
| 算法代表 | | |

*实现以 Git 中 Python 注册表与 JSON Schema 为准；本 md 不参与解释执行。*
