# DISPLAY-POLICY-GAP-AC-L01 施工规则（子 agent 必读）

- 仓：`f:/gkx-lumen/repos/demo-ui-science`
- 任务：`DISPLAY-POLICY-GAP-AC-L01`
- **禁止 git commit / git push**
- **禁止**改 `fp-split-run/`、`work/Txx.md` 结论列、T19–T21 专题仓
- **禁止**新 npm 包；演示 Mock 可验收；禁止真爬虫/真 NLP
- 档 B 106 条**不要做**
- T124 清洗档 D **不要做**
- 栈：现有 JSX + antd（本页已用 antd）+ 已有 echarts；D9：统计数字旁已有 ⓘ/🧪 则保持，新增 mock 数字挂 MockBadge/文案「演示」
- 闸门：前提不满足 → **disabled + Empty**（或 Alert），**不要**进 Tab 仍渲染完整 mock 当已就绪
- 默认数据可走完成态（有检索结果、已选政策），但必须能切到未就绪：清空结果 / 清空 Select / 关 Switch
- `policyData.js` **仅 Interpret 簇可改** `policyTextAnalysis` / `policyImpactScopeData` / `policyPathForecastData`；其余簇用页内 `useState` 或 `policyPcData.js` / 本簇已有文件
- 做完在本目录写 `DONE-<簇>.md`：列已改文件、档 A #、档 C 功能点、怎么点页面验收

路由（vite 4176）：政策跟踪在 `src` 路由里搜 `policy-tracking` / `PolicyPanorama` / `PolicyPcPages`。
