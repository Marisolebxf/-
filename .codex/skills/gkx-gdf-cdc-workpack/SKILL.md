---
name: gkx-gdf-cdc-workpack
description: >-
  Reads a GDF workpack under agent-delivery/data/GDF/派单包 and generates two
  DRAFT CDC Excel jobs (Wave A 贴源, Wave B 明细 Mapping). Use when the user
  asks to 生成 CDC 表, 预填作业, 贴源_模板, 明细数据_模板, GDF-*-WORKPACK, or to turn a
  派单包 into GDF Excel. Not for analyzing existing 执行结果 (use officecli).
---

# GDF 派单包 → 两张 CDC 预填表

真源与 Cursor 同文：`.cursor/skills/gkx-gdf-cdc-workpack/`。改技能先改那边。给人看的协作说明：`agent-delivery/data/GDF/GDF协作指南.md`。

脚本在 `scripts/gdf-cdc/`：`parse_workpack.py`、`fill.py`。

企业 / 人才 / 专题共用本流程。约定见 [reference.md](reference.md)。

## 何时开工 / 何时停止

**开工**：用户指定工作包路径，或说「按派单包生成 CDC / 预填两张表」。

**停止并只报告缺口**（不要造表）：

- README / `00` 写明 **已作废**（例如 v1）
- 缺 `02-WaveA-贴源表清单.yaml`
- 缺 Mapping 施工真源（`09-*Mapping明细*` 或 README 标明的正式 `09`；禁止用短版导读当字段矩阵）
- 工作包状态为「暂缓投递」且用户未明确说「仍生成草稿」

## 标准顺序

```
- [ ] 1. 锁定工作包（现行未作废目录）
- [ ] 2. officecli load_skill excel
- [ ] 3. python scripts/gdf-cdc/parse_workpack.py → inventory.json
- [ ] 4. python scripts/gdf-cdc/fill.py both（克隆模板壳）
- [ ] 5. officecli view + 对照 inventory 抽检 P0 规则
- [ ] 6. 写 GENERATION-REPORT.md；向用户说明这是 DRAFT
```

工作包根：`agent-delivery/data/GDF/派单包/{域}/GDF-*-WORKPACK-vN/`。

```bash
python scripts/gdf-cdc/parse_workpack.py --workpack "<WORKPACK_DIR>" -o inventory.json
python scripts/gdf-cdc/fill.py both --workpack "<WORKPACK_DIR>" --inventory inventory.json --out "<WORKPACK_DIR>/预填作业"
```

产出：`1、贴源_预填-DRAFT.xlsx`、`2、明细数据_预填-DRAFT.xlsx`、`GENERATION-REPORT.md`。禁止写入 `执行结果/`。

硬规则与模板列见 [reference.md](reference.md)。完整步骤见 `.cursor/skills/gkx-gdf-cdc-workpack/SKILL.md`。
