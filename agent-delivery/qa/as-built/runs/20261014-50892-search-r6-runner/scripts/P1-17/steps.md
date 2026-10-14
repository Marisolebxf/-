# P1-17 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search?mode=advanced ✓
2. **click** 收起字段库 ✓
3. **evaluate** 字段标签隐藏且 Footer 操作仍在 — (observed 面，见截图/expect) ✓
4. **click** 展开字段库 ✓
5. **assert_visible** 字段标签恢复 — locator.waitFor: Timeout 6000ms exceeded. ✗

## expect 逐条

- ✓ 收起后字段标签隐藏且 Footer 操作仍在
- ✗ 展开后字段标签恢复可见 — expect visible 超时 8000ms | assert: await expect(page.getByText('企业所属地区').first()).toBeVisible({ timeout: 8000 })

判定：**fail**
