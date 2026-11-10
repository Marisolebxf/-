# DS10-QRY-FDE · 波次 D · frontend-agent

总单：`POL-L2-DS10-QRY-FDE-L01`。会签已闭合（`DS10-QRY-FDE-C-异议闭合.md`）。  
你是 frontend-agent。只改展示仓 `lumen-ui-science-pc`。强度：ponytail full。

## 真源（只读）

- 说明书「#### 197」
- `sdd/l2/会签/DS10-QRY-FDE-蓝色区-线框.md`
- `sdd/l2/会签/DS10-QRY-FDE-C-异议闭合.md`（含 1B/2B/3A）
- `sdd/l2/会签/DS10-QRY-FDE-C-热门预填对照.md`
- 专题文案常量（**复制**进展示仓，禁止运行时依赖 demo/topic）：  
  `repos/lumen-ui-topic/src/views/policy/policySearchModel.ts` 的 `POLICY_QUERY_EXAMPLES` / `POLICY_KEYWORD_EXAMPLES`

## 改什么（仓：`e:\zhipu\gkx-lumen\repos\lumen-ui-science-pc`）

主要：`src/views/policy/panorama/search/DisplayPolicySearchHub.vue`、`displayPolicySearchConfig.ts`、父页 `panorama/index.vue`（最近检索位置）。

1. **Tab 文案跟招标**：保持「智能检索 / 关键词搜索 / 高级检索功能」
2. **示例分套**：智能 = 专题 QUERY 四条；关键词 = 专题 KEYWORD 四条；高级不挂文案示例行
3. **点示例只填不搜**
4. **最近检索**：挪到蓝色区下（Hub 内或紧贴下方）；按 mode 分桶；高级态仍在蓝色区下 advanced 桶；收藏仍留结果区；扩展 localStorage 结构带 `mode`（兼容旧无 mode 记录：可读时归 keyword 或不展示，选一种写进注释）
5. **热门**：filter → 切高级 + 按对照表预填 FilterDSL + 待应用（不立刻 search）；若出现非 filter → 只填关键词、不自动搜（1B）
6. **本波不验收**（2B）：失败/停用/热门空不新做专门 UI；沿既有 intent 回退

## 验证

- `pnpm type-check`（或仓规定等价）绿
- 有最小自检更好（非必须框架）
- **不要 push**；自检绿后停在本地，等监管人确认再推（fe-manual-confirm-push）

## 回复

改了哪些文件；自检命令与结果；待推送。
