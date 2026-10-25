#!/usr/bin/env node
/**
 * One runnable check for GitLab CI variable client. No live GitLab, no .env.
 */
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import {
  listVariables,
  parseEnvText,
  publicVar,
  redact,
  resolveProjectId,
  upsertVariable,
} from './lib/gitlab-ci-var.mjs';

let failed = 0;
function assert(cond, msg) {
  if (cond) {
    console.log(`ok  ${msg}`);
    return;
  }
  failed += 1;
  console.error(`FAIL  ${msg}`);
}

const parsed = parseEnvText('GKX_GITLAB_TOKEN="glpat-test"\nGKX_GITLAB_BASE=https://gitlab.example/\n# x\n');
assert(parsed.GKX_GITLAB_TOKEN === 'glpat-test', 'parse quoted token');
assert(parsed.GKX_GITLAB_BASE === 'https://gitlab.example/', 'parse base');

const secret = 'secret-value-not-for-output';
assert(redact(`bad ${secret}`, secret) === 'bad ***', 'redact secret');
assert(!('value' in publicVar({ key: 'A', value: secret, masked: true })), 'publicVar drops value');
assert(publicVar({ key: 'A', value: secret, masked: true }).value_length === secret.length, 'publicVar keeps length');

function mockFetch(routes) {
  return async (url, init) => {
    const method = init.method || 'GET';
    const route = routes.find((item) => item.method === method && url.includes(item.match));
    if (!route) throw new Error(`unexpected ${method} ${url}`);
    route.seen = { url, init };
    const body = route.body === undefined ? '' : JSON.stringify(route.body);
    return {
      status: route.status || 200,
      text: async () => body,
    };
  };
}

const env = {
  token: 'glpat-test',
  base: 'https://gitlab.example',
  fetchImpl: mockFetch([
    {
      method: 'GET',
      match: '/api/v4/projects?',
      body: [
        { id: 9, path_with_namespace: 'other/lumen-algo-py' },
        { id: 8, path_with_namespace: 'sz-gkx/gkx-lumen/lumen-algo-py' },
      ],
    },
  ]),
};
const id = await resolveProjectId(env, 'sz-gkx/gkx-lumen/lumen-algo-py');
assert(id === '8', 'resolve exact path to numeric id');
const numeric = await resolveProjectId(
  { ...env, fetchImpl: async () => { throw new Error('search must not run'); } },
  '8',
);
assert(numeric === '8', 'numeric id skips search');

const listEnv = {
  token: 'glpat-test',
  base: 'https://gitlab.example',
  fetchImpl: mockFetch([
    { method: 'GET', match: '/api/v4/projects?', body: [{ id: 8, path_with_namespace: 'sz-gkx/gkx-lumen/lumen-algo-py' }] },
    {
      method: 'GET',
      match: '/variables',
      body: [{ key: 'ZHIPU_LLM_API_KEY', value: secret, masked: true, protected: false, raw: true, environment_scope: '*' }],
    },
  ]),
};
const listed = await listVariables(listEnv, 'sz-gkx/gkx-lumen/lumen-algo-py');
assert(!JSON.stringify(listed).includes(secret), 'list result hides value');
assert(listed.variables[0].value_length === secret.length, 'list keeps value_length');
assert(listed.project_id === '8', 'list uses numeric id');

let posted;
const setEnv = {
  token: 'glpat-test',
  base: 'https://gitlab.example',
  fetchImpl: mockFetch([
    { method: 'GET', match: '/api/v4/projects?', body: [{ id: 8, path_with_namespace: 'sz-gkx/gkx-lumen/lumen-algo-py' }] },
    { method: 'GET', match: '/variables', body: [] },
    {
      method: 'POST',
      match: '/variables',
      status: 201,
      body: { key: 'ZHIPU_LLM_MODEL', value: 'glm-5.3-flash', masked: true, protected: false, raw: true, environment_scope: '*' },
    },
  ]),
};
const original = setEnv.fetchImpl;
setEnv.fetchImpl = async (url, init) => {
  if (init.method === 'POST') posted = JSON.parse(init.body);
  assert(init.headers['PRIVATE-TOKEN'] === 'glpat-test', 'token stays in header');
  assert(!url.includes('glpat-test'), 'token stays out of URL');
  return original(url, init);
};
const created = await upsertVariable(setEnv, 'sz-gkx/gkx-lumen/lumen-algo-py', {
  key: 'ZHIPU_LLM_MODEL',
  value: 'glm-5.3-flash',
});
assert(created.action === 'created', 'missing key is created');
assert(posted.protected === false && posted.masked === true && posted.raw === true, 'defaults are masked, unprotected, raw');
assert(!('value' in created), 'set result has no value field');
assert(!JSON.stringify(created).includes('glm-5.3-flash'), 'set result hides value');
assert(created.value_length === 'glm-5.3-flash'.length, 'set result keeps length');

const failEnv = {
  token: 'glpat-test',
  base: 'https://gitlab.example',
  fetchImpl: mockFetch([
    { method: 'GET', match: '/api/v4/projects?', body: [{ id: 8, path_with_namespace: 'sz-gkx/gkx-lumen/lumen-algo-py' }] },
    { method: 'GET', match: '/variables', body: [{ key: 'ZHIPU_LLM_API_KEY' }] },
    { method: 'PUT', match: '/variables/', status: 400, body: { message: `rejected ${secret}` } },
  ]),
};
let caught = '';
try {
  await upsertVariable(failEnv, '8', { key: 'ZHIPU_LLM_API_KEY', value: secret });
} catch (err) {
  caught = err.message;
}
assert(caught.includes('http=400') && !caught.includes(secret), 'error redacts value');

const proc = spawn(process.execPath, [fileURLToPath(new URL('./gitlab-ci-var-mcp-server.mjs', import.meta.url))], {
  stdio: ['pipe', 'pipe', 'pipe'],
});
let out = '';
proc.stdout.on('data', (chunk) => { out += chunk; });
proc.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'initialize', params: {} })}\n`);
proc.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id: 2, method: 'tools/list' })}\n`);
proc.stdin.end();
await new Promise((resolve) => proc.on('close', resolve));
assert(out.includes('gitlab-ci-var-list') && out.includes('gitlab-ci-var-set'), 'MCP lists both tools');

if (failed) {
  console.error(`${failed} failed`);
  process.exit(1);
}
console.log('gitlab-ci-var selfcheck passed');
