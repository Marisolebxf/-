import { expect, test, type Page, type Request, type Response } from '@playwright/test'
import fs from 'node:fs'
import path from 'node:path'

const DEMO_UPSTREAM =
  /demo-algo|demo-svc|demo-platform|demo-ui-topic|demo-ui-science|skxrules\.unicomcn/i
const SEARCH_API = /\/policy\/topic\/v1\/policy\/search(?:\?|$)/
const CLUSTERS_API = /\/topic\/v1\/meta\/industry-clusters/
const CREATE_API = /\/topicAsync\/topic\/v1\/analysis\/tasks(?:\?|$)/
const SHA256 = /^[a-f0-9]{64}$/
const PLAIN_FP_MSG = /analysis_fp 必须是 64 位小写 SHA-256/
const JOB_WAIT_MS = 240_000
const NOTES_PATH = path.join(__dirname, 'run-notes.json')
const SHOTS = path.join(__dirname, 'shots')

function loadNotes(): Record<string, unknown>[] {
  try {
    return JSON.parse(fs.readFileSync(NOTES_PATH, 'utf8')) as Record<string, unknown>[]
  } catch {
    return []
  }
}

function note(entry: Record<string, unknown>) {
  const prior = loadNotes()
  prior.push({ at: new Date().toISOString(), ...entry })
  fs.writeFileSync(NOTES_PATH, JSON.stringify(prior, null, 2), 'utf8')
}

function headerTrace(res: Response) {
  return res.headers()['x-trace-id'] || res.headers()['X-Trace-Id'] || ''
}

function startButton(page: Page) {
  return page.getByTestId('policy-start-analysis')
}

function attachGuards(page: Page) {
  const demoHits: string[] = []
  const serverErrors: string[] = []
  const traces: { url: string; status: number; trace: string; method: string }[] = []
  const createPosts: { fp?: string; body: unknown; url: string }[] = []
  const clusterResps: { status: number; trace: string; l0: string[] }[] = []
  page.on('request', (req: Request) => {
    const url = req.url()
    if (!url.includes('/api/')) return
    if (DEMO_UPSTREAM.test(url)) demoHits.push(url)
    if (req.method() === 'POST' && CREATE_API.test(url)) {
      const body = req.postDataJSON() as Record<string, unknown> | null
      const fp = String(body?.analysis_fp ?? body?.analysisFp ?? '')
      createPosts.push({ fp, body, url })
    }
  })
  page.on('response', async (res) => {
    const url = res.url()
    if (url.includes('/api/')) {
      const trace = headerTrace(res)
      if (trace) traces.push({ url, status: res.status(), trace, method: res.request().method() })
    }
    if (res.status() >= 500) serverErrors.push(`${res.status()} ${url}`)
    if (CLUSTERS_API.test(url) && res.request().method() === 'GET') {
      const payload = await res.json().catch(() => null)
      const items = payload?.data?.items ?? []
      const l0: string[] = []
      for (const item of Array.isArray(items) ? items : []) {
        for (const row of item?.l0 ?? []) l0.push(String(row.industry_id ?? ''))
      }
      clusterResps.push({ status: res.status(), trace: headerTrace(res), l0 })
    }
  })
  return {
    traces,
    createPosts,
    clusterResps,
    serverErrors,
    demoHits,
    check() {
      expect(demoHits, `D12 hit demo-*: ${demoHits.join('\n')}`).toEqual([])
    },
  }
}

async function login(page: Page) {
  await page.goto('/login', { waitUntil: 'domcontentloaded' })
  await expect(page.getByRole('button', { name: '登录' })).toBeVisible({ timeout: 20_000 })
  await page.getByRole('button', { name: '登录' }).click()
  await expect(page).not.toHaveURL(/\/login/, { timeout: 20_000 })
}

async function pageSnapshot(page: Page) {
  const start = startButton(page)
  const startCount = await start.count()
  let startEnabled = false
  if (startCount) {
    startEnabled = await start.first().isEnabled({ timeout: 3_000 }).catch(() => false)
  }
  const hint = await page.getByTestId('policy-scope-hint').innerText({ timeout: 2_000 }).catch(() => '')
  const vid = await page.locator('p.diagnosis-config-review-hint').first().innerText({ timeout: 2_000 }).catch(() => '')
  const footer = await page.locator('.diagnosis-weight-footer').innerText({ timeout: 2_000 }).catch(() => '')
  return {
    url: page.url(),
    startCount,
    startEnabled,
    hint,
    vid,
    footer,
    processing: /view=processing|demo_state=processing/.test(page.url()),
    result: /view=result|demo_state=result/.test(page.url()),
  }
}

async function shot(page: Page, name: string) {
  await page.screenshot({ path: path.join(SHOTS, `${name}.png`), fullPage: true }).catch(() => undefined)
}

async function pickSelect(page: Page, index: 0 | 1, prefer: RegExp) {
  const box = page.locator('.industry-cluster-select .arco-select').nth(index)
  await expect(box).toBeVisible({ timeout: 15_000 })
  const disabled = await box.evaluate((el) => el.className.includes('arco-select-view-disabled')).catch(() => false)
  if (disabled) return { count: 0, texts: [] as string[], picked: '', disabled: true }
  await box.click({ timeout: 8_000 })
  const dropdown = page.locator('.arco-select-dropdown:visible').last()
  await expect(dropdown).toBeVisible({ timeout: 8_000 })
  const options = dropdown.locator('.arco-select-option:not(.arco-select-option-disabled)')
  const texts = await options.allInnerTexts().catch(() => [])
  const count = await options.count()
  if (!count) {
    await page.keyboard.press('Escape').catch(() => undefined)
    return { count: 0, texts, picked: '', disabled: false }
  }
  const hit = options.filter({ hasText: prefer })
  const target = (await hit.count()) ? hit.first() : options.first()
  const picked = (await target.innerText().catch(() => '')).trim()
  await target.click({ timeout: 8_000 })
  await dropdown.waitFor({ state: 'hidden', timeout: 5_000 }).catch(() => undefined)
  return { count, texts, picked, disabled: false }
}

function industrySubmitOf(body: unknown) {
  const root = (body ?? {}) as Record<string, unknown>
  const params = (root.params ?? root) as Record<string, unknown>
  return {
    industry_id: String(params.industry_id ?? root.industry_id ?? ''),
    industry_vid: String(params.industry_vid ?? root.industry_vid ?? ''),
    fakeShortVid: String(params.industry_vid ?? '') === 'chain:INB1303',
  }
}

async function clickStartFromUi(page: Page) {
  const start = startButton(page)
  const enabled = (await start.count()) ? await start.first().isEnabled({ timeout: 3_000 }).catch(() => false) : false
  if (!enabled) {
    return {
      startEnabled: false,
      createStatus: 0,
      createTrace: '',
      createBody: null as unknown,
      toast: '',
      urlAfter: page.url(),
      clickMode: 'none',
    }
  }
  await start.first().scrollIntoViewIfNeeded().catch(() => undefined)
  await page.locator('.system-task-fab, .task-float-btn, .arco-badge').last().evaluate((el) => {
    ;(el as HTMLElement).style.pointerEvents = 'none'
  }).catch(() => undefined)
  const createWait = page.waitForResponse(
    (res) => CREATE_API.test(res.url()) && res.request().method() === 'POST',
    { timeout: 25_000 },
  )
  let clickMode = 'force'
  await start.first().click({ force: true, timeout: 8_000, position: { x: 24, y: 12 } })
  let create: Response | null = null
  let createBody: unknown = null
  const first = await Promise.race([
    createWait.then((res) => ({ kind: 'create' as const, res })).catch(() => ({ kind: 'miss' as const, res: null })),
    page.waitForURL(/view=processing|demo_state=processing/, { timeout: 8_000 }).then(() => ({ kind: 'url' as const, res: null })).catch(() => ({ kind: 'miss' as const, res: null })),
  ])
  if (first.kind === 'create') {
    create = first.res
    createBody = await create?.json().catch(() => null)
  }
  if (!create && !/view=processing|demo_state=processing/.test(page.url())) {
    clickMode = 'dom'
    await start.first().evaluate((el) => (el as HTMLButtonElement).click())
    try {
      create = await page.waitForResponse(
        (res) => CREATE_API.test(res.url()) && res.request().method() === 'POST',
        { timeout: 20_000 },
      )
      createBody = await create.json().catch(() => null)
    } catch {
      /* today-reuse may skip POST */
    }
  } else if (!create) {
    try {
      create = await createWait
      createBody = await create.json().catch(() => null)
    } catch {
      /* ignore */
    }
  }
  const toast = page.locator('.arco-message, .arco-message-wrapper').last()
  const toastText = await toast.innerText({ timeout: 4_000 }).catch(() => '')
  await page.waitForURL(/view=processing|demo_state=processing/, { timeout: 15_000 }).catch(() => undefined)
  return {
    startEnabled: true,
    createStatus: create?.status() ?? 0,
    createTrace: create ? headerTrace(create) : '',
    createBody,
    toast: toastText,
    urlAfter: page.url(),
    clickMode,
  }
}

async function waitViewThenOpenResult(page: Page, gold: string) {
  expect(
    /view=processing|demo_state=processing/.test(page.url()),
    `${gold} must be on processing before waiting Job (no proxy POST)`,
  ).toBeTruthy()
  const viewBtn = page.getByRole('button', { name: '查看分析结果' })
  const failAlert = page.getByText('本次分析生成失败')
  await expect(viewBtn.or(failAlert)).toBeVisible({ timeout: JOB_WAIT_MS })
  const failed = await failAlert.isVisible().catch(() => false)
  note({
    gold: `${gold}-wait_view`,
    url: page.url(),
    failed,
    viewBtn: await viewBtn.isVisible().catch(() => false),
    snap: await pageSnapshot(page),
  })
  expect(failed, `${gold} Job failed ≠ 空态`).toBeFalsy()
  await viewBtn.click({ timeout: 8_000 })
  await page.waitForURL(/view=result|demo_state=result/, { timeout: 20_000 })
  await shot(page, `${gold}-result`)
  return pageSnapshot(page)
}

function vidPrefillUrl(route: string, analysisType: string, industry: string) {
  const params = new URLSearchParams({
    analysis_type: analysisType,
    object_type: 'industry',
    draft: '1',
  })
  params.append('object_ids[]', industry)
  params.append('object_names[]', '半导体与集成电路')
  return `${route}?${params.toString()}`
}

test.describe('POLICY gold L0VID retest (UI only, no proxy POST PASS)', () => {
  test('#1 US-E7-POL-01c search', async ({ page }) => {
    const g = attachGuards(page)
    await login(page)
    await page.goto('/policy/search', { waitUntil: 'domcontentloaded' })
    await expect(page.getByRole('button', { name: '搜索' })).toBeVisible({ timeout: 20_000 })
    const body = await page.locator('body').innerText({ timeout: 8_000 })
    expect(body).not.toMatch(/加入对比篮/)
    expect(body).not.toMatch(/深度分析/)
    await page.locator('input').first().fill('半导体')
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
    }
    const after = await page.locator('body').innerText({ timeout: 8_000 })
    expect(after).not.toMatch(/加入对比篮/)
    expect(after).not.toMatch(/深度分析/)
    await shot(page, '01-search')
    g.check()
  })

  test('#2 US-E7-POL-01/05 in-page cluster→L0 including INB4', async ({ page }) => {
    test.setTimeout(90_000)
    const g = attachGuards(page)
    await login(page)
    const clustersWait = page.waitForResponse((res) => CLUSTERS_API.test(res.url()), { timeout: 25_000 })
    await page.goto('/policy/overview', { waitUntil: 'domcontentloaded' })
    const clusters = await clustersWait.catch(() => null)
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })
    await page.locator('.industry-cluster-select').waitFor({ timeout: 15_000 })

    let createFired = 0
    page.on('request', (req) => {
      if (req.method() === 'POST' && CREATE_API.test(req.url())) createFired += 1
    })
    await expect(startButton(page).first()).toBeDisabled()
    await startButton(page).first().click({ force: true, timeout: 5_000 }).catch(() => undefined)
    await page.waitForTimeout(400)
    expect(createFired, 'empty run must not POST create').toBe(0)

    const clusterPick = await pickSelect(page, 0, /新一代信息技术/)
    const l0Pick = await pickSelect(page, 1, /集成电路/)
    const snap = await pageSnapshot(page)
    await shot(page, '02-cluster-l0')
    const l0Ids = g.clusterResps[0]?.l0 ?? []
    const hasInb4 =
      l0Ids.includes('INB1303') ||
      /INB1303/.test(snap.vid) ||
      l0Pick.texts.some((t) => /集成电路|INB1303/.test(t))

    const started = snap.startEnabled ? await clickStartFromUi(page) : { startEnabled: false as const }
    const submit = industrySubmitOf(g.createPosts[0]?.body)
    note({
      gold: '#2',
      clustersHttp: clusters?.status() ?? g.clusterResps[0]?.status ?? 0,
      clustersTrace: clusters ? headerTrace(clusters) : g.clusterResps[0]?.trace,
      l0Ids,
      hasInb4,
      clusterPick,
      l0Pick,
      snap,
      started,
      submit,
      createFp: g.createPosts[0]?.fp,
      fpSha256: SHA256.test(String(g.createPosts[0]?.fp ?? '')),
      java4xx: (started as { createStatus?: number }).createStatus
        ? Number((started as { createStatus?: number }).createStatus) >= 400
        : false,
    })
    expect(g.clusterResps[0]?.status ?? clusters?.status(), 'clusters must not be 500').not.toBe(500)
    expect(l0Pick.disabled, 'industry select must not stay disabled').toBeFalsy()
    expect(l0Pick.count, 'INB4/map L0 must be selectable').toBeGreaterThan(0)
    expect(hasInb4, 'INB1303 / 集成电路 must appear').toBeTruthy()
    expect(snap.startEnabled, 'start analysis after cluster→L0').toBeTruthy()
    expect(submit.fakeShortVid, 'must not forge chain:INB1303').toBeFalsy()
    if (g.createPosts.length) {
      expect(submit.industry_id, 'INB4 Create must send industry_id as-is').toBe('INB1303')
      expect(submit.industry_vid).toBe('')
    }
    g.check()
  })

  test('#3 US-E7-POL-02/06 timeseries UI Create + wait_view', async ({ page }) => {
    test.setTimeout(360_000)
    const g = attachGuards(page)
    await login(page)

    await page.goto('/policy/overview?industry=INB170101', { waitUntil: 'domcontentloaded' })
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })
    const industryQuerySnap = await pageSnapshot(page)
    note({ gold: '#3-industry-query', snap: industryQuerySnap })

    await page.goto(vidPrefillUrl('/policy/overview', 'policy_timeseries', 'INB170101'), {
      waitUntil: 'domcontentloaded',
    })
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })
    await page.locator('.industry-cluster-select').waitFor({ timeout: 15_000 })

    let createBefore = 0
    page.on('request', (req) => {
      if (req.method() === 'POST' && CREATE_API.test(req.url())) createBefore += 1
    })
    await page.getByRole('radio', { name: '季' }).click({ timeout: 5_000 }).catch(() => undefined)
    await page.getByRole('radio', { name: '年' }).click({ timeout: 5_000 }).catch(() => undefined)
    await page.waitForTimeout(400)
    expect(createBefore, 'I2-12: changing conditions must not auto-create').toBe(0)

    const snap = await pageSnapshot(page)
    await shot(page, '03-vid-prefill')
    expect(snap.startEnabled, '#3 VID prefill start must be clickable even if clusterId empty').toBeTruthy()
    expect(snap.vid).toMatch(/chain:INB170101/)

    const started = await clickStartFromUi(page)
    note({
      gold: '#3-ui',
      snap,
      ...started,
      fps: g.createPosts.map((p) => p.fp),
      submit: industrySubmitOf(g.createPosts[0]?.body),
    })
    expect(started.startEnabled).toBeTruthy()
    expect(/view=processing|demo_state=processing/.test(page.url()), '#3 UI must enter processing').toBeTruthy()
    if (g.createPosts[0]?.fp) expect(String(g.createPosts[0].fp)).toMatch(SHA256)
    expect(String(started.toast ?? '')).not.toMatch(PLAIN_FP_MSG)
    await shot(page, '03-processing')
    await waitViewThenOpenResult(page, '#3')
    g.check()
  })

  test('#4 US-E7-POL-03 regional UI Create + wait_view', async ({ page }) => {
    test.setTimeout(360_000)
    const g = attachGuards(page)
    await login(page)
    await page.goto(vidPrefillUrl('/policy/analysis', 'policy_region_compare', 'INB170101'), {
      waitUntil: 'domcontentloaded',
    })
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })
    const snap = await pageSnapshot(page)
    await shot(page, '04-vid-prefill')
    expect(snap.startEnabled, '#4 VID prefill start must be clickable').toBeTruthy()
    expect(snap.vid).toMatch(/chain:INB170101/)
    const started = await clickStartFromUi(page)
    note({ gold: '#4-ui', snap, ...started, fps: g.createPosts.map((p) => p.fp) })
    expect(started.startEnabled).toBeTruthy()
    expect(/view=processing|demo_state=processing/.test(page.url()), '#4 UI must enter processing').toBeTruthy()
    await shot(page, '04-processing')
    await waitViewThenOpenResult(page, '#4')
    g.check()
  })

  test('#5 US-E7-POL-04 shenzhen UI Create + wait_view', async ({ page }) => {
    test.setTimeout(360_000)
    const g = attachGuards(page)
    await login(page)
    await page.goto(vidPrefillUrl('/policy/recommendation', 'policy_sz_3d', 'chain:INB170101'), {
      waitUntil: 'domcontentloaded',
    })
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })
    const weight = await page.locator('text=/一级权重\\s*100%/').count()
    const snap = await pageSnapshot(page)
    await shot(page, '05-vid-prefill')
    expect(snap.startEnabled, '#5 VID prefill start must be clickable').toBeTruthy()
    expect(snap.vid).toMatch(/chain:INB170101/)
    const started = await clickStartFromUi(page)
    note({ gold: '#5-ui', snap, weight100: weight > 0, ...started, fps: g.createPosts.map((p) => p.fp) })
    expect(started.startEnabled).toBeTruthy()
    expect(/view=processing|demo_state=processing/.test(page.url()), '#5 UI must enter processing').toBeTruthy()
    await shot(page, '05-processing')
    await waitViewThenOpenResult(page, '#5')
    g.check()
  })
})
