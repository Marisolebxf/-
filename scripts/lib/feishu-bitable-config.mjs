#!/usr/bin/env node
/**
 * Parse agent-delivery/feishu-bitable.yaml (bitable + inbound + webhook).
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ORCH_ROOT = path.resolve(__dirname, '..', '..');
export const CONFIG_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-bitable.yaml');

const DEFAULT_STATUS_MAP = {
  backlog: 'Backlog',
  ready: 'Ready',
  claimed: '已认领',
  in_progress: '进行中',
  review: '评审中',
  done: '已完成',
  blocked: '阻塞',
};

function parseSimpleYamlMap(raw, sectionKey) {
  const map = {};
  const re = new RegExp(`^${sectionKey}:\\s*\\r?\\n((?:[ \\t].+\\r?\\n)+)`, 'm');
  const m = raw.match(re);
  if (!m) return map;
  for (const line of m[1].split(/\r?\n/)) {
    const km = line.match(/^\s+([A-Za-z0-9_-]+):\s*"?(.*?)"?\s*$/);
    if (km) map[km[1]] = km[2];
  }
  return map;
}

function parseYamlList(raw, sectionKey) {
  const items = [];
  const re = new RegExp(`^${sectionKey}:\\s*\\r?\\n((?:\\s+- .+\\r?\\n)+)`, 'm');
  const m = raw.match(re);
  if (!m) return items;
  for (const line of m[1].split(/\r?\n/)) {
    const lm = line.match(/^\s+-\s+(.+)$/);
    if (lm) items.push(lm[1].trim().replace(/^["']|["']$/g, ''));
  }
  return items;
}

function parseSectionBlock(raw, sectionKey) {
  const re = new RegExp(`^${sectionKey}:\\s*\\r?\\n((?:  .+\\r?\\n)+)`, 'm');
  return raw.match(re)?.[1] || '';
}

export function loadDotEnv(orchRoot = ORCH_ROOT) {
  const envFile = path.join(orchRoot, '.env');
  if (!fs.existsSync(envFile)) return;
  const text = fs.readFileSync(envFile, 'utf8');
  for (const line of text.split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const m = t.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!m) continue;
    let v = m[2].trim();
    if (
      (v.startsWith('"') && v.endsWith('"')) ||
      (v.startsWith("'") && v.endsWith("'"))
    ) {
      v = v.slice(1, -1);
    }
    if (process.env[m[1]] === undefined) process.env[m[1]] = v;
  }
}

export function loadBitableConfig(configPath = CONFIG_PATH) {
  const raw = fs.readFileSync(configPath, 'utf8');
  const get = (key) => {
    const m = raw.match(new RegExp(`^\\s+${key}:\\s*"([^"]*)"`, 'm'));
    return m ? m[1] : '';
  };
  const getBool = (block, key, fallback = false) => {
    const m = block.match(new RegExp(`^\\s+${key}:\\s*(true|false)`, 'm'));
    return m ? m[1] === 'true' : fallback;
  };

  const inboundBlock = parseSectionBlock(raw, 'inbound');
  const webhookBlock = parseSectionBlock(raw, 'webhook');

  const statusMap = { ...DEFAULT_STATUS_MAP, ...parseSimpleYamlMap(raw, 'status_map') };
  const statusReverse = {};
  for (const [k, v] of Object.entries(statusMap)) statusReverse[v] = k;

  const dispatchGateMap = {
    none: '—',
    pending: '待确认',
    confirmed: '已确认',
    rejected: '已驳回',
    gap_proposed: '待审建单',
    gap_accepted: '建单已采纳',
    gap_rejected: '建单已驳回',
    ...parseSimpleYamlMap(raw, 'dispatch_gate_map'),
  };

  const allowedInbound =
    parseYamlList(inboundBlock, 'allowed_fields').length > 0
      ? parseYamlList(inboundBlock, 'allowed_fields')
      : ['status', 'claimed_by', 'sprint_id', 'title', 'priority'];

  const webhookAllowedTokens = parseYamlList(webhookBlock, 'allowed_app_tokens');
  const webhookAllowedTables = parseYamlList(webhookBlock, 'allowed_table_ids');

  return {
    raw,
    appToken: get('app_token'),
    tableId: get('table_id'),
    fieldTaskId: get('task_id') || 'Task ID',
    fieldTitle: get('title') || '标题',
    fieldStatus: get('status') || '状态',
    fieldSprint: get('sprint_id') || 'Sprint',
    fieldClaimed: get('claimed_by') || '认领',
    fieldPriority: get('priority') || '优先级',
    fieldDispatchGate: get('dispatch_gate') || '派单门控',
    fieldDispatchConfirmBy: get('dispatch_confirm_by') || '确认人',
    fieldDispatchTrigger: get('dispatch_trigger') || '解锁说明',
    dispatchGateMap,
    statusMap,
    statusReverse,
    inbound: {
      enabled: getBool(inboundBlock, 'enabled', true),
      allowedFields: allowedInbound,
      newTasks: (inboundBlock.match(/^\s+new_tasks:\s*(\w+)/m) || [])[1] || 'queue',
      proposalsFile:
        (inboundBlock.match(/^\s+proposals_file:\s*(.+)/m) || [])[1]?.trim() ||
        'agent-delivery/bitable-inbound-proposals.yaml',
      normalizeHumanPrefix: getBool(inboundBlock, 'normalize_human_prefix', true),
      validateTransitions:
        (inboundBlock.match(/^\s+validate_transitions:\s*(\w+)/m) || [])[1] || 'warn',
      taskIdPattern:
        (inboundBlock.match(/^\s+task_id_pattern:\s*"(.+)"\s*$/m) || [])[1] ||
        '^[A-Z][A-Za-z0-9-]+$',
    },
    humanPrefix:
      (raw.match(/^\s+registry_human_prefix:\s*"(.*)"/m) || [])[1] || 'human:',
    atPrefix: (raw.match(/^\s+bitable_at_prefix:\s*"(.*)"/m) || [])[1] || '@',
    webhook: {
      enabled: getBool(webhookBlock, 'enabled', false),
      path:
        (webhookBlock.match(/^\s+path:\s*(.+)/m) || [])[1]?.trim() ||
        '/internal/feishu-bitable/webhook',
      host: (webhookBlock.match(/^\s+host:\s*"(.*)"/m) || [])[1] || '0.0.0.0',
      port: Number((webhookBlock.match(/^\s+port:\s*(\d+)/m) || [])[1] || '8787'),
      verificationToken:
        (webhookBlock.match(/^\s+verification_token:\s*"(.*)"/m) || [])[1] || '',
      signingSecret:
        process.env.FEISHU_BITABLE_WEBHOOK_SECRET ||
        (webhookBlock.match(/^\s+signing_secret:\s*"(.*)"/m) || [])[1] ||
        '',
      skipVerification: getBool(webhookBlock, 'skip_verification', false),
      fetchRecordOnRecordId: getBool(webhookBlock, 'fetch_record_on_record_id', true),
      validateTransitions:
        (webhookBlock.match(/^\s+validate_transitions:\s*(\w+)/m) || [])[1] || 'warn',
      autoGitPush: getBool(webhookBlock, 'auto_git_push', true),
      auditLog:
        (webhookBlock.match(/^\s+audit_log:\s*(.+)/m) || [])[1]?.trim() ||
        'agent-delivery/_tmp/feishu-webhook-audit.jsonl',
      allowedAppTokens: webhookAllowedTokens.length
        ? webhookAllowedTokens
        : [get('app_token')].filter(Boolean),
      allowedTableIds: webhookAllowedTables.length
        ? webhookAllowedTables
        : [get('table_id')].filter(Boolean),
    },
  };
}
