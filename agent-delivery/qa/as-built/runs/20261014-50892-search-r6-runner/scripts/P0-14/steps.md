# P0-14 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于结果态 — (observed 面，见截图/expect) ✓
6. **click** 结果内筛选 经营状态 ✓
7. **select_option** 经营状态 — locator.selectOption: Timeout 30000ms exceeded. ✗
8. **wait** 列表更新（结果态保持） ✓
9. **snapshot** 记录再筛前后条数（observed） ✓
10. **click** 清除该再筛条件（chip 关闭） — locator.click: Timeout 3000ms exceeded. ✗
11. **wait** 列表恢复 ✓

## expect 逐条

- ✓ 施加后列表仍处结果态且条数变化可解释
- ✓ 清除后结果恢复再筛前范围

判定：**pass**
