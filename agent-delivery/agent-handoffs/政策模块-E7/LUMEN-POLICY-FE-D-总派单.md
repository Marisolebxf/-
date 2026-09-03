# D 段总派单 · lumen-ui-topic 政策复刻

> **管线**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> **细叶**：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §2  
> **Demo 对照**：`demo-ui-topic` `src/app/pages/policy*`  
> **复刻**：[`fe-replica-visual-dod.md`](../../templates/fe-replica-visual-dod.md)

## `/goal` 头（SHELL）

```
/goal LUMEN-POLICY-D-SHELL-L01
角色：frontend-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic · origin/dev
强度：ponytail full
复刻：布局+交互+样式+评审+Mock开关。必读 templates/fe-replica-visual-dod.md。
范围：侧栏政策菜单 + src/api/policy 薄封装 + 对比篮产业 Tab「政策分析」分组。占位与只改 Hero 不算完成。
禁止：贴 JSX；页内 MOCK；自造 ⓘ；lumen 调 demo-* 服务（D12）；USE_MOCK=false 时 fixture 填数。
数仓：不换库。Java 读的就是 demo_gkxlumenx_*（lumen 现网数仓 = demo 源）。
对照：demo-ui-topic 政策菜单 + 本仓企业/产业兄弟页。handoff 须 V1–V7（本叶若无检索页则 N/A 并写明）。
```

故事叶禁止 ENTRY/WORKSPACE 当完成。查询叶必过 V1–V7；工作区叶必过 W1–W3。只调 Java。
