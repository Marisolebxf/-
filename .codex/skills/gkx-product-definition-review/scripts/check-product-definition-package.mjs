#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const args = Object.fromEntries(
  process.argv.slice(2).reduce((pairs, arg, index, values) => {
    if (arg.startsWith('--')) pairs.push([arg.slice(2), values[index + 1]]);
    return pairs;
  }, []),
);

const required = ['module-id', 'module-name', 'leaf-id', 'leaf-name'];
const missing = required.filter((key) => !args[key]);
if (missing.length) {
  console.error(`Missing required arguments: ${missing.map((key) => `--${key}`).join(', ')}`);
  process.exit(2);
}

const moduleKey = `${args['module-id']}-${args['module-name']}`;
const fileModuleKey = `${args['module-id'].replaceAll('-', '')}-${args['module-name']}`;
const productRoot = path.resolve(
  args.root ?? process.cwd(),
  'agent-delivery/agent-handoffs/产品整体定义',
);
const files = {
  usm: path.join(productRoot, moduleKey, `USM-${moduleKey}.md`),
  trace: path.join(productRoot, moduleKey, `TRACE-${fileModuleKey}.yaml`),
  ia: path.join(productRoot, moduleKey, `IA-${fileModuleKey}.md`),
  wireframe: path.join(productRoot, moduleKey, `Wireframe-${fileModuleKey}.md`),
};

const failures = [];
const checks = [];
const check = (condition, message) => {
  checks.push(message);
  if (!condition) failures.push(message);
};
const read = (file) => (fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : '');

Object.entries(files).forEach(([kind, file]) => check(fs.existsSync(file), `${kind} file exists: ${file}`));

const usm = read(files.usm);
const trace = read(files.trace);
const ia = read(files.ia);
const wireframe = read(files.wireframe);

check(trace.includes(`module: ${moduleKey}`), 'TRACE declares the parent module');
check(/\nleaves:\n/.test(trace), 'TRACE contains a leaves collection');
check(new RegExp(`\\n\\s+- id: ${args['leaf-id']}(?:\\n|\\r\\n)`).test(trace), 'TRACE maps the requested leaf');
check(trace.includes('compliance_refs:'), 'TRACE contains compliance references');
check(usm.includes(args['leaf-id']) && usm.includes('用户故事') && usm.includes('验收场景'), 'USM defines the leaf story and testable acceptance');
check(ia.includes(args['leaf-id']), 'IA contains the requested leaf');
check(wireframe.includes(args['leaf-id']), 'Wireframe contains the requested leaf');
check(wireframe.includes('内部评审模式') && wireframe.includes('用户 / 角色切换'), 'Wireframe records the global internal-review convention');

if (failures.length) {
  console.error(`Product-definition package check failed (${failures.length}/${checks.length}):`);
  failures.forEach((item) => console.error(`- ${item}`));
  process.exit(1);
}

console.log(`Product-definition package check passed (${checks.length} checks): ${moduleKey} → ${args['leaf-id']}-${args['leaf-name']}`);
