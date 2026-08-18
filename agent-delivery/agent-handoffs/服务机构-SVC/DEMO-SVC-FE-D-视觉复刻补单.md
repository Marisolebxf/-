# SVC 段 D · 视觉复刻补单（按 2026-08-17 新规）

> **日期**：2026-08-18  
> **监管**：`human:侯佳伟` · 长任务已授权「后续认领不必再问」  
> **仓**：`lumen-ui-topic` · `origin/dev` · **同仓一次一张** frontend 单  
> **真源**：[`DEMO-SVC-FE-D-总派单.md`](./DEMO-SVC-FE-D-总派单.md) · [`templates/fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)  
> **背景**：Gate-0/1「有数长任务」已跑完且金路径 5/5 绿，但派单**未**按昨晚 D 段 `/goal` 区块清单 + V/R/W 收单。本包补视觉复刻，**金路径绿 ≠ 本包完成**。

## 状态说明（回答「长任务开始了没」）

| 管线 | 状态 |
|------|------|
| Gate-0 底座 + Gate-1 有数/金路径 | **已跑完**（E 冒烟 `ready_to_sign`） |
| 段 D 按新规约的视觉复刻长任务 | **主链已收口**（门户+分析 → `pending_test`；等 QA / 人审截图） |

## 叶（同仓串行）

| 序 | ID | 范围 | 依赖 |
|----|-----|------|------|
| 1 | `LUMEN-SVC-FE-PORTAL-VISUAL-L01` | 门户五 Tab 区块清单 + V1–V7（若适用）+ R1–R5 | ✅ `pending_test`（`404a607`） |
| 2 | `LUMEN-SVC-FE-ANALYSIS-VISUAL-L01` | 分析三键 + 生态 + 招引；R1–R5 + **W1–W3** | ✅ `pending_test`（`db6ef55`） |
| — | `LUMEN-SVC-FE-SEARCH-REPLICA-C2` | 查询+篮 | 已 `integration`，本包不重复开；缺口另开补单 |

## `/goal` 头（每叶必贴）

```
任务：{ID}
仓：lumen-ui-topic · origin/dev
监管：human:侯佳伟 · coordinator_dispatch · lock 24h
强度：ponytail full
复刻：布局+交互+样式+评审+Mock开关。必读 templates/fe-replica-visual-dod.md。
范围：{本叶路由/键，列出区块}。占位与只改 Hero 不算完成。
禁止：贴 JSX；USE_MOCK=false 时硬 mock 或 Demo fixture 填数；自造 ⓘ；再 new 地图。
必读：DEMO-SVC-FE-D-总派单 · fe-replica-visual-dod · demo-ui-topic service-* · Design.md
handoff：V1–V7（查询类）+ R1–R5；工作区另加 W1–W3。缺条 needs-revision。
```
