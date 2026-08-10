# ENT-MOD-SEARCH-API-CONTRACT-L01 — 存量覆盖说明（不重复编码）

- **日期**：2026-08-03
- **确认人**：`human:侯佳伟`（后端 Lead / 本单监管人）
- **结论**：**不需要为本新单重新编码**；Java API 契约与门面已由旧任务交付，本单应为「故事库映射关单」。
- **仓**：`lumen-svc-platform` / `origin/dev`

## 1. 背景

| 项 | 说明 |
|---|---|
| 新单 | `ENT-MOD-SEARCH-API-CONTRACT-L01`（`ready`，故事驱动草案，门3 `ENT-MOD-SEARCH-DG-G3` 解锁后入库） |
| 触发 | `story-impl-proposals` 因故事库 `implementation_tasks` **未挂接**既有 Java 任务，误判「8 条故事未覆盖」 |
| 旧交付 | `ENT-ARCH-API-CONTRACT` + `ENT-JAVA-SEARCH-BIZ`（及同批企业检索门面） |

新单 `definition_of_done` 为空、派单包文件缺失；与旧交付范围高度重叠，不宜再开一轮实现。

## 2. 故事 → 存量任务映射

| 故事 | 标题 | 覆盖任务（主） | 证据 |
|---|---|---|---|
| US-E1-SCH-01 | 查企业：企业名称关键词查询 | `ENT-ARCH-API-CONTRACT` | commit `4d7b41e` 门面骨架；后续 `05bddb3` 等 gkx-search 透传 |
| US-E1-SCH-02 | 智能搜索：多字段关键词匹配 | `ENT-ARCH-API-CONTRACT` | 同上；检索/智能搜索 Feign → `/internal/gkx-search/**` |
| US-E1-SCH-03 | 初始态引导：示例、热门场景与最近检索 | `ENT-JAVA-SEARCH-BIZ` | commit `4a053de`；handoff `ENT-JAVA-SEARCH-BIZ.md`（#77–85） |
| US-E1-SCH-04 | 高级筛选：简化条件构造 | `ENT-ARCH-API-CONTRACT` + `ENT-JAVA-ENUM-CONTRACT-L02` | query_tree / filters；`84eb0fe` §25 + query-tree-schema |
| US-E1-SCH-05 | 结果列表：排序、再筛与对象确认 | `ENT-ARCH-API-CONTRACT` | 搜索列表门面 + 排序字段白名单（与 Python 契约对齐） |
| US-E1-SCH-06 | 对比篮与跨模块分析 | `ENT-ARCH-API-CONTRACT`（compare） | commit `7f05642` filter-template + compare-basket |
| US-E1-SCH-07 | 导出当前查询结果 | `ENT-ARCH-API-CONTRACT` / 企业门面批次 | 检索结果导出路径随企业门面批次落地（详见 API 全量目录） |
| US-E1-SCH-08 | 初始空态推荐企业 | `ENT-JAVA-SEARCH-BIZ` + recommend 门面 | SEARCH-BIZ 场景/示例；`4bcdd60` recommend facade |

## 3. 关键旧任务状态与验收

| 旧 task-id | 曾验收 | 当前 registry | 说明 |
|---|---|---|---|
| `ENT-ARCH-API-CONTRACT` | 2026-07-29 `human:淮政玮` → **done**（`ACCEPTANCE-2026-07-29-淮政玮-ENT-JAVA批次.md`） | `integration` | 2026-08-03 存量修正：实现阶段「联调未完成」回退，**非代码未交付** |
| `ENT-JAVA-SEARCH-BIZ` | handoff 已交 review | `integration` | 关单尚待 Theme 演示路径；**编码已完成** |

## 4. 关键代码证据（摘录）

| commit | 说明 | 作者标记 |
|---|---|---|
| `4d7b41e` | enterprise facade skeleton（search/compare/profile） | `[human:侯佳伟]` |
| `4a053de` | SEARCH-BIZ examples/scenes/history | `[human:侯佳伟]` |
| `7f05642` | filter-template + compare-basket | `[human:侯佳伟]` |
| `05bddb3` | remaining gkx-search Java facades | （同批集成） |
| `4ab99de` | Feign `/api` → `/internal/gkx-search`（架构 D2） | `[agent:data-agent]` |
| `84eb0fe` | §25 enum + query-tree-schema | `[agent:api-agent]`（监管 `human:侯佳伟`） |

Handoff：

- `agent-handoffs/企业战略分析-ENT/ENT-JAVA-SEARCH-BIZ.md`
- `agent-handoffs/企业战略分析-ENT/ACCEPTANCE-2026-07-29-淮政玮-ENT-JAVA批次.md`

## 5. 请 coordinator 执行的动作（建议）

1. **本单** `ENT-MOD-SEARCH-API-CONTRACT-L01`：标注「存量覆盖 / 不重复编码」；`note` 回链本文；按 chore/映射关单路径推进（或 claim → 附本说明 → ready_to_sign），**勿再派 api-agent 重写门面**。
2. **故事库**：将 `US-E1-SCH-01`～`08` 的 `implementation_tasks` 补挂 `ENT-ARCH-API-CONTRACT`、`ENT-JAVA-SEARCH-BIZ`（及本单 ID 作映射叶），避免再次误拆。
3. **联调**：继续跟 `ENT-ARCH-API-CONTRACT` / `ENT-JAVA-SEARCH-BIZ` 的 `integration` 收口与 Theme 演示，与「是否重新编码」解耦。

## 6. 开放项（非本单编码范围）

- 前后端联调 / Theme 演示路径通（旧单 `integration`）
- 故事库 `implementation_tasks` 回填（doc/PM）
- 若评审发现 SCH-07 导出接口缺口，单开 **delta bugfix**，不重开整叶

---

**监管确认**：`human:侯佳伟` — 同意本新单以存量覆盖关单，无需再编码。
