# ENT-SHENZHEN validation report

> 状态：E-35 v0.4 已完成四件套、Demo、交付覆盖与双模式浏览器验证；本轮模式显隐与图表单位修正已验证，领域概况视觉仍保留 `manual_review`。

## 范围

- 页面：`/enterprise-center/overview?tab=shenzhen`
- 覆盖：既有 v0.3 行为；领域概况删除固定映射覆盖率与进度条，改为当前数据集合的“已识别领域/环节 X 个”；Q049 说明仅在评审态显示。
- 不覆盖：正式 metric_id、ADS 来源、产业链正式映射、重点企业正式判定、企业清单下钻。

## 机器验证

- `node --experimental-strip-types tests/e35-shenzhen-trend-selection.test.mjs`：5/5 通过。
- `node --experimental-strip-types tests/e35-shenzhen-layout-navigation.test.mjs`：5/5 通过。
- `node tests/enterprise-overview-e33-e35.test.mjs`：E-33~E-35 页面静态合同通过。
- `npm run design:check`：Design contract checks passed。
- `npm run build`：生产构建成功；保留仓库既有大 chunk 警告，无新增构建错误。
- `curl -I http://127.0.0.1:4177/enterprise-center/overview?...`：HTTP 200。
- `git diff --check`：本次 Demo 写入文件无空白错误。

## 浏览器验证

- 评审态初始：URL `future_industry_code=integrated-circuit` 初始化为集成电路单选，趋势展示单序列。
- 双选：点击人工智能后显示 `已选 2/2`，数量柱、按钮、折线与图例同步为两个产业。
- 上限：双选后点击新能源，显示“最多对比两个产业，请先取消一个已选产业”，选择仍保持 2 个。
- 业务态：隐藏顶部说明、数据时间和历史趋势，保留当年数量对比并占满整行；DOM 不得检出评审说明。
- 评审态：保留 Q049、DEMO、连续可比点阈值与局部联动边界说明。
- 领域区：原始需求说明仅在评审态显示；概况与列表保持上下结构；不再显示“产业链领域映射覆盖”、固定 76%/32% 或进度条。
- 动态计数：集成电路显示“已识别领域/环节 15 个”，切换海洋经济后显示“9 个”，证明数字来自当前产业去重领域/环节集合而非统一占位值。
- 评审态：显示“覆盖率口径与全量环节分母待 Q049 确认。”；业务态 DOM 中 Q049、覆盖率标签和 progressbar 均为 0 项。
- 重点企业宽视口：八个产业以横向 Tabs 展示，一次只显示当前产业企业卡。
- 重点企业窄视口：显示 4 个可见 Tabs 和可搜索“更多产业”；搜索并选择“量子信息”后，该产业进入可见 Tab，显示 `当前产业：量子信息` 及对应卡片，全部目录仍可达。
- v0.4 业务态：保留领域计数、领域展开和重点企业导航；领域区 DOM 未检出 `Q049`、映射覆盖标签或进度条。
- 本轮评审态：顶部说明、历史趋势和领域需求说明均可见；数量对比、趋势和规模图的纵轴单位“家”完整显示。
- 本轮业务态：顶部说明、历史趋势、领域需求说明均不可见；数量对比卡宽度 1425px，占页面内容剩余整行；“当前产业链”“当前产业”均未检出。

## 证据

- `e35-trend-single-review.png`：评审态单产业。
- `e35-trend-dual-review.png`：评审态双产业，两条完整 2020~2024 折线。
- `e35-trend-limit-review.png`：第三产业阻止反馈。
- `e35-trend-q049-review.png`：Q049 评审溯源。
- `e35-trend-dual-business.png`：业务态双产业与普通语言显隐检查。
- `e35-v03-domain-review.png`：评审态领域上下结构与首批 12 项。
- `e35-v03-domain-expanded-review.png`：评审态领域全部展开与收起入口。
- `e35-v03-domain-business.png`：业务态领域区显隐。
- `e35-v04-domain-summary-review.png`：评审态集成电路 15 个已识别领域/环节及 Q049 说明。
- `e35-v04-domain-summary-business-marine.png`：业务态海洋经济 9 个已识别领域/环节，无覆盖率和进度条。
- `e35-v03-key-enterprise-review.png`：评审态宽视口产业 Tabs 与单产业企业卡。
- `e35-v03-key-enterprise-business.png`：业务态重点企业区显隐。
- `e35-v03-key-enterprise-narrow-overflow.png`：窄视口“更多产业”搜索选择“量子信息”后的可见 Tab 与卡片。
- `e35-review-feedback-review.png`：本轮评审态显隐与数量/趋势单位。
- `e35-review-feedback-business.png`：本轮业务态整行数量对比与显隐。
- `e35-review-feedback-scale-unit.png`：规模分析纵轴单位“家”完整显示。

本轮证据目录：`/Users/ying/.codex/visualizations/2026/07/15/019f64c5-2efe-77e0-907d-f2c48214bf35/`

## 结论

- `E35-TREND-VISIBILITY`、`E35-TREND-DUAL-MODE`、`E35-CHART-UNIT-LAYOUT`：`verified`。
- `E35-TREND-SELECTION`、`E35-DOMAIN-VERTICAL-DISCLOSURE`、`E35-KEY-ENTERPRISE-NAVIGATION`：实现、行为和浏览器证据已验证，等待产品方最终视觉确认，标记 `manual_review`；领域项已消除虚假覆盖率，但 Q049 仍未闭合。
- Q049 未闭合，数据仍为确定性模拟序列；本报告不代表 Gate 1、正式指标或数据接入通过。
