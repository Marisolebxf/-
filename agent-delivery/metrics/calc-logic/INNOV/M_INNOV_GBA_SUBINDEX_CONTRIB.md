# 湾区子指数贡献度（M_INNOV_GBA_SUBINDEX_CONTRIB）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SUBINDEX_CONTRIB.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SUBINDEX_CONTRIB.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SUBINDEX_CONTRIB_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_SUBINDEX_CONTRIB |
| 指标名称 | 湾区子指数贡献度 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV / 湾区创新监测 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 湾区创新能力四子指数贡献饼图/堆叠图｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_SUBINDEX_CONTRIB.md` |

## 口径定义

11/12 分项可算，深圳占 56.33%、广州 36.28%、东莞 7.09%、惠州 0.30%；但只有 4/11 城、政策覆盖缺、权重自定义，判部分支持。

## 计算逻辑说明

```text
子指数=可用分项 min-max 后等权平均；城贡献=城子指数/四城合计×100%；分项总贡献=norm×权重/Σ(norm×权重)×100%
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SUBINDEX_CONTRIB.md` §二（M_INNOV_GBA_SUBINDEX_CONTRIB.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：12 分项中 11 项可算，4 城四子指数与贡献份额全部落盘；但政策覆盖因 theme 全空不可算，环境维只剩 2 项；面板只有 4/11 城（其余 7 城实体基数近零），不是完整湾区；联合专利只覆盖 20,000 pn（0.68%）、研发投入只覆盖上市主体（856 家）、载体产出与资源维重复计位；权重为自定义。故判部分支持，贡献份额只能作内部结构参考。
- **基期声明**：分项窗口不同：专利 2021—2024；论文 2021—2023（2024 年论文量 32,379 是 2023 年的 4.87 倍，属批次断层，排除）；研发投入 2019—2024（上市主体年报）；项目 2021—2023；转移 2021—2026；政策为存量（无年度窗口）。used 列出并集，未把任何缺年补 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_SUBINDEX_CONTRIB.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SUBINDEX_CONTRIB.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_SUBINDEX_CONTRIB_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

