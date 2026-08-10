# 派单包：SYNTH-MOD-ELEMENT-V1-HIFI

- **派单方**：coordinator / product（Pack1 会签后解锁）
- **时间**：2026-08-10
- **Epic**：`E8-综合智能分析`
- **叶子**：`SYNTH-ELEMENT` · 区域创新要素分析
- **Agent**：`ui-agent`（可协作 `frontend-agent`）
- **认领 / 监管**：`human:淮政玮`（已 claimed）
- **仓**：`${GKX_ROOT}/repos/demo-ui-topic` · push **`origin/dev`**
- **上游**：`SYNTH-MOD-ELEMENT-PACK-L01` = **done**
- **并行**：`SYNTH-MOD-ELEMENT-METRIC-OPEN-L01`（王惠；不阻塞本单开工，指标未闭合处保持诚实态）
- **历史参照（非权威）**：旧 `TOPIC-SYNTH-R3` / `intelligence/*` 实现、旧 `SYNTH-REGION` 五件套 — **禁止**把旧「人才/资本/平台/项目」四类当权威

## 1. 目标

在 `demo-ui-topic` 交付 `/intelligence/elements` **V1 高保真 Demo**，严格消费 Pack1 交互五件套：

- **指标 + 计算方法 + 计算结果**对用户显性展示（禁止黑盒总分）
- **默认**深圳 × 全国重点城市 × 最近 3 年 → **跑批秒开**
- **改默认**后点「开始分析」→ 后台任务 + **要素场景**可视化五阶段过程页

## 2. 权威输入（必读，禁止 compress 代替精读）

| 优先级 | 路径 |
| --- | --- |
| P0 | `agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-ELEMENT-区域创新要素分析/`（IA / TRACE / USM / UX-SPEC / Wireframe） |
| P0 | `agent-handoffs/SYNTH-MOD-ELEMENT-PACK-L01.md` |
| P0 | `Design.md` + `UX-UE 通用交互组件规范.md`（D10） |
| P0 | `data-lineage-policy.md` v1.3 §2.3（D9 角标 / 评审模式） |
| P1 | `SYS-ANALYSIS-JOBS` 过程壳（任务摘要卡 + 可视化分析过程卡） |
| 参照 only | 旧 `demo-ui-topic` `src/app/pages/intelligence/*`、旧 `SYNTH-REGION-*` |

## 3. 实现范围

### 3.1 页面 / 路由

| Frame | 路由 | 要点 |
| --- | --- | --- |
| F-ELEM-01 | `/intelligence/elements` | 上下文条 + 秒开结果面 / 改条件待分析态 + 底栏「开始分析」 |
| F-ELEM-02 | `/intelligence/elements/tasks/:taskId` | 任务摘要 + 可视化五阶段；完成后不自动跳；「查看分析结果」 |
| F-ELEM-03 | Drawer `panel=method` | 指标与方法说明（§10.6–10.9 步骤 + 临时权重 ⚠️） |

### 3.2 默认秒开 vs 改条件（产品铁律）

```
默认三元组（深圳 / 全国重点城市 / 最近3年）且有预计算快照
  → 秒开结果面；不创建 task；不进 F-ELEM-02

任一字段离开默认（或无跑批）
  → 脏态 / 待分析 → 用户点「开始分析」→ F-ELEM-02
```

共享上下文契约：`CT-SYN-CTX`（与 VITALITY/COLLAB 同 key，禁止另起默认值）。

### 3.3 可视化五阶段文案（必须用要素场景，禁止产业链四力 / 活力四维文案）

1. 任务提交与分析条件冻结
2. 汇聚七类创新要素多源数据与全景快照
3. 计算要素类型指数与层次指数
4. 计算领域指数并量化要素贡献路径
5. 合成要素综合指数、优势短板与分析报告组装

### 3.4 七要素与四模型（算法库对齐）

- 正式要素清单 **仅**：人才 / 企业 / 政策 / 服务机构 / 科研机构 / 资金 / 空间
- 透镜：类型（§10.6）/ 层次（§10.7）/ 领域（§10.8）/ 综合（§10.9）
- 结果面须同页可见：综合指数、三透镜指数、七要素得分、权重、指标明细、方法入口、贡献路径区、排名/趋势/优劣

### 3.5 D9 / 诚实态

- 每个统计数字旁角标；评审模式门控 + 组件自闸；关闭零泄漏
- `M_SYNTH_ELEM_*` D1 missing/draft → 红问号 / ⚠️ + 🧪；不伪闭合公式与贡献路径
- Mock / 跑批预计算须可识别（评审态完整）

## 4. 禁止

- 扩做 8.1 活力总榜 / 8.3 协同图谱业务页（仅顺链出口 + `CT-SYN-CTX`）
- 用旧 DEMO「人才/资本/平台/项目」冒充算法七要素
- 伪造百分比进度；过程动作放标题栏
- 默认条件伪装秒开却实际空转假 loading
- 擅自改 `package.json` / 加新依赖（除非任务明确批准）
- push `--force`；lumen 正式仓本单不改（本单只动 `demo-ui-topic`）

## 5. Definition of Done

1. F-ELEM-01/02/03 按 Pack1 落地；指标/方法/结果显性
2. 默认三元组秒开；改条件五阶段过程可用，并可从系统任务浮层恢复（对齐 SYS-ANALYSIS-JOBS 契约即可，可先本叶 mock 任务总线）
3. D9 角标 + 评审模式；算法未定诚实态
4. `tsc` / `vite build` 通过；push `origin/dev`；CI 绿（若有）
5. handoff：`agent-handoffs/SYNTH-MOD-ELEMENT-V1-HIFI.md` + cost 四字段
6. 不宣告门 1 / PDR-G1 闭合（METRIC-OPEN / PDR-G1 另单）

## 6. 认领话术（粘贴）

```markdown
/goal ui-agent
身份：你是资深 UI/前端实现工程师，精通 React + Vite + Arco Design + ECharts；严格按已会签产品定义出高保真 Demo，不另起交互体系。
任务 ID：SYNTH-MOD-ELEMENT-V1-HIFI
监管 / 认领：human:淮政玮
Epic：E8-综合智能分析 · 叶子 SYNTH-ELEMENT（区域创新要素分析）
仓：${GKX_ROOT}/repos/demo-ui-topic · 分支 origin/dev
强度：ponytail full
目标：交付 /intelligence/elements V1 高保真 Demo（秒开 + 改条件可视化过程）
必读（禁止 compress 代替精读）：
  - agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-ELEMENT-区域创新要素分析/（IA/TRACE/USM/UX-SPEC/Wireframe 全读）
  - agent-handoffs/SYNTH-MOD-ELEMENT-PACK-L01.md
  - agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-MOD-ELEMENT-V1-HIFI-派单包.md（本包）
  - agent-delivery/Design.md + UX-UE 通用交互组件规范.md
  - agent-delivery/data-lineage-policy.md v1.3 §2.3
  - （过程壳参照）agent-handoffs/产品整体定义/SYS-ANALYSIS-JOBS/
  - （仅参照）旧 intelligence/* 与 SYNTH-REGION — 禁止当权威；要素清单以算法库七要素为准
实现要点：
  1) 对用户显性展示：指标、计算方法、计算结果（同页可及）
  2) 默认：深圳 × 全国重点城市 × 最近3年 → 跑批秒开（有预计算则不进过程页）
  3) 改默认后「开始分析」→ F-ELEM-02 要素五阶段（文案见派单包 §3.3，禁止产业链四力 / 活力四维文案）
  4) CT-SYN-CTX 三叶共享；D9 角标 + 评审自闸；Q-SYNTH-02/E-* 诚实态
铁律：调用链不越层；不伪闭合算法；不扩 8.1/8.3；commit 带 [agent:ui-agent]；禁止 force push
Handoff：agent-handoffs/SYNTH-MOD-ELEMENT-V1-HIFI.md
```

## 7. 开工检查

- [x] Pack1 `done`
- [x] 本任务 `claimed`（`human:淮政玮`）
- [ ] 开 Cursor 会话粘贴 §6 → `in_progress`
- [ ] 交付后 handoff + 转 review / pending_test

## 8. 下游

| 任务 | 关系 |
| --- | --- |
| `SYNTH-MOD-ELEMENT-METRIC-OPEN-L01` | 并行；指标卡闭合后可回刷 Demo 诚实角标文案 |
| `SYNTH-MOD-ELEMENT-PDR-G1` | METRIC-OPEN + 本 Demo UX 可评后建单 |
| VITALITY / COLLAB V1-HIFI | 各自 Pack done 后另派；共用 `CT-SYN-CTX` |
