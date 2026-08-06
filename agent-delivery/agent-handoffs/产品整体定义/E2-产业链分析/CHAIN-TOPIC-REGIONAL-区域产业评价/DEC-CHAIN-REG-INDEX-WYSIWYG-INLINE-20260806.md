# DEC · 去掉轻量预览，配置区内联「所见即所得」

| 项 | 内容 |
| --- | --- |
| ID | `DEC-CHAIN-REG-INDEX-WYSIWYG-INLINE-20260806` |
| 日期 | 2026-08-06 |
| 模块 | `CHAIN-TOPIC-REGIONAL` / F-REG-02 |
| 批准人 | `human:当前会话用户`（选项 A：五件套 + Demo 同步） |
| 方案稿 | `PLAN-CHAIN-REG-REMOVE-LIGHTWEIGHT-PREVIEW-20260806.md` |
| 废止 | 独立「轻量预览」按钮与 `PI-CHAIN-REG-LIGHTWEIGHT-PREVIEW` 作为交付合同；旧 DEC 中「支持轻量预览」条款 |

## 决定

1. **Bid `.2.3.1` 落实方式**：配置区对**已就绪指标底分**按当前已计入指标与权重做重加权，综合指数（及可选四维）**随调整即时刷新**＝「所见即所得 / 实时计算」。  
2. **删除**：独立「轻量预览」按钮、点击后预览表、`previewing` 用户态、挂点 `CHAIN-REG-F02-PREVIEW`。  
3. **替代**：配置区常驻「配置即时汇总」；旁注「基于底分快照的配置反馈，非正式分析结果」；不建 task、不入分析记录。  
4. **数据边界**：拿产业链对象 ≠ 有综合指数；无底分时不展示伪正式综合指数（Demo 可用 Mock 底分 + 🧪）。  
5. **正式结果**：仍须「生成分析」→ 任务 → 显式查看不可变结果；与即时汇总必须可区分。

## 影响

五件套 v1.5 + Demo `IndustryRegionalPage` / `industryRegionalModel` / 测试同步。
