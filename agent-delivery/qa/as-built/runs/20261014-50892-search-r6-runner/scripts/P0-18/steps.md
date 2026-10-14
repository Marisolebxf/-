# P0-18 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **click** tab 查企业 ✓
3. **assert_visible** 查企业搜索框（占位指向企业名称） — locator.waitFor: Timeout 6000ms exceeded. ✗
4. **click** tab 高级筛选 ✓
5. **assert_visible** 字段库 ✓
6. **evaluate** 确认无智能搜索大输入框 — (observed 面，见截图/expect) ✓
7. **click** tab 智能搜索 ✓
8. **assert_visible** 四层主视觉与引导态 — locator.waitFor: Timeout 6000ms exceeded. ✗

## expect 逐条

- ✓ 查企业下搜索框占位指向企业名称关键词
- ✗ 高级筛选下呈现字段库且无智能搜索大输入框 — expect visible 超时 8000ms | assert: await expect(page.locator('main').getByText(/企业所属地区/).first()).toBeVisible({ timeout: 8000 }); await expect(page.getByRo
- ✓ 切回智能搜索后四层主视觉与引导态再现

判定：**fail**
