# METRIC-CALC-REFRESH-1027-L01 · 20261027 批调研真源刷新：calc-logic 规整 + 1027 正文替换 1024 + repro 同步 + 路径清洗

> 任务类型：定义/归档整理（spike 型文档治理）。只读 gkx 源、只改 `agent-delivery/metrics/` 下文档与复现产物。
> 监管人：`human:唐绍祖` · 执行：`agent`（glm-5.3，Cursor）· 建单日：2026-10-28 · 状态：成果已交付（commit `bd7d4a89`），待签收
> 上游：`METRIC-SRS-GAP-L01`（分级结果与 20261027 批正本，产物 `agent-delivery/agent-handoffs/指标算法库上线/METRIC-SRS-GAP-L01/产物/20261027三系统兼容升级/`）

## 1. 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:唐绍祖` |
| supervised_by | `human:唐绍祖` |
| claim_type | pull |
| 仓 | `gkx-orchestration` |
| 说明 | 用户 2026-10-28 指令四步：① 规整 calc-logic 抬头与「详细计算过程」标题；② 1027 批正文替换 1024 并入版；③ 复检 code/ 迁移覆盖 repro；④ 任务工作区（不入 git 的本地目录）路径清洗复检 |

## 2. Ponytail（coding 任务必填；调研任务写 N/A）

| 字段 | 值 |
|------|-----|
| ponytail | N/A |

## 3. 交付物（全部在 `agent-delivery/metrics/`，commit `bd7d4a89` 已 push dev）

| 落点 | 内容 |
|------|------|
| `metrics/calc-logic/{11 域}/` | 565 件标题 `# 详细计算过程（…1024 并入版）` → `# 最新指标调研报告`，批次信息降入标题下内容框；〇、章前抬头按「归属与维护 / 指标画像 / 复现与产物 / 版本与分级」四组分段分点 |
| 同上 | 573 件正文整体替换为 20261027 批正本（三系统兼容升级版）：565 件重建 + 8 件 `_ZT`/`_ZS` 拆分新件按域新增（CHAIN×4、ENT×2、TALENT×2）+ COMMON 1 件补齐 |
| 同上 | 18 件 1027 批无源件（BOTTLENECK 族、SZ_SCALE_DIST 等）维持骨架版，补维护者/适用系统抬头与「不在 1027 批源内」版本说明 |
| `metrics/repro/` | 573 份 py 脚本全量覆盖（SHA256 与 1027 批 `code/` 逐件对齐 573/573）；`_gkxdb.py` 为历史公共连接件保留 |
| `metrics/repro/out/` | 573 份 `_out.json` 产物全量覆盖（SHA256 对齐 573/573），含 8 件拆分新件产物 |
| 全 metrics 域 | 任务工作区路径引用清零（566 件 md + 11 py + 11 out.json 改写为仓内新路径或「不入仓附件」标注，GAP 5 件旧式指针一并清洗） |

## 4. 核心结论（供决策）

1. calc-logic 旧标题 `# 详细计算过程（…）` 全库清零（565→0），573 件统一为 `# 最新指标调研报告` 新体例。
2. 1027 批正本覆盖度 573/583：8 件拆分新件入域新增；**18 件在 1021/1027 两批调研源中均无正本**（M_CHAIN_BOTTLENECK_{CAPITAL,TALENT,DEMAND,TECH,POLICY}、M_CHAIN_{MARKET_CONCENTRATION,STAGE_HEALTH_SCORE,HIGH_END_INDEX,ADDED_VALUE_RATE,PROFIT_MARGIN,TECH_BARRIER_INDEX,GROWTH_RATE}、M_ENT_{RD_INVEST_AVG,TECH_SCORE,SEARCH_RESULT_COUNT,SZ_SCALE_DIST,CLUSTER_INDEX,BUSINESS_SCORE}），维持骨架版待后续调研批次补源。
3. repro 与 1027 批 code 的 SHA256 一致性 573/573（py）与 573/573（out.json），零漂移。
4. `agent-delivery/metrics/` 全域（calc-logic + repro + out）任务工作区路径字符串残留 0。

## 5. 下游承接

- 三仓弹窗（`UI-METRIC-POPUP-3SYS-L01`）已消费 1027 批 md，本次真源刷新不改变其数据基准（正文同源）。
- 后续指标开发以 calc-logic「最新指标调研报告」节为唯一口径真源；18 件无源件如需升级，须先立调研单补正本。

## 6. 迁移说明（2026-10-28）

- 原落盘位置：编排主仓之外的任务工作区 20261027 批调研目录（不同步远程 GitLab）；本单为该批成果向 `metrics/` 真源目录的**第二次落点**（第一次为 METRIC-SRS-GAP-L01 产物区归档）。
- 迁移范围：573 md + 573 py + 573 out.json + 抬头治理脚本（过程件，留工作区）。
- 清洗校验：md rg 扫描 + 抬头/骨架逐类改写，metrics 全域任务工作区路径引用 0 处。
- 维护真源：本单交付后，`agent-delivery/metrics/calc-logic/` 与 `metrics/repro/` 即为该 573 件指标的唯一维护真源；上游产物区（METRIC-SRS-GAP-L01/产物/20261027三系统兼容升级/）转为只读存档。
