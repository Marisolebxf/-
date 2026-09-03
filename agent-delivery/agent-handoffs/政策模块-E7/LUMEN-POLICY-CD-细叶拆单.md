# C/D 细叶拆单 · 政策分析 E7 专题

> **管线**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> **切法**：C = 一对外 REST 路径一叶；D = 一实施权威故事一叶 + 共享壳。  
> **对照 Demo**：`demo-ui-topic` `/policy/search|overview|analysis|recommendation` · `/policy-portal/overview` · `/policy/maintenance`  
> **禁止**：把 `demo-algo-ent-analysis` 的 `/v1/policy/mock/**` 做成专题 C 路径。

---

## 1. C · REST 路径叶（`gkxlumen-topic-policy`）

对外前缀一律 `/topic/v1/policy`。下游 Feign 只打 `lumen-algo-py` `/internal/policy/**`。

| 建议 task-id | 方法 + 路径 | 覆盖故事 | 闸门 |
|--------------|-------------|----------|------|
| `LUMEN-POLICY-C-BOOT-L01` | 模块/网关骨架（Nacos、helm、`gkx-gateway` 路由） | — | 先于路径叶；**不算**完成门面 |
| `LUMEN-POLICY-C-SEARCH-L01` | `GET /topic/v1/policy/search`（+ 详情 `GET /{id}`） | US-E7-POL-01c | D 查询叶依赖 |
| `LUMEN-POLICY-C-GRAPH-L01` | `GET /topic/v1/policy/graph` | 配置页关联语料 / 图谱只读 | source 诚实 |
| `LUMEN-POLICY-C-METRICS-L01` | `GET /topic/v1/policy/metrics` · `GET /indicators` | 三项结果 KPI | D9 ⓘ 由前端消费 catalog |
| `LUMEN-POLICY-C-TASK-L01` | `POST/GET /topic/v1/analysis/tasks`（policy types）+ result | US-E7-POL-02/03/04/06 | 扩 async-service；I2-12 单飞 |
| `LUMEN-POLICY-C-PORTAL-L01` | `GET /topic/v1/policy/portal/**`（概览/覆盖/动态/深圳） | US-E7-POL-08 | P1，不挡 E |

同一 path 的 GET+POST 可同叶。Job 真源在 async-service，C-TASK 叶写签发 snapshot。

废作路径：`/v1/policy/mock/**`、直透 `/v1/policy/graph/hang` 给前端（图谱写操作留算法库联调台）。

---

## 2. D · 故事叶（`lumen-ui-topic`）

对照 USM `产品整体定义/E7-政策分析/USM-E7-政策分析.md`。每叶 `/goal` 必须有范围清单 + 复刻五维。

| 建议 task-id | 故事 | 路由 / 范围 | 金路径 |
|--------------|------|-------------|--------|
| `LUMEN-POLICY-D-SHELL-L01` | 菜单 + `src/api/policy` 薄封装 + 产业篮「政策分析」分组 | 侧栏；**不**占完成页 | 闸1 |
| `LUMEN-POLICY-D-POL-01c-L01` | US-E7-POL-01c | `/policy/search`（V1–V7） | #1 |
| `LUMEN-POLICY-D-POL-01-L01` | US-E7-POL-01 / 01b / 05 | 产业篮分发 + 三分析配置页对象栏 | #2（旧：篮发起） |
| `LUMEN-POLICY-D-POL-01-SCOPE-L01` | US-E7-POL-01 / 01b | 三项分析配置页产业选择对齐 demo：集群(map)→L0；**不强制对比篮** | #2 人审修正 |
| `LUMEN-POLICY-D-WAITVIEW-L01` | US-E7-POL-06（复用 SystemTaskLayer） | wait_view；禁止复制队列 | #3 依赖 |
| `LUMEN-POLICY-D-POL-02-L01` | US-E7-POL-02 | `/policy/overview` 工作区 W1–W3 | #3 |
| `LUMEN-POLICY-D-POL-03-L01` | US-E7-POL-03 | `/policy/analysis` | #4 |
| `LUMEN-POLICY-D-POL-04-L01` | US-E7-POL-04 | `/policy/recommendation` | #5 |
| `LUMEN-POLICY-D-POL-08-L01` | US-E7-POL-08 | `/policy-portal/overview` 四 Tab | P1 |
| `LUMEN-POLICY-D-POL-07-L01` | US-E7-POL-07 | 报告 HTML→PDF（ENT-EXPORT） | P1 |
| `LUMEN-POLICY-D-POL-09-L01` | US-E7-POL-09 | `/policy/maintenance` 复用 ENT-OPS 壳 | P1 |

`US-E7-POL-01b` 配置页 XOR 锚点并进 `POL-01` 叶；**产业选择人审修正**走 `LUMEN-POLICY-D-POL-01-SCOPE-L01`（集群→L0，不强制篮）。

---

## 3. DAG（与总控 §3 一致）

```text
C-BOOT → C-SEARCH ─┬→ D-SHELL → D-POL-01c
                   └→ D-POL-01
C-TASK → D-WAITVIEW → D-POL-02 / 03 / 04
C-GRAPH / C-METRICS 按分析叶需要穿插
C-PORTAL → D-POL-08（P1）
```

闸4 = D-SHELL + D-WAITVIEW + D-POL-01c + D-POL-01 + D-POL-02 + D-POL-03 + D-POL-04 均 ≥ pending_test。
