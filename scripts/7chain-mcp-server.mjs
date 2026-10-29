#!/usr/bin/env node
/**
 * gkx-7chain MCP · M1（CROSS-MCP-7CHAIN-L02）
 *
 * stdio JSON-RPC，循环同 scripts/metric-mcp-server.mjs。
 * HTTP 只打 GKX_MCP_API_BASE（demo 网关）。search-policy 的关键词列表与详情改打
 * GKX_MCP_POLICY_BASE（lumen 网关 Java /policy/topic/v1/policy/search 与 /docs）。
 * 禁止直连 demo-algo-* / lumen-algo-py / Neo4j，禁止直连 Python /internal/*。
 * 现网入口：NodePort 反代 /api → demo-platform-gateway。
 * 产业链 Java 门面在 gkx-innov /v1/industry/**；全局过滤器已剥第一段，
 * 所以网关路径是 /innov/v1/industry/**。/topic 路由再配 StripPrefix 会剥成 /industry/** 并 404。
 * /chain/v1/chain/** 落到 /v1/chain/**，控制器不在那里。
 *
 * search-enterprise 走专题页智能搜索：POST /enterprise/topic/v1/search/smart。
 * 基址与政策检索相同（GKX_MCP_POLICY_BASE，lumen 网关）；可用 GKX_MCP_ENTERPRISE_BASE 覆盖。
 * ponytail: ent-recommend 把 industry 原样放进 body。现网 attract/cultivate 不按 industry 过滤，
 * 名单以返回为准，MCP 不编排名。
 */

import { randomBytes } from 'node:crypto';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const MCPServer = { name: 'gkx-7chain', version: '1.0.0' };
const NODE_CAP = 80;
const DEFAULT_TIMEOUT_MS = 30000;
const BANNED = ['demo-algo', 'lumen-algo', 'entan-py', 'innov-py', 'neo4j'];

const CHAIN_ASPECTS = [
  'cycle', 'key-nodes', 'bottlenecks', 'region-index',
  'shenzhen', 'roadmap', 'recommendation', 'competitiveness',
];
const EVAL_SUB = { tech: 'technology', business: 'business', competitiveness: 'competitiveness' };
const SYNTH_VITALITY = 'M_SYNTH_186_1';
const SYNTH_ELEMENTS = {
  composite: 'M_SYNTH_190_1',
  type: 'M_SYNTH_187_1',
  level: 'M_SYNTH_188_1',
  domain: 'M_SYNTH_189_1',
};
const SYNTH_COLLAB = 'M_SYNTH_191_1';
const SVC_INDICATOR_TOPIC = { field: 'layout', trend: 'new', shenzhen: 'sz' };
const SVC_MODEL_TOPIC = { tech: 'tech', gap: 'gap', attract: 'attract', cultivate: 'cultivate' };

let httpFetch = null;
let mintedToken = '';
let mintedUntil = 0;

export function setHttpFetch(fn) {
  httpFetch = fn;
}

export function clearMintedToken() {
  mintedToken = '';
  mintedUntil = 0;
}

function getFetch() {
  return httpFetch || globalThis.fetch;
}

function jsonRpcError(id, code, message) {
  return JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
}

function jsonRpcResult(id, result) {
  return JSON.stringify({ jsonrpc: '2.0', id, result });
}

function ok(obj) {
  return { content: [{ type: 'text', text: JSON.stringify(obj, null, 2) }] };
}

function fail(message, extra = {}) {
  return {
    isError: true,
    content: [{ type: 'text', text: JSON.stringify({ error: message, ...extra }, null, 2) }],
  };
}

function enumErr(name, value, allowed) {
  return `${name} 必须是 ${allowed.join('|')}，收到 ${JSON.stringify(value)}`;
}

function clampLimit(raw, def, max) {
  if (raw === undefined || raw === null || raw === '') return { value: def };
  const n = Number(raw);
  if (!Number.isInteger(n) || n < 1) return { error: 'limit 必须是正整数' };
  if (n > max) return { error: `limit 上限 ${max}` };
  return { value: n };
}

function assertBase(base, label) {
  if (!base) {
    const err = new Error(`${label} 未设置`);
    err.code = 'NO_BASE';
    throw err;
  }
  let url;
  try {
    url = new URL(base);
  } catch {
    throw new Error(`${label} 不是合法 URL`);
  }
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new Error(`${label} 只允许 http(s)`);
  }
  const low = base.toLowerCase();
  for (const ban of BANNED) {
    if (low.includes(ban)) throw new Error(`${label} 指向禁止的进程（${ban}）`);
  }
  return base.replace(/\/$/, '');
}

function traceHeaders() {
  const traceId = randomBytes(16).toString('hex');
  const spanId = randomBytes(8).toString('hex');
  return {
    traceId,
    headers: {
      'X-Trace-Id': traceId,
      traceparent: `00-${traceId}-${spanId}-01`,
    },
  };
}

function nodeKey(node, index) {
  return node?.id ?? node?.node_id ?? node?.node_key ?? node?.org_id ?? node?.name ?? `i${index}`;
}

function countNodes(payload) {
  let n = 0;
  const walk = (obj) => {
    if (!obj || typeof obj !== 'object') return;
    if (Array.isArray(obj.nodes)) n += obj.nodes.length;
    for (const value of Object.values(obj)) {
      if (value && typeof value === 'object') walk(value);
    }
  };
  walk(payload);
  return n;
}

export function truncateGraph(payload) {
  if (!payload || typeof payload !== 'object') return { payload, truncated: false, node_count: 0 };
  const copy = structuredClone(payload);
  const holders = [];
  const seen = new Set();
  const walk = (obj) => {
    if (!obj || typeof obj !== 'object' || seen.has(obj)) return;
    seen.add(obj);
    if (Array.isArray(obj.nodes) && obj.nodes.length > NODE_CAP) holders.push(obj);
    for (const value of (Array.isArray(obj) ? obj : Object.values(obj))) walk(value);
  };
  walk(copy);
  if (!holders.length) return { payload: copy, truncated: false, node_count: countNodes(copy) };
  for (const holder of holders) {
    const kept = holder.nodes.slice(0, NODE_CAP);
    const ids = new Set(kept.map(nodeKey));
    holder.nodes = kept;
    if (Array.isArray(holder.edges)) {
      holder.edges = holder.edges.filter((edge) => {
        const source = edge?.source ?? edge?.src ?? edge?.from ?? edge?.start;
        const target = edge?.target ?? edge?.dst ?? edge?.to ?? edge?.end;
        if (source == null || target == null) return true;
        return ids.has(source) && ids.has(target);
      });
    }
    holder.truncated = true;
    holder.node_cap = NODE_CAP;
  }
  return { payload: copy, truncated: true, node_count: countNodes(copy) };
}

function currentBearer() {
  if (mintedToken && Date.now() < mintedUntil) return mintedToken;
  return (process.env.GKX_MCP_TOKEN || '').trim();
}

async function mintToken() {
  const root = gatewayBase();
  const url = new URL('auth/oauth2/token', `${root}/`);
  const id = (process.env.GKX_MCP_CLIENT_ID || 'pig').trim();
  const secret = (process.env.GKX_MCP_CLIENT_SECRET || 'pig').trim();
  const { headers } = traceHeaders();
  headers.Authorization = `Basic ${Buffer.from(`${id}:${secret}`).toString('base64')}`;
  headers.Accept = 'application/json';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  const res = await getFetch()(url, {
    method: 'POST',
    headers,
    body: 'grant_type=client_credentials',
    redirect: 'manual',
    signal: AbortSignal.timeout(Number(process.env.GKX_MCP_TIMEOUT_MS) || DEFAULT_TIMEOUT_MS),
  });
  const text = await res.text();
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = null;
  }
  const token = json?.access_token || json?.data?.access_token;
  if (!res.ok || !token) return false;
  mintedToken = String(token);
  const ttl = Number(json.expires_in || json.data?.expires_in) || 3600;
  mintedUntil = Date.now() + Math.max(30, ttl - 60) * 1000;
  return true;
}

async function httpCall(base, method, relPath, { query, body, token } = {}) {
  const root = assertBase(base, 'base');
  const url = new URL(relPath.replace(/^\//, ''), `${root}/`);
  if (url.origin !== new URL(root).origin) throw new Error('拒绝越出配置的基址');
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && value !== '') url.searchParams.set(key, String(value));
    }
  }
  const { traceId, headers } = traceHeaders();
  const bearer = token !== undefined ? token : (process.env.GKX_MCP_TOKEN || '').trim();
  if (bearer) headers.Authorization = `Bearer ${bearer}`;
  headers.Accept = 'application/json';
  const init = {
    method,
    headers,
    redirect: 'manual',
    signal: AbortSignal.timeout(Number(process.env.GKX_MCP_TIMEOUT_MS) || DEFAULT_TIMEOUT_MS),
  };
  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(body);
  }
  const res = await getFetch()(url, init);
  const text = await res.text();
  let json = null;
  if (text) {
    try {
      json = JSON.parse(text);
    } catch {
      json = null;
    }
  }
  const location = res.headers?.get?.('location') || null;
  if (res.status >= 300 && res.status < 400) {
    return {
      ok: false,
      status: res.status,
      json,
      error: `网关返回 ${res.status}，已停止跟随重定向`,
      location,
      traceId,
      method,
      path: `${url.pathname}${url.search}`,
    };
  }
  return {
    ok: res.ok,
    status: res.status,
    json,
    text: json ? undefined : (text || '').slice(0, 500),
    traceId,
    upstreamTraceId: res.headers?.get?.('x-trace-id') || res.headers?.get?.('X-Trace-Id') || null,
    method,
    path: `${url.pathname}${url.search}`,
  };
}

function gatewayBase() {
  return assertBase((process.env.GKX_MCP_API_BASE || '').trim(), 'GKX_MCP_API_BASE');
}

function policyBase() {
  return assertBase((process.env.GKX_MCP_POLICY_BASE || '').trim(), 'GKX_MCP_POLICY_BASE');
}

function enterpriseBase() {
  const raw = (process.env.GKX_MCP_ENTERPRISE_BASE || process.env.GKX_MCP_POLICY_BASE || '').trim();
  if (!raw) {
    const err = new Error('GKX_MCP_ENTERPRISE_BASE 未设置（可与政策检索共用 GKX_MCP_POLICY_BASE）');
    err.code = 'NO_BASE';
    throw err;
  }
  return assertBase(raw, 'GKX_MCP_ENTERPRISE_BASE');
}

function upstreamMessage(res) {
  if (res.error) return res.error;
  if (!res.ok) {
    return res.json?.msg || res.json?.message || res.json?.detail || res.text || `HTTP ${res.status}`;
  }
  const code = res.json?.code;
  if (code !== undefined && code !== null && code !== 0 && code !== '0') {
    return res.json?.msg || res.json?.message || `上游 code=${code}`;
  }
  return null;
}

function callMeta(res, extra = {}) {
  const meta = {
    method: res.method,
    path: res.path,
    status: res.status,
    trace_id: res.traceId,
    upstream_trace_id: res.upstreamTraceId,
    ...extra,
  };
  if (res.authHint) meta.hint = res.authHint;
  else if (res.status === 401 || res.status === 424) meta.hint = '该路由需要环境变量 GKX_MCP_TOKEN，token 不进 git';
  return meta;
}

async function gateway(method, relPath, opts) {
  const first = await httpCall(gatewayBase(), method, relPath, { ...opts, token: currentBearer() });
  if (first.status !== 401 && first.status !== 424) return first;
  const minted = await mintToken();
  if (!minted) {
    first.authHint = 'client_credentials 换票失败。可设 GKX_MCP_CLIENT_ID / GKX_MCP_CLIENT_SECRET，或更新 GKX_MCP_TOKEN';
    return first;
  }
  return httpCall(gatewayBase(), method, relPath, { ...opts, token: mintedToken });
}

function synthBody(args) {
  const body = {};
  if (args.year !== undefined && args.year !== null && args.year !== '') body.year = args.year;
  if (args.region) {
    body.region = args.region;
    if (/省|自治区|特别行政区$/.test(args.region)) body.province = args.region.replace(/省$/, '');
    else body.city = args.region;
  }
  return body;
}

function asArray(json) {
  const data = json?.data ?? json;
  if (Array.isArray(data)) return data;
  for (const key of ['list', 'items', 'rows', 'metrics', 'chains', 'policies']) {
    if (Array.isArray(data?.[key])) return data[key];
  }
  return null;
}

function includesText(value, needle) {
  return JSON.stringify(value).toLowerCase().includes(String(needle).toLowerCase());
}

function finish(route, payload, extra = {}) {
  const cut = truncateGraph(payload);
  return ok({
    route,
    truncated: cut.truncated,
    node_cap: NODE_CAP,
    node_count: cut.node_count,
    ...extra,
    data: cut.payload,
  });
}

function carried(json) {
  const data = json?.data;
  return {
    metric_id: data?.metric_id ?? json?.metric_id,
    data_source: data?.data_source ?? json?.data_source,
  };
}

const TOOLS = {};

function define(name, description, inputSchema, validate, run) {
  TOOLS[name] = { description, inputSchema, validate, run };
}

define(
  'search-enterprise',
  '按专题页「企业查询 / 智能搜索」检索企业。覆盖数据查询 L4 企业查询（US-E1-SCH）。q、industry、region、type 至少一项，拼成一条关键词，与页面智能输入一致（如「固态电池」「固态电池 深圳」）。type 只许 外企|高企|小微|上市。limit 默认 20 上限 50。POST /enterprise/topic/v1/search/smart，body 含 keyword、keywords、q、page、size。基址是 GKX_MCP_ENTERPRISE_BASE，未设时用 GKX_MCP_POLICY_BASE（lumen 网关，不是 demo 图谱）。enterprise_code 取 org_id，可交给 ent-evaluate / ent-diagnose。排序与页面默认相同：competitiveness_score desc。',
  {
    type: 'object',
    properties: {
      q: { type: 'string', description: '智能搜索关键词，可空，但与筛选至少给一项' },
      industry: { type: 'string' },
      region: { type: 'string' },
      type: { type: 'string', enum: ['外企', '高企', '小微', '上市'] },
      limit: { type: 'number', description: '默认 20，上限 50' },
    },
  },
  (args) => {
    if (!args.q && !args.industry && !args.region && !args.type) return 'q、industry、region、type 至少给一项';
    if (args.type && !['外企', '高企', '小微', '上市'].includes(args.type)) return enumErr('type', args.type, ['外企', '高企', '小微', '上市']);
    return clampLimit(args.limit, 20, 50).error;
  },
  async (args) => {
    const limit = clampLimit(args.limit, 20, 50).value;
    const keyword = [args.q, args.industry, args.region, args.type].map((part) => String(part || '').trim()).filter(Boolean).join(' ');
    const base = enterpriseBase();
    const res = await httpCall(base, 'POST', '/enterprise/topic/v1/search/smart', {
      body: {
        keyword,
        keywords: [keyword],
        q: keyword,
        page: 1,
        size: limit,
        page_size: limit,
        sort_field: 'competitiveness_score',
        sort_order: 'desc',
      },
    });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    const data = res.json?.data && typeof res.json.data === 'object' ? res.json.data : {};
    const list = Array.isArray(data.list) ? data.list : [];
    const enterprises = list.slice(0, limit).map((item) => ({
      ...item,
      enterprise_code: item?.org_id || item?.enterprise_code || item?.social_credit_code || null,
      name: item?.name_cn || item?.name || null,
    }));
    return finish(callMeta(res), {
      enterprises,
      total: data.total ?? enterprises.length,
      page: data.page ?? 1,
      size: data.size ?? limit,
      mode: 'smart',
      ...carried(res.json),
    });
  },
);

define(
  'search-industry',
  '按产业名、链名或同义词检索产业链，返回 chain_id。覆盖数据查询 L4 产业查询。q 必填，limit 默认 10。后端 GET /innov/v1/industry/list（Java /v1/industry/list）；清单无关键词参数时由 MCP 做包含匹配。不返回图谱或瓶颈。',
  {
    type: 'object',
    properties: {
      q: { type: 'string', description: '链名或同义词，必填' },
      limit: { type: 'number', description: '默认 10' },
    },
    required: ['q'],
  },
  (args) => {
    if (!args.q || !String(args.q).trim()) return 'q 必填';
    return clampLimit(args.limit, 10, 50).error;
  },
  async (args) => {
    const limit = clampLimit(args.limit, 10, 50).value;
    const res = await gateway('GET', '/innov/v1/industry/list');
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    const list = (asArray(res.json) || []).filter((item) => includesText(item, args.q)).slice(0, limit);
    return finish(callMeta(res), { chains: list, ...carried(res.json) });
  },
);

define(
  'search-policy',
  '按标题或关键词检索政策，并可按效力层级、产业词筛选；或用 subject_id 反查可匹配政策。覆盖数据查询 L4 政策查询。limit 默认 20。关键词列表走 lumen Java GET /policy/topic/v1/policy/search（q 与 keyword 同词，与专题页智能检索一致），再对每条 GET /policy/topic/v1/policy/docs/{id}，详情里的 content 原样带回。基址是 GKX_MCP_POLICY_BASE，不是 demo mock 清单。反查仍走 demo GET /policy/v1/policy/match。时序和区域对比用 policy-indicators。',
  {
    type: 'object',
    properties: {
      q: { type: 'string' },
      level: { type: 'string', enum: ['国家', '省', '市'] },
      industry: { type: 'string' },
      subject_id: { type: 'string' },
      subject_type: { type: 'string' },
      limit: { type: 'number', description: '默认 20' },
    },
  },
  (args) => {
    if (args.level && !['国家', '省', '市'].includes(args.level)) return enumErr('level', args.level, ['国家', '省', '市']);
    if (!args.q && !args.level && !args.industry && !args.subject_id) return 'q、level、industry、subject_id 至少给一项';
    return clampLimit(args.limit, 20, 50).error;
  },
  async (args) => {
    const limit = clampLimit(args.limit, 20, 50).value;
    if (args.subject_id) {
      const res = await gateway('GET', '/policy/v1/policy/match', {
        query: { subject_id: args.subject_id, subject_type: args.subject_type, limit },
      });
      const msg = upstreamMessage(res);
      if (msg) return fail(String(msg), { route: callMeta(res) });
      const rows = (asArray(res.json) || []).slice(0, limit);
      return finish(callMeta(res), { policies: rows, mode: 'match', ...carried(res.json) });
    }
    const base = policyBase();
    const keyword = [args.q, args.industry].map((part) => String(part || '').trim()).filter(Boolean).join(' ');
    const res = await httpCall(base, 'GET', '/policy/topic/v1/policy/search', {
      query: { q: keyword, keyword, level: args.level, limit },
    });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    const data = res.json?.data && typeof res.json.data === 'object' ? res.json.data : {};
    const items = Array.isArray(data.items) ? data.items.slice(0, limit) : [];
    const policies = await Promise.all(items.map((item) => withPolicyDetail(base, item)));
    return finish(callMeta(res), {
      policies,
      total: data.total,
      honesty: data.honesty,
      mode: 'search',
      ...carried(res.json),
    });
  },
);

async function withPolicyDetail(base, item) {
  const id = item?.policy_id || item?.id;
  if (!id) return { ...item, detail_error: '缺少 policy_id' };
  const doc = await httpCall(base, 'GET', `/policy/topic/v1/policy/docs/${encodeURIComponent(id)}`);
  const docMsg = upstreamMessage(doc);
  if (docMsg) return { ...item, detail_error: String(docMsg) };
  const payload = doc.json?.data;
  const detail = payload?.item;
  if (!detail || typeof detail !== 'object') {
    return { ...item, detail_error: '详情为空', detail_honesty: payload?.honesty };
  }
  return { ...item, ...detail, detail_honesty: payload?.honesty };
}

define(
  'synth-index',
  '计算区域创新活力（M_SYNTH_186_1）或创新要素（默认 M_SYNTH_190_1，分维 type/level/domain = M_SYNTH_187_1/188_1/189_1），或列出综合指标目录。覆盖区域创新活力分析与区域创新要素分析。index=vitality|elements|catalog。catalog 不需要区域。每条分数保留 metric_id。缺维不补 0。8 件套另调 metric-get。',
  {
    type: 'object',
    properties: {
      index: { type: 'string', enum: ['vitality', 'elements', 'catalog'] },
      region: { type: 'string' },
      year: { type: 'number' },
      facet: { type: 'string', enum: ['type', 'level', 'domain', 'composite'], description: 'elements 默认 composite' },
    },
    required: ['index'],
  },
  (args) => {
    if (!['vitality', 'elements', 'catalog'].includes(args.index)) return enumErr('index', args.index, ['vitality', 'elements', 'catalog']);
    if (args.facet && !SYNTH_ELEMENTS[args.facet]) return enumErr('facet', args.facet, Object.keys(SYNTH_ELEMENTS));
    return null;
  },
  async (args) => {
    if (args.index === 'catalog') {
      const res = await gateway('GET', '/entan/v1/synth-metric/catalog');
      const msg = upstreamMessage(res);
      if (msg) return fail(String(msg), { route: callMeta(res) });
      return finish(callMeta(res), res.json?.data ?? res.json);
    }
    const metricId = args.index === 'vitality' ? SYNTH_VITALITY : SYNTH_ELEMENTS[args.facet || 'composite'];
    const res = await gateway('POST', `/entan/v1/synth-metric/metric/${metricId}/compute`, { body: synthBody(args) });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res), metric_id: metricId });
    return finish(callMeta(res), res.json?.data ?? res.json, { metric_id: metricId });
  },
);

define(
  'synth-collab',
  '区域创新协同。action=index 计算 M_SYNTH_191_1（与 M_SYNTH_COLLAB_INDEX 同核）；action=graph 返回企业—机构—人才合作网络。region 必填。hops 默认 1 上限 2。图谱默认截断 80 个节点并标 truncated。完整度不含服务机构。',
  {
    type: 'object',
    properties: {
      action: { type: 'string', enum: ['index', 'graph'] },
      region: { type: 'string' },
      year: { type: 'number' },
      center: { type: 'string' },
      hops: { type: 'number', description: '默认 1，上限 2' },
      industry: { type: 'string' },
    },
    required: ['action', 'region'],
  },
  (args) => {
    if (!['index', 'graph'].includes(args.action)) return enumErr('action', args.action, ['index', 'graph']);
    if (!args.region) return 'region 必填';
    if (args.hops !== undefined && args.hops !== null && args.hops !== '') {
      const hops = Number(args.hops);
      if (!Number.isInteger(hops) || hops < 1 || hops > 2) return 'hops 默认 1，上限 2';
    }
    return null;
  },
  async (args) => {
    if (args.action === 'index') {
      const res = await gateway('POST', `/entan/v1/synth-metric/metric/${SYNTH_COLLAB}/compute`, { body: synthBody(args) });
      const msg = upstreamMessage(res);
      if (msg) return fail(String(msg), { route: callMeta(res), metric_id: SYNTH_COLLAB });
      return finish(callMeta(res), res.json?.data ?? res.json, { metric_id: SYNTH_COLLAB });
    }
    const hops = args.hops || 1;
    const query = { center: args.center, hops, limit: NODE_CAP, industry: args.industry, region: args.region };
    const graph = await gateway('GET', '/industry-comp/v1/comp/graph', { query });
    const graphMsg = upstreamMessage(graph);
    if (graphMsg) return fail(String(graphMsg), { route: callMeta(graph) });
    const metrics = await gateway('GET', '/industry-comp/v1/comp/graph/metrics', { query });
    const viz = await gateway('GET', '/industry-comp/v1/comp/graph/viz', { query });
    return finish(callMeta(graph), {
      graph: graph.json?.data ?? graph.json,
      metrics: upstreamMessage(metrics) ? undefined : (metrics.json?.data ?? metrics.json),
      metrics_error: upstreamMessage(metrics) || undefined,
      viz: upstreamMessage(viz) ? undefined : (viz.json?.data ?? viz.json),
      viz_error: upstreamMessage(viz) || undefined,
      data_source: graph.json?.data?.data_source,
    });
  },
);

define(
  'ent-evaluate',
  '对 1～20 家企业按技术力、商业力或竞争力打分。覆盖企业技术力/商业力/竞争力评估。sub_type=tech|business|competitiveness（请求后端时 tech 映射为 technology）。POST /entan/v1/evaluation/compute。分数字段保留 metric_id。不生成雷达图图片。权重沿用后端默认。',
  {
    type: 'object',
    properties: {
      enterprise_codes: { type: 'array', items: { type: 'string' }, description: '1～20 个企业码' },
      sub_type: { type: 'string', enum: ['tech', 'business', 'competitiveness'] },
    },
    required: ['enterprise_codes', 'sub_type'],
  },
  (args) => {
    if (!Array.isArray(args.enterprise_codes) || args.enterprise_codes.length < 1 || args.enterprise_codes.length > 20) {
      return 'enterprise_codes 必填，1～20 个';
    }
    if (!EVAL_SUB[args.sub_type]) return enumErr('sub_type', args.sub_type, Object.keys(EVAL_SUB));
    return null;
  },
  async (args) => {
    const res = await gateway('POST', '/entan/v1/evaluation/compute', {
      body: { enterprise_codes: args.enterprise_codes, sub_type: EVAL_SUB[args.sub_type] },
    });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    return finish(callMeta(res), res.json?.data ?? res.json);
  },
);

define(
  'ent-recommend',
  '按目标产业推荐招引（全国）或培育（深圳）企业。覆盖招引企业推荐、培育企业推荐。kind=attract|cultivate，industry 必填，limit 默认 10 上限 30。POST /entan/v1/recommend/{kind}。名单是模型推荐，不是已签约对象；返回保留模型名与数据来源。',
  {
    type: 'object',
    properties: {
      kind: { type: 'string', enum: ['attract', 'cultivate'] },
      industry: { type: 'string' },
      limit: { type: 'number', description: '默认 10，上限 30' },
      region: { type: 'string', description: 'attract 默认全国，cultivate 固定深圳' },
    },
    required: ['kind', 'industry'],
  },
  (args) => {
    if (!['attract', 'cultivate'].includes(args.kind)) return enumErr('kind', args.kind, ['attract', 'cultivate']);
    if (!args.industry || !String(args.industry).trim()) return 'industry 必填';
    return clampLimit(args.limit, 10, 30).error;
  },
  async (args) => {
    const limit = clampLimit(args.limit, 10, 30).value;
    const region = args.region || (args.kind === 'cultivate' ? '深圳' : '全国');
    const res = await gateway('POST', `/entan/v1/recommend/${args.kind}`, {
      body: { industry: args.industry, limit, region },
    });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    return finish(callMeta(res), res.json?.data ?? res.json, { requested: { industry: args.industry, region, limit } });
  },
);

define(
  'ent-diagnose',
  '单家或一组企业的诊断、排名、综合分或风险。覆盖企业发展痛难点（P0）以及现状/排名/风险近似。action=diagnose|rank|score|risk。diagnose/score/risk 需要 enterprise_code；rank 需要 industry 或 region。GET /entan/v1/diagnosis|ranking|score|risk。现状分析是排名加区域筛选的近似，不是独立深圳报表。',
  {
    type: 'object',
    properties: {
      action: { type: 'string', enum: ['diagnose', 'rank', 'score', 'risk'] },
      enterprise_code: { type: 'string' },
      industry: { type: 'string' },
      region: { type: 'string' },
    },
    required: ['action'],
  },
  (args) => {
    if (!['diagnose', 'rank', 'score', 'risk'].includes(args.action)) return enumErr('action', args.action, ['diagnose', 'rank', 'score', 'risk']);
    if (args.action === 'rank') {
      if (!args.industry && !args.region) return 'rank 需要 industry 或 region';
      return null;
    }
    if (!args.enterprise_code) return `${args.action} 需要 enterprise_code`;
    return null;
  },
  async (args) => {
    const path = { diagnose: '/entan/v1/diagnosis', rank: '/entan/v1/ranking', score: '/entan/v1/score', risk: '/entan/v1/risk' }[args.action];
    const query = { limit: 20 };
    if (args.action === 'rank') {
      query.dim = 'overall';
      if (args.industry) query.chain = args.industry;
      if (args.region) query.city = args.region;
    } else {
      query.keyword = args.enterprise_code;
      if (args.industry) query.chain = args.industry;
      if (args.region) query.city = args.region;
    }
    const res = await gateway('GET', path, { query });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    return finish(callMeta(res), res.json?.data ?? res.json);
  },
);

define(
  'chain-panorama',
  '一条产业链的环节、连线、断点。覆盖产业链全景图谱。chain_id 必填。GET /innov/v1/industry/{chain_id}/panorama（Java /v1/industry/{id}/panorama）。节点超过 80 截断并标 truncated。不渲染图谱。',
  {
    type: 'object',
    properties: { chain_id: { type: 'string' } },
    required: ['chain_id'],
  },
  (args) => {
    if (!args.chain_id || !String(args.chain_id).trim()) return 'chain_id 必填';
    if (!/^[\w.-]+$/.test(args.chain_id)) return 'chain_id 含非法字符';
    return null;
  },
  async (args) => {
    const res = await gateway('GET', `/innov/v1/industry/${args.chain_id}/panorama`);
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    return finish(callMeta(res), res.json?.data ?? res.json);
  },
);

define(
  'chain-analyze',
  '对一条链只算一个视角：cycle|key-nodes|bottlenecks|region-index|shenzhen|roadmap|recommendation|competitiveness。覆盖产业周期、关键环节、瓶颈（P0）以及区域指数、深圳对比、发展路径、推荐、竞争力（P1）。GET /innov/v1/industry/{chain_id}/{aspect}。保留 metric_id 与 generated_by，不把生成文本改写成已核实事实。',
  {
    type: 'object',
    properties: {
      chain_id: { type: 'string' },
      aspect: { type: 'string', enum: CHAIN_ASPECTS },
    },
    required: ['chain_id', 'aspect'],
  },
  (args) => {
    if (!args.chain_id || !/^[\w.-]+$/.test(String(args.chain_id))) return 'chain_id 必填且只能含字母数字._-';
    if (Array.isArray(args.aspect) || String(args.aspect || '').includes(',')) return '一次 chain-analyze 只算一个 aspect';
    if (!CHAIN_ASPECTS.includes(args.aspect)) return enumErr('aspect', args.aspect, CHAIN_ASPECTS);
    return null;
  },
  async (args) => {
    const res = await gateway('GET', `/innov/v1/industry/${args.chain_id}/${args.aspect}`);
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    return finish(callMeta(res), res.json?.data ?? res.json);
  },
);

define(
  'policy-indicators',
  '政策密度、区域对比或深圳现状。覆盖政策时序、区域政策对比、深圳政策现状。kind=timeseries|national|sz|level|type|all。GET /policy/v1/policy/indicators。all 只在明确要总览时使用。口径以返回中的 metric_id 为准。',
  {
    type: 'object',
    properties: {
      kind: { type: 'string', enum: ['timeseries', 'national', 'sz', 'level', 'type', 'all'] },
      industry: { type: 'string' },
      tech: { type: 'string' },
    },
    required: ['kind'],
  },
  (args) => {
    const kinds = ['timeseries', 'national', 'sz', 'level', 'type', 'all'];
    if (!kinds.includes(args.kind)) return enumErr('kind', args.kind, kinds);
    return null;
  },
  async (args) => {
    const res = await gateway('GET', '/policy/v1/policy/indicators', {
      query: { kind: args.kind, industry_code: args.industry, tech: args.tech },
    });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res) });
    return finish(callMeta(res), res.json?.data ?? res.json);
  },
);

define(
  'policy-apply',
  '政策条款解析、主体匹配或效果推演。增值能力，不在政策三个 L6 内。action=parse 要 policy_id；match 要 subject_id 与 subject_type；simulate 要 scope_code，可选 scenario_id。GET /policy/v1/policy/text/parse、/match、/simulate。simulate 失败时返回后端错误，不编造推演。成功的推演标注 model_output。',
  {
    type: 'object',
    properties: {
      action: { type: 'string', enum: ['parse', 'match', 'simulate'] },
      policy_id: { type: 'string' },
      subject_id: { type: 'string' },
      subject_type: { type: 'string' },
      scope_code: { type: 'string' },
      scenario_id: { type: 'string' },
      limit: { type: 'number' },
    },
    required: ['action'],
  },
  (args) => {
    if (!['parse', 'match', 'simulate'].includes(args.action)) return enumErr('action', args.action, ['parse', 'match', 'simulate']);
    if (args.action === 'parse' && !args.policy_id) return 'parse 需要 policy_id';
    if (args.action === 'match' && (!args.subject_id || !args.subject_type)) return 'match 需要 subject_id 与 subject_type';
    if (args.action === 'simulate' && !args.scope_code) return 'simulate 需要 scope_code';
    return clampLimit(args.limit, 20, 100).error;
  },
  async (args) => {
    const limit = clampLimit(args.limit, 20, 100).value;
    const spec = {
      parse: ['/policy/v1/policy/text/parse', { policy_id: args.policy_id, limit }],
      match: ['/policy/v1/policy/match', { subject_id: args.subject_id, subject_type: args.subject_type, limit }],
      simulate: ['/policy/v1/policy/simulate', { scope_code: args.scope_code, scenario_id: args.scenario_id, limit }],
    }[args.action];
    const res = await gateway('GET', spec[0], { query: spec[1] });
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res), action: args.action });
    const extra = args.action === 'simulate' ? { model_output: true } : {};
    return finish(callMeta(res), res.json?.data ?? res.json, extra);
  },
);

define(
  'svc-analysis',
  '服务机构指标或模型：领域、趋势、技术力、短板、引入、培育、深圳现状。覆盖技术力/短板/引入/培育（P0）与领域/趋势/深圳现状（P1）。kind=indicators|models。models 时 topic 或 model_id 必填。先打网关 /entan/v1/svc/*；若 404 且配置了 GKX_MCP_SVC_BASE，再直调该域 /v1/svc/* 并标 demo_only。模型未就绪时返回后端错误，不编名单。统计数字保留 metric_id。',
  {
    type: 'object',
    properties: {
      kind: { type: 'string', enum: ['indicators', 'models'] },
      topic: { type: 'string', enum: ['field', 'trend', 'tech', 'gap', 'attract', 'cultivate', 'shenzhen'] },
      industry: { type: 'string' },
      org_ids: { type: 'array', items: { type: 'string' } },
      model_id: { type: 'string' },
    },
    required: ['kind'],
  },
  (args) => {
    if (!['indicators', 'models'].includes(args.kind)) return enumErr('kind', args.kind, ['indicators', 'models']);
    if (args.kind === 'models' && !args.topic && !args.model_id) return 'kind=models 时 topic 或 model_id 必填';
    if (args.kind === 'indicators' && args.topic && !SVC_INDICATOR_TOPIC[args.topic]) {
      return `topic=${args.topic} 属于模型，请用 kind=models`;
    }
    if (args.kind === 'models' && args.topic && !SVC_MODEL_TOPIC[args.topic]) {
      return `topic=${args.topic} 属于指标，请用 kind=indicators`;
    }
    return null;
  },
  async (args) => {
    const kindQuery = args.kind === 'indicators'
      ? (SVC_INDICATOR_TOPIC[args.topic] || 'all')
      : (SVC_MODEL_TOPIC[args.topic] || args.model_id || 'all');
    const rel = args.kind === 'indicators' ? '/entan/v1/svc/indicators' : '/entan/v1/svc/models';
    const query = {
      kind: kindQuery,
      industry: args.industry,
      model_id: args.model_id,
      org_ids: Array.isArray(args.org_ids) ? args.org_ids.join(',') : undefined,
      topic: args.topic,
    };
    let res = await gateway('GET', rel, { query });
    let demoOnly = false;
    if (res.status === 404) {
      const svcBase = (process.env.GKX_MCP_SVC_BASE || '').trim();
      if (!svcBase) {
        return fail('网关 404，未配置 GKX_MCP_SVC_BASE。禁止直连算法进程', { route: callMeta(res) });
      }
      const direct = rel.replace(/^\/entan/, '');
      res = await httpCall(svcBase, 'GET', direct, { query });
      demoOnly = true;
    }
    const msg = upstreamMessage(res);
    if (msg) return fail(String(msg), { route: callMeta(res, demoOnly ? { demo_only: true } : {}) });
    return finish(callMeta(res, demoOnly ? { demo_only: true } : {}), res.json?.data ?? res.json, demoOnly ? { demo_only: true } : {});
  },
);

export async function callTool(name, args) {
  const tool = TOOLS[name];
  if (!tool) return fail(`Tool not found: ${name}`);
  const problem = tool.validate(args || {});
  if (problem) return fail(problem);
  try {
    return await tool.run(args || {});
  } catch (err) {
    return fail(err.message || String(err));
  }
}

export function listToolDefs() {
  return Object.entries(TOOLS).map(([name, def]) => ({
    name,
    description: def.description,
    inputSchema: def.inputSchema,
  }));
}

export async function handleRequest(id, method, params) {
  switch (method) {
    case 'initialize':
      return jsonRpcResult(id, {
        protocolVersion: '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: { name: MCPServer.name, version: MCPServer.version },
      });
    case 'notifications/initialized':
      return null;
    case 'tools/list':
      return jsonRpcResult(id, { tools: listToolDefs() });
    case 'tools/call': {
      const { name, arguments: args } = params || {};
      const result = await callTool(name, args);
      return jsonRpcResult(id, result);
    }
    default:
      return jsonRpcError(id, -32601, `Method not found: ${method}`);
  }
}

function launchedAsCli() {
  const arg = process.argv[1];
  if (!arg) return false;
  try {
    return import.meta.url.toLowerCase() === pathToFileURL(path.resolve(arg)).href.toLowerCase();
  } catch {
    return false;
  }
}

function start() {
  let buffer = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => {
    buffer += chunk;
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      void handleLine(trimmed);
    }
  });
  process.stdin.on('end', () => process.exit(0));
  process.on('uncaughtException', (err) => {
    process.stderr.write(`Uncaught: ${err.stack || err.message}\n`);
    process.exit(1);
  });
  process.stderr.write(`MCP server "${MCPServer.name}" v${MCPServer.version} started\n`);
}

async function handleLine(trimmed) {
  let msg;
  try {
    msg = JSON.parse(trimmed);
  } catch {
    process.stderr.write(`Invalid JSON-RPC: ${trimmed.slice(0, 200)}\n`);
    return;
  }
  const { id, method, params } = msg;
  try {
    const response = await handleRequest(id, method, params);
    if (response) process.stdout.write(`${response}\n`);
  } catch (err) {
    process.stderr.write(`Handler error: ${err.stack || err.message}\n`);
    if (id !== undefined && id !== null) {
      process.stdout.write(`${jsonRpcError(id, -32603, err.message || 'Internal error')}\n`);
    }
  }
}

if (launchedAsCli()) start();
