// 一次性 CLI 包装：通过 stdio JSON-RPC 调用 task-mcp-server.mjs
// 用法: node task-mcp-cli.mjs <toolName> [jsonArgs]
// 仅在 Cursor MCP 面板无法加载 server 时作为应急通道；正常操作仍走 MCP 工具。
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const serverPath = join(__dirname, 'task-mcp-server.mjs');

import { readFileSync } from 'node:fs';

const toolName = process.argv[2];
let argsJson = process.argv[3] || '{}';
if (argsJson.startsWith('@')) {
  argsJson = readFileSync(argsJson.slice(1), 'utf8').replace(/^﻿/, '');
}
if (!toolName) {
  console.error('usage: node task-mcp-cli.mjs <toolName> [jsonArgs]');
  process.exit(2);
}

const child = spawn(process.execPath, [serverPath], { stdio: ['pipe', 'pipe', 'inherit'] });
const rl = createInterface({ input: child.stdout });

let nextId = 1;
const pending = new Map();

function send(method, params) {
  const id = nextId++;
  child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

rl.on('line', (line) => {
  if (!line.trim()) return;
  let msg;
  try { msg = JSON.parse(line); } catch { return; }
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(JSON.stringify(msg.error)));
    else resolve(msg.result);
  }
});

const timeout = setTimeout(() => {
  console.error('timeout waiting for server response');
  child.kill();
  process.exit(1);
}, 60000);

try {
  await send('initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'task-mcp-cli', version: '1.0.0' },
  });
  child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
  const result = await send('tools/call', { name: toolName, arguments: JSON.parse(argsJson) });
  const text = (result.content || []).map((c) => (c.type === 'text' ? c.text : JSON.stringify(c))).join('\n');
  console.log(text);
} finally {
  clearTimeout(timeout);
  child.kill();
}
