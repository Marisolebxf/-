# P0-10 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search?mode=advanced ✓
2. **click** 字段 企业所属地区 ✓
3. **select_option** 地区选择器 — locator.selectOption: Timeout 30000ms exceeded. ✗
4. **click** 字段 经营状态 ✓
5. **select_option** 经营状态 — locator.selectOption: Timeout 30000ms exceeded. ✗
6. **click** 应用筛选 ✓
7. **wait** 高级筛选结果标题 ✓

## expect 逐条

- ✗ 应用前可见已选条件计数 — expect visible 超时 8000ms | assert: await expect(page.getByText(/已选 \d+/).first()).toBeVisible({ timeout: 8000 })
- ✓ 应用后结果标题为高级筛选结果且含命中条数或明确空态
- ✗ 当前条件区含所设条件之一 — 当前条件区未见所设条件 | assert: const condText = await page.getByText('当前条件').first().innerText().catch(() => page.locator('body').innerText()); if (!co

判定：**fail**
