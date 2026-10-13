# P0-17 逐步实际操作

1. 注入 window.fetch / XMLHttpRequest.open 捕获钩子（window.__qa_captures）
2. 智能搜索输入「华为」→ click 搜索
3. 读取捕获：仅 1 条 /api/enterprise/topic/v1/search/smart ✅
4. 断言：无 /internal/* 直连（Python 内部接口不出前端）✅；无跨域第三方 ✅
5. 判定 Pass（前端只走 Java REST 网关，架构链路合规）
