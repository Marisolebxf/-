# P1-13 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **click** tab 查企业 ✓
3. **evaluate** 确认「热门企业」分区可见 — (observed 面，见截图/expect) ✓
4. **click** 热门企业任一 chip ✓
5. **wait** 查企业结果标题（立即检索） ✓

## expect 逐条

- ✗ 页面出现查企业结果标题（立即检索，区别于示例查询仅回填） — expect visible 超时 8000ms | assert: await expect(page.getByText('查企业结果')).toBeVisible({ timeout: 8000 }); await expect(page.getByText(/命中 \d+ 家企业/).first())

判定：**fail**
