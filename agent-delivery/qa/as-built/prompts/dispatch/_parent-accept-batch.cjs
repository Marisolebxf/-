#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const root = path.resolve(__dirname, '../../../../..');
const tools = path.join(root, 'agent-delivery/qa/as-built/tools');
const scriptsRoot = path.join(root, 'agent-delivery/qa/as-built/scripts/SDWJSF-KJZTFWSFK');

function slug(cpid) {
  return cpid.replace(/\./g, '-');
}

function countFuncRows(funcMd) {
  const s = fs.readFileSync(path.join(root, funcMd), 'utf8');
  return (s.match(/^\| ZNFWJQ-SDWJSF\/KJZTFWSFK-v1\.0-FUNC-/gm) || []).length;
}

function backfillAutoIds(funcMd) {
  const p = path.join(root, funcMd);
  let s = fs.readFileSync(p, 'utf8');
  let n = 0;
  s = s.replace(/^\| ZNFWJQ[^\n]+$/gm, (line) => {
    const m = line.match(/FUNC-(\d{5})/);
    if (!m) return line;
    const funcId = `FUNC-${m[1]}`;
    if (line.includes(`| ${funcId} |`)) return line;
    let patched = line.replace(/\| INTEG \|  \|  \| endpoint_id/, `| INTEG |  | ${funcId} | endpoint_id`);
    if (patched !== line) {
      n++;
      return patched;
    }
    patched = line.replace(/\| INTEG \|  \|  \| catalog_page_id/, `| INTEG |  | ${funcId} | catalog_page_id`);
    if (patched !== line) {
      n++;
      return patched;
    }
    return line;
  });
  if (n) fs.writeFileSync(p, s);
  return n;
}

function findFuncMd(cpid) {
  const tcRoot = path.join(root, 'agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK');
  let found = null;
  const walk = (d) => {
    for (const ent of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, ent.name);
      if (ent.isDirectory()) walk(p);
      else if (ent.name.startsWith('FUNC-') && ent.name.endsWith('-用例.md')) {
        const head = fs.readFileSync(p, 'utf8').slice(0, 2000);
        if (head.includes(`catalog_page_id=${cpid}`)) {
          found = 'agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/' + path.relative(tcRoot, p).split(path.sep).join('/');
        }
      }
    }
  };
  walk(tcRoot);
  return found;
}

const catalog = fs.readFileSync(path.join(root, 'agent-delivery/qa/as-built/catalog/SDWJSF-KJZTFWSFK.yaml'), 'utf8');

for (const cpid of process.argv.slice(2)) {
  const block = catalog.split('\n- id: ').find((b) => b.startsWith(cpid));
  if (!block) {
    console.log(cpid, 'FAIL no catalog block');
    continue;
  }
  const mod = (block.match(/\n  module: (\S+)/) || [])[1];
  const dir = path.join(scriptsRoot, mod, slug(cpid));
  const casesDir = path.join(dir, 'cases');
  if (!fs.existsSync(casesDir)) {
    console.log(cpid, 'FAIL no cases dir');
    continue;
  }
  const yamls = fs.readdirSync(casesDir).filter((f) => f.endsWith('.yaml'));
  const funcMd = findFuncMd(cpid);
  if (!funcMd) {
    console.log(cpid, 'FAIL no func md');
    continue;
  }
  const expected = countFuncRows(funcMd);
  const skip = yamls.some((f) => fs.readFileSync(path.join(casesDir, f), 'utf8').includes('allow_skip'));
  let checkOut = '';
  try {
    const rel = path.relative(tools, dir);
    checkOut = execSync(`node run-apiview.mjs ${rel} --check`, { cwd: tools, encoding: 'utf8' }).trim();
  } catch (e) {
    checkOut = String(e.stdout || '') + String(e.stderr || '');
  }
  const idsFilled = backfillAutoIds(funcMd);
  const ok = yamls.length === expected && !skip && /编译错误 0/.test(checkOut);
  console.log(JSON.stringify({ cpid, expected, yamls: yamls.length, skip, checkOut, idsFilled, ok }));
}
