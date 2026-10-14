# P1-04 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **click** 结果卡查看画像按钮 ✓
7. **wait** 抽屉打开 ✓
8. **assert_visible** .arco-drawer ✓
9. **evaluate** 默认页签为工商概况；关闭抽屉后结果态保留（顺带核对） — (observed 面，见截图/expect) ✓

## expect 逐条

- ✓ 抽屉打开且路由不变
- ✗ 默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms | assert: await expect(page.locator('.arco-drawer, .arco-modal').filter({ hasText: '企业' }).first()).toContainText('工商概况')

判定：**fail**
