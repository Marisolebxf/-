# 企业维度 Scrum 主题试点（SEARCH + KEYENT · 1C + 2B）

> **决策**：1C 试点模块 + 2B 薄垂直主题（每 Theme 2～3 条用户故事，端到端可演示）  
> **状态**：Planning 草案 · 2026-08-03  
> **Owner**：PM 郭万迎 + coordinator；执行对齐孔东 / 侯佳伟 / 徐滕强  
> **真源**：本文件 + `scrum-sprint.yaml#2026-W32`；任务 leaf 仍以 `task-registry` 为准  
> **不做**：不拆合现有工程 leaf ID；不批量改 EVAL/RISK/RECRUIT；定义轨 PDR/RECLOSE 不改 Theme 模型

---

## 0. 口径：`implemented` vs Theme Done

| 术语 | 含义 | 真源 |
|------|------|------|
| **库 `status`（细粒度）** | 由关联任务滚动汇总：已定义 / 已排Sprint / 开发中 / 开发完成 / 联调中 / 测试中 / 已完成（`scripts/lib/story-progress.mjs`） | `user-story-library.yaml` |
| **Theme Done** | 本 Theme 演示脚本在 Review 当场跑通（前端→Java→Python/ADS 或约定 Mock 路径明确） | 本文件 §2 演示脚本 + Sprint Review 纪要 |
| **leaf `done`** | 仍走实现规程门 I3 / 签收；关单须含「所属 Theme 演示路径通」一句 | registry + handoff |

**本试点不做**：给故事库加 `theme_status` 机器字段。Theme 进度用下表人工维护，试点通过后再评估是否入库。

### Theme 进度板（人工）

| Theme | 故事 | 状态 | Review 证据 |
|-------|------|------|-------------|
| S-T1 筛选可用 | US-E1-SCH-04（+SCH-05 再筛） | 🔲 未演示 | |
| S-T2 初始引导 | US-E1-SCH-03, US-E1-SCH-08 | 🔲 未演示 | |
| S-T3 结果确认硬化 | US-E1-SCH-01, US-E1-SCH-05 | 🔲 未演示 | |
| K-T1 发现集合 | US-KEYENT-01, US-KEYENT-02 | 🔲 未演示 | |
| K-T2 领域布局 | US-KEYENT-03, US-KEYENT-05 | 🔲 未演示 | |
| K-T3 编组接力 | US-KEYENT-04 | 🔲 未演示 | |

---

## 1. Theme 总表与 leaf 映射

### 1.1 SEARCH

| Theme | 故事包 | 演示增量 | committed leaf | stretch |
|-------|--------|----------|----------------|---------|
| **S-T1 筛选可用** | US-E1-SCH-04；验收触点含 SCH-05「再筛」 | 高级筛选：地区树 + 字典条件 → 可复现结果列表 | `ENT-FE-SEARCH-REGION-FILTER`, `ENT-JAVA-SEARCH-REGION-META`, `FE-ENT-DICT-WIRE-L05`, `DATA-ENT-DICT-IMPL-L02`, `DATA-ENT-DICT-REGION-SEED-L03`, `API-ENT-DICT-JAVA-L04` | `DATA-ENT-LISTING-SCALE-ETL-L06` |
| **S-T2 初始引导** | US-E1-SCH-03, US-E1-SCH-08 | 空态示例/热门/最近检索/推荐企业可点可跳 | `ENT-JAVA-SEARCH-BIZ`, `FE-ENT-SEARCH-STATE-CLOSURE` | — |
| **S-T3 结果确认硬化** | US-E1-SCH-01, US-E1-SCH-05 | 关键词/智能搜 → 排序勾选 → 进画像；四态闭环 | （主要依赖 S-T2 的 `FE-ENT-SEARCH-STATE-CLOSURE`） | `ENT-ES-ETL-L01` |

**暂缓（不进本 Sprint Goal）**：US-E1-SCH-06 对比篮接力、US-E1-SCH-07 导出。

### 1.2 KEYENT

| Theme | 故事包 | 演示增量 | committed / stretch leaf |
|-------|--------|----------|--------------------------|
| **K-T1 发现集合** | US-KEYENT-01, US-KEYENT-02 | 区域+类型筛选 → 地图/结构 → 企业清单 | committed：`E-ENT-KEYENT-PY-L01`, `E-ENT-KEYENT-JAVA-L01`, `E-ENT-KEYENT-UI-L01`（验收路径 01/02） |
| **K-T2 领域布局** | US-KEYENT-03, US-KEYENT-05 | 选企业 → 领域矩阵/映射依据 → 可进画像 | stretch：同上三 leaf（验收路径 03/05） |
| **K-T3 编组接力** | US-KEYENT-04 | 类型结果入对比篮 ↔ 从篮发起领域分析 | 后续 Sprint；缺口再单列 FE |

KEYENT **不新拆仓任务**；三 leaf 共用，靠 `user_story` + note 中的 Theme 标签区分验收切片。

---

## 2. 端到端演示脚本

### S-T1 筛选可用

1. 角色：政府/园区/投资机构（Persona 任选）  
2. 打开 lumen-ui-topic 企业查询 → 高级筛选  
3. 选择「企业所属地区」全国树至省/市；叠加规模或上市字典条件（有则）  
4. 应用筛选 → 结果列表条数/卡片与条件一致；可再次改条件再筛（触点 SCH-05）  
5. **Pass**：路径无前端→Java→meta/检索断链；空态/错态有提示；Mock 与真实切换策略可口述

### S-T2 初始引导

1. 清空检索进入初始空态  
2. 点击示例查询 / 热门场景 / 最近检索之一 → 进入有结果态  
3. 若有推荐企业，点击可进入画像或结果  
4. **Pass**：`search-biz` 相关接口通或明确降级；四态不卡死

### S-T3 结果确认硬化（stretch 主题）

1. 企业名称关键词检索 → 列表排序/勾选 → 打开画像  
2. 覆盖空/加载/有结果/错误四态（`FE-ENT-SEARCH-STATE-CLOSURE`）  
3. **Pass**：四态闭环；ES ETL 有则列表数据来源可说明

### K-T1 发现集合

1. 打开重点企业分析页  
2. 设定区域范围 + 企业类型（外企/高企等）筛选  
3. 地图/结构视图可见数量或占比；下钻或清单可看到企业集合  
4. **Pass**：前端→Java Feign→Python `/key-analysis/*` 联调通（或手写降级说明进 handoff）

### K-T2 领域布局（stretch）

1. 从集合选 1～N 家企业  
2. 打开领域矩阵/映射依据  
3. 可跳转画像或其他研判入口  
4. **Pass**：US-KEYENT-03/05 路径通

### K-T3（后续）

对比篮进出与领域分析发起连续工作，不纳入本 Sprint Goal。

---

## 3. Registry 挂接约定

每个试点 leaf 须具备：

- `user_story`: 本 Theme 故事 ID（逗号分隔）  
- `note` 追加：`[Theme=S-Tx|K-Tx] 关单须 Theme 演示路径通；见 sprints/ent-scrum-theme-pilot-SEARCH-KEYENT.md`

| leaf | Theme | user_story |
|------|-------|------------|
| ENT-FE-SEARCH-REGION-FILTER | S-T1 | US-E1-SCH-04 |
| ENT-JAVA-SEARCH-REGION-META | S-T1 | US-E1-SCH-04 |
| FE-ENT-DICT-WIRE-L05 | S-T1 | US-E1-SCH-04 |
| DATA-ENT-DICT-IMPL-L02 | S-T1 | US-E1-SCH-04 |
| DATA-ENT-DICT-REGION-SEED-L03 | S-T1 | US-E1-SCH-04 |
| API-ENT-DICT-JAVA-L04 | S-T1 | US-E1-SCH-04 |
| DATA-ENT-LISTING-SCALE-ETL-L06 | S-T1 stretch | US-E1-SCH-04 |
| ENT-JAVA-SEARCH-BIZ | S-T2 | US-E1-SCH-03,US-E1-SCH-08 |
| FE-ENT-SEARCH-STATE-CLOSURE | S-T2 + S-T3 | US-E1-SCH-03,US-E1-SCH-05,US-E1-SCH-08 |
| ENT-ES-ETL-L01 | S-T3 stretch | US-E1-SCH-01,US-E1-SCH-05 |
| E-ENT-KEYENT-PY-L01 | K-T1（+K-T2 stretch） | US-KEYENT-01,US-KEYENT-02,US-KEYENT-03,US-KEYENT-05 |
| E-ENT-KEYENT-JAVA-L01 | 同上 | US-KEYENT-01,US-KEYENT-02,US-KEYENT-03,US-KEYENT-05 |
| E-ENT-KEYENT-UI-L01 | K-T1/T2/T3 全挂 | US-KEYENT-01,US-KEYENT-02,US-KEYENT-03,US-KEYENT-04,US-KEYENT-05 |

---

## 4. Sprint 承诺（写入 `scrum-sprint.yaml` · 2026-W32）

W30（2026-07-21～08-03）收口结束；**Theme 试点正式容器 = 2026-W32**（避免半截 W30 静默加活；叶上原 `sprint_id=2026-W31` 的 KEYENT 等并入 W32 committed 对齐）。

**Sprint Goal**：

- SEARCH：`S-T1 筛选可用` + `S-T2 初始引导` 可按 §2 演示  
- KEYENT：`K-T1 发现集合` 端到端联调通；`K-T2` 为 stretch

**committed_task_ids**：§1.1 S-T1+S-T2 committed + §1.2 K-T1 三 leaf  

**stretch_task_ids**：S-T1 的 L06、S-T3 的 ES-ETL、K-T2 验收（仍用 KEYENT 三 leaf，不另建 ID）

定义轨 RECLOSE / V1-FINAL **不进**本 Goal（可并行，非 Theme 验收对象）。

---

## 5. 扩模块门（pilot-gate）

**在同时满足前，禁止对 COMPARE / EVAL / RISK / RECRUIT 复制 Theme 模板大批量改 sprint：**

1. Planning / Standup 能用 **Theme 名** 讲清本周演示（而非「还剩几个 Java 单」）  
2. **S-T1** Review 按 §2 演示通过，并在上表标 ✅  
3. **K-T1** 三 leaf 联调路径按 US-KEYENT-01/02 演示通过，并在上表标 ✅  
4. Retro 结论：2B 粒度可执行

通过后：复制本文件结构为 `ent-scrum-theme-COMPARE.md` 等，再改对应 leaf 的 `user_story` / Sprint Goal。

---

## 6. 相关链接

- `agent-delivery/user-story-library.yaml`  
- `agent-delivery/产品实现规程.md`  
- `agent-delivery/scrum-sprint.yaml`  
- `agent-delivery/sprints/ent-scrum-pdr-backlog.md`

---

## 7. 演示就绪评估（2026-08-03）

> 非 Theme Done。用于 Standup / 预演：哪些 leaf 已在 integration、谁该带演示。

### S-T1 筛选可用

| leaf | status | sprint_id | 预演关注点 |
|------|--------|-----------|------------|
| DATA-ENT-DICT-IMPL-L02 | integration | →W32 | DIM/meta 是否可被 Java 读到 |
| DATA-ENT-DICT-REGION-SEED-L03 | integration | →W32 | 地区树数据是否全 |
| API-ENT-DICT-JAVA-L04 | integration | →W32 | meta 透传 |
| ENT-JAVA-SEARCH-REGION-META | integration | →W32 | regions 契约 |
| ENT-FE-SEARCH-REGION-FILTER | integration | →W32 | 高筛地区字段 |
| FE-ENT-DICT-WIRE-L05 | integration | →W32 | **演示主路径**（监管：淮政玮） |
| DATA-ENT-LISTING-SCALE-ETL-L06 | integration | →W32 | stretch；无则口述降级 |

**建议预演人**：孔东/曹丽影（FE）+ 侯佳伟（Java）+ 数据侧（DIM）  
**最小 Pass**：高筛选地区 → 结果列表变化可解释；字典失败有降级提示。

### S-T2 初始引导

| leaf | status | 预演关注点 |
|------|--------|------------|
| ENT-JAVA-SEARCH-BIZ | integration | 示例/热门/最近检索 9 接口（监管：侯佳伟） |
| FE-ENT-SEARCH-STATE-CLOSURE | ready | 四态 + 空态引导（尚未开工；可与 S-T2 同场） |

**风险**：STATE-CLOSURE 仍为 `ready`，S-T2 完整四态可能需先认领开工。

### K-T1 发现集合

| leaf | status | sprint_id | 预演关注点 |
|------|--------|-----------|------------|
| E-ENT-KEYENT-PY-L01 | integration | →W32 | /key-analysis/*（徐滕强） |
| E-ENT-KEYENT-JAVA-L01 | integration | →W32 | Feign（侯佳伟） |
| E-ENT-KEYENT-UI-L01 | integration | →W32 | **演示主路径**（孔东）；验收 US-01/02 |

**建议预演人**：孔东 + 侯佳伟 + 徐滕强  
**最小 Pass**：区域+类型筛选 → 地图/清单有集合；链路断点写进 handoff 不算 Theme Done。

### 建议本周动作顺序

1. leaf `sprint_id` 全部对齐 `2026-W32`（与 yaml committed 一致）  
2. Standup 用 Theme 名点名 S-T1 / K-T1 预演时段  
3. 预演通过后在本文件 §0 进度板改 ✅ 并附 Review 纪要路径  
4. **勿**在 S-T1+K-T1 未 ✅ 前批量 Theme 化 COMPARE/EVAL
