# FE-DR-BE-API-REQ-L01 · 科技数据资源：前端视角后台接口需求（四 GET Dataset）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 定义任务；只整理「前端 → 聚合」HTTP 需求，不写实现代码 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | definition / 文档类；未改业务仓代码；未用 YAGNI 跳过四 GET / 信封 / 根键清单 |

## 范围与实现

- 复核并修订 `FE-DR-BE-API-REQ-DRAFT.md` → 状态 **READY_FOR_SIGN**。
- 覆盖四视窗四个无参 GET：`/display/v1/data-ops/{overview\|access\|theme\|application}/dataset`。
- 写明 PigX 信封 `code=0 → data`、空库仍 0、键保留。
- 按 `types/dataResources.ts` 列出必有根键（overview 17 / access 11 / theme 6 / application 19）+ 页面用途。
- 写明前端不要求：筛导出 API、WS、主题卡涨跌字段、Nebula 全图、R-01～R-24 直出、直连科学数据中心。
- 待对齐项 A–G 交给 `BE-DR-FE-API-ALIGN-L01`。
- **未改** `lumen-ui-science-pc` / `lumen-svc-platform` 代码；**未替代** `BE-DR-CONTRACT-01` 冻结正文。

## 接线事实（复核）

`src/api/dataResources.ts` 四条 `real()` 仍返回 `create*Dataset()`（注释「接线已撤回」），**未接网关**。四页初值为种子 Dataset。正式 `request()` 接线属 `DR-RES-D1` 或后续叶，本单不做。

## 产物

| 产物 | 路径 |
|---|---|
| 接口需求（可审） | `agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-DRAFT.md` |
| 本 handoff | `agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-L01.md` |

## 测试结果

- 文档任务：对照 `types/dataResources.ts`、`api/dataResources.ts`、`mock/modules/dataResources.ts`、四页 `views/data-resources/*`、`BE-DR-CONTRACT-01`、方案 §5 人工核对根键与「不要求」边界。
- 无业务仓编译 / CI（本叶不改代码）。

## 遗留风险 / 交下游

- 叶 2 `BE-DR-FE-API-ALIGN-L01`：FE↔契约/C 差异 + 聚合→科学数据中心上游需求表。
- 契约文「裸 fetch」与现仓「回种子」不一致 → 记在草稿 §9-F，本叶不改契约。
- 监管人审过草稿后，本 definition 可走会签 / `ready_to_sign`；**done 仅 human:淮政玮**。

## CI/CD

- 仓：`gkx-orchestration`，分支 `dev`
- 仅文档变更；无业务镜像 / K8s rollout

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 前端→Java→… | ✅ 本草稿只要求聚合四 GET；写明不直连科学数据中心 |
| 不写算法 / Nebula 全图 | ✅ |
| D12 demo 隔离 | ✅ 未改 demo；只读 lumen-ui 真源 |
| 不替代契约 | ✅ |
| 可观测 / D8/D9/D10 | N/A（本叶无 UI 实现） |

## 涉及文件

- `agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-DRAFT.md`（修订）
- `agent-delivery/agent-handoffs/科技数据资源-DR/FE-DR-BE-API-REQ-L01.md`（本文件）
