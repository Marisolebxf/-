# Handoff · DS10-SEARCH-REUSE-L01

> 展示科创政策全景「多维检索」复用专题政策查询内核  
> agent: frontend-agent · 依据 `DEC-DS10-SEARCH-REUSE-20260808`（沈悦已批）· 2026-08-08

## 1. 范围与实现

| 决策 | 落地 |
| --- | --- |
| 方案 B 嵌入式同构 | `#search` 顶部接入 `DisplayPolicySearchHub`，不跳转 `/policy/search` |
| 蓝底 + 橙黄 CTA | `displaySearch.css` + `enterprise-search-bg.png`，CTA `#ff7d00` |
| 智能检索 Wave0 | 模式「智能检索」+ `displaySmartParser` + 🧪 |
| 页内勾选上限 5 | `PAGE_COMPARE_LIMIT=5`；文案「页内比对，无对比篮」 |
| 主模式文案 | 「多维检索」 |

## 2. 产物

**代码（`repos/demo-ui-science`）**

- `src/shared/search/queryEngine.js`
- `src/pages/policy-tracking/search/DisplayPolicySearchHub.jsx`
- `src/pages/policy-tracking/search/displayPolicySearchConfig.js`
- `src/pages/policy-tracking/search/displaySmartParser.js`
- `src/pages/policy-tracking/search/displaySearch.css`
- `src/assets/enterprise-search-bg.png`
- `src/pages/policy-tracking/PolicyPanorama.jsx`（接入）

**方案文档**

- `产品整体定义/DS10-12-科技政策跟踪/PLAN-DS10-多维检索复用专题政策查询-完整方案.md`（approved）

## 3. 分轨自检

- 无对比篮 UI / ENT-COMPARE  
- recent key：`gkx-policy-display-search-recents:v1`  
- 不导航专题 `/policy/search`  
- `npm run build` 通过（2026-08-08）

## 4. 验收建议

1. 侧栏 → 科创政策全景 → 检索全景：见蓝底三模式，默认「多维检索」  
2. 智能检索输入「深圳 人工智能 市级」→ chip + 列表过滤  
3. 勾选第 6 项 → 提示上限 5  
4. Application 存储无 `gkx-policy-topic-search-recents`

## 5. 下一步

- 人工走查（沈悦视觉：蓝底橙黄按钮）  
- 可选：commit/push `demo-ui-science`  
- Wireframe 勾选上限回写为 5（产品小改）  
