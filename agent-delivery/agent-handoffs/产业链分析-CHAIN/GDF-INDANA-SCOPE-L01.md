# GDF-INDANA-SCOPE-L01 · 行业分析禁令裁定包 GDF-INDANA-SCOPE-v1（WBS-06-06B）

> 日期：2026-11-09 · 性质：裁定叶（**不是 Mapping 成包**）· 优先级：市场研究红标第 3

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent`（协作 data / product） |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 派单说明 `派单说明-市场研究红标成包-20261109.md` 优先级 3 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off`（定义 / 裁定叶，派单指定） |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 纯文档裁定，未挂载 |

## 范围与实现

- **裁定结论**：行业分析六表现行**只贴 ODS**（`gkx` → `gkxlumenx_ods` 同名镜像，施工入口仍是 CHAIN-v2 Wave A）；**禁止洗项目 DWD**（`CHAIN-B2-INDANA` 继续关闭，李伟 2026-09-01）；`GDF-INDANA-WORKPACK` 不开。
- 对照 WBS-06-06 / 06B、`GDF实施工作范围` §2 / §4、CHAIN-v2 `00`/`02`/`06`/`09`/`10`。
- 本叶只收口既有禁令，**不新增、不放宽**；业务口径未触碰。

## 产物清单

| 产物 | 路径 |
|---|---|
| 裁定包 README | `agent-delivery/data/GDF/派单包/行业分析/GDF-INDANA-SCOPE-v1/README.md` |
| 裁定说明书（结论 / 依据 / 六表 / 禁止项 F1–F7 / 解禁占位 U1–U6 / companies 102 / 冲突处理） | 同目录 `00-裁定说明书.md` |
| 只贴表清单（mirror_only，与 CHAIN-v2 `02` 一致） | 同目录 `02-只贴表清单.yaml` |
| 派单包索引 | `agent-delivery/data/GDF/派单包/README.md`（新增「裁定 / 只贴，非 Mapping 包」小节） |
| WBS 指针 | `…/06-GDF数据治理集成/WBS.md` WBS-06-06B 行 |

## 偏离说明 / 要点

1. **storage 店面冲突**：`storage/CHAIN` 行业分析店面（draft，`OPEN-CHAIN-INDANA-05` 待李伟会签）写了「入站 → 项目 DWD 去前缀」。裁定：它是**设计态，不构成施工授权**；GDF 只认 CHAIN-v2；设计快照 SQL 禁止 APPLY。未改该店面（避免与其会签流程混淆），建议李伟会签时一并确认。
2. **「弱信号」旁路**：实施工作范围 §4 提到「只读 ODS + 算法」。本裁定**不授权**；若要做须另叶 + 会签，且不得冒充正本反馈维。
3. **解禁占位 U1–U6 全空**：须李伟 / 架构师 / product 书面，agent 不得代填；空即未解禁。
4. `SYSINT-06-06-L01` 完成口径 = CHAIN-v2 Wave A 六表对账回执；**只贴不算 Mapping 跑通**，本叶 done ≠ 跑通叶 done。

## 验收证据

- 六表名 / 行数（1,000 / 102 / 3,047 / 1,052 / 1,000 / 1,000）取自 `GKX数据源表及行数报告-20261109-1026`；表名与 CHAIN-v2 `02-WaveA-贴源表清单.yaml` `chain_indana` 组逐表一致。
- 相对链接已逐条 `Test-Path` 核对。

## 架构合规自检（D12 等）

| 铁律 | 结果 |
|---|---|
| 算法只在 Python / 调用链 / Nebula / 可观测 | ✅ 不涉及 |
| D12 demo/lumen 隔离 | ✅ 仅编排仓文档，不涉及 demo 服务 |
| D14 / D16 / D18（不新建 gapfill / mock 表） | ✅ 未建表；明确禁止 gapfill 冒充补数 |
| 业务口径不由 agent 拍板（§3.8） | ✅ 仅范围裁定；解禁归人 |
| 只读 ADS 链路（F6） | ✅ 禁止直读 ODS 出数 |

## CI/CD

- 分支：`origin/dev`（编排仓，无业务 CI）
- commit：`[agent:architect]`，见 git log
- pipeline / K8s：N/A（纯文档）

## Cost

| 字段 | 值 |
|---|---|
| model_used | Claude Sonnet 5.5 |
| actual_tokens | 估 ~6 万 |
| actual_cost | 估 <$2 |
| cost_warn | green |
