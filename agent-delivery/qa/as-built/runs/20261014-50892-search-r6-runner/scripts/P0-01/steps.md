# P0-01 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **assert_url** /enterprise/enterprise-search ✓
3. **assert_visible** tab「智能搜索」 — locator.waitFor: Timeout 6000ms exceeded. ✗

## expect 逐条

- ✓ 路由为企业查询页且智能搜索为选中态
- ✗ 顶部自上而下依次为检索模式、搜索框、示例查询、热门场景 — locator.isVisible: Error: strict mode violation: locator('main').getByText('热门场景') resolved to 2 elements: | assert: await expect(page.getByRole('tab', { name: '智能搜索' })).toBeVisible({ timeout: 8000 }); await expect(page.getByRole('textb
- ⚠ 示例查询与热门场景各占独立一行
- ✓ 蓝色搜索主视觉可见

判定：**fail**
