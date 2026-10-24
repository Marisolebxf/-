# ALGO-LIB-POL-PORTAL-SZ-DIST-L01 · 深圳各区发布情况（执行完毕）

> **执行日期**：2026-10-24 ｜ **执行方式**：并入 [ALGO-LIB-POL-PORTAL-NINE-L01.md](ALGO-LIB-POL-PORTAL-NINE-L01.md) 统一执行（九条同构，合并交付，细节真源见该件 §一/§三/§四）
> **claimed_by**: `agent:algorithm-agent`（代 human:唐绍祖 执行）｜ **supervised_by**: `human:淮政玮`

## DoD 对照

- 菜单「政策扶持-深圳各区发布情况」只展示本条算法结果与序列图：`portal_gaps.sz_district_publish`（区县切片 region 第7字起，无区归「市本级」不硬分区），实测 5 组（盐田4 / 光明1 / 南山1 / 大鹏1 / 市本级872）✅
- gkx 三方库区县级数据基本为空（'NULL' 字面量 18,835/20,000），以 demo `region` 切片为准并在口径备忘注明 ✅
- 拒绝改挂红线保留：M_POLICY_SZ_DIST / M_CHAIN_SZ_POLICY 的按区存量计数不顶本条 ✅
- 不改契约、指标种子和就绪度矩阵，demo 不进 lumen ✅
- 本文件即本单 handoff（登记路径与 DoD 一致）

## 测试

全仓 `pytest tests/ -q` → **304 passed**（含本条两层契约）。
