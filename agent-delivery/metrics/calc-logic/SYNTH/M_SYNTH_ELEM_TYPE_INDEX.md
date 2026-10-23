# 区域创新要素类型指数（M_SYNTH_ELEM_TYPE_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_TYPE_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_TYPE_INDEX |
| 指标名称 | 区域创新要素类型指数 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新要素分析／要素评价模型构建 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_ELEM_TYPE_INDEX.md` |

## 口径定义

类型指数的算法面没有障碍：12 个进加权叶子先做四城极值归一，再按维内等权平均出 6 个维分，最后按「缺维不进分母」取六维均值，四城结果与面板 `type.index` 逐城差 < 1e-6。卡住的是输入面：创新人才整维不可算，且资金、空间两维都是代理口径。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_TYPE_INDEX.md` §二（M_SYNTH_ELEM_TYPE_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_financing`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：七个要素维里 6 个可算（企业、政策、服务机构、科研机构、资金、空间），创新人才整维不可算：研发人员列 90,926 行中 >0 行为 0，硕博学者按机构名落城后四城仅 111 人、东莞与惠州为 0。指数 = 6 个可用维等权均值，逐城复算与面板一致；但 17 个类型叶子里 3 个无承载、1 个样本不足、1 个退化（服务机构类型数四城恒 6），且资金维是上市口径、空间维只有名称弱代理，故判部分支持。
- **基期声明**：类型指数是 2024 单年截面：企业注册数按 2024 成立年、融资按 2024 完成日、上市研发按 2024 年报期；高企名录、服务机构池、科研机构表、政策存量是当前时点存量（政策不按年截断，见 DATA_FACTS §3.7）。2021—2023 未入集是本族单年截面设计，不是缺数；2025/2026 不完整不进分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_TYPE_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

