# FIX-POL-CMP-SEARCH-L01 · 政策详情对比候选下拉连库搜索

- **仓 / commit**：`lumen-ui-science-pc` · `5d3b636`（2026-11-05 已推 `origin/dev`）
- **类型 / 状态**：bugfix · in_progress（完工即推，待 CI 部署后 QA 复测）
- **强度**：ponytail full
- **认领 / 监管**：`agent:frontend-agent` / `human:淮政玮`
- **强度行**：ponytail full（最小 diff，2 文件 35+/8-，零新依赖）

## 走查问题

政策详情对比弹窗（214），候选下拉输入「广东」显示「暂无数据」；无法连库搜索到目标政策
（如 `18363390` 广东省科学技术厅工作方案、`18407696` 深圳市外国人来华工作许可工资标准），
只能从打开时预载的固定列表里挑。

## 根因（代码 + 产线数据双重核实，2026-11-05 只读探测）

1. **前端只拉一次首页**：`ComparisonModal.vue#loadLiveOptions` 仅在弹窗打开时调
   `panoramaSearch({})`——不带关键词、不带分页。Python 侧 `search_policies`（`polan/search.py`）
   默认 `ORDER BY publish_date DESC, policy_id LIMIT 20`。
2. **产线首页被脏数据霸屏**：`gkxlumenx_dwd.policy_base_info` 共 40000 行有效，
   首页 20 条全是 `publish_date=9999-01-01/2999-01-01` 的国际政策行（外文标题）。
   目标两条 2022 年政策排在数千页之外，候选框永远拉不到。
3. **输入只做本地过滤**：`a-select` 无 `remote`，输入只在已载 20 条里过滤，故必空。
4. 后端 `keyword` LIKE 契约早已存在（`search_policies(keyword)` /
   `buildPanoramaSearchQuery` 的 `query.keyword`），只是前端没接。

## 修复内容（前端 2 文件）

| 文件 | 改动 |
|---|---|
| `src/views/policy/panorama/components/ComparisonModal.vue` | `a-select` 加 `remote` + `@search="onLiveOptionSearch"`；`loadLiveOptions(keyword)` 支持关键词（空回落首页默认 20 条）；300ms 防抖；并发序号守卫（`liveSearchSeq`）只认最后一次输入；搜索失败不清已返回候选（沿用「读失败不清已返回块」语义） |
| `src/views/policy/panorama/FE-POL-CMP-LIVE.test.mjs` | 新增 4 条断言：`@search` 接防抖远程搜索 / `remote` 模式 / 防抖函数在场 / `loadLiveOptions(keyword` 连库入参 |

后端零改动（display / element / polan 均未动）。

## 验证

- `FE-POL-CMP-LIVE.test.mjs` 全绿（含新增远程搜索断言）
- 政策族 14 个自检回归：12/14 绿；`FE-POL-06A` / `FE-POL-04A` **基线即红**
  （stash 掉本单改动后复测仍红，reviewMode 断言相关，存量问题不属本单，未修）
- `pnpm type-check`（vue-tsc --build）绿，EXIT=0

## 测试政策对（六维全有值，2026-11-05 产线库只读核实）

| 维度 | 18363390 | 18407696 |
|---|---|---|
| 申报时间 | 2022-04-06 | 2022-06-15 |
| 受理部门 | 广东省科学技术厅 | 深圳市科技创新委员会 |
| 产业类别 | 政策文件-管理办法/实施方案 | 其他通知 |
| 申报条件/材料 | gapfill 行有值 | gapfill 行有值 |
| 支持力度 | 32.5（policy_intensity，mock_20260623 批） | 32.5 |

备选对：`18358888`（北京市）/ `18359216`（上海市）。绕行路径不变：检索页勾选 → 对比条开始比对。

## 复测口径（CI 部署后）

弹窗候选输入「广东」→ 下拉出现含两目标的候选；选中 2 条 → 开始对比 → 六维有值；
计算支持力度 → 力度分回填（依赖 FIX-POL-INTENSITY-FP-L02 `aba7c0a` 已部署）。

## 已知边界（不在本单修）

- 首页默认 20 条被 `publish_date=9999/2999` 国际行霸屏——首页候选质量口径属数据侧决策
  （是否过滤 `source_plane` 或封顶日期），待登记客户决策清单。
- 06A/04A 存量红。

## 架构合规自检

| 条 | 结论 |
|---|---|
| 调用链不越层 | ✅ 前端 → display `/display/v1/policy/panorama/search`，零新端点 |
| D9 诚实性 | ✅ 无行空态不造数据；失败不清已返回候选 |
| I2-12 | ✅ 切输入不起分析任务；watch 仍只做复位（断言未松） |
| D12 | ✅ 只调 gkxlumen 链 |
| ponytail | ✅ 最小 diff，复用既有 search 契约 |

## Cost 回填（估算）

| 字段 | 值 |
|---|---|
| actual_tokens | 60000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.03 |
| cost_warn | green |
