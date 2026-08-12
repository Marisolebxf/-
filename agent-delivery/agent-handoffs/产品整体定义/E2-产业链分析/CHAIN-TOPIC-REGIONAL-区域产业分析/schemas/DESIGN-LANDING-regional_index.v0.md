# 落地设计 · 区域产业指数（`regional_index`）v0

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.1-draft |
| 日期 | 2026-08-12 |
| 作者 | `human:李伟`（架构师）+ architect-agent |
| 状态 | 落地设计收口稿；计算型 Job，默认可无重 Prompt |
| 样板依赖 | Runtime 样板键 `key_link`；差量见 ISOMORPH §3.3 |
| Bid | 区域产业指数相关章节（展示/算法以 REGIONAL 五件套 TRACE 为准） |
| 产品真源 | `CHAIN-TOPIC-REGIONAL` 五件套 + DEC-CHAIN-REG-INDEX-* / MENU-SPLIT |
| Runtime 真源 | `../../系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 同构差量 | `../../ISOMORPH-chain-analysis-jobs.v0.md` §3.3 |

---

## 0. 一句话

> **不换厨房，只换菜谱**：配置区 WYSIWYG 即时汇总 ≠ 正式结果；  
> 点「生成分析」冻结模板/计入项/权重，产出不可变 `regional_index` Result。

口诀：`chain:regional:index` = **产业×区域** + **加权指数排名** + 叶子贡献；LLM 不作分数真源。

### 0.1 命名纪律

| 术语 | 含义 | 禁止 |
| --- | --- | --- |
| `stage_code` | 过程步 | 与四力维度名混用 |
| 四力维度 | 产业力/创新力/学术力/支撑力（QC11 临时） | 与竞争力三维模型混用 |
| 计入项 | 参与加权的指标子集 | 默认勾选全库 |

---

## 1. 范围与非目标

### 1.1 覆盖

注册 / draft（模板+权重）/ Graph / Result（KPI+排名+四力+叶子+短板）/ Tab=`index` 接线 / S1–S5。

### 1.2 明确不做

- 禁止「轻量预览」按钮 / `previewing` 态（已废止）  
- 禁止独立预览写历史或正式 Result  
- 禁止运营侧 CRUD 官方模板/指标库（本键消费只读模板）  
- 禁止多产业×多区域对象组合  
- 禁止 LLM 作为指数/排名真源  
- 不把竞争力三维混入本 Tab  

---

## 2. 身份注册

| 字段 | 值 |
| --- | --- |
| `analysis_key` | `regional_index` |
| `task_type` | `chain:regional:index` |
| `graph_version` | `regional_index.graph.v1` |
| `input_schema_version` | `chain.regional_index.input.v1` |
| `result_schema_version` | `chain.regional_index.result_payload.v1` |
| 互斥 | 同用户 + 同 `task_type` |
| 路由 | `/industry-center/regional?tab=index` |
| 菜单 | `DEC-CHAIN-REG-MENU-SPLIT`：`workspace=index` ≡ `tab=index` |

---

## 3. 相对 key_link 差量

| 维度 | key_link | regional_index |
| --- | --- | --- |
| 主对象 | industry_chain | **1 产业+1~5 区域** 或 **2~5 产业+1 区域** |
| 配置 | 三因子只读 | **模板 + 计入项 + 可调权重 + WYSIWYG** |
| 计算 | 五环节高端化 | **加权指数 + 排名 + 叶子贡献** |
| Prompt | N4c | **—/轻**（gap_explain 可选） |
| 结果 | 关键全链 | **KPI + 排名表 + 四力 + 叶子 + 短板** |

---

## 4. 端到端主路径

```text
对比篮确认对象组合
  → Tab=index 选模板、计入指标、调权重（配置即汇总=预览）
  → 生成分析 → 冻结 evaluation_config 快照
  → Job 出正式 Result → wait_view → 显式查看
```

### 4.1 Create draft

```json
{
  "client_request_id": "uuid",
  "task_type": "chain:regional:index",
  "analysis_key": "regional_index",
  "draft": {
    "object": {
      "industries": [{ "industry_id": "INB1204", "display_name": "集成电路" }],
      "regions": [
        { "region_code": "440300", "display_name": "深圳市", "level": "city" },
        { "region_code": "310000", "display_name": "上海市", "level": "province_city" }
      ]
    },
    "evaluation_config": {
      "template_id": "reg_index_sys_default",
      "template_version": "1.0.0",
      "template_kind": "system",
      "included_metrics": [
        { "metric_id": "M_REG_IND_SCALE", "weight": 25, "dimension_group": "industry_force" }
      ],
      "weight_sum": 100,
      "model_version": "reg_index_model.v1",
      "data_snapshot_id": "optional-or-server-fill"
    },
    "ui": { "route_path": "/industry-center/regional", "tab": "index" }
  }
}
```

**Java 硬门禁**：

1. 对象组合合法（禁多×多）  
2. `included_metrics` ≥1；`weight_sum===100`（仅计入项）  
3. 底分未就绪 → `base_score_missing`；指标不可用 → 阻断并引用 `GAP-CHAIN-REG-METRICS`  
4. 拒绝前端 `graph_version`；同 task_type 互斥  

---

## 5. Graph · `regional_index.graph.v1`

| # | stage_code | 文案要点 | LLM？ | Artifact |
| --- | --- | --- | --- | --- |
| 1 | `freeze` | 对象+模板+权重快照冻结 | 否 | `art.context` |
| 2 | `load_base_scores` | 底分/ADS 就绪校验 | 否 | `art.base_scores` |
| 3 | `score` | 加权重算+排名 | 否 | `art.score_bundle` |
| 4 | `gap_explain` | 优劣/短板叙述 | 可选轻 | `art.gap_text` |
| 5 | `validate_assemble` | 组装 | 否 | `art.result_payload` |

```text
STAGE_LABELS = {
  "freeze": "任务提交与评价配置冻结",
  "load_base_scores": "底分与数据就绪校验",
  "score": "加权合成指数与排名计算",
  "gap_explain": "优劣短板归纳",
  "validate_assemble": "结果可信性校验与报告组装",
}
```

**硬失败**：对象非法；底分关键缺失导致无法对任一主体打分；权重合计≠100（应在 Create 拦）。  
**降级**：`gap_explain` LLM 失败 → 空短板叙述或规则模板句 + honesty；**分数/排名不可降级假造**。  
不可比：版本/权重不一致主体 → `incomparable` + 原因，**禁伪排名**。

---

## 6. Result Payload

```text
result_schema_version: chain.regional_index.result_payload.v1
kpi:                         # 锚定综合第 1 名主体写死
  composite_index
  strongest_dimension
  relative_gap
  delta_vs_second
sections:
  ranking_comparison         # 区域|主体|综合指数|排名
  dimension_scores           # 四力分组
  leaf_contributions         # 仅已计入叶子
  advantage_gap              # 文字短板 → 具体叶子
  config_honesty             # 模板/权重/Mock 诚实条
honesty / versions / object / metrics_used[]
```

### Complete 不变量

1. 排名表主体集合 ⊆ Input 对象组合  
2. `weight_sum` 回显 = 100；叶子仅含计入项  
3. 有可比主体时排名连续；不可比不得插入伪名次  
4. KPI 主体 = 综合第 1（写死，禁泛化「领先」文案无主体）  
5. 展示数字带 `metric_id`；QC11 维度文案诚实条  

---

## 7. Prompt

默认无重 Pack。若启用：`regional_index.gap.prompts.v1` 仅叙述，禁改分数。

---

## 8. 数据依赖与开放项

| 依赖 | 策略 |
| --- | --- |
| 模板注册表 | Create 硬失败 |
| 底分 ADS | load_base_scores 硬失败或 incomparable |
| QC11 四力文案 | 页内 ⚠️；不挡 Job |
| QC05 / GAP-CHAIN-REG-METRICS | Mock/Pending + metric_gap_ref |

---

## 9. 分层职责

FE：WYSIWYG 预览本地可算，**正式结果只认 Job Result**。  
Java：门禁+快照；不写加权算法。  
Python：打分排名真源。

---

## 10. 切片 S1–S5

| S | 出口 |
| --- | --- |
| S1 | 注册+对象/权重门禁+五段文案 |
| S2 | 底分校验失败可见 |
| S3 | 正式排名+四力与配置预览可对照但 ID 不同 |
| S4 | 叶子贡献仅计入项；短板可降级 |
| S5 | 记录恢复同一 result_snapshot_id |

---

## 11. DoD

- [ ] 配置预览 ≠ 正式 Result（生成后才不可变）  
- [ ] 非法组合/权重≠100 无法提交  
- [ ] wait_view；结果 KPI 写死第 1 名主体  
- [ ] 无 LLM 分数真源；QC11 诚实可见  

---

## 12. 已收口决策

| ID | 决策 |
| --- | --- |
| RI1 | WYSIWYG 预览不写正式 Result（DEC-WYSIWYG） |
| RI2 | 废止轻量预览态 |
| RI3 | 四力 = QC11 临时默认 |
| RI4 | 结果结构以 DEC-RESULT-RANK-LEAF 为准 |
| RI5 | 统一 analysis-jobs |

---

## 13. 产物清单

落在 `CHAIN-TOPIC-REGIONAL-区域产业分析/schemas/`：

| 文件 | 状态 |
| --- | --- |
| `DESIGN-LANDING-regional_index.v0.md` | **本文件** |
| `GRAPH-regional_index.v0.md` | 待建 |
| `chain.regional_index.input.v1.schema.json` | 待建 |
| `chain.regional_index.result_payload.v1.schema.json` | 待建 |
| OpenAPI draft oneOf | 待补丁 |

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
