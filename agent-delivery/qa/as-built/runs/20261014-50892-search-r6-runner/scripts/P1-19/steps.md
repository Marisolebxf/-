# P1-19 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **click** 结果卡引育候选按钮 ✓
7. **assert_visible** 菜单 — locator.waitFor: Timeout 6000ms exceeded. ✗
8. **click** 加入招引候选 ✓
9. **wait** 反馈出现 ✓

## expect 逐条

- ✗ 出现已加入候选类反馈或菜单项变为已在候选态 — 未见加入候选反馈或已在候选态 | assert: const bodyText = await page.locator('main, body').first().innerText(); if (!/已加入|已在.*候选|已加入候选|候选/.test(bodyText)) { awai

判定：**fail**
