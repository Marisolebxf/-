# P1-26 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态并勾选 1~2 家 — (observed 面，见截图/expect) ✓
6. **click** 开启内部评审模式 — locator.click: Timeout 3000ms exceeded. ✗
7. **click** 关闭内部评审模式 — locator.click: Timeout 3000ms exceeded. ✗
8. **evaluate** 核对已选计数与切换前一致 — (observed 面，见截图/expect) ✓

## expect 逐条

- ✗ 开关往返后已选企业计数与切换前一致 — 已选计数条与评审开关均不可见（R4 locator 缺失，见 observed） | assert: const bar = page.locator('main').getByText(/已选 \d+ 家企业/).first(); const count1 = await bar.innerText().catch(() => null)

判定：**fail**
