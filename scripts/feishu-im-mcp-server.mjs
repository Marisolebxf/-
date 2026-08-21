#!/usr/bin/env node
/**
 * feishu-im-mcp-server.mjs — Phase-1 outbound Feishu IM for GKX humans.
 *
 * Allowlist = team-roster.yaml ∩ feishu-user-map.yaml.
 * Every send requires a registry task_id. Same person+task is deduped for 30 minutes.
 */
import {
  assertTaskId,
  checkRateLimit,
  formatNotifyText,
  listAllowedHumans,
  loadDotEnv,
  pickNotifyRecipients,
  RATE_WINDOW_MS,
  readTaskNotifyTargets,
  recordSend,
  resolveAllowedHuman,
} from './lib/feishu-im-guard.mjs';
import { sendTextToOpenId } from './lib/feishu-im.mjs';
import { ORCH_ROOT } from './lib/task-registry-lib.mjs';

loadDotEnv(ORCH_ROOT);

const MCPServer = {
  name: 'feishu-im-mcp',
  version: '1.0.0',
};

function jsonRpcError(id, code, message) {
  return JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
}

function jsonRpcResult(id, result) {
  return JSON.stringify({ jsonrpc: '2.0', id, result });
}

function toolText(payload) {
  return { content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }] };
}

async function deliver(person, taskId, text, dryRun) {
  const formatted = formatNotifyText(taskId, text);
  if (!formatted.ok) return formatted;
  const rate = checkRateLimit(person.registry_name, taskId);
  if (!rate.ok) return rate;
  const sent = await sendTextToOpenId(person.feishu_open_id, formatted.text, { dryRun });
  if (!dryRun && sent.ok) recordSend(person.registry_name, taskId);
  return {
    ok: true,
    dry_run: Boolean(dryRun),
    to: person.registry_name,
    name: person.name,
    task_id: taskId,
    message_id: sent.message_id || null,
  };
}

const TOOLS = {};

TOOLS['im-resolve'] = {
  description: '查询可发飞书私信的项目成员（花名册∩飞书映射）。不发消息。',
  inputSchema: {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        description: '真名或 human:真名；省略则列出全部可发成员',
      },
    },
  },
  async handler(args) {
    const name = args?.name;
    if (!name) {
      return toolText({
        window_minutes: RATE_WINDOW_MS / 60000,
        humans: listAllowedHumans(),
      });
    }
    const hit = resolveAllowedHuman(name);
    if (!hit.ok) return toolText({ ok: false, error: hit.error });
    return toolText({
      ok: true,
      name: hit.name,
      registry_name: hit.registry_name,
      mapped: true,
    });
  },
};

TOOLS['im-send'] = {
  description:
    '向花名册成员发飞书私信。必须带 task_id；禁止 open_id。同人同任务 30 分钟内去重。不接触甲方。',
  inputSchema: {
    type: 'object',
    properties: {
      to: {
        type: 'string',
        description: '收件人真名或 human:真名（如 徐滕强）',
      },
      task_id: {
        type: 'string',
        description: 'task-registry 任务 ID',
      },
      text: {
        type: 'string',
        description: '正文。会自动加上 【task_id】 前缀',
      },
      dry_run: {
        type: 'boolean',
        description: '只校验不发送',
        default: false,
      },
    },
    required: ['to', 'task_id', 'text'],
  },
  async handler(args) {
    const idCheck = assertTaskId(args?.task_id);
    if (!idCheck.ok) return toolText(idCheck);
    const task = readTaskNotifyTargets(idCheck.id);
    if (!task.ok) return toolText(task);
    const person = resolveAllowedHuman(args?.to);
    if (!person.ok) return toolText(person);
    const result = await deliver(person, idCheck.id, args?.text, Boolean(args?.dry_run));
    return toolText({ ...result, task_title: task.title, task_status: task.status });
  },
};

TOOLS['im-notify-task'] = {
  description:
    '按任务 supervised_by / claimed_by（仅 human:）发飞书私信。claimed 为 agent 时跳过。必须带正文。',
  inputSchema: {
    type: 'object',
    properties: {
      task_id: { type: 'string', description: 'task-registry 任务 ID' },
      text: { type: 'string', description: '正文' },
      audience: {
        type: 'string',
        enum: ['supervisor', 'claimed', 'both'],
        description: '默认 supervisor',
      },
      dry_run: { type: 'boolean', default: false },
    },
    required: ['task_id', 'text'],
  },
  async handler(args) {
    const task = readTaskNotifyTargets(args?.task_id);
    if (!task.ok) return toolText(task);
    const audience = args?.audience || 'supervisor';
    const recipients = pickNotifyRecipients(task, audience);
    if (!recipients.length) {
      return toolText({
        ok: false,
        error: `没有可发的 human 收件人（audience=${audience} supervised_by=${task.supervised_by || '-'} claimed_by=${task.claimed_by || '-'}）`,
      });
    }
    const sent = [];
    for (const person of recipients) {
      sent.push(await deliver(person, task.id, args?.text, Boolean(args?.dry_run)));
    }
    return toolText({
      ok: sent.every((s) => s.ok),
      task_id: task.id,
      task_title: task.title,
      task_status: task.status,
      audience,
      results: sent,
    });
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
      const { name, arguments: toolArgs } = params || {};
      const tool = TOOLS[name];
      if (!tool) return jsonRpcError(id, -32601, `Tool not found: ${name}`);
      const result = tool.handler(toolArgs);
      if (result && typeof result.then === 'function') {
        result
          .then((res) => {
            process.stdout.write(`${jsonRpcResult(id, res)}\n`);
          })
          .catch((err) => {
            process.stderr.write(`Error in tool ${name}: ${err.stack || err.message}\n`);
            process.stdout.write(`${jsonRpcError(id, -32603, err.message || 'Internal error')}\n`);
          });
        return null;
      }
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
      if (response) process.stdout.write(`${response}\n`);
    } catch (err) {
      process.stderr.write(`Handler error: ${err.stack || err.message}\n`);
      if (id !== undefined && id !== null) {
        process.stdout.write(`${jsonRpcError(id, -32603, err.message || 'Internal error')}\n`);
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
