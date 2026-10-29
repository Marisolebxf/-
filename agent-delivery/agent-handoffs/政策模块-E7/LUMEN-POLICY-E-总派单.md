# E 段总派单 · 政策专题已发布冒烟

> **管线**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md) §4  
> **缺陷包**：[`long-task-e-defect-pack.md`](../../templates/long-task-e-defect-pack.md)

## E0

```
/goal LUMEN-POLICY-E-DEVOPS-L01
角色：devops-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic / lumen-svc-platform / lumen-algo-py helm+CI
强度：ponytail full
点名：lumen-ui-topic · gkxlumen-topic-policy · gkxlumen-topic-async-service · lumen-algo-py
数仓：demo_gkxlumenx_*（lumen 现网 = demo 源；helm 禁止改正式前缀数据面）
禁止：等聊天「已经滚了」；把 innov/entan 搭车当本轮 E0。
```

## E1

```
/goal LUMEN-POLICY-E-QA-SMOKE-L01
角色：qa-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
只认：http://10.50.69.111:30892
金路径：总控 §4 五条。期望未发生必红。QA 不改代码。
CI：e2e:policy-gold（未绿前手跑）。失败先 C1–C6 分类。
```
