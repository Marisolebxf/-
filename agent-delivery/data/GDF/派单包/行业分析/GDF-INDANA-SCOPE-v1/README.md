# GDF-INDANA-SCOPE-v1 · 行业分析：裁定 / 只贴（非 Mapping 包）

> **这不是可投递的 Mapping 包。** GDF 团队无需为本目录建任何 Mapping / DWD / ADS 作业。  
> 日期：2026-11-09 · 任务 `GDF-INDANA-SCOPE-L01`（WBS-06-06B）· 监管 `human:淮政玮`  
> 优先级：市场研究红标 **第 3**（MACRO → FIN → INDANA）

## 一句话

行业分析六表**只贴 ODS**（`gkx` → `gkxlumenx_ods` 同名镜像），**禁止洗项目 DWD**（`CHAIN-B2-INDANA` 关闭，李伟 2026-09-01）。`companies` 仅 102 行，**禁用于覆盖维**。**不解禁，不开 `GDF-INDANA-WORKPACK`。**

## 文件

| 文件 | 内容 |
|---|---|
| [00-裁定说明书.md](./00-裁定说明书.md) | 裁定结论 · 依据 · 六表清单 · 禁止项 · **解禁条件占位（须李伟/架构书面）** · companies 102 · 与 storage 店面 draft 的冲突处理 |
| [02-只贴表清单.yaml](./02-只贴表清单.yaml) | 六表 `mirror_only` 机读清单（与 CHAIN-v2 `02` 的 `chain_indana` 组一致） |

> 编号 `01` 不使用，保留给「若解禁后的 Mapping 包」（届时另开 `GDF-INDANA-WORKPACK`，不在本目录）。

## 施工入口

- 贴源：仍走 **[GDF-CHAIN-WORKPACK-v2](../../产业链/GDF-CHAIN-WORKPACK-v2/) Wave A**（`02` 的 `chain_indana` 组）。
- 本目录不新增作业；`SYSINT-06-06-L01` 的完成口径 = CHAIN-v2 Wave A 六表对账回执，**只贴不算 Mapping 跑通**。

## 解禁

见 [00 §5](./00-裁定说明书.md)。U1–U6 全部由 `human:李伟` / 架构师 / product 书面填齐前，一律视为未解禁；任何 agent 不得代填。
