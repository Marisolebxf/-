# P1-05 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **click** 单家企业卡「加入对比」 — locator.click: Timeout 3000ms exceeded. ✗
7. **wait** 成功反馈（toast/角标变化） ✓
8. **click** 对比篮按钮 ✓
9. **wait** 浮层展开 ✓
10. **snapshot**  ✓

## expect 逐条

- ✗ 加入后有成功反馈 — 已选计数条未出现(文本级) | assert: const mt = await page.locator('main').innerText(); if (!/已选 \d+ 家企业/.test(mt)) throw new Error('已选计数条未出现(文本级)'); await e
- ✓ 对比篮浮层列出至少一家企业

判定：**fail**
