/**
 * 算法库联调台会话与调用步骤。只给 run-apiview.mjs 用。
 * 口令只读环境变量，不进文件。
 */
import fs from 'node:fs';
import path from 'node:path';

// ponytail: 名称表抄自 industryCascade.js 的 CLUSTER_SEED，外加该文件里的 CATALOG_L1。
// 不在表里的 id 不猜名字，搜索失败就停。
const CHAIN_L0 = {
  INB1701: '新一代信息技术',
  INB170101: '半导体与集成电路',
  INB1702: '生物',
  INB1703: '新能源',
  INB1704: '新材料',
  INB1705: '高端装备',
  INB1706: '智能网联新能源汽车',
  INB1707: '绿色环保',
  INB1708: '低空经济与空天',
  INB1709: '传统与创意',
  INB1710: '海洋',
  INB1801: '未来制造',
  INB1802: '未来信息',
  INB1803: '未来能源',
  INB1804: '未来空间',
  INB1805: '未来健康',
};

function escapeRegExp(text) {
  return String(text).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// 搜索结果是「集群 / 产业 / 子产业」。同名时取最后一段等于目标、且路径最长的那条。
export function pickChainOptionIndex(texts, leaf) {
  let best = -1;
  let bestLen = -1;
  texts.forEach((text, i) => {
    const parts = String(text).replace(/\s+/g, '').split('/').filter(Boolean);
    if (parts.at(-1) !== leaf) return;
    if (parts.length > bestLen) {
      bestLen = parts.length;
      best = i;
    }
  });
  return best;
}

export function formatExchange({ pathLine, requestUrl, params, response }) {
  const body = String(response ?? '').trim();
  if (!body) throw new Error('response 为空，不写 exchange.txt');
  const paramText = String(params ?? '').trim();
  return [
    `path: ${String(pathLine || '').trim()}`,
    `request_url: ${requestUrl || '无'}`,
    'params:',
    paramText || '无',
    'response:',
    body,
    '',
  ].join('\n');
}

export async function ensureApiviewLogin(page) {
  const card = page.locator('.login-card');
  const workspace = page.getByRole('tab', { name: '接口信息' });
  // 联调台先打开目标 hash，路由守卫随后才切到登录页。只看地址会在卡片出现前返回。
  await Promise.race([
    card.waitFor({ state: 'visible', timeout: 15000 }),
    workspace.waitFor({ state: 'visible', timeout: 15000 }),
  ]).catch(() => {});
  if (!(await card.isVisible().catch(() => false))) return;
  const username = process.env.ALGO_LOGIN_USER;
  const password = process.env.ALGO_LOGIN_PASSWORD;
  if (!username || !password) {
    throw new Error('需要环境变量 ALGO_LOGIN_USER 与 ALGO_LOGIN_PASSWORD');
  }
  await card.locator('input').first().fill(username);
  await card.locator('input[type=password]').fill(password);
  await page.getByRole('button', { name: '进入算法库' }).click();
  await workspace.waitFor({ state: 'visible', timeout: 15000 });
}

function formItem(page, name) {
  return page.locator('.param-form .arco-form-item').filter({ hasText: `${name} ·` }).first();
}

export async function algoTab(page, target) {
  const name = target === 'api' || target === '接口信息' ? '接口信息' : '算法测试';
  await page.getByRole('tab', { name }).click();
}

export async function clickPopupOption(page, title) {
  const name = String(title).replace(/「|」/g, '');
  const popup = page.locator('.arco-trigger-popup:visible');
  const option = popup.locator('.arco-select-option').filter({
    hasText: new RegExp(`^\\s*${escapeRegExp(name)}\\s*$`),
  }).first();
  await option.scrollIntoViewIfNeeded({ timeout: 5000 });
  await option.click({ timeout: 5000 });
}

export async function algoPick(page, title) {
  const root = page.locator('.tab-endpoint-select').filter({ visible: true }).first();
  await root.locator('.arco-select-view').click();
  await clickPopupOption(page, title);
}

async function selectChain(page, item, id) {
  const box = item.locator('.chain-cascader');
  const tag = box.locator('.arco-tag').first();
  if (await tag.isVisible().catch(() => false) && (await tag.innerText()).trim() === id) return;
  const leaf = CHAIN_L0[id];
  if (!leaf) throw new Error(`级联名称表没有 ${id}，不按 id 原文去点`);
  await box.locator('.arco-select-view').click({ timeout: 5000 });
  await box.locator('.arco-select-view input').first().fill(leaf);
  const options = page.locator('.arco-trigger-popup:visible .arco-cascader-search-option');
  await options.first().waitFor({ state: 'visible', timeout: 5000 });
  const texts = await options.allInnerTexts();
  const index = pickChainOptionIndex(texts, leaf);
  if (index < 0) throw new Error(`级联搜索没有以「${leaf}」结尾的项`);
  const chosen = options.nth(index);
  await chosen.scrollIntoViewIfNeeded({ timeout: 5000 });
  const radio = chosen.locator('.arco-radio');
  if (await radio.count()) await radio.click({ timeout: 5000 });
  else await chosen.click({ timeout: 5000 });
  await box.locator('.arco-tag').filter({ hasText: id }).waitFor({ state: 'visible', timeout: 8000 });
}

async function clearChain(item) {
  const box = item.locator('.chain-cascader');
  const tag = box.locator('.arco-tag');
  if (!(await tag.count())) return;
  await box.locator('.arco-select-view').hover();
  await box.locator('.arco-select-view-clear-btn').click({ timeout: 3000 });
  await tag.first().waitFor({ state: 'hidden', timeout: 3000 });
}

async function setField(page, name, value) {
  const item = formItem(page, name);
  await item.waitFor({ state: 'visible', timeout: 8000 });
  if (name === 'chainId' || (await item.locator('.chain-cascader').count())) {
    await selectChain(page, item, String(value));
    return;
  }
  if (await item.locator('.arco-select').count()) {
    await item.locator('.arco-select-view').click();
    await clickPopupOption(page, value);
    return;
  }
  if (await item.locator('.arco-radio').count()) {
    await item.getByText(String(value), { exact: true }).click();
    return;
  }
  await item.locator('input, textarea').first().fill(String(value));
}

async function clearField(page, name) {
  const item = formItem(page, name);
  if (!(await item.count())) return;
  if (name === 'chainId' || (await item.locator('.chain-cascader').count())) {
    await clearChain(item);
    return;
  }
  const input = item.locator('input, textarea').first();
  if (await input.count()) await input.fill('');
}

export async function algoFill(page, step) {
  const set = step.set && typeof step.set === 'object' && !Array.isArray(step.set) ? step.set : {};
  const omit = Array.isArray(step.omit) ? step.omit : step.omit ? [step.omit] : [];
  for (const name of omit) await clearField(page, String(name));
  for (const [name, value] of Object.entries(set)) await setField(page, name, value);
}

async function readParamLines(page) {
  const items = page.locator('.param-form .arco-form-item');
  const n = await items.count();
  if (!n) return '无';
  const lines = [];
  for (let i = 0; i < n; i++) {
    const item = items.nth(i);
    const extra = (await item.locator('.arco-form-item-extra').innerText().catch(() => '')).trim();
    const name = extra.split('·')[0].trim();
    if (!name) continue;
    let value = '';
    const tag = item.locator('.chain-cascader .arco-tag');
    if (await tag.count()) value = (await tag.first().innerText()).trim();
    else {
      const input = item.locator('input, textarea').first();
      if (await input.count()) value = await input.inputValue().catch(() => '');
    }
    lines.push(`${name}=${value}`);
  }
  return lines.length ? lines.join('\n') : '无';
}

export async function algoRun(page, caseDir) {
  const source = (await page.locator('.test-workbench .test-source').innerText()).replace(/\s+/g, ' ').trim();
  const found = source.match(/(GET|POST|PUT|DELETE|PATCH)\s+(\S+)/);
  const method = found ? found[1] : '';
  const apiPath = found ? found[2] : '';
  const params = await readParamLines(page);
  let captured = null;
  const onResponse = (resp) => {
    if (!apiPath || !method) return;
    if (resp.request().method() !== method) return;
    if (!resp.url().includes(apiPath)) return;
    captured = resp;
  };
  page.on('response', onResponse);
  try {
    await page.locator('.test-workbench').getByRole('button', { name: '执行接口' }).click();
    const viewer = page.locator('.test-workbench .json-viewer');
    const alert = page.locator('.test-workbench .test-control-column .arco-alert');
    await Promise.race([
      viewer.waitFor({ state: 'visible', timeout: 20000 }),
      alert.first().waitFor({ state: 'visible', timeout: 20000 }),
    ]);
  } finally {
    page.off('response', onResponse);
  }
  let requestUrl = '无';
  let response = '';
  if (captured) {
    requestUrl = captured.url();
    response = await captured.text();
  } else {
    const alert = page.locator('.test-workbench .test-control-column .arco-alert');
    if (await alert.count()) response = (await alert.first().innerText()).trim();
    if (!response) {
      const viewer = page.locator('.test-workbench .json-viewer');
      if (await viewer.count()) response = (await viewer.innerText()).trim();
    }
  }
  fs.writeFileSync(path.join(caseDir, 'exchange.txt'), formatExchange({
    pathLine: found ? found[0] : source,
    requestUrl,
    params,
    response,
  }));
  await page.locator('.test-workbench .test-card').filter({ hasText: '运行结果' }).screenshot({
    path: path.join(caseDir, 'screenshots', 'result-card.png'),
  }).catch(() => {});
}

const self = process.argv[1] && process.argv[1].endsWith('apiview-session.mjs');
if (self) {
  const text = formatExchange({
    pathLine: 'GET /innov/v1/industry/market-stats',
    requestUrl: '无',
    params: 'chainId=INB1701\nstatYear=2025',
    response: '{"data":[]}',
  });
  const ok = text.startsWith('path: GET /innov/v1/industry/market-stats\n')
    && text.includes('request_url: 无\n')
    && text.includes('chainId=INB1701\nstatYear=2025\n')
    && text.includes('response:\n{"data":[]}');
  let threw = false;
  try { formatExchange({ pathLine: 'GET /x', requestUrl: '无', params: '无', response: '  ' }); }
  catch { threw = true; }
  const chainPick = pickChainOptionIndex([
    '新一代信息技术',
    '新一代信息技术 / 新一代信息技术',
    '新一代信息技术 / 新一代信息技术 / 半导体与集成电路',
  ], '新一代信息技术');
  const bioPick = pickChainOptionIndex([
    '生物产业',
    '生物产业 / 生物',
  ], '生物');
  const miss = pickChainOptionIndex(['生物产业'], '生物');
  if (!ok || !threw || chainPick !== 1 || bioPick !== 1 || miss !== -1) {
    console.error('apiview-session self-check failed');
    process.exit(1);
  }
  console.log('apiview-session ok');
}
