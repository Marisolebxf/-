# 派单包：SYNTH-MOD-COLLAB-V1-HIFI

- **派单方**：coordinator / product（Pack1 会签后解锁）
- **时间**：2026-08-10
- **Epic**：`E8-综合智能分析`
- **叶子**：`SYNTH-COLLAB` · 区域创新协同分析
- **Agent**：`ui-agent`（可协作 `frontend-agent`）
- **认领 / 监管**：`human:淮政玮`
- **仓**：`${GKX_ROOT}/repos/demo-ui-topic` · push **`origin/main`**（demo 仓直推）
- **上游**：`SYNTH-MOD-COLLAB-PACK-L01` = **done**
- **并行**：`SYNTH-MOD-COLLAB-METRIC-OPEN-L01`（王惠；不阻塞本单开工，指标未闭合处保持诚实态）
- **历史参照（非权威）**：旧 `TOPIC-SYNTH-R3` / `intelligence/*`、旧 `SYNTH-REGION` 五件套 — **禁止**把「密度×强度」当权威

## 1. 目标

在 `demo-ui-topic` 交付 `/intelligence/collaboration`（或 Pack1 约定路由）**V1 高保真 Demo**，严格消费 Pack1 交互五件套：

- **指标 + 计算方法 + 计算结果**对用户显性展示（禁止黑盒总分）
- **默认**深圳 × 全国重点城市 × 最近 3 年 → **跑批秒开**
- **改默认**后点「开始分析」→ 后台任务 + **协同场景**可视化五阶段过程页

## 2. 权威输入（必读，禁止 compress 代替精读）

| 优先级 | 路径 |
| --- | --- |
| P0 | `agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/`（IA / TRACE / USM / UX-SPEC / Wireframe） |
| P0 | `agent-handoffs/SYNTH-MOD-COLLAB-PACK-L01.md` |
| P0 | `Design.md` + `UX-UE 通用交互组件规范.md`（D10） |
| P0 | `data-lineage-policy.md` v1.3 §2.3（D9 角标 / 评审模式） |
| P1 | `SYS-ANALYSIS-JOBS` 过程壳（任务摘要卡 + 可视化分析过程卡） |
| 参照 only | 旧 `demo-ui-topic` `src/app/pages/intelligence/*`、旧 `SYNTH-REGION-*` |

## 3. 实现范围

### 3.1 页面 / 路由

| Frame | 路由 | 要点 |
| --- | --- | --- |
| F-COLLAB-01 | `/intelligence/collaboration` | 上下文条 + 秒开结果面 / 改条件待分析态 + 底栏「开始分析」 |
| F-COLLAB-02 | `/intelligence/collaboration/tasks/:taskId` | 任务摘要 + 可视化五阶段；完成后不自动跳；「查看分析结果」 |
| F-COLLAB-03 | Drawer `panel=method` | 指标与方法说明（§10.10 三指标 + 指数；临时演示公式 🧪） |

### 3.2 默认秒开 vs 改条件（产品铁律）

```
默认三元组（深圳 / 全国重点城市 / 最近3年）且有预计算快照
  → 秒开结果面；不创建 task；不进 F-COLLAB-02

任一字段离开默认（或无跑批）
  → 脏态 / 待分析 → 用户点「开始分析」→ F-COLLAB-02
```

共享上下文契约：`CT-SYN-CTX`（与 VITALITY/ELEMENT 同 key，禁止另起默认值）。
任务类型：`task_type=region_innovation_collaboration`（`CT-SYN-JOBS`）。

### 3.3 可视化五阶段文案（必须用协同场景，禁止产业链四力 / 活力四维 / 要素四模型文案）

1. 任务提交与分析条件冻结
2. 装载创新主体与合作关系快照，构建区域协同网络
3. 计算完整度、中心度与密度三项网络指标
4. 合成协同指数，识别高效集群、孤立主体与优势不足
5. 校验横向对比与趋势结果，组装协同效率报告快照

### 3.4 指标与诚实态

- 完整度 / 中心度 / 密度 / 协同指数 / 关系输入 / 协同–产出关联（`M_SYNTH_COLLAB_*`）
- 结果面须同页可见：三指标、指数、对比/趋势、中心主体、集群/孤立、方法入口、效果评估与报告
- 演示公式仅标 🧪；正式图类型/分母/边权/权重/校准未定 → D1 missing/draft + Q-SYNTH-C-*
- D9：每个统计数字旁角标；评审模式门控 + 组件自闸；关闭零泄漏

## 4. 禁止

- 扩做 8.1 活力总榜 / 8.2 要素业务页（仅顺链出口 + `CT-SYN-CTX`）
- 用「密度×强度」冒充算法库三指标权威合成
- 伪造百分比进度；过程动作放标题栏
- 默认条件伪装秒开却实际空转假 loading
- 擅自改 `package.json` / 加新依赖（除非任务明确批准）
- push `--force`；lumen 正式仓本单不改（本单只动 `demo-ui-topic`）

## 5. Definition of Done

1. F-COLLAB-01/02/03 按 Pack1 落地；指标/方法/结果显性
2. 默认三元组秒开；改条件五阶段过程可用，并可从系统任务浮层恢复（对齐 SYS-ANALYSIS-JOBS 契约即可，可先本叶 mock 任务总线）
3. D9 角标 + 评审模式；算法未定诚实态；完整度不得遗漏
4. `tsc` / `vite build` 通过；push `origin/main`；CI 绿（若有）
5. handoff：`agent-handoffs/SYNTH-MOD-COLLAB-V1-HIFI.md` + cost 四字段
6. 不宣告门 1 / PDR-G1 闭合（METRIC-OPEN / PDR-G1 另单）

## 6. 认领话术（粘贴）

```markdown
/goal ui-agent
身份：你是资深 UI/前端实现工程师，精通 React + Vite + Arco Design + ECharts/G6；严格按已会签产品定义出高保真 Demo，不另起交互体系。
任务 ID：SYNTH-MOD-COLLAB-V1-HIFI
监管 / 认领：human:淮政玮
Epic：E8-综合智能分析 · 叶子 SYNTH-COLLAB（区域创新协同分析）
仓：${GKX_ROOT}/repos/demo-ui-topic · 分支 origin/main（demo 仓直推）
强度：ponytail full
目标：交付 /intelligence/collaboration V1 高保真 Demo（秒开 + 改条件可视化过程）
必读（禁止 compress 代替精读）：
  - agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/（IA/TRACE/USM/UX-SPEC/Wireframe 全读）
  - agent-handoffs/SYNTH-MOD-COLLAB-PACK-L01.md
  - agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-MOD-COLLAB-V1-HIFI-派单包.md（本包）
  - agent-delivery/Design.md + UX-UE 通用交互组件规范.md
  - agent-delivery/data-lineage-policy.md v1.3 §2.3
  - （过程壳参照）agent-handoffs/产品整体定义/SYS-ANALYSIS-JOBS/
  - （仅参照）旧 intelligence/* 与 SYNTH-REGION — 禁止当权威；禁止「密度×强度」冒充正式公式
实现要点：
  1) 对用户显性展示：指标、计算方法、计算结果（同页可及；含完整度）
  2) 默认：深圳 × 全国重点城市 × 最近3年 → 跑批秒开（有预计算则不进过程页）
  3) 改默认后「开始分析」→ F-COLLAB-02 协同五阶段（文案见派单包 §3.3，禁止产业链/活力/要素文案串台）
  4) CT-SYN-CTX 三叶共享；D9 角标 + 评审自闸；Q-SYNTH-03/C-* 诚实态
铁律：调用链不越层；不伪闭合算法；不扩 8.1/8.2；commit 带 [agent:ui-agent]；禁止 force push
Handoff：agent-handoffs/SYNTH-MOD-COLLAB-V1-HIFI.md
```

## 7. 开工检查

- [x] Pack1 `done`
- [x] 本任务 `claimed`（`agent:ui-agent` / 监管 `human:淮政玮`）
- [x] 开 Cursor 会话粘贴 §6 → `in_progress`
- [ ] 交付后 handoff + 转 review / pending_test（handoff 已写；push 待 rebase 结束后）

## 8. 下游

| 任务 | 关系 |
| --- | --- |
| `SYNTH-MOD-COLLAB-METRIC-OPEN-L01` | 并行；指标卡闭合后可回刷 Demo 诚实角标文案 |
| `SYNTH-MOD-COLLAB-PDR-G1` | METRIC-OPEN + 本 Demo UX 可评后建单 |
| VITALITY / ELEMENT V1-HIFI | 各自 Pack done 后另派；共用 `CT-SYN-CTX` |
