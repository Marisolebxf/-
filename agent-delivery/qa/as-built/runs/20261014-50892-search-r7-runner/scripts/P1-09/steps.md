# P1-09 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **evaluate** 施加极窄再筛条件组合至零命中（如经营状态+企业规模交叠） — (observed 面，见截图/expect) ✓
7. **wait** 局部空态 ✓
8. **snapshot**  ✓

## expect 逐条

- ✗ 原查询摘要与排序、再筛、对比篮等结果操作区保留 — First argument to String.prototype.includes must not be a regular expression | assert: const bodyText = await page.locator('main, body').first().innerText(); for (const marker of ['智能搜索结果', '排序', /导出当前结果|结果内
- ✗ 仅列表区呈局部空态 — expect visible 超时 8000ms | assert: await expect(page.getByText('未命中结果，可调整条件或切换高级筛选').first()).toBeVisible({ timeout: 8000 }); await expect(page.getByText('

判定：**fail**
