# 深圳政策现状分析 · 总派单

真源：[`LUMEN-POLICY-SZ3D-长任务总控.md`](./LUMEN-POLICY-SZ3D-长任务总控.md) 与 FUNC-DESIGN §3.6 v0.5。  
授权句未落款前，只建单、不认领。coding `/goal` 必须带下面的强度行。

## B · `LUMEN-POLICY-SZ3D-B-JOB-L01`

```text
/goal LUMEN-POLICY-SZ3D-B-JOB-L01
角色：algorithm-agent
仓：lumen-algo-py · 分支 origin/dev
强度：ponytail full
图：不必（不改存储拓扑；结果板仍读既有政策 DWD）
必读：政策模块-E7/LUMEN-POLICY-SZ3D-长任务总控.md §0
      FUNC-DESIGN-E7-政策分析.md §3.6 v0.5
      metrics/calc-logic/POLICY/M_POLICY_SUPPORT_STRENGTH.md
范围：policy_shenzhen / policy_sz_3d 的 jobs/execute 结果板改为分卡。
  支持力度：城市截面，因子仅政策条数与政策层级；档位 value=null 且 reason=无金额列；
  附深圳分数、名次、条数、层级均值；diagnostics 保留与条数的秩相关；
  禁止用 dwd_bid_* 填金额；禁止按 industry_vid 重算该分。
  产业适配性：沿用 M_POLICY_INDUSTRY_FIT，范围=请求锚点；无命中则空，不补数。
  落地实效：computable=false，不输出执行率/覆盖/满意度。
  不输出三维综合分。
DoD：见 registry。handoff 含 ponytail: full 与结果 JSON 样例。
```

## C · `LUMEN-POLICY-SZ3D-C-FACADE-L01`

```text
/goal LUMEN-POLICY-SZ3D-C-FACADE-L01
角色：api-agent
仓：lumen-svc-platform · 分支 origin/dev
强度：ponytail full
依赖：B 叶 integration + handoff 字段表
范围：gkxlumen-topic-policy / topic-async 对 policy_shenzhen 结果原样透传。
  任务快照保存三张卡可算状态与冻结因子，不再把 selected_indicators 当入模清单。
  indicators?kind=all 仍只透传分布，不组装二级目录。
  Java 不补综合分、不把 null 档位写成 0。
```

## D · `LUMEN-POLICY-SZ3D-D-FE-L01`

```text
/goal LUMEN-POLICY-SZ3D-D-FE-L01
角色：frontend-agent
仓：lumen-ui-topic · 分支 origin/dev
强度：ponytail full
复刻：本叶不是 demo 勾选模型复刻。视觉仍用现页壳与 Design.md token；
      交互以 FUNC-DESIGN §3.6 v0.5 / Wireframe §6 v1.4.6 为准，废止 demo POLICY_SZ_CORE_INDICATORS。
范围清单：
  1. 配置区三张固定卡，删除二级 Checkbox 与一级权重步进器、一键均分。
  2. 支持力度只读两条因子 + 档位不可算；ⓘ = M_POLICY_SUPPORT_STRENGTH；QPOL-02 PendingBadge。
  3. 开始分析只看锚点。删除「目录为空则 indicatorOk=true」的绿条。
  4. 结果只渲染 Java result：深圳截面、适配性有字段才画、实效空卡、无综合分。
  5. USE_MOCK=false 不引用 demo 二级池。
DoD 含 V1–V7 中本叶改到的配置区与结果区；未改的时序/区域页不得回退。
```

## E0 / E1

E0：点名发布 lumen-algo-py、lumen-svc-platform（topic-policy + async）、lumen-ui-topic。deploy 绿才算 E0 完成。  
E1：总控 §2 五条金路径。期望未发生必红。QA 不改代码。失败先按规约分类再由 coordinator 派修。
