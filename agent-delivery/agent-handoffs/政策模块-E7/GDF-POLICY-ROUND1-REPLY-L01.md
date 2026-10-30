# GDF-POLICY-ROUND1-REPLY-L01 · 政策包 v2 round1 回包签收与答复

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-30 用户口令开始执行。锁至 MCP 返回的 `lock_until`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 脚本只加补偿软删和状态备注，判定放在已有 `--self-check`。未新建测试框架。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未用压缩。交付说明和两份脚本按原文对照。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 未改 `01-data-flow.md`，未改 POLICY 存储流图 |
| 会签态 | 不适用 |
| 说明 | `script_state` 若以后收成写库边，另开会签。本叶不建边。 |

## 问题清单

- 回包指纹按 LF 与交付说明一致。CRL 检出时整文件哈希不同。
- 不确认「五个核心函数全部逐字节一致」。C2 `structure_one` 已按交付说明改成按内容指纹跳过。
- `policy_support` 字面 `'null'` 已确认是源上就没有。清重口径仍待确认。嵌入服务的 NodePort 数字未写入包。
- 建议 A–D 已于 2026-10-30 确认并写入设计。产线未建 `script_state`，现网未 ALTER。清重口径仍待确认。

## 修改内容

- 新增 `22-round1回包签收与答复.md`，第 4 节改为已确认。
- `scripts/` 换为 round1，并加上 C1 补偿软删、C2 只备注。
- `12`、`15` 写上状态表、退出码 7、`--force` 必须带 `--policy-id`。
- 新增 `10/script_state-MySQL.md`，`dwd.md` 增加同结构一节。目标键写在 `dwd.md`、`ads.md`、`10`、`14` 的旁注，没有可执行的改表语句。
- `README.md`、`CHANGELOG.md` 记为 v2.0.4。

## 测试结果

- 用 LF 归一后的 SHA-256 核对回包两份 Python，与交付说明指纹一致。覆盖进包之后又加了补偿，包内文件不再等于该指纹。
- 两份脚本 `--self-check` 通过。未连库，未执行 `script_state.sql`，未 ALTER。

## 遗留风险

- 对方自述的 40,000 行和退出码未复核。
- 代理机经 `10.50.69.111` 加 NodePort 访问嵌入服务。清单仍是 ClusterIP，NodePort 数字未写入包。
- Milvus 地址按 `10.50.69.111:19530` 写入答复。没有从代理机再探测。
- 锚点：要等产业链产线完成并做「产业链入向量库」才产生。政策 C1 不建锚点。
- `LLM_API_KEY` 测试密钥写在 `22` 第 6 条和 `12` 环境表。`script_state` 产线未建，缺表时退出码 4。
- 目标唯一键未加到现网。清重口径未定。`policy_support` 字面 `'null'` 是源上就没有，不回刷。

## CI/CD（必填）

| 项 | 值 |
|----|-----|
| cicd | `skip` |
| 说明 | 定义类。只改编排仓文档。 |

## 可观测性（建议）

无运行时改动。

## 涉及文件

- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/22-round1回包签收与答复.md`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/scripts/policy_c1_industry.py`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/scripts/policy_c2_clauses.py`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/12-DWD后加工-抽取产业与条款结构化.md`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/15-GDF触发调度与回执.md`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/10-DWD-MySQL-DDL/script_state-MySQL.md`
- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/dwd.md`
- `agent-delivery/data/data-design/storage/POLICY/stores/mysql/ads.md`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/README.md`
- `agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/CHANGELOG.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 调用链 | 未改。仍是 GDF 节点跑包内 Python，不配内部 HTTP |
| 不改产线表 | 是。未执行 DDL，未 ALTER |
| 不代替 WBS-06-03 | 是 |
| D12 | 未改 lumen 仓，未调用 demo 服务 |
