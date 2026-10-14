# COMPARISON · 20261014-50892-search-r8-runner vs 20261014-50892-keytype-r2

runner 逐条 verdict 对照基准 run（目标一致率 100%）。

| id | 基准 | runner | 一致 | 归因 |
|---|---|---|---|---|
| P0-01 | pass | pass | ✅ |  |
| P0-02 | pass | pass | ✅ |  |
| P0-03 | pass | pass | ✅ |  |
| P0-04 | pass | fail | ❌ | runner 断言失败：✗ 抽屉在当前页打开且路由不变 — locator.waitFor: Timeout 8000ms exceeded. / assert:  |
| P0-05 | pass | pass | ✅ |  |
| P0-06 | pass | pass | ✅ |  |
| P0-07 | pass | pass | ✅ |  |
| P0-08 | pass | pass | ✅ |  |
| P0-09 | pass | pass | ✅ |  |
| P0-10 | pass | fail | ❌ | runner 断言失败：✗ 应用前可见已选条件计数 — 已选条件计数未出现(文本级) / assert: const mt10 = await page.locat |
| P0-11 | pass | fail | ❌ | runner 断言失败：✗ 选项含至少两个省级名称 — locator.innerText: Timeout 30000ms exceeded. / assert: |
| P0-12 | pass | fail | ❌ | runner 断言失败：✗ 方案可保存并命名 — locator.waitFor: Timeout 8000ms exceeded. / assert: await |
| P0-13 | pass | pass | ✅ |  |
| P0-14 | pass | pass | ✅ |  |
| P0-15 | pass | pass | ✅ |  |
| P0-16 | (缺) | fail | ❌ | runner 断言失败：✗ 勾选后出现已选企业计数条 — 已选计数条未出现(文本级) / assert: const mt = await page.locator |
| P0-17 | (缺) | pass | ❌ | 基准非 pass |
| P0-18 | (缺) | fail | ❌ | runner 断言失败：✗ 高级筛选下呈现字段库且无智能搜索大输入框 — expect visible 超时 8000ms / assert: await expe |
| P1-01 | pass | fail | ❌ | runner 断言失败：✗ 分区含推荐卡且卡上有「查看画像」 — 未见「推荐企业」分区（若为引导空态按 allow_skip 判 Pass-N/A） / asser |
| P1-02 | pass | fail | ❌ | runner 断言失败：✗ 开启后推荐区可见推荐机制与示例数据类说明 — expect visible 超时 8000ms / assert: const ps = |
| P1-03 | pass | pass | ✅ |  |
| P1-04 | pass | fail | ❌ | runner 断言失败：✗ 默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms / assert: await expec |
| P1-05 | pass | fail | ❌ | runner 断言失败：✗ 加入后有成功反馈 — 已选计数条未出现(文本级) / assert: const mt = await page.locator('ma |
| P1-07 | pass | pass | ✅ |  |
| P1-08 | pass | pass | ✅ |  |
| P1-09 | pass | fail | ❌ | runner 断言失败：✗ 仅列表区呈局部空态 — expect visible 超时 8000ms / assert: await expect(page.get |
| P1-10 | (缺) | fail | ❌ | runner 断言失败：✗ 展开后可见不少于一级可选项（热门城市/省/市） — expect visible 超时 8000ms / assert: const p |
| P1-11 | (缺) | fail | ❌ | runner 断言失败：✗ 弹层字段范围含附录B七字段 — expect visible 超时 8000ms / assert: const modal = pag |
| P1-12 | (缺) | pass | ❌ | 基准非 pass |
| P1-13 | (缺) | fail | ❌ | runner 断言失败：✗ 页面出现查企业结果标题（立即检索，区别于示例查询仅回填） — expect visible 超时 8000ms / assert: aw |
| P1-14 | (缺) | pass | ❌ | 基准非 pass |
| P1-15 | (缺) | pass | ❌ | 基准非 pass |
| P1-17 | (缺) | fail | ❌ | runner 断言失败：✗ 展开后字段标签恢复可见 — expect visible 超时 8000ms / assert: await expect(page.g |
| P1-18 | (缺) | fail | ❌ | runner 断言失败：✗ 页面回到字段库编辑态 — expect visible 超时 8000ms / assert: await expect(page.ge |
| P1-19 | (缺) | fail | ❌ | runner 断言失败：✗ 出现已加入候选类反馈或菜单项变为已在候选态 — 未见加入候选反馈或已在候选态 / assert: const bodyText = aw |
| P1-20 | (缺) | pass | ❌ | 基准非 pass |
| P1-21 | (缺) | pass | ❌ | 基准非 pass |
| P1-22 | (缺) | fail | ❌ | runner 断言失败：✗ 弹层导出范围为单个企业且对象数量为 1 — expect visible 超时 8000ms / assert: const modal |
| P1-23 | (缺) | pass | ❌ | 基准非 pass |
| P1-24 | (缺) | fail | ❌ | runner 断言失败：✗ 清除后离开结果态或结果被清空 — expect count=0 超时 5000ms / assert: const mt24 = awa |
| P1-26 | (缺) | fail | ❌ | runner 断言失败：✗ 开关往返后已选企业计数与切换前一致 — 已选计数条与评审开关均不可见（R4 locator 缺失，见 observed） / asser |

**一致率：14/41**

## 不一致条目归因

### P0-04 点击企业名称打开当前页画像抽屉且十页签齐全
- runner verdict: **fail**
- actual: ✗ 抽屉在当前页打开且路由不变 — locator.waitFor: Timeout 8000ms exceeded. | assert: await page.locator('.arco-drawer').first().waitFor({ state: 'visible', timeout: 8000 }); await expect(page).toHaveURL(/e | ✗ 抽屉含企业头部且默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms | assert: await expect(page.locator('.arco-drawer'
- 失败断言: 抽屉在当前页打开且路由不变 — locator.waitFor: Timeout 8000ms exceeded. | assert: await page.locator('.arco-drawer').first().waitFor({ state: 'visible', timeout: 8000 }); await expect(page).toHaveURL(/e
- 失败断言: 抽屉含企业头部且默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms | assert: await expect(page.locator('.arco-drawer')).toContainText('工商概况'); await expect(page.locator('.arco-drawer .arco-tabs-tab
- 失败断言: 页签共十项齐全（清单见用例册附录A） — expect visible 超时 8000ms | assert: const drawer = page.locator('.arco-drawer'); for (const t of ['工商概况','主要团队','资质荣誉','知识产权','经营财务','供应链关系','关系图谱','舆情动态','

### P0-10 高级筛选条件可逐项叠加并应用出结果
- runner verdict: **fail**
- actual: ✗ 应用前可见已选条件计数 — 已选条件计数未出现(文本级) | assert: const mt10 = await page.locator('main').innerText(); if (!/已选 \d+/.test(mt10)) throw new Error('已选条件计数未出现(文本级)') | ✗ 当前条件区含所设条件之一 — 当前条件区未见所设条件 | assert: const condText = await page.getByText('当前条件').first().innerText().catch(() => page.locator('body').innerT
- 失败断言: 应用前可见已选条件计数 — 已选条件计数未出现(文本级) | assert: const mt10 = await page.locator('main').innerText(); if (!/已选 \d+/.test(mt10)) throw new Error('已选条件计数未出现(文本级)')
- 失败断言: 当前条件区含所设条件之一 — 当前条件区未见所设条件 | assert: const condText = await page.getByText('当前条件').first().innerText().catch(() => page.locator('body').innerText()); if (!co

### P0-11 「企业所属地区」为全国省市区级联非死写深圳
- runner verdict: **fail**
- actual: ✗ 选项含至少两个省级名称 — locator.innerText: Timeout 30000ms exceeded. | assert: const panel = page.locator('.arco-cascader-panel, .arco-cascader-panel-column, .arco-trigger-popup:visible .arco-cascade | ✗ 非仅深圳区县作为唯一一层 — locator.innerText: Timeout 30000ms exceeded. | assert: const panelText = await page.locat
- 失败断言: 选项含至少两个省级名称 — locator.innerText: Timeout 30000ms exceeded. | assert: const panel = page.locator('.arco-cascader-panel, .arco-cascader-panel-column, .arco-trigger-popup:visible .arco-cascade
- 失败断言: 非仅深圳区县作为唯一一层 — locator.innerText: Timeout 30000ms exceeded. | assert: const panelText = await page.locator('.arco-cascader-panel, .arco-cascader-panel-column').first().innerText(); const pro

### P0-12 查询方案仅保存高筛条件使用后可恢复
- runner verdict: **fail**
- actual: ✗ 方案可保存并命名 — locator.waitFor: Timeout 8000ms exceeded. | assert: await page.locator('.arco-modal:visible, [role=dialog]:visible').first().waitFor({ state: 'visible', timeout: 8000 }); a
- 失败断言: 方案可保存并命名 — locator.waitFor: Timeout 8000ms exceeded. | assert: await page.locator('.arco-modal:visible, [role=dialog]:visible').first().waitFor({ state: 'visible', timeout: 8000 }); a

### P0-16 勾选多家企业后出现已选条且可批量加入对比
- runner verdict: **fail**
- actual: ✗ 勾选后出现已选企业计数条 — 已选计数条未出现(文本级) | assert: const mt = await page.locator('main').innerText(); if (!/已选 \d+ 家企业/.test(mt)) throw new Error('已选计数条未出现(文本级)'); await e
- 失败断言: 勾选后出现已选企业计数条 — 已选计数条未出现(文本级) | assert: const mt = await page.locator('main').innerText(); if (!/已选 \d+ 家企业/.test(mt)) throw new Error('已选计数条未出现(文本级)'); await e

### P0-17 检索与字典请求经专题 Java 门面且断链可读
- runner verdict: **pass**
- actual: 2 项机检断言通过；1 项待人工

### P0-18 三种检索模式可切换且各自主区正确
- runner verdict: **fail**
- actual: ✗ 高级筛选下呈现字段库且无智能搜索大输入框 — expect visible 超时 8000ms | assert: await expect(page.locator('main').getByText(/企业所属地区/).first()).toBeVisible({ timeout: 8000 }); await expect(page.getByRo
- 失败断言: 高级筛选下呈现字段库且无智能搜索大输入框 — expect visible 超时 8000ms | assert: await expect(page.locator('main').getByText(/企业所属地区/).first()).toBeVisible({ timeout: 8000 }); await expect(page.getByRo

### P1-01 初始空态展示推荐企业分区且动作受限
- runner verdict: **fail**
- actual: ✗ 分区含推荐卡且卡上有「查看画像」 — 未见「推荐企业」分区（若为引导空态按 allow_skip 判 Pass-N/A） | assert: const section = page.locator('.recommend-section, [class*=recommend]').first(); const hasSection = await section.isVisib | ✗ 对比动作为加入对比或已在对比篮 — 未见加入对比或对比篮入口 | assert: const bodyText = await page.locator('body').innerText(); if (
- 失败断言: 分区含推荐卡且卡上有「查看画像」 — 未见「推荐企业」分区（若为引导空态按 allow_skip 判 Pass-N/A） | assert: const section = page.locator('.recommend-section, [class*=recommend]').first(); const hasSection = await section.isVisib
- 失败断言: 对比动作为加入对比或已在对比篮 — 未见加入对比或对比篮入口 | assert: const bodyText = await page.locator('body').innerText(); if (!bodyText.includes('加入对比') && !bodyText.includes('对比篮')) { 

### P1-02 业务态显示单企推荐理由机制说明仅评审模式可见
- runner verdict: **fail**
- actual: ✗ 开启后推荐区可见推荐机制与示例数据类说明 — expect visible 超时 8000ms | assert: const ps = page.locator('button.persona-switch'); if (!(await page.locator('.persona-menu').count())) { await ps.first()
- 失败断言: 开启后推荐区可见推荐机制与示例数据类说明 — expect visible 超时 8000ms | assert: const ps = page.locator('button.persona-switch'); if (!(await page.locator('.persona-menu').count())) { await ps.first()

### P1-04 结果卡「查看画像」打开抽屉且路由不变
- runner verdict: **fail**
- actual: ✗ 默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms | assert: await expect(page.locator('.arco-drawer, .arco-modal').filter({ hasText: '企业' }).first()).toContainText('工商概况')
- 失败断言: 默认页签为「工商概况」 — expect contains "工商概况" 超时 5000ms | assert: await expect(page.locator('.arco-drawer, .arco-modal').filter({ hasText: '企业' }).first()).toContainText('工商概况')

### P1-05 单家企业加入对比后可打开对比篮浮层
- runner verdict: **fail**
- actual: ✗ 加入后有成功反馈 — 已选计数条未出现(文本级) | assert: const mt = await page.locator('main').innerText(); if (!/已选 \d+ 家企业/.test(mt)) throw new Error('已选计数条未出现(文本级)'); await e
- 失败断言: 加入后有成功反馈 — 已选计数条未出现(文本级) | assert: const mt = await page.locator('main').innerText(); if (!/已选 \d+ 家企业/.test(mt)) throw new Error('已选计数条未出现(文本级)'); await e

### P1-09 结果内再筛零命中时保留结果操作区呈局部空态
- runner verdict: **fail**
- actual: ✗ 仅列表区呈局部空态 — expect visible 超时 8000ms | assert: await expect(page.getByText('未命中结果，可调整条件或切换高级筛选').first()).toBeVisible({ timeout: 8000 }); await expect(page.getByText('
- 失败断言: 仅列表区呈局部空态 — expect visible 超时 8000ms | assert: await expect(page.getByText('未命中结果，可调整条件或切换高级筛选').first()).toBeVisible({ timeout: 8000 }); await expect(page.getByText('

### P1-10 结果工具条「选择区域」可打开级联选择
- runner verdict: **fail**
- actual: ✗ 展开后可见不少于一级可选项（热门城市/省/市） — expect visible 超时 8000ms | assert: const panel = page.locator('.arco-cascader-panel, .arco-select-dropdown').first(); await expect(panel).toBeVisible({ tim
- 失败断言: 展开后可见不少于一级可选项（热门城市/省/市） — expect visible 超时 8000ms | assert: const panel = page.locator('.arco-cascader-panel, .arco-select-dropdown').first(); await expect(panel).toBeVisible({ tim

### P1-11 导出当前结果创建任务后产出文件且字段可核对
- runner verdict: **fail**
- actual: ✗ 弹层字段范围含附录B七字段 — expect visible 超时 8000ms | assert: const modal = page.locator('.arco-modal').filter({ hasText: '确认导出查询清单' }).first(); await expect(modal).toBeVisible({ tim
- 失败断言: 弹层字段范围含附录B七字段 — expect visible 超时 8000ms | assert: const modal = page.locator('.arco-modal').filter({ hasText: '确认导出查询清单' }).first(); await expect(modal).toBeVisible({ tim

### P1-12 智能搜索页可见文本无大模型能力承诺
- runner verdict: **pass**
- actual: 1 项机检断言通过

### P1-13 查企业「热门企业」chip 点击后立即检索出结果
- runner verdict: **fail**
- actual: ✗ 页面出现查企业结果标题（立即检索，区别于示例查询仅回填） — expect visible 超时 8000ms | assert: await expect(page.getByText('查企业结果')).toBeVisible({ timeout: 8000 }); await expect(page.getByText(/命中 \d+ 家企业/).first())
- 失败断言: 页面出现查企业结果标题（立即检索，区别于示例查询仅回填） — expect visible 超时 8000ms | assert: await expect(page.getByText('查企业结果')).toBeVisible({ timeout: 8000 }); await expect(page.getByText(/命中 \d+ 家企业/).first())

### P1-14 带高级筛选参数直入时字段库与面包屑正确
- runner verdict: **pass**
- actual: 2 项机检断言通过

### P1-15 智能搜索结果摘要卡呈现匹配字段或兜底文案
- runner verdict: **pass**
- actual: 2 项机检断言通过

### P1-17 字段库可收起再展开且 Footer 操作不丢失
- runner verdict: **fail**
- actual: ✗ 展开后字段标签恢复可见 — expect visible 超时 8000ms | assert: await expect(page.getByText('企业所属地区').first()).toBeVisible({ timeout: 8000 })
- 失败断言: 展开后字段标签恢复可见 — expect visible 超时 8000ms | assert: await expect(page.getByText('企业所属地区').first()).toBeVisible({ timeout: 8000 })

### P1-18 结果态「编辑高级筛选」可回到字段库且条件保留
- runner verdict: **fail**
- actual: ✗ 页面回到字段库编辑态 — expect visible 超时 8000ms | assert: await expect(page.getByText('企业所属地区').first()).toBeVisible({ timeout: 8000 }); await expect(page.getByRole('button', { n | ✗ 先前已选条件保留 — 回字段库后未见保留的已选条件计数 | assert: const bodyText = await page.locator('main, body').first().innerText(); if (!/已选\s*[1-9]
- 失败断言: 页面回到字段库编辑态 — expect visible 超时 8000ms | assert: await expect(page.getByText('企业所属地区').first()).toBeVisible({ timeout: 8000 }); await expect(page.getByRole('button', { n
- 失败断言: 先前已选条件保留 — 回字段库后未见保留的已选条件计数 | assert: const bodyText = await page.locator('main, body').first().innerText(); if (!/已选\s*[1-9]\d*\s*(个条件|家企业)/.test(bodyText)) 

### P1-19 结果卡「引育候选」可加入招引候选且有反馈
- runner verdict: **fail**
- actual: ✗ 出现已加入候选类反馈或菜单项变为已在候选态 — 未见加入候选反馈或已在候选态 | assert: const bodyText = await page.locator('main, body').first().innerText(); if (!/已加入|已在.*候选|已加入候选|候选/.test(bodyText)) { awai
- 失败断言: 出现已加入候选类反馈或菜单项变为已在候选态 — 未见加入候选反馈或已在候选态 | assert: const bodyText = await page.locator('main, body').first().innerText(); if (!/已加入|已在.*候选|已加入候选|候选/.test(bodyText)) { awai

### P1-20 结果区仅长卡片形态无表格卡片视图切换
- runner verdict: **pass**
- actual: 1 项机检断言通过

### P1-21 清空最近检索后当前模式记录消失
- runner verdict: **pass**
- actual: 1 项机检断言通过

### P1-22 单企导出产出仅含该企业的文件
- runner verdict: **fail**
- actual: ✗ 弹层导出范围为单个企业且对象数量为 1 — expect visible 超时 8000ms | assert: const modal = page.locator('.arco-modal').filter({ hasText: '确认导出查询清单' }).first(); await expect(modal).toBeVisible({ tim
- 失败断言: 弹层导出范围为单个企业且对象数量为 1 — expect visible 超时 8000ms | assert: const modal = page.locator('.arco-modal').filter({ hasText: '确认导出查询清单' }).first(); await expect(modal).toBeVisible({ tim

### P1-23 排序方向按钮可往返切换且列表稳定
- runner verdict: **pass**
- actual: 1 项机检断言通过

### P1-24 清除搜索框后离开结果态回到引导形态
- runner verdict: **fail**
- actual: ✗ 清除后离开结果态或结果被清空 — expect count=0 超时 5000ms | assert: const mt24 = await page.locator('main').innerText(); if (mt24.includes('智能搜索结果 命中')) throw new Error('清除后结果态仍在'); await 
- 失败断言: 清除后离开结果态或结果被清空 — expect count=0 超时 5000ms | assert: const mt24 = await page.locator('main').innerText(); if (mt24.includes('智能搜索结果 命中')) throw new Error('清除后结果态仍在'); await 

### P1-26 切换评审模式不改变已勾选企业集合
- runner verdict: **fail**
- actual: ✗ 开关往返后已选企业计数与切换前一致 — 已选计数条与评审开关均不可见（R4 locator 缺失，见 observed） | assert: const bar = page.locator('main').getByText(/已选 \d+ 家企业/).first(); const count1 = await bar.innerText().catch(() => null)
- 失败断言: 开关往返后已选企业计数与切换前一致 — 已选计数条与评审开关均不可见（R4 locator 缺失，见 observed） | assert: const bar = page.locator('main').getByText(/已选 \d+ 家企业/).first(); const count1 = await bar.innerText().catch(() => null)

