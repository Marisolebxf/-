# POL-REPORT-CACHE · 长任务总控（分解稿）

> **日期**：2026-11-14  
> **授权人**：`human:淮政玮`（只授权到「先分解」）  
> **目标**：中台按报告类型各开一个菜单，用 FDE 做出生成并写入缓存；后台批量跑出正文；再迁到现有 lumen。展示系统现有页面的布局和现有正文保持不动。  
> **模式**：长任务分解。规约：[`长任务执行规约.md`](../../长任务执行规约.md)。设计：[`sdd/简报/2026-11-14-POL-报告缓存架构.md`](sdd/简报/2026-11-14-POL-报告缓存架构.md)  
> **授权句**：2026-11-14 15:40 `human:淮政玮` 确认六类生成逻辑按各稿第 5 节推荐项执行，并确认可以做中台菜单。仍**没有**「后续认领不必再问」。只放开第一张菜单 `POL-RPT-CACHE-DEPTH-MENU`。其余菜单、批量、迁 lumen 仍不认领。禁止改 lumen 页面，禁止写 `gkxlumenx_*`。

## 已拍板

1. **不改 UI 展现**。`lumen-ui-science-pc` 政策动向、政策分析评价上现有的区块、标题、按钮、空态都留着。迁移只换表里的正文，不改模板。
2. **现在屏幕上的内容都还在**。生成失败不删旧行，不把「缺项演示」擦成空白。只有新正文写成功，才在迁移叶替换对应领域的旧演示行。
3. **先中台，后 lumen**。中台 = `demo-ui-system-test`（`origin/dev`）。每类报告一个菜单。每类单独走 FDE（产品定义 → 架构定档 → 中台菜单实现）。中台阶段只写 demo 库，不写 `gkxlumenx_*`。
4. **先能生成一条，再批量**。某类菜单能单条生成并落 demo 缓存后，才允许该类后台批量。
5. **调用链不变**。中台页面 → Java → Python `/internal/*`。Java 不写正文、不调模型。前端不直连 Python。D4 仍是 mock（`is_mock=1`）。
6. **不进本管线**：214 优缺点（实时，不落表）、205/206 图表、222/231 导出壳、223–230 与 226/237 只读、614–618 研报。

升级人：结构歧义 `human:李伟`。锁：开工后 `lock_hours=24`。

## 2026-11-14 确认的生成逻辑

六份稿：`sdd/简报/2026-11-14-RPT-{DEPTH,IMPACT,HOTSPOT,ASSESS,BENCH,INTERP}-生成逻辑.md`。各稿第 5 节第一项已确认。写库统一为 `demo_gkxlumenx_ads` 的同名表。展示页继续读 `gkxlumenx_gapfill`，这一步不换句子。

中台菜单同仓串行，先做深度分析报告。影响评估及以后的菜单等上一张菜单 handoff 后再领。

## 段表

同仓串行。`demo-ui-system-test` 同时只做一张菜单叶。定义叶可按表内顺序做，不并行改同一简报。

| 段 | 长任务 | registry ID | 仓 | 依赖门 | 状态 |
|----|--------|-------------|-----|--------|------|
| M1 定义 | 深度分析报告 FDE | `POL-RPT-CACHE-DEPTH-FDE` | gkx-orchestration | 无 | backlog |
| M1 菜单 | 深度分析报告菜单 | `POL-RPT-CACHE-DEPTH-MENU` | demo-ui-system-test | 上一张 FDE ≥ integration | backlog |
| M2 定义 | 政策影响评估 FDE | `POL-RPT-CACHE-IMPACT-FDE` | gkx-orchestration | 无 | backlog |
| M2 菜单 | 政策影响评估菜单 | `POL-RPT-CACHE-IMPACT-MENU` | demo-ui-system-test | 本类 FDE ≥ integration，且上一张菜单叶已有 handoff | backlog |
| M3 定义 | 热点识别 FDE | `POL-RPT-CACHE-HOTSPOT-FDE` | gkx-orchestration | 无 | backlog |
| M3 菜单 | 热点识别菜单 | `POL-RPT-CACHE-HOTSPOT-MENU` | demo-ui-system-test | 同上 | backlog |
| M4 定义 | 效果评估报告 FDE（211） | `POL-RPT-CACHE-ASSESS-FDE` | gkx-orchestration | 无 | backlog |
| M4 菜单 | 效果评估报告菜单 | `POL-RPT-CACHE-ASSESS-MENU` | demo-ui-system-test | 同上 | backlog |
| M5 定义 | 对标报告 FDE（217） | `POL-RPT-CACHE-BENCH-FDE` | gkx-orchestration | 无 | backlog |
| M5 菜单 | 对标报告菜单 | `POL-RPT-CACHE-BENCH-MENU` | demo-ui-system-test | 同上 | backlog |
| M6 定义 | 政策解读报告 FDE（242） | `POL-RPT-CACHE-INTERP-FDE` | gkx-orchestration | 无 | backlog |
| M6 菜单 | 政策解读报告菜单 | `POL-RPT-CACHE-INTERP-MENU` | demo-ui-system-test | 同上。242 在 lumen 已有读面，本叶只补中台菜单，不重做 lumen | backlog |
| B | 后台批量 | `POL-RPT-CACHE-BATCH` | lumen-algo-py | 六张菜单叶均 ≥ integration | backlog |
| L | 迁到现有 lumen | `POL-RPT-CACHE-LUMEN` | lumen-svc-platform | BATCH ≥ integration | backlog |

FDE 定义叶做到：功能点、中台菜单上必须看见什么、成功/失败/做一半、不改 lumen 展现。菜单叶做到：该菜单能对一条样本生成并写入 **demo** 缓存。批量叶做到：每类至少跑出一批成功正文，失败批次不删已有行。迁移叶做到：正式缺项表出现这批正文；`lumen-ui-science-pc` 本叶 diff 为空；打开原页面仍看得到原区块，有新正文的领域显示新正文，没有的领域仍是现在的句子。

## 依赖

```text
DEPTH-FDE → DEPTH-MENU ─┐
IMPACT-FDE → IMPACT-MENU ┤
HOTSPOT-FDE → HOTSPOT-MENU ┼→ BATCH → LUMEN
ASSESS-FDE → ASSESS-MENU ┤
BENCH-FDE → BENCH-MENU ┤
INTERP-FDE → INTERP-MENU ┘
```

菜单叶之间在 `demo-ui-system-test` 上串行：DEPTH-MENU → IMPACT-MENU → HOTSPOT-MENU → ASSESS-MENU → BENCH-MENU → INTERP-MENU。定义叶不占这个仓。

废作：不要把 214 优缺点改成缓存；不要在本管线改 lumen 政策页模板；不要在中台阶段写 `gkxlumenx_*`。

## 开工顺序（补授权句之后才执行）

1. 六张 FDE 定义按上表做完并会签。  
2. 按菜单顺序在中台实现。每张菜单单独 FDE，不并菜单。  
3. 六张菜单都能单条生成后，跑 BATCH。  
4. BATCH 有成功正文后，做 LUMEN。前端仓不改。  
5. 段 E 只点现有展示页：区块还在，新正文替换成功的领域不再是「缺项演示」开头；没替换到的领域仍显示原句。

卡住只允许：demo 库不可写、正式库误写风险、报告类型边界要改已拍板清单、授权句还没补。
