# API · 科技发展态势（TS）· M7 科技创新评估（接口契约草案）

> **任务**：`BE-TS-CONTRACT-02`（M2–M9 接口契约定义，按批冻结）
> **日期**：2026-10-14 · **作者**：agent:architect-agent（监管：human:李伟；会签：human:孔东 / human:徐腾强 / human:堂绍祖）
> **状态**：**草案（未冻结）**。本模块属**批 4**（M7/M8/M9），批 4 开工前冻结。
> **范围**：仅 M7（科技创新评估 · demo `tech-innovation-evaluation-new`）。

**真源引用**

| 用途 | 真源 |
|---|---|
| 接口用途与数据需求 | `TS-模块开发规划与任务拆分.md` §4 M7（FE-TS-07a~07c） |
| 默认筛选（领域/产业/区域/时间/口径/模型） | `demo-ui-science/src/pages/tech-innovation-evaluation-new/TechInnovationEvaluationNewPage.jsx` L61–L72 |
| 阶段顺序 | 同上 L74 `stageOrder` |
| 四维默认权重 | 同上 L76–L81 `DEFAULT_WEIGHTS` |
| 四维指标体系（含二级指标/状态/摘要/口径） | 同上 L83–L174 `dimensionBaseConfigs` |
| 流程任务 / 数据进度 / 产业链阶段 / 政策建议 | 同上 L176–L200 |

---

## 1. 模块约定（增量）

全局约定继承 `API-TS-M1.md` §1 / §4 / §5。

| 项 | 约定 |
|---|---|
| 服务内路径前缀 | `/v1/situation/innovation-evaluation/**`（网关对外 `/display/v1/situation/innovation-evaluation/**`） |
| 与 M3 边界 | M3 = 技术评估（四方法 × 五维度，面向**技术方向**）；M7 = 区域/产业**科技创新综合评估**（四维：科学/技术/产业/政策）。两套评估体系独立，不合并 |
| 读写面 | 全只读 ADS；报告预览只读；无带写面 |

## 2. 枚举字典（前端只读消费）

### 2.1 评估维度 `dimension_key`（4 类，逐字含中文标题）
`dimensionBaseConfigs`（L83–L174）：

| `key` | 标题 |
|---|---|
| `science` | 科学创造力指标展示 |
| `technology` | 技术创新力指标展示 |
| `industry` | 产业发展潜力指标展示 |
| `policy` | 政策与条件保障力指标展示 |

### 2.2 阶段 `stage`（3 类，逐字）
`stageOrder`（L74）：`setup`选择评估条件 · `running`评估进行中 · `result`评估结果（与 M3 §2.1 同枚举，跨模块复用）。

### 2.3 趋势方向 `score_trend`（3 类）
`up` · `flat` · `down`（L89/L110 等）。

### 2.4 状态 `status`（逐字示例）
`较强` · `稳步提升` · `具备潜力` · `需加强`（L91/L112 等）——状态文案由后端按分数段生成并下发，前端不映射。

### 2.5 筛选枚举（逐字）
`TechInnovationEvaluationNewPage.jsx` L70–L72：

| 枚举 | 取值 |
|---|---|
| `time_range` | `2019年 - 2025年` · `2020年 - 2025年` · `2021年 - 2025年` · `2022年 - 2025年` |
| `data_caliber` | `申报量 / 授权 / 公开` · `申报量 / 授权` · `授权 / 公开` · `公开数据` |
| `model` | `综合评估 - 系统仿真模型` · `专家评估 - 德尔菲法` · `趋势预测 - 仿真模型` |

## 3. 接口清单（3 类）

### 3.1 `GET /v1/situation/innovation-evaluation/result` — 评估结果

**用途**（规划 M7-BE ①）：综合分 / 四维分 / 建议 / 范围（FE-TS-07a 结果 Tab）。

| Query | 说明 |
|---|---|
| `field` / `industry` / `region` | 评估范围（默认对齐 demo `DEFAULT_FILTERS` L61–L68：industry `CL-SEI-01`/`INB1303`、region 深圳南山区） |
| `time_range` / `data_caliber` / `model` | §2.5 枚举 |

```json
{
  "code": 0,
  "data": {
    "composite_score": 76,
    "stage": "result",
    "dimensions": [
      {
        "key": "science", "title": "科学创造力指标展示",
        "score": 83, "score_trend": "up", "tone": "blue", "status": "较强",
        "summary": "科学论文产出活跃，合作网络结构稳定，研究前沿保持增长。",
        "metrics": [
          { "name": "论文数量", "full_name": "科学论文数量分析", "score": 86, "delta": "18.6%", "trend": "up", "metric_id": "Q0xx" }
        ],
        "indicator_intro": {
          "definition": "反映研究主体在所选领域内科学论文产出、合作网络位置、研究热点和未来趋势。",
          "sources": ["论文期刊数据库", "中文学术文献数据库", "学术知识图谱", "Crossref 元数据服务"],
          "method": "采用文献计量、引文网络分析与趋势预测模型，计算科学创造力综合得分。"
        },
        "metric_id": "Q0xx"
      }
    ],
    "process_tasks": ["论文合作网络分析", "专利质量评估", "产业成熟度分析", "政策文本分析", "德尔菲专家预判", "系统仿真预测"],
    "data_progress": [ { "name": "论文数据", "value": 85 } ],
    "chain_stages": [ { "label": "基础研究" }, { "label": "应用研究" }, { "label": "产业技术" }, { "label": "产品商业化", "full_label": "产品及商业化" } ],
    "policy_suggestions": ["…"],
    "filter_echo": { "time_range": "2019年 - 2025年", "data_caliber": "申报量 / 授权 / 公开", "model": "综合评估 - 系统仿真模型" },
    "metric_ids": ["Q0xx"]
  }
}
```

字段逐字对齐 `dimensionBaseConfigs`（L83–L174）+ `PROCESS_TASKS`（L176–L183）+ `dataProgress`（L185–L191）+ `chainStages`（L193–L198）+ `policySuggestions`（L200 起）。边界：
- `delta` 为字符串（含 `%` 或绝对值，demo 混用，如 L115 `2.6` vs L94 `18.6%`），契约统一为 `{ "value": number, "unit": "%"|"分" }` 结构化，**待 M0 确认**（U2）。
- `data_progress` 为数据就绪度展示，属 D9 就绪度族，**禁止伪造 100%**；真源为数据侧就绪清单。

### 3.2 `GET /v1/situation/innovation-evaluation/indicator-config` — 维度体系配置（只读）

**用途**（规划 M7-BE ③）：四维 + 二级指标 + 一级/二级权重（FE-TS-07b 指标 Tab，只读）。

```json
{
  "code": 0,
  "data": {
    "dimension_weights": [
      { "key": "science",    "weight": 25, "metric_weights": [25, 25, 25, 25] },
      { "key": "technology", "weight": 30, "metric_weights": [17, 17, 16, 17, 16, 17] },
      { "key": "industry",   "weight": 25, "metric_weights": [17, 17, 16, 17, 16, 17] },
      { "key": "policy",     "weight": 20, "metric_weights": [17, 17, 17, 16, 16, 17] }
    ],
    "metrics_catalog": [
      { "dimension_key": "science", "name": "论文数量", "full_name": "科学论文数量分析", "metric_id": "Q0xx" }
    ]
  }
}
```

权重逐字对齐 `DEFAULT_WEIGHTS`（L76–L81）。边界：权重为**只读**配置（本模块不开放编辑，区别于 M3 参数模板导入）；`metric_weights` 长度须与该维 `metrics` 数量一致（science 4 / technology 6 / industry 6 / policy 6）。

### 3.3 历史报告 + 预览

**用途**（规划 M7-BE ②）：历史报告 4 条 + 归档态（FE-TS-07c 报告中心）。

`GET /v1/situation/innovation-evaluation/reports`：

```json
{
  "code": 0,
  "data": {
    "total": 4, "page": 1, "size": 20,
    "records": [
      { "report_id": "RPT-2025-Q4", "title": "2025 年 Q4 科技创新评估报告",
        "period_key": "2025Q4", "region_scope": "shenzhen", "composite_score": 76,
        "report_status": "archived", "archived_at": "2026-01-15T10:00:00+08:00",
        "created_at": "2026-01-10T09:00:00+08:00" }
    ]
  }
}
```

`GET /v1/situation/innovation-evaluation/reports/{report_id}`：返报告快照（结构同 §3.1 result + 归档元数据）。

边界：`report_status` 枚举 `generated`已生成 / `archived`已归档（U3：是否含 `draft`）；报告为**快照**（归档后数据不随库更新），快照口径需在响应中带 `data_as_of`。

## 4. 数据需求与存储建议（Mock 先行 D7）

| # | 域 | 建议表名 | 关键字段 | 消费接口 | 备注 |
|---|---|---|---|---|---|
| 1 | 评估结果 | `ts_ie_result` | `region_scope, industry, field, time_range, data_caliber, model, composite_score, dimensions JSON, metric_id, calc_batch_id` | §3.1 | 算法产物 |
| 2 | 维度配置 | `ts_ie_dimension_config`（只读字典） | `dimension_key, title, weight, metric_weights JSON, version` | §3.2 | 权重版本化 |
| 3 | 历史报告 | `ts_ie_report` | `report_id, title, period_key, composite_score, report_status, snapshot JSON, data_as_of, archived_at` | §3.3 | 快照不可变 |
| 4 | 数据就绪 | 复用 D9 就绪度镜像 | `data_progress` | §3.1 | 禁伪造 |

## 5. 未决项

| # | 未决 | 归属 / 动作 |
|---|---|---|
| U1 | `model` 枚举与 M3 `eval_model` 是否同一字典（跨模块复用） | M0 拍板 |
| U2 | `delta` 结构化（`{value, unit}`）替代 demo 字符串混用 | M0 前端侧 |
| U3 | `report_status` 是否含 `draft`；归档触发动作（人工/自动） | M0 产品侧 |
| U4 | 四维分与综合分 `metric_id` 清单登记 | `ALL-TS-D9`，随批 4 评审 |
| U5 | 评估触发：M7 是否需异步任务（附录 E），还是只读最新结果 | M0 拍板（demo 无触发入口，仅展示） |

## 6. 自检（冻结前）

- [ ] 四维 `dimension_key` / 标题 / 权重与 `dimensionBaseConfigs` / `DEFAULT_WEIGHTS` 逐字一致
- [ ] 筛选枚举（time_range / data_caliber / model）与 L70–L72 逐字一致
- [ ] `metric_weights` 长度与二级指标数一致（4/6/6/6）
- [ ] 报告为快照（`data_as_of` 必返）；归档后不可变
- [ ] `data_progress` 不伪造 100%；缺数 / 空态与 M1 §5 一致

## 7. 会签记录（批 4 评审待签）

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 前端 | human:孔东 | 待签 | — |
| 后端 / 架构 | human:徐腾强 · human:李伟 | 待签 | — |
| 算法 | human:堂绍祖 | 待签 | — |
