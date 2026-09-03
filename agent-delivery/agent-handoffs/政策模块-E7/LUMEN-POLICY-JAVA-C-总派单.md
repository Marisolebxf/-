# C 段总派单 · gkxlumen-topic-policy

> **管线**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> **细叶**：[`LUMEN-POLICY-CD-细叶拆单.md`](./LUMEN-POLICY-CD-细叶拆单.md) §1

## `/goal` 头（BOOT）

```
/goal LUMEN-POLICY-C-BOOT-L01
角色：api-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-svc-platform · origin/dev
强度：ponytail full
图：必含 POLICY-STORAGE-FLOW（Java 产品链改实线）
必读：总控 §0 · architecture-baseline D12 · 细叶拆单 §1
禁止：Java 内 NLP/图谱算法；直连 nGQL；Feign demo-platform-entan-py / demo-svc-*。
JDBC / 读 ADS：demo_gkxlumenx_*（lumen 数仓 = demo 源；禁止另接正式数据面）。
对外：/topic/v1/policy/** ；下游 /internal/policy/**
```

FACADE/JOB 骨架不算完成叶。施工按细叶一路径一叶，同仓串行。
