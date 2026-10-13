# P0-15 · 内部评审模式开关联动追溯显隐且关闭后零泄漏（00398）

1. goto `/enterprise/key-enterprise-analysis?view=type`；记录开关默认态 = 关（observed）。
2. 点击右上 persona 按钮（ref e0）展开人设面板。
3. 开启「内部评审模式」switch（ref e132 → checked）。
4. snapshot + CDP 核对评审元素：
   - main 区需求追溯按钮 3 处（分析类型输入归属 / 类型与区域分析 / 重点企业空间分布）；
   - `.perm-pending-badge` 3 处，含「口径待甲方确认，当前为团队临时默认值。」提示；
   - 指标说明按钮 ×2、指标未登记按钮 ×2。
5. 再开 persona 菜单，关闭「内部评审模式」switch（ref e160）。
6. CDP 零泄漏核验：main 区文本与 aria-label 中 需求追溯/口径待甲方确认/Q010/指标说明/指标未登记/M_ENT_* 全部不存在；badgeCount=0、traceCount=0、specBtns=0。

判定：三条预期（开启显追溯与角标 / 角标含待确认提示 / 关闭零泄漏）均成立 → Pass。
