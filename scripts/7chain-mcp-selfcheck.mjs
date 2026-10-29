#!/usr/bin/env node
/**
 * gkx-7chain M1 自检。不连后端。断言 13 个工具的参数校验与网关路由。
 * 跑法：node scripts/7chain-mcp-selfcheck.mjs
 */
import assert from 'node:assert/strict';
import { callTool, clearMintedToken, handleRequest, listToolDefs, setHttpFetch, truncateGraph } from './7chain-mcp-server.mjs';

const M1 = [
  'search-enterprise', 'search-industry', 'search-policy',
  'synth-index', 'synth-collab',
  'ent-evaluate', 'ent-recommend', 'ent-diagnose',
  'chain-panorama', 'chain-analyze',
  'policy-indicators', 'policy-apply',
  'svc-analysis',
];
const M2 = ['ent-graph', 'chain-list', 'chain-stats', 'policy-analysis', 'svc-orgs', 'svc-graph'];

const saved = {
  GKX_MCP_API_BASE: process.env.GKX_MCP_API_BASE,
  GKX_MCP_TOKEN: process.env.GKX_MCP_TOKEN,
  GKX_MCP_SVC_BASE: process.env.GKX_MCP_SVC_BASE,
  GKX_MCP_POLICY_BASE: process.env.GKX_MCP_POLICY_BASE,
  GKX_MCP_ENTERPRISE_BASE: process.env.GKX_MCP_ENTERPRISE_BASE,
};

function restoreEnv() {
  for (const [key, value] of Object.entries(saved)) {
    if (value === undefined) delete process.env[key];
    else process.env[key] = value;
  }
  setHttpFetch(null);
}

function jsonResponse(status, body, headers = {}) {
  return {
    status,
    ok: status >= 200 && status < 300,
    headers: { get: (name) => headers[name.toLowerCase()] ?? null },
    text: async () => (typeof body === 'string' ? body : JSON.stringify(body)),
  };
}

function installFetch(handler) {
  const calls = [];
  setHttpFetch(async (url, init) => {
    calls.push({ url: String(url), init });
    return handler(url, init, calls);
  });
  return calls;
}

function textOf(result) {
  return result?.content?.[0]?.text || '';
}

function parsed(result) {
  return JSON.parse(textOf(result));
}

process.env.GKX_MCP_API_BASE = 'http://gateway.test/api';
delete process.env.GKX_MCP_TOKEN;
delete process.env.GKX_MCP_SVC_BASE;
delete process.env.GKX_MCP_POLICY_BASE;
delete process.env.GKX_MCP_ENTERPRISE_BASE;

const names = listToolDefs().map((tool) => tool.name);
assert.deepEqual(names, M1, 'tools/list 必须正好是 M1 的 13 个工具');
for (const banned of M2) assert.equal(names.includes(banned), false, `${banned} 属于 M2`);
for (const tool of listToolDefs()) {
  assert.equal(typeof tool.description, 'string');
  assert.ok(tool.description.length > 40, `${tool.name} 描述过短`);
  assert.equal(tool.inputSchema.type, 'object');
}

const init = JSON.parse(await handleRequest(1, 'initialize', {}));
assert.equal(init.result.protocolVersion, '2024-11-05');
assert.equal(init.result.serverInfo.name, 'gkx-7chain');
assert.equal(await handleRequest(2, 'notifications/initialized', {}), null);
const listed = JSON.parse(await handleRequest(3, 'tools/list', {}));
assert.equal(listed.result.tools.length, 13);

const callsFor = (status, body) => installFetch(async () => jsonResponse(status, body));

async function rejects(name, args, snippet) {
  const calls = callsFor(200, { code: 0, data: {} });
  const result = await callTool(name, args);
  assert.equal(result.isError, true, `${name} 应拒绝 ${JSON.stringify(args)}`);
  assert.equal(calls.length, 0, `${name} 校验失败不得打网关`);
  if (snippet) assert.match(textOf(result), snippet);
}

async function hits(name, args, { method, path, bodyIncludes }) {
  const calls = callsFor(200, { code: 0, data: { metric_id: 'M_KEEP', data_source: 'mock', nodes: [{ id: 'n1' }] } });
  const result = await callTool(name, args);
  assert.notEqual(result.isError, true, `${name} 失败: ${textOf(result)}`);
  assert.equal(calls.length >= 1, true, `${name} 未请求网关`);
  const hit = calls[0];
  assert.equal(hit.init.method, method);
  assert.match(hit.url, new RegExp(path.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  assert.equal(hit.init.headers['X-Trace-Id'].length, 32);
  assert.match(hit.init.headers.traceparent, /^00-[0-9a-f]{32}-[0-9a-f]{16}-01$/);
  if (bodyIncludes) assert.match(hit.init.body, bodyIncludes);
  const body = parsed(result);
  assert.match(JSON.stringify(body), /M_KEEP/, `${name} 应透传 metric_id`);
  assert.match(JSON.stringify(body), /mock/, `${name} 应透传 data_source`);
  return { calls, body };
}

await rejects('search-enterprise', {}, /至少给一项/);
await rejects('search-enterprise', { q: '华为', limit: 51 }, /上限 50/);
await rejects('search-industry', {}, /q 必填/);
await rejects('search-policy', {}, /至少给一项/);
await rejects('ent-evaluate', { enterprise_codes: [], sub_type: 'tech' }, /1～20/);
await rejects('ent-evaluate', { enterprise_codes: ['a'], sub_type: 'nope' }, /sub_type/);
await rejects('ent-recommend', { kind: 'attract' }, /industry/);
await rejects('ent-recommend', { kind: 'attract', industry: '光刻', limit: 31 }, /上限 30/);
await rejects('ent-diagnose', { action: 'diagnose' }, /enterprise_code/);
await rejects('ent-diagnose', { action: 'rank' }, /industry 或 region/);
await rejects('chain-panorama', {}, /chain_id/);
await rejects('chain-analyze', { chain_id: 'INB1', aspect: 'cycle,bottlenecks' }, /一个 aspect/);
await rejects('chain-analyze', { chain_id: 'INB1', aspect: 'nope' }, /aspect/);
await rejects('policy-indicators', {}, /kind/);
await rejects('policy-apply', { action: 'parse' }, /policy_id/);
await rejects('policy-apply', { action: 'match', subject_id: 'E1' }, /subject_type/);
await rejects('policy-apply', { action: 'simulate' }, /scope_code/);
await rejects('svc-analysis', { kind: 'models' }, /topic 或 model_id/);
await rejects('svc-analysis', { kind: 'indicators', topic: 'tech' }, /kind=models/);
await rejects('synth-index', { index: 'nope' }, /index/);
await rejects('synth-collab', { action: 'graph' }, /region/);
await rejects('synth-collab', { action: 'graph', region: '深圳', hops: 3 }, /上限 2/);

{
  const calls = callsFor(200, { code: 0, data: { list: [] } });
  const missing = await callTool('search-enterprise', { q: '华为' });
  assert.equal(missing.isError, true);
  assert.match(textOf(missing), /GKX_MCP_POLICY_BASE|GKX_MCP_ENTERPRISE_BASE/);
  assert.equal(calls.length, 0);
}
{
  process.env.GKX_MCP_POLICY_BASE = 'http://policy.test';
  const calls = installFetch(async (url, init) => {
    assert.equal(init.method, 'POST');
    assert.match(String(url), /^http:\/\/policy\.test\/enterprise\/topic\/v1\/search\/smart$/);
    const sent = JSON.parse(init.body);
    assert.equal(sent.keyword, '固态电池');
    assert.deepEqual(sent.keywords, ['固态电池']);
    assert.equal(sent.q, '固态电池');
    assert.equal(sent.size, 5);
    assert.equal(sent.sort_field, 'competitiveness_score');
    return jsonResponse(200, {
      code: 0,
      data: {
        list: [{ org_id: 'abc', name_cn: '国轩高科股份有限公司' }],
        total: 197,
        page: 1,
        size: 5,
        metric_id: 'M_KEEP',
        data_source: 'mock',
      },
    });
  });
  const result = await callTool('search-enterprise', { q: '固态电池', limit: 5 });
  assert.notEqual(result.isError, true, textOf(result));
  assert.equal(calls.length, 1);
  const body = parsed(result);
  assert.equal(body.data.mode, 'smart');
  assert.equal(body.data.total, 197);
  assert.equal(body.data.enterprises[0].enterprise_code, 'abc');
  assert.equal(body.data.enterprises[0].name, '国轩高科股份有限公司');
  assert.match(JSON.stringify(body), /M_KEEP/);
  delete process.env.GKX_MCP_POLICY_BASE;
}
await hits('search-industry', { q: '光刻' }, { method: 'GET', path: '/api/innov/v1/industry/list' });
await hits('search-policy', { subject_id: 'E0001' }, { method: 'GET', path: '/api/policy/v1/policy/match' });
await hits('ent-evaluate', { enterprise_codes: ['E1'], sub_type: 'tech' }, {
  method: 'POST',
  path: '/api/entan/v1/evaluation/compute',
  bodyIncludes: /"sub_type":"technology"/,
});
await hits('ent-recommend', { kind: 'cultivate', industry: '半导体' }, {
  method: 'POST',
  path: '/api/entan/v1/recommend/cultivate',
  bodyIncludes: /"region":"深圳"/,
});
await hits('ent-diagnose', { action: 'diagnose', enterprise_code: 'E1' }, { method: 'GET', path: '/api/entan/v1/diagnosis' });
await hits('chain-panorama', { chain_id: 'INB1701' }, { method: 'GET', path: '/api/innov/v1/industry/INB1701/panorama' });
await hits('chain-analyze', { chain_id: 'INB1701', aspect: 'cycle' }, { method: 'GET', path: '/api/innov/v1/industry/INB1701/cycle' });
await hits('policy-indicators', { kind: 'timeseries', industry: '光刻' }, { method: 'GET', path: '/api/policy/v1/policy/indicators' });
await hits('policy-apply', { action: 'parse', policy_id: 'P1' }, { method: 'GET', path: '/api/policy/v1/policy/text/parse' });
await hits('policy-apply', { action: 'match', subject_id: 'E1', subject_type: 'enterprise' }, { method: 'GET', path: '/api/policy/v1/policy/match' });
await hits('svc-analysis', { kind: 'indicators', topic: 'field' }, { method: 'GET', path: '/api/entan/v1/svc/indicators' });
await hits('synth-index', { index: 'vitality', region: '深圳', year: 2024 }, {
  method: 'POST',
  path: '/api/entan/v1/synth-metric/metric/M_SYNTH_186_1/compute',
  bodyIncludes: /"city":"深圳"/,
});
await hits('synth-index', { index: 'elements', facet: 'type', region: '深圳' }, {
  method: 'POST',
  path: '/api/entan/v1/synth-metric/metric/M_SYNTH_187_1/compute',
});
await hits('synth-index', { index: 'catalog' }, { method: 'GET', path: '/api/entan/v1/synth-metric/catalog' });
await hits('synth-collab', { action: 'index', region: '深圳' }, {
  method: 'POST',
  path: '/api/entan/v1/synth-metric/metric/M_SYNTH_191_1/compute',
});

{
  const calls = callsFor(200, { code: 0, data: { nodes: [], edges: [] } });
  const result = await callTool('synth-collab', { action: 'graph', region: '深圳', hops: 1 });
  assert.notEqual(result.isError, true, textOf(result));
  assert.ok(calls.some((call) => call.url.includes('/industry-comp/v1/comp/graph')));
  assert.ok(calls.some((call) => call.url.includes('/graph/metrics')));
  assert.ok(calls.some((call) => call.url.includes('/graph/viz')));
  assert.equal(calls[0].url.includes('hops=3'), false);
}

{
  const nodes = Array.from({ length: 100 }, (_, i) => ({ id: `n${i}`, metric_id: 'M_GRAPH' }));
  const edges = [{ source: 'n0', target: 'n90' }, { source: 'n0', target: 'n1' }];
  const calls = callsFor(200, { code: 0, data: { nodes, edges, metric_id: 'M_GRAPH', data_source: 'mock' } });
  const result = await callTool('chain-panorama', { chain_id: 'INB1701' });
  assert.equal(calls.length, 1);
  const body = parsed(result);
  assert.equal(body.truncated, true);
  assert.equal(body.data.nodes.length, 80);
  assert.equal(body.data.truncated, true);
  assert.equal(body.data.edges.length, 1);
  assert.equal(body.data.edges[0].target, 'n1');
  assert.equal(body.data.metric_id, 'M_GRAPH');
  assert.equal(body.data.data_source, 'mock');
}

{
  const cut = truncateGraph({ nodes: [{ id: 'a' }, { id: 'b' }] });
  assert.equal(cut.truncated, false);
  assert.equal(cut.node_count, 2);
}

{
  const calls = callsFor(200, { code: 0, data: { items: [] } });
  const result = await callTool('search-policy', { q: '光刻' });
  assert.equal(result.isError, true);
  assert.match(textOf(result), /GKX_MCP_POLICY_BASE/);
  assert.equal(calls.length, 0);
}

{
  process.env.GKX_MCP_POLICY_BASE = 'http://policy.test';
  const calls = installFetch(async (url) => {
    const target = String(url);
    if (target.includes('/policy/search')) {
      return jsonResponse(200, {
        code: 0,
        data: {
          items: [{ policy_id: 'p1', title: '光刻专项' }],
          total: 1,
          honesty: { empty: false, source: 'dwd' },
        },
      });
    }
    return jsonResponse(200, {
      code: 0,
      data: {
        item: { policy_id: 'p1', title: '光刻专项', content: '正文' },
        honesty: { empty: false },
      },
    });
  });
  const result = await callTool('search-policy', { q: '光刻', level: '国家' });
  assert.notEqual(result.isError, true, textOf(result));
  assert.equal(calls.length, 2);
  assert.match(calls[0].url, /^http:\/\/policy\.test\/policy\/topic\/v1\/policy\/search\?/);
  assert.match(calls[0].url, /(?:^|[?&])q=/);
  assert.match(calls[0].url, /(?:^|[?&])keyword=/);
  assert.match(calls[0].url, /(?:^|[?&])level=/);
  assert.match(calls[1].url, /^http:\/\/policy\.test\/policy\/topic\/v1\/policy\/docs\/p1$/);
  const body = parsed(result);
  assert.equal(body.data.mode, 'search');
  assert.equal(body.data.mock, undefined);
  assert.equal(body.data.policies.length, 1);
  assert.equal(body.data.policies[0].content, '正文');
  assert.equal(body.data.honesty.source, 'dwd');
  delete process.env.GKX_MCP_POLICY_BASE;
}

{
  const calls = callsFor(500, { code: 1, msg: 'simulate backend down' });
  const result = await callTool('policy-apply', { action: 'simulate', scope_code: '4403' });
  assert.equal(result.isError, true);
  assert.match(textOf(result), /simulate backend down/);
  assert.equal(textOf(result).includes('推演得分'), false);
  assert.equal(calls.length, 1);
  assert.match(calls[0].url, /\/policy\/simulate/);
}

{
  const calls = installFetch(async () => jsonResponse(404, { code: 1, msg: 'missing' }));
  const result = await callTool('svc-analysis', { kind: 'models', topic: 'gap' });
  assert.equal(result.isError, true);
  assert.match(textOf(result), /404/);
  assert.match(textOf(result), /GKX_MCP_SVC_BASE/);
  assert.equal(calls.length, 1);
  assert.match(calls[0].url, /gateway\.test/);
}

{
  process.env.GKX_MCP_SVC_BASE = 'http://svc-domain.test';
  const calls = installFetch(async (url) => {
    if (String(url).includes('gateway.test')) return jsonResponse(404, { msg: 'no route' });
    return jsonResponse(200, { code: 0, data: { metric_id: 'M_SVC', data_source: 'mock', list: [] } });
  });
  const result = await callTool('svc-analysis', { kind: 'indicators' });
  assert.notEqual(result.isError, true, textOf(result));
  assert.equal(calls.length, 2);
  assert.match(calls[1].url, /^http:\/\/svc-domain\.test\/v1\/svc\/indicators/);
  const body = parsed(result);
  assert.equal(body.demo_only, true);
  assert.equal(body.route.demo_only, true);
  delete process.env.GKX_MCP_SVC_BASE;
}

{
  delete process.env.GKX_MCP_API_BASE;
  const calls = callsFor(200, { code: 0, data: {} });
  const result = await callTool('synth-index', { index: 'catalog' });
  assert.equal(result.isError, true);
  assert.match(textOf(result), /GKX_MCP_API_BASE/);
  assert.equal(calls.length, 0);
  process.env.GKX_MCP_API_BASE = 'http://gateway.test/api';
}

{
  process.env.GKX_MCP_API_BASE = 'http://demo-algo-science:8000';
  const calls = callsFor(200, {});
  const result = await callTool('search-industry', { q: '光刻' });
  assert.equal(result.isError, true);
  assert.match(textOf(result), /禁止的进程/);
  assert.equal(calls.length, 0);
  process.env.GKX_MCP_API_BASE = 'http://gateway.test/api';
}

{
  process.env.GKX_MCP_TOKEN = 'test-token-xyz';
  const calls = callsFor(200, { code: 0, data: { metric_id: 'M_KEEP', data_source: 'mock' } });
  const result = await callTool('policy-indicators', { kind: 'sz' });
  assert.equal(calls[0].init.headers.Authorization, 'Bearer test-token-xyz');
  assert.equal(textOf(result).includes('test-token-xyz'), false);
  delete process.env.GKX_MCP_TOKEN;
}

{
  const calls = installFetch(async () => jsonResponse(302, '', { location: 'http://demo-algo-science:8000/internal' }));
  const result = await callTool('search-industry', { q: '光刻' });
  assert.equal(result.isError, true);
  assert.match(textOf(result), /重定向/);
  assert.equal(calls.length, 1);
}

{
  clearMintedToken();
  const calls = callsFor(424, { code: 1, msg: 'token expired' });
  const result = await callTool('chain-panorama', { chain_id: 'INB1701' });
  assert.equal(result.isError, true);
  assert.match(textOf(result), /换票失败/);
  assert.equal(calls.length, 2);
  assert.match(calls[1].url, /\/auth\/oauth2\/token$/);
  assert.equal(calls[1].init.method, 'POST');
  assert.equal(textOf(result).includes('pig'), false);
}

{
  clearMintedToken();
  process.env.GKX_MCP_TOKEN = 'stale-token';
  const calls = installFetch(async (url, init) => {
    if (String(url).includes('/auth/oauth2/token')) {
      return jsonResponse(200, { access_token: 'fresh-token', expires_in: 3600 });
    }
    if (init.headers.Authorization === 'Bearer stale-token') return jsonResponse(424, { msg: '用户凭证已过期' });
    return jsonResponse(200, { code: 0, data: [{ chain_id: 'INB1701', chain_name: '新一代信息技术' }] });
  });
  const result = await callTool('search-industry', { q: '信息' });
  assert.notEqual(result.isError, true, textOf(result));
  assert.match(textOf(result), /INB1701/);
  assert.equal(textOf(result).includes('fresh-token'), false);
  assert.equal(calls.length, 3);
  assert.equal(calls[2].init.headers.Authorization, 'Bearer fresh-token');
  const again = await callTool('search-industry', { q: '信息' });
  assert.notEqual(again.isError, true, textOf(again));
  assert.equal(calls.length, 4);
  assert.equal(calls.filter((call) => String(call.url).includes('/auth/oauth2/token')).length, 1);
  delete process.env.GKX_MCP_TOKEN;
  clearMintedToken();
}

const missing = JSON.parse(await handleRequest(9, 'nope', {}));
assert.equal(missing.error.code, -32601);

restoreEnv();
process.stdout.write('7chain-mcp-selfcheck: ok\n');
