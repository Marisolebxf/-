# SUMMARY · 20261014-50892-search-r8-runner

原生 Playwright runner 校准跑（feature=search）。环境 http://111.198.38.90:50892（admin）。
P0/P1 机检通过 21/41；总判定 Pass 21 / Fail 20 / Blocked 0 / N-A 0。

| id | 用例 | 标题 | 判定 | 说明 |
|---|---|---|---|---|
| P0-01 | 00438 | 侧栏进入企业查询默认智能搜索四层主视觉自上而下排布 | pass | 3 项机检断言通过；1 项待人工 |
| P0-02 | 00439 | 点击示例查询 chip 仅回填关键词不自动检索 | pass | 2 项机检断言通过 |
| P0-03 | 00440 | 智能搜索关键词检索后得到长卡片结果与命中条数 | pass | 3 项机检断言通过 |
| P0-04 | 00443 | 点击企业名称打开当前页画像抽屉且十页签齐全 | fail | ✗ 抽屉在当前页打开且路由不变 — locator.waitFor: Timeout 8000ms exceeded. / assert: await page.locator('.arco-draw |
| P0-05 | 00456 | 综合竞争力说明卡可打开且业务可见区无内部编号泄漏 | pass | 2 项机检断言通过 |
| P0-06 | 00444 | 点击热门场景后切换高级筛选并立即得到结果 | pass | 3 项机检断言通过 |
| P0-07 | 00441 | 查企业按名称关键词检索得到长卡片结果 | pass | 3 项机检断言通过 |
| P0-08 | 00449 | 点击最近检索记录可恢复该次查询结果 | pass | 2 项机检断言通过 |
| P0-09 | 00445 | 高级筛选字段库与底部 Footer 构成齐备 | pass | 3 项机检断言通过 |
| P0-10 | 00446 | 高级筛选条件可逐项叠加并应用出结果 | fail | ✗ 应用前可见已选条件计数 — 已选条件计数未出现(文本级) / assert: const mt10 = await page.locator('main').innerText(); if (!/ |
| P0-11 | 00447 | 「企业所属地区」为全国省市区级联非死写深圳 | fail | ✗ 选项含至少两个省级名称 — locator.innerText: Timeout 30000ms exceeded. / assert: const panel = page.locator('. |
| P0-12 | 00448 | 查询方案仅保存高筛条件使用后可恢复 | fail | ✗ 方案可保存并命名 — locator.waitFor: Timeout 8000ms exceeded. / assert: await page.locator('.arco-modal:vis |
| P0-13 | 00450 | 结果区四类排序均可切换 | pass | 2 项机检断言通过 |
| P0-14 | 00458 | 结果内再筛可施加、收窄且可清除恢复 | pass | 2 项机检断言通过 |
| P0-15 | 00462 | 翻页或再筛后已勾选企业被清除 | pass | 2 项机检断言通过 |
| P0-16 | 00457 | 勾选多家企业后出现已选条且可批量加入对比 | fail | ✗ 勾选后出现已选企业计数条 — 已选计数条未出现(文本级) / assert: const mt = await page.locator('main').innerText(); if (!/已选 |
| P0-17 | 00455 | 检索与字典请求经专题 Java 门面且断链可读 | pass | 2 项机检断言通过；1 项待人工 |
| P0-18 | 00442 | 三种检索模式可切换且各自主区正确 | fail | ✗ 高级筛选下呈现字段库且无智能搜索大输入框 — expect visible 超时 8000ms / assert: await expect(page.locator('main').getByT |
| P1-01 | 00453 | 初始空态展示推荐企业分区且动作受限 | fail | ✗ 分区含推荐卡且卡上有「查看画像」 — 未见「推荐企业」分区（若为引导空态按 allow_skip 判 Pass-N/A） / assert: const section = page.locato |
| P1-02 | 00467 | 业务态显示单企推荐理由机制说明仅评审模式可见 | fail | ✗ 开启后推荐区可见推荐机制与示例数据类说明 — expect visible 超时 8000ms / assert: const ps = page.locator('button.persona- |
| P1-03 | 00476 | 零命中空态提供纠错动作且不推推荐 | pass | 2 项机检断言通过 |
| P1-04 | 00451 | 结果卡「查看画像」打开抽屉且路由不变 | fail | ✗ 默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms / assert: await expect(page.locator('.arco-drawer,  |
| P1-05 | 00469 | 单家企业加入对比后可打开对比篮浮层 | fail | ✗ 加入后有成功反馈 — 已选计数条未出现(文本级) / assert: const mt = await page.locator('main').innerText(); if (!/已选 \d+ |
| P1-07 | 00471 | 查企业模式下点击热门场景同样进入高级筛选结果 | pass | 2 项机检断言通过 |
| P1-08 | 00468 | 评审模式显示章节溯源关闭后隐藏且不改变检索结果 | pass | 2 项机检断言通过；1 项待人工 |
| P1-09 | 00472 | 结果内再筛零命中时保留结果操作区呈局部空态 | fail | ✗ 仅列表区呈局部空态 — expect visible 超时 8000ms / assert: await expect(page.getByText('未命中结果，可调整条件或切换高级筛选').f |
| P1-10 | 00459 | 结果工具条「选择区域」可打开级联选择 | fail | ✗ 展开后可见不少于一级可选项（热门城市/省/市） — expect visible 超时 8000ms / assert: const panel = page.locator('.arco-cas |
| P1-11 | 00478 | 导出当前结果创建任务后产出文件且字段可核对 | fail | ✗ 弹层字段范围含附录B七字段 — expect visible 超时 8000ms / assert: const modal = page.locator('.arco-modal').filte |
| P1-12 | 00477 | 智能搜索页可见文本无大模型能力承诺 | pass | 1 项机检断言通过 |
| P1-13 | 00463 | 查企业「热门企业」chip 点击后立即检索出结果 | fail | ✗ 页面出现查企业结果标题（立即检索，区别于示例查询仅回填） — expect visible 超时 8000ms / assert: await expect(page.getByText('查企业 |
| P1-14 | 00452 | 带高级筛选参数直入时字段库与面包屑正确 | pass | 2 项机检断言通过 |
| P1-15 | 00454 | 智能搜索结果摘要卡呈现匹配字段或兜底文案 | pass | 2 项机检断言通过 |
| P1-17 | 00464 | 字段库可收起再展开且 Footer 操作不丢失 | fail | ✗ 展开后字段标签恢复可见 — expect visible 超时 8000ms / assert: await expect(page.getByText('企业所属地区').first()).to |
| P1-18 | 00465 | 结果态「编辑高级筛选」可回到字段库且条件保留 | fail | ✗ 页面回到字段库编辑态 — expect visible 超时 8000ms / assert: await expect(page.getByText('企业所属地区').first()).toB |
| P1-19 | 00466 | 结果卡「引育候选」可加入招引候选且有反馈 | fail | ✗ 出现已加入候选类反馈或菜单项变为已在候选态 — 未见加入候选反馈或已在候选态 / assert: const bodyText = await page.locator('main, body') |
| P1-20 | 00460 | 结果区仅长卡片形态无表格卡片视图切换 | pass | 1 项机检断言通过 |
| P1-21 | 00474 | 清空最近检索后当前模式记录消失 | pass | 1 项机检断言通过 |
| P1-22 | 00479 | 单企导出产出仅含该企业的文件 | fail | ✗ 弹层导出范围为单个企业且对象数量为 1 — expect visible 超时 8000ms / assert: const modal = page.locator('.arco-modal') |
| P1-23 | 00461 | 排序方向按钮可往返切换且列表稳定 | pass | 1 项机检断言通过 |
| P1-24 | 00475 | 清除搜索框后离开结果态回到引导形态 | fail | ✗ 清除后离开结果态或结果被清空 — expect count=0 超时 5000ms / assert: const mt24 = await page.locator('main').innerT |
| P1-26 | 00470 | 切换评审模式不改变已勾选企业集合 | fail | ✗ 开关往返后已选企业计数与切换前一致 — 已选计数条与评审开关均不可见（R4 locator 缺失，见 observed） / assert: const bar = page.locator('m |
