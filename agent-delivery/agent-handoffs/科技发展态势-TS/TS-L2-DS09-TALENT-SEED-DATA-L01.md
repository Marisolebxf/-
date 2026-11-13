# TS-L2-DS09-TALENT-SEED-DATA-L01 · ts_plan_talent_flow 演示种子日期分布重排(覆盖 range 三窗)

## 任务认领(必填)

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:zcode`(用户授权跨角色代办:原派 data-agent,因催办加速由本会话执行) |
| supervised_by | `human:王梓真` |
| 任务 | `TS-L2-DS09-TALENT-SEED-DATA-L01`(DATA 类,P2,S/2 分) |
| 前置 | `TS-L2-DS09-TALENT-RANGE-L01`(range 过滤已上线,2026-11-13) |

## 背景

range 过滤上线后,`ts_plan_talent_flow` 5 条 record 行 updated_at 全在 2026-03(12m 窗内),3m/6m 窗口诚实空态→时间维度联动无法演示。按 §6.5.4 DATA 类缺口处理:重排演示种子日期分布(数据仍标注 talent_fill_demo,合规性不变)。

## 执行内容

1. **种子脚本存档**:`scripts/ts_plan_seed/seed_dump.json` talentFlowData 4 条 date 更新(id1 清华→华为 2026-11-08/id2 腾讯→中科院 2026-07-15/id3 MIT→字节 2026-11-10/id4 百度→北大 2026-07-18;id5 斯坦福维持 2026-03-10 仅 12m 窗)——灌数脚本 seed_ts_plan.py 从 dump 读 date,无需改代码,新环境重跑即复现;
2. **dev 库执行**:`gkxlumenx_ads.ts_plan_talent_flow` 仅更新上述 4 条 record 行 updated_at(varchar 列,日期串);斯坦福行与其余 11 行(stats 6/institution 5)不动;source=talent_fill_demo 保留。

## 验证(接口与库对账,2026-11-13)

| range | records | stats(预警/学→产/产→学) | 全窗口块 |
|---|---|---|---|
| 3m | **2**(清华→华为 11-08、MIT→字节 11-10) | 0/20/0 | ✓ |
| 6m | **4**(上述+腾讯 07-15、百度 07-18) | 1/20/10 | ✓ |
| 12m | **5**(再+斯坦福 03-10) | 2/29/10 | ✓ |

net_inflow=2387、TOPS 5 行、od_nodes 6 节点三窗一致(全窗口口径 ✓);时间维度切换演示链路完整。

## 用例同步

TS-L2-DS09-合规演示用例.md:182 行期望输出按实查值更新(三窗行数+stats 数值+日期),主路径第 6 步同步,「保持现状」清单补 TOPS 全窗口口径注记。

## 遗留

- 种子脚本提交:seed_dump.json 改动在 gkx-orchestration(编排资产仓),待与其它编排侧改动一并提交(用户确认后);
- 接真实人才流动数据另行走数据源接入流程(演示种子修补不覆盖)。
