# TOPIC-DS-METRIC-GAP-L01 · 专题+展示差集父单（L02 索引收口）

> 格式参考 `templates/handoff-template.md`。definition / fan-in。不写业务代码。  
> 本叶只做入口索引；分析在子叶完成。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:coordinator-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 两 L02 齐后写索引。L01 子叶冻结为指针快照。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义·索引；不以缩文档跳过子叶对照。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 子叶 yaml / summary 读原文。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 无 |

## 范围与实现

对照 A1 成品表，汇总专题+展示库外缺口与 mapped 对应关系。分析已拆到：

- `TOPIC-ALGO-GAP-L02`（done，missing 7→7）
- `DS-ALGO-GAP-L02`（本会话交卷，missing 70→70）

索引：`metrics/request/TOPIC-DS-METRIC-GAP-L01.md`。

## 偏离说明

- 原 DoD 写「仍挂 L01 两叶签完后 fan-in」。2026-08-24 改为等 L02；L01 不作 A1 对照签收。
- 父单 `depends_on` 登记表仍只列 A1；实际闸门是两 L02。

## 产物清单

- `metrics/request/TOPIC-DS-METRIC-GAP-L01.md`
- 本文件

## 验收证据

- 专题 missing 7 + 展示 missing 70（去重后），改判定行均为 0。
- mapped 专题 171、展示 204 均已填 A1 ID。
- 不改 seed。不重列共有缺口。
- **cicd: skip**

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ |
| 调用链 | ✅ |
| 图谱 | ✅ |
| 可观测 | ✅ |
| CI/CD | ✅ skip |
| D8/D10 | ✅ 无 UI |
| D9 | ✅ 不发明 `M_*` |
| D12 | ✅ 只改编排仓 |

## CI/CD（必填）

- 分支：编排仓 `dev`
- commit：无
- **cicd: skip**

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 20000（估；source: session_estimate；父单索引） |
| model_used | grok-4.6 |
| actual_cost | 0.12 |
| cost_warn | green |

## 遗留风险 / 开放项

- T0-X 仍等 `ALGO-LIB-SEED-TYPE-L01` 交稿 + 本两叶签收。
- L01 两叶看板仍 `in_progress`（冻结快照，不在本父单改状态）。
