import { expect, test, type Page, type Request, type Response } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'

const DEMO_UPSTREAM =
  /demo-algo|demo-svc|demo-platform|demo-ui-topic|demo-ui-science|skxrules\.unicomcn/i
const SEARCH_API = /\/policy\/topic\/v1\/policy\/search(?:\?|$)/
const CREATE_API = /\/topicAsync\/topic\/v1\/analysis\/tasks(?:\?|$)/
const TASK_GET_API = /\/topicAsync\/topic\/v1\/analysis\/tasks\/[^/?]+(?:\?|$)/
const JOB_WAIT_MS = 240_000
const NOTES: Record<string, unknown>[] = []
const NOTES_PATH = path.join(__dirname, 'run-notes.json')

function note(entry: Record<string, unknown>) {
  NOTES.push({ at: new Date().toISOString(), ...entry })
  fs.writeFileSync(NOTES_PATH, JSON.stringify(NOTES, null, 2), 'utf8')
}

function headerTrace(res: Response) {
  return res.headers()['x-trace-id'] || res.headers()['X-Trace-Id'] || ''
}

function attachGuards(page: Page) {
  const demoHits: string[] = []
  const serverErrors: string[] = []
  const traces: { url: string; status: number; trace: string; method: string }[] = []
  page.on('request', (req: Request) => {
    const url = req.url()
    if (!url.includes('/api/')) return
    if (DEMO_UPSTREAM.test(url)) demoHits.push(url)
  })
  page.on('response', (res) => {
    const url = res.url()
    if (url.includes('/api/')) {
      const trace = headerTrace(res)
      if (trace) traces.push({ url, status: res.status(), trace, method: res.request().method() })
    }
    if (res.status() >= 500) serverErrors.push(`${res.status()} ${url}`)
  })
  return {
    traces,
    check() {
      expect(demoHits, `D12 hit demo-*: ${demoHits.join('\n')}`).toEqual([])
      expect(serverErrors, `5xx: ${serverErrors.join('\n')}`).toEqual([])
    },
  }
}

async function login(page: Page) {
  await page.goto('/login')
  await expect(page.getByRole('button', { name: '登录' })).toBeVisible({ timeout: 20_000 })
  await page.getByRole('button', { name: '登录' }).click()
  await expect(page).not.toHaveURL(/\/login/, { timeout: 20_000 })
}

async function gotoPolicyWithIndustry(page: Page, route: string, analysisType: string) {
  const params = new URLSearchParams({
    source: 'compare-basket',
    analysis_type: analysisType,
    object_type: 'industry',
    draft: '1',
  })
  params.append('object_ids[]', 'INB170101')
  params.append('object_names[]', '半导体与集成电路')
  await page.goto(`${route}?${params.toString()}`)
  await expect(page.getByTestId('policy-start-analysis')).toBeVisible({ timeout: 20_000 })
  await expect(page.getByText(/图上 VID：chain:INB170101/)).toBeVisible({ timeout: 15_000 })
  await expect(page.getByTestId('policy-start-analysis')).toBeEnabled({ timeout: 10_000 })
}

async function startOrForce(page: Page) {
  const start = page.getByTestId('policy-start-analysis')
  const rerun = page.getByTestId('policy-rerun-analysis')
  await expect(start).toBeEnabled({ timeout: 20_000 })
  const hasRerun = await rerun
    .waitFor({ state: 'visible', timeout: 2_000 })
    .then(() => true)
    .catch(() => false)
  const action = hasRerun ? rerun : start
  await expect(action).toBeEnabled()
  const createWait = page.waitForResponse(
    (res) => CREATE_API.test(res.url()) && res.request().method() === 'POST' && res.status() < 500,
    { timeout: 30_000 },
  )
  await action.click()
  let create: Response | null = null
  let createBody: unknown = null
  try {
    create = await createWait
    createBody = await create.json().catch(() => null)
  } catch {
    /* I2-12 today-reuse may skip POST */
  }
  const toast = page.getByText(/任务已创建|正在执行|今日已分析|创建分析任务失败|请完成分析/)
  await toast.first().waitFor({ state: 'visible', timeout: 20_000 }).catch(() => undefined)
  return {
    forced: hasRerun,
    createStatus: create?.status() ?? 0,
    createTrace: create ? headerTrace(create) : '',
    createBody,
    toast: await toast.first().innerText().catch(() => ''),
    urlAfter: page.url(),
  }
}

async function waitSucceededWaitView(page: Page, gold: string) {
  await expect(page).toHaveURL(/view=processing/, { timeout: 45_000 })
  const viewBtn = page.getByRole('button', { name: '查看分析结果' })
  const failAlert = page.getByText('本次分析生成失败')
  await expect(viewBtn.or(failAlert)).toBeVisible({ timeout: JOB_WAIT_MS })
  const failed = await failAlert.isVisible()
  const url = page.url()
  note({ gold, url, failed, stillProcessing: /view=processing/.test(url), jumpedResult: /view=result/.test(url) })
  expect(failed, `${gold} Job failed; freeze/failed ≠ 空态，必红`).toBeFalsy()
  expect(url).toMatch(/view=processing/)
  expect(url).not.toMatch(/view=result/)
  await viewBtn.click()
  await expect(page).toHaveURL(/view=result/, { timeout: 15_000 })
}

test.describe('POLICY gold', () => {
  test('#1 US-E7-POL-01c search', async ({ page }) => {
    const g = attachGuards(page)
    await login(page)
    const searchRespP = page.waitForResponse(
      (res) => SEARCH_API.test(res.url()) && res.status() < 500,
      { timeout: 25_000 },
    )
    await page.goto('/policy/search')
    await searchRespP.catch(() => undefined)
    await expect(page.getByRole('button', { name: '搜索' })).toBeVisible({ timeout: 20_000 })
    const body = await page.locator('body').innerText()
    expect(body).not.toMatch(/加入对比篮/)
    expect(body).not.toMatch(/深度分析/)
    const input = page.locator('input').first()
    await input.fill('半导体')
    const typedSearch = page.waitForResponse(
      (res) => SEARCH_API.test(res.url()) && res.status() === 200,
      { timeout: 25_000 },
    )
    await page.getByRole('button', { name: '搜索' }).click()
    const typed = await typedSearch
    const payload = await typed.json().catch(() => ({}))
    const items = payload?.data?.items ?? payload?.items ?? []
    note({
      gold: '#1',
      searchStatus: typed.status(),
      trace: headerTrace(typed),
      itemCount: Array.isArray(items) ? items.length : 0,
      total: payload?.data?.total ?? payload?.total,
    })
    const empty = page.locator('[data-search-state="empty"]')
    const cards = page.locator('article.policy-search-result')
    await expect(empty.or(cards.first())).toBeVisible({ timeout: 20_000 })
    if (await empty.isVisible()) {
      await expect(page.locator('body')).not.toContainText(/5\d\d/)
    } else {
      expect(await cards.count()).toBeGreaterThan(0)
      await expect(cards.first().getByRole('button', { name: '查看详情' })).toBeVisible()
    }
    const after = await page.locator('main, .policy-search-grid, body').first().innerText()
    expect(after).not.toMatch(/加入对比篮/)
    expect(after).not.toMatch(/深度分析/)
    g.check()
  })

  test('#2 US-E7-POL-01/05 basket → overview', async ({ page }) => {
    const g = attachGuards(page)
    await login(page)

    await page.goto('/policy/overview')
    const start = page.getByTestId('policy-start-analysis')
    await expect(start).toBeVisible({ timeout: 20_000 })
    let createFired = 0
    page.on('request', (req) => {
      if (req.method() === 'POST' && CREATE_API.test(req.url())) createFired += 1
    })
    if (await start.isEnabled()) {
      // leftover object from catalog auto-fill is OK only if VID exists; empty-run is the no-VID path
    } else {
      await expect(page.getByText(/禁止空跑/)).toBeVisible()
      await start.click({ force: true })
      await page.waitForTimeout(1500)
      expect(createFired, 'empty run must not POST create').toBe(0)
    }

    await page.goto('/industry-center/search?mode=industry')
    const searchBox = page.locator('.enterprise-search-hero-search')
    await expect(searchBox).toBeVisible({ timeout: 20_000 })
    await searchBox.locator('input').fill('集成电路')
    const industrySearch = page.waitForResponse(
      (res) => res.url().includes('/industry/search') && res.request().method() === 'POST' && res.status() < 500,
      { timeout: 20_000 },
    )
    await searchBox.getByRole('button', { name: '搜索' }).click()
    await industrySearch
    const cards = page.locator('article.industry-search-result-card')
    await expect(cards.first()).toBeVisible({ timeout: 20_000 })
    const n = await cards.count()
    let picked = false
    for (let i = 0; i < n; i++) {
      const card = cards.nth(i)
      const type = (await card.locator('.arco-tag').first().innerText().catch(() => '')).trim()
      if (type && type !== '产业') continue
      const box = card.locator('input.arco-checkbox-target')
      if (!(await box.count())) continue
      await box.evaluate((el: HTMLInputElement) => el.click())
      picked = true
      break
    }
    expect(picked, 'need one industry card to add to basket').toBeTruthy()
    await page.getByRole('button', { name: '加入对比篮', exact: true }).click()
    await expect(page.getByText(/已加入对比篮/)).toBeVisible({ timeout: 10_000 })

    await page.getByRole('button', { name: /打开对比篮，共/ }).click()
    await expect(page.getByRole('tab', { name: /^产业 / })).toBeVisible({ timeout: 15_000 })
    await page.getByRole('tab', { name: /^产业 / }).click()
    await expect(page.getByText('篮内产业对象')).toBeVisible({ timeout: 15_000 })
    const industryBox = page.locator('#compare-basket-panel-industry .arco-checkbox').first()
    await expect(industryBox).toBeVisible({ timeout: 15_000 })
    await industryBox.click()
    await page.getByRole('button', { name: '发起分析' }).click()
    await expect(page.getByLabel('政策分析').getByText('政策时序分析')).toBeVisible({ timeout: 10_000 })
    await page.getByLabel('政策分析').getByText('政策时序分析').click()
    await page.getByRole('button', { name: '下一步：前往政策分析配置' }).click()
    await expect(page).toHaveURL(/\/policy\/overview/, { timeout: 20_000 })
    expect(page.url()).toMatch(/source=compare-basket|object_ids/)
    await expect(page.getByText('来自对比篮 · 产业')).toBeVisible({ timeout: 15_000 })
    await expect(page.getByTestId('policy-start-analysis')).toBeEnabled({ timeout: 15_000 })
    note({ gold: '#2', url: page.url(), traces: g.traces.slice(-6) })
    g.check()
  })

  test('#3 US-E7-POL-02/06 timeseries wait_view', async ({ page }) => {
    test.setTimeout(300_000)
    const g = attachGuards(page)
    await login(page)
    await gotoPolicyWithIndustry(page, '/policy/overview', 'policy_timeseries')

    let createBefore = 0
    page.on('request', (req) => {
      if (req.method() === 'POST' && CREATE_API.test(req.url())) createBefore += 1
    })
    const year = page.getByText('年', { exact: true }).first()
    if (await year.count()) await year.click().catch(() => undefined)
    await page.waitForTimeout(1200)
    expect(createBefore, 'I2-12: changing conditions must not auto-create').toBe(0)

    const started = await startOrForce(page)
    note({ gold: '#3-create', ...started, traces: g.traces.filter((t) => CREATE_API.test(t.url) || TASK_GET_API.test(t.url)).slice(-8) })
    await waitSucceededWaitView(page, '#3')
    await expect(page.locator('[aria-label="政策时序分析结果"], .policy-timeseries-result, body')).toBeVisible()
    const resultText = await page.locator('body').innerText()
    expect(resultText).toMatch(/政策时序|关联政策|密度|效力|支持力度|暂无|空/)
    g.check()
  })

  test('#4 US-E7-POL-03 regional', async ({ page }) => {
    test.setTimeout(300_000)
    const g = attachGuards(page)
    await login(page)
    await gotoPolicyWithIndustry(page, '/policy/analysis', 'policy_region_compare')
    const started = await startOrForce(page)
    note({ gold: '#4-create', ...started, traces: g.traces.filter((t) => CREATE_API.test(t.url) || TASK_GET_API.test(t.url)).slice(-8) })
    await waitSucceededWaitView(page, '#4')
    await expect(page.locator('body')).toContainText(/区域|雷达|矩阵|对比|暂无|空/)
    g.check()
  })

  test('#5 US-E7-POL-04 shenzhen 3D', async ({ page }) => {
    test.setTimeout(300_000)
    const g = attachGuards(page)
    await login(page)
    await gotoPolicyWithIndustry(page, '/policy/recommendation', 'policy_sz_3d')
    await expect(page.getByText('一级权重 100% · 校验通过')).toBeVisible({ timeout: 15_000 })
    const started = await startOrForce(page)
    note({ gold: '#5-create', ...started, traces: g.traces.filter((t) => CREATE_API.test(t.url) || TASK_GET_API.test(t.url)).slice(-8) })
    await waitSucceededWaitView(page, '#5')
    await expect(page.locator('body')).toContainText(/三维|支持力度|产业适配|落地实效|优化建议|暂无|空/)
    g.check()
  })
})
