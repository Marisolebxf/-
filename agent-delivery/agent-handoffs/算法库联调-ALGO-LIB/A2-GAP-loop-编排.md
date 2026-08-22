# A2 差集 · 按页面包编排（2026-08-22 改）

> **任务**：`TOPIC-ALGO-GAP-L01`（A2.1）→ 完成后才 `DS-ALGO-GAP-L01`  
> **监管**：`human:淮政玮` · **执行**：`agent:algorithm-agent` 子会话  
> **截止**：2026-08-24 下班前  
> **页面包清单**：[`metrics/request/专题系统/A2-GAP-page-catalog.yaml`](../../metrics/request/专题系统/A2-GAP-page-catalog.yaml)  
> **状态**：[`metrics/request/A2-GAP-loop-state.yaml`](../../metrics/request/A2-GAP-loop-state.yaml)  
> **页面产物 schema**：[`metrics/request/专题系统/pages/_schema.md`](../../metrics/request/专题系统/pages/_schema.md)

## 方法（相对 T00 的 129 叶平铺）

1. **粒度** = 产品定义叶子（四件套目录），不是 SRS 五级句，不是 Wireframe 每一画板。  
2. **先核语义层**：`METRIC-OPEN` / TRACE.`metrics` / Wireframe 第 6 列 / 算法定义卡。这是本页算法需求。禁止从 USM 叙述发明 `M_*`。  
3. **再对照**算法库 `srs/05` 97 叶 + 已实现（B 轨 63+29）。  
4. 三类不要混：A 库缺口 / B 语义欠账 / C 已覆盖。  
5. 子 agent 只写 `pages/{page_id}.yaml`；fan-in 由父会话合并四件套。

## 波次

| 波 | 内容 | 并行 |
|----|------|------|
| W1 | 产业链 4 叶：全景 / 诊断 / 区域 / 深圳 | 4 子 agent（本波启动） |
| W2 | 服务链 4 叶 | 等 W1 交齐 |
| W3 | 政策 1 + 综合 4 | |
| W4 | 企业/技术链/科研/人才（05.x 边界 + 语义欠账） | |
| W5 | 查询 + 运营 n/a_ops + 数据需求 other_system | |
| FANIN | 合并 yaml → xlsx + summary + handoff | 父会话 |
| A2.2 | 展示叶，**细粒度已预编排** | 专题 FANIN 之后才 claim；见 [`A2.2-GAP-loop-编排.md`](./A2.2-GAP-loop-编排.md) |

A2.2 默认粒度：科技发展态势按 **需规五级**（35 页 / DW1–DW7）；其余按四级或产品包。清单：`metrics/request/展示系统/A2-GAP-page-catalog.yaml`。

跳过：`CHAIN-TOPIC-ANALYSIS`（索引）、空目录、`CHAIN-OPS`（运营）、`CHAIN-PORTAL-OVERVIEW`（门户，A2.2 DW16）。

## 子 agent /goal（W1 共用，换 page_id）

```text
/goal
task: TOPIC-ALGO-GAP-L01
page_id: {PAGE_ID}
agent: algorithm-agent
supervised_by: human:淮政玮
强度：ponytail off
理由：页面语义差集，禁止砍 METRIC-OPEN 覆盖或发明口径。不写业务代码。

只做这一页。读：
- metrics/request/专题系统/A2-GAP-page-catalog.yaml 本 page_id
- metrics/request/专题系统/pages/_schema.md
- 本页四件套 USM/TRACE/IA/Wireframe（只定边界）
- 本页/父模块 METRIC-OPEN（需求清单真源）
- metrics/request/A2-GAP-algo-catalog.yaml
- srs/05 对应维（对照用）

禁止：改 seed；写总表 TOPIC-ALGO-GAP-L01.yaml；开工 DS-ALGO-GAP-L01；从 USM 发明 M_*。
交付：metrics/request/专题系统/pages/{PAGE_ID}.yaml
```
