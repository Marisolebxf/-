---
name: gkx-gdf-cdc-workpack
description: >-
  Reads a GDF workpack under agent-delivery/data/GDF/派单包 and generates two
  DRAFT CDC Excel jobs (Wave A 贴源, Wave B 明细 Mapping). Use when the user
  asks to 生成 CDC 表, 预填作业, 贴源_模板, 明细数据_模板, GDF-*-WORKPACK, or to turn a
  派单包 into GDF Excel. Not for analyzing existing 执行结果 (use officecli).
---

# GDF 派单包 → 两张 CDC 预填表

脚本在 `scripts/gdf-cdc/`：`parse_workpack.py`、`fill.py`。给人看的协作说明：`agent-delivery/data/GDF/GDF协作指南.md`。

企业 / 人才 / 专题共用本流程。工作包目录约定见 [reference.md](reference.md)。v1 明细 CDC 壳的填写规则见 [v1-dwd-cdc-template-rules.md](v1-dwd-cdc-template-rules.md)（生成前必读：17 张业务页都是「数据结果」布局）。校准 V1 执行结果见下方「校准模式」。

## 何时开工 / 何时停止

**开工**：用户指定工作包路径，或说「按派单包生成 CDC / 预填两张表」。

**停止并只报告缺口**（不要造表）：

- README / `00` 写明 **已作废**（例如 v1）
- 缺 `02-WaveA-贴源表清单.yaml`
- 缺 Mapping 施工真源（`09-*Mapping明细*` 或 README 标明的正式 `09`；禁止用短版导读当字段矩阵）
- 工作包状态为「暂缓投递」且用户未明确说「仍生成草稿」

## 标准顺序

复制清单并勾选：

```
- [ ] 1. 锁定工作包（现行未作废目录）
- [ ] 2. officecli load_skill excel
- [ ] 3. python scripts/gdf-cdc/parse_workpack.py → inventory.json
- [ ] 4. python scripts/gdf-cdc/fill.py both（克隆模板壳）
- [ ] 5. officecli view + 对照 inventory 抽检 P0 规则
- [ ] 6. 写 GENERATION-REPORT.md；向用户说明这是 DRAFT
```

### 1. 锁定工作包

默认根：`agent-delivery/data/GDF/派单包/{域}/GDF-*-WORKPACK-vN/`。

用户给了路径就用该路径。否则同一域取 **版本号最大且未作废** 的包。禁止用 v1 的 `02`/`09` 当施工真源。

必读（只读这些，不要读招标 PDF）：

| 文件 | 用途 |
|------|------|
| `README.md` / `00-派单说明书.md` | 作废 / 暂缓 / Mapping 真源文件名 |
| `02-WaveA-贴源表清单.yaml` | Wave A 表清单 |
| `04-技术字段与过滤规则.md` | 默认 `is_deleted = 0` |
| Mapping 明细 `09`（README 指定） | Wave B 字段 |
| `10-DWD-MySQL-DDL/`（若有） | 目标列名校验，不编造列 |

v1 `执行结果/*.xlsx` **只当模板壳**（列布局 / 模板名），不当表清单。

### 2. 解析为 inventory

在 `gkx-orchestration` 根目录执行（把工作包换成绝对路径）：

```bash
python scripts/gdf-cdc/parse_workpack.py --workpack "<WORKPACK_DIR>" -o inventory.json
```

读输出：`wave_a` 全量贴源；`wave_b` 仅 Mapping 要洗的目标表；`mirror_only` 只贴源不洗；`warnings` 必须写进报告。

### 3. 生成两张 CDC

模板优先级：`--template-a` / `--template-b` → 工作包 `templates/` → 同域旧包 `执行结果/1、贴源_模板.xlsx` 与 `2、明细数据_模板.xlsx`。没有模板则停止，向用户要一份 GDF 空白 CDC 模板（`SRC_DB_CDC_TEMPLATE` / `DWD_CDC_TEMPLATE`）。不要从空白 workbook 手搭 24 列布局。

```bash
python scripts/gdf-cdc/fill.py both --workpack "<WORKPACK_DIR>" --inventory inventory.json --out "<WORKPACK_DIR>/预填作业"
```

也可拆开：`wave-a` / `wave-b`，并用 `--template-a` / `--template-b` 指定 CDC 壳。

产出文件名固定：

- `1、贴源_预填-DRAFT.xlsx`
- `2、明细数据_预填-DRAFT.xlsx`
- `GENERATION-REPORT.md`

禁止写入 `执行结果/`。禁止覆盖 GDF 已回传的执行结果。

### 4. 抽检（不过不要宣称完成）

```bash
officecli view "<...>/1、贴源_预填-DRAFT.xlsx" outline
officecli view "<...>/2、明细数据_预填-DRAFT.xlsx" outline
```

对照 inventory 人工抽这几条（v1 回件踩过的坑，详见 [reference.md](reference.md)#hard-rules）：

- 索引表数 = `02` 表数
- P0 主表过滤为 `is_deleted = 0`
- 没有 `yearTime`；年报源字段仍是 `year`
- `registered_capital` 表达式含 `/ 10000`
- `mapping: mirror_only` / 明细「暂不映射」未进 Wave B 索引
- 明细表含中文页 **企业风险汇总**，且为「数据结果」+「预聚合」（不是英文空壳）
- 作业频率可空（DRAFT 允许）；报告里标明「调度未填」

失败 → 改 inventory/脚本后重生成，不要手工改几十格凑数。

### 5. 向用户交付

只说：**预填草稿，待 GDF 导入核对**。列出 `warnings` 与缺表（`--missing`）。下一步是 GDF 回签 `05`，不是本技能再出「执行结果」。

## 硬规则（违反则重做）

1. 表名 / 字段只来自 `02` + Mapping 明细 + `10/` DDL。禁止从 live 库、常识、v1 回件倒灌（**v1 `--calibrate` 除外**：以执行结果为对照，规则写进技能后再填）。
2. Wave A 同构镜像：不改列名。类型清洗（零日期）可进转换页；v2 **禁止** `year → yearTime`（v1 校准必须复现年报转换页）。
3. 默认过滤 `is_deleted = 0`。某表无该列 → 报告例外，不要默默留空。
4. 明细写「万元 / ÷10000」则表达式必须除；写「单位待三方确认」则不除并进 `warnings`。
5. 缺表进「没找到的表」，禁止当已下线删掉。
6. 禁止假值填 ❌ / 不映射字段。
7. 禁止 `git commit` / 对外投递 zip，除非用户明确要求。

## `--missing`

用户或供应方核验名单：`--missing dwd_forg_college_org_info,...`  
这些表从 Wave A 索引移到「没找到的表」，Wave B 若依赖则 `warnings` 升级为阻塞。

## 校准模式（复现 v1 执行结果，禁止当 v2 真源）

目标：只克隆壳，清空已填格子，按本技能规则 + v1 的 `02`/`09` v3 重填，直到与 `执行结果/` **逐格相同**。

**禁止**：把 `执行结果/*.xlsx` 的已填内容拷进产出；禁止写入 `执行结果/`。

```
- [ ] 1. python scripts/gdf-cdc/extract_v1_recipes.py
- [ ] 2. python scripts/gdf-cdc/parse_workpack.py --workpack "<v1>" -o inventory.json
- [ ] 3. python scripts/gdf-cdc/fill.py both --calibrate --workpack "<v1>" --inventory inventory.json --out "<v1>/校准生成"
- [ ] 4. python scripts/gdf-cdc/diff_cdc.py --gold "<v1>/执行结果" --gen "<v1>/校准生成" -o "<v1>/校准生成/DIFF.md"
- [ ] 5. 有 diff → 改本技能 / fill 规则 / 目录 → 从步骤 3 重填
```

`--calibrate` 允许已作废的 v1 包。产出文件名与金标准相同，目录必须是 `校准生成/`。

Wave A：按 `02` yaml 顺序写索引，再套 v1 校准规则（template-rules §7）。

Wave B：17 页都是「数据结果」；左右栏按同一行号拉链填写。`09` v3 不够的字段，用校准目录里从差异固化的事件。

v2 生产不得使用 `yearTime`、不得把风险汇总写成宽表、不得用本校准目录。

## 人才 / 专题

同一套文件名（`02` / `04` / 正式 `09` / 可选 `10`）。域目录不同（`派单包/人才`、`派单包/专题`）。没有 CDC 模板壳时先向 GDF 要空白模板，不要复用企业 DWD 表名。
