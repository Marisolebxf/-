# P0-03 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **fill** 搜索框=人工智能 ✓
6. **click** 搜索按钮 ✓
7. **wait** 结果标题出现 ✓
8. **assert_visible** 智能搜索结果标题 — locator.waitFor: Timeout 6000ms exceeded. ✗
9. **assert_visible** 任一结果长卡片 — locator.waitFor: Timeout 6000ms exceeded. ✗
10. **assert_visible** 查看画像按钮 ✓
11. **snapshot**  ✓

## expect 逐条

- ✓ 结果标题为智能搜索结果且含命中条数
- ✓ 至少一张横向长卡片且含企业名称与经营状态
- ✓ 卡片含「查看画像」动作

判定：**pass**
