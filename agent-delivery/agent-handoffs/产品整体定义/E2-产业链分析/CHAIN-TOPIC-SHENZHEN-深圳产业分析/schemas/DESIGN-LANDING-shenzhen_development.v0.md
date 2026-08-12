# 落地设计 · 深圳发展分析（`shenzhen_development`）v0

| 项 | 内容 |
| --- | --- |
| 文档版本 | v0.1-draft |
| 日期 | 2026-08-12 |
| 作者 | `human:李伟`（架构师）+ architect-agent |
| 状态 | 落地设计收口稿；**硬依赖** comparison Result；路径生成重 LLM |
| 样板依赖 | Runtime=`key_link`；Prompt 权重类似 `cycle`；ISOMORPH §3.5 |
| 产品真源 | `CHAIN-TOPIC-SHENZHEN` 五件套 |
| Runtime 真源 | `../../系统设计说明书-Analysis-Job-Runtime.v0.md` |
| 同构差量 | `../../ISOMORPH-chain-analysis-jobs.v0.md` §3.5 |
| 上游 | `DESIGN-LANDING-shenzhen_comparison.v0.md` |

---

## 0. 一句话

> Create **必须**显式带有效 `source_result_id`（同产业、结构化、已授权的对比 Result）；  
> 禁止静默继承；LLM 生成 ≥2 套路径，规则校验完整度与对比数字一致性。

口诀：`chain:shenzhen:shenzhen_development` = 绑源对比快照 + 政策/技术/人才目标 + **路径 LLM**。

### 0.1 命名纪律

| 术语 | 含义 | 禁止 |
| --- | --- | --- |
| `source_result_id` | 对比 Result Snapshot ID | 静默填最近一次 |
| `source_revision` | 源版本钉扎 | 跨 revision  silently 混用 |
| `paths[]` | ≥2 发展路径 | `<2` 时伪造补齐 |

---

## 1. 范围与非目标

### 1.1 覆盖

注册 / draft（source+goals）/ Graph / Prompt Pack / Result（源证据+三类建议+多路径）/ Tab=`development`。

### 1.2 明确不做

- 禁止 PDF / 跨产业 / 过期 / 无授权 Result 作源  
- 禁止静默继承最近对比  
- 禁止对比页自动跳转导致丢路径上下文（展开对比用**抽屉**，URL 留 development）  
- 禁止项目/预算/工期/责任单位等执行跟踪 UI  
- 禁止 IC-36 未交付时宣称「全局案例已匹配」  
- 禁止发展页装填「产业发展摘要 KPI」  

---

## 2. 身份注册

| 字段 | 值 |
| --- | --- |
| `analysis_key` | `shenzhen_development` |
| `task_type` | `chain:shenzhen:shenzhen_development` |
| `graph_version` | `shenzhen_development.graph.v1` |
| `input_schema_version` | `chain.shenzhen_development.input.v1` |
| `result_schema_version` | `chain.shenzhen_development.result_payload.v1` |
| `prompt_pack_version` | `shenzhen_development.path.prompts.v1` |
| 互斥 | 同用户 + 同 `task_type` |
| 路由 | `/industry-center/shenzhen?tab=development` |

---

## 3. 相对样板差量

| 维度 | key_link | cycle | **本键** |
| --- | --- | --- | --- |
| Input | 链对象 | industry+四参数 | **`source_result_id` 必填** |
| LLM | 1 处叙述 | 2 处 | **路径生成（核心）** |
| 跨 Job | 无 | 无 | **硬依赖 comparison** |
| 结果 | 环节图 | 回溯诊断预测 | **源证据+建议+多路径** |

---

## 4. Create draft

```json
{
  "client_request_id": "uuid",
  "task_type": "chain:shenzhen:shenzhen_development",
  "analysis_key": "shenzhen_development",
  "draft": {
    "object": {
      "industry_id": "INB1204",
      "display_name": "集成电路"
    },
    "source": {
      "source_result_id": "uuid-of-comparison-result",
      "source_revision": "rev-1",
      "source_task_type": "chain:shenzhen:shenzhen_comparison"
    },
    "goals": {
      "policy": "……",
      "technology": "……",
      "talent": "……"
    },
    "ui": { "route_path": "/industry-center/shenzhen", "tab": "development" }
  }
}
```

**Java Create 硬门禁（钉死）**：

1. `source.source_result_id` 非空且能解析为 Result Snapshot  
2. `source_task_type` 必须为 `chain:shenzhen:shenzhen_comparison`（或等价 analysis_key）  
3. 源 Result：同 `industry_id`、结构化完整、当前用户可读授权  
4. 拒绝：PDF 导出物、跨产业、过期策略命中、无授权 → `source_invalid` / `rejected_sources`  
5. **禁止**服务端在缺省时自动填「最近一次对比」  
6. `goals` 三键均须用户显式确认非空（或产品允许空则诚实标未设目标——**v0 建议三键必填**）  
7. 同 task_type 互斥；拒绝前端 graph_version  

---

## 5. Graph · `shenzhen_development.graph.v1`

| # | stage_code | 要点 | LLM？ | Artifact |
| --- | --- | --- | --- | --- |
| 1 | `freeze` | 绑定 source + goals | 否 | `art.context` |
| 2 | `load_source` | 只读加载对比 Result | 否 | `art.source_snapshot` |
| 3 | `path_generate` | ≥2 套发展路径 | **是（核心）** | `art.paths_draft` |
| 4 | `path_validate` | 完整度 + 与对比数字一致 | 规则 | `art.paths_validated` |
| 5 | `validate_assemble` | 组装 | 否 | `art.result_payload` |

```text
STAGE_LABELS = {
  "freeze": "任务提交与对比源及发展目标冻结",
  "load_source": "加载情况对比结果快照",
  "path_generate": "大语言模型生成多套发展路径",
  "path_validate": "路径完整度与对比一致性校验",
  "validate_assemble": "结果可信性校验与报告组装",
}
```

### 5.3 节点契约

#### N1 · `freeze`

核对 source 元数据与 goals；写 honesty 种子。失败：`SOURCE_REF_INVALID` / `GOALS_INCOMPLETE`。

#### N2 · `load_source`

只读取对比 Result；抽取政策/技术/人才摘要与矩阵短板标签。失败：源不可读/结构坏 → **硬失败** `SOURCE_LOAD_FAILED`（不可空跑路径）。

#### N3 · `path_generate`（LLM）

| 项 | 内容 |
| --- | --- |
| 输入 | source 摘要、goals、短板/优势标签 |
| 输出 | `paths[]`（建议 ≥2）；每路径含 steps、horizon、`targets[]`（针对短板/优势）、advice 三向草稿 |
| 禁止 | 编造源中不存在的对比数字；宣称案例库已匹配（IC-36 gap） |
| 失败 | Loop 耗尽 → **不**伪造路径；进入 N4 记 `incomplete_paths` |

#### N4 · `path_validate`

```text
1) 路径数 ≥ 2？否则 Complete 失败或 succeeded+honesty.incomplete_paths（产品钉死：v0 建议 **硬失败** PATH_COUNT_LT_2）
2) 每路径必有 steps≥1、targets 非空、适用/局限字段
3) 引用的对比数字必须 ⊆ art.source_snapshot
4) 通过 → art.paths_validated；建议块可从路径聚合
```

#### N5 · `validate_assemble`

按 §6 组装；双检。

### 5.5 limits（相对 key_link 加严）

| 项 | 默认 |
| --- | --- |
| `llm_retry_max`（path_generate） | ≥2 |
| `node_timeout_sec`（path_generate） | ≥120 |
| `job_timeout_sec` | ≥600 |

---

## 6. Result Payload

```text
result_schema_version: chain.shenzhen_development.result_payload.v1
# 无顶栏包装 KPI
sections:
  source_evidence            # 对比摘要；抽屉可展开完整对比（URL 不改 tab）
  policy_advice
  tech_advice
  talent_advice
  paths[]                    # ≥2；含针对标签 + applicability
  applicability              # 可内嵌 paths
  evidence                   # 引用；IC-36 未交付时 honesty.case_library=unavailable
  limitations
source_ref:
  source_result_id
  source_revision
honesty / versions / object / metrics_used[]
```

### Complete 不变量

1. `source_ref` 与 Input 一致且可追溯  
2. `paths.length ≥ 2`  
3. 路径内数字 ⊆ 源快照  
4. 无产业发展摘要 KPI 块  
5. `honesty.case_library` 不得声称 `matched` 当 IC-36 未交付  
6. 展示统计带 `metric_id`  

### Artifact → Result

| Artifact | Result |
| --- | --- |
| `art.source_snapshot` 摘要 | `sections.source_evidence` |
| `art.paths_validated` | `sections.paths` |
| 聚合建议 | `policy_advice` / `tech_advice` / `talent_advice` |

---

## 7. Prompt Pack

| Pack ID | 节点 | Output 要点 |
| --- | --- | --- |
| `shenzhen_development.path.prompts.v1` | N3 | paths≥2；targets；三向建议草稿；**禁**改源数字 |

升文案一般不升 graph；改校验规则升 `rule_pack_version`。

配套待建：`PROMPT-PACK-shenzhen_development-path.v0.md` + context/output schema。

---

## 8. 数据依赖与开放项

| 依赖 | 策略 |
| --- | --- |
| comparison Result | Create/N2 **硬失败** |
| LLM 网关 | N3 失败 → 路径不足则 **硬失败**（v0） |
| IC-36 案例库 | V1 honesty gap，不宣称匹配 |
| QC08 | 路径「针对」标签与矩阵一致 |

---

## 9. 分层职责

FE：显式选源或接受 CTA 带入；goals 确认；抽屉看对比；不直连 LLM。  
Java：源合法性门禁（最关键）；Snapshot。  
Python：load_source + path LLM + validate。

---

## 10. 切片

| S | 出口 |
| --- | --- |
| S1 | 缺 source 必 400；静默继承测不通 |
| S2 | load_source 成功/失败码 |
| S3 | LLM 出 ≥2 路径或明确失败 |
| S4 | path_validate 拒数字幻觉 |
| S5 | 抽屉展开对比不丢 tab；记录恢复 |

落地序：必须在 `shenzhen_comparison` Result 契约稳定之后（ISOMORPH **#6**）。

---

## 11. DoD

- [ ] 无 source 无法创建；拒绝非法源类型  
- [ ] ≥2 路径；数字与对比一致  
- [ ] 不自动跳转；无执行跟踪 UI  
- [ ] IC-36 诚实 gap；wait_view；算法只在 Python  

---

## 12. 已收口决策

| ID | 决策 |
| --- | --- |
| SD1 | `source_result_id` 显式必填，禁止静默继承 |
| SD2 | 路径数 `<2` → v0 硬失败（不伪补齐） |
| SD3 | 展开对比用抽屉，保留 development tab |
| SD4 | 路径 LLM + 规则校验双段，类似 cycle 的「规则真值/LLM 叙述」精神 |
| SD5 | 统一 analysis-jobs |

---

## 13. 产物清单

| 文件 | 状态 |
| --- | --- |
| `DESIGN-LANDING-shenzhen_development.v0.md` | **本文件** |
| `GRAPH-shenzhen_development.v0.md` | 待建 |
| `chain.shenzhen_development.input.v1.schema.json` | 待建 |
| `chain.shenzhen_development.result_payload.v1.schema.json` | 待建 |
| `PROMPT-PACK-shenzhen_development-path.v0.md` | 待建 |

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
