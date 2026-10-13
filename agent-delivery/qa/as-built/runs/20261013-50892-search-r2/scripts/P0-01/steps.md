# P0-01 逐步实际操作

1. 导航 http://111.198.38.90:50892/ → 自动跳转 /enterprise/enterprise-search（会话保持，未重复登录）
2. 快照确认：三模式 tab（智能搜索 selected / 查企业 / 高级筛选）
3. CDP 读取页面结构：示例查询 5 chip、热门场景 4 chip、搜索按钮、空态提示
4. 断言四层排布顺序（DOM 顺序 = 视觉顺序：tab 行 → input → 示例行 → 热门行）
5. 判定：4 点预期全部满足 → Pass
