#!/usr/bin/env node
/**
 * Feishu Bitable Webhook Handler (RFC-003 Phase C)
 *
 * POST /internal/feishu-bitable/webhook
 *   - Feishu url_verification challenge
 *   - Bitable automation custom JSON { record_id, task_id?, ... }
 *   - Feishu event subscription (record_id in event)
 *
 * CLI:
 *   node scripts/feishu-bitable-webhook-handler.mjs
 *   node scripts/feishu-bitable-webhook-handler.mjs --once --record-id recxxx
 *   node scripts/feishu-bitable-webhook-handler.mjs --once --task-id ID --status done --dry-run
 */

import crypto from 'node:crypto';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { loadBitableConfig, loadDotEnv, ORCH_ROOT } from './lib/feishu-bitable-config.mjs';
import {
  applyInboundChanges,
  buildInboundChanges,
  processInboundRow,
  resolveTaskByRecordId,
} from './lib/feishu-bitable-inbound.mjs';
import { fetchBitableRecord, feishuTenantToken } from './lib/feishu-open-api.mjs';
import { loadAllTasks } from './lib/task-registry-lib.mjs';
import {
  handleDispatchConfirmIntent,
  handleDispatchRejectIntent,
} from './lib/dispatch-webhook-confirm.mjs';
import {
  handleGapProposalAcceptIntent,
  handleGapProposalRejectIntent,
} from './lib/dispatch-webhook-gap-proposal.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

let writeQueue = Promise.resolve();

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  const logDir = path.join(ORCH_ROOT, 'agent-delivery', '_tmp');
  if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
  fs.appendFileSync(path.join(logDir, 'feishu-webhook-handler.log'), `${line}\n`, 'utf8');
}

function appendAudit(cfg, entry) {
  const rel = cfg.webhook.auditLog.replace(/\//g, path.sep);
  const file = path.join(ORCH_ROOT, rel);
  const dir = path.dirname(file);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(file, `${JSON.stringify({ ts: new Date().toISOString(), ...entry })}\n`, 'utf8');
}

function verifySharedSecret(req, cfg) {
  if (cfg.webhook.skipVerification) return { ok: true, mode: 'skip' };
  const secret = cfg.webhook.signingSecret;
  if (!secret) return { ok: false, reason: 'missing signing secret' };

  const hdr =
    req.headers['x-gkx-webhook-secret'] ||
    req.headers['x-webhook-secret'] ||
    '';
  if (hdr && hdr === secret) return { ok: true, mode: 'header-secret' };

  const auth = req.headers.authorization || '';
  if (auth.startsWith('Bearer ') && auth.slice(7) === secret) {
    return { ok: true, mode: 'bearer' };
  }

  return { ok: false, reason: 'invalid shared secret' };
}

function verifyFeishuSignature(req, rawBody, cfg) {
  const timestamp = req.headers['x-lark-request-timestamp'] || req.headers['x-lark-signature-timestamp'];
  const nonce = req.headers['x-lark-request-nonce'] || req.headers['x-lark-signature-nonce'];
  const signature = req.headers['x-lark-signature'] || req.headers['x-lark-request-signature'];
  const secret = cfg.webhook.signingSecret;
  if (!timestamp || !nonce || !signature || !secret) return false;

  const base = `${timestamp}${nonce}${secret}${rawBody}`;
  const hash = crypto.createHash('sha256').update(base, 'utf8').digest('base64');
  return hash === signature;
}

function verifyRequest(req, rawBody, cfg, parsedBody) {
  if (cfg.webhook.skipVerification) return { ok: true, mode: 'skip' };

  if (verifyFeishuSignature(req, rawBody, cfg)) {
    return { ok: true, mode: 'lark-signature' };
  }

  const token =
    parsedBody?.token ||
    parsedBody?.header?.token ||
    req.headers['x-lark-token'] ||
    '';
  if (cfg.webhook.verificationToken && token === cfg.webhook.verificationToken) {
    return { ok: true, mode: 'verification-token' };
  }

  return verifySharedSecret(req, cfg);
}

function parseJsonBody(rawBody) {
  if (!rawBody) return {};
  try {
    return JSON.parse(rawBody);
  } catch {
    return null;
  }
}

function extractWebhookIntent(body) {
  if (!body || typeof body !== 'object') return {};

  if (body.type === 'url_verification' && body.challenge) {
    return { kind: 'challenge', challenge: body.challenge };
  }

  if (body.challenge && !body.record_id && !body.recordId && !body.event) {
    return { kind: 'challenge', challenge: body.challenge };
  }

  if (body.challenge && (body.type === 'url_verification' || body.schema === '1.0')) {
    return { kind: 'challenge', challenge: body.challenge };
  }

  const action = String(
    body.action || body.event?.action || body.type || '',
  )
    .trim()
    .toLowerCase();

  if (
    action === 'dispatch_confirm' ||
    action === 'dispatch_reject' ||
    action === 'gap_proposal_accept' ||
    action === 'gap_proposal_reject'
  ) {
    const recordId =
      body.record_id ||
      body.recordId ||
      body.event?.record_id ||
      body.data?.record_id ||
      '';
    const appToken =
      body.app_token ||
      body.file_token ||
      body.event?.file_token ||
      body.event?.app_token ||
      '';
    const tableId = body.table_id || body.event?.table_id || body.event?.object?.table_id || '';
    const taskId = body.task_id || body.taskId || body.event?.task_id || '';
    return {
      kind: action,
      recordId: String(recordId || '').trim(),
      appToken: String(appToken || '').trim(),
      tableId: String(tableId || '').trim(),
      taskId: String(taskId || '').trim(),
      rawBody: body,
    };
  }

  const recordId =
    body.record_id ||
    body.recordId ||
    body.event?.record_id ||
    body.event?.object?.record_id ||
    body.data?.record_id ||
    '';

  const appToken =
    body.app_token ||
    body.file_token ||
    body.event?.file_token ||
    body.event?.app_token ||
    '';

  const tableId = body.table_id || body.event?.table_id || body.event?.object?.table_id || '';

  const taskId = body.task_id || body.taskId || body.event?.task_id || '';

  const statusLabel =
    body.status ||
    body.status_label ||
    body.fields?.status ||
    body.event?.fields?.status ||
    '';

  return {
    kind: 'inbound',
    recordId: String(recordId || '').trim(),
    appToken: String(appToken || '').trim(),
    tableId: String(tableId || '').trim(),
    taskId: String(taskId || '').trim(),
    statusLabel: String(statusLabel || '').trim(),
    rawEventType: body.header?.event_type || body.event_type || body.type || '',
  };
}

function assertAllowedTable(cfg, appToken, tableId) {
  if (appToken && cfg.webhook.allowedAppTokens.length && !cfg.webhook.allowedAppTokens.includes(appToken)) {
    throw new Error(`app_token not allowed: ${appToken}`);
  }
  if (tableId && cfg.webhook.allowedTableIds.length && !cfg.webhook.allowedTableIds.includes(tableId)) {
    throw new Error(`table_id not allowed: ${tableId}`);
  }
}

function isPlaceholderRecordId(recordId) {
  if (!recordId) return true;
  const v = String(recordId).trim();
  if (!v) return true;
  if (v.includes('{{') || v.includes('}}')) return true;
  if (!/^rec[a-zA-Z0-9]+$/i.test(v)) return true;
  return false;
}

async function resolveRow(cfg, intent) {
  if (intent.taskId) {
    const row = {
      record_id: intent.recordId || '',
      task_id: intent.taskId,
      title: '',
      status_label: intent.statusLabel,
      sprint_id: '',
      priority: '',
      claimed_by: '',
    };
    if (intent.recordId || !intent.statusLabel) {
      const appId = process.env.FEISHU_APP_ID;
      const appSecret = process.env.FEISHU_APP_SECRET;
      if (appId && appSecret && cfg.webhook.fetchRecordOnRecordId && intent.recordId) {
        const token = await feishuTenantToken(appId, appSecret);
        const fetched = await fetchBitableRecord(
          cfg,
          token,
          intent.recordId,
          intent.appToken || cfg.appToken,
          intent.tableId || cfg.tableId,
        );
        return { ...fetched, ...row, status_label: row.status_label || fetched.status_label };
      }
    }
    return row;
  }

  if (!intent.recordId) throw new Error('missing record_id / task_id');

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) throw new Error('FEISHU_APP_ID / FEISHU_APP_SECRET required to fetch record');

  const token = await feishuTenantToken(appId, appSecret);
  return fetchBitableRecord(
    cfg,
    token,
    intent.recordId,
    intent.appToken || cfg.appToken,
    intent.tableId || cfg.tableId,
  );
}

function gitPullSoft() {
  const branch = spawnSync('git', ['rev-parse', '--abbrev-ref', 'HEAD'], {
    cwd: ORCH_ROOT,
    encoding: 'utf8',
  }).stdout?.trim();
  if (!branch) return;
  spawnSync('git', ['pull', '--rebase', 'origin', branch], { cwd: ORCH_ROOT, encoding: 'utf8' });
}

function runDispatchScan(taskId) {
  const r = spawnSync(
    process.execPath,
    [path.join(ORCH_ROOT, 'scripts', 'coordinator-dispatch.mjs'), 'scan', '--cause-task', taskId],
    { cwd: ORCH_ROOT, encoding: 'utf8', env: process.env },
  );
  if (r.status !== 0) {
    log(`WARN dispatch scan failed for ${taskId}: ${r.stderr || r.stdout}`);
    return false;
  }
  log(`dispatch scan ok: ${taskId}`);
  return true;
}

function runFullDispatchScan() {
  const r = spawnSync(
    process.execPath,
    [path.join(ORCH_ROOT, 'scripts', 'coordinator-dispatch.mjs'), 'scan'],
    { cwd: ORCH_ROOT, encoding: 'utf8', env: process.env },
  );
  if (r.status !== 0) {
    log(`WARN full dispatch scan failed: ${r.stderr || r.stdout}`);
    return false;
  }
  log('full dispatch scan ok');
  return true;
}

function runGitPush(cfg, commitMsg) {
  if (!cfg.webhook.autoGitPush) return;
  const prevMsg = process.env.GKX_GIT_COMMIT_MSG;
  if (commitMsg) process.env.GKX_GIT_COMMIT_MSG = commitMsg;
  const ps1 = path.join(ORCH_ROOT, 'scripts', 'lib', 'git-push-registry.ps1');
  if (process.platform === 'win32') {
    spawnSync('powershell', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1], {
      cwd: ORCH_ROOT,
      encoding: 'utf8',
      env: process.env,
    });
  } else {
    const sh = path.join(ORCH_ROOT, 'scripts', 'lib', 'git-push-registry.sh');
    if (fs.existsSync(sh)) {
      spawnSync('bash', [sh], { cwd: ORCH_ROOT, encoding: 'utf8', env: process.env });
    }
  }
  if (commitMsg) {
    if (prevMsg === undefined) delete process.env.GKX_GIT_COMMIT_MSG;
    else process.env.GKX_GIT_COMMIT_MSG = prevMsg;
  }
}

async function handleDispatchIntent(cfg, intent, opts = {}) {
  assertAllowedTable(cfg, intent.appToken, intent.tableId);

  if (isPlaceholderRecordId(intent.recordId) && !intent.taskId) {
    throw new Error(
      'record_id 无效：飞书自动化未替换变量（勿手打 {{record_id}}；在请求体 JSON 里用「插入变量 → 记录 ID」）。' +
        ` 收到: ${JSON.stringify(intent.recordId || '')}`,
    );
  }

  gitPullSoft();

  let result;
  if (intent.kind === 'dispatch_confirm') {
    result = await handleDispatchConfirmIntent(cfg, intent, opts);
  } else {
    result = await handleDispatchRejectIntent(cfg, intent, opts);
  }

  if (!opts.dryRun && result.action !== 'noop') {
    runGitPush(cfg);
  }

  appendAudit(cfg, { intent, result });
  return result;
}

async function handleGapProposalIntent(cfg, intent, opts = {}) {
  assertAllowedTable(cfg, intent.appToken, intent.tableId);

  if (isPlaceholderRecordId(intent.recordId) && !intent.taskId) {
    throw new Error(
      'record_id 无效：飞书自动化未替换变量（勿手打 {{record_id}}；在请求体 JSON 里用「插入变量 → 记录 ID」）。' +
        ` 收到: ${JSON.stringify(intent.recordId || '')}`,
    );
  }

  gitPullSoft();

  let result;
  if (intent.kind === 'gap_proposal_accept') {
    result = await handleGapProposalAcceptIntent(cfg, intent, opts);
  } else {
    result = await handleGapProposalRejectIntent(cfg, intent, opts);
  }

  if (!opts.dryRun && result.action !== 'noop') {
    const msg = `feat(registry): ${result.action} ${result.taskId || result.proposalId} [agent:coordinator]`;
    runGitPush(cfg, msg);
    if (intent.kind === 'gap_proposal_accept') {
      runFullDispatchScan();
    }
  }

  appendAudit(cfg, { intent, result });
  return result;
}

async function handleInboundIntent(cfg, intent, opts = {}) {
  assertAllowedTable(cfg, intent.appToken, intent.tableId);

  if (isPlaceholderRecordId(intent.recordId) && !intent.taskId) {
    throw new Error(
      'record_id 无效：飞书自动化未替换变量（勿手打 {{record_id}}；在请求体 JSON 里用「插入变量 → 记录 ID」）。' +
        ` 收到: ${JSON.stringify(intent.recordId || '')}`,
    );
  }

  if (!intent.taskId && intent.recordId) {
    const byRec = resolveTaskByRecordId(intent.recordId);
    if (byRec) intent.taskId = byRec.id;
  }

  const row = await resolveRow(cfg, intent);
  if (!row.task_id && intent.recordId) {
    const byRec = resolveTaskByRecordId(intent.recordId);
    if (byRec) row.task_id = byRec.id;
  }

  gitPullSoft();

  if (!cfg.inbound?.enabled) {
    const skipped = {
      action: 'skipped',
      reason: 'inbound disabled (feishu display-only); kanban edits do not write registry',
    };
    appendAudit(cfg, { intent, result: skipped });
    log(`inbound skipped: ${skipped.reason}`);
    return skipped;
  }

  const result = processInboundRow(row, cfg, {
    dryRun: opts.dryRun,
    validateTransitions: cfg.webhook.validateTransitions,
    source: 'feishu_bitable_webhook',
  });

  if (result.action === 'updated' && result.statusBecameDone && !opts.dryRun) {
    runDispatchScan(result.taskId);
  }

  if (result.action === 'updated' && !opts.dryRun) {
    runGitPush(cfg);
  }

  appendAudit(cfg, { intent, result });
  return result;
}

async function handleWebhookRequest(req, rawBody, cfg) {
  const parsed = parseJsonBody(rawBody);
  if (parsed === null) {
    return { status: 400, body: { ok: false, error: 'invalid json' } };
  }

  const intent = extractWebhookIntent(parsed);
  if (intent.kind === 'challenge') {
    return { status: 200, body: { challenge: intent.challenge } };
  }

  const auth = verifyRequest(req, rawBody, cfg, parsed);
  if (!auth.ok) {
    appendAudit(cfg, { error: 'unauthorized', reason: auth.reason, intent });
    return { status: 401, body: { ok: false, error: 'unauthorized' } };
  }

  try {
    const handler =
      intent.kind === 'dispatch_confirm' || intent.kind === 'dispatch_reject'
        ? () => handleDispatchIntent(cfg, intent)
        : intent.kind === 'gap_proposal_accept' || intent.kind === 'gap_proposal_reject'
          ? () => handleGapProposalIntent(cfg, intent)
          : () => handleInboundIntent(cfg, intent);
    const result = await enqueueWrite(handler);
    return { status: 200, body: { ok: true, auth: auth.mode, result } };
  } catch (e) {
    appendAudit(cfg, { error: e.message, intent });
    log(`ERROR inbound: ${e.message}`);
    return { status: 422, body: { ok: false, error: e.message } };
  }
}

function enqueueWrite(fn) {
  const run = writeQueue.then(fn);
  writeQueue = run.catch(() => {});
  return run;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function sendJson(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(payload),
  });
  res.end(payload);
}

async function startServer(cfg) {
  const webhookPath = cfg.webhook.path.startsWith('/')
    ? cfg.webhook.path
    : `/${cfg.webhook.path}`;

  const server = http.createServer(async (req, res) => {
    try {
      if (req.method === 'GET' && (req.url === '/health' || req.url === `${webhookPath}/health`)) {
        return sendJson(res, 200, { ok: true, service: 'feishu-bitable-webhook' });
      }

      if (req.method === 'POST' && (req.url === webhookPath || req.url === `${webhookPath}/`)) {
        const rawBody = await readBody(req);
        const out = await handleWebhookRequest(req, rawBody, cfg);
        return sendJson(res, out.status, out.body);
      }

      sendJson(res, 404, { ok: false, error: 'not found' });
    } catch (e) {
      log(`ERROR server: ${e.message}`);
      sendJson(res, 500, { ok: false, error: 'internal error' });
    }
  });

  const host = process.env.FEISHU_BITABLE_WEBHOOK_HOST || cfg.webhook.host;
  const port = Number(process.env.FEISHU_BITABLE_WEBHOOK_PORT || cfg.webhook.port);

  await new Promise((resolve) => server.listen(port, host, resolve));
  log(`listening http://${host}:${port}${webhookPath}`);
  log(`health: http://${host}:${port}/health`);
  return server;
}

function parseCli(argv) {
  const out = {
    once: false,
    recordId: '',
    taskId: '',
    status: '',
    dryRun: false,
    help: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    switch (a) {
      case '--once':
        out.once = true;
        break;
      case '--record-id':
        out.recordId = next();
        break;
      case '--task-id':
        out.taskId = next();
        break;
      case '--status':
        out.status = next();
        break;
      case '--dry-run':
        out.dryRun = true;
        break;
      case '--help':
      case '-h':
        out.help = true;
        break;
      default:
        break;
    }
  }
  return out;
}

async function runOnce(cfg, cli) {
  const intent = {
    kind: 'inbound',
    recordId: cli.recordId,
    taskId: cli.taskId,
    statusLabel: cli.status,
    appToken: cfg.appToken,
    tableId: cfg.tableId,
  };

  if (cli.taskId && cli.status && !cli.recordId) {
    const { byId } = loadAllTasks();
    const task = byId.get(cli.taskId);
    if (!task) throw new Error(`task not found: ${cli.taskId}`);
    const newSt = cfg.statusReverse[cli.status] || cli.status;
    const row = {
      record_id: task.record_id || '',
      status_label: cfg.statusMap[newSt] || cli.status,
      title: task.title,
      sprint_id: task.sprint_id,
      priority: task.priority,
      claimed_by: task.claimed_by,
    };
    const { changes, rejects } = buildInboundChanges(row, task, cfg, {
      validateTransitions: cfg.webhook.validateTransitions,
    });
    if (rejects.length) throw new Error(rejects.join('; '));
    const result = applyInboundChanges(cli.taskId, changes, {
      dryRun: cli.dryRun,
      source: 'feishu_bitable_webhook_cli',
    });
    if (result.statusBecameDone && !cli.dryRun) runDispatchScan(cli.taskId);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  const result = await handleInboundIntent(cfg, intent, { dryRun: cli.dryRun });
  console.log(JSON.stringify(result, null, 2));
}

async function main() {
  loadDotEnv();
  const cfg = loadBitableConfig();

  const cli = parseCli(process.argv.slice(2));
  if (cli.help) {
    console.log(`Usage:
  node scripts/feishu-bitable-webhook-handler.mjs
  node scripts/feishu-bitable-webhook-handler.mjs --once --record-id recxxx
  node scripts/feishu-bitable-webhook-handler.mjs --once --task-id TASK --status 已完成 [--dry-run]
`);
    process.exit(0);
  }

  if (cli.once) {
    await runOnce(cfg, cli);
    return;
  }

  if (!cfg.webhook.enabled) {
    log('webhook.enabled=false in feishu-bitable.yaml — enable or use --once');
    process.exit(1);
  }

  await startServer(cfg);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
