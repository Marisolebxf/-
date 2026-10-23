# 高精度成本模型构建（M_TALENT_DS_16_TALENT_RECRUIT_013）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_013.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_013.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_013_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DS_16_TALENT_RECRUIT_013 |
| 指标名称 | 高精度成本模型构建 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 国际人才引进页「引进成本测算」（建议改为「企业研发投入参考」，见 §5.4） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DS_16_TALENT_RECRUIT_013.md` |

## 口径定义

成本模型的因变量是「引进一个人要花多少钱」。37 个 `cost/income` 列全部是企业分部财务（`core_biz_cost` 等）或期刊排版费（`layout_cost`），0 列薪酬/安家费/猎头费；798 万条招聘记录只有岗位描述、无薪资；学者主档只有 `paper_nums/citation_nums/h_index/reference_nums`。因变量不存在，模型无从谈起，故判**完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_013.md` §二（M_TALENT_DS_16_TALENT_RECRUIT_013.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_journal`
- `dwd_main_business_composition_`
- `dwd_main_business_composition_area`
- `dwd_main_business_composition_industry`
- `dwd_main_business_composition_prod`
- `dwd_org_recruit_info`
- `dwd_scholar`
- `dwd_scholar_talent_flag`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：成本模型的因变量不存在：37 个 cost/income 列全部是企业分部财务或期刊排版费，0 列薪酬/安家费/猎头费；798 万条招聘记录无薪资字段；学者主档无薪酬职级。只能做「企业人均研发费用」这类宏观代理，无法落到个人引进成本，故完全不支持。
- **基期声明**：无基期：成本因变量不存在，财务表虽有 period（198912—202603），但那是企业报表期，不是人才引进成本的时间序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_013.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_013.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_013_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

