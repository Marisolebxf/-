/**
 * Feishu IM phase-1 guards: roster ∩ user-map only, task-id required, 30min dedupe.
 */
import fs from 'node:fs';
import path from 'node:path';
import { findTaskBlock, getScalar, ORCH_ROOT, readRegistryText } from './task-registry-lib.mjs';

export const RATE_WINDOW_MS = 30 * 60 * 1000;
export const TASK_ID_RE = /^[A-Z][A-Za-z0-9][A-Za-z0-9_-]*$/;
export const USER_MAP_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'feishu', 'feishu-user-map.yaml');
export const ROSTER_PATH = path.join(ORCH_ROOT, 'agent-delivery', 'team-roster.yaml');
export const RATE_PATH = path.join(ORCH_ROOT, 'agent-delivery', '_tmp', 'feishu-im-rate.json');

export function loadDotEnv(orchRoot = ORCH_ROOT) {
  const envFile = path.join(orchRoot, '.env');
  if (!fs.existsSync(envFile)) return;
  for (const line of fs.readFileSync(envFile, 'utf8').split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const m = t.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!m) continue;
    let v = m[2].trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
      v = v.slice(1, -1);
    }
    if (process.env[m[1]] === undefined) process.env[m[1]] = v;
  }
}

export function normalizeRegistryName(raw) {
  const value = String(raw || '').trim();
  if (!value) return '';
  if (/^ou[_-]/i.test(value) || /open_id/i.test(value)) return '';
  if (value.startsWith('human:')) return value;
  if (value.startsWith('agent:')) return value;
  return `human:${value}`;
}

export function parseNamedHumans(yamlText) {
  const people = [];
  const blocks = String(yamlText || '').split(/(?=\n\s*- (?:name|registry_name):)/);
  for (const b of blocks) {
    const name = (b.match(/^\s+name:\s*"?([^"\r\n]+)"?/m) || [])[1]?.trim();
    const reg = (b.match(/registry_name:\s*"?([^"\r\n]+)"?/) || [])[1]?.trim();
    const oid = (b.match(/feishu_open_id:\s*"?([^"\r\n]+)"?/) || [])[1]?.trim();
    const registryName = reg || (name ? `human:${name}` : '');
    if (!registryName.startsWith('human:')) continue;
    people.push({
      name: name || registryName.slice(6),
      registry_name: registryName,
      feishu_open_id: oid || '',
    });
  }
  return people;
}

export function loadAllowlist(paths = {}) {
  const rosterText = fs.readFileSync(paths.rosterPath || ROSTER_PATH, 'utf8');
  const mapText = fs.readFileSync(paths.userMapPath || USER_MAP_PATH, 'utf8');
  const roster = new Set(
    parseNamedHumans(rosterText).map((p) => p.registry_name),
  );
  const mapped = parseNamedHumans(mapText).filter((p) => p.feishu_open_id);
  const allow = [];
  for (const p of mapped) {
    if (roster.has(p.registry_name)) allow.push(p);
  }
  return allow;
}

export function resolveAllowedHuman(raw, paths = {}) {
  if (/^ou[_-]/i.test(String(raw || '').trim()) || /open_id/i.test(String(raw || ''))) {
    return { ok: false, error: '禁止传入 open_id；只允许花名册真名或 human:姓名' };
  }
  const registryName = normalizeRegistryName(raw);
  if (!registryName.startsWith('human:')) {
    return { ok: false, error: `无法解析收件人: ${raw || '(empty)'}` };
  }
  const want = registryName.slice('human:'.length);
  const hit = loadAllowlist(paths).find(
    (p) => p.registry_name === registryName || p.name === want,
  );
  if (!hit) {
    return {
      ok: false,
      error: `${registryName} 不在花名册∩飞书映射中（离队映射或未 harvest open_id 不可发）`,
    };
  }
  return { ok: true, ...hit };
}

export function listAllowedHumans(paths = {}) {
  return loadAllowlist(paths).map(({ name, registry_name }) => ({ name, registry_name }));
}

export function assertTaskId(taskId) {
  const id = String(taskId || '').trim();
  if (!TASK_ID_RE.test(id)) {
    return { ok: false, error: 'task_id 必填，且须为登记表 ID（如 ENT-FE-I2-12-ANALYSIS-GATE-L01）' };
  }
  return { ok: true, id };
}

export function readTaskNotifyTargets(taskId) {
  const idCheck = assertTaskId(taskId);
  if (!idCheck.ok) return idCheck;
  const lines = readRegistryText().split(/\r?\n/);
  const loc = findTaskBlock(lines, idCheck.id);
  if (!loc) return { ok: false, error: `任务不存在: ${idCheck.id}` };
  const block = lines.slice(loc.start, loc.end);
  return {
    ok: true,
    id: idCheck.id,
    title: getScalar(block, 'title'),
    status: getScalar(block, 'status'),
    supervised_by: getScalar(block, 'supervised_by'),
    claimed_by: getScalar(block, 'claimed_by'),
  };
}

export function formatNotifyText(taskId, text) {
  const body = String(text || '').trim();
  if (!body) return { ok: false, error: 'text 不能为空' };
  const prefix = `【${taskId}】`;
  const full = body.startsWith(prefix) || body.includes(taskId) ? body : `${prefix}\n${body}`;
  if (full.length > 4000) return { ok: false, error: 'text 超过 4000 字' };
  return { ok: true, text: full };
}

function readRateStore(ratePath) {
  if (!fs.existsSync(ratePath)) return {};
  try {
    return JSON.parse(fs.readFileSync(ratePath, 'utf8'));
  } catch {
    return {};
  }
}

export function rateKey(registryName, taskId) {
  return `${registryName}|${taskId}`;
}

export function checkRateLimit(registryName, taskId, now = Date.now(), opts = {}) {
  const ratePath = opts.ratePath || RATE_PATH;
  const windowMs = opts.windowMs ?? RATE_WINDOW_MS;
  const store = readRateStore(ratePath);
  const key = rateKey(registryName, taskId);
  const last = Number(store[key] || 0);
  if (last && now - last < windowMs) {
    const waitMin = Math.ceil((windowMs - (now - last)) / 60000);
    return {
      ok: false,
      error: `同人同任务 ${Math.round(windowMs / 60000)} 分钟内已发过，约 ${waitMin} 分钟后可再发`,
      last_sent_at: last,
    };
  }
  return { ok: true, key, store, ratePath };
}

export function recordSend(registryName, taskId, now = Date.now(), opts = {}) {
  const ratePath = opts.ratePath || RATE_PATH;
  const store = opts.store || readRateStore(ratePath);
  store[rateKey(registryName, taskId)] = now;
  fs.mkdirSync(path.dirname(ratePath), { recursive: true });
  fs.writeFileSync(ratePath, `${JSON.stringify(store, null, 2)}\n`, 'utf8');
}

export function pickNotifyRecipients(task, audience = 'supervisor') {
  const targets = [];
  const add = (raw, role) => {
    if (!raw || raw.startsWith('agent:')) return;
    const resolved = resolveAllowedHuman(raw);
    if (resolved.ok) targets.push({ ...resolved, role });
  };
  if (audience === 'supervisor' || audience === 'both') add(task.supervised_by, 'supervisor');
  if (audience === 'claimed' || audience === 'both') add(task.claimed_by, 'claimed');
  const unique = [];
  const seen = new Set();
  for (const t of targets) {
    if (seen.has(t.registry_name)) continue;
    seen.add(t.registry_name);
    unique.push(t);
  }
  return unique;
}
