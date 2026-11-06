# TS-L2-M10-LAYER-DATA · handoff

- 任务：`TS-L2-M10-LAYER-DATA`（definition · 图层与数据源后台数据架构设计）
- 日期：2026-11-06 · 监管：`human:刘剑锋` · 认领：`agent:data-agent`
- 状态：数据分册已落盘，**待四角色会签**，不自签 done

## 范围与实现

数据分册（真源）：[`sdd/l2/TS-L2-M10-LAYER-DATA.md`](./sdd/l2/TS-L2-M10-LAYER-DATA.md)

- 四表列级定义（非可执行 SQL）：`cfg_tech_layer`（9 行枚举）/ `cfg_tech_layer_group`（3 行）/ `cfg_tech_datasource`（3 行）/ `cfg_factor_display`（11 行），全落业务库 gkxlumen-display（D15），不进 ODS/DWD/ADS
- 分工裁定：**DDL 归 Java 实现单**（lumen-svc-platform SQL 变更）；**种子行归 data-agent 灌数单**（Python 一次性 26 行）；运行时 CRUD 归 Java（ARCH §3 裁定的落点）
- **事实修正 ARCH**（§0）：demo 冻结种子真值 = 3 数据源 / 3 图层组 / 9 图层枚举 / 11 要素（共 26 行），ARCH 原稿误记「8 数据源 / 9 图层组」；已同步修正 ARCH §3/§4.2 两处数字（未会签稿纠错）。D18 三要素不变
- 不设列裁定：`last_sync`/`test_status`（无同步动作、探测不持久化）、`active`（M1 图例运行态）、`is_mock`/`metric_id`/D16 五件套（真配置非缺项表）

## 偏离说明

- 对 ARCH 为事实性纠错（种子行数），非裁定偏离；已在分册 §0 显式记录前后值与依据（demo 源仓 = lumen 复刻仓逐字核对）
- 补齐 ARCH 未给数的 `cfg_tech_layer` 种子（9 行）与 `cfg_factor_display` 颜色种子来源（`entityColorByKey` 冻结）

## 产物清单

- 新增：`agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-M10-LAYER-DATA.md`
- 修改：`sdd/l2/TS-L2-M10-LAYER-ARCH.md` §3 第 2 点、§2 脚注、§4.2 图（种子数与「四表」措辞修正）
- 本 handoff

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| D7 写数归 Python | ✅ 仅种子灌数归 Python；运行时配置 CRUD 归 Java（ARCH §3 会签点 ①） |
| D15 落库 gkxlumen-display | ✅ 四表业务库 |
| D16 缺项表规矩 | ✅ 不适用：无 gapfill_ 前缀、无五件套列，稿内已说明 |
| D18 表名/灌数方/读接口齐备 | ✅ 逐表 + §1 分工表 |
| 不写 ETL/调度 | ✅ §6 不做清单 |
| 种子为真配置非 mock | ✅ 不挂 is_mock，一致处显式标注 |

## cost

- actual_tokens: ~20k
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$0.5
- cost_warn: green
