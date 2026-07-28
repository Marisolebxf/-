#!/usr/bin/env node
/**
 * Mayor loop → 派单门控「待确认」+ 飞书 IM 通知确认人（默认 human:淮政玮）。
 * 淮政玮在看板把「派单门控」改为「已确认」→ 既有自动化 B → action=dispatch_confirm → confirmPending。
 */

import fs from 'node:fs';
import path from 'node:path';
import { ORCH_ROOT } from './feishu-bitable-config.mjs';
import { projectPendingTargetsToFeishu } from './dispatch-feishu-projection.mjs';
import { sendTextToOpenId } from './feishu-im.mjs';
import { loadPending, loadRules } from '../coordinator-dispatch.mjs';

const PENDING_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'pending-dispatch.yaml');
const USER_MAP = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-user-map.yaml');
const BITABLE_CFG = path.join(ORCH_ROOT, 'agent-delivery', 'feishu-bitable.yaml');

export const MAYOR_LOOP_TRIGGER = 'mayor-loop-dispatch';
export const DEFAULT_MAYOR_CONFIRM_BY = 'human:淮政玮';

function readMayorConfirmBy() {
  if (!fs.existsSync(BITABLE_CFG)) return DEFAULT_MAYOR_CONFIRM_BY;
  const raw = fs.readFileSync(BITABLE_CFG, 'utf8');
  const m = raw.match(/^\s*mayor_loop_confirm_by:\s*"?(human:[^"\r\n]+)"?/m);
  return m ? m[1].trim() : DEFAULT_MAYOR_CONFIRM_BY;
}

function resolveOpenId(registryName) {
  if (!fs.existsSync(USER_MAP)) return '';
  const raw = fs.readFileSync(USER_MAP, 'utf8');
  const want = registryName.replace(/^human:/, '');
  const blocks = raw.split(/(?=\n\s*- name:)/);
  for (const b of blocks) {
    const name = (b.match(/^\s+name:\s*"?([^"\r\n]+)"?/m) || [])[1]?.trim();
    const reg = (b.match(/registry_name:\s*"?([^"\r\n]+)"?/) || [])[1]?.trim();
    const oid = (b.match(/feishu_open_id:\s*"?([^"\r\n]+)"?/) || [])[1]?.trim();
    if (
      oid &&
      (reg === registryName ||
        reg === `human:${want}` ||
        name === want)
    ) {
      return oid;
    }
  }
  return '';
}

function savePendingState(state) {
  const lines = [
    '# coordinator 待确认派单队列（scan / Mayor loop 写入；confirm 后清空条目）',
    'version: 1',
    `updated: "${new Date().toISOString().slice(0, 10)}"`,
    '',
  ];
  if (!state.pending.length) {
    lines.push('pending: []');
  } else {
    lines.push('pending:');
    for (const p of state.pending) {
      lines.push(`  - id: ${p.id}`);
      lines.push(`    created_at: "${p.created_at || new Date().toISOString()}"`);
      lines.push(`    trigger: ${p.trigger}`);
      lines.push(`    cause_task: ${p.cause_task}`);
      lines.push('    targets:');
      for (const t of p.targets) lines.push(`      - ${t}`);
    }
  }
  lines.push('', 'confirmed:');
  if (!state.confirmed?.length) {
    lines.push('  []');
  } else {
    for (const c of (state.confirmed || []).slice(-30)) {
      lines.push(`  - id: ${c.id}`);
      if (c.created_at) lines.push(`    created_at: "${c.created_at}"`);
      lines.push(`    confirmed_at: "${c.confirmed_at}"`);
      lines.push(`    approved_by: ${c.approved_by}`);
      lines.push(`    trigger: ${c.trigger}`);
      lines.push(`    cause_task: ${c.cause_task}`);
      lines.push('    applied_tasks:');
      for (const t of c.applied_tasks || c.targets || []) {
        lines.push(`      - ${t}`);
      }
    }
  }
  lines.push('');
  fs.writeFileSync(PENDING_PATH, lines.join('\n'), 'utf8');
}

/**
 * @param {Array<{id:string,title?:string,agent?:string}>} tasks
 * @param {{ dryRun?: boolean, notify?: boolean, confirmBy?: string }} opts
 */
export async function proposeMayorLoopDispatch(tasks, opts = {}) {
  const dryRun = !!opts.dryRun;
  const notify = opts.notify !== false;
  const confirmBy = opts.confirmBy || readMayorConfirmBy();
  const rules = loadRules();
  const state = loadPending();

  const already = new Set();
  for (const e of state.pending) {
    for (const t of e.targets || []) already.add(t);
  }

  const input = (tasks || []).filter((t) => t?.id);
  const fresh = input.filter((t) => !already.has(t.id));
  const skipped = input.filter((t) => already.has(t.id)).map((t) => t.id);

  if (!fresh.length) {
    return {
      ok: true,
      enqueued: [],
      skipped_already_pending: skipped,
      confirm_by: confirmBy,
      notify: null,
    };
  }

  const stamp = new Date().toISOString().replace(/[:.]/g, '').slice(0, 15);
  const entry = {
    id: `mayor-loop-${stamp}`,
    created_at: new Date().toISOString(),
    trigger: MAYOR_LOOP_TRIGGER,
    cause_task: 'MAYOR-LOOP',
    targets: fresh.map((t) => t.id),
  };

  if (!dryRun) {
    state.pending.push(entry);
    savePendingState(state);
  }

  const byId = new Map(
    fresh.map((t) => [t.id, { id: t.id, title: t.title, agent: t.agent, supervised_by: confirmBy }]),
  );
  const feishu = projectPendingTargetsToFeishu([entry], rules, byId, dryRun);

  let notifyResult = null;
  if (notify) {
    const openId = resolveOpenId(confirmBy);
    const lines = [
      '【Mayor 派单待确认】',
      `确认人：${confirmBy}`,
      `共 ${fresh.length} 条 → 请在飞书看板将「派单门控」改为「已确认」以完成 confirm：`,
      ...fresh.map((t, i) => `${i + 1}. ${t.id}  ${t.title || ''}  (${t.agent || '-'})`),
      '',
      '说明：改门控后自动化 POST action=dispatch_confirm；通过后任务可派（派单包 + gate=已确认）。',
    ];
    if (!openId) {
      notifyResult = { ok: false, error: `no feishu_open_id for ${confirmBy}` };
    } else {
      try {
        notifyResult = await sendTextToOpenId(openId, lines.join('\n'), { dryRun });
      } catch (e) {
        notifyResult = { ok: false, error: e.message };
      }
    }
  }

  return {
    ok: true,
    dryRun,
    entry_id: entry.id,
    enqueued: fresh.map((t) => t.id),
    skipped_already_pending: skipped,
    confirm_by: confirmBy,
    feishu_projection: feishu,
    notify: notifyResult,
  };
}
