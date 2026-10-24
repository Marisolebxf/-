# 覆盖区域数（M_ENT_KEYPANO_REGIONAL_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_REGIONAL_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEYPANO_REGIONAL_COUNT |
| 指标名称 | 覆盖区域数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 重点企业全景 → 链路卡片上的「覆盖区域 N 个」与地图点亮 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_KEYPANO_REGIONAL_COUNT.md` |

## 口径定义

「`COUNT(DISTINCT region_key)`」这个公式没有任何执行障碍：省码、市码从 `dwd_dim_admin_area` 换算，市县都齐；复合区域按规划纲要自建。真正的限制在**名单**：4,561 家全部落在广东省 4 市，区域键的母集只有 29 个，所以 `cover_count` 只能在 21—28 之间摆动，全国 31 个省、339 个市、2,836 个区县里绝大多数永远点不亮。按 §〇 判**部分支持**——不是算不出，是算出来的覆盖面没有代表性。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_REGIONAL_COUNT.md` §二（M_ENT_KEYPANO_REGIONAL_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：公式可完整执行，实出 12 条链的 cover_count（21—28 个键），并集 30 个键 = 1 省 + 4 市 + 23 区县 + 1 个复合区域（大湾区）。但有两条依赖缺口：①重点名单不存在，4,561 家是专利授权≥50 的代理名单，且这 4,561 家全部落在广东省 4 市（深圳 2,590、广州 1,020、东莞 775、惠州 176），区域维因此退化为单省切片——31 个省级行政区只点亮 1 个（3.2258%）、339 个市只点亮 4 个（1.1799%）、2,836 个区县只点亮 23 个（0.8110%）、3 个复合区域只点亮 1 个；②复合区域维表不存在——gkx 里 %scope% 表 0 张，scope 成员是按国务院三份规划纲要的行政范围自建的，不是 region_scope_member。对照证据表明这不是表结构的问题：同一张 dwd_org_industry_tags 全库聚合时每条链覆盖 31—32 个省、250—339 个市。所以判部分支持，不判完全不支持，也不抬成完全转换支持。
- **基期声明**：截面件：名单按专利授权累计量（>=50）一次性截取，上链关系、链位、区域、资质均无年度键，产物与参数中不存在年份窗口，故 used/missing 均为空。不是「缺年按 0 摊入」的情形，也不得用 created_time 反推年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_REGIONAL_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_REGIONAL_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

