# P1-24 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态（搜索框含词） — (observed 面，见截图/expect) ✓
6. **click** 清空按钮 ✓
7. **wait** 离开结果态 ✓
8. **snapshot**  ✓

## expect 逐条

- ✗ 清除后离开结果态或结果被清空 — expect count=0 超时 5000ms | assert: const mt24 = await page.locator('main').innerText(); if (mt24.includes('智能搜索结果 命中')) throw new Error('清除后结果态仍在'); await 
- ✓ 可见示例查询或推荐企业或引导空态之一

判定：**fail**
