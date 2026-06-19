# UX-DS-15-trial · ux-agent 首次试点 · 重点科技人才画像 IA/wireframe

## 执行时间
2026-06-17（ux-agent 角色首次试点）

## 任务
- 覆盖功能点：**DS-15 重点科技人才画像**（acceptance-catalog tier=INTEG）
- 范围真源：`bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.3.3（行 1879–2302）
- 任务范围：把 bid 章节翻译为 **IA + 用户旅程 + 低保真线框**（不写代码、不画视觉、不动 lumen）

## 完成清单（对照 DoD）

| DoD 项 | 状态 | 证据 |
|--------|------|------|
| 4 个产物文件齐全且在隔离目录 | ✅ | 见"产物路径" |
| 每个页面映射到 DS-15 子功能点 + bid-reference 章节号 | ✅ | DS-15-IA.md §3 §6 映射表 |
| mermaid 语法正确（自检通过） | ✅ | 已防御性引号包裹特殊字符；共 8 段 mermaid |
| 范围不超过 bid §1.1.1.1.4.3.3 描述 | ✅ | DS-15-IA.md §8 + DS-15-wireframe.md 末"范围合规自检" |
| git add + commit 到 demo2 main | ✅ | 见 commit hash |
| 未执行 git push | ✅ | 仅本地 commit，由 PM 决定是否 push |
| handoff 已写入 | ✅ | 本文件 |

## 产物绝对路径

1. `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\README.md`
2. `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-IA.md`
3. `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-userflow.md`
4. `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-wireframe.md`

## 体量统计

| 文件 | 行数 | 字符数（含中文） |
|------|------|------------------|
| README.md | 70 | 2,981 |
| DS-15-IA.md | 204 | 10,138 |
| DS-15-userflow.md | 165 | 6,344 |
| DS-15-wireframe.md | 732 | 38,667 |
| **合计** | **1,171** | **58,130** |

## commit hash

```
ddfc273 [sandbox] ux-agent 试点：DS-15 重点科技人才画像 IA/wireframe（不 push）
```

> （初次 commit 为 `fea5104`，因 README DoD 勾选回填做了一次 `--amend`，最终 hash 为 `ddfc273`；amend 安全前提：commit 由本会话创建、尚未 push。）

- **未执行 git push**：本地 commit 已在 demo2 main 分支；是否推送由 PM 决定。
- **使用 `git add -f`**：因 demo2 `.gitignore` 第 6 行 `docs/` 已忽略整个 docs 目录；为遵守"禁止改 .gitignore 等任何现有文件"铁律，采用 `git add -f` 强制添加 **仅本沙箱 4 个文件**，未修改 .gitignore，未触碰任何其他文件。该决策已在本 handoff 显式说明，便于 PM 评审是否长期需要把 `docs/ia/sandbox/` 例外加入 .gitignore。

## 范围与实现

| 项 | 内容 |
|---|---|
| scope_ref | bid-reference §1.1.1.1.4.3.3.1 ~ §1.1.1.1.4.3.3.6（6 大二级子功能） |
| implementation_as_built | 15 个页面/子视图（含 6 Tab + 3 详情子页 + 2 管理页 + 1 订阅页） |
| data_gaps | 数据契约由 algorithm-agent / data-agent 后续落地；本试点字段表为前端期望视角 |
| variance_note | 未扩大范围；移动适配明确后置（对齐 `repo-registry.yaml` ui_mobile.notes） |

## 待人评审的开放项（≥5 条）

> 完整 24 条见 `demo2/docs/ia/sandbox/talent-2026-06-17/DS-15-wireframe.md` 末"全局开放项汇总"。下方按"决策项 / 建议默认值 / 影响"提取 7 条**最关键**项。

| # | 决策项 | 建议默认值（UX 最佳实践） | 影响 |
|---|--------|--------------------------|------|
| **K-O1** | 综合评分（§3.3.1.3）的 4 个分项权重公式（影响力/贡献度/合作/产出）由谁定义？ | 由 **algorithm-agent + 业务方**共同对齐，UI 仅展示分项 + 提示"公式 v1"；不由 ux 默认决定 | 算法依赖；影响 P-06 评分卡呈现 |
| **K-O2** | 引进难度/成本（§3.3.3.1）的角色脱敏与"申请查看"流程 | 默认对所有角色脱敏 + 锁标；点击触发"申请理由 + SSO 角色校验"双重审计；写 Loki `audit=talent` | 合规与法务；影响 P-06 + N-04/N-07 埋点 |
| **K-O3** | 合作网络图谱（§3.5）与研究领域图谱（§3.6）的**可视化技术选型**与**主题演化表达**（桑基/主题流/堆叠） | 沿用 `gkx_demo_ui/src/views/entan/components/GraphView.vue` 同款；主题演化默认"主题流图"；**强烈建议人工评审 + 用户测试** | 性能与体验；P-08/P-09 整体 |
| **K-O4** | 6 Tab 默认加载策略 | 仅基础画像首屏加载，其余 Tab 懒加载；合作/领域独立全屏路由 | 性能 vs 切换流畅度；影响 P-03 路由结构 |
| **K-O5** | 大图降级阈值（默认节点数 > 500）与一跳邻域策略 | 节点 > 500 默认仅一跳；按机构/学科自动聚合；性能告警可视化提示 | 大屏汇报现场体验；P-08 异常 C |
| K-O6 | 雷达图 6–8 维定义 | 待业务方确认默认维度集合（建议：影响力/产出/合作/创新/跨学科/师承/资助/获奖） | P-06 雷达图字段 |
| K-O7 | 推送频率默认 | 每日聚合（避免噪声） | P-15 体验 |

> **5 条返回项**：K-O1 / K-O2 / K-O3 / K-O4 / K-O5（按重要性排序）。

## 给 ui-agent 接力的 next-step 建议

### A. 组件需求清单（demo2 现有 src/components/ 可能缺）

| 需求 | 用途 | 来源 bid 章节 | 建议优先级 |
|------|------|--------------|-----------|
| `<TalentCard>` | 卡片式人才（P-02） | §...3.1.1.3 | P0 |
| `<FacetFilter>` | 多条件筛选器（单位/职称/地域/领域级联） | §...3.1.2.2 | P0 |
| `<MaskedField>` | 脱敏字段 + 锁标 + 申请抽屉 | §...3.1.4 | P0（合规） |
| `<TimelineFeed>` | 时间轴视图（成果） | §...3.4.1.3 | P0 |
| `<GraphCanvas>` | 图谱画布（缩放/拖拽/聚焦/聚合） | §...3.2/3.5/3.6 | **P0**（建议复用 entan GraphView.vue） |
| `<ScoreRadar>` | 评分雷达图 | §...3.3.1.2 | P1 |
| `<TopicStreamChart>` | 主题演化（桑基或主题流） | §...3.6.3.1 | **P1（需评审）** |
| `<DataStalenessBanner>` | 数据时效告警条 | userflow §4.2 | P1 |
| `<SubscribeButton>` | 订阅按钮（订阅/取消） | §...3.1.6.2 | P0 |
| `<ImportWizard>` | 数据导入向导（5 步） | §...3.1.5.1 | P2 |
| `<FeedbackDrawer>` | 反馈纠错抽屉 | §...3.1.6.1 | P1 |

### B. mock 数据结构建议（mocks/ 下）

```
mocks/talent/
├── list.json              # 人才列表（含分页与筛选回包）
├── profile/T0001.json     # 个人画像完整对象
├── profile/T0001/basic.json
├── profile/T0001/relation.json
├── profile/T0001/analysis.json
├── profile/T0001/output.json
├── profile/T0001/collab.json   # 节点 ≈ 50, 边 ≈ 120 (覆盖一跳/二跳)
├── profile/T0001/domain.json   # 主题 ≈ 20, 年份范围 2015-2026
├── output/paper_001.json
├── output/patent_001.json
├── output/project_001.json
├── similar.json           # 相似学者推荐
└── recommend/collab.json  # 算法推荐合作节点
```

> 字段命名严格按 `DS-15-wireframe.md` 各页字段表；**空值率 ≥ 15%** 以测试空态；**敏感字段单独 mock 一份脱敏版**用于演示默认态。

### C. 路由建议落地（src/router）

按 `DS-15-IA.md §4` 注册 15 条路由；**沙箱模式下建议先做 P-01/P-02/P-03/P-04/P-07** 五条核心，其他作 stub 页面占位。

### D. 验收对齐
- ui-agent 完成后通知 coordinator 派 UI/UE 3 人评审，重点看 K-O3 / K-O5 的图谱可视化与降级策略。
- 与 PM 确认 K-O2 引进评估脱敏与申请流程，再上线对应交互。

## 不一致清单（bid-reference vs acceptance-catalog）

| 不一致 | bid 描述 | acceptance-catalog 描述 | 建议 |
|---|---|---|---|
| **scope_summary 措辞** | bid §1.1.1.1.4.3.3 列出 6 大二级：基础/关联/分析/近期成果/合作网络/研究领域 | catalog 行 182 写为"基础/关联/分析画像+成果+合作网络+领域图谱"（口语化简写，但语义一致） | 仅措辞差异，建议 catalog 保持原状即可，**不属于范围冲突**。 |
| **依赖描述** | bid 文本未显式列依赖 | catalog `dependencies: 人才（他方）+机构/成果` | 与 bid 内容一致（来自 §3.1 单位、§3.2 成果关联），无冲突。 |
| （未发现实质性范围冲突） | — | — | 本试点未发现 bid 与 catalog 在 DS-15 范围上的实质冲突；6 大子功能在两文档中均能一一对应。 |

> 注：catalog 中 `route: null` 表示当前未注册前端路由，本试点 IA 提供了 15 条路由建议，可作为 catalog `route` 字段后续填充的依据。

## 自评

### 做得好的（≥2 条）

1. **章节-路由-页面三向闭环**：每个页面同时映射 bid 章节号、DS-15 子功能、对应路由，三者一一可追溯，便于甲方按章节验收（对齐 `repo-registry.yaml` → `demo2_proto.rules.page_naming`）。
2. **严守边界**：未产任何代码（无 `.vue/.ts/.css/.js/.json`），未触碰 demo2 现有 `src/`、`router/`、`package.json` 等任何文件；产物全部隔离在 `docs/ia/sandbox/talent-2026-06-17/`。
3. **复杂可视化显式标"需人工评审"**：合作网络、研究领域、综合评分雷达、主题演化 4 处均未擅自简化，给出建议默认值 + 评审锚点。
4. **遵循 ±10% 范围铁律**：未新增子功能，未删除子功能；脱敏与"自动数据抓取"等后端范畴未占用 UI 范围。
5. **异常路径全面**：覆盖了 4 类异常（信息缺失/数据时效/渲染降级/反馈冲突），不仅给出主路径。

### 想改进的（≥2 条）

1. **mermaid 与中文混排时的可读性**：受 mermaid 语法对特殊字符（`>`、`/`、`:`、`"`、`(`）的限制，部分节点文案被简化（如"超过阈值"代替"> 阈值"）；下次可在外部使用 mermaid live editor 预渲染再贴入，或在 ui-agent 一侧补一份 HTML 截图作汇报使用。
2. **字段表"来源"列粒度**：当前以 bid 章节号标注，对 algorithm-agent / api-agent 不够精确（缺接口名/字段路径）；接力时建议 ui-agent 与 api-agent 共建 `mocks/` schema 时把"接口名 + 字段路径"补回。
3. **未做用户测试与共情**：试点产物为"专家假设最佳实践"，缺真实用户访谈与可用性测试；建议 UI/UE 评审阶段引入 1–2 名管理者/科研服务人员做 think-aloud。
4. **未输出"信息密度地图"**：6 Tab 在不同屏幕下的信息密度未提前测算；ui-agent 实现时可能发现某 Tab 内容过密需要进一步拆分。

## 与编排基线对齐自检

- ✅ 工作根：`E:\gkx_src\demo2`（demo2_proto 仓）
- ✅ 不写代码、不改既有文件、不 push（对齐 §9.1c ux-agent 铁律）
- ✅ 范围未超 bid §1.1.1.1.4.3.3（对齐 `scope-baseline.yaml` ±10% 浮动）
- ✅ demo2 propagation：本产物只在本仓沙箱目录，不入 lumen（对齐 `repo-registry.yaml` → `demo2_proto.propagation.to_lumen=forbidden`）
- ✅ next-step：通知 coordinator 派 ui-agent 接力（按 §6.1 流程 4）

## 涉及文件

- `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\README.md`（新增）
- `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-IA.md`（新增）
- `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-userflow.md`（新增）
- `E:\gkx_src\demo2\docs\ia\sandbox\talent-2026-06-17\DS-15-wireframe.md`（新增）
- `E:\gkx_src\agent-delivery\agent-handoffs\UX-DS-15-trial.md`（本文件，新增）

## 建议下一任务

| 角色 | 任务 | 输入 |
|------|------|------|
| **ui-agent** | 把本 IA/wireframe 翻译为 demo2 仓可演示页面（沙箱模式：建议同样隔离到 `src/views/sandbox-talent-2026-06-17/`，命名空间隔离） | 本试点 4 个产物 + 组件需求清单 + mock 结构 |
| **PM / UI/UE 3 人** | 评审本试点产物 + K-O1~K-O5 关键决策 | 本 handoff |
| **architect-agent** | （可选）评估 GraphCanvas 是否走方案 A 共享聚合（图数据经 Java REST → Nebula），不直连 | DS-15-IA.md §7 |
