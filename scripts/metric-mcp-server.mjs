#!/usr/bin/env node
/**
 * metric-mcp-server.mjs — read-only MCP for metrics/registry
 *
 * Tools: metric-get / metric-query / metric-summary / metric-progress-export / metric-srs-export
 * Does not write seed/matrix YAML. Identity = seed 8件套; D1–D4 = matrix.
 * metric-progress-export / metric-srs-export only overwrite registry/export xlsx.
 *
 * Usage (.cursor/mcp.json):
 *   "metric-registry": {
 *     "type": "stdio",
 *     "command": "node",
 *     "args": ["scripts/metric-mcp-server.mjs"]
 *   }
 */

import { getMetric, queryMetrics, summarizeMetrics } from './lib/metric-registry-lib.mjs';
import { exportMetricProgressBoard } from './lib/metric-progress-export.mjs';
import { exportMetricSrsBoard } from './lib/metric-srs-export.mjs';

const MCPServer = {
  name: 'metric-registry-mcp',
  version: '1.3.0',
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
    '按 metric_id 查询单条指标：8 件套（9 项身份）+ D1–D4 + extras.srs_refs（需规 book/seq/name/brief，不是 8 件套）。未回填 srs_refs 为空列表。禁止把 D1–D4 或 srs_refs 说成 8 件套字段。',
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
      domain: {
        type: 'string',
        description: '域（中文枚举或代码均可）：企业/产业链/产业服务/政策/综合/创新/技术/机构/人才/通用/科技动态，或 ENT/CHAIN/SVC/…',
      },
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
    '按域（中文枚举）/ D1 / D4 / algorithm_type 聚合计数，并给出 seed∩矩阵覆盖与 srs_refs 回填覆盖。不返回具体指标列表。',
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

TOOLS['metric-progress-export'] = {
  description:
    '重新执行「指标进度统计」：按飞书「指标与数据开发进度」同列覆写离线 Excel。模块后有「模块说明」中文列。lifecycle_stage 离线列名「语义层开发阶段」（飞书仍叫「填齐阶段」）。合同集合后有「差集判定」（A2 mapped/missing/other_system/n/a_ops，飞书进度表不加）。合同集合：mapped=F∩L、missing=F−L、注册表有而 A2 未挂=L−F。不写 seed/矩阵 YAML，不调飞书 API。',
  inputSchema: {
    type: 'object',
    properties: {},
  },
  handler() {
    return asText(exportMetricProgressBoard());
  },
};

TOOLS['metric-srs-export'] = {
  description:
    '导出「指标需求来源」完整 Excel：先从 A1/A2 重建 metric-srs-map.yaml，再投影注册表全量 + srs_refs（需规 book/seq/name/brief + 展示/专题）。目录有「来源系统」列，明细有「系统」列。空来源=尚未从 A1/A2 回填，不是无需求。不写 seed/矩阵，不改飞书进度表列。产物 registry/export/指标需求来源.xlsx。',
  inputSchema: {
    type: 'object',
    properties: {},
  },
  handler() {
    return asText(exportMetricSrsBoard());
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
