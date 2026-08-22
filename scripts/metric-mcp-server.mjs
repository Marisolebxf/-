#!/usr/bin/env node
/**
 * metric-mcp-server.mjs — read-only MCP for metrics/registry
 *
 * Tools: metric-get / metric-query / metric-summary
 * Does not write YAML. Identity = seed 8件套; D1–D4 = matrix.
 *
 * Usage (.cursor/mcp.json):
 *   "metric-registry": {
 *     "type": "stdio",
 *     "command": "node",
 *     "args": ["scripts/metric-mcp-server.mjs"]
 *   }
 */

import { getMetric, queryMetrics, summarizeMetrics } from './lib/metric-registry-lib.mjs';

const MCPServer = {
  name: 'metric-registry-mcp',
  version: '1.0.0',
};

function jsonRpcError(id, code, message) {
  return JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
}

function jsonRpcResult(id, result) {
  return JSON.stringify({ jsonrpc: '2.0', id, result });
}

function asText(obj) {
  return { content: [{ type: 'text', text: JSON.stringify(obj, null, 2) }] };
}

const TOOLS = {};

TOOLS['metric-get'] = {
  description:
    '按 metric_id 查询单条指标：8 件套（9 项身份，含 algorithm_type）+ D1–D4 接入状态。缺 seed 或缺矩阵会诚实标 found。未填 algorithm_type 视为 UNKNOWN。禁止把 D1–D4 说成 8 件套字段。',
  inputSchema: {
    type: 'object',
    properties: {
      metric_id: {
        type: 'string',
        description: '指标 ID，如 M_ENT_TOTAL_COUNT（大小写不敏感）',
      },
    },
    required: ['metric_id'],
  },
  handler(args) {
    const id = args?.metric_id || args?.id;
    return asText(getMetric(id));
  },
};

TOOLS['metric-query'] = {
  description:
    '模糊查询指标列表（id / 中文名 / 口径摘要）。可按 domain、D1、D4、algorithm_type 筛选。默认 summary，不要用来倾倒全表。',
  inputSchema: {
    type: 'object',
    properties: {
      q: { type: 'string', description: '模糊关键词（metric_id / 中文名 / definition）' },
      domain: { type: 'string', description: '域代码，如 ENT / CHAIN / SVC / POLICY / SYNTH / TNIE' },
      d1: {
        type: 'string',
        description: 'D1 定义状态',
        enum: ['aligned', 'draft', 'missing'],
      },
      d4: {
        type: 'string',
        description: 'D4 接入状态',
        enum: ['mock', 'ingesting', 'live', 'n/a'],
      },
      algorithm_type: {
        type: 'string',
        description: '8 件套第 5 项；未填条目为 UNKNOWN',
        enum: ['STAT', 'COMPUTE', 'MODEL', 'GRAPH', 'third_party', 'MIXED', 'LITERATURE', 'UNKNOWN'],
      },
      found: {
        type: 'string',
        description: '覆盖面：both / seed / matrix / seed_only / matrix_only',
        enum: ['both', 'seed', 'matrix', 'seed_only', 'matrix_only'],
      },
      limit: { type: 'number', description: '返回条数上限，默认 20' },
      fields: {
        type: 'string',
        description: 'summary=列表字段；full=含 kit+readiness',
        enum: ['summary', 'full'],
      },
    },
  },
  handler(args) {
    return asText(queryMetrics(args || {}));
  },
};

TOOLS['metric-summary'] = {
  description:
    '按域 / D1 / D4 / algorithm_type 聚合计数，并给出 seed∩矩阵覆盖。不返回具体指标列表。',
  inputSchema: {
    type: 'object',
    properties: {
      domain: { type: 'string', description: '可选，只统计某一域' },
    },
  },
  handler(args) {
    return asText(summarizeMetrics(args?.domain));
  },
};

function handleRequest(id, method, params) {
  switch (method) {
    case 'initialize':
      return jsonRpcResult(id, {
        protocolVersion: '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: { name: MCPServer.name, version: MCPServer.version },
      });
    case 'notifications/initialized':
      return null;
    case 'tools/list': {
      const tools = Object.entries(TOOLS).map(([name, def]) => ({
        name,
        description: def.description,
        inputSchema: def.inputSchema,
      }));
      return jsonRpcResult(id, { tools });
    }
    case 'tools/call': {
      const { name, arguments: args } = params || {};
      const tool = TOOLS[name];
      if (!tool) return jsonRpcError(id, -32601, `Tool not found: ${name}`);
      const result = tool.handler(args);
      return jsonRpcResult(id, result);
    }
    default:
      return jsonRpcError(id, -32601, `Method not found: ${method}`);
  }
}

let buffer = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  buffer += chunk;
  const lines = buffer.split('\n');
  buffer = lines.pop() || '';
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    let msg;
    try {
      msg = JSON.parse(trimmed);
    } catch {
      process.stderr.write(`Invalid JSON-RPC: ${trimmed.slice(0, 200)}\n`);
      continue;
    }
    const { id, method, params } = msg;
    try {
      const response = handleRequest(id, method, params);
      if (response) process.stdout.write(response + '\n');
    } catch (err) {
      process.stderr.write(`Handler error: ${err.stack || err.message}\n`);
      if (id !== undefined && id !== null) {
        process.stdout.write(jsonRpcError(id, -32603, err.message || 'Internal error') + '\n');
      }
    }
  }
});

process.stdin.on('end', () => process.exit(0));
process.on('uncaughtException', (err) => {
  process.stderr.write(`Uncaught: ${err.stack || err.message}\n`);
  process.exit(1);
});

process.stderr.write(`MCP server "${MCPServer.name}" v${MCPServer.version} started\n`);
