# P1-01 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **assert_visible** 推荐企业分区 — locator.waitFor: Timeout 6000ms exceeded. ✗
3. **snapshot** 记录推荐卡字段与理由构成（observed） ✓

## expect 逐条

- ✗ 分区含推荐卡且卡上有「查看画像」 — 未见「推荐企业」分区（若为引导空态按 allow_skip 判 Pass-N/A） | assert: const section = page.locator('.recommend-section, [class*=recommend]').first(); const hasSection = await section.isVisib
- ✗ 对比动作为加入对比或已在对比篮 — 未见加入对比或对比篮入口 | assert: const bodyText = await page.locator('body').innerText(); if (!bodyText.includes('加入对比') && !bodyText.includes('对比篮')) { 

判定：**fail**
