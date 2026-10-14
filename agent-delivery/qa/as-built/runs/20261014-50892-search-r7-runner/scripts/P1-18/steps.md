# P1-18 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于高级筛选结果态（承接 P0-06/P0-10） — (observed 面，见截图/expect) ✓
6. **click** 编辑高级筛选 — locator.click: Timeout 3000ms exceeded. ✗
7. **wait** 回到字段库 ✓
8. **assert_visible** 字段库 — locator.waitFor: Timeout 6000ms exceeded. ✗
9. **snapshot** 记录先前条件保留情况 ✓

## expect 逐条

- ✗ 页面回到字段库编辑态 — expect visible 超时 8000ms | assert: await expect(page.getByText('企业所属地区').first()).toBeVisible({ timeout: 8000 }); await expect(page.getByRole('button', { n
- ✗ 先前已选条件保留 — 回字段库后未见保留的已选条件计数 | assert: const bodyText = await page.locator('main, body').first().innerText(); if (!/已选\s*[1-9]\d*\s*(个条件|家企业)/.test(bodyText)) 

判定：**fail**
