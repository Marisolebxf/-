/**
 * E1 gold-path browser smoke against published http://111.198.38.90:50892/
 * Forbidden: localhost. Evidence only.
 */
import { chromium } from 'playwright'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const BASE = 'http://111.198.38.90:50892'
const out = __dirname

function save(name, data) {
  fs.writeFileSync(path.join(out, name), typeof data === 'string' ? data : JSON.stringify(data, null, 2), 'utf8')
}

async function main() {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] })
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'zh-CN' })
  const page = await context.newPage()
  const net = []
  page.on('response', async (res) => {
    const url = res.url()
    if (!url.includes('111.198.38.90:50892')) return
    const req = res.request()
    if (!['xhr', 'fetch'].includes(req.resourceType()) && !url.includes('/svc/') && !url.includes('/topicAsync') && !url.includes('/api/')) return
    const headers = res.headers()
    const trace = headers['x-trace-id'] || headers['x-traceid'] || headers['traceparent'] || ''
    let body = ''
    try { body = (await res.text()).slice(0, 500) } catch { body = '' }
    net.push({ method: req.method(), url, status: res.status(), trace, body })
  })

  const log = []
  const shot = async (name) => {
    await page.screenshot({ path: path.join(out, name + '.png'), fullPage: true })
    log.push({ shot: name, url: page.url() })
  }
  const safeClick = async (locator, timeout = 4000) => {
    try {
      if ((await locator.count()) && (await locator.first().isEnabled())) {
        await locator.first().click({ timeout })
        return true
      }
    } catch { return false }
    return false
  }

  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded', timeout: 60000 })
  await page.waitForTimeout(1500)
  await shot('00-login')
  const user = page.locator('input').first()
  const pass = page.locator('input[type="password"], .arco-input-password input, input').nth(1)
  if (await user.count()) {
    await user.fill('admin')
    await pass.fill('123456')
    await safeClick(page.getByRole('button', { name: /登录/ }))
    await page.waitForTimeout(2500)
  }
  await shot('01-after-login')
  log.push({ afterLogin: page.url(), title: await page.title() })

  await page.goto(BASE + '/service-portal/overview', { waitUntil: 'networkidle', timeout: 60000 })
  await page.waitForTimeout(2500)
  await shot('p1-overview')
  log.push({ p1: { url: page.url(), text: (await page.locator('body').innerText()).slice(0, 1500) } })

  const modes = ['smart', 'org', 'advanced']
  for (const mode of modes) {
    await page.goto(BASE + '/service-center/search?mode=' + mode, { waitUntil: 'networkidle', timeout: 60000 })
    await page.waitForTimeout(1500)
    const input = page.locator('textarea, input[type="search"], .arco-input, input[type="text"]').first()
    if (mode !== 'advanced' && (await input.count())) {
      await input.fill(mode === 'smart' ? '深圳 检验检测' : '检验检测')
      const searchBtn = page.getByRole('button', { name: /搜索|查询/ }).first()
      if (!(await safeClick(searchBtn))) await input.press('Enter').catch(() => {})
      await page.waitForTimeout(2500)
    }
    await shot('p2-search-' + mode)
    log.push({ p2: mode, url: page.url(), text: (await page.locator('body').innerText()).slice(0, 800) })
  }

  await page.goto(BASE + '/service/institution-judgment?workspace=field', { waitUntil: 'networkidle', timeout: 60000 })
  await page.waitForTimeout(2000)
  await shot('p3-field-config')
  await safeClick(page.getByTestId('svc-org-open-picker'))
  await page.waitForTimeout(1200)
  await shot('p3-picker')
  const firstRow = page.locator('.arco-modal, .arco-drawer').locator('button, .arco-checkbox, .arco-table-tr').first()
  if (await firstRow.count()) await firstRow.click({ force: true }).catch(() => {})
  await safeClick(page.getByRole('button', { name: /确定|加入|选择/ }))
  await page.waitForTimeout(800)
  await safeClick(page.getByTestId('svc-org-start-analysis'))
  await safeClick(page.getByRole('button', { name: /开始分析/ }))
  await page.waitForTimeout(4000)
  await shot('p3-after-start')
  log.push({ p3: { url: page.url(), text: (await page.locator('body').innerText()).slice(0, 1500) } })
  log.push({ p3ViewResultVisible: await page.getByRole('button', { name: /查看结果/ }).count() })
  if (await safeClick(page.getByRole('button', { name: /查看结果/ }))) {
    await page.waitForTimeout(3000)
    await shot('p3-wait-view-result')
  }

  for (const url of [BASE + '/service/chain-analysis?workspace=graph', BASE + '/service/institution-judgment?workspace=graph']) {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 })
    await page.waitForTimeout(2000)
    const name = url.includes('chain-analysis') ? 'p4-chain-graph' : 'p4-judgment-graph'
    await shot(name + '-config')
    await safeClick(page.getByRole('button', { name: /开始分析/ }))
    await page.waitForTimeout(4000)
    await shot(name + '-after-start')
    if (await safeClick(page.getByRole('button', { name: /查看结果/ }))) {
      await page.waitForTimeout(3000)
      await shot(name + '-result')
      const filter2 = page.locator('.arco-radio, label').filter({ hasText: /机构及主体|主体|滤镜/ })
      if (await filter2.count()) {
        await filter2.last().click({ force: true }).catch(() => {})
        await page.waitForTimeout(1500)
        await shot(name + '-filter2')
      }
    }
    log.push({ p4: url, pageUrl: page.url(), text: (await page.locator('body').innerText()).slice(0, 1200) })
  }

  await page.goto(BASE + '/service/institution-decision?workspace=attract', { waitUntil: 'networkidle', timeout: 60000 })
  await page.waitForTimeout(2000)
  await shot('p5-attract-config')
  await safeClick(page.getByRole('button', { name: /开始分析/ }))
  await page.waitForTimeout(4000)
  await shot('p5-after-start')
  if (await safeClick(page.getByRole('button', { name: /查看结果/ }))) {
    await page.waitForTimeout(3000)
    await shot('p5-wait-view-result')
  }
  log.push({ p5: { url: page.url(), text: (await page.locator('body').innerText()).slice(0, 1500) } })

  save('network.json', net)
  save('page-log.json', log)
  await browser.close()
  console.log('DONE net=', net.length, 'shots=', log.filter((x) => x.shot).length)
}

main().catch((err) => { console.error(err); process.exit(1) })
