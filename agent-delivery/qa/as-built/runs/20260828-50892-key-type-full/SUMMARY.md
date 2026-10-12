# 重点企业类型分析 P0/P1 全量 · 20260828-50892-key-type-full

环境：http://111.198.38.90:50892/ · 账号 `admin` · 入口 `/enterprise/key-enterprise-analysis?workspace=type&view=type`  
过程：Playwright 打已发布前端；未改业务仓、未改用例/脚本判定。顺序按 `prompts/.../key-type/full.md`。

## 1. 结论

**P0 11/11 通过。P1 5/5 通过。Pass-N/A 0。Fail 0。**

主路径可用：侧栏进类型分析（不落到领域）、四组筛选默认全部、三张 KPI（本轮 0 家/0 类/0 个，记 observed）、地图/列表互斥、清单抽屉空态、区域级联与产业/类型多选、评审开关零泄漏、HTML 报告未付费导出禁用。

未点「重点企业领域分析」。未按企业查询导出口径要 PDF。

## 2. 分条（按脚本）

| 级别 | pass | n/a | fail |
|------|------|-----|------|
| P0 | 11 | 0 | 0 |
| P1 | 5 | 0 | 0 |

对应测试用例号：FUNC-00046～00061（1:1，见 coverage.md）。

| 脚本 | 用例 | 判定 |
|------|------|------|
| P0-01 | FUNC-00046 | pass |
| P0-02 | FUNC-00048 | pass |
| P0-03 | FUNC-00053 | pass |
| P0-04 | FUNC-00054 | pass |
| P0-05 | FUNC-00057 | pass |
| P0-06 | FUNC-00047 | pass |
| P0-07 | FUNC-00049 | pass |
| P0-08 | FUNC-00051 | pass |
| P0-09 | FUNC-00052 | pass |
| P0-10 | FUNC-00056 | pass |
| P0-11 | FUNC-00059 | pass |
| P1-01 | FUNC-00050 | pass |
| P1-02 | FUNC-00055 | pass |
| P1-03 | FUNC-00058 | pass |
| P1-04 | FUNC-00060 | pass |
| P1-05 | FUNC-00061 | pass |

## 3. Fail 列表

无。

## 4. Pass-N/A

无。

## 5. C4 清单（脚本/用例写错）

无。本轮未改 yaml/用例充绿。

## 6. 现场数据（不钉 expect）

- KPI：匹配企业数 **0 家**、覆盖企业类型数 **0 类**、覆盖区域数 **0 个**（0 合法）。
- 当前区域：**深圳市**；清单抽屉标题「深圳市企业清单」；空态「当前搜索条件无匹配企业」。
- 数据更新至：**2026-07-22**。
- 默认年份 2022–2026；P1-01 改为 2023–2026。
- 产业选项 8 个（含人工智能）；类型选项 7 个（含高新技术企业/专精特新/小巨人/链主龙头）。
- 热门城市 19 个。评审开 ⓘ `M_ENT_TYPE_COUNT`；未登记拟用 `M_ENT_KEYPANO_MATCH_COUNT` / `M_ENT_KEYPANO_REGIONAL_COUNT`。

## 7. 噪声（不升 Fail）

控制台多次 `[useCandidateLists] load failed CanceledError: canceled`（切页取消请求），非 5xx，无业务 X-Trace-Id。

## 8. 空目录自检

16 条 `scripts/{id}/` 均有 `result.yaml` + `steps.md`。KPI/清单/抽屉/筛选数据条另有 `observed.yaml`。
