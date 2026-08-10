# 派单包：SYNTH-MOD-VITALITY-PACK-L01

- **派单方**：coordinator  
- **时间**：2026-08-10  
- **Epic**：`E8-综合智能分析`  
- **叶子**：`SYNTH-VITALITY` · 区域创新活力分析  
- **Agent**：`product-agent`（定义轨；可与体验 Owner 共审）  
- **监管人**：`human:淮政玮`  
- **上游修正**：`TOPIC-SYNTH-R3` 单叶废止 → 见 `TOPIC-SYNTH-R3-修正拆叶-Pack1派单总包.md`  
- **历史参照（非权威）**：`SYNTH-REGION-区域创新分析/`（仅对照，禁止复制为已闭合）

## 1. 目标

交付区域创新活力分析叶子的 **交互五件套（Pack1）**：IA / TRACE / USM / UX-SPEC / Wireframe，双源对齐系统方案 §8.1 与算法库 §10.5。

## 2. 范围

### 2.1 系统方案（产品任务）

真源：`bid-reference/科技信息展示系统和科技专题服务系统.md`

| 章节 | 能力 |
| --- | --- |
| §1.1.1.2.4.2.8.1 | 区域创新活力分析（总述） |
| §.8.1.1 | 指标体系构建 |
| §.8.1.2 | 综合评价模型 |
| §.8.1.3 | 区域指数计算与可视化 |

服务对象原文须回指 §8 总述语境（政府科技战略决策 / 资源统筹等），不得自造岗位 persona。

### 2.2 算法库（模型与 I/O）

真源：`bid-reference/科技专题服务算法库.md`

| 章节 | 模型 | Pack 必须落地的算法语义 |
| --- | --- | --- |
| §1.1.1.1.1.1.1.10.5 | 区域创新活力综合分析模型 | 科技/产业/人才/政策四维 → 活力指数；阈值与权重；趋势 |
| §10.1–10.4 | 科技/产业/人才/政策成果评价 | **作为四维输入来源说明**（可引用，不强制本叶再拆四个 UI 叶子） |

输出至少覆盖算法库声明：区域创新活力指数、单维度评分及权重分布、优势与短板、趋势/策略建议（产品层可映射为卡片/榜单/报告入口；算法未定处 D1 missing + Q 开放项）。

### 2.3 产物路径

```text
agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-VITALITY-区域创新活力分析/
├── IA-SYNTH-VITALITY.md
├── TRACE-SYNTH-VITALITY.yaml
├── USM-SYNTH-VITALITY.md
├── UX-SPEC-SYNTH-VITALITY.md
└── Wireframe-SYNTH-VITALITY.md
```

### 2.4 禁止

- 把 8.2 / 8.3 能力写进本叶验收（跨叶仅允许上下文契约与下钻出口）  
- 用旧 `SYNTH-REGION` 演示权重复制冒充算法库对齐  
- 替甲方闭合权重/阈值/合成公式（登记 `Q-SYNTH-01` 细化项 / `Q-SYNTH-V-*`）  
- 写 demo/lumen 业务代码（属后续 V1-HIFI）  
- 新增 npm 依赖或改 `package.json`

## 3. Definition of Done

1. 五份文档齐备、相互一致；TRACE `registry_task: SYNTH-MOD-VITALITY-PACK-L01`  
2. TRACE 反向覆盖 §8.1.1–8.1.3；每条 `source_relation` 可回指  
3. TRACE / USM 显式引用算法库 §10.5（及 §10.1–10.4 输入关系）；I/O 与开放项诚实  
4. UX-SPEC 对照 D10 §19；Wireframe 对照 Design.md（Arco 边界）  
5. 区域共享上下文契约 `CT-SYN-CTX`（与要素/协同叶一致）写明  
6. handoff：`agent-handoffs/SYNTH-MOD-VITALITY-PACK-L01.md` + cost 四字段  
7. 不宣告门 1 闭合（METRIC-OPEN / PDR-G1 另单）

## 4. 认领话术（粘贴）

```markdown
/goal product-agent
身份：你是经验丰富、遵循业界最佳实践的资深产品经理与产业研究分析专家，精通用户故事地图、追溯矩阵与验收设计，并具备区域创新/产业生态研判方法论；不写业务代码。
任务 ID：SYNTH-MOD-VITALITY-PACK-L01
监管：human:淮政玮
Epic：E8-综合智能分析 · 叶子 SYNTH-VITALITY（区域创新活力分析）
目标：交付交互五件套 IA/TRACE/USM/UX-SPEC/Wireframe
必读（禁止 compress 代替精读）：
  - agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md §1.1.1.2.4.2.8.1（含 .1.1–.1.3）
  - agent-delivery/bid-reference/科技专题服务算法库.md §1.1.1.1.1.1.1.10 + §10.5（§10.1–10.4 作四维输入参照）
  - agent-delivery/产品定义评审规程.md §2/§3
  - agent-delivery/Design.md + UX-UE 通用交互组件规范.md
  - agent-delivery/data-lineage-policy.md v1.3 §2.3
  - agent-handoffs/产品整体定义/E8-综合智能分析/TOPIC-SYNTH-R3-修正拆叶-Pack1派单总包.md
  - （仅参照）SYNTH-REGION-区域创新分析/ 旧五件套 — 禁止当作权威
产出目录：agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-VITALITY-区域创新活力分析/
铁律：双源对齐；角色可回指源章节；算法未定 D1 missing + Q；不写代码；ponytail 定义类默认 off（禁止用强度行压缩文档完整性）
Handoff：agent-handoffs/SYNTH-MOD-VITALITY-PACK-L01.md
```

## 5. 下游

| 任务 | 关系 |
| --- | --- |
| `SYNTH-MOD-VITALITY-METRIC-OPEN-L01` | PACK 后启动；闭合 ④⑤ |
| `SYNTH-MOD-VITALITY-V1-HIFI` | 消费本 Pack + 旧 demo 参照 |
| `SYNTH-MOD-VITALITY-PDR-G1` | METRIC-OPEN + UX 可评后 |
| 兄弟叶 ELEMENT / COLLAB Pack | 并行；共享 `CT-SYN-CTX` |
