# INFLUENCE-FIX-L01 验收对照表

> 逐项对照 [spec.md](./spec.md) §5。所有项已在本机实测（2026-11-01），证据见 [INFLUENCE-FIX-L01.md](../../INFLUENCE-FIX-L01.md) §四。

## 一、后端（`http://localhost:7099/v1/situation/influence`）

- [x] 全域无筛选 → `cards.length = 5`、`defaultFactorType = "technologyOutput"`（实测 5 卡：技术产出 / 企业 / 科研机构 / 专家 / 服务项目）
- [x] `regionPaths=[[city-cluster,gba,shenzhen]]` → 企业卡 `count` 显著变小（51,758 → 23,837），机构卡 items 全部「深圳」
- [x] `enabledFactorKeys=["paper"]` → 不含 `institution` 卡（实测仅 1 张技术产出卡，子类仅「论文」）
- [x] `searchTerm=清华` → 机构卡按关键词联动（**实测为榜单内过滤而非整卡消失**：仅剩「清华大学伯克利分校深圳研究院」1 家；spec 原文「整卡消失」基于「湾区无清华系机构」的错误假设，按结果侧过滤更符合 py 能力边界）
- [x] 机构卡 `count == null`；`averageScore = 32.5 ∈ (0,100]`；`items[0].score == 100`；`source` 含「归一化（M_INNOV_ORG_INFLUENCE 范式）」与「专利维未接入」；`caliberNote` 含 log1p / min-max / 缺测重归一
- [x] 三张 mock 卡带 `mock=true / mockReason / mockVersion=influence-v1`；同参二次调用值完全一致（幂等，无随机）
- [x] 换 `timeRange`（2020–2026 → 2010–2026）→ mock 卡值变化（技术产出 94.5→95.5、专家 86.6→87.4、服务 82.8→83.6）

## 二、前端

- [x] `npm run type-check` 0 error
- [x] `npm run build` 构建成功
- [x] `:3000` 页面实跑：切地域到深圳市后企业卡 51,379 → 23,834（筛选联动）；机构卡「对象数量」显示「—」+ 口径说明；公式注释已改「口径注释 + 当前来源」，无虚假复合公式
- [x] 评审关闭零泄漏：`REVIEW_FEATURE.enabled=false` 时 `.mock-badge` DOM 计数 0、无「代码层 mock」/「mock_version」文案，卡片数值与标签正常；验后恢复 `true` 且 `src/review/feature.ts` `git diff` 为 0 行

## 三、文档

- [x] `mock-ledger.md` 追加影响力 3 行（technologyOutput / scholar / service，含真实源指标 ID、缺口原因、接替条件、清理动作）
- [x] `INFLUENCE-FIX-L01.md`：mock 点清单 + 机构归一化待改真实口径（专利维接入后按 0.6923 / 0.3077）+ 已知限制（服务项目卡不可达 / 机构榜不支持年份与领域）
- [x] `task-registry.yaml` + `WBS.md` 登记 `INFLUENCE-FIX-L01`（WBS-05-18-12，`status: integration`）

## 四、闸门

- [x] 两仓改动停本地，**未 commit / 未 push**（`git status` 已核对）
