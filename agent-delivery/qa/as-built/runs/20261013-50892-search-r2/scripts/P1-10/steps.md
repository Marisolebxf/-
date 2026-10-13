# P1-10 逐步实际操作

1. 结果态，定位工具条区域控件（.arco-select-view-single.sci-arco-cascader）
2. 记录控件当前值：「全国热门科创城市 / 深圳 / 全部」
3. mousedown+click 展开 → .arco-cascader-panel 出现
4. 读取第一列 .arco-cascader-panel-column 选项：全球 / 全国 / 区域 / 全国热门科创城市
5. Esc 收起面板
6. 判定：控件可打开级联 ✅ + 展开后 ≥ 一级可选项 ✅ → Pass（占位文案差异记 observed）
