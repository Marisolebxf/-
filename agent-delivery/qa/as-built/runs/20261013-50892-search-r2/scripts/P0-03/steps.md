# P0-03 逐步实际操作

1. 搜索框已含「人工智能」（承接 P0-02）
2. browser_click 搜索按钮被对比篮侧面板遮挡（Click intercepted by non-interactive div 336x698）→ 改 JS click（btns.find('搜索').click()）成功
3. 等待 2.5s 后 CDP 读取：结果标题「智能搜索结果 命中 4493 家企业」出现
4. 确认长卡结构：企业名 button（深圳市三通连接系统有限公司）+ 在营 + 查看画像 + 引育候选；36 个复选框（9 卡/页 × 4 组 DOM）
5. 判定：结果标题+命中条数 ✅、长卡含名称与经营状态 ✅、查看画像 ✅ → Pass
