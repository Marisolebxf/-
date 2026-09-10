# 派单包 · CROSS-VEC-SAD-L01

```yaml
task_id: CROSS-VEC-SAD-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:淮政玮
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: N/A
```

> 调度者只建单、写厚包。**不写业务代码。** 执行前须 confirm → ready → 认领。

## 1. 为什么派

产业对齐缺少跨系统 SAD。稿已在 `跨系统-向量库/`（**v0.3-draft**，含 ETL 跑批 §3.1/§3.2）。本叶是 **会签关门**。

## 2. 范围 / 不做

**做**：三卷+INDEX+导读定稿会签；冻结：

1. 建库 = 灌链末段一次 `embed/rebuild`
2. 重灌同步 = 仅 L0+L1，不调 Milvus/LLM
3. 消费 = 按钮 **或** ETL Job A/B（非重灌内）
4. Milvus 共用实例、禁止 `amcpdp-*`
5. 与知识图谱 Hang 夜班顺序对齐（先槽后边）

**不做**：OpenAPI 生产契约；改业务仓；采购向量云；文档 RAG。

## 3. 必读

- `跨系统-向量库/` 全目录（尤其 02 §3.1–3.2）
- `跨系统-知识图谱/` 02 §3.1–3.2（Hang ≠ G3）
- `architecture-baseline.md` D1–D12

## 4. /goal

```text
/goal architect-agent
身份：资深系统架构师；只评审与维护基线，不写业务代码。
任务：CROSS-VEC-SAD-L01
目标：跨系统向量库 SAD 会签关门（v0.3-draft，含 ETL Job A/B 切面）。
仓库：${GKX_ROOT}/gkx-orchestration（agent-delivery）
必读：跨系统-向量库 INDEX+01/02/03；跨系统-知识图谱 02§3.1。
铁律：向量不替代建图；重灌不上图/不 search；Job A/B 为长任务；禁止 amcpdp-*。
冻结：建库=灌链末段 rebuild；夜班 Job A→Hang；G3 分析不是上图。
产出：会签写入 SAD 封面；handoff CROSS-VEC-SAD-L01.md（cost）。
禁止：改 lumen-* 业务代码；当生产 OpenAPI。
```
