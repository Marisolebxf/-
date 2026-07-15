# ENT-STAR validation report

## 当前结论

E-34 v0.5 “产品功能全景”已按修改后的四件套落地并完成机器与双模式浏览器验证。覆盖项共 6 项，其中 `E34-PRODUCT-MEDIA`、`E34-TEAM-SHOWCASE` 为 `verified`，其余 4 项维持既有 `manual_review`；P0 blocker 为无。

## 本轮产品功能全景实现范围

- 产品数据模型补齐 `productId/productName/productSummary/impactSummary/sortOrder/publishStatus`，以及功能模块、场景、案例和媒体关联字段。
- 当前企业产品按 `sortOrder` 展示，支持 `0..N`；中屏每页最多 3 个，1~3 个隐藏分页，4 个及以上显示标题右侧页码与上一页/下一页。
- 翻页选择目标页第一项；产品卡显示明确选中态并联动功能模块、模块说明、应用场景、行业案例和当前产品媒体。
- 产品、页码与模块均为局部状态，不写 URL；切换产品关闭旧媒体层并重置首个模块，切换企业回到第 1 页首个产品。
- 产品卡、模块和分页均具备按钮语义、键盘路径、焦点样式、边界禁用和 `aria-live` 状态播报；没有自动轮播、循环或整页横向滚动。
- 业务态只显示产品业务内容和必要示例披露；评审态追加产品/模块原始 ID、发布状态与 Q041。

## 既有团队模块实现范围

- 团队模块从原技术/团队双栏拆出，置于“技术优势可视化”下方并独占一行。
- 业务态展示当前成员写实人物照片、画像摘要、专业领域、行业成就、主导项目、其他成员卡、人才比例和团队成果。
- 上一位、下一位、成员卡点击与键盘左右键均可循环切换；切换企业后恢复该企业首位已发布成员。
- 内部评审模式打开后继续保留完整人物展示，并在其下追加 Q041、数据时间、发布状态、照片授权和外链授权表。
- 无已发布成员时展示局部空态；无有效授权外链时不显示“了解更多”。
- 四张人物图片为 AI 生成的虚构写实职业肖像，压缩后随源码本地打包；不指向真实企业成员、公众人物或外部图片地址。

## TDD

- RED 4：v0.5 专项合同因缺少 `productId` 和产品分页数据失败。
- GREEN 4：扩展确定性产品数据模型，并为集成电路明星企业增加 5 个产品以覆盖第二页。
- RED 5：专项合同继续因缺少 `PRODUCT_PAGE_SIZE`、产品局部状态、分页按钮和选中联动失败。
- GREEN 5：实现每页 3 个、目标页首项选中、模块/媒体联动、空态和无障碍状态后通过。

- RED 1：专项合同因缺少独立 `StarTeamShowcase`、成员字段、人物资产与全宽顺序失败。
- GREEN 1：实现团队数据模型、全宽人物轮播、模式门控与本地人物资产后通过。
- RED 2：针对图片丢失反馈，合同因缺少随构建打包的人物资源失败。
- GREEN 2：资源改由 `src/assets` 静态导入后通过，浏览器四图均 `complete=true`。
- RED 3：针对“内部评审模式打开后要显示”，合同因评审分支替换人物展示失败。
- GREEN 3：人物展示改为双模式共享，评审字段作为追加内容后通过。

## 浏览器证据

- 产品评审态：第 2/2 页显示 Chiplet 互连平台与可靠性验证平台；当前产品为 Chiplet 互连平台；下一页禁用、上一页可用；原始产品/模块 ID、发布状态和 Q041 可见。
- 产品业务态：同一第 2/2 页保留产品、模块、场景、案例和媒体；`product_id`、`publish_status`、Q041、追溯头和成员审查表均不可见；数据时间与必要演示披露仍保留。
- 产品业务态截图：`/Users/ying/.codex/visualizations/2026/07/15/019f64c5-2efe-77e0-907d-f2c48214bf35/e34-product-business.png`
- 产品评审态截图：`/Users/ying/.codex/visualizations/2026/07/15/019f64c5-2efe-77e0-907d-f2c48214bf35/e34-product-review.png`
- 产品 DOM 快照：同目录 `e34-product-business.txt`、`e34-product-review.txt`。

- 业务态：4 张写实人物照片均加载，`naturalWidth=675`、`naturalHeight=900`；轮播与上一位/下一位可见；点击下一位后从核心成员 A 切换到 B；评审表与 Q041 不可见。
- 内部评审态：4 张写实人物照片、轮播与切换按钮继续可见；Q041 和成员发布授权表同时可见。
- 业务态截图：`/Users/ying/.codex/visualizations/2026/07/15/019f64b1-95ff-7dc2-88fe-6176e314bad3/e34-team-business.png`
- 评审态截图：`/Users/ying/.codex/visualizations/2026/07/15/019f64b1-95ff-7dc2-88fe-6176e314bad3/e34-team-review.png`
- DOM 快照：同目录 `e34-team-business.txt`、`e34-team-review.txt`。

## 机器检查

- `node tests/enterprise-overview-e33-e35.test.mjs`：通过。
- `npm run design:check`：通过。
- `npm run build`：通过；Vite 仅保留既有大 chunk 警告，不影响退出码。
- TRACE 与 3 份交付覆盖 YAML：最终解析见本次交付输出。
- `git diff --check`：最终验证见本次交付输出。

## 剩余人工复核

- 既有两级产业/企业选择、入选标准 Drawer、技术局部空态和生态关系 Drawer 等 4 个覆盖项仍沿用原 `manual_review` 状态，未被本次产品与团队验证冒充为已复核。
