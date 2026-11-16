# ZMATE-RPT · E 波次 · §6.5 跑测记录简报

- 任务：`ZMATE-RPT-QA-L01`
- 日期：2026-11-16
- 执行：`agent:qa-agent` · 监管人 `human:淮政玮`
- 实现基线：`demo-ui-topic` @ `3c088cf`
- 用例：`…/sdd/合规演示用例-ZMATE-RPT.md`（规程入口：`03-专题系统集成/合规演示用例/ZMATE-RPT-合规演示用例.md`）

## §6.5 适用范围说明

本模块为 **Demo 纯前端**（无 Java REST / 无线上库读路径）。规程 §6.5.3「纯后端 token 探测 + 只读库」对本叶 **N/A**，不建 `{模块}-DEMO-ACCEPT-LOOP`，不开 DATA/QUERY/ALGO 子任务。  
本简报按派单约束：以 **手工浏览器走查 + 解锁自检脚本 + build** 作为可核对验收记录。

## 运行 2026-11-16

- 用例：`agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/sdd/合规演示用例-ZMATE-RPT.md`
- 库：N/A（localStorage `zmate-strategy-workspace-v2`）
- 样本满足：**是**（覆盖表 13 条 USM + 人闸/Judge 专项均可演；黄项见下，不挡 Demo 收口）
- 停止：通过（后端 LOOP N/A）

### 核对摘要

| USM | 结果 | 证据 |
|---|---|---|
| 01 创作壳 | 绿 | preview 打开 `/zmate-strategy-demo`；创建任务 → Hub |
| 02 安装≠使用 | 绿（局限） | 创作壳双区可见；skillsUsed 写入；无调用时间线 |
| 03 人闸禁 autoRun | 绿 | 澄清站「等待需求确认」；Hub 无一键跑完；后站锁定 |
| 04 研判卡 slice_id | 绿 | 代码+澄清末步候选卡；确认后绑定 |
| 05 Hub 阶段序 | 绿 | Hub 锁定态快照；`qa-gate-check.mjs` 解锁合同 |
| 06 辩论卷宗 | 绿 | 代码走查；人控轮次/结束后只读 |
| 07 术语分离 | 绿 | 辩论/切片 banner + ReviewMounts 术语卡 |
| 08 四态诚实 | 绿 | DEMO_SLICE 四态；无假 live |
| 09 装配溯源 | 绿 | Writer generating 空正文；citationLabels |
| 10 Judge FAIL | 绿 | Default-FAIL；`qa-gate-check` findings→FAIL |
| 11 项目轨恢复 | 黄 | 新建 runId 恢复绿；fixture `task-demo-*` fallback 黄 |
| 12 评审模式 | 绿 | ReviewMounts 自闸；开见挂载 |
| 13 Demo 边界 | 绿 | 壳副标题 + FE/QA 文档声明 |

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `project-rail.task-demo-*.stage` | ENV/产品 | fixture 任务 id 不在 localStorage | 点入恢复到该任务阶段 | V1 真链或 Demo 启动种子对齐；不挡本轮 | 不建 LOOP 子任务（后端 N/A） |
| `skill-timeline.silent-invoke` | 产品示意 | 无 Skill 调用时间线 UI | USM-02 可目视「取消后不调用」 | 后续若加时间线再核 | — |

### 工程证据

| 项 | 结果 |
|---|---|
| `pnpm build` | 绿 · ~36s · exit 0 |
| `node …/sdd/简报/qa-gate-check.mjs` | OK |
| `pnpm exec vite preview --host 127.0.0.1 --port 4173` | 创作壳 / Hub / 澄清人闸目视通过 |

## 结论

- 合规演示用例覆盖 **ZMATE-USM-01…13（13 条）** + 人闸/Judge FAIL 专项；**无红项阻断**；黄项 2 条已记。  
- §6.5 后端 LOOP 本阶段 N/A；Demo 走查样本满足，可签收本 QA 叶。
