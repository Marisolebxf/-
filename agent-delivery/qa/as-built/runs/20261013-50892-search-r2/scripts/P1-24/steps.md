# P1-24 逐步实际操作

1. 结果态（搜索框含「人工智能」），定位输入框尾部 .arco-input-clear-btn
2. click 清除 → input value=""
3. 核对：结果标题消失（stillResult=false）、卡片 0、示例查询行在、引导空态文案在
4. 判定：离开结果态 ✅ + 引导形态可见（示例查询+引导空态）→ Pass
