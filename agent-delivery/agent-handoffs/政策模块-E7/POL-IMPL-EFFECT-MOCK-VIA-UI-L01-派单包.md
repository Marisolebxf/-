# POL-IMPL-EFFECT-MOCK-VIA-UI-L01 · 派单包

> coordinator 2026-11-09 · 监管人授权 mock/造数 · 过程必须挂进算法库页两个按钮

## /goal（可直接开会话）

```
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师，精通数仓分层与 D16 gapfill 缺项补齐；本单明确授权 mock/造数以满足演示。
强度：ponytail full。禁止用 YAGNI 跳过 D16 边界（缺项只进 gapfill_）与双入口挂钩。
任务 ID：POL-IMPL-EFFECT-MOCK-VIA-UI-L01
claim_type：coordinator_dispatch
supervised_by：human:淮政玮
仓库：${GKX_ROOT}/repos/demo-algo-ent-analysis（主）；若线上跑 lumen-algo-py vendor 副本则同改
目标：落地实效三维缺项可演示；无结构建表、有结构灌数；mock 过程必须包含图上两个过程。

背景：
- 指标 M_POLICY_IMPLEMENTATION_EFFECT 三维输入（启动日/受益对象/反馈分）现读 gkxlumenx_gapfill.gapfill_policy_sz_effect。
- EFFECT-SYNTH 已把写入挂到 synth；前序 DATA 单因「无非空源禁造数」blocked。本单监管人授权造数。
- UI：http://10.50.69.111:30889/#/policy/mock（政策分析算法库）
  ①「Mock 10 条数据」→ synth.run
  ②「真实政策补外围：深圳 40 + 随机 10」→ synth.run_real

Mock 原则（硬）：
1. 没有结构 → CREATE（列对齐 effect_gapfill.CREATE_SQL / EFFECT-GAPFILL）
2. 有结构 → INSERT/UPSERT 灌可演示行
3. 只写 gapfill_；禁止 ODS / 正式 DWD / ADS / 供应方库
4. 缺失不写成 0、不写零日期、不把发布日当实施日

必做：
1. 认领 task-claim id=POL-IMPL-EFFECT-MOCK-VIA-UI-L01 claimed_by=agent:data-agent supervised_by=human:淮政玮
2. 核实现网/Demo 库：表是否存在、行数；「已补」政策是否缺 effect 行
3. 修/补链路：两入口任一点后，当次政策必有 gapfill_policy_sz_effect 行（含 implementation_date / support_object / feedback_score + 元数据列）
4. 对已补无 effect 的存量：通过再跑补外围或同入口可触发补写，使可演示
5. 双仓：demo-algo-ent-analysis 与 lumen-algo-py/vendor/entan-py 同逻辑对齐
6. 证据：两入口调用前后 SQL COUNT；handoff 写 agent-delivery/agent-handoffs/政策模块-E7/POL-IMPL-EFFECT-MOCK-VIA-UI-L01.md
7. 完工：task-update-fields + status→ready_to_sign（tech_task）；cost 四字段
8. **系统详细设计（监管人 2026-11-09 追加）**：对应章节已起稿于
   `agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md` §3 / §3.1
   （落地实效读 gapfill + Mock10/补外围双入口）。data-agent 须核对 as-built 与 §3.1 一致；
   若实现偏离，修订 §3.1 并同步 `data/data-design/storage/POLICY/stores/README.md` 中该表「写入口」句。
   禁止另起与双入口无关的旁路灌数文档当详设。

DoD：见 task-registry POL-IMPL-EFFECT-MOCK-VIA-UI-L01
参考：
- polan/mockgen/effect_gapfill.py、synth.py（_insert_effects / run / run_real）
- TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-SYNTH.md
- metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md
- 05.6.2-深圳政策现状分析.md §3.1
```

## 边界

| 做 | 不做 |
|----|------|
| gapfill 建表/灌数；两入口挂钩自检 | 改展示顶栏写死 92.5（属 FE） |
| 存量已补政策补 effect | 写正式 ODS/DWD/ADS |
| vendor 双落说明 | 改按钮文案条数 |

## 前序

- EFFECT-GAPFILL / EFFECT-SYNTH = done
- TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA = blocked（禁造数）→ **不复开**，本单替代演示 mock 路径
