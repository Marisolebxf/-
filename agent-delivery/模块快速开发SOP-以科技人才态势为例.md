# 模块快速开发 SOP（从科技发展态势沉淀 · 以科技人才态势为首个应用）

- 版本：v1.0 · 2026-11-06
- 作者：agent:coordinator-agent（监管：human:孔东）
- 来源：科技发展态势（TS）9 子模块完整交付经验 + 久新对接探底 + 算法库联调沉淀
- 适用：展示系统 / 专题系统任意新模块开工（下一个：科技人才态势 TA）
- 机器真源索引：各节「真源」字段为准，本文只做导航与检查单，**不复制规范正文**
- 使用方式：新模块开工时按 §10 检查单逐项打勾；每完成一个模块，向 §11 追加本模块教训

---

## 0. 全流程一张图

```text
① 模块定位（WBS/需求/原型三对齐）
        │
② WBS 创建（system-wbs.yaml + project-plan.yaml）
        │
③ 任务创建与关联（task-registry 建单 → scan/confirm 解锁 → 认领）
        │
④ 文档留痕骨架（agent-handoffs/{模块}-{缩写}/ 目录 + 规划真源文档）
        │
⑤ 对接开发（契约先行：集成卡/API 契约单；FE mock 先行，BE 契约冻结后联调）
        │
⑥ 维度读库（本仓五库 + 久新只读通道 + 数据源映射登记）
        │
⑦ 算法支持（STAT→GDF→ADS；MODEL/GRAPH→Python /internal/*）
        │
⑧ 联调测试（产品实现规程 I2 门 → D9 防漏 → I3 验收关闭）
        │
⑨ 收尾（经验清单追加 + Retro + handoff 归档）
```

---

## 1. 模块定位（开工第一步，半天内完成）

| 动作 | 真源 / 模板 |
|------|------------|
| 需求叶数清点 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/{模块名}/*.md`（分册逐页） |
| 需求↔原型对照 | demo 仓对应 `src/pages/**` 逐区块比对（TA 样例：`demo-ui-science/src/pages/talent-trend/`，4 页 36 组件 ≈ 11k 行） |
| WBS 定位 | `agent-delivery/system-wbs.yaml#elements`（E1~E7 七要素）；样例 E5 人才：`type: chain`、`primary_indicators: 4`、`integration: third_party_api`、`java_module: gkxlumen-topic-talent` |
| 历史遗留区分 | 试点/旧版目录明确**不作为复刻真源**（TA 例：`科技人才态势-DS15/` 与 `talent-preview/` 已废止，真源只有 `talent-trend/`） |

**产出**：一行结论——本模块对应 WBS 要素 id、demo 真源目录、SRS 分册路径、叶数统计。

---

## 2. WBS 创建

1. `system-wbs.yaml#elements` 增补/确认本模块条目（字段：id/name/type/primary_indicators/deep_models/integration/python_repo/java_module/topic_pages/display_pages）。
2. `project-plan.yaml` 增补本模块 stages（每阶段：id/title/window/owner/exit_criteria/nodes[]，node 挂 `task_ids`）。
3. 波次归位：`system-wbs.yaml#waves` 确认本模块所属建设波次；integration=third_party_api 的模块（如 TA）须同步登记三方接口依赖文档（见 §7）。

> 真源：`agent-delivery/system-wbs.yaml` · `agent-delivery/project-plan.yaml`（PM 交付阶段）

---

## 3. 任务创建与关联（task-registry 建单）

> 完整规约见 `task-creation-guide.md` / `task-claiming-guide.md`，此处只列模块开工必走的路径 A。

### 3.1 建单（PM/架构师，leaf 一律 `backlog`）

```text
Task ID：{Epic前缀}-{模块缩写}-{类型}-{序号}
样例：FE-TA-01A · BE-TA-CONTRACT-01 · FE-TS-01A · ARCH-TS-L3-01
```

- **定义轨**（`delivery_phase: definition`）：按 `产品定义评审规程.md` §9.1.1 链（PACK → METRIC-OPEN ∥ UX → 门1 → DG-G3）。
- **实现轨**（`delivery_phase: implementation`）：按 `产品实现规程.md` §8.1 拆单，`depends_on` 必含本模块 `*-DG-G3`；门 3 之前禁止标 `ready`。
- 复制模板：`templates/task-leaf-template.yaml`；最低必填字段：id/title/epic/agent/repo/depends_on/status/delivery_phase/priority/definition_of_done。
- 接口侧**一张大单**模式（TS/TA 均采用）：`BE-{模块}-CONTRACT-01`，内部拆分与排期由接口负责人自决（TA 样例：human:李伟）。

### 3.2 关联与解锁

- 同模块 leaf 共用 `parent`（如 `*-DG-G3`）便于追溯；`depends_on` 无环、上游必须已存在。
- 解锁走 **scan → confirm**（`自动派单与确认规约.md`）：上游 done 后 `coordinator-dispatch.mjs scan` → PM confirm → backlog→ready + 派单包。
- 缺口检测：`node scripts/suggest-registry-tasks.mjs scan --module {模块}`（缺 leaf / 坏依赖自动建议，PM 审阅后 merge）。
- Sprint：Planning 时写 `sprint_id` 进 `scrum-sprint.yaml#committed_task_ids`；认领时 `supervised_by` 必填真人真名（与 commit `[human:真名]` 一致）。

### 3.3 批次化（TS/TA 经验）

- 批 1 = 模块基座（FE-S01）+ 首个整页 + 契约单启动 → 地图/筛选/抽屉全能力在首页试点。
- 批 2 = 复用批 1 沉淀的其余整页；体量最大页（XL）单独排。
- 批 3 = 尾页 + 契约冻结后真机联调收尾；每批独立上 K8s dev 验收。

---

## 4. 文档留痕骨架（模块目录规范）

> 一切过程物落在 `agent-delivery/agent-handoffs/{模块名}-{缩写}/`，TS 样例 99 文件，结构如下：

```text
agent-handoffs/科技发展态势-TS/
├── TS-模块开发规划与任务拆分.md      ← 模块开工真源（决策/约束/拆分/契约对齐）
├── {模块}-demo-lumen复刻经验清单.md  ← 教训真源，每次整页复刻后追加（挂 AGENTS.md 摘要镜像）
├── API-{模块}-M*.md                 ← 各子模块 API 契约
├── BE-{模块}-CONTRACT-01.md         ← 接口契约总单
├── ARCH-{模块}-L3-*.md + sdd/l2/    ← 分层设计 + 会签
├── FE-{模块}-01A~10A / S01.md       ← 整页复刻 handoff（一单一档）
├── {X}-spec/ + {X}-tasks/           ← spec 与任务成对
├── 派单说明/                        ← 派单包
├── mock-ledger.md                   ← mock 种子台账（真源/冻结来源/同步任务 ID）
└── REVIEW-*.md / *-REMEDIATION      ← 评审与整改
```

**必用模板**（`agent-delivery/templates/`）：`handoff-template.md`（handoff 最小骨架 + 7 项 checklist）、`test-case-template.md` / `test-record-template.md` / `test-retest-template.md`、`acceptance-test-report-template.md`、`metric-spec-card-template.md`（D9 指标卡）、`task-leaf-template.yaml`。

**CMMI 卷留痕**：`工程过程/` 只索引不搬家——过程记录入对应 00~09 卷，每日进展入 `工程过程/当日进展/`。

**handoff 7 项 checklist**（coordinator 验收门）：范围 / 偏离 / 验收证据 / 架构合规自检 / 图即契约 / D9 角标防漏 / cost。真源：`产品实现规程.md` 附录 A–E。

---

## 5. 对接开发（契约先行 + mock 先行）

1. **调用链铁律**：前端 → Java REST（`gkxlumen-platform-gateway`）→ Python `/internal/*`；Java 不写算法、只读 ADS；前端不感知 Python。
2. **契约真源**：集成卡（TA 样例：`agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A12~A15.yaml`，含 contract_draft / metric 挂接 / 无源 IP 清单）→ 由 Java 侧出具 `API-{模块}-*.md`；**前端不猜路径**，DTO/枚举 Java 主导定稿。
3. **并行策略**：FE 不依赖 BE 契约——mock 种子冻结自 demo 先行（`USE_MOCK` 统一开关，`USE_MOCK=false` 零 fixture 直连网关）；契约冻结后切真机联调。
4. **无源项**：mock 态照 demo 渲染 + 🧪 MockBadge 复刻期不删区块；联调期按集成卡 `metric_missing` 清单空态 + ⚠️，**禁止 fixture 顶替**（不伪闭合）。
5. **D9 血缘**：每个统计数字旁 ⓘ（metric_id 经 `/metrics/v1/catalog`）；指标注册种子 `metrics/registry/cfg_metric-{模块}-seed.yaml` + `metric-readiness-matrix-{模块}.yaml`（过渡态只读镜像，禁前端手写状态）。

> 真源：`agent-delivery/data-lineage-policy.md` v1.3 · `agent-delivery/Design.md` §7.4.1 · 各模块「模块开发规划与任务拆分」§0 决策表

---

## 6. 维度读库

### 6.1 本仓库读库（自建五库）

- **连接真源**：`agent-handoffs/算法库联调-ALGO-LIB/algo-mysql-connection-info.md`（MySQL `10.50.11.76:3306`，五业务库 `gkxlumenx_ads/dwd/dim/cfg/ods`，应用账号 `gkxlumenx`）；demo PG `117.50.223.145`（仅 demo）。
- **架构铁律**（`agent-delivery/数据库设计.md` §1）：Java 业务 API **仅查 ADS + app_user，禁扫 ODS/DWD**；Python 写、API 读；图谱主存 Nebula（禁 Neo4j）；ES 8.x。
- **ADS 契约面冻结**（§12）：Mock 由 Python 写 ADS，`calc_batch_id` 前缀 `mock_`；契约面变更须走登记。
- **Python 读链**：`agent-delivery/企业维度-Python微服务架构预设计.md` v1.3——Java 聚合层只读 ADS + Feign 调 Python `/internal/*`，Python 直连 ES/Nebula/PG；**所有数据含指标元数据均经 Python，Java 不直读**。

### 6.2 数据源映射（维度对照）

- 登记表：`agent-delivery/data-source-mapping-registry.yaml`，状态机 `pending_source → mapped → verified`；条目含 std_table/std_fields/source_system/field_map/transform_rule——**填表，不另立文档**。
- 数仓对照文档：ADS_SCHEMA（6.30.0）为列名核对真源；TS 探底结论「缺的不是数据是对照关系」——新模块先补 `field_map` 再谈接口。

### 6.3 久新库读库（三方只读通道）

- **探底经验**（真源：`agent-handoffs/科技发展态势-TS/SITUATION-ENT-D-维度打通任务单草案.md`）：
  - 久新只读账号（`test2`）**无 information_schema 权限**——列名用逐表 `SELECT * ... LIMIT 1` 实测；
  - 逐表核对 ADS_SCHEMA 数仓文档后再映射，禁止凭文档直写 `field_map`；
  - 依赖北京九新的交付形态（SQL / Python / API）以确认清单为准：`agent-handoffs/算法库联调-ALGO-LIB/JIUXIN-TECH-ORG-TALENT-L01.md`。
- **调研档案**：`agent-handoffs/系统集成-SYSINT/SYSINT-CMP-02-L01/久新数据库调研/`（久新 130 表溯源深度调研等 3 份）。
- **模块级接口依赖清单**（TA 必读）：`工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/05-科技人才态势-科技发展态势-科技知识图谱-第三方API接口清单.md` 与 `06b-科技人才态势-久新侧接口需求（字段级）.md`（85KB，字段级需求）。

### 6.4 深度模型数据（Nebula/ES）

图谱/关系类（TA 例：合作网络、研究领域图谱）主存 Nebula，经 Java→Python 链路取数，前端不感知存储引擎；图数据 schema 按 `agent-delivery/graph-engine.md`。

---

## 7. 算法支持

| 算法类型 | 分流 | 落点 |
|----------|------|------|
| STAT 统计类 | GDF 出 ADS | 各模块负责人 Java 只读聚合 |
| MODEL / GRAPH 深度类 | Python（监管：算法负责人） | Python `/internal/*` → Java 聚合 |

- **工作流真源**：`agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md`（「两套合同、一个指标对象、按算法类型分流」）。
- **算法仓样例**：`repos/demo-algo-science/README.md` + `算法设计说明.md`（mock ODS → P1–P9 流水线 → 写 MySQL `gkxlumenx_*`；本仓只暴露健康检查 + 流水线触发；CI → Harbor → K8s）。
- **TA 算法需求**：`bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/人才/深度分析.md`；指标口径种子 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
- **铁律**：算法侧任务拆分由算法负责人统筹决策，模块规划文档中 ALGO 行**仅列参考输入，不作为派发依据**。

---

## 8. 联调测试

1. **门 I2 联调集成门**（`产品实现规程.md` §6，I2-01~12）：契约冻结 → 真机切换 → 联调检查单（附录 C）逐项过。
2. **异步分析工作区**（若模块有）：I2-12 / 附录 E——切条件不自动起任务、条件栏「开始分析」、同用户同条件仅一条在跑、当天已成功直接打开结果。
3. **D9 防漏扫描**（附录 D，强制）：D.1 页面差集 → D.2 本地 KPI；关闭评审模式后 DOM 零泄漏（不得出现 `metric_id` / `Q0xx` / `GAP-*` / 就绪度字样）。
4. **验证三绿**：`pnpm type-check`（vue-tsc 空跑）0 错 + 最小自检 `test.mjs` + `pnpm build`；状态机移植保留最小自检。
5. **验收留痕**：`templates/test-record-template.md` + `test-retest-template.md`（回归）+ `acceptance-test-report-template.md`；e2e 演示按 `acceptance-e2e-demo-template.md`。
6. **Convoy 串行**：联调类 leaf 注明 Convoy（`dispatch-queue.yaml#convoy_groups`），同组 WIP=1。

---

## 9. 收尾沉淀

- 整页复刻教训追加进 `{模块}-demo-lumen复刻经验清单.md`（附出处 task-id），并同步 AGENTS.md 仓级摘要。
- 数据源映射条目推到 `verified`；mock-ledger 关闭 mock 项。
- Retro 补单走 `task-creation-guide.md` §4.3；贡献分按 `effort_points` 结算（`report-contribution.mjs`）。

---

## 10. 新模块开工检查单（复制即用）

```text
□ 1  WBS 条目确认/增补（system-wbs.yaml#elements + waves）
□ 2  SRS 分册叶数清点 + demo 真源目录锁定（区分历史试点遗留）
□ 3  模块目录 agent-handoffs/{模块}-{缩写}/ 建立 + 规划真源文档（决策表/约束/拆分）
□ 4  定义轨 leaf 入库（§9.1.1 链，backlog）→ 门1 → DG-G3
□ 5  实现轨 leaf 入库（§8.1 链，depends_on 含 DG-G3）+ 批次划分
□ 6  集成卡/契约单启动（BE-{模块}-CONTRACT-01）+ FE mock 种子冻结先行
□ 7  数据源映射登记（data-source-mapping-registry.yaml）；涉久新：先读 §6.3 三份文档再探底
□ 8  指标注册种子（cfg_metric-{模块}-seed.yaml + readiness-matrix）
□ 9  算法分流确认（STAT/MODEL/GRAPH）+ 算法负责人对齐
□ 10 复刻经验清单建档（AGENTS.md 摘要镜像挂接）
□ 11 联调门 I2 + D9 防漏扫描 + 验证三绿
□ 12 收尾：经验追加 / 映射 verified / mock 台账关闭 / Retro
```

**科技人才态势（TA）现状核对**：□1~□5 已完成（`TA-模块开发规划与任务拆分.md` 定稿 + FE-TA-S01/01A~04A + BE-TA-CONTRACT-01 已入库）；□6 集成卡 A12~A15 ready_to_sign；□7/□8/□9 待办（外部接口 05/06b 清单 + cfg_metric-TALENT-seed 已备好，待挂接）；□10 沿用 TS 复刻经验清单（FE-TA 教训已在附）。

---

## 11. 模块教训追加区

| 模块 | 教训真源 | 状态 |
|------|---------|------|
| 科技发展态势 TS | `agent-handoffs/科技发展态势-TS/TS-demo-lumen复刻经验清单.md` | 持续追加中 |
| 科技人才态势 TA | 同上（FE-TA-01A/02A/03A 教训已并入附表） | 进行中 |

> 每完成一个模块：在 `system-wbs.yaml#elements` 回写实际交付形态，并向本节追加一行。
