/**
 * 两个 runner 共用的读册、断言、截图和单条结果文件。
 * 登录、评审开关、系统专有动作不在这里。
 * 专题入口 run-scripts.mjs；算法库入口 run-apiview.mjs。
 */
import fs from 'node:fs';
import path from 'node:path';

// 支持语法子集（覆盖本项目 scripts/gold/testdata/result/meta 全部实际用法）：
//   - 嵌套 map / list（- 项，含 "- key: value" 行内起始 map；`k:` 下子列表缩进或顶格均支持）
//   - 单/双引号字符串（双引号 \" \\ 转义；单引号 '' 转义；引号内跨行折叠为空格）、裸标量（数字/bool/null/中文/含 / 与（） 等）
//   - flow list: [a, b, 'c']；flow map: {a: 1, b: 'x'}（一层，值不再嵌套 flow）
//   - 折叠标量: >- / > / |- / |（按缩进收集后续行折叠/保行）
//   - # 注释（引号外）、空行
// 不支持：锚点&/*、多文档---、tag、嵌套 flow、Tab 缩进 → 遇到 throw
// ---------------------------------------------------------------------------
export function parseYaml(text) {
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

export function yamlLoad(file) {
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
export function pwExpect(locOrPage, opt) {
  return makeMatchers(locOrPage, false, opt && opt.timeout);
}

// 极简 YAML 序列化（result/meta 用；字符串含特殊字符一律双引号转义）
export function yamlDump(obj, indent = 0) {
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

function naturalIdKey(id) {
  return String(id).split(/(\d+)/).map((p) => (/^\d+$/.test(p) ? Number(p) : p.toLowerCase()));
}
export function loadCasesV1(dir) {
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
  return { byId, order: order.map((id) => byId.get(id)).filter(Boolean) };
}

export function slug(s) {
  return String(s).replace(/[^\w\u4e00-\u9fff]+/g, '-').slice(0, 24).replace(/^-+|-+$/g, '') || 'step';
}

export function checkAsserts(selected) {
  let bad = 0;
  for (const s of selected) {
    for (const [i, exp] of (s.expect || []).entries()) {
      if (exp && typeof exp === 'object' && exp.assert) {
        try { new Function('page', 'expect', 'baseUrl', 'return (async () => {' + exp.assert + '})()'); }
        catch (e) { bad++; console.error(`  ✗ ${s.id}.expect[${i}] 编译失败: ${e.message}\n    ${exp.assert}`); }
      } else if (typeof exp === 'string') {
        console.warn(`  ⚠ ${s.id}.expect[${i}] 裸字符串（未转换）: ${exp}`);
      }
    }
  }
  return bad;
}

export async function evalExpects(page, script, baseUrl) {
  const verdicts = [];
  const warnings = [];
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
          await new Function('page', 'expect', 'baseUrl', 'return (async () => {' + exp.assert + '})()')(page, pwExpect, baseUrl);
          verdicts.push({ note: exp.note, status: 'pass', detail: '' });
        } catch (e) {
          verdicts.push({ note: exp.note, status: 'fail', detail: String(e.message).split('\n')[0] + ' | assert: ' + String(exp.assert).slice(0, 120) });
        }
      } else verdicts.push({ note: exp.note, status: 'warn', detail: '无 assert 且非 manual（待补）' });
    }
  }
  return { verdicts, warnings };
}

export function judgeRun({ aborted, skip, verdicts, warnings }) {
  const fails = verdicts.filter((v) => v.status === 'fail');
  const passes = verdicts.filter((v) => v.status === 'pass');
  const manuals = verdicts.filter((v) => v.status === 'pending_manual');
  let verdict, failClass = null, actual;
  if (aborted) { verdict = 'blocked'; failClass = 'C6'; actual = '执行异常中断: ' + String(aborted.message).split('\n')[0]; }
  else if (skip) { verdict = 'n/a'; actual = 'allow_skip 命中：关键前置 5s 不可见（详见 steps.md）'; }
  else if (fails.length) { verdict = 'fail'; failClass = 'C6'; actual = fails.map((f) => `✗ ${f.note} — ${f.detail}`).join(' | '); }
  else { verdict = 'pass'; actual = `${passes.length} 项机检断言通过` + (manuals.length ? `；${manuals.length} 项待人工` : '') + (warnings.length ? `；${warnings.length} 条 warning` : ''); }
  return { verdict, fail_class: failClass, actual };
}

export async function shotStep(page, caseDir, shotIdx, action, label) {
  await page.waitForLoadState('networkidle', { timeout: 4000 }).catch(() => {});
  await page.waitForTimeout(350);
  await page.screenshot({
    path: path.join(caseDir, 'screenshots', `${String(shotIdx).padStart(2, '0')}-${slug(action + '-' + label)}.png`),
  }).catch(() => {});
}

export async function readFailText(page, verdict) {
  if (verdict !== 'fail' && verdict !== 'blocked') return '';
  let visibleText = await page.locator('main').innerText().catch(() => '');
  if (!visibleText.trim()) visibleText = await page.locator('body').innerText().catch(() => '');
  return visibleText.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim().slice(0, 1500);
}

export function writeCaseRecord(runDir, script, r, visibleText) {
  const dir = path.join(runDir, 'scripts', script.id);
  const shotCount = fs.existsSync(path.join(dir, 'screenshots')) ? fs.readdirSync(path.join(dir, 'screenshots')).length : 0;
  fs.writeFileSync(path.join(dir, 'result.yaml'), yamlDump({
    id: script.id, priority: script.priority, func_id: script.func_id,
    verdict: r.verdict, fail_class: r.fail_class, actual: r.actual,
    screenshot_count: shotCount,
    visible_text: visibleText || null,
    time: new Date().toISOString().slice(0, 16).replace('T', ' '),
  }) + '\n');
  const md = [`# ${script.id} 逐步实际操作（playwright-runner）`, ''];
  for (const s of r.steps) md.push(`${s.n}. **${s.action}** ${s.label}${s.detail ? ' — ' + s.detail : ''} ${s.ok ? '✓' : '✗'}`);
  if (r.verdicts && r.verdicts.length) {
    md.push('', '## expect 逐条', '');
    for (const v of r.verdicts) md.push(`- ${v.status === 'pass' ? '✓' : v.status === 'fail' ? '✗' : '⚠'} ${v.note}${v.detail ? ' — ' + v.detail : ''}`);
  }
  md.push('', `判定：**${r.verdict}**`);
  if (visibleText) md.push('', '## 失败时主区文字', '', visibleText);
  fs.writeFileSync(path.join(dir, 'steps.md'), md.join('\n') + '\n');
}
