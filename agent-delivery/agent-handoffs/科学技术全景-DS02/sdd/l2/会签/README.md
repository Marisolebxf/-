# 会签

四角色会签稿放本目录。命名对齐政策跟踪：`{分册}-SIGNOFF-{ARCH|ALGO|DATA|PRODUCT}.md`。

对象是功能架构 `TS-L2-DS02-ARCH`。2026-11-05 四角色都已同意。签收仍由 `human:淮政玮` 做，本目录不把任务标 done。

| 角色 | 稿 | 结论 |
|---|---|---|
| 架构 | `TS-L2-DS02-ARCH-SIGNOFF-ARCH.md` | 第一轮不同意（调用图缺 Python 跳，选中后关系未写 200 条）。第 2 节改完后第二轮同意 |
| 算法 | `TS-L2-DS02-ARCH-SIGNOFF-ALGO.md` | 同意 |
| 数据 | `TS-L2-DS02-ARCH-SIGNOFF-DATA.md` | 同意 |
| 产品 | `TS-L2-DS02-ARCH-SIGNOFF-PRODUCT.md` | 同意 |

## 二级四单（as-built）

对象是 `TS-L2-DS02-{GRAPH,ENTITY,PATH}-{ARCH,API,METRIC,DATA}` 共 12 份。2026-11-07 四角色会签。审的是记录是否如实、合规、偏离是否已登记且有归属。文字级修正已直接改在被审稿里，各会签稿写明「第一轮 → 已改 → 第二轮」。没有改代码。四角色同意不是签收，签收仍由 `human:淮政玮` 做。

| 角色 | 稿 | GRAPH | ENTITY | PATH |
|---|---|---|---|---|
| 架构 | `TS-L2-DS02-L2SET-SIGNOFF-ARCH.md` | 不同意 → 已改 → 有条件同意 | 不同意 → 已改 → 有条件同意 | 不同意 → 已改 → 有条件同意 |
| 算法 | `TS-L2-DS02-L2SET-SIGNOFF-ALGO.md` | 有条件同意 | 有条件同意 | 同意 as-built，口径转登记 |
| 数据 | `TS-L2-DS02-L2SET-SIGNOFF-DATA.md` | 不同意 → 已改 → 有条件同意 | 不同意 → 已改 → 同意 | 同意 |
| 产品 | `TS-L2-DS02-L2SET-SIGNOFF-PRODUCT.md` | 不同意 → 已改 → 有条件同意 | 有条件同意 | 同意 as-built，口径转登记 |

条件要 coordinator 建单或改单：查询缺口（`IndexNotFound` 当空）返修；`SEL-FIX` 的透传截断从「可选」改为必做；`relationCount` 返修；子学科外部 `_dev` 库归属；抽屉两张卡；待甲方确认角标；时间筛选无年份时的提示。建议登记到客户决策清单的四条口径，列在产品稿末节。
