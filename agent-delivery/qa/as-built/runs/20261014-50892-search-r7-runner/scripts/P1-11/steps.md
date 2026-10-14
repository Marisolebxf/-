# P1-11 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于非空结果态（智能搜索 人工智能） — (observed 面，见截图/expect) ✓
6. **click** 导出当前结果 ✓
7. **assert_visible** 弹层标题「确认导出查询清单」 ✓
8. **snapshot** 记录弹层字段范围与对象数量（observed） ✓
9. **click** 创建导出任务 ✓
10. **wait** 任务完成（导出记录可下载） ✓
11. **evaluate** 下载文件入 artifacts/ — (observed 面，见截图/expect) ✓
12. **evaluate** 按附录B七字段核对（≥6/7 且行数=弹层对象数） — (observed 面，见截图/expect) ✓

## expect 逐条

- ✗ 弹层字段范围含附录B七字段 — expect visible 超时 8000ms | assert: const modal = page.locator('.arco-modal').filter({ hasText: '确认导出查询清单' }).first(); await expect(modal).toBeVisible({ tim
- ✓ 任务达到已完成且产出非空文件
- ⚠ 文件表头或正文含七字段至少六个
- ⚠ 文件行数与弹层对象数量一致

判定：**fail**
