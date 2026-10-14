# P1-15 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **fill** 搜索框=人工智能 ✓
3. **click** 搜索 ✓
4. **wait** 结果标题出现 ✓
5. **evaluate** 处于智能搜索结果态 — (observed 面，见截图/expect) ✓
6. **assert_visible** 结果摘要卡 ✓
7. **snapshot** 记录匹配字段 chips 或兜底文案（observed） ✓

## expect 逐条

- ✓ 显示已匹配字段与可关闭 chip
- ✓ 或显示未命中预设字段的多字段兜底文案（二者其一）

判定：**pass**
