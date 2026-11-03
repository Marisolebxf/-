# SITUATION-TS-TRACKING-PERSIST-L01 · 范围挂载与持久化回读（区域/时间/领域 + 历史与模板跨重启 + D9 缺口角标）

> 任务：`SITUATION-TS-TRACKING-PERSIST-L01` ｜ 状态：`integration`（等人工走查）｜ agent：`api-agent`
> 监管人：`human:唐绍祖` ｜ 仓：`lumen-svc-platform` + `lumen-ui-science-pc` ｜ 日期：2026-11-03
> 设计说明真源：`repos/lumen-ui-science-pc/docs/tracking-真评估接入设计.md`（§8–§12）

## 1. 目标

三件事必须"真"：① 评估范围（区域/时间/领域）**真的进 SQL**；② 评估历史与自定义参数模板**跨重启可回读**；③ 页面数字在指标库无已签收指标时**如实落 D9 缺口角标**，不挂错指标。

## 2. 落地实现

### 2.1 范围挂载（口径 → 参数 → SQL）

| 维度 | 链路 | 落地状态 |
|---|---|---|
| 时间 | 前端 `timeRange` → `evaluation/run` → 年度趋势 `year_from/year_to` | ✅ 生效（同时也决定热力图列区间） |
| 区域 | 前端 `regionSelection` → `collectSelectedRegionKeys()`（防「取字符串最后一个字符」退化）→ `location_id` → `ads_geo_yearly_metrics` 过滤 | ✅ 生效；无数据时**回落全量并如实回传**（不谎称已过滤） |
| 领域 | 前端产业领域（`CL-*` / `INB*`）→ display `resolveSubfieldIds()` → innov `GET /v1/meta/industry-clusters/industry-subfields`（读 `{dim}.subfield_topic_map`）→ `subfield_ids` | ✅ 生效（2026-11-03 接通，复用科技全域态势同一条真源） |

口径回传：`dataset.scopeEffectNote` 逐维度写「已生效 / 回落 + 原因」，前端页脚与筛选行提示**只读它**，不前端臆测。

**踩坑修复（重要）**：`meta.globalFilterDefaults.fieldScope` 原写死 `""`，前端把默认 `CL-FUT-05` 覆盖成空 → 领域**永远不生效**。
现改为下发 innov 集群目录首个 `mapped` 集群（实测 `CL-SEI-01`）；目录不可用时才留空，前端保持空选择并明说「未选领域」。

### 2.2 持久化回读

| 数据 | 表 | 实现 |
|---|---|---|
| 评估历史 | `tech_evaluation_history` | display `ensureHistoryLoaded()`（30s 节流重试、按 id 去重、升序、补 `finishedAt`、`recomputeHistoryTrend()`），文案 `buildHistoryNote()` 动态生成（不再写死「当前服务无数据源」） |
| 自定义参数模板 | `evaluation_template` | `ensureTemplatesLoaded()` + `buildTemplateStoreNote()`；保存/删除走 `parameter-templates` / `-remove` |

### 2.3 D9 缺口角标

`components/MetricGapHint.vue`：D1 `missing` → 红问号（`IconQuestionCircle` `#F53F3F`），点开只显治理引用
`DS-03-METRIC-OPEN-L01` / `Q-MO-DS03-01…06`，**不显伪 8 件套**；受 `?review=1` 门控、组件自闸。

> 已推翻早前"挂 7 条 `M_TECH_*`"的建议：`DS-03` 那 7 条 `d4_ingestion_status: mock`、seed `is_mock=true`、`ui_mount` 指向别的页 —— 挂上去即错挂。

## 3. 实测证据（2026-11-03）

- `POST /dataset`（`fieldValues=["CL-FUT-05"]`，`2000-2025`）→ `scopeEffectNote`：
  「时间范围：已生效…区域范围：…技术领域：已生效（经 `subfield_topic_map` 反查 **N** 个久新子学科，年度趋势按 `subfield_ids` 过滤）」
- 页面（默认 `CL-SEI-01`）→ 领域提示「已映射 **39** 个久新子学科（`subfield_topic_map`），参与取数」；同请求口径回传「技术领域：已生效」。
- 重启后回读：`[tracking] 已从库回读评估历史 9 条`、`已从库回读自定义参数模板 N 条`。
- D9：`?review=1` 下综合潜力指数旁 1 枚红问号，`aria-label=指标缺失说明：综合潜力指数`（结果页验证）。

## 4. 遗留与风险

1. **`DS-03-METRIC-OPEN-L01` 6 项开放未闭合**（2026-08-22 起停滞）→ 红问号无法翻转为 ⓘ，需治理侧推进。
2. 区域只取**第一个**城市 `location_id`（多选区域尚未做交叉过滤）；`regions` 层与年度指标不在同一粒度，需数据侧确认。
3. `subfield_ids` 上限 50（`resolveSubfieldIds` 截断），超集产业领域会被裁；如需全量需先确认下游 `IN` 长度与性能。
4. 历史/模板为「单机 MySQL + 内存缓存」形态，多副本一致性未验证。

## 5. 纪律

⚠️ 人工验收闸门（2026-10-20 裁定）：改动已本地 commit（前端 `e5c5085` / 后端 `44b7843` / 台账 `b0cfe7eb`），**未 push**，等 `human:孔东` / `human:唐绍祖` 走查通过后推 `origin/dev`。
