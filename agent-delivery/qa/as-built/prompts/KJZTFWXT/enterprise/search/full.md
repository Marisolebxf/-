# 企业查询 P0/P1 全量 · 执行提示词

先读 `prompts/_result.md`、`scripts/KJZTFWXT/enterprise/search/gold.yaml`、`scripts.yaml`、`coverage.md`、`fixtures/testdata.yaml`。

环境：http://111.198.38.90:50892/  
账号：fixtures。已在业务页则不要反复登出。

**不要改金样 id。** `P0-01`～`P0-05` 以 `gold.yaml` 为准。

## 顺序

1. **金样**（同 `gold.md`）：P0-01 → P0-02 → P0-03 → P0-04 → P0-05  
2. **仍在结果态**：P1-16 关抽屉 → P1-04 查看画像 → Escape → P1-12 无 LLM → P1-15 chips → P1-20 无双视图 → P1-22 单卡导出 → P0-13 四类排序 → P1-23 升降序 → P0-14 再筛 → P1-09 若能收到 0 条 → P1-10 选择区域 → P0-15 分页 → P0-16 勾选批量对比 → P1-26 评审不丢选择 → P1-05 对比篮 → P1-19 引育 → P1-11 导出（必须有文件）→ P0-17 对照本段 Network  
3. **Hub 历史**：滚到顶部 P0-08 最近检索 → P1-21 清空最近检索  
4. **reload 企业查询**：P0-18 三 Tab → P1-01 推荐 → P1-02 理由/机制 → P1-25 另一示例回填（不要搜）→ P0-06 热门场景 → 必要时再 reload  
5. **查企业**：P0-07 → P1-13 热门企业（没有「热门企业」区则 Pass-N/A）→ P1-07 查企业点热门场景 → P1-03 0 命中 → P1-24 清除搜索框  
6. **高筛**：P0-09 字段库 → P0-11 全国地区 → P0-10 叠加应用 → P0-12 保存/使用方案 → P1-06 Footer 清空 → P1-17 收起展开 → P1-18 编辑高级筛选 → P1-14 `?mode=advanced` 面包屑  
7. **评审**：P1-08 开/关「内部评审模式」

每条独立目录：`runs/{run-id}/scripts/{id}/`，必须有 `result.yaml` + `steps.md`。检索条写命中名单，画像条写十页签及页内可见内容（`observed.yaml`）。**禁止只 mkdir 空目录、禁止只写根 `results.yaml`。** 最后 `SUMMARY.md`（P0/P1 分计；Pass-N/A 单独列）。

## 口径

- 公司全名、命中精确数字不钉死。  
- 热门场景 / 方案恢复 / 对比篮入口 / 无全选按钮：按 `coverage.md` as-built 列，不要用旧 FUNC 表打 Fail。  
- 分页命中 ≤9、无热门企业、再筛收不到 0：`allow_skip` → Pass-N/A。  
- 导出：必须「创建导出任务」、把文件放入 `scripts/{id}/artifacts/`，并核字段范围；只开确认框即过已废止。无文件 = Fail。
