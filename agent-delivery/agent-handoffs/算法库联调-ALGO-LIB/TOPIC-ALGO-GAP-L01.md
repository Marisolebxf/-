# TOPIC-ALGO-GAP-L01 · Round 17 指针返工

> 格式参考 `templates/handoff-template.md`。定义类；**不写业务代码、不改 seed、不签收、不 commit。**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | METRIC-OPEN-LOOP Round 17。旧版淮政玮指定不签收。本轮只改指针 + 分类。状态留 `in_progress`。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义·文档类 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 指针返工；未压缩会签原文 |

## 相对旧版 diff：指针 / 计数

**指针**：11 页 catalog `metric_open_status` missing → present（SVCCHAIN×4、TOPIC-ENT/TECH/ORG/TALENT/QUERY、E7-POLICY、SYNTH-REGION 父索引）。E7-POLICY **已删**「METRIC-OPEN-E7-DS10-12 是展示政策跟踪，勿误用」，改挂 `POLICY-METRIC-OPEN-L01`。SYNTH-REGION 挂父索引（`metric_open_role: parent_index`），三兄弟 OPEN 路径已在 catalog，不另建叶。CHAIN 补 present，禁止 missing。ZHIKU 专题 n/a，未新增 `TOPIC-ZHIKU`。TOPIC-OPS / TOPIC-DATAREQ 保持 n/a。

**计数**：缺 OPEN 叶 11→**0**；库 missing **7→7（未改 mapped）**。mapped 171 / third_party 10 / other_system 39 / n/a_ops 23 / 语义欠账 111 条数不变。SVCCHAIN 29 `M_SVC_*` 仍 mapped。

## 范围与实现

协议 `METRIC-OPEN-LOOP-循环工程.md` §4 Round 17。指针真源 `_work/METRIC-OPEN-LOOP-a2-patch.yaml`。会签通过**仅指指针返工口径**。旧版不签；库 missing 未改。禁止开工 `DS-ALGO-GAP-L01`。8/25 前不派唐绍祖。不改展示 catalog、不改 LOOP-state、不改 seed。

## 产物清单

- `metrics/request/专题系统/A2-GAP-page-catalog.yaml` + `pages/*.yaml`
- `metrics/request/专题系统/TOPIC-ALGO-GAP-L01.yaml` / `-summary.md` / `.xlsx` / `.md`
- 本文件

## 验收证据

- 缺 OPEN 叶 0；库 missing 7。
- 展示 catalog 未动。
- **cicd: skip**。不签收。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 调用链 | ✅ |
| Nebula | ✅ |
| D9 不发明正式 `M_*` 进 seed | ✅ |
| CI/CD | ✅ skip |
| D12 | ✅ 只改编排仓 |

## CI/CD（必填）

- 分支：编排仓 `dev`（未 commit）
- **cicd: skip**

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000（估） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 2.8（估） |
| cost_warn | green |
