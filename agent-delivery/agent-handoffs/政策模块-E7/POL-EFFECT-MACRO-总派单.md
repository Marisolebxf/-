# 落地实效 · 宏观结果面代理 · 总派单

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md)  
> 监管：`human:淮政玮` · `claim_type=coordinator_dispatch` · `lock_hours=24`

## 段 A0 · 口径（definition）

```
/goal product-agent + architect-agent（主写 data/architect 会签）
身份：资深产品/架构，口径诚实优先。
强度：ponytail off（定义）。
任务 ID：POL-EFFECT-MACRO-CALIBER-L01
目标：冻结「宏观结果面代理」临时默认；改 calc-logic 双轨叙述；改 05.6.2 §3；客户决策清单 QPOL-02 增补一行。
DoD：见 registry。
Handoff：agent-handoffs/政策模块-E7/POL-EFFECT-MACRO-CALIBER-L01.md
```

## 段 A1 · 数据映射

```
/goal data-agent
身份：资深数据工程师。
强度：ponytail full。
任务 ID：POL-EFFECT-MACRO-DATA-L01
目标：指标白名单（≤12 个 index_code）+ 区划对齐键 + 读路径（只读 gkx→算法内存/Demo ADS 汇聚，不写供应方）。
必读：加工报告宏观/行业分析节；stores 与 etl 索引可补一节。
DoD：见 registry。
Handoff：…/POL-EFFECT-MACRO-DATA-L01.md
```

## 段 B · 算法

```
/goal algorithm-agent
身份：资深算法工程师；算法只在 Python。
强度：ponytail full。禁止用 YAGNI 跳过可观测与双仓同文。
任务 ID：POL-EFFECT-MACRO-ALGO-L01
仓库：demo-algo-ent-analysis + lumen-algo-py/vendor/entan-py
目标：shenzhen_board / effect 城市卡读宏观代理；ext.caliber=macro_outcome_proxy；正本三维可读时仍可补 gapfill；自检可跑。
DoD：见 registry。
```

## 段 B2 · 算法中台

```
/goal frontend-agent
身份：资深前端；算法中台 demo-ui-system-test。
强度：ponytail full。
任务 ID：POL-EFFECT-MACRO-MID-L01
仓库：demo-ui-system-test
目标：政策算法相关页展示新口径、试算入口或结果说明；禁止写死分数；推送等人确认。
复刻：N/A（中台页，非 demo→lumen 复刻五维）。
```

## 段 C · Java

```
/goal api-agent
强度：ponytail full。
任务 ID：POL-EFFECT-MACRO-JAVA-L01
仓库：lumen-svc-platform
目标：透传 cards.effect.ext（caliber/白名单版本）；不改算法；契约/OpenAPI 补字段说明。
```

## 段 D · lumen 专题 FE

```
/goal frontend-agent
强度：ponytail full。
复刻：布局+交互+样式+评审+Mock开关（对照已评审深圳页）。
任务 ID：POL-EFFECT-MACRO-FE-TOPIC-L01
仓库：lumen-ui-topic
页：/policy/recommendation
目标：结果板实效卡接新 ext；⚠️ 待确认；空不编 0；type-check 绿；推送等人确认。
```

## 段 E

- E0 `POL-EFFECT-MACRO-E0-DEVOPS-L01`：点名相关 pipeline 绿 / rollout  
- E1 `POL-EFFECT-MACRO-E1-QA-L01`：总控 §3 金路径；期望未发生必红  

---

## 进度板（coordinator 滚动）

| 叶 | 状态 | 备注 |
|----|------|------|
| CALIBER-L01 | ready_to_sign / 已交付口径 | QPOL-02 双轨 |
| DATA-L01 | ready_to_sign / 白名单冻 | macro-eff-v1 |
| ALGO-L01 | **integration** | 双仓推；深圳样例 ~78.58；联调通过 |
| MID-L01 | **integration** | 已推 `41d757a` + algo `707edd0` |
| JAVA-L01 | **integration** | `925df28` 已推 |
| FE-TOPIC-L01 | **pending_test** | 已推 `112afa6`；人确认推送 2026-11-09 |
| E0 | **done** | 五仓 Pipeline 绿；entan-py 可达 gkx 且 computable |
| E1 | **claimed→派单** | 金路径冒烟；勿硬断言 9 指标/精确分 |
