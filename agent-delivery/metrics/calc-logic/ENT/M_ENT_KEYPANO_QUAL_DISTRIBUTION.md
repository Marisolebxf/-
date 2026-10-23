# 整链资质分布（M_ENT_KEYPANO_QUAL_DISTRIBUTION）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_QUAL_DISTRIBUTION.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_QUAL_DISTRIBUTION.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_QUAL_DISTRIBUTION_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEYPANO_QUAL_DISTRIBUTION |
| 指标名称 | 整链资质分布 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 重点企业全景 → 资质结构堆叠图 / 区域资质热力表 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_KEYPANO_QUAL_DISTRIBUTION.md` |

## 口径定义

三维里**资质维**最实：`dwd_org_tech_tag` 202,424 行、55 类、名单内 2,981 家有至少一类；**区域维**结构齐但数据退化：`dwd_org_base_info` 189,116 行里 188,776 行（99.8200%）在广东省，31 个省级行政区只点亮 1 个；**名单维**完全不存在：280 张表八个模式扫描只命中一张新闻表。三维里一维实、两维虚，按 §〇 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_QUAL_DISTRIBUTION.md` §二（M_ENT_KEYPANO_QUAL_DISTRIBUTION.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_corp_basic_info`
- `dwd_dim_admin_area`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`
- `dwd_org_tech_tag`
- `dwd_sec_basic_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：资质维与区域维都能落格：dwd_org_tech_tag 202,424 行、32,322 家、55 类，代理名单内 2,981 家有至少一类资质；区域由 dwd_dim_admin_area 换算，实出 1,560 个非空格、72 个全国格。但三处缺口使其不能判「完全转换支持」：①六类里只有 3 类是直取（高企/专精特新/小巨人），sme 用「科技型中小企业」代理、foreign 与 listed 只能从 org_type 字样代理，库内无 tag_dict；②重点名单不存在（280 表零命中），2,981 家是专利阈值代理名单的子集；③区域维退化为单省切片——代理名单 4,561 家全在广东省 4 市，复合区域只能点亮大湾区，长三角与京津冀点亮 0 家。三条都不是公式问题，是依赖数据问题，按定义判部分支持。
- **基期声明**：截面件：名单按专利授权累计量（>=50）一次性截取，上链关系、链位、区域、资质均无年度键，产物与参数中不存在年份窗口，故 used/missing 均为空。不是「缺年按 0 摊入」的情形，也不得用 created_time 反推年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_KEYPANO_QUAL_DISTRIBUTION.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_QUAL_DISTRIBUTION.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_KEYPANO_QUAL_DISTRIBUTION_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

