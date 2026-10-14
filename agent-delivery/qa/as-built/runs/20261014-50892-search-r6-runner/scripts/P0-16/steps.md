# P0-16 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **click** 第一张卡复选框 ✓
7. **click** 第二张卡复选框 ✓
8. **assert_visible** 已选企业计数条 — locator.waitFor: Timeout 6000ms exceeded. ✗
9. **evaluate** 记录加篮前对比篮角标数 — (observed 面，见截图/expect) ✓
10. **click** 加入对比 — locator.click: Timeout 3000ms exceeded. ✗
11. **wait** 角标数量变化 ✓

## expect 逐条

- ✗ 勾选后出现已选企业计数条 — expect visible 超时 8000ms | assert: await expect(page.getByText(/已选 \d+ 家企业/).first()).toBeVisible({ timeout: 8000 }); await expect(page.getByText('清除选择').f
- ✓ 批量加入后对比篮角标数量增加

判定：**fail**
