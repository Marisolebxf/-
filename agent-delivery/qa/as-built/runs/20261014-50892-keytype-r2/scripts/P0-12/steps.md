# P0-12 · 关闭企业清单抽屉后返回看板且筛选与洞察保持（00391）

1. 承接 P0-05：抽屉 .arco-drawer 打开态
2. 坐标点击 Close 被滚动约束拦截（element top=14 不可滚入）→ 改 CDP DOM click .arco-drawer-close-btn
3. 观察离场动画：slide-right-drawer-leave-active → 复核 getBoundingClientRect().x=1206（整宽 720 移出右侧视口）
4. 核对仍在类型分析页（URL 不变）、筛选四组默认值保持、H3 区域洞察 + 查看企业清单（0）保持
5. 判定：关闭恢复 + 状态保持 2 点全部满足 → Pass
