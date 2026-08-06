# DEC · 瓶颈词汇分层（健康 / 瓶颈 / 卡脖子）

| 项 | 内容 |
| --- | --- |
| ID | `DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806` |
| 日期 | 2026-08-06 |
| 模块 | `CHAIN-TOPIC-DIAGNOSIS` / F-DIAG-04 |
| 批准人 | `human:当前会话用户`（评审决定：方案 1 严重度制 + Demo/六文档同步） |

## 决定

1. **两层语义，禁止三词平级**  
   - L1 健康分档：`稳健` / `关注` / `薄弱`（Bid `.5.1`）  
   - L2 瓶颈判定：是否入选瓶颈清单（Bid `.5.2` / 算法 `.3.9`）  
   - L2+ 卡脖子：`瓶颈 ∧ severity=高`（严重度制；正式阈值待算法表）  
2. **关系**：薄弱 ≠ 瓶颈；卡脖子 ⊂ 瓶颈；`卡脖子环节数 ⊆ 瓶颈数`。  
3. **禁词**：本 Tab 禁止「断链」「断链风险」（属企业供应链/服务链叶子）。  
4. **UI**：图例分「健康分档」「判定角标」两行；详情分列「是否瓶颈」「是否卡脖子」；禁止「薄弱/瓶颈」并格。

## 影响

五件套 + FUNC-DESIGN → v1.13；Demo `IndustryBottleneckGraph` / `BottleneckResult` / `industryDiagnosisModel` 同步。
