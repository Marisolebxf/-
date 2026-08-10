# 派单包：SYNTH-MOD-ELEMENT-PACK-L01

- **派单方**：coordinator  
- **时间**：2026-08-10  
- **Epic**：`E8-综合智能分析`  
- **叶子**：`SYNTH-ELEMENT` · 区域创新要素分析  
- **Agent**：`product-agent`  
- **监管人**：`human:淮政玮`  
- **上游修正**：`TOPIC-SYNTH-R3-修正拆叶-Pack1派单总包.md`  
- **历史参照（非权威）**：`SYNTH-REGION-区域创新分析/`

## 1. 目标

交付区域创新要素分析叶子的 **交互五件套（Pack1）**，对齐系统方案 §8.2 与算法库 §10.6–10.9（类型 / 层次 / 领域 / 综合）。

## 2. 范围

### 2.1 系统方案（产品任务）

真源：`bid-reference/科技信息展示系统和科技专题服务系统.md`

| 章节 | 能力 |
| --- | --- |
| §1.1.1.2.4.2.8.2 | 区域创新要素分析（总述） |
| §.8.2.1 | 创新要素数据汇聚 |
| §.8.2.2 | 要素评价模型构建 |
| §.8.2.3 | 要素影响关联分析 |

### 2.2 算法库（模型与 I/O）

真源：`bid-reference/科技专题服务算法库.md`

| 章节 | 模型 | Pack 必须落地的算法语义 |
| --- | --- | --- |
| §10.6 | 区域创新要素类型综合评价模型 | 人才/企业/政策/服务机构/科研机构/资金/空间等类型指数 |
| §10.7 | 区域创新要素层次综合评价模型 | 七大结构成熟度 / 均衡度 / 层次指数 |
| §10.8 | 区域创新要素领域综合评价模型 | 产业领域 × 技术领域覆盖与领域指数 |
| §10.9 | 区域创新要素综合分析模型 | 类型+层次+领域 → 要素综合指数 |

系统方案「汇聚 / 评价 / 影响关联」须映射到上述四模型：汇聚=多源要素数据与全景；评价=类型/层次/领域及综合指数；影响关联=贡献路径/优势短板（算法未定处开放项，禁止伪闭合）。  
旧原型「四类要素（人才/资本/平台/项目）」若与算法库七要素冲突：**以算法库为准**，差异写入 USM「源需求 / 本轮决策 / 待确认」。

### 2.3 产物路径

```text
agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-ELEMENT-区域创新要素分析/
├── IA-SYNTH-ELEMENT.md
├── TRACE-SYNTH-ELEMENT.yaml
├── USM-SYNTH-ELEMENT.md
├── UX-SPEC-SYNTH-ELEMENT.md
└── Wireframe-SYNTH-ELEMENT.md
```

### 2.4 禁止

- 把活力指数总榜或协同图谱主验收写入本叶  
- 用旧 SYNTH-REGION「四类要素」口径覆盖算法库七要素而不登记差异  
- 替甲方闭合类型/层次/领域权重与综合合成公式  
- 写业务代码 / 改依赖

## 3. Definition of Done

1. 五份文档齐备一致；`registry_task: SYNTH-MOD-ELEMENT-PACK-L01`  
2. TRACE 覆盖 §8.2.1–8.2.3，并分别挂接 §10.6–10.9  
3. 要素对象清单与算法库一致或差异分层清晰；metric 前缀建议 `M_SYNTH_ELEM_*`  
4. UX-SPEC / Wireframe 满足 D10 / Design；共享 `CT-SYN-CTX`  
5. 开放项承接并细化 `Q-SYNTH-02` → `Q-SYNTH-E-*`  
6. handoff + cost；不宣告门 1 闭合

## 4. 认领话术（粘贴）

```markdown
/goal product-agent
身份：你是经验丰富、遵循业界最佳实践的资深产品经理与产业研究分析专家，精通用户故事地图、追溯矩阵与验收设计，并具备区域创新/产业生态研判方法论；不写业务代码。
任务 ID：SYNTH-MOD-ELEMENT-PACK-L01
监管：human:淮政玮
Epic：E8-综合智能分析 · 叶子 SYNTH-ELEMENT（区域创新要素分析）
目标：交付交互五件套 IA/TRACE/USM/UX-SPEC/Wireframe
必读（禁止 compress 代替精读）：
  - 科技信息展示系统和科技专题服务系统.md §1.1.1.2.4.2.8.2（含 .2.1–.2.3）
  - 科技专题服务算法库.md §1.1.1.1.1.1.1.10.6–10.9
  - 产品定义评审规程.md §2/§3；Design.md；UX-UE 通用交互组件规范.md；data-lineage-policy.md v1.3 §2.3
  - TOPIC-SYNTH-R3-修正拆叶-Pack1派单总包.md
  - （仅参照）SYNTH-REGION 旧五件套 — 禁止当作权威
产出目录：…/SYNTH-ELEMENT-区域创新要素分析/
铁律：算法库七要素优先于旧四类演示口径；差异分层；D1 missing + Q；不写代码
Handoff：agent-handoffs/SYNTH-MOD-ELEMENT-PACK-L01.md
```

## 5. 下游

| 任务 | 关系 |
| --- | --- |
| `SYNTH-MOD-ELEMENT-METRIC-OPEN-L01` | 四模型指标卡 + gap catalog |
| `SYNTH-MOD-ELEMENT-V1-HIFI` | Pack 后 |
| `SYNTH-MOD-ELEMENT-PDR-G1` | 门 1 |
| 兄弟叶 VITALITY / COLLAB | 并行 + `CT-SYN-CTX` |
