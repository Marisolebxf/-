import { chromium } from 'playwright'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
const __dirname = path.dirname(fileURLToPath(import.meta.url))
const BASE = 'http://111.198.38.90:50892'
const net = []
async function main() {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] })
  const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'zh-CN' })).newPage()
  page.on('response', async (res) => {
    const url = res.url()
    if (!url.includes('/svc/') && !url.includes('/topicAsync') && !url.includes('/analysis/')) return
    let body = ''
    try { body = (await res.text()).slice(0, 400) } catch {}
    net.push({ method: res.request().method(), status: res.status(), url, trace: res.headers()['x-trace-id'] || '', body })
  })
  await page.goto(BASE + '/login', { waitUntil: 'domcontentloaded', timeout: 60000 })
  await page.waitForTimeout(800)
  await page.locator('input').first().fill('admin')
  await page.locator('input').nth(1).fill('123456')
  await page.getByRole('button', { name: '登录' }).click().catch(() => {})
  await page.waitForTimeout(1500)
  await page.goto(BASE + '/service/institution-judgment?workspace=field', { waitUntil: 'networkidle', timeout: 60000 })
  await page.waitForTimeout(1500)
  await page.screenshot({ path: path.join(__dirname, 'p3b-config.png'), fullPage: true })
  await page.getByRole('button', { name: '选择机构' }).click()
  await page.waitForTimeout(2000)
  await page.screenshot({ path: path.join(__dirname, 'p3b-picker.png'), fullPage: true })
  const cb = page.locator('.arco-modal .arco-checkbox, .arco-drawer .arco-checkbox').nth(1)
  if (await cb.count()) await cb.click({ force: true })
  else await page.locator('.arco-modal .arco-table-tr').nth(1).click({ force: true }).catch(() => {})
  await page.waitForTimeout(500)
  const ok = page.locator('.arco-modal, .arco-drawer').getByRole('button', { name: /确定|加入|完成/ })
  if (await ok.count()) await ok.first().click()
  await page.waitForTimeout(1000)
  await page.screenshot({ path: path.join(__dirname, 'p3b-selected.png'), fullPage: true })
  await page.getByRole('button', { name: '开始分析' }).click()
  await page.waitForTimeout(5000)
  await page.screenshot({ path: path.join(__dirname, 'p3b-after-start.png'), fullPage: true })
  const vr = page.getByRole('button', { name: '查看结果' })
  const n = await vr.count()
  if (n) {
    await vr.first().click()
    await page.waitForTimeout(4000)
    await page.screenshot({ path: path.join(__dirname, 'p3b-result.png'), fullPage: true })
  }
  const text = (await page.locator('body').innerText()).slice(0, 2000)
  fs.writeFileSync(path.join(__dirname, 'p3b-log.json'), JSON.stringify({ url: page.url(), viewResult: n, text, net }, null, 2))
  await browser.close()
  console.log('P3B url', page.url(), 'viewResult', n, 'net', net.length)
}
main().catch((e) => { console.error(e); process.exit(1) })
