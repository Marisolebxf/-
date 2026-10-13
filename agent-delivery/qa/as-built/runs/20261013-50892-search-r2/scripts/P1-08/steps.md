# P1-08 逐步实际操作

1. click 右上「创新工作台 INNO」→ persona-menu 展开（政府驾驶舱/创新工作台/研判/访客/运营/系统 6 视角 + 付费权益 + 内部评审模式 + 高级演示调节）
2. 断言「内部评审模式」switch 存在（aria-label=内部评审模式）✅ 默认 checked=true ✅
3. 开启态记录 observed：结果标题「智能搜索结果 命中 0 家企业」，无溯源字样
4. click switch → aria-checked=false ✅
5. 断言 DOM 零泄漏：metric_id / GAP- / Q0xx / 就绪度 全无 ✅
6. 判定 Pass（开关行为 + 关闭态干净；标题溯源切换本页未呈现记 observed）
