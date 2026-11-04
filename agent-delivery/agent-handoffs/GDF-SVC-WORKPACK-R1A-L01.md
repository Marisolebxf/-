# GDF-SVC-WORKPACK-R1A-L01 · 服务机构 GDF 派单包 round1 答复落地

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（文档 / 派单包修订） |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-GDF-DWD-ENTRY-20261104` |
| 图 diff | 去掉 &lt;10 整表回退与「无 id 停工」；改为 ODS 读 + 复合键 md5 |
| 会签态 | draft（包内 mermaid） |

## 范围与实现

将 GDF round1 十二问拍板写入 `GDF-SVC-WORKPACK` v1.1，并回写 `storage/SVC` 冲突条款（fallback、A5 period、event_id 注释）。产出 round2 答复材料供对方关闭提问。

对照 bid / 加工链路：服务机构圈定 + 事件 + A1–A6 后加工包，不建作业、不灌数。

## 偏离说明

- 源表由「只读供应方四表」改为「读 `gkxlumenx_ods` + 联读 product.main_activities」（Q0/Q4）。
- `event_id` 唯一键由三列改为单列（Q1）；正式库需 ALTER，本单只改文档快照。
- `svcseed` 代码内 fallback **未改**（遗留：另单或本域代码叶关掉）。

## 产物清单

- 包：`agent-delivery/data/GDF/派单包/服务机构/GDF-SVC-WORKPACK/`（00/01/04/06/08/09/10/11/12/13/README/CHANGELOG + round2/）
- storage：`seeds/svc_rule_demo_kw_v1.md`、`seeds/README.md`、`etl/ods-to-ads-mapping.md`、`etl/ods-to-dwd-mapping.md`、`02-asbuilt-process-chain.md`
- 对接：`…/GDF侧提交/…/round2/02-answers-round1.md`

## 验收证据

- 文档 diff 自检：包内无「禁读 ODS / 源 id 停工 / 不足 10 整表入池」作为现行规则
- DDL 快照唯一键为 `UNIQUE(event_id)`
- 未执行建表 / 未灌数 / 未改 demo seed 代码

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本单无 Java 算法 |
| 调用链 | ✅ 不涉及前端越层 |
| 图谱 Nebula | ✅ 本包不写图 |
| 可观测 | N/A 文档叶 |
| CI/CD | 文档推 `origin/dev` |
| demo2 只读 merge | ✅ |
| D12 lumen≠demo 服务 | ✅ |
| D14 桶 | N/A |

## cost（回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~45000（估） |
| model_used | Composer |
| actual_cost | ~1.5（估） |
| cost_warn | green |

## 遗留风险

1. 正式库 / demo 库 `uk_svc_finance_event` 仍为三列唯一键，GDF 开工前须 ALTER。
2. `entan/svcseed.py` 仍含 `hits <10 → fallback all`，与包不一致，需代码叶关闭。
3. `05` 签字栏仍空（Q7 流程项）。

## CI/CD

- 分支：`dev`
- commit：（本 handoff 同批推送）
- pipeline：编排仓文档无业务 CI
- K8s：N/A
