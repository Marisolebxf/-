# 落地设计 · 区域竞争力（`regional_competitiveness`）v0

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.1-draft |
| 日期 | 2026-08-12 |
| 作者 | `human:李伟`（架构师）+ architect-agent |
| 状态 | 落地设计收口稿；指数同构变体 + 结果可视化（柱状/热力/条件 GIS） |
| 样板依赖 | Runtime=`key_link`；计算同构=`regional_index`；可视化见 DEC-COMP-RESULT-VIZ |
| 产品真源 | `CHAIN-TOPIC-REGIONAL` + DEC-CHAIN-REG-COMP-* / MENU-SPLIT-COMP |
| Runtime 真源 | `../../系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 同构差量 | `../../ISOMORPH-chain-analysis-jobs.v0.md` §3.3 |

---

## 0. 一句话

> 与指数共享**对象栏契约**，**不继承**对方模板/权重；  
> 固定三维合成竞争力，结果以柱状+热力（+条件 GIS）为主阅读。

口诀：`chain:regional:competitiveness` = 产业×区域 + **三维权重=100%** + 可视化排名；禁四力/模板 UX。

### 0.1 三维钉死（Bid / 算法 `.3.10`）

| 键 | 展示文案 |
| --- | --- |
| `industry_foundation` | 产业基础 |
| `academic_ecology` | 学术生态 |
| `innovation_ecology` | 创新生态 |

禁止增删维、禁止降为两维、禁止与指数四力混名。

---

## 1. 范围与非目标

### 1.1 覆盖

注册 / draft 三维权重 / Graph / Result（KPI+柱状+热力+GIS 条件+明细+短板）/ Tab=`competitiveness`。

### 1.2 明确不做

- 禁止指数 Tab 的模板/「添加指标」/四力 UX  
- 禁止跨 Tab 自动继承权重  
- 禁止 multi-industry 伪 GIS  
- 禁止 LLM 定综合分/排名  
- 禁止图表失败时静默丢数（明细表为准）  

---

## 2. 身份注册

| 字段 | 值 |
| --- | --- |
| `analysis_key` | `regional_competitiveness` |
| `task_type` | `chain:regional:competitiveness` |
| `graph_version` | `regional_competitiveness.graph.v1` |
| `input_schema_version` | `chain.regional_competitiveness.input.v1` |
| `result_schema_version` | `chain.regional_competitiveness.result_payload.v1` |
| 互斥 | 同用户 + 同 `task_type` |
| 路由 | `/industry-center/regional?tab=competitiveness` |
| 菜单 | `workspace=competitiveness` ≡ `tab=competitiveness`（MENU-SPLIT-COMP） |

---

## 3. 相对样板差量

| 维度 | key_link | regional_index | **本键** |
| --- | --- | --- | --- |
| draft | 三因子 | 模板+计入项 | **仅三维权重** |
| 结果主轴 | 关键图 | 排名+叶子 | **柱状+热力+条件 GIS** |
| 维度模型 | — | 四力 QC11 | **固定三维** |

---

## 4. Create draft

```json
{
  "client_request_id": "uuid",
  "task_type": "chain:regional:competitiveness",
  "analysis_key": "regional_competitiveness",
  "draft": {
    "object": {
      "industries": [{ "industry_id": "INB1204", "display_name": "集成电路" }],
      "regions": [
        { "region_code": "440300", "display_name": "深圳市", "level": "city" },
        { "region_code": "110000", "display_name": "北京市", "level": "province_city" }
      ]
    },
    "dimension_weights": {
      "industry_foundation": 33.3,
      "academic_ecology": 33.3,
      "innovation_ecology": 33.4
    },
    "model_version": "reg_comp_model.v1",
    "data_snapshot_id": null,
    "ui": { "route_path": "/industry-center/regional", "tab": "competitiveness" }
  }
}
```

**硬门禁**：对象组合同指数规则；三维齐全；权重合计 100%（容差实现侧钉死，建议绝对值差 ≤0.05 先归一再存，或 Create 要求精确 100）；缺维禁提交；拒绝前端 graph_version。

---

## 5. Graph · `regional_competitiveness.graph.v1`

| # | stage_code | 要点 | LLM？ |
| --- | --- | --- | --- |
| 1 | `freeze` | 对象+三维权重冻结 | 否 |
| 2 | `load_base_scores` | 底分就绪（可较指数简化） | 否 |
| 3 | `score` | 三维合成+综合排名 | 否 |
| 4 | `gap_explain` | 短板列表 | 可选轻 |
| 5 | `validate_assemble` | 组装（含 viz 数据同源） | 否 |

```text
STAGE_LABELS = {
  "freeze": "任务提交与三维权重冻结",
  "load_base_scores": "底分与数据就绪校验",
  "score": "三维竞争力合成与排名计算",
  "gap_explain": "短板与差异归纳",
  "validate_assemble": "结果可信性校验与报告组装",
}
```

**硬失败**：缺维底分导致无法合成。  
**viz 同源**：`bar_ranking` / `heatmap_matrix` / `dimension_comparison` 必须来自同一 `art.score_bundle`，禁止前端重算。

---

## 6. Result Payload

```text
result_schema_version: chain.regional_competitiveness.result_payload.v1
kpi:  # 写死主体
  composite_competitiveness
  strongest_dimension
  weakest_dimension
sections:
  bar_ranking                # Bid 柱状必达
  heatmap_matrix             # 区域×（三维+综合）
  heatmap_gis                # 条件：multi-region 且区域≥2；multi-industry → 省略本 section
  dimension_comparison       # 明细表（与图同源）
  advantage_gap
  config_honesty             # 权重快照+版本边界
  report_handoff             # 生成报告交接（非页内 PDF）
```

### 阅读顺序（DEC-COMP-RESULT-VIZ）

KPI → 柱状 → 热力矩阵 →（GIS）→ 明细 → 短板 → 版本边界 → 报告。

### Complete 不变量

1. 三维键齐全；权重和=100  
2. 图表与明细数值一致  
3. multi-industry 时 **无** `heatmap_gis` 或显式 `skipped_reason`  
4. 版本混用 → `incomparable`，禁跨版本回写  
5. 展示数字带 `metric_id`  

---

## 7. Prompt

同指数：可选轻叙述；分数真源确定性。

---

## 8. 开放项

GAP-CHAIN-REG-METRICS（三维叶子）；QC05/QC11 **不**用于本 Tab 四力文案；版本混用产品态。

---

## 9. 分层职责

FE 只渲染 Result 内 viz 数据，不本地重算综合分。Java 门禁。Python 出 score_bundle。

---

## 10. 切片

| S | 出口 |
| --- | --- |
| S1 | 三维权重门禁+注册 |
| S2 | 底分校验 |
| S3 | 柱状+明细同源 |
| S4 | 热力；GIS 条件分支 |
| S5 | 报告交接+记录恢复 |

建议序：ISOMORPH 在 `regional_index` 与 `shenzhen_comparison` 之后。

---

## 11. DoD

- [ ] 不出现四力/模板指标选择器  
- [ ] 柱状必达；图表失败明细仍在  
- [ ] GIS 仅 multi-region≥2  
- [ ] wait_view；算法只在 Python  

---

## 12. 已收口决策

| ID | 决策 |
| --- | --- |
| RC1 | 固定三维，不可增删 |
| RC2 | 结果可视化以 DEC-COMP-RESULT-VIZ 为准 |
| RC3 | 与指数共享对象栏、隔离配置 |
| RC4 | 统一 analysis-jobs |

---

## 13. 产物清单

| 文件 | 状态 |
| --- | --- |
| `DESIGN-LANDING-regional_competitiveness.v0.md` | **本文件** |
| `GRAPH-regional_competitiveness.v0.md` | 待建 |
| `chain.regional_competitiveness.input.v1.schema.json` | 待建 |
| `chain.regional_competitiveness.result_payload.v1.schema.json` | 待建 |

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
