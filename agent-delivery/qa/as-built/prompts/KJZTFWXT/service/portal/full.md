# 专题服务 · 全量执行顺序（2026-10-14 BATCH32，22 条）

entry_id=`svc-portal` · 路由 `/service-portal` → `/service-portal/overview`

## 推荐顺序

1. **金样冒烟**（P0-01→P0-06）：入口 → 概况图表 → 产业分布 → 区域 → 技术能力 → 深圳抽屉（空则 N/A）
2. **壳层与筛选**（P0-07→P0-10）：五 Tab 互斥 → 链禁用 → 级联解锁 → KPI 构成
3. **各视图深径**（P0-11→P0-16）：环节下钻 / 圆点 / 金银铜 / 深圳分流 / 卡片墙 / 筛选持久化
4. **备选与异常**（P1-01→P1-06）：技术能力切换 → 参数恢复 → 评审角标 → 零泄漏 → 无映射 → 非法参

## 易错点

- **P3 评审**：`aria-label="内部评审模式"`，禁止 `first()` 盲点第二个 switch；菜单开着会挡主区。
- **P7 下拉**：点 `.arco-select-view`（含 placeholder 的可见触发器），勿点隐藏 input。
- **P8 隔离**：进入页对比篮常默认展开 → 先点「关闭对比篮」；每条 assert 自含 goto/关浮层。
- **子路由**：Tab 切换后为 `industry-distribution` / `region-map` / `capability-rank` / `shenzhen`，断言 URL 时带上。
- **诚实空**：规模四档 / 环节分布 / 热力 / 技术力榜 / 重点机构墙 均可空——对应脚本已 `allow_skip` 或按空态文案代理，勿发明演示数据断言。
- **深圳按钮**：页头 primary `button「深圳产业服务介绍」` ≠ Tab 同名；勿点「检索深圳服务机构」以免跳转 svc-search。

## 不跑

禁止本步 `run-scripts.mjs` 全量批跑；禁止新建 `runs/`。
