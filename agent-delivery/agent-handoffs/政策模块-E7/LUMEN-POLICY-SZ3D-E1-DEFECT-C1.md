# 段 E 缺陷包 · 深圳政策现状金路径 4

| 字段 | 值 |
|------|-----|
| 管线 / 总控 | `LUMEN-POLICY-SZ3D` / `LUMEN-POLICY-SZ3D-长任务总控.md` §2 第 4 条 |
| 故事 ID | `US-E7-POL-04` |
| 已发布 URL | http://10.50.69.111:30892/policy/recommendation |
| 操作步骤 | 登录后打开深圳政策现状。未选锚点时开始分析禁用。选「新一代信息技术 / 半导体与集成电路」后提交。再选另一产业（任务 `POLICY-20261025-011`，`industry_vid=chain:INB1702`）提交。打开结果板。 |
| 期望 | 更换产业后，支持力度城市截面分数不变；适配性请求范围变化。 |
| 实际现象 | 支持力度不变：两条任务分数都是 32.6694，名次 5，条数 879，层级均值 0.4579。适配性没有变化：两条结果都是 `reason=未提供链名`，`anchor_name` 为空，`hit_count=0`。页面锚点标题能显示「半导体与集成电路」，适配卡不使用这个名称。 |
| HTTP / 页面态 | 创建任务 HTTP 200，任务 `success`。结果页三张卡都在。不是 5xx，不是白屏。 |
| **失败分类** | C1 产品/代码 |
| **X-Trace-Id** | `cd3b7cdd8c4c4e9199458eabbdf590e8`（创建 `POLICY-20261025-010` 的响应头） |
| Tempo | `http://10.50.69.111:30202/api/traces/cd3b7cdd8c4c4e9199458eabbdf590e8` 有约 40KB 链路。Grafana `http://10.50.69.111:31300` 数据源 Tempo，TraceID 用同一值。 |
| Loki | 本包未从 Loki 摘错误行。任务已成功，失败在口径没用上产业名，不是异常栈。 |
| 怀疑层 | FE。具体产业只提交 `industry_vid`，不提交 `industry_name`。Python `polan/job.py` `_shenzhen_anchor` 只把 `industry_name` 交给标题匹配，VID 不参与针词。Java 已把 `industry_vid` 写入 `input_payload`。 |
| 诚实空态？ | 否。选了具体产业仍写「未提供链名」，不是允许的空态。 |

对照任务（同一已发布环境，`user_id=guest`）：

| 任务 | 请求锚点 | 支持力度分 | 适配性 |
|------|----------|------------|--------|
| `POLICY-20261025-010` | `industry_vid=chain:INB170101`，无 `industry_name` | 32.6694 | 未提供链名 |
| `POLICY-20261025-011` | `industry_vid=chain:INB1702`，`industry_id=INB1702`，无 `industry_name` | 32.6694 | 未提供链名 |

`_chain_needle` 还会把含「全部」的名称收成空针。集群「全部」也会得到同一句原因。本包的红是具体产业：名称根本没进计算。

```text
/goal
你是经验丰富的 frontend-agent。
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
强度：ponytail full。
必读：本缺陷包 + 长任务总控 + observability.md §9。
禁止：改无关仓；无闸门写正式库；问用户选仓。
修完 push origin/dev；handoff 写清 commit 与是否需要 devops 再确认 rollout。
根因：具体产业提交时带上页面上的产业名称（industry_name），同时保留 industry_vid。不要改支持力度的城市截面，不要把 null 写成 0。
```
