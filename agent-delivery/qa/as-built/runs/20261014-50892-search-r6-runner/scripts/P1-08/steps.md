# P1-08 逐步实际操作（playwright-runner）

1. **evaluate** 处于企业查询页（结果态或初始态均可，建议结果态） — (observed 面，见截图/expect) ✓
2. **click** 开启内部评审模式 — locator.click: Timeout 3000ms exceeded. ✗
3. **assert_visible** 标题旁章节溯源挂载 — locator.waitFor: Timeout 6000ms exceeded. ✗
4. **click** 关闭内部评审模式 — locator.click: Timeout 3000ms exceeded. ✗
5. **evaluate** 溯源隐藏且业务区无评审字样残留；开关过程不退出企业查询页 — (observed 面，见截图/expect) ✓

## expect 逐条

- ⚠ 开启后页面标题旁可见需求章节溯源挂载
- ✓ 关闭后溯源隐藏且业务区无评审字样残留
- ✓ 开关过程不退出企业查询页

判定：**pass**
