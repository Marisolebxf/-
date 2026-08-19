# DONE · 1-panorama（DISPLAY-POLICY-GAP-AC-L01）

路由：`demo-ui-science` 政策跟踪 → `PolicyPanorama`（检索全景 / 政策动向 / 舆情评估 / 政策重点比对）。  
默认演示为完成态；页头 **演示闸门 Switch** 可切到未就绪。禁止 commit/push。

## 改动文件

| 文件 | 说明 |
|---|---|
| `repos/demo-ui-science/src/pages/policy-tracking/search/displayPolicySearchConfig.js` | `SORT_OPTIONS`：`level` 标签「效力级别（高→低）」；新增 `levelAsc` / `viewsAsc` |
| `repos/demo-ui-science/src/pages/policy-tracking/search/displaySearchResultUtils.js` | `sortPolicyResults` 升序 case；`refinePoliciesByPublishRange` |
| `repos/demo-ui-science/src/pages/policy-tracking/policyPanoramaGapMock.js` | **新建**页内 mock：优缺点、真实需求、意见聚类、按企业匹配、对标缩放、邮箱校验 |
| `repos/demo-ui-science/src/pages/policy-tracking/PolicyPanorama.jsx` | 档 A #3–#9 + 档 C 24 条闸门 |

未改：`policyData.js`、`fp-split-run/`。

## 档 A #1–#9

| # | 验收点 |
|---|---|
| 1 | 检索全景 → 排序下拉「效力级别（低→高）」；区县级排国家级前。原「效力级别（高→低）」仍高→低 |
| 2 | 「浏览量（低→高）」按 `viewCount` 升序；「浏览量（高→低）」不变 |
| 3 | 命中结果区「二次筛选 · 发布日期」两个 DatePicker（与高级检索发布年分离）。起点晚于终点 → Alert + 不切片 |
| 4–5 | 舆情评估 → 打开政策对比工具 → 总结区按政策列出 **优点/缺点** `<ul>`（非「可据此识别优缺点」） |
| 6 | 反馈列表每条「真实需求：…」+ 详情 Descriptions |
| 7 | 意见征集渠道出现「意见识别 / 聚类结果」区 |
| 8 | 匹配弹窗切换企业（智航 / 博济 / 蔚蓝）匹配列表不同；清空企业 → Empty |
| 9 | 标杆比对「选择对标政策」Select，雷达/柱/热力/表数字随政策变 |

## 档 C 24 条（`1-panorama-C.md`）

页头 Switch 默认开；关掉对应项应 Empty/Alert/disabled。另有「有检索结果」便于切空命中。

| T | 闸门 | 怎么点 |
|---|---|---|
| T36 | 未整合不可全景可视化 | 关「政策已整合」→ 顶部 KPI 变 Alert |
| T36 | 无结果不可排序/二次筛/分组/分享 | 关「有检索结果」→ 控件 disabled + Empty |
| T36 | 起点不得晚于终点 | 二次筛起点选更晚日期 → 红 Alert |
| T36 | 分享邮箱格式 | 有结果时分享 → 邮件 → 填非法地址 → 报错 |
| T37 | 未更新不可看最新列表 | 动向 Tab，关「政策库已更新」 |
| T37 | 订阅至少一项条件 | 政策订阅服务：四类条件全空保存 → warning |
| T37 | 未汇总举措不可分析重点领域 | 关「举措已汇总」 |
| T37 | 未完成分析不可看深度报告 | 关「分析已完成」→ 深度报告按钮 disabled |
| T37 | 未完成可视化不可看分布 | 关「可视化已完成」→ 热力/趋势 Empty |
| T38 | 未完成差异分析 | 舆情 → 关「差异分析已完成」 |
| T38 | 无实施数据不可跟踪 | 关「已具备实施数据」 |
| T38 | 未收集完不可评估落地 | 关「数据收集已完成」→ 状态「待评估」+ Alert |
| T38 | 无反馈不可看汇总 | 关「已收集到反馈」 |
| T38 | 实施数据+反馈缺一不可生成报告 | 关上述任一 → 评估报告 Empty |
| T38 | 无登记信息不可匹配 | 匹配弹窗清空企业 Select |
| T38 | 未完成匹配不可查看适合政策 | 关「匹配已完成」 |
| T38 | 无匹配结果不可推送 | 企业有画像但 matches 空时推送 disabled |
| T39 | 未选政策不可新旧对比 | 重点比对清空政策 Select |
| T39 | 部门对比 ≥2 且跨区域 | 部门对比少选或同区 → Empty |
| T39 | 未选对标对象不可生成报告 | 标杆比对取消全部城市 → 按钮 disabled |

## 未完成项

无。
