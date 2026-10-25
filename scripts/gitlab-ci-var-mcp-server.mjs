#!/usr/bin/env node
/**
 * gitlab-ci-var MCP. Token is read from gkx-orchestration/.env.
 * Tool results never include the variable value.
 *
 * .cursor/mcp.json:
 *   "gitlab-ci-var": {
 *     "type": "stdio",
 *     "command": "node",
 *     "args": ["scripts/gitlab-ci-var-mcp-server.mjs"]
 *   }
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { listVariables, loadGitlabEnv, upsertVariable } from './lib/gitlab-ci-var.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');

const MCPServer = { name: 'gitlab-ci-var', version: '1.0.0' };

function jsonRpcError(id, code, message) {
  return JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
}

function jsonRpcResult(id, result) {
  return JSON.stringify({ jsonrpc: '2.0', id, result });
}

function asText(obj) {
  return { content: [{ type: 'text', text: JSON.stringify(obj, null, 2) }] };
}

function env() {
  return loadGitlabEnv(ORCH_ROOT);
}

const TOOLS = {};

TOOLS['gitlab-ci-var-list'] = {
  description:
    '列出一个 GitLab 项目的 CI/CD 变量。只返回名称、masked、protected、raw、environment_scope、value_length，不返回 value。project 用 path_with_namespace（如 sz-gkx/gkx-lumen/lumen-algo-py）或数字 ID。令牌从编排仓 .env 读取，不要当参数传入。',
  inputSchema: {
    type: 'object',
    properties: {
      project: { type: 'string', description: 'path_with_namespace 或数字项目 ID' },
    },
    required: ['project'],
  },
  handler(args) {
    return listVariables(env(), args?.project);
  },
};

TOOLS['gitlab-ci-var-set'] = {
  description:
    '写入或更新一条 GitLab CI/CD 变量。默认 masked=true、protected=false、raw=true、environment_scope=*。响应不含 value。未提供新密钥时不要调用本工具覆盖 ZHIPU_LLM_API_KEY。不要从集群 Secret 读取 api-key 再写入。',
  inputSchema: {
    type: 'object',
    properties: {
      project: { type: 'string', description: 'path_with_namespace 或数字项目 ID' },
      key: { type: 'string', description: '变量名' },
      value: { type: 'string', description: '变量值。调用方不得在对话里复述。' },
      masked: { type: 'boolean', description: '默认 true' },
      protected: { type: 'boolean', description: '默认 false。dev 流水线需要读到时必须保持 false' },
      raw: { type: 'boolean', description: '默认 true' },
      environment_scope: { type: 'string', description: '默认 *' },
      description: { type: 'string', description: '可选说明，不要写入密钥' },
    },
    required: ['project', 'key', 'value'],
  },
  handler(args) {
    return upsertVariable(env(), args?.project, args || {});
  },
};

async function handleRequest(id, method, params) {
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
      const result = await tool.handler(args);
      return jsonRpcResult(id, asText(result));
    }
    default:
      return jsonRpcError(id, -32601, `Method not found: ${method}`);
  }
}

let buffer = '';
let pending = 0;
let ended = false;

function maybeExit() {
  if (!(ended && pending === 0)) return;
  process.stdout.write('', () => process.exit(0));
}

process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  buffer += chunk;
  const lines = buffer.split('\n');
  buffer = lines.pop() || '';
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    pending += 1;
    handleLine(trimmed).finally(() => {
      pending -= 1;
      maybeExit();
    });
  }
});

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
    process.stderr.write(`Handler error: ${err.message}\n`);
    if (id !== undefined && id !== null) {
      process.stdout.write(jsonRpcError(id, -32603, err.message || 'Internal error') + '\n');
    }
  }
}

process.stdin.on('end', () => {
  const rest = buffer.trim();
  buffer = '';
  if (rest) {
    pending += 1;
    handleLine(rest).finally(() => {
      pending -= 1;
      maybeExit();
    });
  }
  ended = true;
  maybeExit();
});
process.on('uncaughtException', (err) => {
  process.stderr.write(`Uncaught: ${err.message}\n`);
  process.exit(1);
});

process.stderr.write(`MCP server "${MCPServer.name}" v${MCPServer.version} started\n`);
