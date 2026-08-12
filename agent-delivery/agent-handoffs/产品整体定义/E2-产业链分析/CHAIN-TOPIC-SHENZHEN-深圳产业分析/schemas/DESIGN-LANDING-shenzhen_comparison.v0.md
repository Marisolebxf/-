# 落地设计 · 深圳情况对比（`shenzhen_comparison`）v0

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.1-draft |
| 日期 | 2026-08-12 |
| 作者 | `human:李伟`（架构师）+ architect-agent |
| 状态 | 落地设计收口稿；计算型 + 标杆门禁；可喂给 development |
| 样板依赖 | Runtime=`key_link`；ISOMORPH §3.4 |
| 产品真源 | `CHAIN-TOPIC-SHENZHEN` 五件套 |
| Runtime 真源 | `../../系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 同构差量 | `../../ISOMORPH-chain-analysis-jobs.v0.md` §3.4 |

---

## 0. 一句话

> **固定深圳** + 1 产业 + 1~5 就绪标杆；四维确定性对比；  
> 结果可携带 `source_result_id` 进入发展分析，**禁止**自动跳转/自动跑发展。

口诀：`chain:shenzhen:shenzhen_comparison` = 标杆门禁 + 四维矩阵 + 综合判断字段；LLM 轻量可选。

### 0.1 四维钉死

| 维 | 说明 |
| --- | --- |
| 产业 | Bid `.6.2` 产业化相关分块 |
| 专利 | |
| 政策 | |
| 人才 | Bid `.6.1`；**禁止**与产业合并标签 |

综合判断字段（原文字段，禁散列 KPI 卡）：技术成熟度 / 市场前景 / 技术可行性 / 发展阶段 / 阶段描述。

---

## 1. 范围与非目标

### 1.1 覆盖

注册 / draft（标杆列表+四维模型版本）/ Graph / Result / Tab=`comparison` / 带入发展 CTA。

### 1.2 明确不做

- 禁止对比页顶部「产业发展摘要 KPI」  
- 禁止完成后自动进结果 / 自动跑发展分析  
- 禁止「标杆就绪检测」独立按钮（= 选择+提交校验）  
- 禁止国内城市 Select 平替四级 Cascader  
- 禁止静默删标杆或冒名默认标杆  
- 禁止 PDF/过期/跨产业 Result 冒充本键正式对比（本键自身输出结构化 Result）  

---

## 2. 身份注册

| 字段 | 值 |
| --- | --- |
| `analysis_key` | `shenzhen_comparison` |
| `task_type` | `chain:shenzhen:shenzhen_comparison` |
| `graph_version` | `shenzhen_comparison.graph.v1` |
| `input_schema_version` | `chain.shenzhen_comparison.input.v1` |
| `result_schema_version` | `chain.shenzhen_comparison.result_payload.v1` |
| 互斥 | 同用户 + 同 `task_type` |
| 路由 | `/industry-center/shenzhen?tab=comparison` |
| 可喂发展 | `may_feed_development: true`（Result 元数据） |

---

## 3. 相对 key_link 差量

| 维度 | key_link | 本键 |
| --- | --- | --- |
| 主对象 | 产业链 | **深圳(固定)+产业+多标杆** |
| 配置 | 三因子 | **标杆多选 + 四维只读确认** |
| 计算 | 五环节 | **四维对比 + 矩阵标签 + 阶段判断** |
| LLM | N4c 核心 | **轻/可选 narrative** |
| 下游 | 无 | **可被 development 引用** |

---

## 4. Create draft

```json
{
  "client_request_id": "uuid",
  "task_type": "chain:shenzhen:shenzhen_comparison",
  "analysis_key": "shenzhen_comparison",
  "draft": {
    "object": {
      "subject_region": { "region_code": "440300", "display_name": "深圳市", "fixed": true },
      "industry": { "industry_id": "INB1204", "display_name": "集成电路" },
      "benchmarks": [
        {
          "region_code": "US-CA-SV",
          "path": ["全球", "北美", "硅谷"],
          "readiness": "ready"
        }
      ]
    },
    "dimension_model_version": "sz_cmp_dims.v1",
    "data_snapshot_id": null,
    "ui": { "route_path": "/industry-center/shenzhen", "tab": "comparison" }
  }
}
```

**Java 硬门禁**：

1. `subject_region.fixed=true` 且为深圳（服务端再校验，防篡改）  
2. 恰好 1 产业；标杆 1~5；**至少 1 个 readiness=ready**  
3. pending 标杆不得进入正式计算集（Create 直接 400 或剥离策略须产品钉死：**建议直接拒绝含 pending 的提交**）  
4. 产业变更不得静默替换旧标杆列表  
5. 同 task_type 互斥；拒绝前端 graph_version  

---

## 5. Graph · `shenzhen_comparison.graph.v1`

| # | stage_code | 要点 | LLM？ |
| --- | --- | --- | --- |
| 1 | `freeze` | 标杆列表+四维模型只读确认 | 否 |
| 2 | `benchmark_ready_check` | 执行侧再校验就绪 | 否 |
| 3 | `score_dimensions` | 四维对比+矩阵标签+综合判断字段 | 否 |
| 4 | `narrative` | 对比解读 | 可选轻 |
| 5 | `validate_assemble` | 组装 | 否 |

```text
STAGE_LABELS = {
  "freeze": "任务提交与标杆及四维模型冻结",
  "benchmark_ready_check": "标杆就绪复核",
  "score_dimensions": "四维对比计算与综合判断",
  "narrative": "对比解读归纳",
  "validate_assemble": "结果可信性校验与报告组装",
}
```

**硬失败**：执行时标杆变未就绪 / 无有效标杆 → `no_benchmark` / `benchmark_not_ready`。  
**矩阵标签**：`领先` / `相当` / `落后`；UI 列文案「深圳处于 {label}」，去重前缀。  
**降级**：narrative 失败不影响四维与矩阵。

---

## 6. Result Payload

```text
result_schema_version: chain.shenzhen_comparison.result_payload.v1
# 无顶栏数值 KPI 卡片
sections:
  dimension_comparison       # 四维分块（人才/产业等禁合并）
  advantage_gap_matrix       # 对比矩阵：深圳处于 领先|相当|落后
  synthesis_judgment         # 产业化潜力与发展阶段综合判断
  judgment_fields            # 五字段原文字段列表
  stale_note?                # 标杆后续失效说明（只读快照仍可看）
  carry_to_development       # CTA 元数据：可生成带 source_result_id 的深链
meta:
  may_feed_development: true
  industry_id
  subject_region_code
honesty / versions / object / metrics_used[]
```

### Complete 不变量

1. 主体恒为深圳；产业与 Input 一致  
2. 矩阵每个标杆×维有合法标签枚举  
3. judgment_fields 五键齐全（值可标 gap/mock）  
4. 无「产业发展摘要」顶栏 KPI 块  
5. `may_feed_development=true` 仅当结构化完整且授权可读  

---

## 7. Prompt

可选 `shenzhen_comparison.narrative.prompts.v1`；禁改矩阵标签与四维分数。

---

## 8. 开放项

| ID | 说明 |
| --- | --- |
| QC08 | 对比中间层权重；与 Q016 对标集合并 |
| GAP-CHAIN-SZ-METRICS | 四维叶子 Mock/Pending |
| 标杆就绪 | 未就绪 ⚠️，禁伪默认 |

---

## 9. 分层职责

FE：Cascader 选标杆；Create；wait_view；结果 CTA「带入发展分析」带 `source_result_id`。  
Java：深圳固定校验、就绪门禁、Snapshot。  
Python：四维与矩阵真源。

---

## 10. 切片

| S | 出口 |
| --- | --- |
| S1 | 门禁：无就绪标杆不可建 |
| S2 | 执行侧就绪复核失败码 |
| S3 | 四维+矩阵标签 |
| S4 | judgment_fields + 可选 narrative |
| S5 | carry_to_development 深链可被 development Create 消费 |

---

## 11. DoD

- [ ] 深圳不可改；≥1 就绪标杆  
- [ ] 无自动跳发展；无顶栏摘要 KPI  
- [ ] Cascader 四级；wait_view  
- [ ] 结果可作 development 合法源  

---

## 12. 已收口决策

| ID | 决策 |
| --- | --- |
| SC1 | 标杆 1~5；Create 拒绝 pending |
| SC2 | 四维分开展示；禁合并标签 |
| SC3 | 不自动跳转 development |
| SC4 | 统一 analysis-jobs |

---

## 13. 产物清单

落在 `CHAIN-TOPIC-SHENZHEN-深圳产业分析/schemas/`：

| 文件 | 状态 |
| --- | --- |
| `DESIGN-LANDING-shenzhen_comparison.v0.md` | **本文件** |
| `GRAPH-shenzhen_comparison.v0.md` | 待建 |
| `chain.shenzhen_comparison.input.v1.schema.json` | 待建 |
| `chain.shenzhen_comparison.result_payload.v1.schema.json` | 待建 |

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
