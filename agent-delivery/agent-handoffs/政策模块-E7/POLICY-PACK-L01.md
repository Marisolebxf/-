# Handoff · POLICY-PACK-L01

> **任务**：政策分析 E7 — 核心产品包（USM/TRACE/IA/Wireframe）  
> **执行**：agent:ux-agent  
> **监管**：human:高颖  
> **日期**：2026-08-05  
> **包版本**：v1.4.3  
> **状态建议**：definition → integration（会签）

## 1. 范围与实现（对照 bid-reference）

| Bid 锚点 | 验收叶子 | 产物落点 |
| --- | --- | --- |
| §1.1.1.2.4.2.6.1 政策时序分析 | P-70 | `/policy/overview` · US-E7-POL-02 · F-POL-01 |
| §1.1.1.2.4.2.6.2 区域政策对比 | P-72 | `/policy/analysis` · US-E7-POL-03 · F-POL-02 |
| §1.1.1.2.4.2.6.3 深圳政策现状分析 | P-73 | `/policy/recommendation` · US-E7-POL-04 · F-POL-03 |
| §1.1.1.1.1.1.2.1～.6 门户政策扶持 | P-17～P-22 | `/policy-portal/*` · US-E7-POL-08 · F-POL-PORTAL |
| §1.1.1.2.4.5.1.6 / §5.6.7 维护 | P-76/P-77（相关） | `/policy/maintenance` · US-E7-POL-09 · F-POL-OPS |

配套：政策查询只入篮（US-01）；系统对比篮政策 Tab 为**唯一分析发起**（US-05）；系统任务（US-06）；统一报告模板 HTML→PDF（US-07）。

**三条系统共享能力**（与企业/产业共用）：① 对比篮 ② 任务浮层 ③ 报告模板（`ENT-EXPORT`：统一模板 → HTML 预览 → PDF）。

**对象流铁律**（`DEC-E7-BASKET-ONLY-LAUNCH-20260805`）：查询/门户结果 → 加入对比篮暂存 → **仅**系统对比篮「发起分析」→ 三项分析。禁止「深度分析」直达。

**分析页空态（对比篮能力 · `DEC-E7-EMPTY-STATE-BY-BASKET-20260805`）**：无分发上下文时，政策篮空→只引导查询入篮；篮内有对象→引导查询或打开对比篮。

**明确排除**：展示系统科技政策跟踪及核增对比结果页；查询/门户直达分析；跳过 HTML 直出 PDF；独立政策任务/下载中心；页内导出替代系统报告。

## 2. 偏离说明

| 项 | 说明 |
| --- | --- |
| 政策密度指数 | `M_POLICY_TOTAL_COUNT` 代理 + GAP-E7-01 |
| screen_tier | 规范化为 `medium_1440_1920` |
| P-71/74/75 | TBD / Wave2，见 TRACE |
| P-76/P-77 | catalog 后台/TBD；以前端维护菜单承接（GAP-E7-08） |
| 查询入口 | DEC-E7-SEARCH-REUSE；结果**只入篮** |
| 对比篮 | DEC-E7-COMPARE-ACTIVATE；**唯一发起分析** |
| 系统任务 | DEC-E7-SYSTEM-TASK-REUSE |
| 报告模板 HTML→PDF | DEC-E7-REPORT-TEMPLATE-HTML-PDF；对齐 ENT-EXPORT |
| 门户展示 | DEC-E7-PORTAL-INCLUDE；展示入篮 |
| 维护管理 | DEC-E7-OPS-REUSE；复用 ENT-OPS 菜单形态 |

## 3. 产物清单

目录：`agent-delivery/agent-handoffs/产品整体定义/E7-政策分析/`

| 文件 | 版本 |
| --- | --- |
| `TRACE-E7-政策分析.yaml` | v1.4.2 |
| `USM-E7-政策分析.md` | v1.4.2 |
| `IA-E7-政策分析.md` | v1.4.2（§3.2 任务 · §3.3 报告模板） |
| `Wireframe-E7-政策分析.md` | v1.4.2（F-POL-REPORT：HTML→PDF） |

## 4. DoD 对照

- [x] USM：角色来自 bid，主/异常 walkthrough + 验收场景  
- [x] TRACE：P-17～22 + P-70/72/73，`screen_tier=medium_1440_1920`；stories=9  
- [x] IA：查询/门户只入篮 + 对比篮唯一发起 + 任务/报告 + OPS  
- [x] Wireframe：F-POL-PORTAL / OPS / TASK / REPORT；无深度分析直达  
- [x] 四份文档位于 `产品整体定义/E7-政策分析/`

## 5. 验收证据

- 本地文件齐套  
- TRACE `leaves_mapped == leaves_required == 9`  
- `ready_for_v1: false`（QPOL / GAP 未闭合）

## 6. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1–2 | 算法 Python；前端→Java→Python | ✅ |
| 7 | 共享对比篮/任务/报告/OPS 壳 | ✅ |
| 9–10 | Design / D9 metric | ✅ Wireframe |
| 11 | D10 | ⏭ POLICY-UX-L01 |

## 7. 开放项

- QPOL-01/02/03/05  
- GAP-E7-01～08  
- 下游：`POLICY-UX-L01`

## 8. Cost（预算回填）

| 字段 | 值 |
| --- | --- |
| actual_tokens | ~150000（估，含 v1.1–v1.4.1） |
| model_used | cursor-grok-4.5 |
| actual_cost | 待会话结算 |
| cost_warn | false |
