import { expect, test, type Page, type Request, type Response } from '@playwright/test'
import { createHash } from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const DEMO_UPSTREAM =
  /demo-algo|demo-svc|demo-platform|demo-ui-topic|demo-ui-science|skxrules\.unicomcn/i
const SEARCH_API = /\/policy\/topic\/v1\/policy\/search(?:\?|$)/
const CLUSTERS_API = /\/topic\/v1\/meta\/industry-clusters/
const CREATE_API = /\/topicAsync\/topic\/v1\/analysis\/tasks(?:\?|$)/
const TASK_GET_API = /\/topicAsync\/topic\/v1\/analysis\/tasks\/[^/?]+(?:\?|$)/
const SHA256 = /^[a-f0-9]{64}$/
const PLAIN_FP_MSG = /analysis_fp 必须是 64 位小写 SHA-256/
const JOB_WAIT_MS = 280_000
const NOTES: Record<string, unknown>[] = []
const NOTES_PATH = path.join(__dirname, 'run-notes.json')

function note(entry: Record<string, unknown>) {
  const row = { at: new Date().toISOString(), ...entry }
  NOTES.push(row)
  let prior: Record<string, unknown>[] = []
  try {
    prior = JSON.parse(fs.readFileSync(NOTES_PATH, 'utf8')) as Record<string, unknown>[]
  } catch {
    prior = []
  }
  prior.push(row)
  fs.writeFileSync(NOTES_PATH, JSON.stringify(prior, null, 2), 'utf8')
}

function headerTrace(res: Response) {
  return res.headers()['x-trace-id'] || res.headers()['X-Trace-Id'] || ''
}

function attachGuards(page: Page) {
  const demoHits: string[] = []
  const serverErrors: string[] = []
  const traces: { url: string; status: number; trace: string; method: string }[] = []
  const createPosts: { fp?: string; body: unknown }[] = []
  const clusterResps: { status: number; trace: string; l0: string[] }[] = []
  page.on('request', (req: Request) => {
    const url = req.url()
    if (!url.includes('/api/')) return
    if (DEMO_UPSTREAM.test(url)) demoHits.push(url)
    if (req.method() === 'POST' && CREATE_API.test(url)) {
      const body = req.postDataJSON() as Record<string, unknown> | null
      const fp = String(body?.analysis_fp ?? body?.analysisFp ?? '')
      createPosts.push({ fp, body })
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
    check() {
      expect(demoHits, `D12 hit demo-*: ${demoHits.join('\n')}`).toEqual([])
    },
  }
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize)
  if (!value || typeof value !== 'object') return value
  return Object.fromEntries(
    Object.entries(value as Record<string, unknown>)
      .filter(([, item]) => item !== undefined)
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([key, item]) => [key, canonicalize(item)]),
  )
}

function sha256Fingerprint(input: unknown) {
  return createHash('sha256').update(JSON.stringify(canonicalize(input))).digest('hex')
}

async function login(page: Page) {
  await page.goto('/login')
  await expect(page.getByRole('button', { name: '登录' })).toBeVisible({ timeout: 20_000 })
  await page.getByRole('button', { name: '登录' }).click()
  await expect(page).not.toHaveURL(/\/login/, { timeout: 20_000 })
}

function startButton(page: Page) {
  return page.getByTestId('policy-start-analysis').or(page.getByRole('button', { name: '开始分析' }))
}

async function pageSnapshot(page: Page) {
  const start = startButton(page)
  return {
    url: page.url(),
    title: await page.title(),
    startCount: await start.count(),
    startEnabled: (await start.count()) ? await start.first().isEnabled() : false,
    hint: await page.getByTestId('policy-scope-hint').innerText().catch(() => ''),
    vid: await page
      .getByText(/图上 VID/)
      .first()
      .innerText()
      .catch(() => ''),
    noIndustry: await page.getByText('无相关产业数据').count(),
    noObject: await page.getByText('尚未选择分析对象').count(),
    bodyHead: (await page.locator('body').innerText().catch(() => '')).slice(0, 1200),
  }
}

async function pickArcoOption(page: Page, ariaLabel: string, prefer?: RegExp) {
  await page.getByLabel(ariaLabel, { exact: true }).click()
  const dropdown = page.locator('.arco-select-dropdown:visible').last()
  await expect(dropdown).toBeVisible({ timeout: 20_000 })
  const options = dropdown.locator('.arco-select-option:not(.arco-select-option-disabled)')
  const texts = await options.allInnerTexts().catch(() => [])
  const count = await options.count()
  if (!count) {
    await page.keyboard.press('Escape').catch(() => undefined)
    return { count: 0, texts }
  }
  if (prefer) {
    const hit = options.filter({ hasText: prefer })
    if (await hit.count()) {
      await hit.first().click()
      return { count, texts }
    }
  }
  await options.first().click()
  return { count, texts }
}

async function postCreate(
  page: Page,
  javaType: 'policy_timeseries' | 'policy_regional' | 'policy_shenzhen',
  source: string,
) {
  const fp = sha256Fingerprint({
    javaType,
    scopeKind: 'industry',
    objectKey: 'chain:INB170101',
    granularity: 'year',
    timeseriesDims: ['publish', 'effect', 'support'].sort(),
    regions: [],
    dims: [],
    weights: {},
    selectedIndicators: {},
  })
  const body = {
    user_id: 'guest',
    analysisType: javaType,
    analysis_key: javaType,
    analysis_fp: fp,
    force: true,
    client_request_id: `${javaType}:${fp}:${Date.now()}`,
    params: {
      sub_type: javaType,
      task_type: javaType,
      analysisType: javaType,
      scope_kind: 'industry',
      industry_vid: 'chain:INB170101',
      granularity: 'year',
      timeseries_dims: ['publish', 'effect', 'support'],
      analysis_fp: fp,
      viewed: false,
    },
    draft: { analysis_fp: fp },
  }
  const res = await page.request.post('/api/topicAsync/topic/v1/analysis/tasks', {
    data: body,
    headers: { 'Content-Type': 'application/json' },
  })
  const json = await res.json().catch(() => null)
  const trace = res.headers()['x-trace-id'] || res.headers()['X-Trace-Id'] || ''
  note({
    gold: `${source}-create-post`,
    source,
    http: res.status(),
    trace,
    fp,
    fpSha256: SHA256.test(fp),
    msg: json?.msg ?? json?.message ?? '',
    code: json?.code,
    plaintextGate: PLAIN_FP_MSG.test(String(json?.msg ?? json?.message ?? '')),
    bodyHead: JSON.stringify(json).slice(0, 800),
  })
  return { res, json, trace, fp }
}

async function startAnalysis(page: Page) {
  const start = startButton(page)
  const enabled = (await start.count()) ? await start.first().isEnabled() : false
  if (!enabled) {
    return {
      createStatus: 0,
      createTrace: '',
      createBody: null,
      toast: '',
      urlAfter: page.url(),
      startEnabled: false,
    }
  }
  const createWait = page.waitForResponse(
    (res) => CREATE_API.test(res.url()) && res.request().method() === 'POST' && res.status() < 500,
    { timeout: 30_000 },
  )
  await start.first().click()
  let create: Response | null = null
  let createBody: unknown = null
  try {
    create = await createWait
    createBody = await create.json().catch(() => null)
  } catch {
    /* I2-12 today-reuse may skip POST */
  }
  const toast = page.getByText(/任务已创建|正在执行|今日已分析|创建分析任务失败|请完成分析|analysis_fp|无相关产业数据|尚未选择/)
  await toast.first().waitFor({ state: 'visible', timeout: 8_000 }).catch(() => undefined)
  return {
    createStatus: create?.status() ?? 0,
    createTrace: create ? headerTrace(create) : '',
    createBody,
    toast: await toast.first().innerText().catch(() => ''),
    urlAfter: page.url(),
    startEnabled: true,
  }
}

test.describe('POLICY gold clusters retest', () => {
  test('#1 US-E7-POL-01c search', async ({ page }) => {
    const g = attachGuards(page)
    await login(page)
    await page.goto('/policy/search')
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
    }
    const after = await page.locator('body').innerText()
    expect(after).not.toMatch(/加入对比篮/)
    expect(after).not.toMatch(/深度分析/)
    g.check()
  })

  test('#2 US-E7-POL-01/05 in-page cluster→L0', async ({ page }) => {
    const g = attachGuards(page)
    await login(page)
    const clustersWait = page.waitForResponse((res) => CLUSTERS_API.test(res.url()), { timeout: 25_000 })
    await page.goto('/policy/overview')
    const clusters = await clustersWait.catch(() => null)
    const start = startButton(page)
    await expect(start.first()).toBeVisible({ timeout: 20_000 })

    let createFired = 0
    page.on('request', (req) => {
      if (req.method() === 'POST' && CREATE_API.test(req.url())) createFired += 1
    })
    await expect.soft(start.first()).toBeDisabled()
    await start.first().click({ force: true })
    await page.waitForTimeout(800)
    expect(createFired, 'empty run must not POST create').toBe(0)

    const clusterPick = await pickArcoOption(page, '集群', /新一代|半导体|集成电路|电子信息/).catch(async (err) => {
      note({ gold: '#2-cluster-pick-error', err: String(err), snap: await pageSnapshot(page) })
      return { count: 0, texts: [] as string[] }
    })
    const l0Pick = await pickArcoOption(page, '产业').catch(async (err) => {
      note({ gold: '#2-l0-pick-error', err: String(err), snap: await pageSnapshot(page) })
      return { count: 0, texts: [] as string[] }
    })
    const snap = await pageSnapshot(page)
    const l0Ids = g.clusterResps[0]?.l0 ?? []
    const shortOnly = l0Ids.length > 0 && l0Ids.every((id) => /^INB\d{4}$/.test(id))
    note({
      gold: '#2',
      clustersHttp: clusters?.status() ?? g.clusterResps[0]?.status ?? 0,
      clustersTrace: clusters ? headerTrace(clusters) : g.clusterResps[0]?.trace,
      l0Ids,
      shortOnly,
      clusterOptionCount: clusterPick.count,
      clusterOptions: clusterPick.texts.slice(0, 20),
      l0OptionCount: l0Pick.count,
      l0Options: l0Pick.texts.slice(0, 20),
      snap,
      startEnabled: snap.startEnabled,
    })
    expect(g.clusterResps[0]?.status ?? clusters?.status(), 'clusters must not be 500').not.toBe(500)
    expect.soft(l0Pick.count, 'L0 options after requireGraphVid').toBeGreaterThan(0)
    expect.soft(snap.startEnabled, 'start analysis after cluster→L0').toBeTruthy()
    expect.soft(snap.vid).toMatch(/chain:INB/)
    g.check()
  })

  test('#3 US-E7-POL-02/06 timeseries Create', async ({ page }) => {
    test.setTimeout(360_000)
    const g = attachGuards(page)
    await login(page)
    const params = new URLSearchParams({
      analysis_type: 'policy_timeseries',
      object_type: 'industry',
      draft: '1',
    })
    params.append('object_ids[]', 'INB170101')
    params.append('object_names[]', '半导体与集成电路')
    await page.goto(`/policy/overview?${params.toString()}`)
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })

    let createBefore = 0
    page.on('request', (req) => {
      if (req.method() === 'POST' && CREATE_API.test(req.url())) createBefore += 1
    })
    const year = page.getByText('年', { exact: true }).first()
    if (await year.count()) await year.click().catch(() => undefined)
    await page.waitForTimeout(800)
    expect(createBefore, 'I2-12: changing conditions must not auto-create').toBe(0)

    const snap = await pageSnapshot(page)
    const started = await startAnalysis(page)
    note({ gold: '#3-ui', snap, ...started, fps: g.createPosts.map((p) => p.fp) })

    if (!g.createPosts.length) {
      await postCreate(page, 'policy_timeseries', '#3')
    } else {
      const msg = String((started.createBody as { msg?: string } | null)?.msg ?? '')
      note({
        gold: '#3-ui-create',
        fp: g.createPosts[0]?.fp,
        fpSha256: SHA256.test(String(g.createPosts[0]?.fp ?? '')),
        plaintextGate: PLAIN_FP_MSG.test(msg),
        msg,
        trace: started.createTrace,
      })
    }

    if (started.startEnabled && /view=processing/.test(page.url())) {
      const viewBtn = page.getByRole('button', { name: '查看分析结果' })
      const failAlert = page.getByText('本次分析生成失败')
      await expect(viewBtn.or(failAlert)).toBeVisible({ timeout: JOB_WAIT_MS })
      expect(await failAlert.isVisible(), '#3 Job failed ≠ 空态').toBeFalsy()
    } else {
      expect.soft(started.startEnabled, '#3 start enabled').toBeTruthy()
    }
    g.check()
  })

  test('#4 US-E7-POL-03 regional Create', async ({ page }) => {
    test.setTimeout(360_000)
    const g = attachGuards(page)
    await login(page)
    const params = new URLSearchParams({
      analysis_type: 'policy_region_compare',
      object_type: 'industry',
      draft: '1',
    })
    params.append('object_ids[]', 'INB170101')
    params.append('object_names[]', '半导体与集成电路')
    await page.goto(`/policy/analysis?${params.toString()}`)
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })
    const snap = await pageSnapshot(page)
    const started = await startAnalysis(page)
    note({ gold: '#4-ui', snap, ...started, fps: g.createPosts.map((p) => p.fp) })
    if (!g.createPosts.length) {
      await postCreate(page, 'policy_regional', '#4')
    } else {
      const msg = String((started.createBody as { msg?: string } | null)?.msg ?? '')
      note({
        gold: '#4-ui-create',
        fp: g.createPosts[0]?.fp,
        plaintextGate: PLAIN_FP_MSG.test(msg),
        msg,
        trace: started.createTrace,
      })
    }
    expect.soft(started.startEnabled, '#4 start enabled').toBeTruthy()
    g.check()
  })

  test('#5 US-E7-POL-04 shenzhen Create', async ({ page }) => {
    test.setTimeout(360_000)
    const g = attachGuards(page)
    await login(page)
    const params = new URLSearchParams({
      analysis_type: 'policy_sz_3d',
      object_type: 'industry',
      draft: '1',
    })
    params.append('object_ids[]', 'INB170101')
    params.append('object_names[]', '半导体与集成电路')
    await page.goto(`/policy/recommendation?${params.toString()}`)
    await expect(startButton(page).first()).toBeVisible({ timeout: 20_000 })
    const weight = await page.getByText(/一级权重\s*100%/).count()
    const snap = await pageSnapshot(page)
    const started = await startAnalysis(page)
    note({ gold: '#5-ui', snap, weight100: weight > 0, ...started, fps: g.createPosts.map((p) => p.fp) })
    if (!g.createPosts.length) {
      await postCreate(page, 'policy_shenzhen', '#5')
    } else {
      const msg = String((started.createBody as { msg?: string } | null)?.msg ?? '')
      note({
        gold: '#5-ui-create',
        fp: g.createPosts[0]?.fp,
        plaintextGate: PLAIN_FP_MSG.test(msg),
        msg,
        trace: started.createTrace,
      })
    }
    expect.soft(started.startEnabled, '#5 start enabled').toBeTruthy()
    g.check()
  })
})
