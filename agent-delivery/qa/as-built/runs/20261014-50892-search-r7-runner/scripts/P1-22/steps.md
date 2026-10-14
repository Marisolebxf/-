# P1-22 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于非空结果态 — (observed 面，见截图/expect) ✓
6. **click** 任一卡片行「导出」 ✓
7. **assert_visible** 弹层标题 ✓
8. **snapshot** 记录导出范围=单个企业且对象数量 1（observed） ✓
9. **click** 创建导出任务 ✓
10. **wait** 任务完成 ✓
11. **evaluate** 下载文件入 artifacts/ 并核对（附录B 同 P1-11） — (observed 面，见截图/expect) ✓

## expect 逐条

- ✗ 弹层导出范围为单个企业且对象数量为 1 — expect visible 超时 8000ms | assert: const modal = page.locator('.arco-modal').filter({ hasText: '确认导出查询清单' }).first(); await expect(modal).toBeVisible({ tim
- ⚠ 文件含该行企业名称且声明字段可核对

判定：**fail**
