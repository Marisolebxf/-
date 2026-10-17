# API · 科技发展态势（TS）· M3 技术发展跟踪（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。路径前缀 / DTO 命名 / 服务归属沿用 `API-TS-M1.md` U1/U2 的 M0 结论；本模块属**批 2**，开工前必须冻结。
> **范围**：仅 M3（技术发展跟踪 · 技术评估与跟踪）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M3（FE-TS-03a~03c） |
| 评估阶段 / 方法 / 维度枚举 | `demo-ui-science/src/App.jsx` L7793–L7809 |
| 参数模板（5 套权重/阈值/维度） | `demo-ui-science/src/App.jsx` L7827–L7873 |
| 推荐组合预设 | `demo-ui-science/src/App.jsx` L7877–L7886 |
| 四方法知识体系（含案例） | `demo-ui-science/src/App.jsx` L8006–L8063 |
| 配置导入校验规则 | `demo-ui-science/src/App.jsx` L7948–L8000 `normalizeTechnologyEvaluationParameterConfig` |
| 评估气泡图默认轴 | `demo-ui-science/src/App.jsx` L8067–L8070 |
| 异步分析工作区 CTA 口径 | `产品实现规程.md` I2-12 / 附录 E / Q-ANALYSIS-01 |

---

## 1. 模块约定（增量）

全局约定继承 `API-TS-M1.md` §1 / §4 / §5。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/tracking/**`（网关对外 `/display/v1/situation/tracking/**`） |
| 评估参数导入 | 参数 Tab 展示只读，但支持**本地 JSON 导入**（demo 在客户端校验）；契约将校验规则服务端化，导入 JSON 通过 `POST /evaluation/imports` 校验后返回规范模板 |
| 异步评估任务 | M3 含「评估进行中 → 评估结果」流程，按**附录 E** 口径（切条件不自动起任务；同用户同条件只允许一条在跑；当天已成功直接打开结果；支持重新分析） |
| 前端组件 | `chart/GraphChart`（气泡图，横轴 `maturity` / 纵轴 `potential` 默认可切换） |

## 2. 枚举字典（前端只读消费）

### 2.1 评估阶段 `eval_stage`（3 类，逐字）
`App.jsx` L7793–L7797：`setup`选择评估条件 · `running`评估进行中 · `result`评估结果。

### 2.2 评估方法 `eval_method`（4 类，逐字）
`App.jsx` L7799 `defaultTechnologyEvaluationMethodKeys`：`expert`专家评估法 · `economic`经济分析法 · `operations`运筹学评价法 · `comprehensive`综合评价法。

### 2.3 评估维度 `eval_dimension`（5 类，逐字含中文标签）
`App.jsx` L7801–L7825：

| `key` | 中文标签 |
|---|---|
| `maturity` | 技术成熟度 |
| `potential` | 产业化能力 |
| `activity` | 创新活跃度 |
| `trend` | 发展趋势 |
| `policy` | 政策关联度 |

### 2.4 参数模板 `param_template`（5 套，逐字）
`App.jsx` L7827–L7873：

| `key` | `template`（中文名） |
|---|---|
| `system-comprehensive-default` | 综合评估默认模板 |
| `system-industrialization` | 产业化落地优先模板 |
| `system-frontier-tracking` | 前沿技术跟踪模板 |
| `system-policy-match` | 政策匹配评估模板 |
| `system-risk-review` | 风险识别加强模板 |

### 2.5 评估气泡图默认轴
`App.jsx` L8067–L8070：x 轴 `maturity`，y 轴 `potential`（前端可切换）。

### 2.6 趋势方向 `score_trend`（3 类）
`up`上升 · `flat`持平 · `down`下降。

### 2.7 评估模型 `eval_model`（3 类，逐字）
M7 的 `TechInnovationEvaluationNewPage.jsx` L72 `MODEL_OPTIONS` 含：`综合评估 - 系统仿真模型` · `专家评估 - 德尔菲法` · `趋势预测 - 仿真模型`。M3 规划 §4 列「参数模板（5 套权重/阈值/启用维度）」；`eval_model` 为 M3 在 M7 借用字段，**M0 确认是否复用同一枚举**。

## 3. 接口清单（6 类）

### 3.1 `GET /v1/situation/tracking/evaluation/current` — 当前评估结果

**用途**（规划 M3-BE ①）：综合分 / 四方法分 / 阶段 / 分项（FE-TS-03a）。

| Query | 说明 |
|---|---|
| `region_scope` / `field_scope` / `keyword` | 评估范围（公共筛选 §1.3） |
| `template_key` | 使用模板（§2.4），默认 `system-comprehensive-default` |

```json
{
  "code": 0,
  "data": {
    "eval_stage": "result",
    "composite_score": 80,
    "method_scores": [
      { "method_key": "expert",        "method_label": "专家评估法",    "score": 83.2 },
      { "method_key": "economic",      "method_label": "经济分析法",    "score": 78.5 },
      { "method_key": "operations",    "method_label": "运筹学评价法",  "score": 76.1 },
      { "method_key": "comprehensive", "method_label": "综合评价法",    "score": 81.4 }
    ],
    "dimensions": [
      { "key": "maturity", "label": "技术成熟度", "score": 72, "weight": 30, "threshold": 60, "pass": true },
      { "key": "potential", "label": "产业化能力", "score": 65, "weight": 25, "threshold": 55, "pass": true },
      { "key": "activity", "label": "创新活跃度", "score": 58, "weight": 20, "threshold": 50, "pass": true },
      { "key": "trend", "label": "发展趋势", "score": 70, "weight": 15, "threshold": 55, "pass": true },
      { "key": "policy", "label": "政策关联度", "score": 68, "weight": 10, "threshold": 45, "pass": true }
    ],
    "bubble_axes": { "x": "maturity", "y": "potential", "label_x": "技术成熟度", "label_y": "产业化能力" },
    "progress": { "setup_done": true, "running_done": true, "result_ready": true },
    "metric_ids": ["Q0xx"]
  }
}
```

边界：
- `eval_stage` 为 `setup` / `running` 时，`method_scores` 为空数组（进行中不给假分）。
- `dimensions` 中的 `weight` / `threshold` 按所选模板返回，前端据此渲染阶段条（评估流程概览）。
- 四方法分必须带 `metric_id`（D9），每项独立登记。

### 3.2 `GET /v1/situation/tracking/evaluation/history` — 历史评估矩阵

**用途**（规划 M3-BE ②）：四期 × 四方法 cells（FE-TS-03a「4 期历史矩阵下钻」）。

```json
{
  "code": 0,
  "data": {
    "periods": [
      { "period_key": "2025Q1", "period_label": "2025 年 Q1", "region_scope": "shenzhen", "field_scope": "CL-FUT-05" },
      { "period_key": "2025Q2", "period_label": "2025 年 Q2", "region_scope": "shenzhen", "field_scope": "CL-FUT-05" },
      { "period_key": "2025Q3", "period_label": "2025 年 Q3", "region_scope": "shenzhen", "field_scope": "CL-FUT-05" },
      { "period_key": "2025Q4", "period_label": "2025 年 Q4", "region_scope": "shenzhen", "field_scope": "CL-FUT-05" }
    ],
    "cells": [
      { "period_key": "2025Q1", "method_key": "expert", "composite_score": 79, "dimension_scores": { "maturity": 70, "potential": 64, "activity": 55, "trend": 68, "policy": 67 } },
      { "period_key": "2025Q4", "method_key": "comprehensive", "composite_score": 82, "dimension_scores": { "maturity": 74, "potential": 68, "activity": 62, "trend": 72, "policy": 70 } }
    ],
    "metric_ids": ["Q0xx"]
  }
}
```

边界：cells 含跨 period × method 的组合；缺某个 period → 该格 `composite_score=null`（矩阵不补假，保留空位态）。

### 3.3 `GET /v1/situation/tracking/evaluation/templates` — 参数模板（只读）

**用途**（规划 M3-BE ③）：5 套模板 + 推荐组合（FE-TS-03b）。

```json
{
  "code": 0,
  "data": {
    "templates": [
      {
        "key": "system-comprehensive-default",
        "template": "综合评估默认模板",
        "group": "system",
        "scenario": "适用于跨技术方向综合判断、汇报评分和横向比较。",
        "weights": { "maturity": 30, "potential": 25, "activity": 20, "trend": 15, "policy": 10 },
        "thresholds": { "maturity": 60, "potential": 55, "activity": 50, "trend": 55, "policy": 45 },
        "dimensions": ["maturity", "potential", "activity", "trend", "policy"]
      }
    ],
    "recommended_preset": {
      "key": "method-recommendation-synthetic-biology",
      "template": "合成生物推荐组合（未保存）",
      "method_keys": ["comprehensive", "expert", "economic"],
      "weights": { "maturity": 28, "potential": 30, "activity": 18, "trend": 12, "policy": 12 },
      "thresholds": { "maturity": 65, "potential": 62, "activity": 55, "trend": 52, "policy": 55 },
      "dimensions": ["maturity", "potential", "activity", "trend", "policy"],
      "reason": "合成生物同时涉及工程成熟度、产业化投入产出和前沿不确定性，建议以综合评价法形成总分，结合专家评估法复核风险，并用经济分析法校验落地价值。"
    }
  }
}
```

边界：推荐组合（`recommended_preset`）按当前筛选条件动态生成，**不可写**（仅展示）；实际使用仍需前端选模板后触发 §3.5 评估任务。

### 3.4 `GET /v1/situation/tracking/evaluation/methods` — 评估方法知识（4 法详解+案例）

**用途**（规划 M3-BE ④）：FE-TS-03c 方法 Tab（4 法详解 + 案例）。

```json
{
  "code": 0,
  "data": {
    "methods": [
      {
        "key": "expert",
        "name": "专家评估法",
        "short_name": "专家判断",
        "principle": "组织领域专家从技术先进性、可实现性、风险和战略价值等维度形成定性与半定量判断。",
        "scenarios": "适用于前沿技术、数据不足、验证周期长或需要快速形成方向性判断的主题。",
        "steps": ["明确评估对象和问题边界", "构建专家评分维度和权重", "收集专家独立判断", "汇总分歧并形成复核结论"],
        "strengths": "能处理不确定性和隐性知识，适合早期研判。",
        "limits": "依赖专家结构和评审一致性，需要保留复核机制。",
        "inputs": "专家名单、技术材料、指标权重、风险清单",
        "outputs": "专家评分、分歧项、复核建议",
        "case_study": "量子计算纠错在工程化数据不足时，先由量子硬件、算法和产业专家判断技术瓶颈优先级。",
        "best_practice": "专家组应覆盖技术、产业和应用三类角色，评分后必须记录分歧原因。"
      }
    ]
  }
}
```

方法字段与 `technologyEvaluationMethods`（`App.jsx` L8006–L8063）逐字一致；知识条目无 `metric_id`（非统计数字，仅为说明性内容）。

### 3.5 异步评估任务（附录 E 口径）

**用途**：03a「评估进行中 → 评估结果」流程，触发型（不自动创建）。

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/v1/situation/tracking/evaluation/runs` | 创建评估 `{ region_scope, field_scope, template_key, keyword }` → `run_id`；同用户同条件**只允许一条在跑**（`409`），当天已成功直接打开结果（`410` 复用提示） |
| `GET` | `/v1/situation/tracking/evaluation/runs/{run_id}` | 状态查询：`status` ∈ `queued`/`running`/`success`/`failed` + `stage` + `result_preview` |
| `POST` | `/v1/situation/tracking/evaluation/runs/{run_id}/retry` | 重新分析（强制新建 `run_id`，不受「当天已成功」限制） |

```json
{
  "code": 0,
  "data": {
    "run_id": "RUN-20261014-0001",
    "status": "running",
    "stage": "comprehensive",
    "progress": { "completed": 2, "total": 4, "current_method": "comprehensive" },
    "filter_echo": { "region_scope": "shenzhen", "field_scope": "CL-FUT-05", "template_key": "system-comprehensive-default" }
  }
}
```

边界：
- 同条件判断逻辑：`(user, region_scope, field_scope, template_key, keyword)` 五元组一致即算「同条件」。
- 进度 `progress` **禁止百分比**（同 M1 §3.8 导出五阶段口径），只返事实状态：当前方法名 + `completed/total`。
- 评估失败 → `status=failed` + `error_stage` + `retry_url`；前端「重新分析」走 retry。

### 3.6 `POST /v1/situation/tracking/evaluation/imports` — 参数配置导入（服务端化校验）

**用途**：FE-TS-03b 参数 Tab 支持用户上传本地 JSON 配置文件，服务端校验后返回标准化模板对象，不静默通过。

**请求体**

```json
{
  "template": "自定义评估模板",
  "weights": { "maturity": 30, "potential": 25, "activity": 20, "trend": 15, "policy": 10 },
  "thresholds": { "maturity": 60, "potential": 55, "activity": 50, "trend": 55, "policy": 45 },
  "dimensions": ["maturity", "potential", "activity", "trend", "policy"]
}
```

**响应**

```json
{
  "code": 0,
  "data": {
    "template_key": "import-20261014-001",
    "template": "自定义评估模板",
    "group": "imported",
    "scenario": "用户导入配置",
    "weights": { "maturity": 30, "potential": 25, "activity": 20, "trend": 15, "policy": 10 },
    "thresholds": { "maturity": 60, "potential": 55, "activity": 50, "trend": 55, "policy": 45 },
    "dimensions": ["maturity", "potential", "activity", "trend", "policy"],
    "valid": true,
    "warnings": []
  }
}
```

**边界**：
- 校验失败时返回 `400`，`errors` 数组逐条列出不通过规则（不静默吞）：
  ```json
  {
    "code": 400,
    "message": "导入配置校验失败",
    "errors": [
      { "field": "weights.potential", "rule": "range", "detail": "权重必须在 0–100 之间" },
      { "field": "weights", "rule": "sum", "detail": "权重合计必须等于 100，当前为 105" }
    ]
  }
  ```
- 校验五规则同 §4（服务端硬闸）；导入成功后 `template_key` 前缀固定 `import-`，不可与 `system-*` 前缀冲突。
- 导入模板仅当前会话有效，**不入库持久化**（如需保存走 U3 未决项）。

## 4. 参数导入校验规则（§3.6 的服务端硬闸）

demo `normalizeTechnologyEvaluationParameterConfig`（`App.jsx` L7948–L8000）校验规则契约化：

| 规则 | 前端 | 服务端 |
|---|---|---|
| `weights` 每项 0–100 | 前端已校验 | 服务端硬闸（`400`） |
| `weights` 合计 = 100 | 前端已校验 | 服务端硬闸（`400`） |
| `thresholds` 每项 0–100 | 前端已校验 | 服务端硬闸（`400`） |
| `dimensions` 至少一个 | 前端已校验 | 服务端硬闸（`400`） |
| `template` 必填 | 前端已校验 | 服务端硬闸（`400`） |

POST `/v1/situation/tracking/evaluation/imports` 统一校验并返回标准模板对象，不静默通过。

## 5. 数据需求与存储建议（Mock 先行 D7）

| # | 域 | 建议表名 | 关键字段 | 消费接口 | 备注 |
|---|---|---|---|---|---|
| 1 | 评估结果 | `ts_tracking_result` | `run_id, region_scope, field_scope, template_key, composite_score, method_scores JSON, dimension_scores JSON, eval_stage, created_at` | §3.1 / §3.2 | 含 `metric_id` 映射（D9） |
| 2 | 历史矩阵 | `ts_tracking_history` | `period_key, method_key, composite_score, dimension_scores, metric_id, calc_batch_id` | §3.2 | 算法产物 |
| 3 | 模板/知识 | `ts_tracking_template`（只读字典） | `key, template, group, scenario, weights JSON, thresholds JSON, dimensions JSON` | §3.3 | 禁止前端手写 |
| 4 | 评估任务 | `ts_tracking_run`（app_user 侧） | `run_id, user_id, filter_snapshot, status, result_json, created_at, completed_at` | §3.5 | 带写面（任务创建） |

## 6. 未决项

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | `eval_model` 枚举（M3 参数模板）是否复用 M7 的 `MODEL_OPTIONS`（`综合评估 - 系统仿真模型` 等 3 类） | M0 拍板 |
| U2 | 异步评估任务是否需图像/视频产出（demo 无），还是仅 JSON 结果 | M0 + 产品侧 |
| U3 | 推荐组合 `recommended_preset` 是否由算法动态生成 | M0 + 算法侧 |
| U4 | 四方法分与维度分的 `metric_id` 清单登记 | `ALL-TS-D9`，随批 2 评审 |
| U5 | 评估任务执行时间上限（超时失败策略） | M0 |

## 7. 自检（冻结前）

- [ ] `eval_method` / `eval_dimension` / `param_template` 与 `App.jsx` L7799/L7801/L7827 逐字一致
- [ ] 四方法知识字段与 `technologyEvaluationMethods`（L8006–L8063）逐字一致
- [ ] 导入校验五规则（权重范围/合计/阈值/维度/模板名）全部服务端硬闸
- [ ] 异步任务：同条件单飞 + 当天复用 + 重新分析可强制重跑；禁止百分比进度
- [ ] `eval_stage` 为 `running` 时 method_scores 为空，不补假分
- [ ] 缺数 / 空态与 M1 §5 一致

## 8. 会签记录（批 2 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
