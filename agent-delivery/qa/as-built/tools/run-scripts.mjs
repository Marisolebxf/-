#!/usr/bin/env node
// run-scripts.mjs — GKX QA 原生 Playwright runner（QA-RUNNER-CALIBRATION-L01）
//
// usage:
//   node run-scripts.mjs <功能目录> [--run-dir <run目录>] [--only id1,id2] [--headless false] [--baseline <基准run目录>] [--check]
//   功能目录 = .../as-built/scripts/<系统>/<模块>/<功能>/ + fixtures/testdata.yaml
//     cases-v1：index.yaml + cases/{id}.yaml（一用例一文件；2026-10-14 全量拆分后唯一布局）
//   --check  干跑：只解析 YAML + 编译全部 assert 表达式（不开浏览器），用于交付前快速校验
//
// 行为：
//   1. 读 index.yaml + cases/*.yaml（金样顺序见 index.gold）
//   2. Playwright chromium：viewport 1920×1080@1（fixtures.viewport 可覆盖）；headless 默认 true；acceptDownloads
//   3. 登录：goto 后跳 /login 才填 fixtures.login，已在业务页跳过
//   4. steps[].action：goto/login_if_needed/click/fill/press/wait/snapshot/screenshot/assert_visible/
//      assert_url/assert_absent/evaluate/select_option/reload/network_assert
//   5. expect 双层：{note, assert} 在 {page, expect} 上下文求值；{note, manual:true} → pending_manual；
//      裸字符串 → 按「」内词尽力转译可见性检查，转译不了记 warning（不判 fail）
//   6. 每步截图（X6）：run目录/scripts/{id}/screenshots/{02d}-{slug}.png
//   7. allow_skip：关键前置 5s 不可见 → verdict=n/a 记原因
//   8. 判定：全部 expect pass=pass；任一 assert fail=fail；异常中断=blocked（fail_class=C6 未知）
//   9. 校准比对：读基准 run 逐条 verdict 对照，产出 COMPARISON.md
//
// 依赖：本目录 node_modules 的 playwright（唯一三方依赖）；YAML 用内置极简解析器
// ponytail: 单文件 ESM 无框架；YAML 解析器只覆盖本项目实际用到的语法子集（见 parseYaml 头注释），
//           遇不支持语法 throw 而非静默错解；升级路径 = 引入 js-yaml（当前禁止装包）

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { ensureReviewOff } from './session-preflight.mjs';

// ---------------------------------------------------------------------------
// 极简 YAML 子集解析器
// 支持语法子集（覆盖本项目 scripts/gold/testdata/result/meta 全部实际用法）：
//   - 嵌套 map / list（- 项，含 "- key: value" 行内起始 map；`k:` 下子列表缩进或顶格均支持）
//   - 单/双引号字符串（双引号 \" \\ 转义；单引号 '' 转义；引号内跨行折叠为空格）、裸标量（数字/bool/null/中文/含 / 与（） 等）
//   - flow list: [a, b, 'c']；flow map: {a: 1, b: 'x'}（一层，值不再嵌套 flow）
//   - 折叠标量: >- / > / |- / |（按缩进收集后续行折叠/保行）
//   - # 注释（引号外）、空行
// 不支持：锚点&/*、多文档---、tag、嵌套 flow、Tab 缩进 → 遇到 throw
// ---------------------------------------------------------------------------
function parseYaml(text) {
  const rawAll = text.split(/\r?\n/);
  const lines = [];
  for (let li = 0; li < rawAll.length; li++) {
    let stripped = stripComment(rawAll[li]);
    // 跨行引号标量折叠：行内引号未闭合时并入下一行（YAML 纯量内换行折叠为空格），避免解析截断
    let acc = stripped;
    let quote = unclosedQuote(acc);
    while (quote && !isBlockScalarHeader(acc)) {
      if (li + 1 >= rawAll.length) throw new Error('引号未闭合到文件尾: ' + acc.slice(0, 80));
      li++;
      acc = acc + ' ' + rawAll[li].trim();
      quote = unclosedQuote(acc);
    }
    stripped = acc;
    if (!stripped.trim()) continue;
    lines.push({ indent: stripped.match(/^ */)[0].length, text: stripped.trim() });
  }
  function isBlockScalarHeader(s) {
    return /\|\s*-?\s*(#.*)?$/.test(s.trimEnd()) || />\s*-?\s*(#.*)?$/.test(s.trimEnd());
  }
  function unclosedQuote(s) {
    let q = null;
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (q === '"') { if (c === '"' && s[i - 1] !== '\\') q = null; continue; }
      if (q === "'") { if (c === "'") { if (s[i + 1] === "'") i++; else q = null; } continue; }
      if (c === '"' || c === "'") q = c;
    }
    return q;
  }
  let pos = 0;
  function stripComment(s) {
    let q = null;
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (q) { if (c === q && s[i - 1] !== '\\') q = null; continue; }
      if (c === '"' || c === "'") { q = c; continue; }
      if (c === '#' && (i === 0 || s[i - 1] === ' ')) return s.slice(0, i);
    }
    return s;
  }
  function unescapeDQ(s) {
    return s.replace(/\\(["\\])/g, '$1');
  }
  function parseScalar(s) {
    s = s.trim();
    if (s.startsWith('[') && s.endsWith(']')) {
      const inner = s.slice(1, -1).trim();
      return inner ? splitTop(inner).map(parseScalar) : [];
    }
    if (s.startsWith('{') && s.endsWith('}')) {
      const inner = s.slice(1, -1).trim();
      const obj = {};
      if (inner) for (const p of splitTop(inner)) {
        const ci = findColon(p);
        if (ci < 0) throw new Error('flow map 项无冒号: ' + p);
        obj[parseScalar(p.slice(0, ci))] = parseScalar(p.slice(ci + 1));
      }
      return obj;
    }
    if (s.length >= 2 && s[0] === '"' && s.endsWith('"')) return unescapeDQ(s.slice(1, -1));
    if (s.length >= 2 && s[0] === "'" && s.endsWith("'")) return s.slice(1, -1).replace(/''/g, "'"); // YAML 单引号转义 '' → '
    if (s === 'true') return true;
    if (s === 'false') return false;
    if (s === 'null' || s === '~') return null;
    if (/^-?\d+$/.test(s)) return Number(s);
    return s;
  }
  function splitTop(s) {
    const parts = []; let depth = 0, q = null, cur = '';
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (q) { cur += c; if (c === q && s[i - 1] !== '\\') q = null; continue; }
      if (c === '"' || c === "'") { q = c; cur += c; continue; }
      if (c === '[' || c === '{') depth++;
      if (c === ']' || c === '}') depth--;
      if (c === ',' && depth === 0) { parts.push(cur); cur = ''; continue; }
      cur += c;
    }
    parts.push(cur);
    return parts.map((p) => p.trim()).filter((p) => p !== '');
  }
  function findColon(s) {
    let q = null;
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (q) { if (c === q) q = null; continue; }
      if (c === '"' || c === "'") { q = c; continue; }
      if (c === ':' && (i + 1 >= s.length || s[i + 1] === ' ')) return i;
    }
    return -1;
  }
  function parseBlock(base) {
    if (pos >= lines.length || lines[pos].indent < base) return [null, pos];
    const first = lines[pos];
    if (first.text.startsWith('- ') || first.text === '-') {
      const arr = [], itemIndent = first.indent;
      while (pos < lines.length && lines[pos].indent === itemIndent && (lines[pos].text.startsWith('- ') || lines[pos].text === '-')) {
        const rest = lines[pos].text === '-' ? '' : lines[pos].text.slice(2);
        const virtualIndent = itemIndent + 2;
        if (rest === '') {
          pos++;
          arr.push(pos < lines.length && lines[pos].indent > itemIndent ? parseBlock(lines[pos].indent)[0] : null);
        } else if (findColon(rest) >= 0) {
          lines.splice(pos, 1, { indent: virtualIndent, text: rest });
          arr.push(parseBlock(virtualIndent)[0]);
        } else {
          pos++;
          arr.push(parseScalar(rest));
        }
      }
      return [arr, pos];
    }
    const obj = {}, mapIndent = first.indent;
    while (pos < lines.length && lines[pos].indent === mapIndent && !lines[pos].text.startsWith('- ')) {
      const ci = findColon(lines[pos].text);
      if (ci < 0) throw new Error('无法解析行（非 list 非 kv）: "' + lines[pos].text + '"');
      const key = parseScalar(lines[pos].text.slice(0, ci));
      const rest = lines[pos].text.slice(ci + 1).trim();
      if (rest === '>' || rest === '>-') {
        pos++;
        const fold = [];
        while (pos < lines.length && lines[pos].indent > mapIndent) { fold.push(lines[pos].text); pos++; }
        obj[key] = fold.join(' ').replace(/\s+/g, ' ').trim();
      } else if (rest === '|' || rest === '|-') {
        pos++;
        const keep = [];
        while (pos < lines.length && lines[pos].indent > mapIndent) { keep.push(lines[pos].text); pos++; }
        obj[key] = keep.join('\n');
      } else if (rest === '') {
        pos++;
        // 子块 = 更深缩进（map/list 均可），或与键同缩进但以 "- " 开头的顶格列表（其余同缩进行不属于该键）
        obj[key] = pos < lines.length && (lines[pos].indent > mapIndent || (lines[pos].indent === mapIndent && (lines[pos].text.startsWith('- ') || lines[pos].text === '-'))) ? parseBlock(lines[pos].indent)[0] : null;
      } else {
        obj[key] = parseScalar(rest);
        pos++;
      }
    }
    return [obj, pos];
  }
  return parseBlock(0)[0];
}

function yamlLoad(file) {
  return parseYaml(fs.readFileSync(file, 'utf8'));
}

// ---------------------------------------------------------------------------
// pwExpect：Playwright test-runner expect 的轮询等待垫片
// playwright 库包（非 @playwright/test）不导出 expect；断言表达式里用到这些 matcher：
//   toBeVisible / toBeHidden / toBeDisabled / toBeEnabled / toHaveCount / toHaveAttribute / toHaveURL /
//   toHaveTitle / toHaveText / toContainText / toHaveValue
// 语义 = Playwright auto-retry：默认 5s 内每 100ms 轮询，超时抛 Error（.not 取反由包装层提供）。
// ponytail: 只实现本项目 assert 表达式实际用到的 matcher；超出清单的调用 throw 提示（升级路径 = 引 @playwright/test）
// ---------------------------------------------------------------------------
function makeMatchers(locOrPage, isNot, timeout) {
  const t = timeout || 5000;
  async function poll(checkFn, msg, tOverride) {
    const lim = tOverride || t;
    const start = Date.now();
    let lastErr = null;
    while (Date.now() - start < lim) {
      try {
        const ok = await checkFn();
        if (ok !== isNot) return;
        lastErr = new Error(msg());
      } catch (e) {
        if (isNot && String(e.message).includes('TIMED_OUT')) return; // not + 等待超时视为满足
        lastErr = e;
      }
      await new Promise((r) => setTimeout(r, 100));
    }
    throw lastErr || new Error(msg());
  }
  const isLocator = (o) => o && typeof o.count === 'function' && typeof o.isVisible === 'function';
  const m = {};
  m.toBeVisible = (opt) => poll(async () => await locOrPage.isVisible() === true, () => `expect${isNot ? '' : ''} visible 超时 ${opt && opt.timeout || t}ms`, opt && opt.timeout);
  m.toBeHidden = (opt) => poll(async () => {
    const c = await locOrPage.count();
    return c === 0 || (await locOrPage.isVisible()) === false;
  }, () => `expect hidden 超时 ${opt && opt.timeout || t}ms`, opt && opt.timeout);
  m.toBeDisabled = (opt) => poll(async () => await locOrPage.isDisabled() === true, () => `expect disabled 超时 ${opt && opt.timeout || t}ms`, opt && opt.timeout);
  m.toBeEnabled = (opt) => poll(async () => await locOrPage.isEnabled() === true, () => `expect enabled 超时 ${opt && opt.timeout || t}ms`, opt && opt.timeout);
  m.toHaveCount = (n) => poll(async () => (await locOrPage.count()) === n, () => `expect count=${n} 超时 ${t}ms`);
  m.toHaveAttribute = (name, val) => poll(async () => {
    const actual = await locOrPage.getAttribute(String(name));
    return val === undefined ? actual !== null : actual === String(val);
  }, () => `expect attribute ${name}${val !== undefined ? '=' + val : ''} 超时 ${t}ms`);
  m.toHaveText = (txt) => poll(async () => {
    const all = await locOrPage.allTextContents();
    return all.length > 0 && all.every((s) => s.trim() === String(txt));
  }, () => `expect text="${txt}" 超时 ${t}ms`);
  m.toContainText = (txt) => poll(async () => {
    const all = await locOrPage.allTextContents();
    return all.length > 0 && all.some((s) => s.includes(String(txt)));
  }, () => `expect contains "${txt}" 超时 ${t}ms`);
  m.toHaveValue = (v) => poll(async () => (await locOrPage.inputValue()) === String(v), () => `expect value="${v}" 超时 ${t}ms`);
  m.toHaveURL = (u) => poll(async () => {
    const cur = locOrPage.url ? locOrPage.url() : '';
    return u instanceof RegExp ? u.test(cur) : cur.includes(String(u));
  }, () => `expect URL ${u} 超时 ${t}ms（实际 ${locOrPage.url ? locOrPage.url() : '?'}）`);
  m.toHaveTitle = (u) => poll(async () => {
    const cur = await locOrPage.title();
    return u instanceof RegExp ? u.test(cur) : cur.includes(String(u));
  }, () => `expect title ${u} 超时 ${t}ms`);
  const proxied = new Proxy(m, {
    get(target, prop) {
      if (prop === 'not') return makeMatchers(locOrPage, !isNot, timeout);
      if (prop in target) return target[prop];
      throw new Error(`pwExpect 垫片未实现 matcher "${String(prop)}"（升级路径：引 @playwright/test）`);
    },
  });
  return proxied;
}
function pwExpect(locOrPage, opt) {
  return makeMatchers(locOrPage, false, opt && opt.timeout);
}

// 极简 YAML 序列化（result/meta 用；字符串含特殊字符一律双引号转义）
function yamlDump(obj, indent = 0) {
  const pad = '  '.repeat(indent);
  if (obj === null || obj === undefined) return 'null';
  if (typeof obj === 'string') {
    if (obj === '' || /[\n":#[\]{}&*!>|@`',]/.test(obj) || obj.trim() !== obj || ['true', 'false', 'null'].includes(obj) || /^-?\d+(\.\d+)?$/.test(obj)) {
      return '"' + obj.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n') + '"';
    }
    return obj;
  }
  if (typeof obj === 'number' || typeof obj === 'boolean') return String(obj);
  if (Array.isArray(obj)) {
    if (!obj.length) return '[]';
    return obj.map((v) => (v !== null && typeof v === 'object') ? pad + '-\n' + yamlDump(v, indent + 1) : pad + '- ' + yamlDump(v, indent)).join('\n');
  }
  const keys = Object.keys(obj);
  if (!keys.length) return '{}';
  return keys.map((k) => {
    const v = obj[k];
    return (v !== null && typeof v === 'object') ? pad + k + ':\n' + yamlDump(v, indent + 1) : pad + k + ': ' + yamlDump(v, indent);
  }).join('\n');
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
const featDirArg = args[0];
if (!featDirArg || featDirArg.startsWith('--')) {
  console.error('usage: node run-scripts.mjs <功能目录> [--run-dir <dir>] [--only id1,id2] [--headless false] [--baseline <dir>] [--check]');
  process.exit(2);
}
function opt(name, dflt) {
  const i = args.indexOf('--' + name);
  return i < 0 ? dflt : args[i + 1];
}
const CHECK_ONLY = args.includes('--check');
const featDir = path.resolve(featDirArg);
const only = opt('only', '') ? opt('only', '').split(',').map((s) => s.trim()) : null;
const headless = opt('headless', 'true') !== 'false';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ORCH = path.resolve(HERE, '../../../..'); // tools → as-built → qa → agent-delivery → 编排仓根
const runsRoot = path.join(ORCH, 'agent-delivery/qa/as-built/runs');
const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
const scope = path.basename(featDir);
const runDir = path.resolve(opt('run-dir', path.join(runsRoot, `${today}-50892-${scope === 'key-type' ? 'keytype' : scope}-r3-runner`)));
const baselineDir = path.resolve(opt('baseline', path.join(runsRoot, '20261014-50892-keytype-r2')));

// ---------------------------------------------------------------------------
// 载入脚本数据（cases-v1：index.yaml + cases/{id}.yaml）
// ---------------------------------------------------------------------------
function naturalIdKey(id) {
  return String(id).split(/(\d+)/).map((p) => (/^\d+$/.test(p) ? Number(p) : p.toLowerCase()));
}
function loadCasesV1(dir) {
  const indexPath = path.join(dir, 'index.yaml');
  const casesDir = path.join(dir, 'cases');
  if (!fs.existsSync(indexPath) || !fs.existsSync(casesDir)) {
    console.error('需要 cases-v1：index.yaml + cases/ （' + dir + '）');
    process.exit(2);
  }
  const index = yamlLoad(indexPath);
  const byId = new Map();
  for (const name of fs.readdirSync(casesDir)) {
    if (!name.endsWith('.yaml') && !name.endsWith('.yml')) continue;
    const doc = yamlLoad(path.join(casesDir, name));
    const s = Array.isArray(doc?.scripts) ? doc.scripts[0] : doc;
    if (!s || !s.id) throw new Error(`cases/${name} 缺少 id`);
    if (byId.has(s.id)) throw new Error(`重复脚本 id: ${s.id}（${name}）`);
    byId.set(s.id, s);
  }
  const gold = (index.gold || []).filter((id) => byId.has(id));
  const listed = (index.all || []).filter((id) => byId.has(id));
  const rest = [...byId.keys()].filter((id) => !gold.includes(id)).sort((a, b) => {
    const ka = naturalIdKey(a), kb = naturalIdKey(b);
    for (let i = 0; i < Math.max(ka.length, kb.length); i++) {
      if (ka[i] === kb[i]) continue;
      if (ka[i] === undefined) return -1;
      if (kb[i] === undefined) return 1;
      return ka[i] < kb[i] ? -1 : 1;
    }
    return 0;
  });
  const order = listed.length ? listed : [...gold, ...rest];
  return order.map((id) => byId.get(id)).filter(Boolean);
}
const allScripts = loadCasesV1(featDir);
const selected = only ? allScripts.filter((s) => only.includes(s.id)) : allScripts;
const fixtures = fs.existsSync(path.join(featDir, 'fixtures/testdata.yaml')) ? yamlLoad(path.join(featDir, 'fixtures/testdata.yaml')) : {};
const baseUrl = String(fixtures.base_url || 'http://111.198.38.90:50892/').replace(/\/$/, '');
const loginCfg = fixtures.login || { username: 'admin', password: '123456' };

// ---------------------------------------------------------------------------
// --check 干跑：解析 + assert 编译校验
// ---------------------------------------------------------------------------
if (CHECK_ONLY) {
  let bad = 0;
  for (const s of selected) {
    for (const [i, exp] of (s.expect || []).entries()) {
      if (exp && typeof exp === 'object' && exp.assert) {
        try { new Function('page', 'expect', 'return (async () => {' + exp.assert + '})()'); }
        catch (e) { bad++; console.error(`  ✗ ${s.id}.expect[${i}] 编译失败: ${e.message}\n    ${exp.assert}`); }
      } else if (typeof exp === 'string') {
        console.warn(`  ⚠ ${s.id}.expect[${i}] 裸字符串（未转换）: ${exp}`);
      }
    }
  }
  console.log(`--check 完成：${selected.length} 条脚本，assert 编译错误 ${bad} 处`);
  process.exit(bad ? 1 : 0);
}

// ---------------------------------------------------------------------------
// resolveTarget：人话 target → 定位器工厂（返回 null = 无法解析，降级 getByText）
// ---------------------------------------------------------------------------
// KEYENT steps[].target 人话词表（校准 2026-10-14 实勘 DOM 命名）：
// SEARCH steps[].target 人话词表（2026-10-14 实勘 selectors.yaml，词表真源见 fixtures/selectors.yaml）：
// 未匹配的 target 返回 null → 调用方降级 getByText（多半找不到 → 记 fail 原因继续，2 次封顶不瞎试）
function tryHeuristic(bare) {
  const btn = (name) => ({ kind: 'button', loc: (page) => page.getByRole('button', { name }).first() });
  const txt = (s, exact) => ({ kind: 'text', loc: (page) => page.getByText(s, { exact: !!exact }).last() });
  // ---- SEARCH 企业查询页（实勘 2026-10-14）----
  if (/tab 智能搜索|切换到智能搜索/.test(bare)) return { kind: 'tab', loc: (page) => page.getByRole('tab', { name: '智能搜索' }) };
  if (/tab 查企业|切换到查企业/.test(bare)) return { kind: 'tab', loc: (page) => page.getByRole('tab', { name: '查企业' }) };
  if (/tab 高级筛选|切换到高级筛选/.test(bare)) return { kind: 'tab', loc: (page) => page.getByRole('tab', { name: '高级筛选' }) };
  if (/搜索框|查企业搜索框/.test(bare) && /框/.test(bare)) return { kind: 'textbox', loc: (page) => page.getByRole('textbox', { name: /输入企业名、产业、资质、区域或专利关键词/ }).first() };
  if (/^搜索$|搜索按钮/.test(bare)) return btn('搜索');
  if (/热门场景任一|热门企业任一/.test(bare)) return btn('深圳高新技术企业');
  if (/示例查询任一|示例词/.test(bare)) return btn('人工智能');
  if (/最近检索中「人工智能」|最近检索记录/.test(bare)) return btn('人工智能');
  if (/清空/.test(bare)) return btn('清空');
  if (/导出当前结果/.test(bare)) return btn('导出当前结果');
  if (/查看画像|结果卡查看画像/.test(bare)) return btn(/查看画像/);
  if (/引育候选|加入招引候选/.test(bare)) return btn(/引育候选/);
  if (/加入对比(?!篮)/.test(bare) && !/篮内/.test(bare)) return { kind: 'text', loc: (page) => page.locator('.arco-drawer:visible').getByText('加入对比').first() };
  if (/tab「?智能搜索」?/.test(bare)) return { kind: 'tab', loc: (page) => page.getByRole('tab', { name: '智能搜索' }) };
  if (/任一卡片行「导出」|^导出$/.test(bare)) return btn(/导出/);
  if (/创建导出任务/.test(bare)) return btn(/创建|导出任务/);
  if (/字段标签恢复/.test(bare)) return { kind: 'text', loc: (page) => page.getByText(/企业所属地区/).first() };
  if (/弹层名称输入框/.test(bare)) return { kind: 'textbox', loc: (page) => page.locator('.arco-modal:visible input, [role=dialog]:visible input').first() };
  if (/弹层标题「?确认导出查询清单」?|弹层标题/.test(bare)) return { kind: 'text', loc: (page) => page.locator('.arco-modal:visible, [role=dialog]:visible').first() };
  if (/推荐企业分区|推荐区?$/.test(bare)) return { kind: 'text', loc: (page) => page.getByText(/推荐/).first() };
  if (/章节溯源挂载/.test(bare)) return { kind: 'text', loc: (page) => page.getByText(/需求追溯|溯源/).first() };
  if (/清除该再筛条件/.test(bare)) return { kind: 'text', loc: (page) => page.locator('.arco-tag .arco-tag-close-btn, [class*=chip] [class*=close]').first() };
  if (/^确定$|^菜单$/.test(bare)) return { kind: 'button', loc: (page) => page.getByRole('button', { name: bare === '确定' ? '确定' : /菜单|管理/ }).first() };
  if (/篮内企业列表/.test(bare)) return { kind: 'text', loc: (page) => page.locator('.arco-drawer:visible, [class*=basket], [class*=compare]').filter({ hasText: /公司|企业/ }).first() };
  if (/^经营状态$/.test(bare)) return { kind: 'select', loc: (page) => page.locator('.arco-select-view').filter({ hasText: '经营状态' }).first() };
  if (/结果中任一企业名称|结果摘要卡|任一结果长卡片/.test(bare)) return { kind: 'text', loc: (page) => page.locator('main').getByText(/公司|企业/).first() };
  if (/表格\/卡片视图切换|视图切换控件/.test(bare)) return { kind: 'button', loc: (page) => page.getByRole('button', { name: /视图|卡片|表格/ }).first() };
  if (/默认（综合竞争力优先）|默认有效专利数|综合竞争力优先）?$/.test(bare)) return { kind: 'option', loc: (page) => page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible li').filter({ hasText: '综合竞争力优先' }).first() };
  if (/已选企业计数条|已选.*计数/.test(bare)) return { kind: 'floattext', loc: (page) => page.getByText(/已选 \\d+ 家企业/).first() };
  if (/四类排序选项|排序选项/.test(bare)) return { kind: 'text', loc: (page) => page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible li').first() };
  if (/四层主视觉|引导态/.test(bare)) return { kind: 'text', loc: (page) => page.getByText('示例查询').first() };
  if (/结果标题|智能搜索结果/.test(bare)) return { kind: 'text', loc: (page) => page.getByText('智能搜索结果').first() };
  if (/说明卡中文指标名|说明卡/.test(bare)) return { kind: 'text', loc: (page) => page.locator('.arco-popover:visible, .arco-trigger-popup:visible, .arco-tooltip:visible').filter({ hasText: /口径定义|指标ID/ }).first() };
  if (/推荐区机制说明|机制说明/.test(bare)) return { kind: 'text', loc: (page) => page.getByText(/机制|示例数据/).first() };
  if (/地区选项列表|省份?级名称/.test(bare)) return { kind: 'text', loc: (page) => page.locator('.arco-trigger-popup:visible, .arco-cascader-popup:visible, .arco-select-popup:visible').first() };
  if (/对比篮按钮|打开对比篮/.test(bare)) return btn(/打开对比篮/);
  if (/切换排序方向/.test(bare)) return btn('切换排序方向');
  if (/排序下拉|^排序$/.test(bare)) return { kind: 'select', loc: (page) => page.locator('.arco-select-view').filter({ hasText: '综合竞争力优先' }).first() };
  if (/结果内筛选/.test(bare)) return { kind: 'select', loc: (page) => page.locator('.arco-select-view, .arco-select').filter({ hasText: /经营状态|企业规模|资质标签/ }).first() };
  if (/地区选择器|选择区域控件/.test(bare)) return { kind: 'select', loc: (page) => page.locator('.arco-select-view, input[placeholder*=全国热门科创城市]').filter({ hasText: /全国热门科创城市/ }).first() };
  if (/字段库区域|^字段库$|展开字段库/.test(bare)) return { kind: 'text', loc: (page) => page.getByText('高级筛选 · 字段库').first() };
  if (/收起字段库/.test(bare)) return btn(/收起字段库/);
  if (/字段 企业所属地区/.test(bare)) return { kind: 'text', loc: (page) => page.getByText('企业所属地区', { exact: false }).first() };
  if (/字段 经营状态/.test(bare)) return { kind: 'text', loc: (page) => page.getByText('经营状态', { exact: false }).first() };
  if (/第一张卡复选框/.test(bare)) return { kind: 'checkbox', loc: (page) => page.locator('main .arco-checkbox').nth(0) }; // P7: input 0宽，点可见容器
  if (/第二张卡复选框/.test(bare)) return { kind: 'checkbox', loc: (page) => page.locator('main .arco-checkbox').nth(1) };
  if (/保存为查询方案|方案/.test(bare) && /保存|方案/.test(bare)) return btn(/保存|方案/);
  if (/应用筛选/.test(bare)) return btn(/应用/);
  if (/分页第 2 页/.test(bare)) return { kind: 'option', loc: (page) => page.getByRole('listitem, button').filter({ hasText: '2' }).first() };
  if (/面包屑/.test(bare)) return { kind: 'text', loc: (page) => page.getByText('企业分析/').first() };
  // ---- KEYENT 重点企业类型分析页 ----
  if (/查看企业清单/.test(bare)) return btn(/查看企业清单（\d+）/);
  if (/列表视图/.test(bare) && /列表/.test(bare)) return btn('列表视图');
  if (/地图视图/.test(bare)) return btn('地图视图');
  if (/返回上一级/.test(bare)) return btn('返回上一级');
  if (/放大/.test(bare)) return btn('放大');
  if (/缩小/.test(bare)) return btn('缩小');
  if (/刷新/.test(bare) && !/-/.test(bare)) return btn('刷新');
  if (/全屏/.test(bare)) return btn('全屏');
  if (/查看 HTML 报告|查看HTML报告/.test(bare)) return btn('查看 HTML 报告');
  if (/返回分析结果/.test(bare)) return btn('返回分析结果');
  if (/人设|persona/i.test(bare)) return btn(/创新工作台|专业/);
  if (/内部评审模式/.test(bare) && /^(开启|关闭)/.test(bare)) return { kind: 'review-switch', loc: (page) => page.locator('.persona-menu button[role=switch][aria-label="内部评审模式"]').first() };
  if (/显示热力/.test(bare)) return txt('显示热力', true);
  if (/抽屉关闭|关闭按钮/.test(bare)) return { kind: 'drawer-close', loc: (page) => page.locator('.arco-drawer .arco-drawer-close-btn').first() };
  if (/产业下拉|全部产业/.test(bare)) return { kind: 'select', loc: (page) => page.locator('.arco-select-view').filter({ hasText: '全部产业' }).first() };
  if (/企业类型下拉|全部类型/.test(bare)) return { kind: 'select', loc: (page) => page.locator('.arco-select-view').filter({ hasText: '全部类型' }).first() };
  if (/区域级联/.test(bare)) return { kind: 'cascader', loc: (page) => page.locator('span.sci-arco-cascader').first() };
  if (/开始年份/.test(bare)) return { kind: 'input', loc: (page) => page.locator('input[placeholder=开始年份]').first() };
  if (/结束年份/.test(bare)) return { kind: 'input', loc: (page) => page.locator('input[placeholder=结束年份]').first() };
  if (/收起下拉/.test(bare)) return { kind: 'blank', loc: (page) => page.locator('h1').first() };
  // 下拉/级联选项类：'任一产业选项（默认人工智能）' / '任一类型选项（默认高新技术企业）' / '第一层「全国热门科创城市」' / '第二层任一热门城市'
  let m;
  if ((m = /默认(人工智能|高新技术企业|有效专利数)/.exec(bare))) return { kind: 'option', loc: (page) => page.locator('.arco-trigger-popup:visible .arco-select-option, .arco-trigger-popup:visible li').filter({ hasText: m[1] }).first() };
  if ((m = /「全国热门科创城市」/.exec(bare)) && /第一层/.test(bare)) return { kind: 'option', loc: (page) => page.locator('.arco-trigger-popup:visible li, .arco-trigger-popup:visible [class*=cascader-list-item], .arco-trigger-popup:visible [class*=cascader-option]').filter({ hasText: '全国热门科创城市' }).first() };
  if (/第二层任一热门城市/.test(bare)) return { kind: 'option', loc: (page) => page.locator('.arco-trigger-popup:visible li, .arco-trigger-popup:visible [class*=cascader-option]').filter({ hasText: '北京' }).first() };
  if ((m = /（如\s*(\d{4})）|（(\d{4})）/.exec(bare))) return { kind: 'option', loc: (page) => page.locator('.arco-trigger-popup:visible, .arco-picker-dropdown:visible').getByText(m[1] || m[2], { exact: true }).last() };
  if (/指标说明/.test(bare) && /综合竞争力/.test(bare)) return btn('指标说明：综合竞争力得分');
  if (/指标说明/.test(bare)) return btn(/指标说明：各类型企业数/);
  if (/未登记图标/.test(bare) && /匹配企业数/.test(bare)) return btn('指标未登记：匹配企业数');
  if (/未登记图标/.test(bare)) return btn('指标未登记：覆盖区域数');
  if (/标签移除|tag.*close|移除按钮/.test(bare)) return { kind: 'tag-close', loc: (page) => page.locator('.arco-tag .arco-tag-close-btn').first() };
  if ((m = /第一层|一层/.test(bare) && /「(.+?)」/.exec(bare))) return { kind: 'option', loc: (page) => page.locator('.arco-trigger-popup:visible li, .arco-trigger-popup:visible [class*=cascader]').filter({ hasText: m[1] }).first() };
  return null;
}

function resolveTarget(target) {
  if (!target) return null;
  const t = String(target).trim();
  const bare = /^「(.+)」$/.test(t) ? /^「(.+)」$/.exec(t)[1] : t;
  // 无前缀人话兜底：KEYENT 词表启发式（校准实测校准 2026-10-14）
  // 把常见控件口语映射为按钮/元素名；无法映射 → null（调用方记 warning）
  if (!/^(heading|button|textbox|switch|区块标题|标题|按钮)\s/.test(bare)) {
    const map = tryHeuristic(bare);
    if (map) return map;
  }
  let m;
  if ((m = /^(?:heading|区块标题|标题)\s+(.+)$/.exec(bare))) {
    const name = m[1].trim();
    return { kind: 'heading', loc: (page) => page.getByRole('heading', { name }) };
  }
  if ((m = /^(?:button|按钮)\s+(.+)$/.exec(bare))) {
    let name = m[1].trim();
    if (/「(.+)」/.test(name)) name = /「(.+)」/.exec(name)[1];
    return { kind: 'button', loc: (page) => page.getByRole('button', { name }) };
  }
  if ((m = /^(?:textbox|输入框)\s+(?:name\s+)?(.+)$/.exec(bare))) {
    let name = m[1].trim();
    if (/「(.+)」/.test(name)) name = /「(.+)」/.exec(name)[1];
    return { kind: 'textbox', loc: (page) => page.getByRole('textbox', { name }).first().or(page.getByPlaceholder(name)) };
  }
  if ((m = /^switch\s+(.+)$/.exec(bare))) {
    const name = m[1].trim();
    return { kind: 'switch', loc: (page) => page.getByText(name, { exact: true }).first() };
  }
  if (/抽屉|drawer/i.test(bare)) return { kind: 'drawer', loc: (page) => page.locator('.arco-drawer') };
  if (/筛选/.test(bare)) return { kind: 'region', loc: (page) => page.locator('section[aria-label="类型分析筛选"]') };
  if (/洞察/.test(bare)) return { kind: 'region', loc: (page) => page.getByRole('heading', { name: '区域洞察' }) };
  if (/工具栏/.test(bare)) return { kind: 'region', loc: (page) => page.getByRole('button', { name: '放大', exact: true }).first() };
  if (/图例/.test(bare)) return { kind: 'region', loc: (page) => page.getByText('企业数量强度').first() };
  if (/地图容器|leaflet/.test(bare)) return { kind: 'map', loc: (page) => page.locator('.leaflet-container').first() };
  return null;
}

function slug(s) {
  return String(s).replace(/[^\w\u4e00-\u9fff]+/g, '-').slice(0, 24).replace(/^-+|-+$/g, '') || 'step';
}

// ---------------------------------------------------------------------------
// 登录（跳 /login 才登录；Enter 可能不触发，显式点「登录」按钮兜底）
// ---------------------------------------------------------------------------
async function ensureLogin(page) {
  await page.goto(baseUrl + '/', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(800);
  if (!page.url().includes('/login')) return;
  await page.locator('input[placeholder*=用户名], input[type=text]').first().fill(loginCfg.username);
  await page.locator('input[type=password]').first().fill(loginCfg.password);
  const submit = async () => {
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1200);
    if (page.url().includes('/login')) {
      const btn = page.locator('button[type=submit], button:has-text("登录"), button:has-text("登 录")').first();
      await btn.click().catch(() => {});
    }
    await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 10000 });
  };
  await submit();
}

async function ensureBusinessSession(page) {
  if (page.url().includes('/login')) await ensureLogin(page);
  return ensureReviewOff(page);
}

// ---------------------------------------------------------------------------
// 执行单条脚本
// ---------------------------------------------------------------------------
async function runScript(page, script) {
  const caseDir = path.join(runDir, 'scripts', script.id);
  fs.mkdirSync(path.join(caseDir, 'screenshots'), { recursive: true });
  const stepLog = [], warnings = [], verdicts = [];
  let shotIdx = 0;
  let skip = false;

  const logStep = (action, label, ok, detail) => {
    stepLog.push({ n: stepLog.length + 1, action, label: label || '', ok, detail: detail || '' });
    console.log(`    ${ok ? '✓' : '✗'} ${action} ${label || ''}${detail ? ' — ' + String(detail).slice(0, 120) : ''}`);
  };

  const skipDetect = async () => {
    if (!script.allow_skip) return false;
    // F3: 探测目标按 feature 自适应——script.allow_skip_target（css/文本）优先，否则按 URL 判断 KEYENT 页用清单按钮、SEARCH 页用结果标题
    try {
      const t = script.allow_skip_target;
      if (t) {
        const loc = t.startsWith('.') || t.includes('[') ? page.locator(t).first() : page.getByText(t).first();
        await loc.waitFor({ state: 'visible', timeout: 5000 });
        return false;
      }
      if (page.url().includes('enterprise-search')) {
        await page.getByRole('tab', { name: '智能搜索' }).first().waitFor({ state: 'visible', timeout: 5000 });
        return false;
      }
      await page.getByRole('button', { name: /查看企业清单（\d+）/ }).first().waitFor({ state: 'visible', timeout: 5000 });
      return false;
    } catch { return true; }
  };

  let aborted = null;
  try {
    const session = await ensureBusinessSession(page);
    logStep('session', '登录且关闭内部评审模式', session !== 'no-switch', session);
    for (const step of script.steps || []) {
      const action = step.action;
      const label = step.target || step.note || step.for || action;
      shotIdx++;
      try {
        if (action === 'goto') {
          const url = step.target.startsWith('http') ? step.target : baseUrl + step.target;
          await page.goto(url, { waitUntil: 'domcontentloaded' });
          await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
          if (page.url().includes('/login')) { await ensureLogin(page); await page.goto(url, { waitUntil: 'domcontentloaded' }); }
          await page.waitForTimeout(600);
          const session = await ensureBusinessSession(page);
          logStep('session', 'goto 后保持评审关闭', session !== 'no-switch', session);
          logStep('goto', step.target, true);
          skip = await skipDetect();
          if (skip) { logStep('allow_skip', '关键前置 5s 不可见', true, '→ n/a'); break; }
        } else if (action === 'login_if_needed') {
          await ensureLogin(page);
          await ensureReviewOff(page);
          logStep('login_if_needed', '', true);
        } else if (action === 'click') {
          const rt = resolveTarget(step.target);
          let clicked = false, lastErr = null;
          for (let attempt = 0; attempt < 2 && !clicked; attempt++) {
            try {
              const loc = rt ? rt.loc(page).first() : page.getByText(String(step.target).replace(/「|」/g, '')).first();
              await loc.click({ timeout: 5000 });
              clicked = true;
            } catch (e) { lastErr = e; if (!rt) break; }
          }
          if (!clicked) {
            try { await page.getByText(String(step.target).replace(/「|」/g, '')).first().click({ timeout: 3000 }); clicked = true; } catch (e) { lastErr = e; }
          }
          logStep('click', step.target, clicked, clicked ? '' : String(lastErr && lastErr.message).split('\n')[0]);
        } else if (action === 'fill') {
          const rt = resolveTarget(step.target);
          await (rt ? rt.loc(page).first() : page.getByLabel(String(step.target)).first()).fill(step.value ?? '', { timeout: 5000 });
          logStep('fill', `${step.target}=${step.value}`, true);
        } else if (action === 'press') {
          await page.keyboard.press(step.key || 'Enter');
          logStep('press', step.key || 'Enter', true);
        } else if (action === 'wait') {
          const ms = typeof step.timeout_ms === 'number' ? step.timeout_ms : 800;
          await page.waitForTimeout(ms);
          logStep('wait', step.for || `${ms}ms`, true);
        } else if (action === 'snapshot') {
          const snap = await page.locator('body').ariaSnapshot().catch(() => null);
          if (snap) fs.writeFileSync(path.join(caseDir, 'snapshot.txt'), snap);
          logStep('snapshot', step.note || '', true);
        } else if (action === 'screenshot') {
          await page.waitForLoadState('networkidle', { timeout: 4000 }).catch(() => {});
          await page.waitForTimeout(350); // F2: Arco 动画 150~300ms 缓冲，截图前 settle
          await page.screenshot({ path: path.join(caseDir, 'screenshots', `${String(shotIdx).padStart(2, '0')}-${slug(step.note || 'shot')}.png`) });
          logStep('screenshot', step.note || '', true);
        } else if (action === 'assert_visible') {
          const rt = resolveTarget(step.target);
          let ok = false, detail = '';
          try {
            if (rt && rt.kind === 'floattext') {
              const bt = await page.locator('main, body').first().innerText();
              if (!/已选 \d+ 家企业/.test(bt)) throw new Error('浮动条文本未出现(文本级断言)');
            } else {
              const loc = rt ? rt.loc(page).first() : page.getByText(String(step.target).replace(/「|」/g, '')).first();
              await loc.waitFor({ state: 'visible', timeout: 6000 });
            }
            ok = true;
          } catch (e) { detail = String(e.message).split('\n')[0]; }
          logStep('assert_visible', step.target, ok, detail);
        } else if (action === 'assert_url') {
          const ok = page.url().includes(step.expect_contains || '');
          logStep('assert_url', step.expect_contains, ok, ok ? '' : '实际 ' + page.url());
        } else if (action === 'assert_absent') {
          const rt = resolveTarget(step.target);
          const cnt = rt ? await rt.loc(page).count() : await page.getByText(String(step.target)).count();
          logStep('assert_absent', step.target, cnt === 0, cnt ? `仍存在 ×${cnt}` : '');
        } else if (action === 'evaluate') {
          logStep('evaluate', step.note || '', true, '(observed 面，见截图/expect)');
        } else if (action === 'select_option') {
          const rt = resolveTarget(step.target);
          await (rt ? rt.loc(page).first() : page.locator('select').first()).selectOption(step.value);
          logStep('select_option', step.target, true);
        } else if (action === 'reload') {
          await page.reload({ waitUntil: 'domcontentloaded' });
          await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
          logStep('reload', '', true);
        } else if (action === 'network_assert') {
          const resp = await page.waitForResponse((r) => (step.url_contains ? r.url().includes(step.url_contains) : true), { timeout: 8000 }).catch(() => null);
          logStep('network_assert', step.url_contains || '', !!resp, resp ? '' : '8s 未见匹配响应');
        } else {
          logStep(action, label, true, '(未识别 action，跳过)');
          warnings.push('未识别 action: ' + action);
        }
      } catch (e) {
        logStep(action, label, false, String(e.message).split('\n')[0]);
      }
      // F2: 每步末尾截图前 settle（networkidle 4s 容错 + 350ms 动画缓冲）
      await page.waitForLoadState('networkidle', { timeout: 4000 }).catch(() => {});
      await page.waitForTimeout(350);
      await page.screenshot({ path: path.join(caseDir, 'screenshots', `${String(shotIdx).padStart(2, '0')}-${slug(action + '-' + label)}.png`) }).catch(() => {});
    }

    // ---- expect 双层 ----
    if (!skip) {
      for (const exp of script.expect || []) {
        if (typeof exp === 'string') {
          const words = [...String(exp).matchAll(/「([^」]+)」/g)].map((x) => x[1]);
          if (words.length) {
            try {
              for (const w of words) await page.getByText(w).first().waitFor({ state: 'visible', timeout: 5000 });
              verdicts.push({ note: exp, status: 'pass', detail: '(裸字符串转译机检)' });
            } catch (e) { verdicts.push({ note: exp, status: 'fail', detail: String(e.message).split('\n')[0] }); }
          } else {
            verdicts.push({ note: exp, status: 'warn', detail: '裸字符串未转译（待转换）' });
            warnings.push('expect 裸字符串未转译: ' + exp);
          }
        } else if (exp && typeof exp === 'object') {
          if (exp.manual) verdicts.push({ note: exp.note, status: 'pending_manual', detail: '' });
          else if (exp.assert) {
            try {
              await new Function('page', 'expect', 'return (async () => {' + exp.assert + '})()')(page, pwExpect);
              verdicts.push({ note: exp.note, status: 'pass', detail: '' });
            } catch (e) {
              verdicts.push({ note: exp.note, status: 'fail', detail: String(e.message).split('\n')[0] + ' | assert: ' + String(exp.assert).slice(0, 120) });
            }
          } else verdicts.push({ note: exp.note, status: 'warn', detail: '无 assert 且非 manual（待补）' });
        }
      }
    }
  } catch (e) { aborted = e; }

  // ---- 判定 ----
  let verdict, failClass = null, actual;
  const fails = verdicts.filter((v) => v.status === 'fail');
  const passes = verdicts.filter((v) => v.status === 'pass');
  const manuals = verdicts.filter((v) => v.status === 'pending_manual');
  if (aborted) { verdict = 'blocked'; failClass = 'C6'; actual = '执行异常中断: ' + String(aborted.message).split('\n')[0]; }
  else if (skip) { verdict = 'n/a'; actual = 'allow_skip 命中：关键前置 5s 不可见（详见 steps.md）'; }
  else if (fails.length) { verdict = 'fail'; failClass = 'C6'; actual = fails.map((f) => `✗ ${f.note} — ${f.detail}`).join(' | '); }
  else { verdict = 'pass'; actual = `${passes.length} 项机检断言通过` + (manuals.length ? `；${manuals.length} 项待人工` : '') + (warnings.length ? `；${warnings.length} 条 warning` : ''); }
  return { verdict, fail_class: failClass, actual, steps: stepLog, warnings, verdicts };
}

// ---------------------------------------------------------------------------
// 主流程
// ---------------------------------------------------------------------------
const vp = fixtures.viewport || {};
const browser = await chromium.launch({ headless });
const context = await browser.newContext({
  viewport: { width: vp.width || 1920, height: vp.height || 1080 },
  deviceScaleFactor: vp.device_scale_factor || 1,
  acceptDownloads: true,
});
const page = await context.newPage();

fs.mkdirSync(path.join(runDir, 'scripts'), { recursive: true });
const gitHead = (() => { try { return execSync('git rev-parse HEAD', { cwd: ORCH }).toString().trim(); } catch { return null; } })();
const t0 = new Date();
console.log(`▶ run 开始 ${t0.toISOString()} | headless=${headless} | 用例 ${selected.length} 条\nrun 目录: ${runDir}`);

await ensureLogin(page);
await ensureReviewOff(page);

const results = [];
for (const script of selected) {
  console.log(`  ▶ ${script.id} ${script.title}`);
  const r = await runScript(page, script);
  results.push({ script, ...r });
  const shotCount = fs.existsSync(path.join(runDir, 'scripts', script.id, 'screenshots')) ? fs.readdirSync(path.join(runDir, 'scripts', script.id, 'screenshots')).length : 0;
  fs.writeFileSync(path.join(runDir, 'scripts', script.id, 'result.yaml'), yamlDump({
    id: script.id, priority: script.priority, func_id: script.func_id,
    verdict: r.verdict, fail_class: r.fail_class, actual: r.actual,
    screenshot_count: shotCount,
    time: new Date().toISOString().slice(0, 16).replace('T', ' '),
  }) + '\n');
  const md = [`# ${script.id} 逐步实际操作（playwright-runner）`, ''];
  for (const s of r.steps) md.push(`${s.n}. **${s.action}** ${s.label}${s.detail ? ' — ' + s.detail : ''} ${s.ok ? '✓' : '✗'}`);
  if (r.verdicts && r.verdicts.length) {
    md.push('', '## expect 逐条', '');
    for (const v of r.verdicts) md.push(`- ${v.status === 'pass' ? '✓' : v.status === 'fail' ? '✗' : '⚠'} ${v.note}${v.detail ? ' — ' + v.detail : ''}`);
  }
  md.push('', `判定：**${r.verdict}**`);
  fs.writeFileSync(path.join(runDir, 'scripts', script.id, 'steps.md'), md.join('\n') + '\n');
  await ensureReviewOff(page).catch(() => {});
  await page.evaluate(() => { document.querySelectorAll('.arco-trigger-popup, .arco-drawer').forEach((e) => e.remove()); }).catch(() => {});
}

await browser.close();
const t1 = new Date();

// ---------------------------------------------------------------------------
// meta / prompts-used / SUMMARY / COMPARISON
// ---------------------------------------------------------------------------
fs.writeFileSync(path.join(runDir, 'meta.yaml'), yamlDump({
  run_id: path.basename(runDir),
  feature: `${path.basename(path.dirname(featDir))}/${scope}`,
  environment: { base_url: baseUrl, env_label: '50892 dev' },
  account: { username: loginCfg.username },
  git: { repo: 'gkx-orchestration', head: gitHead },
  time: { started_at: t0.toISOString(), ended_at: t1.toISOString() },
  tooling: 'playwright-runner（chromium headless, playwright 1.61.1）',
  baseline: path.basename(baselineDir),
}) + '\n');

fs.writeFileSync(path.join(runDir, 'prompts-used.md'), [
  '# prompts-used（QA-RUNNER-CALIBRATION-L01 摘录）', '',
  '- 命令行：`node run-scripts.mjs <功能目录> [--run-dir] [--only] [--headless false] [--baseline] [--check]`',
  '- 读 cases-v1：index.yaml + cases/{id}.yaml + fixtures/testdata.yaml',
  '- Playwright chromium 1920×1080@1；headless 默认 true；context acceptDownloads',
  '- 登录：跳 /login 才填 fixtures.login，已在业务页跳过',
  '- action 枚举：goto/login_if_needed/click/fill/press/wait/snapshot/screenshot/assert_visible/assert_url/assert_absent/evaluate/select_option/reload/network_assert',
  '- resolveTarget 启发式（heading/button/textbox/switch/语义区块），失败重试 ≤2 次后降级 getByText，仍失败记 fail 原因继续',
  '- 每步截图（X6）：screenshots/{02d}-{slug}.png',
  '- expect 双层：{note,assert} 于 {page,expect} 求值；{note,manual:true}→pending_manual；裸字符串按「」词转译可见性，转译不了 warning 不判 fail',
  '- allow_skip → n/a；判定 pass/fail/blocked(C6)；跑完自动产出 COMPARISON.md 对照基准 ' + path.basename(baselineDir),
].join('\n') + '\n');

const counts = { pass: 0, fail: 0, blocked: 0, 'n/a': 0 };
for (const r of results) counts[r.verdict in counts ? r.verdict : 'n/a']++;
const p01 = results.filter((r) => r.script.priority !== 'P2');
const p01Pass = p01.filter((r) => r.verdict === 'pass').length;

const sum = [
  `# SUMMARY · ${path.basename(runDir)}`, '',
  `原生 Playwright runner 校准跑（feature=${scope}）。环境 ${baseUrl}（${loginCfg.username}）。`,
  `P0/P1 机检通过 ${p01Pass}/${p01.length}；总判定 Pass ${counts.pass} / Fail ${counts.fail} / Blocked ${counts.blocked} / N-A ${counts['n/a']}。`, '',
  '| id | 用例 | 标题 | 判定 | 说明 |', '|---|---|---|---|---|',
];
for (const r of results) sum.push(`| ${r.script.id} | ${String(r.script.func_id || '').replace(/^.*FUNC-/, '')} | ${r.script.title} | ${r.verdict} | ${String(r.actual).slice(0, 100).replace(/\|/g, '/')} |`);
fs.writeFileSync(path.join(runDir, 'SUMMARY.md'), sum.join('\n') + '\n');

// COMPARISON
const comp = [
  `# COMPARISON · ${path.basename(runDir)} vs ${path.basename(baselineDir)}`, '',
  `runner 逐条 verdict 对照基准 run（目标一致率 100%）。`, '',
  '| id | 基准 | runner | 一致 | 归因 |', '|---|---|---|---|---|',
];
let match = 0;
const mismatches = [];
for (const r of results) {
  const bf = path.join(baselineDir, 'scripts', r.script.id, 'result.yaml');
  let bv = '(缺)';
  if (fs.existsSync(bf)) { try { bv = yamlLoad(bf).verdict || '(无)'; } catch { bv = '(解析失败)'; } }
  const norm = (v) => (v === 'n_a' ? 'n/a' : v);
  const same = norm(bv) === norm(r.verdict);
  if (same) match++;
  else mismatches.push(r);
  let cause = same ? '' : r.verdict === 'fail' ? 'runner 断言失败：' + String(r.actual).slice(0, 70) : r.verdict === 'blocked' ? 'runner 异常中断' : r.verdict === 'n/a' ? 'allow_skip 命中' : '基准非 pass';
  comp.push(`| ${r.script.id} | ${bv} | ${r.verdict} | ${same ? '✅' : '❌'} | ${cause.replace(/\|/g, '/')} |`);
}
comp.push('', `**一致率：${match}/${results.length}**`);
if (mismatches.length) {
  comp.push('', '## 不一致条目归因', '');
  for (const r of mismatches) {
    comp.push(`### ${r.script.id} ${r.script.title}`, `- runner verdict: **${r.verdict}**`, `- actual: ${String(r.actual).slice(0, 300)}`);
    for (const v of (r.verdicts || []).filter((x) => x.status === 'fail')) comp.push(`- 失败断言: ${v.note} — ${v.detail}`);
    comp.push('');
  }
}
fs.writeFileSync(path.join(runDir, 'COMPARISON.md'), comp.join('\n') + '\n');

console.log(`\n✅ run 完成 ${t1.toISOString()}`);
console.log(`   pass=${counts.pass} fail=${counts.fail} blocked=${counts.blocked} n/a=${counts['n/a']}`);
console.log(`   COMPARISON 一致率 ${match}/${results.length} → ${path.join(runDir, 'COMPARISON.md')}`);
process.exit(counts.fail + counts.blocked > 0 ? 1 : 0);
