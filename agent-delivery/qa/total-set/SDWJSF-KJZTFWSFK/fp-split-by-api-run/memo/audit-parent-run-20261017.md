# 父控全库复核报告（不进 F4）

- **时间**：2026-10-17（父控自动扫 + P0 金样断言）
- **catalog**：`lumen-ui-algo-apiview/src/catalog`（**184** 个 `endpoint.id`）
- **work / review**：60 / 60 齐全
- **脚本**：`scripts/audit_l6_catalog_binding.py`（可重复执行）

## 结论（自动硬门禁）

| 检查项 | 结果 |
|--------|------|
| **3c** `endpoint_id` + `field_key` 全库唯一 | **通过** |
| **7b** `catalog_status` ∈ live / unavailable / req_only | **通过** |
| **页归属** work 中每个 `endpoint_id` ∈ `_l6-to-catalog-map.yaml` 的 `pages[]` | **通过** |
| **L13** 仅 `comp.graph.*`（6 个） | **通过** |
| **L05–L12** 无 `comp.graph.*` | **通过** |
| **表解析** 每行 11 列（无未转义 `\|` 破坏） | **通过** |
| **meta 表行数** = 实际数据行 | **通过**（曾 L04 27→28，已修） |

**自动硬门禁：绿。** 仍 **不进 F4**，等人签收 L13 + 文档真源同步（见下）。

## P0 金样断言（L13 类错挂）

| 六级 | 期望 | 实测 |
|------|------|------|
| L13 | 仅 6× `comp.graph.*` | OK |
| L05 | 仅 `chain.panorama.ops` | OK |
| L14 | 仅 `chain.panorama.main`（ops 在 L05） | OK |
| L06 | 无 catalog 行（写入契约见 L05） | OK |

## 文档 / 提示词漂移（非 work 表错，但会导致下次派单再错）

| 真源 | 问题 | 建议 |
|------|------|------|
| `fp-split-by-api-playbook.md` | 仍写「图谱 endpoint 主挂 L13」「L05–L12 契约见 L13」 | PM/父控改 playbook §F2/F3 |
| `科技专题服务算法库-功能点拆分原则-by-api.md` | §4A 仍「构建主挂 L13」 | 与 2026-10-17 方案 A 对齐 |
| `prompts/L14.md`–`L60.md` | 模板尾仍含旧 4A 话术（与 L05–L12 已改不一致） | 批量改为「不适用 / 见 map」或删旧句 |

**本轮 work 未再检出「L13 式整页错挂」**；漂移项是 **再发子 agent 时的复发风险**。

## 人检闸门（父控不能代签）

- [ ] **L13**：apiview 下拉 6 接口 ↔ `work/L13.md` 字段行（39 行 + 2 req_only）
- [ ] **L05 / L09 / L14**：抽检描述是否可验收（脚本只验 id 归属）
- [ ] **L02–L03、L15–L60**：按业务理解 spot-check「六级名 = 该 catalog 页」— 自动扫仅验 **id 落在 map.pages**，不验语义是否像 L13 那样张冠李戴

## 各六级 endpoint 页归属（摘要）

| Lxx | #endpoint_id | catalog pages |
|---|---:|---|
| L01 | 10 | chain.basic |
| L02 | 7 | entan.basic |
| L03 | 2 | policy.basic |
| L04 | 1 | svc.basic |
| L05 | 1 | chain.panorama |
| L06 | 0 | — |
| L07 | 2 | policy.graph |
| L08 | 4 | policy.graph |
| L09 | 2 | entan.graph |
| L10 | 10 | entan.graph |
| L11 | 2 | svc.graph |
| L12 | 8 | svc.graph |
| L13 | 6 | comp.graph |
| L14 | 1 | chain.panorama |
| L15–L60 | 各 1–4 | 与 map 一致（见脚本输出历史版） |

全表 60 行见本文件 git 上一版或重跑脚本。

## 下一步（仍不进 F4）

1. 人签收 **L13**（及可选 L05–L14 抽检）
2. 同步 **playbook + 原则 §4A**（防复发）
3. 可选：父控派单 **L02–L60 语义 spot-check**（按模块抽样，非全表重写）
4. 上述完成后 → 再开 **F4**（3c/7b 已绿，合表 + 7b 终扫）
