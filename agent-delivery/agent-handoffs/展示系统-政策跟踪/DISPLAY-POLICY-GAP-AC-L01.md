# DISPLAY-POLICY-GAP-AC-L01 · 展示政策原型 档A 37条+档C校验闸门

> 本地未 commit / 未 push。供淮政玮在 `demo-ui-science` 验 demo。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-08-19 授权：档 C 按拆点补闸门；37 条拆 loop+多子 agent；核增不单独拆；禁提交 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D9 MockBadge / 闸门 Empty；禁止真爬虫/真 NLP |

## 问题清单

- 档 A 37 条能力未实现 + 档 C 94 条校验闸门（T124 档 D 不派前端）要在 `demo-ui-science` Mock 可验收。
- 档 B 106 条本单不做。

## 修改内容

分 6 簇改政策跟踪页，默认完成态，关 Switch / 清空 Select → disabled + Empty。

| 簇 | 页 | 档 A | 档 C |
|---|---|---|---|
| 1 全景 | `PolicyPanorama` | #1–#9 升序/二次筛/优缺点/需求/意见/换企业匹配/对标按政策 | T36–T39 共 24 |
| 2 分析 | `PolicyAnalysis` | #11–#16 优劣筛/模拟归档/排期/汇报流转 | T41+T42 共 16 |
| 3 预估 | `EstimateWorkbench` + 页头综合分闸门 | #17–#23 产业图/创新预测/区域政策类型/四项识别 | T43 共 8 |
| 4 推演 | `InterpretWorkbench` | #24–#27 选文本/非导图图表/覆盖面/历史路径 | T44 共 18 |
| 5 区域 | `analysis/*` | #10 资源投向筛选 | T40 共 7 |
| 6 核增 | `PolicyPcPages` | #28–#37 指标库/海外/细则/metrics 下游/对比参数/行业数据/权威源 | T125–T140（跳过 T124、不改 T132 能力）共 21 |

页顶维度条 `resourceTarget` 已接到 `RegionGroupCompare`。产业影响图随新出台政策 Select 缩放。

## 测试结果

- `node tests/display-policy-gap-ac-sort.test.mjs`：效力/浏览量升序 + 发布日期二次筛（起点晚于终点不切片）
- 页面验收步骤见 `qa/total-set/KJXXZSXT/fp-proto-diff-run/loop-DISPLAY-POLICY-GAP-AC/DONE-*-*.md`

## 遗留风险

- 档 B 未做（真导出、雷达随筛重算、报告静态草稿等）
- T124 清洗不派前端
- 未 commit，K8s/CI 未发；仅本机 `pnpm dev`

## CI/CD（必填）

- 分支：`demo-ui-science` 工作区脏，**未提交**
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未发
- dev 测试 URL / 命令：`pnpm dev` → `http://127.0.0.1:4176` ；侧栏科技政策跟踪：
  - `policy-panorama` 科创政策全景
  - `policy-analysis` 政策分析评价
  - `policy-simulation` 政策效果推演（预估 / 推演）
  - `policy-governance` / `policy-parse` / `policy-compare-upgrade` / `policy-insight-report` 核增链路

## 可观测性（建议）

- 演示页沿用已有 MockBadge / MetricSpecTrigger，未接新 OTel 服务

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 前端仅 mock，无真 NLP/爬虫 |
| 调用链 | ✅ 未直连 Python |
| Nebula | ✅ 未引入 Neo4j |
| 可观测 | ✅ 沿用页内埋点/角标，未减 |
| D8 | ✅ 未新加 npm；沿用 antd 本页栈 |
| D9 | ✅ 统计旁 MockBadge / ⓘ 保留 |
| D10 | ✅ 闸门 Empty + disabled |
| D12 | ✅ 只改 demo-ui-science |

## 涉及文件

见各 `DONE-*.md`；编排仓 loop 目录：`agent-delivery/qa/total-set/KJXXZSXT/fp-proto-diff-run/loop-DISPLAY-POLICY-GAP-AC/`
