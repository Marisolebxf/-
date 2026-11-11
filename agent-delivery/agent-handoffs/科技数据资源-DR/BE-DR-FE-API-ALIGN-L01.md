# BE-DR-FE-API-ALIGN-L01 · 聚合→科学数据中心需求 + FE↔契约/C 差异

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（监管人 `/goal` 明示认领；FE 草稿 READY_FOR_SIGN 按可用放行） |
| 仓 | `gkx-orchestration`（文档/handoff；未改业务仓） |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `off` |
| 说明 | definition：只出上游接口需求表与差异摘要，不写实现代码 |

## 修改内容

1. **主交付** `BE-DR-SDC-UPSTREAM-API-REQ.md`：聚合服务（调用方）→ 科学数据中心（提供方）粗粒度接口需求表，覆盖四视窗 R-01～R-24；列 = 界面｜需规seq｜接口中文名｜输入必填｜输入选填｜期望输出。
2. **本文**：FE-DR-BE-API-REQ-DRAFT ↔ BE-DR-CONTRACT-01 / C1～C4 差异结论（默认不改契约、不改前端、不扩对外四 GET）。

## 辅 · FE ↔ 契约 / C1～C4 差异摘要

对照真源（2026-11-11）：

- FE：`FE-DR-BE-API-REQ-DRAFT.md`（READY_FOR_SIGN）+ `lumen-ui-science-pc` types/api/seed
- 契约：`BE-DR-CONTRACT-01.md`（done）
- 实现：`DR-RES-C1-L01`～`C4-L01` handoff（均联调态；读 `gapfill_dr_*`）

### A. 路径 / 信封 / 范围 — 一致

| 项 | 结论 |
|---|---|
| 四个无参 GET | FE 草稿 = 契约 = C1～C4；**不扩** `/sources` `/themes` `/usage` 等 |
| 信封 `{code,msg,data}`，`code===0` 才用 data；空库仍 0 | 一致 |
| 根键计数 | overview 17 / access 11 / theme 6 / application 19；契约与 FE 草稿一致；C1～C4 handoff 声称根键齐 |
| 允许多出 | `origin`、`entityStock`（overview）、`columnCatalog`（theme）— FE 基本不读，契约允许，C1 已出 `entityStock` |

### B. 种子多键 vs 类型 — 禁止 HTTP 出站

| 键 | 种子 | 类型/契约 | FE 草稿 | 结论 |
|---|---|---|---|---|
| `resourceUsageStats.totalCalls` | 有 | **无**（仅四监控数字） | 明确禁止出站 | **禁止**聚合 HTTP 多出该键 |
| `knowledgeGraphNodeDetails.*.parentDB` | 有 | **无** | 明确禁止出站 | **禁止**多出 |
| 应用页 `supplierStats` / `supplierRegionGroups` / `supplierCallDetails` / 部门组等行内 `totalCalls` | 有 | **有**（契约细表必有） | 须保留 | **要有**；与 overview 监控块的 `totalCalls` **分开**，勿混禁 |

### C. 接线事实 — 差异（非契约缺键）

| 项 | 事实 | 处置 |
|---|---|---|
| FE `real()` | 现仓固定 `create*Dataset()`，**未** `request()` 网关（api 头注释「接线已撤回」） | 记差异；正式接线属 `DR-RES-D1`；本叶不改前端 |
| 契约文「裸 fetch」 | `BE-DR-CONTRACT-01` §现有 real() 仍写裸 fetch | 与现仓「回种子」不完全一致；**事实源=现仓代码**；契约叙述修订须人批准，本叶不改 |
| C1～C4 数据源 | 读 gapfill mock 表，非科学数据中心 HTTP | 与主表「上游需求」目标态并列；切供方对接另开实现叶 |

### D. 缺键 / 多余键（相对类型）

| 类别 | 结论 |
|---|---|
| FE 草稿相对契约 | **无缺根键、无改名**；待对齐项 A–G 已由 FE 列出，本叶确认 |
| 契约相对类型 | 仅允许多出 `origin`/`entityStock`/`columnCatalog`；其余不多 |
| C1～C4 相对契约 | handoff 声明根键齐；嵌套空数字/空串见各 C handoff「已知空数」— **属灌数/组装填充度**，非路径缺键；不据此扩 GET |
| 主题涨跌 / 实时监控 | 涨跌页面本地；监控用 `usageCallTrend` 本地跳动 — FE=契约=C4，无第二接口 |

### E. 总判（给监管人）

1. **对外四 GET 冻结可维持**；FE 草稿与契约根键对齐，无需本叶改契约正文或前端 types。  
2. **种子多出类型无的键**（`resourceUsageStats.totalCalls`、`parentDB`）→ **禁止 HTTP 出站**；应用侧行内 `totalCalls` 保留。  
3. **真正缺口在上游供数与接线**：聚合→科学数据中心见主表；前端→网关接线见 D1；现行 gapfill 仅为演示。  
4. 必读「能力对照-科技数据资源-科学数据中心.md」仓内未找到 → 主表已注明；补文件后可修订主表。

## 测试结果

- 文档对照：已读 FE 草稿、契约、C1/C4 handoff、R-01～R-24 清单、对接澄清字段级、`dataResources.ts`、`dataResources.ts` api（回种子）、种子 `totalCalls`/`parentDB`。  
- 未改 Java/前端；未跑构建/CI。

## 遗留风险

- 科学数据中心侧现名/鉴权/是否 HTTP 直出 vs 库表，待总集/供方确认；本表按 R 清单粗粒度预置。  
- FE 叶仍 `integration`（待人会签）；本叶按监管人 `/goal` 放行草稿可用。  
- C4 仍 `integration` 非 done；差异结论以 handoff+契约为准。  
- R-18 检索接口与现行「整包+浏览器筛」策略并存；默认不扩对外 GET。

## CI/CD

- 分支：`dev`（编排仓文档）  
- commit：本叶交付后由会话提交（未 push 业务仓）  
- pipeline / K8s：无（纯文档）

## evidence

| 产物 | 路径 |
|---|---|
| 上游接口需求主表 | `agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-SDC-UPSTREAM-API-REQ.md` |
| 本 handoff / 差异摘要 | `agent-delivery/agent-handoffs/科技数据资源-DR/BE-DR-FE-API-ALIGN-L01.md` |

## 涉及文件

- 新增：`BE-DR-SDC-UPSTREAM-API-REQ.md`、`BE-DR-FE-API-ALIGN-L01.md`  
- 只读：`FE-DR-BE-API-REQ-DRAFT.md`、`BE-DR-CONTRACT-01.md`、`DR-RES-C1-L01.md`～`C4`、`04-…第三方API接口清单.md`、`对接澄清-科技数据资源-字段级.md`、`lumen-ui-science-pc` types/api/seed
