# P0-02 逐步实际操作

1. 初始态快照（browser_click ref e7 = 示例 chip「人工智能」）
2. 点击后快照确认：textbox value=人工智能；active/focused 态在该 chip
3. CDP 确认空态提示仍在、无结果标题（「智能搜索结果」字样不存在）
4. 判定：回填 ✅ + 维持引导态 ✅ → Pass
