# P1-14 逐步实际操作

1. 直接导航 /enterprise/enterprise-search?mode=advanced（全量加载，非 SPA 内切换）
2. 断言：高级筛选 tab aria-selected=true ✅；字段库/高筛面板在 ✅；hero 搜索框不可见 ✅
3. 附带发现（非断言）：/enterprise/search?mode=advanced 为错误路由 → 企业详情壳 + Request failed 424（记 observed）
4. 判定 Pass
