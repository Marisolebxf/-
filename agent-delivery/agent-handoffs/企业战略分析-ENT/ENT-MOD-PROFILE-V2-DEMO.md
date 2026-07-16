# ENT-MOD-PROFILE-V2-DEMO handoff（执行中）

- **status**：`in_progress`
- **监管**：`human:曹丽影`
- **范围调整（2026-07-16）**：详情**不**做独立页；在高级筛选页（COMPONENTS `AdvancedFilterView`）Mock 1 条企业，点击打开 `ElementProfile` **抽屉**。

## 当前演示路径

1. COMPONENTS worktree → 菜单「高级筛选」
2. 点击「演示结果」Mock 卡片 → 企业画像抽屉
3. 抽屉内「查看详情」仍留在抽屉，不跳转 `/enterprise/:code`

## 开放项

- PROFILE 原 `EnterpriseDetail.vue` 整页方案搁置（菜单已摘掉 component）
- 若需抽屉内完整 Tab（关系图谱等），再把 `EnterpriseProfileTabPanel` 合入抽屉/弹层
- commit / MR 待确认
