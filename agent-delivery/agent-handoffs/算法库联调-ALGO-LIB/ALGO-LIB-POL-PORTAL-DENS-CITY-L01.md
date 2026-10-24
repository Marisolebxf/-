# ALGO-LIB-POL-PORTAL-DENS-CITY-L01 · 市发布密度（执行完毕）

> **执行日期**：2026-10-24 ｜ **执行方式**：并入 [ALGO-LIB-POL-PORTAL-NINE-L01.md](ALGO-LIB-POL-PORTAL-NINE-L01.md) 统一执行（九条同构，合并交付，细节真源见该件 §一/§三/§四）
> **claimed_by**: `agent:algorithm-agent`（代 human:唐绍祖 执行）｜ **supervised_by**: `human:淮政玮`

## DoD 对照

- 菜单「政策扶持-市发布密度」只展示本条算法结果与序列图：`portal_gaps.density_city`（名单内城市存量条数对比；区域×月矩阵逐月展开为二期），北京市 2,268 / 深圳 879 ✅
- 诚实口径：当前为存量对比，reason 写明「逐月矩阵二期」，不谎称条/月密度 ✅
- 拒绝改挂红线保留：M_POLICY_NATIONAL_DIST 不顶本条 ✅
- 不改契约、指标种子和就绪度矩阵，demo 不进 lumen ✅
- 本文件即本单 handoff（登记路径与 DoD 一致）

## 测试

全仓 `pytest tests/ -q` → **304 passed**（含本条两层契约）。
