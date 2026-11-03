# GRANULARITY-FIX-L01 · 多时间粒度趋势打通 + 年份滑块塌缩

> 状态：**integration（2026-11-01 完工：后端五档 curl 验证 + 前端三绿 + 浏览器实测通过；改动停本地未 commit 未 push，待 `human:李伟` 人工走查）**
> 监管人：`human:李伟` ｜ 仓：`lumen-svc-platform` + `lumen-ui-science-pc`
> 关联：WBS-05-18-13；同链路上一轮 `INFLUENCE-FIX-L01`（筛选联动排查）

## 一、用户指令与根因

- 指令原文：「还是不能改变 现在是时间范围；**需规明确写了 支持多时间维度查看，包括日、月、季、年等不同时间维度的趋势展示**」。
- 根因：筛选栏统一时间控件的**粒度按钮（日/周/月/季/年）从未接线**——前端 `granularity` 只有 ref（4 处引用全在展示层），不进任何数据请求；后端 9 个端点完全没有 granularity 概念。用户感知的「时间不能改变」此前一半是真（滑块不接三 Tab，已在上一轮修），另一半就是**粒度切换零效果**（本轮修）。

## 二、改造内容（全部真实重分桶，非摊薄）

| 层 | 文件 | 改动 |
|---|---|---|
| element | `EnterpriseController.trend` | 新增 `granularity` 参数（白名单 year/quarter/month/week/day），`registration_date` 是日粒度事实列 → SQL `GROUP BY` 按粒度重分桶：年=`YEAR()`、季=`CONCAT(YEAR,'-Q',QUARTER())`、月=`DATE_FORMAT('%Y-%m')`、周=`DATE_FORMAT('%x-W%v')`（ISO 周年 `%x`，避免跨年周归错年）、日=`DATE_FORMAT('%Y-%m-%d')`；白名单外回落 year（兼容旧调用）。分桶标签统一从 `stat_year` 列返回，下游零改动 |
| display | `RemoteElementClient.enterpriseTrend` | 签名加 `granularity`（defaultValue=year） |
| display | `SituationController.overview` | 读 `params.granularity` → `GRANULARITIES` 白名单校验 → 透传 element；响应新增 **`trendGranularity`**（回传实际生效粒度，让白名单回落可观测）；`/compare` 调用点显式补 `"year"`；Scope javadoc 粒度条目由「不参与」改写为「仅参与趋势分桶」 |
| 前端 | `types/situation.ts` | `SituationOverviewParams.granularity?`、`OverviewDataset.trendGranularity?`（注释写明诚实边界） |
| 前端 | `overview/index.vue` | overview watch 依赖加 `g: granularity.value`、请求带 `granularity` |
| 前端 | `OverviewTab.vue` | `trendGranularityMeta`：标题/轴注**以后端回传的 `trendGranularity` 为准**（年度/季度/月度/周/日趋势 · 按注册年/季/月/周/日），标题栏同时注明「仅企业序列（论文/专利/人才/项目/机构仅年度粒度）」；导出入口同步 |
| 前端 | `chartBuilders.ts` | `buildTrendMultiLineOption` 点数 >90 时 `showSymbol:false`（日粒度 11 年 ≈4k 点防糊；数据不抽样不截断，hover tooltip 仍在） |

## 三、诚实边界（D9，不伪闭合）

1. **粒度只改趋势图 X 轴分桶，不改样本**——「哪些企业被统计」仍由年份区间决定；KPI 总量/分布/影响力/聚类不受粒度影响（它们的数据源无子年粒度，不应假装有）。
2. **久新五要素（论文/专利/人才/项目/机构）物理只有年度粒度**（ADS 年度表），趋势图只载企业序列；标题栏如实写出，不把年度值摊薄成月/季。
3. 影响力 Tab（`node_influence` 无时间维）与聚类 Tab（散点无时间轴）不接粒度参数——不是漏接，是无数据事实可切。

## 四、验证证据

1. **element 直连（:7082，2020–2022）**：year=3 点 / quarter=12 点（2020-Q1→2022-Q4）/ month=36 点 / week=156 点（ISO W01–W52）/ day=890 点——**五档合计均 = 38,308**，重分桶不丢数不造数；非法粒度 `hourly` 回落 year（3 点）。
2. **display overview（:7099）**：`granularity` 透传四档与缺省（回落 year）全部符合，`trendGranularity` 回传与请求一致。
3. **前端三绿**：`vue-tsc --build` exit 0（修掉 `noUncheckedIndexedAccess` 下 `trendGranularityMeta` TS18048）、`npm run build` exit 0（1m3s）。
4. **浏览器实测（:3000）**：切「月」→ `/overview` 请求体含 `"granularity":"month"`、响应 `trendGranularity=month`、X 轴变 `2016-01…`、标题「月度趋势 · 按注册月」；切「季」→ `2024-Q1` 形、「季度趋势」；滑块塌缩回归：拖滑块到 2020 → 请求体 `startYear=endYear=2020`、实时数据企业 KPI 102,167→12,932、影响力/聚类同范围联动。

## 五、遗留与风险

- 日/周粒度点数大（4k/570 点）已用 `showSymbol:false` 处理；未加 dataZoom（不加非必要功能，需规未提缩放）。
- 事件 Tab 的 period 标签（`getTimelineEventPeriodLabel`）本就随粒度切换，无需后端改造；事件总量仍按年份过滤（与滑块/范围同口径）。
- ⚠️ 改动停本地未 commit 未 push（铁律：等 `human:李伟` 人工验收）。

## 六、改动文件清单

```
lumen-svc-platform:
  gkxlumen-element/.../controller/EnterpriseController.java        (trend 粒度白名单)
  gkxlumen-display/.../feign/RemoteElementClient.java              (granularity 参数)
  gkxlumen-display/.../controller/SituationController.java         (GRANULARITIES/透传/trendGranularity/javadoc)
lumen-ui-science-pc:
  src/types/situation.ts                                           (granularity / trendGranularity)
  src/views/situation/overview/index.vue                           (watch 依赖 + 请求参数)
  src/views/situation/overview/components/OverviewTab.vue          (趋势标题随粒度 + 诚实标注)
  src/views/situation/overview/models/chartBuilders.ts             (稠密 showSymbol)
```

## 七、Cost

| 项 | 值 |
|---|---|
| model_used | Kimi-K3 |
| actual_cost | 中等（后端 3 文件 + 前端 4 文件 + 双侧重启 + curl/浏览器双验证） |
| cost_warn | green |
| ponytail | 停本地待走查；走查通过后可随 INFLUENCE-FIX-L01 同批 commit |

## 八、追加修复 · 时间控件年份切换（2026-11-01 晚，同单）

用户指令：「现在时间控件还有问题 选择时间的时候 无法切换年份 切换完 想手动拉取进度条或者点击左右选择年份 就会随机变成某一年固定范围」。

### 根因（两处叠加）

1. **切片出口把区间塌缩成单年**：`emitSlice`（滑块 / 左右箭头 / 跳首尾共用）同时 emit `time-range-change {year, year}`，于是每拖一次，时间范围只剩一年。
2. **导航轴取的是塌缩后的区间**：滑块 `max` 与左右按钮的索引都基于 `rangeYears`（区间内年份），塌缩后长度为 1 → `max=0`、索引恒为 0 → 再也切不动年份，表现为「固定在某一年」。
3. 附带的布局缺陷：面板原为「快捷列 112px + 主列」两列网格；本次移除点击无反应的快捷列后主区被挤进 112px，滑块渲染宽度 0（首轮浏览器实测发现，已修）。

### 改造（按用户两项裁定）

- **裁定一**：拖动滑块 / 点左右箭头**只切换当前年份，时间范围保持不变**。`emitSlice` 只 emit `current-year-change`；区间仅由开始/结束年份下拉（`updateRange`）设定。
- **裁定二**：月/季/周/日 精度下面板的静态日历与 Q1–Q4 按钮换成**可用的年份轴**。删掉演示件（`calendarDays` / `quickActions`）；年份滑块与左右切年按钮对所有粒度常量显示；面板内补 `granularityHint`（子年粒度只影响趋势分桶与事件时间标签，切片仍按年；区间收成单年时用下拉扩大）。
- 导航轴仍取「区间内年份」：保证 `currentYear` 与 `timeRange` 不自相矛盾（否则会出现「区间 2016-2026、当前年 2029」这类请求）。
- 触发按钮文案由 `{{ granularityLabel }}粒度 · {{ currentText }}`（含硬编码 Q2 / -05 / 第19周 假切片）改为 `{{ granularityLabel }}粒度 · {{ safeSlice }}`；面板标题同步取 `safeSlice`。

### 验证

- `npx vue-tsc --build` exit 0（两轮）；`npm run build` exit 0。
- 浏览器实测（:3000，两轮）：①「›」连续点击年份逐级变化、区间文本保持 `2016-2026` 不塌缩；②鼠标真实拖动滑块（非脚本赋值）年份随之变化，之后再点「›」仍可继续切年；③切「月」粒度后年份滑块仍在、箭头仍能切年；④面板单列布局、滑块可见可拖（0px 宽度已消除）；⑤控制台无 error。

### 改动文件（增量）

```
lumen-ui-science-pc:
  src/views/situation/overview/components/SituationFilterBar.vue  (导航轴/emitSlice 去塌缩/移除假日历与季度按钮/粒度说明)
  src/views/situation/overview/styles/demo-situation.css          (面板单列 + 删除 __quick 死样式)
```

> 语义变更说明：本轮按用户最新裁定，**废止此前「滑块塌缩驱动三 Tab」的交互**（实时数据/影响力/聚类不再随滑块联动，只随开始/结束年份下拉设定的区间联动）。仍停本地未 commit 未 push。

