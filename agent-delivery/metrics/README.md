# metrics/ —— 指标真源目录（D9 数据血缘）

> 模型定义：`../data-lineage-policy.md` §2.3（v1.3.1）。本 README 只讲**这个目录怎么维护**，特别是口径侧（王惠）派单与提交格式。

## 1. 目录内容物

| 文件 | 角色 | Owner |
|------|------|-------|
| `cfg_metric-{域}-seed.yaml` | 指标 8 件套注册真源（ENT / POLICY / CHAIN / TNIE…） | data-agent（口径拍板：王惠/甲方） |
| `metric-readiness-matrix-{域}.yaml` | 四维就绪度真源（**每个要素域一个文件**，如 `metric-readiness-matrix-ENT.yaml`） | data-agent（D2 核验：lineage-subcoord） |
| `README.md` | 本文件 | data lead |

**唯一性铁律**：同一要素域禁止出现第二份矩阵 / 第二份 seed；禁止以 Excel、Word、散落 md 表格形式维护平行状态表。FE 与 API 只认本目录 YAML。

## 2. 口径侧（王惠）派单与提交格式 ⭐

> 背景：口径梳理习惯用 Excel 做工作底稿——**允许**，但 Excel 只是底稿，**不是真源、不进 git 仓**。
> 决策：2026-08-01 项目负责人（淮政玮）。

### 2.1 派单话术必含（coordinator / PM 派单时逐条带上）

1. 产出物 = 对应要素域 YAML 真源的**增量更新**（如 `metrics/metric-readiness-matrix-ENT.yaml` 的 D1 列 + `cfg_metric-ENT-seed.yaml` 的 8 件套），**不是** Excel 附件本身；
2. Excel 底稿列结构须与矩阵 schema 字段对得上（至少含：`metric_id` / 中文名 / 口径定义 / `d1_def_status` 判定 / 关联 Q-* 开放项）；无 metric_id 的新指标行须显式标「待注册」；
3. 交付路径 = 发给 data-agent 正式化，**不要**直接改 YAML（避免格式/枚举错漏），也不要把 Excel commit 进仓；
4. 业务口径歧义不得自行拍板 → 登记 `客户决策清单跟踪表.md`（🟡），矩阵对应条目保持 `d1_def_status: draft`。

### 2.2 data-agent 正式化步骤（收到 Excel 后）

1. 逐行核对 metric_id 是否在 seed；新指标先注册 seed（8 件套），再入矩阵；
2. 更新矩阵对应条目（通常只动 D1 列 + `d1_pending_ref`；D2/D3/D4 不随口径提交联动）；
3. 矩阵头部更新 `updated` 日期 + 在生成任务注释追加来源任务 ID；
4. 枚举校验（`aligned|draft|missing` 等）+ 汇总统计段刷新；
5. commit message 标 `[agent:data-agent]` 并注明「正式化自 王惠 {日期} Excel 底稿」；
6. 同步通知 FE（demo 镜像 `readinessSeed.ts` / Wave 1 catalog API）。

### 2.3 验收标准（handoff 必附）

- [ ] YAML 可被解析（无缩进/枚举错误），统计段与条目一致
- [ ] 每条 `draft` 都挂 `d1_pending_ref`（Q-* / GAP-*），且与 `客户决策清单跟踪表.md` 一致
- [ ] 无第二真源：Excel 未进仓、无平行状态表
- [ ] `aligned` 条目有口径定义落在 seed 的 `definition`（≥50 字，policy §2 第 3 项）

## 3. 就绪度矩阵维护规则（速查）

- D1 由口径提交驱动（上文）；D2 由架构/data-agent 评估 + lineage-subcoord 核验（`pending→ready/partial/missing`，`provisional→verified`）；D3 由 GDF 映射结论驱动（8/20 后复判）；D4 由数据工厂接入事实驱动
- 任何维度**禁止**在无证据情况下改绿（policy §2.3 诚实性约束）
- 矩阵变更后 demo 侧镜像同步任务：见 `agent-handoffs/ENT-MOD-EVAL-READINESS-UI-L01.md` 模式

## 4. calc-logic/ · 指标计算逻辑真源（md 文件）

> 背景：口径侧（王惠）Excel 底稿含多级子指标（L1/L2/L3）的详细口径定义、计算逻辑、源表字段等信息，超出 seed yaml 8 件套的摘要粒度。为方便编排智能体（Cursor 等）随时按需读取，将底稿正式化为**按目录 + README.md 索引**的 md 文件。
> 决策：2026-08-18 项目负责人（淮政玮）确认入仓方案。

### 4.1 目录结构

```
metrics/calc-logic/{域}/
├── README.md          ← 索引：列出全部指标 ID + 名称 + 一句话描述 + 文件链接
├── M_{域}_*.md        ← 每个指标 ID 一个 md 文件
└── ...                ← 多级子指标合并为单文件（文件内按 L1→L2→L3 分节）
```

当前已入仓：`calc-logic/ENT/`（企业域，60 个指标 ID，134 行底稿 → 60 个 md + 1 个 README）。

### 4.2 md 文件规格

**单行指标（仅 L1）**：
- 元数据（指标ID / 名称 / 模块 / 频率 / 对齐状态 / 是否在数据库 / 关联Q编号）
- 口径定义、计算逻辑说明、源表字段、待建表字段、备注

**多级子指标（L1 + L2/L3）**：
- L1 节：指标一级的元数据 + 口径定义 + 计算逻辑 + 源表字段
- 子指标详情节：按 L2 维度分小节，每个 L3 子指标列出独立的口径定义、计算逻辑、源表字段、对齐状态、数据库支持
- 同一 `metric_id` 的所有行合并为单文件，文件内按层级嵌套

### 4.3 与 seed yaml 的关系

- seed yaml 的 `calc_logic_ref` 字段指向本目录下的 md 文件路径（如 `metrics/calc-logic/ENT/M_ENT_TOTAL_COUNT.md`）
- seed yaml 保持 8 件套摘要级信息；md 文件提供完整口径细节（含子指标）
- 口径变更时：先更新 md 文件，再同步 seed yaml 的 `definition` / `formula` 等字段

### 4.4 维护规则

1. 口径变更流程：王惠更新 Excel 底稿 → data-agent 重新生成对应 md 文件 → commit message 标 `[agent:data-agent]` 并注明「正式化自 王惠 {日期} Excel 底稿」
2. Excel 底稿**不进 git**（符合 §2 政策）
3. 文件命名：`{metric_id}.md`，与 `metric_id` 一一对应
4. 多级指标合并：同一 `metric_id` 的所有 L1/L2/L3 行合并为单文件
5. 新增域时在 `calc-logic/` 下新建子目录（如 `calc-logic/POLICY/`），并生成对应的 README.md 索引

## 5. 算法任务结果落点（2026-08-21）

算法梳理 / 算法库分析 / 指标依赖类任务的 **handoff 与分析表一律落本目录**，不要写到 `agent-handoffs/`。派单包仍可放 `agent-handoffs/算法库联调-ALGO-LIB/`（给人派单，不是结果）。

| 路径 | 用途 |
|------|------|
| `algo-results/` | 算法叶 handoff + 分析表。A1 双表：`*-requirements.yaml` + `*-metrics.yaml` + 8/25 `*-ods-gaps.*`；schema 见同目录 `ALGO-LIB-METRIC-DEPS-L01-schema.md` |
| `request/` | **A2 页面/专题差集**（`专题系统/`、`展示系统/`）+ 展示半成品 xlsx；schema：`request/A2-GAP-schema.md` |
| `indicator-inventory/` | 旧四叶草稿（只读） |
| `calc-logic/{域}/` | 王惠口径计算逻辑 md（B 轨已入 CHAIN/SVC） |
| `cfg_metric-*.yaml` / `metric-readiness-matrix-*.yaml` | 8 件套与就绪度；A 轨分析叶默认不改 |

Excel 底稿仍不进 git。
