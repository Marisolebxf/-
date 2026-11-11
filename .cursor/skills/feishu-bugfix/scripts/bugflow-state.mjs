#!/usr/bin/env node
/**
 * Dependency-free run ledger and validator for the Feishu bug-fix P0 workflow.
 * Validates state schema, exact gates, real git/evidence facts and versioned policy.
 *
 * Design source: references/P0-DESIGN.md (relative to this Skill package)
 * No external dependencies. Node.js >= 18.
 */
import { createHash, randomUUID } from 'node:crypto';
import { closeSync, existsSync, mkdirSync, openSync, readFileSync, renameSync, statSync, unlinkSync, writeFileSync } from 'node:fs';
import { hostname } from 'node:os';
import { execFileSync } from 'node:child_process';
import { dirname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
import { validateJsonSchema } from './lib/mini-json-schema.mjs';
import { loadPolicy, matchTableToPolicy, validatePolicy } from './lib/policy-file.mjs';

export const VALIDATOR_VERSION = 'bugflow-state-p0-v9';
export const SCHEMA_VERSION = 2;
export const PROJECTION_VERSION = 'p0-v3';
export const PHASES = [
  'INTAKE',
  'CLAIMED',
  'DIAGNOSED',
  'READY_DEV',
  'IMPLEMENTING',
  'REVIEWING',
  'VERIFYING',
  'READY_SHIP',
  'SHIPPING',
  'DEV_VERIFYING',
  'AWAITING_ACCEPTANCE',
  'RESOLVED',
  'BLOCKED',
  'REOPENED',
  'DEV_VERIFY_FAILED',
  'ROLLED_BACK',
  'CANCELLED',
];

const ALLOWED_TRANSITIONS = {
  INTAKE: ['CLAIMED', 'BLOCKED', 'CANCELLED'],
  CLAIMED: ['DIAGNOSED', 'BLOCKED', 'CANCELLED'],
  DIAGNOSED: ['READY_DEV', 'BLOCKED', 'CANCELLED'],
  READY_DEV: ['IMPLEMENTING', 'BLOCKED', 'CANCELLED'],
  IMPLEMENTING: ['REVIEWING', 'BLOCKED', 'CANCELLED'],
  REVIEWING: ['VERIFYING', 'BLOCKED', 'CANCELLED'],
  VERIFYING: ['READY_SHIP', 'BLOCKED', 'CANCELLED'],
  READY_SHIP: ['SHIPPING', 'READY_DEV', 'BLOCKED', 'CANCELLED'],
  SHIPPING: ['DEV_VERIFYING', 'DEV_VERIFY_FAILED', 'BLOCKED', 'CANCELLED'],
  DEV_VERIFYING: ['AWAITING_ACCEPTANCE', 'DEV_VERIFY_FAILED', 'BLOCKED', 'CANCELLED'],
  AWAITING_ACCEPTANCE: ['RESOLVED', 'REOPENED', 'BLOCKED', 'CANCELLED'],
  RESOLVED: ['REOPENED'],
  REOPENED: ['DIAGNOSED', 'BLOCKED', 'CANCELLED'],
  DEV_VERIFY_FAILED: ['ROLLED_BACK', 'REOPENED', 'BLOCKED', 'CANCELLED'],
  ROLLED_BACK: ['REOPENED', 'BLOCKED', 'CANCELLED'],
  BLOCKED: [],
  CANCELLED: ['REOPENED'],
};

const RUN_LOCK_STALE_MS = 10 * 60_000;

const TOKENS = {
  enter_dev: '进入开发',
  ship: '提测',
  acceptance: '验收通过',
};

const BASE_VERIFICATION_CATEGORIES = ['fix', 'regression'];
const ALL_VERIFICATION_CATEGORIES = [
  ...BASE_VERIFICATION_CATEGORIES,
  'boundary',
  'integration',
  'data',
  'algorithm',
  'security',
  'performance',
  'rollback',
];
const DATA_WRITE_OPERATIONS = ['insert', 'update', 'delete', 'replace', 'upsert', 'truncate', 'create', 'alter', 'drop', 'load', 'mock'];

const SCRIPT_PATH = fileURLToPath(import.meta.url);
export const SKILL_ROOT = resolve(dirname(SCRIPT_PATH), '..');
function resolveRepoRoot() {
  try {
    return execFileSync('git', ['-C', SKILL_ROOT, 'rev-parse', '--show-toplevel'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch {
    return resolve(SKILL_ROOT, '../../..');
  }
}
export const REPO_ROOT = resolveRepoRoot();
export const RUNS_ROOT = join(REPO_ROOT, 'agent-delivery', 'bugfix-runs');
export const STATE_SCHEMA_PATH = join(SKILL_ROOT, 'templates', 'state.schema.json');
export const POLICY_ROOT = join(SKILL_ROOT, 'policies');
export const REPO_REGISTRY_PATH = join(REPO_ROOT, 'agent-delivery', 'repo-registry.yaml');

let stateSchemaCache = null;
let repoRegistryCache = null;

function isoNow() {
  const d = new Date();
  const offset = -d.getTimezoneOffset();
  const sign = offset >= 0 ? '+' : '-';
  const pad = (n) => String(Math.floor(Math.abs(n))).padStart(2, '0');
  const local = new Date(d.getTime() - d.getTimezoneOffset() * 60_000)
    .toISOString()
    .replace('Z', '');
  return `${local}${sign}${pad(offset / 60)}:${pad(offset % 60)}`;
}

function compactTimestamp(iso) {
  return iso.replace(/[-:]/g, '').replace(/\.\d{3}/, '');
}

function processIsAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error?.code !== 'ESRCH';
  }
}

function runLockIsStale(lockPath) {
  let lock = null;
  try {
    lock = readJson(lockPath);
  } catch {
    // Malformed or partially written lock: use the file age below.
  }
  if (lock?.host === hostname() && Number.isInteger(lock.pid)) return !processIsAlive(lock.pid);
  try {
    return Date.now() - statSync(lockPath).mtimeMs > RUN_LOCK_STALE_MS;
  } catch {
    return true;
  }
}

function reclaimRunLockIfUnchanged(lockPath) {
  let observedText = null;
  try {
    observedText = readFileSync(lockPath, 'utf8');
  } catch {
    return false;
  }
  if (!runLockIsStale(lockPath)) return false;
  let currentText = null;
  try {
    currentText = readFileSync(lockPath, 'utf8');
  } catch {
    return false;
  }
  if (currentText !== observedText) return false;
  try {
    unlinkSync(lockPath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Serialize every command that touches a run directory.
 *
 * state.json and evidence/manifest.json both use read-modify-write semantics, so a per-run
 * lock must cover the whole command rather than only record-evidence. The lock is removed on
 * normal process exit and can be reclaimed after a crash when its PID is gone or it is stale.
 */
export function acquireRunLock(runDir, command, options = {}) {
  if (!existsSync(runDir)) {
    if (options.create !== true) throw new Error(`RUN_NOT_FOUND: ${runDir}`);
    mkdirSync(runDir, { recursive: true });
  }
  const lockPath = join(runDir, '.bugflow.lock');
  const token = randomUUID();
  const payload = {
    token,
    pid: process.pid,
    host: hostname(),
    command,
    created_at: isoNow(),
  };
  for (let attempt = 0; attempt < 2; attempt += 1) {
    let fd = null;
    try {
      fd = openSync(lockPath, 'wx', 0o600);
      writeFileSync(fd, `${JSON.stringify(payload)}\n`, 'utf8');
      closeSync(fd);
      return () => {
        try {
          const current = readJson(lockPath);
          if (current?.token === token) unlinkSync(lockPath);
        } catch {
          // A missing/replaced lock is not ours to delete.
        }
      };
    } catch (error) {
      if (fd != null) {
        try { closeSync(fd); } catch { /* ignore */ }
      }
      if (error?.code !== 'EEXIST') throw error;
      if (attempt === 0 && reclaimRunLockIfUnchanged(lockPath)) {
        continue;
      }
      let owner = '';
      try {
        const current = readJson(lockPath);
        owner = current ? ` pid=${current.pid ?? '?'} command=${current.command ?? '?'} host=${current.host ?? '?'}` : '';
      } catch { /* ignore */ }
      throw new Error(`RUN_LOCKED: ${runDir}${owner}`);
    }
  }
  throw new Error(`RUN_LOCKED: ${runDir}`);
}

function numericIdentifier(value, label) {
  const normalized = String(value ?? '').trim();
  if (!/^\d+$/.test(normalized)) throw new Error(`${label} must contain digits only`);
  return normalized;
}

function stableProjection(value) {
  if (Array.isArray(value)) return value.map(stableProjection);
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .filter((key) => value[key] !== undefined)
        .map((key) => [key, stableProjection(value[key])]),
    );
  }
  return value;
}

export function sha256(value) {
  const payload = typeof value === 'string' ? value : JSON.stringify(stableProjection(value));
  return `sha256:${createHash('sha256').update(payload, 'utf8').digest('hex')}`;
}

function sha256Bytes(value) {
  return `sha256:${createHash('sha256').update(value).digest('hex')}`;
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function atomicWrite(path, content) {
  mkdirSync(dirname(path), { recursive: true });
  const tmp = `${path}.tmp-${process.pid}-${Date.now()}`;
  writeFileSync(tmp, content, 'utf8');
  renameSync(tmp, path);
}

function writeJson(path, value) {
  atomicWrite(path, `${JSON.stringify(value, null, 2)}\n`);
}

function loadStateSchema() {
  if (!stateSchemaCache) stateSchemaCache = readJson(STATE_SCHEMA_PATH);
  return stateSchemaCache;
}

function hashFile(path) {
  return sha256Bytes(readFileSync(path));
}

function isWithin(parent, child) {
  const rel = relative(resolve(parent), resolve(child));
  return rel === '' || (!rel.startsWith(`..${sep}`) && rel !== '..' && !isAbsolute(rel));
}

function resolveInside(parent, child) {
  const path = resolve(parent, child);
  if (!isWithin(parent, path)) throw new Error(`PATH_ESCAPE: ${child} resolves outside ${parent}`);
  return path;
}

function loadRepoRegistry() {
  if (repoRegistryCache) return repoRegistryCache;
  if (!existsSync(REPO_REGISTRY_PATH)) throw new Error(`REPO_REGISTRY_NOT_FOUND: ${REPO_REGISTRY_PATH}`);
  const lines = readFileSync(REPO_REGISTRY_PATH, 'utf8').split(/\r?\n/);
  const entries = [];
  let current = null;
  let inRepos = false;
  for (const line of lines) {
    if (/^repos:\s*$/.test(line)) {
      inRepos = true;
      continue;
    }
    if (inRepos && /^[A-Za-z_][A-Za-z0-9_]*:\s*$/.test(line)) {
      if (current) entries.push(current);
      current = null;
      inRepos = false;
      continue;
    }
    if (!inRepos) continue;
    const idMatch = line.match(/^  - id:\s*([^\s#]+)/);
    if (idMatch) {
      if (current) entries.push(current);
      current = { id: idMatch[1], names: [], remotes: [] };
      continue;
    }
    if (!current) continue;
    const nameMatch = line.match(/^\s+name:\s*([^\s#]+)/);
    if (nameMatch) current.names.push(nameMatch[1]);
    const remoteMatch = line.match(/^\s+remote:\s*(\S+)/);
    if (remoteMatch) current.remotes.push(remoteMatch[1]);
  }
  if (current) entries.push(current);
  repoRegistryCache = entries;
  return entries;
}

function assertRepoRegistryBinding(repo) {
  const registered = loadRepoRegistry().find((entry) => entry.id === repo.repo_id);
  if (!registered) throw new Error(`REPOS_INVALID: repo_id ${repo.repo_id} is not registered in agent-delivery/repo-registry.yaml`);
  if (!registered.names.includes(repo.repo_name)) {
    throw new Error(`REPOS_INVALID: ${repo.repo_id}.repo_name=${repo.repo_name} does not match repo-registry.yaml`);
  }
  if (!registered.remotes.includes(repo.remote)) {
    throw new Error(`REPOS_INVALID: ${repo.repo_id}.remote does not match repo-registry.yaml`);
  }
}

function git(repoDir, args) {
  try {
    return execFileSync('git', ['-C', repoDir, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  } catch (error) {
    const detail = String(error.stderr ?? error.stdout ?? error.message).trim();
    throw new Error(`GIT_COMMAND_FAILED: git ${args.join(' ')}${detail ? `\n${detail}` : ''}`);
  }
}

function normalizeSpace(value) {
  return String(value ?? '').trim();
}

function requireString(value, name, errors) {
  if (typeof value !== 'string' || value.trim() === '') errors.push(`${name} must be a non-empty string`);
}

function requireArray(value, name, errors) {
  if (!Array.isArray(value)) errors.push(`${name} must be an array`);
}

function projectRepoBinding(gateName, repo) {
  const common = { repo_id: repo.repo_id };
  const bundleFields = {
    ...(repo.role != null ? { role: repo.role } : {}),
    ...(repo.ship_order != null ? { ship_order: repo.ship_order } : {}),
    ...(Array.isArray(repo.depends_on) ? { depends_on: repo.depends_on } : {}),
  };
  if (gateName === 'enter_dev') {
    return {
      ...common,
      repo_name: repo.repo_name,
      base_sha: repo.base_sha,
      planned_change_scope: repo.planned_change_scope,
      ...bundleFields,
    };
  }
  return {
    ...common,
    candidate_sha: repo.candidate_sha,
    diff_hash: repo.diff_hash,
    verification_hash: repo.verification_hash,
    review_hash: repo.review_hash,
    data_policy_hash: repo.data_policy_hash,
    data_scope_hash: repo.data_scope_hash,
    ...bundleFields,
  };
}

function projectGateBinding(gateName, binding) {
  if (!binding || typeof binding !== 'object') return null;
  const repos = Array.isArray(binding.repos)
    ? [...binding.repos]
      .sort((a, b) => String(a.repo_id).localeCompare(String(b.repo_id)))
      .map((repo) => projectRepoBinding(gateName, repo))
    : binding.repos;
  if (gateName === 'enter_dev') {
    return {
      repos,
      diagnosis_hash: binding.diagnosis_hash,
      plan_hash: binding.plan_hash,
      risk_level: binding.risk_level,
      data_policy_version: binding.data_policy_version,
      data_policy_hash: binding.data_policy_hash,
      data_scope_hash: binding.data_scope_hash,
    };
  }
  if (gateName === 'acceptance') {
    return {
      work_item_id: binding.work_item_id,
      claim_id: binding.claim_id,
      ship_gate_hash: binding.ship_gate_hash,
      dev_verification_result: binding.dev_verification_result,
      evidence_manifest_hash: binding.evidence_manifest_hash,
      current_status: binding.current_status,
    };
  }
  return {
    repos,
    risk_level: binding.risk_level,
    deploy_target: binding.deploy_target,
  };
}

function gateProjection(state, gateName, gate) {
  return {
    projection_version: gate.projection_version ?? PROJECTION_VERSION,
    validator_version: gate.validator_version ?? gate.validation?.validator_version ?? VALIDATOR_VERSION,
    source: gate.source,
    token_text: gate.token_text,
    approved_by: gate.approved_by,
    approved_session_id: gate.approved_session_id ?? null,
    approved_machine_id: gate.approved_machine_id ?? null,
    claim_id: gate.claim_id,
    gate: gateName,
    bound_to: projectGateBinding(gateName, gate.bound_to),
  };
}

export function computeGateHash(state, gateName, gate) {
  return sha256(gateProjection(state, gateName, gate));
}

export function validateStateShape(state) {
  if (!state || typeof state !== 'object' || Array.isArray(state)) return ['state must be an object'];
  const errors = validateJsonSchema(state, loadStateSchema());
  if (state.phase && state.phase !== 'INTAKE') {
    for (const key of ['claim_comment_ref', 'claim_operator', 'claimed_at']) {
      if (typeof state.ownership?.[key] !== 'string' || state.ownership[key].trim() === '') {
        errors.push(`ownership.${key} is required after claim`);
      }
    }
  }
  if (state.phase === 'BLOCKED') {
    requireString(state.blocked_from, 'blocked_from', errors);
    requireString(state.resume_phase, 'resume_phase', errors);
    requireString(state.resume_condition, 'resume_condition', errors);
  }
  if (Array.isArray(state.cycles) && state.current_cycle_id) {
    if (!state.cycles.some((c) => c.cycle_id === state.current_cycle_id)) {
      errors.push('current_cycle_id must exist in cycles[]');
    }
    if (state.cycles.length !== state.cycle_seq) errors.push('cycles.length must equal cycle_seq');
  }
  for (const [collection, values] of [
    ['repos', state.repos],
    ['implementation.repos', state.implementation?.repos],
    ['review.repos', state.review?.repos],
    ['ship_package.repos', state.ship_package?.repos],
  ]) {
    if (!Array.isArray(values)) continue;
    const ids = values.map((value) => value?.repo_id).filter(Boolean);
    if (new Set(ids).size !== ids.length) errors.push(`${collection} contains duplicate repo_id values`);
  }
  try {
    assertBundleTopology(state.repos ?? []);
  } catch (error) {
    errors.push(error.message);
  }
  for (const [index, review] of (state.review?.repos ?? []).entries()) {
    if (review?.review_hash && review.review_hash !== reviewHash(review)) {
      errors.push(`review.repos[${index}].review_hash mismatch`);
    }
  }
  for (const [index, decision] of (state.decisions ?? []).entries()) {
    if (decision?.requires_human_ratification === true && decision.ratified_by != null
      && (typeof decision.ratified_by !== 'string' || !decision.ratified_by.startsWith('human:'))) {
      errors.push(`decisions[${index}].ratified_by must start with human: when ratification is required`);
    }
  }
  for (const gateName of ['enter_dev', 'ship', 'acceptance']) {
    const gate = state.gates?.[gateName];
    if (gate?.status === 'approved') {
      if (!gate.bound_to) errors.push(`gates.${gateName}.bound_to is required when approved`);
      const actual = computeGateHash(state, gateName, gate);
      if (actual !== gate.gate_hash) errors.push(`gates.${gateName}.gate_hash mismatch`);
    }
  }
  if (state.acceptance?.status === 'approved') {
    requireString(state.acceptance.evidence_ref, 'acceptance.evidence_ref', errors);
    if (state.acceptance.current_status !== 'RESOLVED') errors.push('acceptance.current_status must be RESOLVED');
  }
  return errors;
}

function assertStateShape(state) {
  const errors = validateStateShape(state);
  if (errors.length) throw new Error(`STATE_INVALID:\n- ${errors.join('\n- ')}`);
}

export function diagnosisHash(state) {
  return sha256({ diagnosis: state.diagnosis ?? null, plan: state.plan ?? null });
}

function implementationRepo(state, repoId) {
  return (state.implementation?.repos ?? []).find((repo) => repo.repo_id === repoId) ?? null;
}

function verificationProjection(state, repoId) {
  return (state.verification_matrix ?? [])
    .filter((item) => (item.repo_ids ?? []).includes(repoId))
    .map((item) => ({
      id: item.id,
      category: item.category,
      behavior: item.behavior,
      result: item.result,
      evidence_refs: item.evidence_refs,
      simulated: item.simulated ?? false,
      skipped_reason: item.skipped_reason ?? null,
    }));
}

export function verificationHash(state, repoId) {
  return sha256(verificationProjection(state, repoId));
}

export function reviewHash(review) {
  return sha256({
    repo_id: review.repo_id,
    reviewer: review.reviewer,
    independent: review.independent,
    reviewed_sha: review.reviewed_sha,
    verdict: review.verdict,
    scope: review.scope,
    findings: review.findings ?? [],
    round: review.round ?? 1,
  });
}

function exactRepoSet(left, right) {
  return sameStringSet((left ?? []).map((repo) => repo.repo_id ?? repo), (right ?? []).map((repo) => repo.repo_id ?? repo));
}

function assertGateBinding(gateName, binding) {
  const errors = [];
  if (!binding || typeof binding !== 'object') throw new Error('GATE_BINDING_INVALID: binding must be an object');
  if (gateName === 'acceptance') {
    for (const key of ['work_item_id', 'claim_id', 'ship_gate_hash', 'dev_verification_result', 'evidence_manifest_hash', 'current_status']) {
      requireString(binding[key], `bound_to.${key}`, errors);
    }
    if (binding.dev_verification_result !== 'PASS') errors.push('bound_to.dev_verification_result must be PASS');
    if (errors.length) throw new Error(`GATE_BINDING_INVALID:\n- ${errors.join('\n- ')}`);
    return;
  }
  requireArray(binding.repos, 'bound_to.repos', errors);
  if (Array.isArray(binding.repos) && binding.repos.length === 0) errors.push('bound_to.repos must not be empty');
  const repoIds = (binding.repos ?? []).map((repo) => repo?.repo_id).filter(Boolean);
  if (new Set(repoIds).size !== repoIds.length) errors.push('bound_to.repos contains duplicate repo_id values');
  for (const [i, repo] of (binding.repos ?? []).entries()) {
    requireString(repo.repo_id, `bound_to.repos[${i}].repo_id`, errors);
    if (gateName === 'enter_dev') {
      requireString(repo.repo_name, `bound_to.repos[${i}].repo_name`, errors);
      requireString(repo.base_sha, `bound_to.repos[${i}].base_sha`, errors);
      requireArray(repo.planned_change_scope, `bound_to.repos[${i}].planned_change_scope`, errors);
      if (repo.candidate_sha != null) errors.push(`bound_to.repos[${i}].candidate_sha must be null for enter_dev`);
    } else {
      requireString(repo.candidate_sha, `bound_to.repos[${i}].candidate_sha`, errors);
      for (const key of ['diff_hash', 'verification_hash', 'review_hash', 'data_policy_hash', 'data_scope_hash']) {
        requireString(repo[key], `bound_to.repos[${i}].${key}`, errors);
      }
    }
  }
  if ((binding.repos ?? []).length > 1) {
    for (const [i, repo] of (binding.repos ?? []).entries()) {
      requireString(repo.role, `bound_to.repos[${i}].role`, errors);
      requireArray(repo.depends_on, `bound_to.repos[${i}].depends_on`, errors);
      if (!Number.isInteger(repo.ship_order) || repo.ship_order < 1) {
        errors.push(`bound_to.repos[${i}].ship_order must be a positive integer`);
      }
    }
  }
  if (gateName === 'enter_dev') {
    for (const key of ['diagnosis_hash', 'plan_hash', 'risk_level', 'data_policy_version', 'data_policy_hash', 'data_scope_hash']) {
      requireString(binding[key], `bound_to.${key}`, errors);
    }
  } else {
    requireString(binding.risk_level, 'bound_to.risk_level', errors);
    if (binding.deploy_target !== 'dev') errors.push('bound_to.deploy_target must be dev');
  }
  if (errors.length) throw new Error(`GATE_BINDING_INVALID:\n- ${errors.join('\n- ')}`);
}

function tokenAllowsMessage(gateName, message, autoNumber, activeRuns) {
  const token = TOKENS[gateName];
  if (!token) return false;
  const exact = message === token;
  const withNumber = message === `${token}${autoNumber}` || message === `${token} ${autoNumber}`;
  if (activeRuns > 1) return withNumber;
  return exact || withNumber;
}

function sameStringSet(left, right) {
  const a = [...new Set((left ?? []).map(String))].sort();
  const b = [...new Set((right ?? []).map(String))].sort();
  return a.length === b.length && a.every((value, index) => value === b[index]);
}

function bindingStateErrors(state, gateName, binding, options = {}) {
  const errors = [];
  if (!binding || typeof binding !== 'object') return ['bound_to must be an object'];
  if (gateName === 'acceptance') {
    if (binding.work_item_id !== state.work_item.work_item_id) errors.push('work_item_id mismatch');
    if (binding.claim_id !== state.ownership.claim_id) errors.push('claim_id mismatch');
    if (binding.ship_gate_hash !== state.gates?.ship?.gate_hash) errors.push('ship_gate_hash mismatch');
    if (binding.dev_verification_result !== state.ship_package?.dev_verification?.result) {
      errors.push('dev_verification_result mismatch');
    }
    if (binding.evidence_manifest_hash !== state.evidence?.verification?.manifest_hash) {
      errors.push('evidence_manifest_hash mismatch');
    }
    if (!normalizeSpace(binding.current_status)) errors.push('current_status is required');
    return errors;
  }
  if (!exactRepoSet(state.repos, binding.repos)) {
    errors.push('bound_to.repos must exactly equal state.repos');
  }
  if (binding.risk_level !== state.risk.level) errors.push(`risk_level mismatch: expected ${state.risk.level}`);
  if (gateName === 'enter_dev') {
    if (binding.diagnosis_hash !== diagnosisHash(state)) errors.push('diagnosis_hash mismatch');
    if (binding.plan_hash !== sha256(state.plan ?? null)) errors.push('plan_hash mismatch');
    if (binding.data_policy_version !== state.data_policy.policy_version) {
      errors.push('data_policy_version mismatch');
    }
    if (binding.data_policy_hash !== state.data_policy.policy_hash) errors.push('data_policy_hash mismatch');
    if (binding.data_scope_hash !== state.data_policy.scope_hash) errors.push('data_scope_hash mismatch');
  }
  for (const [i, boundRepo] of (binding.repos ?? []).entries()) {
    const repo = (state.repos ?? []).find((candidate) => candidate.repo_id === boundRepo.repo_id);
    if (!repo) {
      errors.push(`bound_to.repos[${i}] is not present in state.repos`);
      continue;
    }
    const bundleMismatch = (
      (boundRepo.role != null && repo.role !== boundRepo.role)
      || (boundRepo.ship_order != null && repo.ship_order !== boundRepo.ship_order)
      || (Array.isArray(boundRepo.depends_on) && !sameStringSet(repo.depends_on ?? [], boundRepo.depends_on))
    );
    if (bundleMismatch) errors.push(`${boundRepo.repo_id}: bundle role/depends_on/ship_order mismatch`);
    if (gateName === 'enter_dev') {
      if (!options.allowEnterDevCandidate && repo.candidate_sha != null) {
        errors.push(`${boundRepo.repo_id}: candidate_sha must be null before enter_dev`);
      }
      if (repo.base_sha !== boundRepo.base_sha) errors.push(`${boundRepo.repo_id}: base_sha mismatch`);
      if (!sameStringSet(repo.planned_change_scope, boundRepo.planned_change_scope)) {
        errors.push(`${boundRepo.repo_id}: planned_change_scope mismatch`);
      }
    } else {
      if (repo.candidate_sha !== boundRepo.candidate_sha) errors.push(`${boundRepo.repo_id}: candidate_sha mismatch`);
      const implementation = implementationRepo(state, boundRepo.repo_id);
      if (!implementation) errors.push(`${boundRepo.repo_id}: implementation record is missing`);
      else {
        if (implementation.candidate_sha !== boundRepo.candidate_sha) errors.push(`${boundRepo.repo_id}: implementation candidate_sha mismatch`);
        if (implementation.diff_hash !== boundRepo.diff_hash) errors.push(`${boundRepo.repo_id}: diff_hash mismatch`);
        if (verificationHash(state, boundRepo.repo_id) !== boundRepo.verification_hash) {
          errors.push(`${boundRepo.repo_id}: verification_hash mismatch`);
        }
      }
      if (boundRepo.data_policy_hash !== state.data_policy.policy_hash) {
        errors.push(`${boundRepo.repo_id}: data_policy_hash mismatch`);
      }
      if (boundRepo.data_scope_hash !== state.data_policy.scope_hash) {
        errors.push(`${boundRepo.repo_id}: data_scope_hash mismatch`);
      }
      const review = (state.review?.repos ?? []).find((candidate) => candidate.repo_id === boundRepo.repo_id);
      if (!review) errors.push(`${boundRepo.repo_id}: review record is missing`);
      else {
        if (review.reviewed_sha !== boundRepo.candidate_sha) errors.push(`${boundRepo.repo_id}: review reviewed_sha mismatch`);
        if (review.review_hash !== boundRepo.review_hash) errors.push(`${boundRepo.repo_id}: review_hash mismatch`);
        if (review.verdict !== 'PASS') errors.push(`${boundRepo.repo_id}: review verdict is not PASS`);
        if (state.risk.level !== 'S' && review.independent !== true) {
          errors.push(`${boundRepo.repo_id}: M/L review must be independent`);
        }
      }
    }
  }
  return errors;
}

function assertBindingMatchesState(state, gateName, binding, options = {}) {
  const errors = bindingStateErrors(state, gateName, binding, options);
  if (errors.length) throw new Error(`GATE_BINDING_STATE_MISMATCH:\n- ${errors.join('\n- ')}`);
}

export function approveGate(state, input) {
  const gateName = input.gate;
  if (!TOKENS[gateName]) throw new Error('GATE_INVALID: gate must be enter_dev, ship or acceptance');
  assertStateShape(state);
  if (typeof input.sessionId !== 'string' || input.sessionId.trim() === '') {
    throw new Error('GATE_CONTEXT_REQUIRED: --session-id is required');
  }
  if (typeof input.machineId !== 'string' || input.machineId.trim() === '') {
    throw new Error('GATE_CONTEXT_REQUIRED: --machine-id is required');
  }
  const approvalPhases = {
    enter_dev: { first: 'READY_DEV', reconfirm: 'IMPLEMENTING' },
    ship: { first: 'READY_SHIP', reconfirm: 'SHIPPING' },
    acceptance: { first: 'AWAITING_ACCEPTANCE', reconfirm: null },
  };
  const phases = approvalPhases[gateName];
  const blockedGateApproval = state.phase === 'BLOCKED' && (
    (gateName === 'enter_dev' && ['READY_DEV', 'IMPLEMENTING'].includes(state.resume_phase))
    || (gateName === 'ship' && ['READY_SHIP', 'SHIPPING'].includes(state.resume_phase))
  );
  const firstApproval = state.phase === phases.first
    || (blockedGateApproval && state.gates[gateName]?.status !== 'approved');
  const needsReconfirm = ['needs_reconfirm', 'invalidated'].includes(state.gates[gateName]?.status);
  const reConfirmation = (phases.reconfirm != null && state.phase === phases.reconfirm && needsReconfirm)
    || (blockedGateApproval && needsReconfirm);
  if (!firstApproval && !reConfirmation) {
    throw new Error(`GATE_PHASE_INVALID: ${gateName} requires ${phases.first}${phases.reconfirm ? `, or ${phases.reconfirm} after invalidation` : ''}`);
  }
  if (input.claimId && input.claimId !== state.ownership.claim_id) {
    throw new Error('GATE_CLAIM_MISMATCH: current claim does not match state.ownership.claim_id');
  }
  if (!tokenAllowsMessage(gateName, input.message, state.work_item.auto_number, input.activeRuns ?? 1)) {
    const multiple = (input.activeRuns ?? 1) > 1 ? `；当前有多个 active run，必须使用 ${TOKENS[gateName]}${state.work_item.auto_number}` : '';
    throw new Error(`GATE_TOKEN_INVALID: expected exact ${TOKENS[gateName]}${multiple}`);
  }
  loadAndValidatePolicy(state, input.policiesRoot ?? POLICY_ROOT, input.now ?? new Date());
  if (gateName === 'ship') {
    const ratificationErrors = [];
    unratifiedDecisionErrors(state, ratificationErrors);
    if (ratificationErrors.length) {
      throw new Error(`DECISION_RATIFICATION_REQUIRED:\n- ${ratificationErrors.join('\n- ')}`);
    }
  }
  if (gateName === 'enter_dev' && firstApproval) {
    assertPhaseRequirements(state, 'DIAGNOSED');
    assertPhaseRequirements(state, 'READY_DEV');
  }
  if (gateName === 'acceptance') {
    assertPhaseRequirements(state, 'AWAITING_ACCEPTANCE');
  }
  else {
    assertPhaseRequirements(state, gateName === 'enter_dev' ? 'IMPLEMENTING' : 'READY_SHIP');
  }
  assertGateBinding(gateName, input.binding);
  assertBindingMatchesState(state, gateName, input.binding, {
    allowEnterDevCandidate: gateName === 'enter_dev' && (
      state.phase === 'IMPLEMENTING'
      || (state.phase === 'BLOCKED' && state.resume_phase === 'IMPLEMENTING')
    ),
  });
  const at = isoNow();
  const gate = {
    status: 'approved',
    source: 'chat',
    token_text: input.message,
    approved_by: input.approvedBy ?? 'current_user',
    approved_at: at,
    approved_session_id: input.sessionId ?? state.ownership.session_id ?? null,
    approved_machine_id: input.machineId ?? state.ownership.machine_id ?? null,
    claim_id: state.ownership.claim_id,
    message_ref: input.messageRef ?? null,
    projection_version: PROJECTION_VERSION,
    validator_version: VALIDATOR_VERSION,
    bound_to: input.binding,
    gate_hash: null,
    validation: {
      result: 'PASS',
      checked_at: at,
      validator_version: VALIDATOR_VERSION,
      actual: { claim_id: state.ownership.claim_id },
      expected: { claim_id: state.ownership.claim_id },
    },
  };
  gate.gate_hash = computeGateHash(state, gateName, gate);
  state.gates[gateName] = gate;
  state.updated_at = at;
  return gate;
}

export function validateGate(state, gateName, context = {}) {
  if (!TOKENS[gateName]) return { ok: false, code: 'GATE_INVALID', errors: ['gate must be enter_dev, ship or acceptance'] };
  const gate = state.gates?.[gateName];
  if (!gate || gate.status !== 'approved') {
    return { ok: false, code: 'GATE_NOT_APPROVED', errors: [`gates.${gateName} is not approved`] };
  }
  const errors = [];
  if (gate.claim_id !== state.ownership.claim_id) errors.push('claim_id mismatch');
  if (!context.sessionId) errors.push('session context is required');
  else if (gate.approved_session_id && gate.approved_session_id !== context.sessionId) {
    errors.push('session changed; exact token must be supplied again');
  }
  if (!context.machineId) errors.push('machine context is required');
  else if (gate.approved_machine_id && gate.approved_machine_id !== context.machineId) {
    errors.push('machine changed; exact token must be supplied again');
  }
  const actualHash = computeGateHash(state, gateName, gate);
  if (actualHash !== gate.gate_hash) errors.push('gate_hash mismatch');
  try {
    loadAndValidatePolicy(state, context.policiesRoot ?? POLICY_ROOT, context.now ?? new Date());
    assertGateBinding(gateName, gate.bound_to);
    assertBindingMatchesState(state, gateName, gate.bound_to, {
      allowEnterDevCandidate: context.allowEnterDevCandidate === true,
    });
  } catch (error) {
    errors.push(error.message);
  }
  const ok = errors.length === 0;
  return { ok, code: ok ? 'PASS' : 'GATE_INVALID', errors, actualHash, expectedHash: gate.gate_hash };
}

function mutateGateValidation(state, gateName, result) {
  const gate = state.gates[gateName];
  if (!gate) return;
  gate.validation = {
    result: result.ok ? 'PASS' : 'FAIL',
    checked_at: isoNow(),
    validator_version: VALIDATOR_VERSION,
    actual: result.actualHash ?? null,
    expected: result.expectedHash ?? null,
    errors: result.errors,
  };
  if (!result.ok) {
    gate.status = 'needs_reconfirm';
  }
}

function assertTransitionAllowed(from, to, state) {
  if (from === 'BLOCKED' && state.resume_phase === to) return;
  if (!(ALLOWED_TRANSITIONS[from] ?? []).includes(to)) {
    throw new Error(`TRANSITION_NOT_ALLOWED: ${from} -> ${to}`);
  }
}

function transitionRequirement(state, to) {
  if (to === 'IMPLEMENTING') return 'enter_dev';
  if (to === 'SHIPPING') return 'ship';
  if (to === 'RESOLVED' && state.acceptance?.mode === 'chat_exact') return 'acceptance';
  return null;
}

function nonEmptyArray(value) {
  return Array.isArray(value) && value.length > 0;
}

function isCrossRepoBundle(state) {
  return (state.repos ?? []).length > 1;
}

function bundleRepoIds(state) {
  return (state.repos ?? []).map((repo) => repo.repo_id).filter(Boolean);
}

function assertBundleTopology(repos) {
  const multiRepo = repos.length > 1;
  const ids = new Set(repos.map((repo) => repo.repo_id));
  const orders = [];
  for (const [index, repo] of repos.entries()) {
    if (multiRepo && (typeof repo.role !== 'string' || repo.role.trim() === '')) {
      throw new Error(`REPOS_INVALID: cross-repo bundle requires repos[${index}].role`);
    }
    if (repo.ship_order != null && (!Number.isInteger(repo.ship_order) || repo.ship_order < 1)) {
      throw new Error(`REPOS_INVALID: repos[${index}].ship_order must be a positive integer`);
    }
    if (multiRepo && repo.ship_order == null) {
      throw new Error(`REPOS_INVALID: cross-repo bundle requires repos[${index}].ship_order`);
    }
    if (multiRepo && !Array.isArray(repo.depends_on)) {
      throw new Error(`REPOS_INVALID: cross-repo bundle requires repos[${index}].depends_on array`);
    }
    if (repo.ship_order != null) orders.push(repo.ship_order);
  }
  if (!multiRepo) return;
  const expected = Array.from({ length: repos.length }, (_, index) => index + 1);
  const actual = [...orders].sort((a, b) => a - b);
  if (actual.length !== expected.length || actual.some((value, index) => value !== expected[index])) {
    throw new Error(`REPOS_INVALID: cross-repo bundle ship_order must be contiguous 1..${repos.length}`);
  }
  const orderById = new Map(repos.map((repo) => [repo.repo_id, repo.ship_order]));
  for (const [index, repo] of repos.entries()) {
    const seen = new Set();
    for (const dependency of repo.depends_on ?? []) {
      if (seen.has(dependency)) throw new Error(`REPOS_INVALID: repos[${index}].depends_on contains duplicate ${dependency}`);
      seen.add(dependency);
      if (dependency === repo.repo_id) throw new Error(`REPOS_INVALID: repos[${index}].depends_on cannot reference itself`);
      if (!ids.has(dependency)) throw new Error(`REPOS_INVALID: repos[${index}].depends_on references unknown repo ${dependency}`);
      if (orderById.get(dependency) >= repo.ship_order) {
        throw new Error(`REPOS_INVALID: repos[${index}].depends_on ${dependency} must ship before ${repo.repo_id}`);
      }
    }
  }
}

function crossRepoIntegrationErrors(state, errors) {
  if (!isCrossRepoBundle(state)) return;
  const expectedIds = bundleRepoIds(state);
  const integrated = (state.verification_matrix ?? []).some((item) => (
    item.category === 'integration'
    && sameStringSet(item.repo_ids ?? [], expectedIds)
    && ['PASS', 'SIMULATED'].includes(item.result)
  ));
  if (!integrated) {
    errors.push('CROSS_REPO_BUNDLE_INTEGRATION_REQUIRED: at least one PASS/SIMULATED integration verification must cover every repo in the bundle');
  }
}

function requireFields(fields) {
  const errors = fields.filter(([value]) => typeof value !== 'string' || value.trim() === '').map(([, name]) => `${name} is required`);
  if (errors.length) throw new Error(`PHASE_REQUIREMENTS:\n- ${errors.join('\n- ')}`);
}

function claimEvidenceErrors(state, errors) {
  for (const key of ['claim_comment_ref', 'claim_operator', 'claimed_at']) {
    if (typeof state.ownership?.[key] !== 'string' || state.ownership[key].trim() === '') {
      errors.push(`ownership.${key} is required before CLAIMED`);
    }
  }
}

function automationBoundaryErrors(state, errors) {
  if (state.risk?.level === 'L') {
    errors.push('L_ROUTE_REQUIRED: L defects must use the existing task-registry and long-task workflow');
  }
  if (isCrossRepoBundle(state) && state.risk?.level === 'S') {
    errors.push('CROSS_REPO_BUNDLE_REQUIRES_M: one bug may span multiple repositories, but its bundle risk must be at least M');
  }
}

function unratifiedDecisionErrors(state, errors) {
  for (const decision of state.decisions ?? []) {
    if (decision.requires_human_ratification === true && !normalizeSpace(decision.ratified_by)) {
      errors.push(`decision requires human ratification before ship: ${decision.decision}`);
    }
  }
}

function assertPhaseRequirements(state, to) {
  const errors = [];
  if (to === 'CLAIMED') claimEvidenceErrors(state, errors);
  if (to === 'DIAGNOSED') {
    requireFields([
      [state.diagnosis?.symptom, 'diagnosis.symptom'],
      [state.diagnosis?.root_cause, 'diagnosis.root_cause'],
    ]);
    if (!nonEmptyArray(state.diagnosis?.impact_scope)) errors.push('diagnosis.impact_scope must not be empty');
  }
  if (to === 'READY_DEV') {
    if (!nonEmptyArray(state.plan?.change_scope)) errors.push('plan.change_scope must not be empty');
    if (!nonEmptyArray(state.plan?.verification_plan)) errors.push('plan.verification_plan must not be empty');
    if (!nonEmptyArray(state.plan?.rollback_plan)) errors.push('plan.rollback_plan must not be empty');
    if (!nonEmptyArray(state.diagnosis?.requirement_refs)) errors.push('diagnosis.requirement_refs must not be empty');
  }
  if (to === 'IMPLEMENTING') {
    if (!nonEmptyArray(state.repos)) errors.push('repos must not be empty');
    automationBoundaryErrors(state, errors);
    if (state.plan?.data_access && state.data_policy?.scope?.status !== 'approved') {
      errors.push('approved data scope is required when plan.data_access=true');
    }
  }
  if (to === 'REVIEWING') {
    if (!nonEmptyArray(state.implementation?.repos)) errors.push('implementation.repos must not be empty');
    if (!exactRepoSet(state.repos, state.implementation?.repos)) errors.push('implementation.repos must exactly equal state.repos');
    for (const implementation of state.implementation?.repos ?? []) {
      if (implementation.git_verified !== true) errors.push(`${implementation.repo_id}: git verification is required before REVIEWING`);
      if (!implementation.changed_files?.length) errors.push(`${implementation.repo_id}: changed_files must not be empty`);
    }
  }
  if (to === 'VERIFYING') {
    if (!exactRepoSet(state.repos, state.review?.repos)) errors.push('review.repos must exactly equal state.repos');
    for (const review of state.review?.repos ?? []) {
      if (review.verdict !== 'PASS') errors.push(`${review.repo_id}: review verdict must be PASS`);
      if (state.risk?.level !== 'S' && review.independent !== true) errors.push(`${review.repo_id}: M/L review must be independent`);
    }
  }
  if (to === 'READY_SHIP') {
    automationBoundaryErrors(state, errors);
    unratifiedDecisionErrors(state, errors);
    if (!nonEmptyArray(state.verification_matrix)) errors.push('verification_matrix must not be empty');
    for (const item of state.verification_matrix ?? []) {
      if (!['PASS', 'SKIPPED', 'SIMULATED'].includes(item.result)) errors.push(`verification ${item.id ?? '<unknown>'}: result must be PASS/SKIPPED/SIMULATED`);
      if (!nonEmptyArray(item.evidence_refs)) errors.push(`verification ${item.id ?? '<unknown>'}: evidence_refs must not be empty`);
      if (item.result === 'SKIPPED' && !normalizeSpace(item.skipped_reason)) errors.push(`verification ${item.id ?? '<unknown>'}: skipped_reason is required`);
    }
    crossRepoIntegrationErrors(state, errors);
    for (const repo of state.repos ?? []) {
      if (!(state.verification_matrix ?? []).some((item) => (item.repo_ids ?? []).includes(repo.repo_id))) {
        errors.push(`${repo.repo_id}: verification result is required`);
      }
      for (const category of BASE_VERIFICATION_CATEGORIES) {
        if (!(state.verification_matrix ?? []).some((item) => (item.repo_ids ?? []).includes(repo.repo_id) && item.category === category)) {
          errors.push(`${repo.repo_id}: ${category} verification is required`);
        }
      }
      if (state.risk?.level !== 'S' && !(state.verification_matrix ?? []).some(
        (item) => (item.repo_ids ?? []).includes(repo.repo_id)
          && !BASE_VERIFICATION_CATEGORIES.includes(item.category),
      )) {
        errors.push(`${repo.repo_id}: M/L requires at least one non-happy-path verification category`);
      }
    }
    const verifiedIds = new Set(state.evidence?.verification?.evidence_ids ?? []);
    const verifiedEvidence = state.evidence?.verification?.evidence_results ?? {};
    for (const item of state.verification_matrix ?? []) {
      const refs = (item.evidence_refs ?? []).map((ref) => String(ref).split('#').at(-1));
      for (const ref of refs) {
        if (!verifiedIds.has(ref)) {
          errors.push(`verification ${item.id ?? '<unknown>'}: evidence ${ref} is missing from verified manifest`);
          continue;
        }
        const evidence = verifiedEvidence[ref] ?? {};
        if (item.result === 'PASS') {
          if (evidence.result !== 'PASS') errors.push(`verification ${item.id ?? '<unknown>'}: PASS cannot use ${evidence.result ?? 'unknown'} evidence ${ref}`);
          if (evidence.reviewable !== true || evidence.raw_retained !== true) {
            errors.push(`verification ${item.id ?? '<unknown>'}: PASS evidence ${ref} must be reviewable with raw_retained=true`);
          }
        }
        if (item.result === 'SIMULATED' && evidence.result !== 'SIMULATED') {
          errors.push(`verification ${item.id ?? '<unknown>'}: SIMULATED result requires SIMULATED evidence ${ref}`);
        }
        if (item.result === 'SKIPPED' && !['SKIPPED', 'SIMULATED'].includes(evidence.result)) {
          errors.push(`verification ${item.id ?? '<unknown>'}: SKIPPED result requires SKIPPED/SIMULATED evidence ${ref}`);
        }
      }
    }
    if (state.evidence?.verification?.result !== 'PASS') errors.push('evidence manifest verification must pass before READY_SHIP');
  }
  if (to === 'DEV_VERIFYING') {
    if (!exactRepoSet(state.repos, state.ship_package?.repos)) errors.push('ship_package.repos must exactly equal state.repos');
    for (const repo of state.ship_package?.repos ?? []) {
      if (!normalizeSpace(repo.pipeline_id)) errors.push(`${repo.repo_id}: pipeline_id is required`);
      if (!['success', 'passed'].includes(String(repo.pipeline_status ?? '').toLowerCase())) errors.push(`${repo.repo_id}: pipeline must pass`);
      if (!normalizeSpace(repo.merge_commit_sha)) errors.push(`${repo.repo_id}: merge_commit_sha is required`);
      if (!normalizeSpace(repo.pipeline_url)) errors.push(`${repo.repo_id}: pipeline_url is required`);
      if (!['success', 'complete', 'completed'].includes(String(repo.rollout_status ?? '').toLowerCase())) errors.push(`${repo.repo_id}: rollout must complete`);
    }
  }
  if (to === 'AWAITING_ACCEPTANCE') {
    if (!nonEmptyArray(state.ship_package?.acceptance_steps)) errors.push('ship_package.acceptance_steps must not be empty');
    if (state.ship_package?.dev_verification?.result !== 'PASS') errors.push('ship_package.dev_verification.result must be PASS');
    const verifiedIds = new Set(state.evidence?.verification?.evidence_ids ?? []);
    const verifiedEvidence = state.evidence?.verification?.evidence_results ?? {};
    const devRefs = (state.ship_package?.dev_verification?.evidence_refs ?? []).map((ref) => String(ref).split('#').at(-1));
    if (!devRefs.length) errors.push('dev verification evidence_refs must not be empty');
    for (const ref of devRefs) {
      if (!verifiedIds.has(ref)) errors.push(`dev verification evidence ${ref} is missing from verified manifest`);
      const evidence = verifiedEvidence[ref] ?? {};
      if (evidence.result !== 'PASS' || evidence.reviewable !== true || evidence.raw_retained !== true) {
        errors.push(`dev verification PASS evidence ${ref} must be PASS, reviewable and raw_retained=true`);
      }
    }
  }
  if (['DEV_VERIFY_FAILED', 'ROLLED_BACK'].includes(to)) {
    if (!state.failure_stage) errors.push('failure_stage is required');
    if (!state.failure_class) errors.push('failure_class is required');
  }
  if (errors.length) throw new Error(`PHASE_REQUIREMENTS:\n- ${errors.join('\n- ')}`);
}

function nextActionFor(phase, owner = 'agent') {
  const actions = {
    CLAIMED: '完成复现、根因、反证、需规依据和影响范围，然后进入诊断完成。',
    DIAGNOSED: '提交改动范围、非目标、验证计划和回滚计划，创建 READY_DEV。',
    READY_DEV: '展示进入开发绑定对象并取得精确口令。',
    IMPLEMENTING: '完成改动并运行 verify-repo，然后提交评审。',
    REVIEWING: '完成全部仓库独立评审，PASS 后进入验证。',
    VERIFYING: '执行验证矩阵并运行 verify-evidence，形成提测包。',
    READY_SHIP: '展示提测绑定对象并取得精确口令。',
    SHIPPING: '完成合并、dev 部署和流水线记录。',
    DEV_VERIFYING: '完成 dev 复测、验收步骤和提测总结。',
    AWAITING_ACCEPTANCE: '等待当前会话完整精确消息“验收通过”，或读取人工直接完成的飞书状态迁移。',
    RESOLVED: '无需动作，缺陷已验收。',
    BLOCKED: '满足恢复条件后由负责人恢复。',
    REOPENED: '重新诊断并建立新的 cycle 绑定。',
    DEV_VERIFY_FAILED: '记录失败分类，修复后返工或按流程回滚。',
    ROLLED_BACK: '确认回滚结果并决定返工或关闭。',
    CANCELLED: '确认分支、MR 和 dev 部署清理。',
  };
  return { owner, action: actions[phase] ?? `处理 ${phase} 阶段待办` };
}

function assertAcceptanceCanResolve(state) {
  const a = state.acceptance ?? {};
  const errors = [];
  if (!['policy_only', 'chat_exact'].includes(a.mode)) errors.push('acceptance.mode must be policy_only or chat_exact');
  if (a.status !== 'approved') errors.push('acceptance.status must be approved');
  if (a.current_status !== 'RESOLVED') errors.push('acceptance.current_status must be RESOLVED');
  if (a.operator_verified !== false) errors.push('acceptance.operator_verified must be false');
  requireString(a.evidence_ref, 'acceptance.evidence_ref', errors);
  if (a.mode === 'chat_exact') {
    const gate = state.gates?.acceptance;
    if (!gate || gate.status !== 'approved') errors.push('gates.acceptance must be approved');
    if (gate?.gate_hash !== a.gate_hash) errors.push('acceptance.gate_hash mismatch');
    if (a.approval_message !== TOKENS.acceptance) errors.push('acceptance.approval_message must be 验收通过');
    requireString(a.approval_ref, 'acceptance.approval_ref', errors);
  }
  if (errors.length) throw new Error(`ACCEPTANCE_NOT_VERIFIED:\n- ${errors.join('\n- ')}`);
}

export function advance(state, input) {
  assertStateShape(state);
  const from = state.phase;
  const to = input.to;
  if (from === 'BLOCKED' && input.allowBlockedResume !== true) {
    throw new Error('RESUME_COMMAND_REQUIRED: use `resume` to leave BLOCKED');
  }
  if (!PHASES.includes(to)) throw new Error(`PHASE_INVALID: ${to}`);
  if (to === 'CLAIMED') {
    if (!normalizeSpace(input.claimCommentRef) || !normalizeSpace(input.claimOperator)) {
      throw new Error('CLAIM_EVIDENCE_REQUIRED: claimCommentRef and claimOperator are required when entering CLAIMED');
    }
    state.ownership.claim_comment_ref = input.claimCommentRef;
    state.ownership.claim_operator = input.claimOperator;
    state.ownership.claimed_at = state.ownership.claimed_at ?? isoNow();
  }
  if (to === 'BLOCKED') throw new Error('TRANSITION_COMMAND_REQUIRED: use `block` so blocked_from/resume_phase/resume_condition are recorded');
  if (to === 'CANCELLED') throw new Error('TRANSITION_COMMAND_REQUIRED: use `cancel` so cleanup is recorded');
  if (to === 'REOPENED') throw new Error('TRANSITION_COMMAND_REQUIRED: use `reopen` to archive the current cycle and open a new cycle');
  assertTransitionAllowed(from, to, state);
  const requirement = transitionRequirement(state, to);
  let gateName = null;
  if (requirement) {
    gateName = requirement;
    const result = validateGate(state, gateName, {
      ...input,
      allowEnterDevCandidate: input.allowEnterDevCandidate === true,
    });
    mutateGateValidation(state, gateName, result);
    if (!result.ok) throw new Error(`${result.code}: ${result.errors.join('; ')}`);
  }
  if (to === 'RESOLVED') assertAcceptanceCanResolve(state);
  assertPhaseRequirements(state, to);
  const at = isoNow();
  const gate = gateName ? state.gates[gateName] : null;
  state.transitions.push({
    from,
    to,
    at,
    result: 'PASS',
    validator_version: VALIDATOR_VERSION,
    claim_id: state.ownership.claim_id,
    session_id: input.sessionId ?? state.ownership.session_id ?? null,
    gate: gateName,
    gate_hash: gate?.gate_hash ?? null,
    evidence_refs: input.evidenceRefs ?? [],
    summary: input.summary ?? null,
  });
  if (from === 'READY_SHIP' && to === 'READY_DEV' && state.gates.ship.status === 'approved') {
    state.gates.ship.status = 'invalidated';
  }
  state.phase = to;
  state.next_action = nextActionFor(to);
  if (from === 'BLOCKED' && to !== 'BLOCKED') {
    state.blocked_from = null;
    state.resume_phase = null;
    state.resume_condition = null;
  }
  state.updated_at = at;
  return state;
}

export function resumeState(state, input) {
  assertStateShape(state);
  if (state.phase !== 'BLOCKED') throw new Error(`RESUME_INVALID: phase must be BLOCKED, got ${state.phase}`);
  if (!state.resume_phase) throw new Error('RESUME_INVALID: resume_phase is missing');
  if (input.to !== state.resume_phase) {
    throw new Error(`RESUME_PHASE_MISMATCH: expected ${state.resume_phase}, got ${input.to ?? '<missing>'}`);
  }
  if (!normalizeSpace(input.sessionId) || !normalizeSpace(input.machineId)) {
    throw new Error('RESUME_CONTEXT_REQUIRED: sessionId and machineId are required');
  }
  if (state.ownership.session_id && state.ownership.session_id !== input.sessionId) {
    throw new Error('RESUME_SESSION_MISMATCH: use takeover before resuming from another session');
  }
  if (state.ownership.machine_id && state.ownership.machine_id !== input.machineId) {
    throw new Error('RESUME_MACHINE_MISMATCH: use takeover before resuming from another machine');
  }
  if (!Array.isArray(input.evidenceRefs) || input.evidenceRefs.length === 0) {
    throw new Error('RESUME_EVIDENCE_REQUIRED: provide --evidence-ref for the cleared condition');
  }
  const blocker = [...(state.blockers ?? [])].reverse().find((item) => !item.resolved_at) ?? null;
  advance(state, { ...input, allowBlockedResume: true, allowEnterDevCandidate: true });
  if (blocker) {
    blocker.resolved_at = state.transitions.at(-1)?.at ?? isoNow();
    blocker.resolved_by = input.actor ?? input.sessionId;
    blocker.resume_evidence_refs = [...input.evidenceRefs];
  }
  state.updated_at = isoNow();
  return state;
}

export function setRepos(state, repos) {
  if (!Array.isArray(repos) || repos.length === 0) throw new Error('REPOS_INVALID: repos must be a non-empty array');
  const previous = new Map((state.repos ?? []).map((repo) => [repo.repo_id, repo]));
  const seen = new Set();
  const normalized = repos.map((repo, index) => {
    if (!repo || typeof repo !== 'object') throw new Error(`REPOS_INVALID: repos[${index}] must be an object`);
    for (const key of ['repo_id', 'repo_name', 'remote', 'base_branch', 'base_sha']) {
      if (typeof repo[key] !== 'string' || repo[key].trim() === '') {
        throw new Error(`REPOS_INVALID: repos[${index}].${key} is required`);
      }
    }
    if (repo.candidate_sha != null && (typeof repo.candidate_sha !== 'string' || repo.candidate_sha.trim() === '')) {
      throw new Error(`REPOS_INVALID: repos[${index}].candidate_sha must be null or a non-empty string`);
    }
    if (!Array.isArray(repo.planned_change_scope)) {
      throw new Error(`REPOS_INVALID: repos[${index}].planned_change_scope must be an array`);
    }
    if (repo.role != null && (typeof repo.role !== 'string' || repo.role.trim() === '')) {
      throw new Error(`REPOS_INVALID: repos[${index}].role must be a non-empty string when provided`);
    }
    if (repo.depends_on != null && !Array.isArray(repo.depends_on)) {
      throw new Error(`REPOS_INVALID: repos[${index}].depends_on must be an array when provided`);
    }
    if (repo.ship_order != null && (!Number.isInteger(repo.ship_order) || repo.ship_order < 1)) {
      throw new Error(`REPOS_INVALID: repos[${index}].ship_order must be a positive integer when provided`);
    }
    if (seen.has(repo.repo_id)) throw new Error(`REPOS_INVALID: duplicate repo_id ${repo.repo_id}`);
    seen.add(repo.repo_id);
    const normalizedRepo = {
      repo_id: repo.repo_id,
      repo_name: repo.repo_name,
      remote: repo.remote,
      base_branch: repo.base_branch,
      base_sha: repo.base_sha,
      candidate_sha: repo.candidate_sha ?? null,
      planned_change_scope: repo.planned_change_scope.map(String),
      role: repo.role == null ? null : repo.role.trim(),
      depends_on: repo.depends_on == null ? [] : [...new Set(repo.depends_on.map((value) => String(value).trim()).filter(Boolean))],
      ship_order: repo.ship_order ?? null,
    };
    assertRepoRegistryBinding(normalizedRepo);
    return normalizedRepo;
  });
  assertBundleTopology(normalized);
  assertStateShape(state);
  const repoSetChanged = previous.size !== normalized.length || normalized.some((repo) => !previous.has(repo.repo_id));
  const enterBindingChanged = repoSetChanged || normalized.some((repo) => {
    const old = previous.get(repo.repo_id);
    return old && (
      old.base_sha !== repo.base_sha
      || !sameStringSet(old.planned_change_scope, repo.planned_change_scope)
      || old.role !== repo.role
      || old.ship_order !== repo.ship_order
      || !sameStringSet(old.depends_on ?? [], repo.depends_on ?? [])
    );
  });
  state.repos = normalized;
  if (enterBindingChanged && state.gates.enter_dev.status === 'approved') state.gates.enter_dev.status = 'invalidated';
  if (state.gates.ship.status === 'approved') state.gates.ship.status = 'invalidated';
  state.updated_at = isoNow();
  return state.repos;
}

function normalizeRemote(remote) {
  const raw = String(remote ?? '').trim();
  try {
    const parsed = new URL(raw);
    parsed.username = '';
    parsed.password = '';
    return parsed.toString().replace(/\.git$/, '').replace(/\/$/, '');
  } catch {
    return raw.replace(/\/\/[^/@]+@/, '//').replace(/\.git$/, '').replace(/\/$/, '');
  }
}

function changedFileAllowed(file, scopes) {
  return scopes.some((scope) => {
    const normalized = String(scope).replace(/\\/g, '/').replace(/^\.\//, '').replace(/\/$/, '');
    if (normalized.includes('*')) {
      const pattern = normalized
        .split('*')
        .map((part) => part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
        .join('.*');
      return new RegExp(`^${pattern}$`).test(file);
    }
    return file === normalized || file.startsWith(`${normalized}/`);
  });
}

export function verifyRepo(state, input) {
  assertStateShape(state);
  const repo = (state.repos ?? []).find((candidate) => candidate.repo_id === input.repoId);
  if (!repo) throw new Error(`VERIFY_REPO_INVALID: ${input.repoId} is not in state.repos`);
  if (typeof input.repoDir !== 'string' || !isAbsolute(input.repoDir)) {
    throw new Error('VERIFY_REPO_INVALID: --repo-dir must be an absolute path');
  }
  if (!existsSync(input.repoDir)) throw new Error(`VERIFY_REPO_INVALID: repo directory does not exist: ${input.repoDir}`);
  if (!existsSync(join(input.repoDir, '.git'))) throw new Error(`VERIFY_REPO_INVALID: not a git worktree: ${input.repoDir}`);
  const candidateSha = input.candidateSha ?? repo.candidate_sha;
  const baseSha = input.baseSha ?? repo.base_sha;
  requireString(candidateSha, 'candidate_sha', []);
  requireString(baseSha, 'base_sha', []);
  if (!candidateSha || !baseSha) throw new Error('VERIFY_REPO_INVALID: candidate_sha and base_sha are required');
  const head = git(input.repoDir, ['rev-parse', 'HEAD']);
  if (head !== candidateSha) throw new Error(`VERIFY_REPO_INVALID: worktree HEAD ${head} != candidate_sha ${candidateSha}`);
  const remote = git(input.repoDir, ['remote', 'get-url', 'origin']);
  const normalizedRemote = normalizeRemote(remote);
  if (normalizedRemote !== normalizeRemote(repo.remote)) {
    throw new Error(`VERIFY_REPO_INVALID: origin ${remote} does not match state remote ${repo.remote}`);
  }
  try {
    git(input.repoDir, ['merge-base', '--is-ancestor', baseSha, candidateSha]);
  } catch {
    throw new Error(`VERIFY_REPO_INVALID: base_sha ${baseSha} is not an ancestor of candidate_sha ${candidateSha}`);
  }
  const dirty = git(input.repoDir, ['status', '--porcelain']);
  if (dirty) throw new Error(`VERIFY_REPO_INVALID: worktree is dirty; commit or clean it before verification\n${dirty}`);
  const changedFiles = git(input.repoDir, ['diff', '--name-only', `${baseSha}..${candidateSha}`]).split('\n').filter(Boolean);
  if (!changedFiles.length) throw new Error('VERIFY_REPO_INVALID: base..candidate diff is empty');
  const outside = changedFiles.filter((file) => !changedFileAllowed(file, repo.planned_change_scope));
  if (outside.length) throw new Error(`VERIFY_REPO_INVALID: changed files outside planned scope: ${outside.join(', ')}`);
  const diffBytes = execFileSync('git', ['-C', input.repoDir, 'diff', '--binary', '--full-index', `${baseSha}..${candidateSha}`]);
  const diffHash = sha256Bytes(diffBytes);
  const at = isoNow();
  const verification = {
    repo_id: repo.repo_id,
    base_sha: baseSha,
    candidate_sha: candidateSha,
    remote: normalizedRemote,
    changed_files: changedFiles,
    diff_hash: diffHash,
    git_verified: true,
    verification_source: 'git',
    verified_at: at,
  };
  const otherRepos = (state.implementation?.repos ?? []).filter((item) => item.repo_id !== repo.repo_id);
  state.implementation = { ...(state.implementation ?? {}), repos: [...otherRepos, verification] };
  repo.candidate_sha = candidateSha;
  if (state.gates.ship.status === 'approved') state.gates.ship.status = 'invalidated';
  state.next_action = { owner: 'agent', action: '完成其余仓库 verify-repo，然后提交评审。' };
  state.updated_at = at;
  return verification;
}

export function recordDiagnosis(state, diagnosis) {
  assertStateShape(state);
  if (!diagnosis || typeof diagnosis !== 'object') throw new Error('DIAGNOSIS_INVALID: diagnosis must be an object');
  const normalized = {
    symptom: diagnosis.symptom,
    reproduction: Array.isArray(diagnosis.reproduction) ? diagnosis.reproduction : [],
    root_cause: diagnosis.root_cause,
    counter_evidence: Array.isArray(diagnosis.counter_evidence) ? diagnosis.counter_evidence : [],
    requirement_refs: Array.isArray(diagnosis.requirement_refs) ? diagnosis.requirement_refs : [],
    impact_scope: Array.isArray(diagnosis.impact_scope) ? diagnosis.impact_scope : [],
  };
  requireFields([[normalized.symptom, 'diagnosis.symptom'], [normalized.root_cause, 'diagnosis.root_cause']]);
  if (!normalEmpty(normalized.impact_scope)) throw new Error('DIAGNOSIS_INVALID: impact_scope must not be empty');
  if (!normalEmpty(normalized.requirement_refs)) throw new Error('DIAGNOSIS_INVALID: requirement_refs must not be empty');
  state.diagnosis = normalized;
  if (state.gates.enter_dev.status === 'approved') state.gates.enter_dev.status = 'invalidated';
  state.next_action = { owner: 'agent', action: '提交改动范围、非目标、验证计划和回滚计划。' };
  state.updated_at = isoNow();
  return state.diagnosis;
}

function normalEmpty(value) {
  return Array.isArray(value) && value.length > 0;
}

export function recordPlan(state, plan) {
  assertStateShape(state);
  if (!plan || typeof plan !== 'object') throw new Error('PLAN_INVALID: plan must be an object');
  const normalized = {
    change_scope: Array.isArray(plan.change_scope) ? plan.change_scope : [],
    non_goals: Array.isArray(plan.non_goals) ? plan.non_goals : [],
    verification_plan: Array.isArray(plan.verification_plan) ? plan.verification_plan : [],
    rollback_plan: Array.isArray(plan.rollback_plan) ? plan.rollback_plan : [],
    data_access: plan.data_access === true,
  };
  if (!normalEmpty(normalized.change_scope)) throw new Error('PLAN_INVALID: change_scope must not be empty');
  if (!normalEmpty(normalized.verification_plan)) throw new Error('PLAN_INVALID: verification_plan must not be empty');
  if (!normalEmpty(normalized.rollback_plan)) throw new Error('PLAN_INVALID: rollback_plan must not be empty');
  state.plan = normalized;
  if (state.gates.enter_dev.status === 'approved') state.gates.enter_dev.status = 'invalidated';
  state.next_action = { owner: 'agent', action: '确认仓库绑定和数据 scope，展示进入开发绑定对象。' };
  state.updated_at = isoNow();
  return state.plan;
}

export function recordVerification(state, items) {
  assertStateShape(state);
  if (!Array.isArray(items) || items.length === 0) throw new Error('VERIFICATION_INVALID: items must be a non-empty array');
  const seen = new Set();
  const normalized = items.map((item, index) => {
    for (const key of ['id', 'category', 'behavior', 'result']) {
      if (typeof item?.[key] !== 'string' || item[key].trim() === '') throw new Error(`VERIFICATION_INVALID: items[${index}].${key} is required`);
    }
    if (!ALL_VERIFICATION_CATEGORIES.includes(item.category)) {
      throw new Error(`VERIFICATION_INVALID: items[${index}].category is not supported`);
    }
    if (!['PASS', 'FAIL', 'SKIPPED', 'SIMULATED'].includes(item.result)) throw new Error(`VERIFICATION_INVALID: items[${index}].result is invalid`);
    if (seen.has(item.id)) throw new Error(`VERIFICATION_INVALID: duplicate id ${item.id}`);
    seen.add(item.id);
    if (!Array.isArray(item.evidence_refs) || item.evidence_refs.length === 0) throw new Error(`VERIFICATION_INVALID: items[${index}].evidence_refs must not be empty`);
    const repoIds = Array.isArray(item.repo_ids) ? item.repo_ids.map(String) : [];
    if (!repoIds.length) throw new Error(`VERIFICATION_INVALID: items[${index}].repo_ids must not be empty`);
    for (const repoId of repoIds) {
      if (!(state.repos ?? []).some((repo) => repo.repo_id === repoId)) throw new Error(`VERIFICATION_INVALID: ${repoId} is not in state.repos`);
    }
    if (item.result === 'SKIPPED' && !normalizeSpace(item.skipped_reason)) throw new Error(`VERIFICATION_INVALID: items[${index}].skipped_reason is required`);
    return {
      id: item.id,
      category: item.category,
      behavior: item.behavior,
      result: item.result,
      repo_ids: repoIds,
      evidence_refs: item.evidence_refs.map(String),
      simulated: item.result === 'SIMULATED' || item.simulated === true,
      skipped_reason: item.skipped_reason ?? null,
      notes: item.notes ?? null,
    };
  });
  state.verification_matrix = normalized;
  if (state.gates.ship.status === 'approved') state.gates.ship.status = 'invalidated';
  state.next_action = { owner: 'agent', action: '运行 verify-evidence，确认 manifest 和原始证据可复核。' };
  state.updated_at = isoNow();
  return state.verification_matrix;
}

export function recordShipPackage(state, packageInput) {
  assertStateShape(state);
  if (!packageInput || !Array.isArray(packageInput.repos) || packageInput.repos.length === 0) {
    throw new Error('SHIP_PACKAGE_INVALID: repos must be a non-empty array');
  }
  if (!exactRepoSet(state.repos, packageInput.repos)) throw new Error('SHIP_PACKAGE_INVALID: repos must exactly equal state.repos');
  const repos = packageInput.repos.map((repo, index) => {
    for (const key of ['repo_id', 'candidate_sha', 'merge_request_id', 'merge_commit_sha', 'pipeline_id', 'pipeline_status', 'pipeline_url', 'deployed_sha', 'rollout_status']) {
      if (typeof repo?.[key] !== 'string' || repo[key].trim() === '') throw new Error(`SHIP_PACKAGE_INVALID: repos[${index}].${key} is required`);
    }
    const stateRepo = state.repos.find((candidate) => candidate.repo_id === repo.repo_id);
    if (stateRepo.candidate_sha !== repo.candidate_sha) throw new Error(`SHIP_PACKAGE_INVALID: ${repo.repo_id}.candidate_sha mismatch`);
    return {
      repo_id: repo.repo_id,
      candidate_sha: repo.candidate_sha,
      merge_request_id: repo.merge_request_id,
      merge_commit_sha: repo.merge_commit_sha,
      pipeline_id: repo.pipeline_id,
      pipeline_status: repo.pipeline_status,
      pipeline_url: repo.pipeline_url,
      deployed_sha: repo.deployed_sha,
      rollout_status: repo.rollout_status,
      image_tag: repo.image_tag ?? null,
      role: stateRepo.role ?? null,
      depends_on: stateRepo.depends_on ?? [],
      ship_order: stateRepo.ship_order ?? null,
    };
  }).sort((a, b) => (a.ship_order ?? Number.MAX_SAFE_INTEGER) - (b.ship_order ?? Number.MAX_SAFE_INTEGER));
  const devVerification = packageInput.dev_verification ?? { result: 'PENDING', evidence_refs: [] };
  if (devVerification.result === 'PASS' && (!Array.isArray(devVerification.evidence_refs) || devVerification.evidence_refs.length === 0)) {
    throw new Error('SHIP_PACKAGE_INVALID: PASS dev_verification requires evidence_refs');
  }
  state.ship_package = {
    repos,
    acceptance_steps: Array.isArray(packageInput.acceptance_steps) ? packageInput.acceptance_steps.map(String) : [],
    dev_verification: devVerification,
    summary: packageInput.summary ?? null,
  };
  state.next_action = { owner: 'agent', action: '核对 pipeline、deployed_sha、rollout 和 dev 复测证据。' };
  state.updated_at = isoNow();
  return state.ship_package;
}

export function recordRollback(state, rollback) {
  assertStateShape(state);
  if (!rollback || !Array.isArray(rollback.repos)) throw new Error('ROLLBACK_INVALID: repos must be an array');
  state.rollback = {
    repos: rollback.repos.map((repo) => {
      const stateRepo = state.repos.find((candidate) => candidate.repo_id === repo.repo_id);
      return {
        repo_id: repo.repo_id,
        target_sha: repo.target_sha,
        revert_commit: repo.revert_commit ?? null,
        command: repo.command ?? null,
        verification: repo.verification ?? null,
        role: stateRepo?.role ?? null,
        ship_order: stateRepo?.ship_order ?? null,
      };
    }).sort((a, b) => (a.ship_order ?? Number.MAX_SAFE_INTEGER) - (b.ship_order ?? Number.MAX_SAFE_INTEGER)),
    summary: rollback.summary ?? null,
  };
  state.updated_at = isoNow();
  return state.rollback;
}

export function recordDecision(state, decision) {
  assertStateShape(state);
  if (!decision || typeof decision !== 'object') throw new Error('DECISION_INVALID: decision must be an object');
  for (const key of ['decision', 'basis', 'impact']) {
    if (typeof decision[key] !== 'string' || decision[key].trim() === '') throw new Error(`DECISION_INVALID: ${key} is required`);
  }
  const requiresHumanRatification = decision.requires_human_ratification === true;
  if (requiresHumanRatification && decision.ratified_by != null
    && (typeof decision.ratified_by !== 'string' || !decision.ratified_by.startsWith('human:'))) {
    throw new Error('DECISION_INVALID: ratified_by must start with human: when ratification is required');
  }
  state.decisions.push({
    decision: decision.decision,
    basis: decision.basis,
    impact: decision.impact,
    alternatives: Array.isArray(decision.alternatives) ? decision.alternatives : [],
    requires_human_ratification: requiresHumanRatification,
    ratified_by: decision.ratified_by ?? null,
    at: isoNow(),
  });
  state.updated_at = isoNow();
  return state.decisions.at(-1);
}

export function recordFailure(state, failure) {
  assertStateShape(state);
  if (!failure || typeof failure !== 'object') throw new Error('FAILURE_INVALID: failure must be an object');
  if (!['merge', 'push', 'pipeline', 'rollout', 'dev_verify', 'rework'].includes(failure.stage)) throw new Error('FAILURE_INVALID: stage is invalid');
  if (!['product_or_code', 'environment_or_release', 'allowed_empty', 'expectation_or_case', 'schema_or_permission', 'unknown'].includes(failure.class)) {
    throw new Error('FAILURE_INVALID: class is invalid');
  }
  if (failure.class === 'product_or_code') {
    if (state.patch_round >= 3) throw new Error('FAILURE_INVALID: patch_round limit is 3');
    state.patch_round += 1;
  }
  state.failure_stage = failure.stage;
  state.failure_class = failure.class;
  if (state.gates.ship.status === 'approved') state.gates.ship.status = 'invalidated';
  state.next_action = { owner: 'agent', action: '按 failure_class 处理返工、环境修复、期望澄清或回滚。' };
  state.updated_at = isoNow();
  return { failure_stage: state.failure_stage, failure_class: state.failure_class, patch_round: state.patch_round };
}

export function setRisk(state, risk) {
  assertStateShape(state);
  if (!risk || !['S', 'M', 'L'].includes(risk.level)) throw new Error('RISK_INVALID: level must be S, M, or L');
  const rank = { S: 0, M: 1, L: 2 };
  if (rank[risk.level] < rank[state.risk.level]) {
    throw new Error(`RISK_DOWNGRADE_FORBIDDEN: cannot change ${state.risk.level} to ${risk.level}; reopen a new cycle if the original assessment was wrong`);
  }
  const upgraded = rank[risk.level] > rank[state.risk.level];
  state.risk = {
    level: risk.level,
    reasons: Array.isArray(risk.reasons) ? risk.reasons.map(String) : state.risk.reasons,
    upgraded: state.risk.upgraded || upgraded,
  };
  if (upgraded) {
    for (const name of ['enter_dev', 'ship', 'acceptance']) {
      const gate = state.gates?.[name];
      if (gate && ['approved', 'needs_reconfirm'].includes(gate.status)) {
        gate.status = state.risk.level === 'L' ? 'invalidated' : 'needs_reconfirm';
      }
    }
  }
  if (state.risk.level === 'L') {
    state.next_action = { owner: 'agent', action: 'L 级已识别；停止 P0 轻量流程，转入现有 task-registry 与长任务执行规约。' };
  }
  state.updated_at = isoNow();
  return state.risk;
}

function normalizeDataWrite(write) {
  if (!write || typeof write !== 'object' || Array.isArray(write)) {
    throw new Error('DATA_WRITE_INVALID: write must be an object');
  }
  const normalized = {};
  for (const key of ['environment', 'database', 'schema', 'table', 'operation', 'access_mode', 'host_ref', 'account_ref']) {
    if (typeof write[key] !== 'string' || write[key].trim() === '') {
      throw new Error(`DATA_WRITE_INVALID: ${key} is required`);
    }
    normalized[key] = write[key].trim();
  }
  normalized.operation = normalized.operation.toLowerCase();
  if (!DATA_WRITE_OPERATIONS.includes(normalized.operation)) {
    throw new Error(`DATA_WRITE_INVALID: operation must be one of ${DATA_WRITE_OPERATIONS.join(', ')}`);
  }
  return normalized;
}

function resolveDataWriteScope(state, write, options = {}) {
  const loadedPolicy = loadAndValidatePolicy(state, options.policiesRoot ?? POLICY_ROOT, options.now ?? new Date());
  if (state.data_policy?.scope?.status !== 'approved') {
    throw new Error('DATA_WRITE_DENIED: data scope must be approved before any write');
  }
  const matches = (state.data_policy.scope.tables ?? []).filter((table) =>
    table.environment === write.environment
      && table.database === write.database
      && table.schema === write.schema
      && table.table === write.table
      && table.access_mode === write.access_mode);
  if (matches.length !== 1) {
    throw new Error(`DATA_WRITE_DENIED: ${write.database}.${write.schema}.${write.table} (${write.access_mode}) must match exactly one approved run-scope entry`);
  }
  const table = matches[0];
  const policyMatch = matchTableToPolicy(loadedPolicy.policy, { ...write });
  if (!policyMatch.ok) throw new Error(`DATA_WRITE_DENIED: ${policyMatch.reason}`);
  if (!table.host_ref || table.host_ref !== write.host_ref) {
    throw new Error('DATA_WRITE_DENIED: host_ref does not match the approved run scope');
  }
  if (!table.account_ref || table.account_ref !== write.account_ref) {
    throw new Error('DATA_WRITE_DENIED: account_ref does not match the approved run scope');
  }
  return { loadedPolicy, table };
}

function dataWriteAuthorizationProjection(state, write) {
  return {
    run_id: state.run_id,
    claim_id: state.ownership.claim_id,
    policy_version: state.data_policy.policy_version,
    data_policy_hash: state.data_policy.policy_hash,
    data_scope_hash: state.data_policy.scope_hash,
    enter_dev_gate_hash: state.gates.enter_dev.gate_hash,
    ...write,
  };
}

export function checkDataWrite(state, write, options = {}) {
  assertStateShape(state);
  const normalized = normalizeDataWrite(write);
  if (state.risk?.level === 'L') {
    throw new Error('DATA_WRITE_DENIED: L runs must use the existing long-task workflow');
  }
  if (state.plan?.data_access !== true) {
    throw new Error('DATA_WRITE_DENIED: plan.data_access must be true');
  }
  const gateResult = validateGate(state, 'enter_dev', {
    sessionId: options.sessionId,
    machineId: options.machineId,
    allowEnterDevCandidate: true,
    policiesRoot: options.policiesRoot ?? POLICY_ROOT,
    now: options.now,
  });
  if (!gateResult.ok) throw new Error(`DATA_WRITE_DENIED: enter_dev gate is not valid: ${gateResult.errors.join('; ')}`);
  resolveDataWriteScope(state, normalized, options);
  const projection = {
    ...dataWriteAuthorizationProjection(state, normalized),
    write_checked_at: options.now ? new Date(options.now).toISOString() : isoNow(),
  };
  return {
    ...projection,
    write_authorization_id: sha256(projection),
  };
}

function validateDataWriteEvidence(state, item, options = {}) {
  const normalized = normalizeDataWrite(item);
  resolveDataWriteScope(state, normalized, options);
  for (const key of ['data_policy_hash', 'data_scope_hash', 'enter_dev_gate_hash', 'write_checked_at', 'write_authorization_id']) {
    if (typeof item[key] !== 'string' || item[key].trim() === '') {
      throw new Error(`DATA_WRITE_EVIDENCE_INVALID: ${key} is required`);
    }
  }
  if (item.data_policy_hash !== state.data_policy.policy_hash) throw new Error('DATA_WRITE_EVIDENCE_INVALID: data_policy_hash mismatch');
  if (item.data_scope_hash !== state.data_policy.scope_hash) throw new Error('DATA_WRITE_EVIDENCE_INVALID: data_scope_hash mismatch');
  const gateHashes = new Set(
    (state.transitions ?? [])
      .filter((transition) => transition.gate === 'enter_dev' && transition.result === 'PASS' && transition.gate_hash)
      .map((transition) => transition.gate_hash),
  );
  if (state.gates?.enter_dev?.status === 'approved') gateHashes.add(state.gates.enter_dev.gate_hash);
  if (!gateHashes.has(item.enter_dev_gate_hash)) {
    throw new Error('DATA_WRITE_EVIDENCE_INVALID: enter_dev gate hash is not an approved historical or current gate');
  }
  if (Number.isNaN(new Date(item.write_checked_at).getTime())) throw new Error('DATA_WRITE_EVIDENCE_INVALID: write_checked_at must be an ISO date-time');
  const expected = sha256({
    ...dataWriteAuthorizationProjection(state, normalized),
    write_checked_at: item.write_checked_at,
  });
  if (expected !== item.write_authorization_id) throw new Error('DATA_WRITE_EVIDENCE_INVALID: write_authorization_id mismatch');
  return normalized;
}

export function recordEvidence(runDir, manifest, evidence, options = {}) {
  if (!evidence || typeof evidence !== 'object') throw new Error('EVIDENCE_INVALID: evidence must be an object');
  for (const key of ['evidence_id', 'kind', 'result', 'raw_path', 'commit_sha', 'environment', 'collected_at']) {
    if (typeof evidence[key] !== 'string' || evidence[key].trim() === '') throw new Error(`EVIDENCE_INVALID: ${key} is required`);
  }
  if (isAbsolute(evidence.raw_path)) throw new Error('EVIDENCE_INVALID: raw_path must be relative to the run directory');
  const rawPath = resolveInside(runDir, evidence.raw_path);
  if (!isWithin(join(runDir, 'evidence'), rawPath)) throw new Error('EVIDENCE_INVALID: raw_path must stay under evidence/');
  if (!['PASS', 'FAIL', 'SKIPPED', 'SIMULATED'].includes(evidence.result)) throw new Error('EVIDENCE_INVALID: result is invalid');
  if (typeof evidence.reviewable !== 'boolean') throw new Error('EVIDENCE_INVALID: reviewable must be boolean');
  if (typeof evidence.raw_retained !== 'boolean') throw new Error('EVIDENCE_INVALID: raw_retained must be boolean');
  if (evidence.reviewable === true && evidence.raw_retained !== true) {
    throw new Error('EVIDENCE_INVALID: reviewable=true requires raw_retained=true in P0');
  }
  if ((manifest.items ?? []).some((candidate) => candidate.evidence_id === evidence.evidence_id)) {
    throw new Error(`EVIDENCE_INVALID: duplicate evidence_id ${evidence.evidence_id}`);
  }
  if (evidence.reviewable === false && !normalizeSpace(evidence.non_reviewable_reason)) {
    throw new Error('EVIDENCE_INVALID: non_reviewable_reason is required when reviewable=false');
  }
  if (evidence.raw_retained === true && !existsSync(rawPath)) {
    throw new Error(`EVIDENCE_INVALID: retained raw file does not exist: ${evidence.raw_path}`);
  }
  let actualHash = evidence.sha256 ?? null;
  if (existsSync(rawPath)) {
    const diskHash = hashFile(rawPath);
    if (actualHash && actualHash !== diskHash) throw new Error('EVIDENCE_INVALID: sha256 mismatch');
    actualHash = diskHash;
  }
  if (!actualHash) throw new Error('EVIDENCE_INVALID: sha256 is required when raw_retained=false');
  let dataWrite = null;
  if (evidence.kind === 'db') {
    if (!options.state) throw new Error('EVIDENCE_INVALID: db evidence requires the current state for policy/scope validation');
    dataWrite = validateDataWriteEvidence(options.state, evidence, options);
  }
  const item = {
    evidence_id: evidence.evidence_id,
    kind: evidence.kind,
    result: evidence.result,
    raw_path: evidence.raw_path,
    sha256: actualHash,
    reviewable: evidence.reviewable,
    raw_retained: evidence.raw_retained,
    non_reviewable_reason: evidence.non_reviewable_reason ?? null,
    command: evidence.command ?? null,
    exit_code: Number.isInteger(evidence.exit_code) ? evidence.exit_code : null,
    stdout_path: evidence.stdout_path ?? null,
    commit_sha: evidence.commit_sha,
    environment: evidence.environment,
    collected_at: evidence.collected_at,
    summary: evidence.summary ?? null,
    ...(dataWrite ? {
      operation: dataWrite.operation,
      database: dataWrite.database,
      schema: dataWrite.schema,
      table: dataWrite.table,
      access_mode: dataWrite.access_mode,
      host_ref: dataWrite.host_ref,
      account_ref: dataWrite.account_ref,
      data_policy_hash: evidence.data_policy_hash,
      data_scope_hash: evidence.data_scope_hash,
      enter_dev_gate_hash: evidence.enter_dev_gate_hash,
      write_checked_at: evidence.write_checked_at,
      write_authorization_id: evidence.write_authorization_id,
    } : {}),
  };
  manifest.items = [...(manifest.items ?? []), item];
  manifest.updated_at = isoNow();
  if (options.persist !== false) writeJson(join(runDir, 'evidence', 'manifest.json'), manifest);
  return item;
}

/** Append a batch of evidence in one manifest read-modify-write transaction. */
export function recordEvidenceBatch(runDir, manifest, evidenceItems, options = {}) {
  if (!Array.isArray(evidenceItems) || evidenceItems.length === 0) {
    throw new Error('EVIDENCE_BATCH_INVALID: evidence batch must be a non-empty array');
  }
  const nextManifest = structuredClone(manifest);
  const items = evidenceItems.map((item) => recordEvidence(runDir, nextManifest, item, {
    ...options,
    persist: false,
  }));
  nextManifest.updated_at = isoNow();
  writeJson(join(runDir, 'evidence', 'manifest.json'), nextManifest);
  return items;
}

export function verifyEvidence(state, manifest, runDir) {
  assertStateShape(state);
  const errors = [];
  if (manifest?.schema_version !== 1) errors.push('manifest.schema_version must be 1');
  if (manifest?.run_id !== state.run_id) errors.push('manifest.run_id mismatch');
  const seen = new Set();
  const items = Array.isArray(manifest?.items) ? manifest.items : [];
  if (!Array.isArray(manifest?.items)) errors.push('manifest.items must be an array');
  else if (items.length === 0) errors.push('manifest.items must not be empty');
  for (const [index, item] of items.entries()) {
    for (const key of ['evidence_id', 'kind', 'result', 'raw_path', 'sha256', 'commit_sha', 'environment', 'collected_at']) {
      if (typeof item?.[key] !== 'string' || item[key].trim() === '') errors.push(`manifest.items[${index}].${key} is required`);
    }
    if (seen.has(item.evidence_id)) errors.push(`duplicate evidence_id ${item.evidence_id}`);
    seen.add(item.evidence_id);
    if (typeof item.reviewable !== 'boolean') errors.push(`evidence ${item.evidence_id}: reviewable must be boolean`);
    if (typeof item.raw_retained !== 'boolean') errors.push(`evidence ${item.evidence_id}: raw_retained must be boolean`);
    if (item.kind === 'db') {
      try {
        validateDataWriteEvidence(state, item);
      } catch (error) {
        errors.push(`evidence ${item.evidence_id}: ${error.message}`);
      }
    }
    if (item.reviewable === false && !normalizeSpace(item.non_reviewable_reason)) {
      errors.push(`evidence ${item.evidence_id}: non_reviewable_reason is required`);
    }
    if (item.command != null && (typeof item.command !== 'string' || !item.command.trim())) {
      errors.push(`evidence ${item.evidence_id}: command must be a non-empty string when present`);
    }
    if (item.exit_code != null && !Number.isInteger(item.exit_code)) {
      errors.push(`evidence ${item.evidence_id}: exit_code must be an integer when present`);
    }
    if (item.result === 'PASS' && item.exit_code != null && item.exit_code !== 0) {
      errors.push(`evidence ${item.evidence_id}: PASS evidence cannot have non-zero exit_code`);
    }
    if (item.stdout_path != null) {
      if (typeof item.stdout_path !== 'string' || isAbsolute(item.stdout_path)) {
        errors.push(`evidence ${item.evidence_id}: stdout_path must be relative`);
      } else {
        try {
          const stdoutPath = resolveInside(runDir, item.stdout_path);
          if (!isWithin(join(runDir, 'evidence'), stdoutPath)) errors.push(`evidence ${item.evidence_id}: stdout_path escapes evidence/`);
          else if (!existsSync(stdoutPath)) errors.push(`evidence ${item.evidence_id}: stdout_path is missing`);
        } catch (error) {
          errors.push(`evidence ${item.evidence_id}: ${error.message}`);
        }
      }
    }
    if (typeof item.raw_path !== 'string' || isAbsolute(item.raw_path)) {
      errors.push(`evidence ${item.evidence_id}: raw_path must be relative`);
      continue;
    }
    if (item.reviewable === true && item.raw_retained !== true) {
      errors.push(`evidence ${item.evidence_id}: reviewable=true requires raw_retained=true in P0`);
    }
    if (item.raw_retained === true) {
      try {
        const rawPath = resolveInside(runDir, item.raw_path);
        if (!isWithin(join(runDir, 'evidence'), rawPath)) errors.push(`evidence ${item.evidence_id}: raw_path escapes evidence/`);
        else if (!existsSync(rawPath)) errors.push(`evidence ${item.evidence_id}: raw file is missing`);
        else if (hashFile(rawPath) !== item.sha256) errors.push(`evidence ${item.evidence_id}: sha256 mismatch`);
      } catch (error) {
        errors.push(`evidence ${item.evidence_id}: ${error.message}`);
      }
    }
  }
  const verifiedIds = new Set(items.map((item) => item.evidence_id));
  for (const item of state.verification_matrix ?? []) {
    for (const ref of item.evidence_refs ?? []) {
      const evidenceId = String(ref).split('#').at(-1);
      if (!verifiedIds.has(evidenceId)) errors.push(`verification ${item.id ?? '<unknown>'}: evidence ${evidenceId} is missing from manifest`);
    }
  }
  for (const ref of state.ship_package?.dev_verification?.evidence_refs ?? []) {
    const evidenceId = String(ref).split('#').at(-1);
    if (!verifiedIds.has(evidenceId)) errors.push(`dev verification: evidence ${evidenceId} is missing from manifest`);
  }
  const result = {
    result: errors.length ? 'FAIL' : 'PASS',
    checked_at: isoNow(),
    manifest_hash: sha256(manifest),
    item_count: items.length,
    evidence_ids: items.map((item) => item.evidence_id),
    evidence_results: Object.fromEntries(items.map((item) => [item.evidence_id, {
      result: item.result,
      reviewable: item.reviewable,
      raw_retained: item.raw_retained,
    }])),
    non_reviewable: items.filter((item) => item.reviewable === false || item.raw_retained === false).map((item) => item.evidence_id),
    errors,
  };
  state.evidence = {
    ...(state.evidence ?? {}),
    manifest: 'evidence/manifest.json',
    missing: errors,
    verification: result,
  };
  if (state.gates.ship.status === 'approved' && state.phase === 'READY_SHIP') {
    state.gates.ship.status = 'invalidated';
  }
  state.updated_at = isoNow();
  return result;
}

export function recordReview(state, review) {
  if (!review || !Array.isArray(review.repos) || review.repos.length === 0) {
    throw new Error('REVIEW_INVALID: review.repos must be a non-empty array');
  }
  const seen = new Set();
  const normalized = review.repos.map((item, index) => {
    for (const key of ['repo_id', 'reviewer', 'reviewed_sha', 'verdict', 'scope']) {
      if (typeof item?.[key] !== 'string' || item[key].trim() === '') {
        throw new Error(`REVIEW_INVALID: review.repos[${index}].${key} is required`);
      }
    }
    if (!['PASS', 'FAIL'].includes(item.verdict)) throw new Error(`REVIEW_INVALID: review.repos[${index}].verdict must PASS or FAIL`);
    if (typeof item.independent !== 'boolean') throw new Error(`REVIEW_INVALID: review.repos[${index}].independent must be boolean`);
    if (seen.has(item.repo_id)) throw new Error(`REVIEW_INVALID: duplicate repo_id ${item.repo_id}`);
    seen.add(item.repo_id);
    const normalizedItem = {
      ...item,
      findings: Array.isArray(item.findings) ? item.findings : [],
      round: Number.isInteger(item.round) ? item.round : 1,
    };
    normalizedItem.review_hash = reviewHash(normalizedItem);
    return normalizedItem;
  });
  if (!exactRepoSet(state.repos, normalized)) throw new Error('REVIEW_INVALID: review.repos must exactly equal state.repos');
  for (const item of normalized) {
    const repo = (state.repos ?? []).find((candidate) => candidate.repo_id === item.repo_id);
    if (!repo) throw new Error(`REVIEW_INVALID: ${item.repo_id} is not present in state.repos`);
    if (repo.candidate_sha !== item.reviewed_sha) throw new Error(`REVIEW_INVALID: ${item.repo_id} reviewed_sha does not match candidate_sha`);
    if (state.risk.level !== 'S' && item.independent !== true) throw new Error(`REVIEW_INVALID: ${item.repo_id} M/L review must be independent`);
  }
  assertStateShape(state);
  state.review = { repos: normalized };
  if (state.gates.ship.status === 'approved') state.gates.ship.status = 'invalidated';
  state.updated_at = isoNow();
  return state.review;
}

export function recordAcceptance(state, acceptance, options = {}) {
  if (!acceptance || typeof acceptance !== 'object') throw new Error('ACCEPTANCE_INVALID: acceptance must be an object');
  const mode = acceptance.mode ?? 'policy_only';
  if (!['policy_only', 'chat_exact'].includes(mode)) {
    throw new Error('ACCEPTANCE_INVALID: mode must be policy_only or chat_exact');
  }
  const normalized = {
    ...acceptance,
    mode,
    operator_verified: false,
  };
  if (!['pending', 'approved', 'rejected'].includes(normalized.status)) {
    throw new Error('ACCEPTANCE_INVALID: status must be pending, approved, or rejected');
  }
  if (normalized.current_status === 'RESOLVED' && !['AWAITING_ACCEPTANCE', 'RESOLVED'].includes(state.phase)) {
    const at = isoNow();
    state.acceptance = {
      ...normalized,
      status: 'rejected',
      mode: 'policy_only',
      anomaly: 'early_resolved',
      observed_at: normalized.observed_at ?? at,
    };
    if (!['BLOCKED', 'CANCELLED'].includes(state.phase)) {
      blockState(state, {
        reason: 'Feishu moved to RESOLVED before the acceptance gate',
        condition: 'human confirms the external transition and supplies acceptance evidence',
        resumePhase: state.phase,
        owner: 'human',
      });
    }
    state.updated_at = isoNow();
    return state.acceptance;
  }
  const chatExactSeen = state.acceptance?.mode === 'chat_exact'
    || state.gates?.acceptance?.token_text === TOKENS.acceptance;
  if (mode === 'policy_only' && chatExactSeen) {
    throw new Error('ACCEPTANCE_DOWNGRADE_FORBIDDEN: chat_exact acceptance cannot be downgraded to policy_only');
  }
  if (normalized.status === 'approved') {
    if (state.phase !== 'AWAITING_ACCEPTANCE') {
      throw new Error(`ACCEPTANCE_INVALID: cannot record approved acceptance in ${state.phase}`);
    }
    if (normalized.current_status !== 'RESOLVED') throw new Error('ACCEPTANCE_INVALID: approved acceptance requires current_status=RESOLVED');
    if (typeof normalized.evidence_ref !== 'string' || normalized.evidence_ref.trim() === '') {
      throw new Error('ACCEPTANCE_INVALID: evidence_ref is required');
    }
    if (typeof normalized.evidence_kind !== 'string' || normalized.evidence_kind.trim() === '') {
      throw new Error('ACCEPTANCE_INVALID: evidence_kind is required');
    }
    if (typeof normalized.observed_at !== 'string' || normalized.observed_at.trim() === '') {
      throw new Error('ACCEPTANCE_INVALID: observed_at is required');
    }
    if (mode === 'chat_exact') {
      const gate = state.gates?.acceptance;
      if (!gate || gate.status !== 'approved') {
        throw new Error('ACCEPTANCE_INVALID: chat_exact requires an approved acceptance gate');
      }
      if (gate.token_text !== TOKENS.acceptance) {
        throw new Error('ACCEPTANCE_INVALID: acceptance gate token must be 验收通过');
      }
      normalized.approval_message = TOKENS.acceptance;
      normalized.approval_ref = acceptance.approval_ref ?? gate.message_ref;
      if (typeof normalized.approval_ref !== 'string' || normalized.approval_ref.trim() === '') {
        throw new Error('ACCEPTANCE_INVALID: approval_ref is required for chat_exact');
      }
      normalized.approved_at = gate.approved_at;
      normalized.approval_session_id = gate.approved_session_id;
      normalized.approval_machine_id = gate.approved_machine_id;
      normalized.gate_hash = gate.gate_hash;
    }
    if (options.runDir) {
      const manifest = readJson(join(options.runDir, 'evidence', 'manifest.json'));
      const verification = verifyEvidence(state, manifest, options.runDir);
      if (verification.result !== 'PASS') throw new Error(`ACCEPTANCE_INVALID: evidence manifest verification failed: ${verification.errors.join('; ')}`);
      const evidence = manifestEvidence(manifest, normalized.evidence_ref);
      if (!evidence.ok) throw new Error(`ACCEPTANCE_INVALID: ${evidence.reason}`);
    }
  }
  assertStateShape(state);
  state.acceptance = normalized;
  state.next_action = normalized.status === 'approved'
    ? { owner: 'agent', action: mode === 'chat_exact' ? '将内部阶段推进为 RESOLVED，并记录 chat_exact 验收 gate。' : '读取飞书外部迁移证据并将内部阶段推进为 RESOLVED。' }
    : nextActionFor(state.phase);
  state.updated_at = isoNow();
  return state.acceptance;
}

export function loadAndValidatePolicy(state, policiesRoot = POLICY_ROOT, now = new Date()) {
  const loaded = loadPolicy(state.data_policy?.policy_version, policiesRoot);
  const errors = validatePolicy(loaded.policy, now);
  if (state.data_policy?.policy_hash !== loaded.policy_hash) {
    errors.push(`state.data_policy.policy_hash mismatch: expected ${loaded.policy_hash}`);
  }
  if (errors.length) throw new Error(`POLICY_INVALID:\n- ${errors.join('\n- ')}`);
  return loaded;
}

function manifestEvidence(manifest, evidenceRef) {
  const [manifestRef, evidenceId] = String(evidenceRef ?? '').split('#');
  if (manifestRef !== 'evidence/manifest.json' || !evidenceId) {
    return { ok: false, reason: 'evidence_ref must be evidence/manifest.json#<evidence_id>' };
  }
  const item = (manifest?.items ?? []).find((candidate) => candidate.evidence_id === evidenceId);
  if (!item) return { ok: false, reason: `evidence ${evidenceId} is missing from manifest` };
  if (!['PASS', 'SIMULATED'].includes(item.result)) return { ok: false, reason: `evidence ${evidenceId} result is ${item.result}` };
  if (item.reviewable !== true || item.raw_retained !== true) {
    return { ok: false, reason: `evidence ${evidenceId} must be reviewable with raw_retained=true for human-approved data scope` };
  }
  return { ok: true, item };
}

export function setDataScope(state, scope, options = {}) {
  if (!scope || typeof scope !== 'object' || Array.isArray(scope)) throw new Error('SCOPE_INVALID: scope must be an object');
  const loadedPolicy = loadAndValidatePolicy(state, options.policiesRoot ?? POLICY_ROOT, options.now ?? new Date());
  const manifest = options.runDir ? readJson(join(options.runDir, 'evidence', 'manifest.json')) : null;
  const normalized = {
    status: scope.status ?? 'pending',
    tables: Array.isArray(scope.tables) ? scope.tables : [],
  };
  if (!['pending', 'approved', 'rejected'].includes(normalized.status)) {
    throw new Error('SCOPE_INVALID: status must be pending, approved, or rejected');
  }
  if (normalized.status === 'approved' && normalized.tables.length === 0) {
    throw new Error('SCOPE_INVALID: approved scope must enumerate at least one table');
  }
  const normalizedTables = normalized.tables.map((table, i) => {
    for (const key of ['database', 'schema', 'table', 'confirmed_by', 'confirmed_at', 'evidence_ref']) {
      requireString(table[key], `scope.tables[${i}].${key}`, []);
      if (typeof table[key] !== 'string' || table[key].trim() === '') {
        throw new Error(`SCOPE_INVALID: scope.tables[${i}].${key} is required`);
      }
    }
    if (/[%*]/.test(table.table)) throw new Error(`SCOPE_INVALID: wildcard table is forbidden at scope.tables[${i}].table`);
    if (!table.confirmed_by.startsWith('human:')) throw new Error(`SCOPE_INVALID: scope.tables[${i}].confirmed_by must start with human:`);
    if (Number.isNaN(new Date(table.confirmed_at).getTime())) throw new Error(`SCOPE_INVALID: scope.tables[${i}].confirmed_at must be ISO date-time`);
    const normalizedTable = {
      database: table.database,
      schema: table.schema,
      table: table.table,
      environment: table.environment ?? (loadedPolicy.policy.status === 'active-demo' ? 'demo' : 'production'),
      access_mode: table.access_mode ?? null,
      host_ref: table.host_ref ?? null,
      account_ref: table.account_ref ?? null,
      confirmed_by: table.confirmed_by,
      confirmed_at: table.confirmed_at,
      evidence_ref: table.evidence_ref,
    };
    const match = matchTableToPolicy(loadedPolicy.policy, normalizedTable);
    if (!match.ok) throw new Error(`SCOPE_INVALID: scope.tables[${i}] rejected by ${loadedPolicy.policy.policy_version}: ${match.reason}`);
    const group = loadedPolicy.policy.allowed[match.group];
    normalizedTable.access_mode = normalizedTable.access_mode
      ?? (group.access === 'application_only' ? 'application_only' : (group.writers?.[0] ?? 'application_only'));
    if (group.host_ref && normalizedTable.host_ref && group.host_ref !== normalizedTable.host_ref) {
      throw new Error(`SCOPE_INVALID: scope.tables[${i}].host_ref does not match policy group ${match.group}`);
    }
    if (group.account_ref && normalizedTable.account_ref && group.account_ref !== normalizedTable.account_ref) {
      throw new Error(`SCOPE_INVALID: scope.tables[${i}].account_ref does not match policy group ${match.group}`);
    }
    normalizedTable.host_ref = normalizedTable.host_ref ?? group.host_ref ?? null;
    normalizedTable.account_ref = normalizedTable.account_ref ?? group.account_ref ?? null;
    if (manifest) {
      const evidence = manifestEvidence(manifest, normalizedTable.evidence_ref);
      if (!evidence.ok) throw new Error(`SCOPE_INVALID: scope.tables[${i}]: ${evidence.reason}`);
    }
    return normalizedTable;
  });
  normalized.tables = normalizedTables;
  assertStateShape(state);
  state.data_policy.scope = normalized;
  state.data_policy.scope_hash = sha256(normalized);
  for (const gateName of ['enter_dev', 'ship', 'acceptance']) {
    if (state.gates?.[gateName]?.status === 'approved') {
      state.gates[gateName].status = 'invalidated';
      state.gates[gateName].validation = {
        result: 'FAIL',
        checked_at: isoNow(),
        validator_version: VALIDATOR_VERSION,
        actual: state.data_policy.scope_hash,
        expected: state.gates[gateName].gate_hash,
        errors: ['data scope changed; gate invalidated'],
      };
    }
  }
  state.updated_at = isoNow();
  return state.data_policy;
}

export function blockState(state, input) {
  assertStateShape(state);
  if (state.phase === 'RESOLVED' || state.phase === 'CANCELLED' || state.phase === 'BLOCKED') {
    throw new Error(`BLOCK_INVALID: cannot block from ${state.phase}`);
  }
  const resumePhase = input.resumePhase ?? state.phase;
  if (!PHASES.includes(resumePhase) || ['BLOCKED', 'CANCELLED', 'RESOLVED'].includes(resumePhase)) {
    throw new Error(`BLOCK_INVALID: resume_phase is invalid: ${resumePhase}`);
  }
  const allowedResumePhases = new Set([state.phase, ...(ALLOWED_TRANSITIONS[state.phase] ?? [])]);
  if (!allowedResumePhases.has(resumePhase)) {
    throw new Error(`BLOCK_INVALID: resume_phase ${resumePhase} is not reachable from ${state.phase}`);
  }
  if (!normalizeSpace(input.reason)) throw new Error('BLOCK_INVALID: reason is required');
  if (!normalizeSpace(input.condition)) throw new Error('BLOCK_INVALID: resume condition is required');
  const blockedFrom = state.phase;
  const at = isoNow();
  state.transitions.push({
    from: blockedFrom,
    to: 'BLOCKED',
    at,
    result: 'BLOCKED',
    validator_version: VALIDATOR_VERSION,
    claim_id: state.ownership.claim_id,
    session_id: input.sessionId ?? state.ownership.session_id ?? null,
    gate: null,
    gate_hash: null,
    evidence_refs: input.evidenceRefs ?? [],
    summary: input.reason,
  });
  state.phase = 'BLOCKED';
  state.blocked_from = blockedFrom;
  state.resume_phase = resumePhase;
  state.resume_condition = input.condition;
  state.blockers.push({
    reason: input.reason,
    owner: input.owner ?? 'human',
    resume_condition: input.condition,
    at,
  });
  state.next_action = { owner: input.owner ?? 'human', action: input.reason };
  state.updated_at = at;
  return state;
}

export function cancelState(state, input) {
  assertStateShape(state);
  if (['RESOLVED', 'CANCELLED'].includes(state.phase)) {
    throw new Error(`CANCEL_INVALID: cannot cancel from ${state.phase}`);
  }
  if (!normalizeSpace(input.reason)) throw new Error('CANCEL_INVALID: reason is required');
  const at = isoNow();
  state.transitions.push({
    from: state.phase,
    to: 'CANCELLED',
    at,
    result: 'CANCELLED',
    validator_version: VALIDATOR_VERSION,
    claim_id: state.ownership.claim_id,
    session_id: input.sessionId ?? state.ownership.session_id ?? null,
    gate: null,
    gate_hash: null,
    evidence_refs: input.evidenceRefs ?? [],
    summary: input.reason,
  });
  state.phase = 'CANCELLED';
  state.cancellation = {
    by: input.actor ?? 'current_user',
    reason: input.reason,
    at,
    cleanup: input.cleanup ?? 'PENDING',
  };
  state.next_action = { owner: input.actor ?? 'current_user', action: '确认取消后的分支、MR 和 dev 部署清理' };
  state.updated_at = at;
  return state;
}

export function takeoverState(state, input) {
  assertStateShape(state);
  const expected = `接管【${state.work_item.auto_number}】`;
  if (input.message !== expected) throw new Error(`TAKEOVER_TOKEN_INVALID: expected exact ${expected}`);
  if (typeof input.claimId !== 'string' || input.claimId.trim() === '') throw new Error('TAKEOVER_INVALID: new claim id is required');
  if (input.claimId === state.ownership.claim_id) throw new Error('TAKEOVER_INVALID: new claim id must differ from the current claim');
  if (!normalizeSpace(input.claimCommentRef) || !normalizeSpace(input.claimOperator)) {
    throw new Error('TAKEOVER_INVALID: claimCommentRef and claimOperator are required');
  }
  if (typeof input.sessionId !== 'string' || input.sessionId.trim() === '') throw new Error('TAKEOVER_INVALID: session id is required');
  if (typeof input.machineId !== 'string' || input.machineId.trim() === '') throw new Error('TAKEOVER_INVALID: machine id is required');
  if (!normalizeSpace(input.reason)) throw new Error('TAKEOVER_INVALID: reason is required');
  const at = isoNow();
  state.ownership.takeover_history.push({
    from_claim_id: state.ownership.claim_id,
    to_claim_id: input.claimId,
    from_session_id: state.ownership.session_id ?? null,
    from_machine_id: state.ownership.machine_id ?? null,
    from_claim_comment_ref: state.ownership.claim_comment_ref ?? null,
    to_session_id: input.sessionId,
    to_machine_id: input.machineId,
    to_claim_comment_ref: input.claimCommentRef,
    to_claim_operator: input.claimOperator,
    reason: input.reason,
    at,
  });
  state.ownership.claim_id = input.claimId;
  state.ownership.claim_comment_ref = input.claimCommentRef;
  state.ownership.claim_operator = input.claimOperator;
  state.ownership.claimed_at = at;
  state.ownership.session_id = input.sessionId;
  state.ownership.machine_id = input.machineId;
  state.ownership.current_owner = input.owner ?? 'current_user';
  for (const gateName of ['enter_dev', 'ship', 'acceptance']) {
    if (state.gates?.[gateName]?.status === 'approved') state.gates[gateName].status = 'needs_reconfirm';
  }
  state.next_action = { owner: 'agent', action: '接管已记录；重新校验仓库、证据和边界，必要时重新请求当前 gate 口令。' };
  state.updated_at = at;
  return state.ownership;
}

function blankCycleFields(state) {
  state.data_policy.scope = { status: 'pending', tables: [] };
  state.data_policy.scope_hash = sha256(state.data_policy.scope);
  state.diagnosis = { symptom: null, reproduction: [], root_cause: null, counter_evidence: [], requirement_refs: [], impact_scope: [] };
  state.plan = { change_scope: [], non_goals: [], verification_plan: [], rollback_plan: [], data_access: false };
  state.implementation = { repos: [] };
  state.review = { repos: [] };
  state.verification_matrix = [];
  state.gates = { enter_dev: { status: 'pending', bound_to: null }, ship: { status: 'pending', bound_to: null }, acceptance: { status: 'pending', bound_to: null } };
  state.ship_package = { repos: [], acceptance_steps: [], dev_verification: { result: 'PENDING', evidence_refs: [] }, summary: null };
  state.acceptance = {
    status: 'pending',
    mode: 'policy_only',
    operator_verified: false,
    work_item_status: 'IN PROGRESS',
  };
  state.transitions = [];
  state.failure_stage = null;
  state.failure_class = null;
  state.patch_round = 0;
  state.blocked_from = null;
  state.resume_phase = null;
  state.resume_condition = null;
  state.cancellation = null;
  state.rollback = { repos: [], summary: null };
  state.blockers = [];
  state.evidence = { manifest: 'evidence/manifest.json', missing: [], verification: null };
}

export function reopenState(state, input) {
  assertStateShape(state);
  if (!['RESOLVED', 'CANCELLED', 'AWAITING_ACCEPTANCE', 'DEV_VERIFY_FAILED'].includes(state.phase)) {
    throw new Error(`REOPEN_INVALID: cannot reopen from ${state.phase}`);
  }
  if (!normalizeSpace(input.reason)) throw new Error('REOPEN_INVALID: reason is required');
  const oldPhase = state.phase;
  const archivedAt = isoNow();
  const oldCycleId = state.current_cycle_id;
  const archivePath = join(input.runDir, 'cycles', oldCycleId, 'state.json');
  const oldEntry = state.cycles.find((c) => c.cycle_id === oldCycleId);
  if (oldEntry) {
    oldEntry.closed_at = archivedAt;
    oldEntry.close_reason = input.reason;
    oldEntry.state_ref = `cycles/${oldCycleId}/state.json`;
  }
  state.next_action = { owner: 'agent', action: '归档完成，开始新 cycle 的重新诊断。' };
  const archived = structuredClone(state);
  writeJson(archivePath, archived);
  const currentManifestPath = join(input.runDir, 'evidence', 'manifest.json');
  if (existsSync(currentManifestPath)) {
    writeJson(join(input.runDir, 'cycles', oldCycleId, 'evidence', 'manifest.json'), readJson(currentManifestPath));
    writeJson(currentManifestPath, {
      schema_version: 1,
      run_id: state.run_id,
      updated_at: archivedAt,
      items: [],
    });
  }
  const nextSeq = state.cycle_seq + 1;
  const nextCycleId = `cycle-${String(nextSeq).padStart(3, '0')}-${compactTimestamp(archivedAt)}`;
  state.cycle_seq = nextSeq;
  state.current_cycle_id = nextCycleId;
  state.cycles.push({
    cycle_id: nextCycleId,
    seq: nextSeq,
    started_at: archivedAt,
    closed_at: null,
    close_reason: null,
    state_ref: null,
  });
  if (input.claimId) state.ownership.claim_id = input.claimId;
  state.phase = 'REOPENED';
  blankCycleFields(state);
  state.transitions.push({
    from: oldPhase,
    to: 'REOPENED',
    at: archivedAt,
    result: 'REOPENED',
    validator_version: VALIDATOR_VERSION,
    claim_id: state.ownership.claim_id,
    session_id: input.sessionId ?? state.ownership.session_id ?? null,
    gate: null,
    gate_hash: null,
    evidence_refs: input.evidenceRefs ?? [],
    summary: input.reason,
  });
  state.next_action = { owner: 'agent', action: '重新诊断根因、影响范围、需规依据和数据 scope，然后展示新的进入开发绑定对象' };
  state.updated_at = archivedAt;
  return state;
}

export function createInitialState(input) {
  const at = isoNow();
  const autoNumber = numericIdentifier(input.autoNumber, 'auto_number');
  const workItemId = numericIdentifier(input.workItemId, 'work_item_id');
  const initialPhase = input.phase ?? 'CLAIMED';
  if (!['INTAKE', 'CLAIMED'].includes(initialPhase)) {
    throw new Error(`INIT_PHASE_INVALID: init accepts only INTAKE or CLAIMED, got ${initialPhase}`);
  }
  if (initialPhase === 'CLAIMED') {
    if (!normalizeSpace(input.claimCommentRef) || !normalizeSpace(input.claimOperator)) {
      throw new Error('INIT_CLAIM_EVIDENCE_REQUIRED: CLAIMED requires claimCommentRef and claimOperator');
    }
  }
  const cycleId = `cycle-001-${compactTimestamp(at)}`;
  const runId = `${autoNumber}-${workItemId}`;
  const scope = { status: 'pending', tables: [] };
  return {
    schema_version: SCHEMA_VERSION,
    run_id: runId,
    current_cycle_id: cycleId,
    cycle_seq: 1,
    cycles: [
      {
        cycle_id: cycleId,
        seq: 1,
        started_at: at,
        closed_at: null,
        close_reason: null,
        state_ref: null,
      },
    ],
    work_item: {
      project_key: input.projectKey ?? '6a687a81e231818dec771f9a',
      auto_number: autoNumber,
      work_item_id: workItemId,
      title: input.title,
      owner: input.owner ?? null,
      qa_bug_id: input.qaBugId ?? null,
      task_registry_id: input.taskRegistryId ?? null,
    },
    ownership: {
      claim_id: input.claimId,
      claim_comment_ref: input.claimCommentRef ?? null,
      claim_operator: input.claimOperator ?? null,
      claimed_at: initialPhase === 'CLAIMED' ? at : null,
      session_id: input.sessionId ?? null,
      machine_id: input.machineId ?? null,
      current_owner: input.owner ?? 'current_user',
      takeover_history: [],
    },
    phase: initialPhase,
    risk: {
      level: input.risk ?? 'M',
      reasons: [],
      upgraded: false,
    },
    repos: [],
    machine_local: input.machineLocal ?? null,
    data_policy: {
      policy_version: input.policyVersion ?? 'demo-2026-11-10',
      policy_hash: input.policyHash ?? null,
      scope_hash: sha256(scope),
      scope,
    },
    diagnosis: {
      symptom: null,
      reproduction: [],
      root_cause: null,
      counter_evidence: [],
      requirement_refs: [],
      impact_scope: [],
    },
    plan: {
      change_scope: [],
      non_goals: [],
      verification_plan: [],
      rollback_plan: [],
      data_access: false,
    },
    implementation: { repos: [] },
    review: { repos: [] },
    verification_matrix: [],
    gates: {
      enter_dev: { status: 'pending', bound_to: null },
      ship: { status: 'pending', bound_to: null },
      acceptance: { status: 'pending', bound_to: null },
    },
    ship_package: {
      repos: [],
      acceptance_steps: [],
      dev_verification: { result: 'PENDING', evidence_refs: [] },
      summary: null,
    },
    acceptance: {
      status: 'pending',
      mode: 'policy_only',
      operator_verified: false,
      work_item_status: 'IN PROGRESS',
    },
    transitions: [],
    failure_stage: null,
    failure_class: null,
    patch_round: 0,
    blocked_from: null,
    resume_phase: null,
    resume_condition: null,
    cancellation: null,
    decisions: [],
    artifacts: { report: 'report.md' },
    evidence: { manifest: 'evidence/manifest.json', missing: [], verification: null },
    rollback: { repos: [], summary: null },
    cost_summary: { status: 'UNAVAILABLE' },
    blockers: [],
    next_action: {
      owner: 'agent',
      action: '完成诊断并展示进入开发的绑定对象',
    },
    updated_at: at,
  };
}

function runPath(input) {
  const explicitRunDir = input.runDir ?? input['run-dir'];
  const autoNumber = input.autoNumber ?? input['auto-number'];
  const workItemId = input.workItemId ?? input['work-item-id'];
  if (explicitRunDir) return resolve(explicitRunDir);
  if (!autoNumber || !workItemId) throw new Error('--run-dir or both --auto-number and --work-item-id are required');
  return join(RUNS_ROOT, `${numericIdentifier(autoNumber, '--auto-number')}-${numericIdentifier(workItemId, '--work-item-id')}`);
}

function loadRun(runDir) {
  const statePath = join(runDir, 'state.json');
  if (!existsSync(statePath)) throw new Error(`RUN_NOT_FOUND: ${statePath}`);
  return readJson(statePath);
}

function saveRun(runDir, state) {
  assertStateShape(state);
  writeJson(join(runDir, 'state.json'), state);
}

function md(value) {
  if (value == null || value === '') return 'PENDING';
  return String(value).replace(/\|/g, '\\|').replace(/\n/g, '<br>');
}

function listOrPending(items, formatter = (x) => String(x)) {
  if (!items || items.length === 0) return '- PENDING';
  return items.map((item) => `- ${formatter(item)}`).join('\n');
}

export function renderReport(state, manifest = { items: [] }) {
  const risk = state.risk ?? { level: 'PENDING', reasons: [] };
  const dataTables = state.data_policy?.scope?.tables ?? [];
  const gateRows = ['enter_dev', 'ship', 'acceptance']
    .map((name) => {
      const g = state.gates?.[name] ?? { status: 'PENDING' };
      return `| ${name} | ${md(g.status)} | ${md(g.token_text)} | ${md(g.gate_hash)} |`;
    })
    .join('\n');
  const evidenceRows = (manifest.items ?? [])
    .map((e) => `| ${md(e.evidence_id)} | ${md(e.kind)} | ${md(e.result)} | ${e.reviewable ? 'yes' : 'no'} | ${e.raw_retained ? 'yes' : 'no'} | ${md(e.non_reviewable_reason)} | ${md(e.commit_sha)} | ${md(e.summary)} |`)
    .join('\n');
  const repos = state.repos ?? [];
  const bundleKind = repos.length > 1 ? `跨仓 Bundle（${repos.length} repos）` : '单仓';
  return `# 缺陷修复报告：${state.work_item.auto_number} ${state.work_item.title}

> 本文件由 \`.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs render-report\` 从 \`state.json\` 和 \`evidence/manifest.json\` 渲染，不手工补写事实。
> 生成时间：${isoNow()}
> 当前 cycle：${state.current_cycle_id}
> 当前内部阶段：${state.phase}
> 验收模式：${state.acceptance?.mode ?? 'policy_only'}（operator_verified=${state.acceptance?.operator_verified ?? false}）

## 1. 缺陷事实和复现

| 字段 | 值 |
|---|---|
| 飞书编号 | 【${md(state.work_item.auto_number)}】${md(state.work_item.title)} |
| 内部 ID | ${md(state.work_item.work_item_id)} |
| 当前负责人 | ${md(state.work_item.owner)} |
| 现象 | ${md(state.diagnosis?.symptom)} |

${listOrPending(state.diagnosis?.reproduction, (x) => md(typeof x === 'string' ? x : JSON.stringify(x)))}

## 2. 根因、需规依据和影响范围

- 根因：${md(state.diagnosis?.root_cause)}
- 反证：${md((state.diagnosis?.counter_evidence ?? []).join('；'))}
- 需规依据：${md((state.diagnosis?.requirement_refs ?? []).join('；'))}
- 影响范围：${md((state.diagnosis?.impact_scope ?? []).join('；'))}

## 3. 改动摘要、跨仓 Bundle 和非目标

- Bundle 类型：${md(bundleKind)}
- 同一飞书缺陷涉及多个仓库时仍是一个 run、一个 claim、一套 gate；各仓保留独立候选 SHA。

${listOrPending(repos, (r) => `${md(r.repo_id)}：${md(r.repo_name)}，role=${md(r.role)}，ship_order=${md(r.ship_order)}，depends_on=${md((r.depends_on ?? []).join(', '))}，base=${md(r.base_sha)}，candidate=${md(r.candidate_sha)}，scope=${md((r.planned_change_scope ?? []).join(', '))}`)}

实现仓校验：

${listOrPending(state.implementation?.repos, (r) => `${md(r.repo_id)}：candidate=${md(r.candidate_sha)}，diff_hash=${md(r.diff_hash)}，git_verified=${r.git_verified === true ? 'yes' : 'no'}，files=${md((r.changed_files ?? []).join(', '))}`)}

非目标：${md((state.plan?.non_goals ?? []).join('；'))}

## 4. 验证矩阵和证据结果

${listOrPending(state.verification_matrix, (v) => `${md(v.category)} / ${md(v.behavior ?? v.name)}：${md(v.result)}；evidence=${md((v.evidence_refs ?? []).join(', '))}`)}

${evidenceRows ? `| evidence_id | kind | result | reviewable | raw_retained | non-reviewable reason | commit | summary |\n|---|---|---|---|---|---|---|---|\n${evidenceRows}` : '- PENDING'}

DB 写证据授权：

${listOrPending((manifest.items ?? []).filter((item) => item.kind === 'db'), (item) => `${md(item.evidence_id)}：${md(item.database)}.${md(item.schema)}.${md(item.table)}；operation=${md(item.operation)}；gate=${md(item.enter_dev_gate_hash)}；policy=${md(item.data_policy_hash)}；scope=${md(item.data_scope_hash)}；authorization=${md(item.write_authorization_id)}`)}

- manifest 校验：${md(state.evidence?.verification?.result)}；manifest_hash=${md(state.evidence?.verification?.manifest_hash)}；不可复核证据=${md((state.evidence?.verification?.non_reviewable ?? []).join(', '))}

## 5. 已知风险和未覆盖项

${listOrPending(risk.reasons, (x) => md(typeof x === 'string' ? x : JSON.stringify(x)))}

阻塞记录：

${listOrPending(state.blockers, (b) => `${md(b.at)} → ${md(b.resolved_at ?? 'OPEN')}；owner=${md(b.owner)}；reason=${md(b.reason)}；resume_evidence=${md((b.resume_evidence_refs ?? []).join(', '))}`)}

评审记录：

${listOrPending(state.review?.repos, (r) => `${md(r.repo_id)}：reviewer=${md(r.reviewer)}，independent=${r.independent}，sha=${md(r.reviewed_sha)}，verdict=${md(r.verdict)}，hash=${md(r.review_hash)}，findings=${md((r.findings ?? []).join('；'))}`)}

## 6. S/M/L 风险等级和定级理由

- 等级：${md(risk.level)}
- 是否上调：${risk.upgraded ? '是' : '否'}
- 理由：${md((risk.reasons ?? []).join('；'))}

## 7. 数据 policy、run scope 和确认人

- policy_version：${md(state.data_policy?.policy_version)}
- policy_hash：${md(state.data_policy?.policy_hash)}
- scope_hash：${md(state.data_policy?.scope_hash)}
- scope_status：${md(state.data_policy?.scope?.status)}

${listOrPending(dataTables, (t) => `${md(t.database)}.${md(t.table)}；confirmed_by=${md(t.confirmed_by)}；evidence=${md(t.evidence_ref)}`)}

## 8. failure stage、failure class 和返工轮次

- failure_stage：${md(state.failure_stage)}
- failure_class：${md(state.failure_class)}
- patch_round：${state.patch_round ?? 0}

## 9. 提测信息

> 流水线、rollout 和部署 SHA 来自 Agent 对 GitLab 的查询记录，不是本地脚本直接验证的远端事实。

${listOrPending(state.ship_package?.repos, (r) => `${md(r.repo_id)}：ship_order=${md(r.ship_order)}，MR=${md(r.merge_request_id)}，candidate=${md(r.candidate_sha)}，merge=${md(r.merge_commit_sha)}，deployed=${md(r.deployed_sha)}，pipeline=${md(r.pipeline_id)}，pipeline_url=${md(r.pipeline_url)}，image=${md(r.image_tag)}，rollout=${md(r.rollout_status)}`)}

- dev 复测：${md(state.ship_package?.dev_verification?.result)}；evidence=${md((state.ship_package?.dev_verification?.evidence_refs ?? []).join(', '))}

人工验收步骤：

${listOrPending(state.ship_package?.acceptance_steps, (step) => md(step))}

## 10. 精确验收与飞书状态迁移

- 飞书当前状态：${md(state.acceptance?.work_item_status ?? state.acceptance?.current_status)}
- 验收证据：${md(state.acceptance?.evidence_ref)}
- 验收结论：${md(state.acceptance?.status)}
- 验收模式：${md(state.acceptance?.mode)}
- 验收异常：${md(state.acceptance?.anomaly)}
- 验收口令：${md(state.acceptance?.approval_message)}
- 审批引用：${md(state.acceptance?.approval_ref)}
- chat_exact 验收：仅在收到完整精确消息 \`验收通过\` 后，经 acceptance gate 校验并由 Agent 调用飞书状态迁移。

## 11. Gate 状态与绑定对象

| gate | status | token | hash |
|---|---|---|---|
${gateRows}

enter_dev bound_to：${md(state.gates?.enter_dev?.bound_to ? JSON.stringify(state.gates.enter_dev.bound_to) : null)}

ship bound_to：${md(state.gates?.ship?.bound_to ? JSON.stringify(state.gates.ship.bound_to) : null)}

acceptance bound_to：${md(state.gates?.acceptance?.bound_to ? JSON.stringify(state.gates.acceptance.bound_to) : null)}

## 12. 自动决策摘要

${listOrPending(state.decisions, (d) => `${md(d.decision)}；依据=${md(d.basis)}；备选=${md((d.alternatives ?? []).join(' / '))}；影响=${md(d.impact)}；需人工批准=${d.requires_human_ratification === true ? 'yes' : 'no'}；批准人=${md(d.ratified_by)}`)}

## 13. 回滚版本、回滚方式和回滚验证

${listOrPending(state.rollback?.repos, (r) => `${md(r.repo_id)}：target=${md(r.target_sha)}，revert=${md(r.revert_commit)}，command=${md(r.command)}，verified=${md(r.verification)}`)}
`;
}

function main() {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      'run-dir': { type: 'string' },
      'auto-number': { type: 'string' },
      'work-item-id': { type: 'string' },
      title: { type: 'string' },
      'claim-id': { type: 'string' },
      'claim-comment-ref': { type: 'string' },
      'claim-operator': { type: 'string' },
      'session-id': { type: 'string' },
      'machine-id': { type: 'string' },
      'project-key': { type: 'string' },
      owner: { type: 'string' },
      phase: { type: 'string' },
      risk: { type: 'string' },
      'policy-version': { type: 'string' },
      'policy-hash': { type: 'string' },
      'policies-root': { type: 'string' },
      'machine-local': { type: 'string' },
      'repo-id': { type: 'string' },
      'repo-dir': { type: 'string' },
      'candidate-sha': { type: 'string' },
      'base-sha': { type: 'string' },
      'scope-file': { type: 'string' },
      'scope-json': { type: 'string' },
      'input-file': { type: 'string' },
      'input-json': { type: 'string' },
      'items-file': { type: 'string' },
      'items-json': { type: 'string' },
      'evidence-file': { type: 'string' },
      'evidence-json': { type: 'string' },
      'evidence-batch-file': { type: 'string' },
      'evidence-batch-json': { type: 'string' },
      'repos-file': { type: 'string' },
      'repos-json': { type: 'string' },
      'review-file': { type: 'string' },
      'review-json': { type: 'string' },
      'acceptance-file': { type: 'string' },
      'acceptance-json': { type: 'string' },
      gate: { type: 'string' },
      message: { type: 'string' },
      'binding-file': { type: 'string' },
      'binding-json': { type: 'string' },
      'approved-by': { type: 'string' },
      'message-ref': { type: 'string' },
      'active-runs': { type: 'string' },
      to: { type: 'string' },
      reason: { type: 'string' },
      'resume-phase': { type: 'string' },
      condition: { type: 'string' },
      actor: { type: 'string' },
      cleanup: { type: 'string' },
      'evidence-ref': { type: 'string', multiple: true },
      summary: { type: 'string' },
      help: { type: 'boolean', short: 'h' },
    },
  });
  const command = positionals[0];
  if (!command || values.help) {
    process.stdout.write(`Usage: node .cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs <command> [options]\n\nCommands:\n  init                  Create a run ledger\n  approve-gate          Record an exact chat gate\n  validate-gate         Validate gate binding/hash/claim/session/policy\n  validate-state        Validate state schema and semantic invariants\n  set-repos             Replace authoritative repo bindings\n  set-risk              Record S/M/L risk and invalidate stale gates\n  record-diagnosis      Record diagnosis facts\n  record-plan           Record plan, verification and rollback plan\n  check-data-write      Validate a planned DB write against policy + run scope\n  verify-repo           Verify real git HEAD, remote, diff and scope\n  record-verification   Record a verification matrix\n  verify-evidence       Verify manifest paths, SHA256 and auditability\n  record-evidence       Append audited evidence item(s); supports --evidence-batch-*\n  record-review         Record per-repo review and invalidate ship gate\n  record-ship-package   Record merge/deploy/dev-verify facts\n  record-rollback       Record rollback facts\n  record-decision       Record an automatic decision and alternatives\n  record-failure        Record failure stage/class and patch round\n  record-acceptance     Record policy-only or exact 验收通过 acceptance evidence\n  takeover              Explicitly transfer a crashed/stalled run to a new claim\n  set-data-scope        Apply versioned policy + run table whitelist\n  advance               Advance to the next legal phase\n  resume                Resume BLOCKED to its recorded resume_phase\n  block                 Enter BLOCKED with a resume condition\n  cancel                Enter CANCELLED\n  reopen                Archive current cycle and open REOPENED cycle\n  render-report         Render report.md from state + evidence manifest\n\nRun with --help omitted for command-specific errors; see P0-DESIGN.md for fields.\n`);
    return;
  }
  const evidenceRefs = values['evidence-ref'] ?? [];
  let releaseRunLock = null;
  process.on('exit', () => {
    if (releaseRunLock) releaseRunLock();
  });
  const readInput = () => {
    if (values['input-file']) return readJson(resolve(values['input-file']));
    if (values['input-json']) return JSON.parse(values['input-json']);
    throw new Error('--input-file or --input-json is required');
  };

  if (command === 'init') {
    for (const key of ['auto-number', 'work-item-id', 'title', 'claim-id']) {
      if (!values[key]) throw new Error(`--${key} is required`);
    }
    if ((values.phase ?? 'CLAIMED') !== 'INTAKE') {
      for (const key of ['claim-comment-ref', 'claim-operator']) {
        if (!values[key]) throw new Error(`--${key} is required for CLAIMED init`);
      }
    }
    const runDir = runPath(values);
    if (existsSync(join(runDir, 'state.json'))) throw new Error(`RUN_EXISTS: ${runDir}`);
    releaseRunLock = acquireRunLock(runDir, command, { create: true });
    if (existsSync(join(runDir, 'state.json'))) throw new Error(`RUN_EXISTS: ${runDir}`);
    const policiesRoot = values['policies-root'] ? resolve(values['policies-root']) : POLICY_ROOT;
    const policyVersion = values['policy-version'] ?? 'demo-2026-11-10';
    const loadedPolicy = loadPolicy(policyVersion, policiesRoot);
    const policyErrors = validatePolicy(loadedPolicy.policy);
    if (policyErrors.length) throw new Error(`POLICY_INVALID:\n- ${policyErrors.join('\n- ')}`);
    if (values['policy-hash'] && values['policy-hash'] !== loadedPolicy.policy_hash) {
      throw new Error(`POLICY_HASH_MISMATCH: expected ${loadedPolicy.policy_hash}`);
    }
    const state = createInitialState({
      autoNumber: values['auto-number'],
      workItemId: values['work-item-id'],
      title: values.title,
      claimId: values['claim-id'],
      claimCommentRef: values['claim-comment-ref'],
      claimOperator: values['claim-operator'],
      sessionId: values['session-id'],
      machineId: values['machine-id'],
      projectKey: values['project-key'],
      owner: values.owner,
      phase: values.phase,
      risk: values.risk,
      policyVersion,
      policyHash: loadedPolicy.policy_hash,
      machineLocal: values['machine-local'],
    });
    assertStateShape(state);
    mkdirSync(join(runDir, 'evidence', 'raw'), { recursive: true });
    mkdirSync(join(runDir, 'cycles'), { recursive: true });
    writeJson(join(runDir, 'state.json'), state);
    writeJson(join(runDir, 'evidence', 'manifest.json'), {
      schema_version: 1,
      run_id: state.run_id,
      updated_at: isoNow(),
      items: [],
    });
    writeFileSync(join(runDir, 'report.md'), renderReport(state, { items: [] }), 'utf8');
    process.stdout.write(`${runDir}\n`);
    return;
  }

  const runDir = runPath(values);
  releaseRunLock = acquireRunLock(runDir, command);
  const state = loadRun(runDir);
  assertStateShape(state);
  const context = { sessionId: values['session-id'], machineId: values['machine-id'] };

  if (command === 'approve-gate') {
    if (!values.gate) throw new Error('--gate is required');
    if (values.message == null) throw new Error('--message is required');
    let binding;
    if (values['binding-file']) {
      binding = readJson(resolve(values['binding-file']));
    } else if (values['binding-json']) {
      binding = JSON.parse(values['binding-json']);
    } else {
      throw new Error('--binding-file or --binding-json is required');
    }
    const gate = approveGate(state, {
      gate: values.gate,
      message: values.message,
      binding,
      approvedBy: values['approved-by'],
      messageRef: values['message-ref'],
      activeRuns: Number(values['active-runs'] ?? 1),
      sessionId: values['session-id'],
      machineId: values['machine-id'],
      claimId: state.ownership.claim_id,
      policiesRoot: values['policies-root'] ? resolve(values['policies-root']) : POLICY_ROOT,
    });
    saveRun(runDir, state);
    process.stdout.write(`${JSON.stringify({ gate: values.gate, gate_hash: gate.gate_hash, status: gate.status })}\n`);
    return;
  }

  if (command === 'validate-gate') {
    if (!values.gate) throw new Error('--gate is required');
    const result = validateGate(state, values.gate, {
      ...context,
      policiesRoot: values['policies-root'] ? resolve(values['policies-root']) : POLICY_ROOT,
    });
    mutateGateValidation(state, values.gate, result);
    saveRun(runDir, state);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    if (!result.ok) process.exitCode = 2;
    return;
  }

  if (command === 'validate-state') {
    process.stdout.write(`OK: ${state.run_id} phase=${state.phase} cycle=${state.current_cycle_id}\n`);
    return;
  }

  if (command === 'set-repos') {
    let repos;
    if (values['repos-file']) repos = readJson(resolve(values['repos-file']));
    else if (values['repos-json']) repos = JSON.parse(values['repos-json']);
    else throw new Error('--repos-file or --repos-json is required');
    setRepos(state, repos);
    saveRun(runDir, state);
    process.stdout.write(`${state.repos.length} repos recorded\n`);
    return;
  }

  if (command === 'set-risk') {
    setRisk(state, readInput());
    saveRun(runDir, state);
    process.stdout.write(`risk=${state.risk.level}\n`);
    return;
  }

  if (command === 'record-diagnosis') {
    recordDiagnosis(state, readInput());
    saveRun(runDir, state);
    process.stdout.write('diagnosis recorded\n');
    return;
  }

  if (command === 'record-plan') {
    recordPlan(state, readInput());
    saveRun(runDir, state);
    process.stdout.write('plan recorded\n');
    return;
  }

  if (command === 'check-data-write') {
    if (!values['session-id'] || !values['machine-id']) {
      throw new Error('--session-id and --machine-id are required');
    }
    const authorization = checkDataWrite(state, readInput(), {
      sessionId: values['session-id'],
      machineId: values['machine-id'],
      policiesRoot: values['policies-root'] ? resolve(values['policies-root']) : POLICY_ROOT,
    });
    process.stdout.write(`${JSON.stringify(authorization, null, 2)}\n`);
    return;
  }

  if (command === 'verify-repo') {
    if (!values['repo-id'] || !values['repo-dir']) throw new Error('--repo-id and --repo-dir are required');
    const result = verifyRepo(state, {
      repoId: values['repo-id'],
      repoDir: resolve(values['repo-dir']),
      candidateSha: values['candidate-sha'],
      baseSha: values['base-sha'],
    });
    saveRun(runDir, state);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }

  if (command === 'record-verification') {
    let items;
    if (values['items-file']) items = readJson(resolve(values['items-file']));
    else if (values['items-json']) items = JSON.parse(values['items-json']);
    else throw new Error('--items-file or --items-json is required');
    recordVerification(state, items);
    saveRun(runDir, state);
    process.stdout.write(`${state.verification_matrix.length} verification items recorded\n`);
    return;
  }

  if (command === 'verify-evidence') {
    const manifest = readJson(join(runDir, 'evidence', 'manifest.json'));
    const result = verifyEvidence(state, manifest, runDir);
    saveRun(runDir, state);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    if (result.result !== 'PASS') process.exitCode = 2;
    return;
  }

  if (command === 'record-evidence') {
    const manifest = readJson(join(runDir, 'evidence', 'manifest.json'));
    const evidenceOptions = {
      state,
      policiesRoot: values['policies-root'] ? resolve(values['policies-root']) : POLICY_ROOT,
    };
    let batch;
    if (values['evidence-batch-file']) batch = readJson(resolve(values['evidence-batch-file']));
    else if (values['evidence-batch-json']) batch = JSON.parse(values['evidence-batch-json']);
    if (batch !== undefined) {
      const items = recordEvidenceBatch(runDir, manifest, batch, evidenceOptions);
      process.stdout.write(`${JSON.stringify({ recorded: items.length, evidence_ids: items.map((item) => item.evidence_id) }, null, 2)}\n`);
      return;
    }
    let evidence;
    if (values['evidence-file']) evidence = readJson(resolve(values['evidence-file']));
    else if (values['evidence-json']) evidence = JSON.parse(values['evidence-json']);
    else throw new Error('--evidence-file, --evidence-json, --evidence-batch-file or --evidence-batch-json is required');
    const item = recordEvidence(runDir, manifest, evidence, evidenceOptions);
    process.stdout.write(`${JSON.stringify(item, null, 2)}\n`);
    return;
  }

  if (command === 'record-ship-package') {
    recordShipPackage(state, readInput());
    const manifest = readJson(join(runDir, 'evidence', 'manifest.json'));
    const verification = verifyEvidence(state, manifest, runDir);
    saveRun(runDir, state);
    process.stdout.write(`${JSON.stringify({ ship_package: 'recorded', evidence_result: verification.result })}\n`);
    if (verification.result !== 'PASS') process.exitCode = 2;
    return;
  }

  if (command === 'record-rollback') {
    recordRollback(state, readInput());
    saveRun(runDir, state);
    process.stdout.write('rollback recorded\n');
    return;
  }

  if (command === 'record-decision') {
    recordDecision(state, readInput());
    saveRun(runDir, state);
    process.stdout.write('decision recorded\n');
    return;
  }

  if (command === 'record-failure') {
    recordFailure(state, readInput());
    saveRun(runDir, state);
    process.stdout.write(`failure_class=${state.failure_class} patch_round=${state.patch_round}\n`);
    return;
  }

  if (command === 'record-review') {
    let review;
    if (values['review-file']) review = readJson(resolve(values['review-file']));
    else if (values['review-json']) review = JSON.parse(values['review-json']);
    else throw new Error('--review-file or --review-json is required');
    recordReview(state, review);
    saveRun(runDir, state);
    process.stdout.write(`${state.review.repos.length} reviews recorded\n`);
    return;
  }

  if (command === 'record-acceptance') {
    let acceptance;
    if (values['acceptance-file']) acceptance = readJson(resolve(values['acceptance-file']));
    else if (values['acceptance-json']) acceptance = JSON.parse(values['acceptance-json']);
    else throw new Error('--acceptance-file or --acceptance-json is required');
    recordAcceptance(state, acceptance, { runDir });
    saveRun(runDir, state);
    process.stdout.write(`acceptance=${state.acceptance.status}\n`);
    return;
  }

  if (command === 'takeover') {
    if (!values.message) throw new Error('--message is required');
    if (!values['claim-id']) throw new Error('--claim-id is required');
    if (!values['claim-comment-ref'] || !values['claim-operator']) {
      throw new Error('--claim-comment-ref and --claim-operator are required');
    }
    takeoverState(state, {
      message: values.message,
      claimId: values['claim-id'],
      claimCommentRef: values['claim-comment-ref'],
      claimOperator: values['claim-operator'],
      owner: values.owner,
      reason: values.reason,
      sessionId: values['session-id'],
      machineId: values['machine-id'],
    });
    saveRun(runDir, state);
    process.stdout.write(`takeover claim=${state.ownership.claim_id}\n`);
    return;
  }

  if (command === 'set-data-scope') {
    let scope;
    if (values['scope-file']) {
      scope = readJson(resolve(values['scope-file']));
    } else if (values['scope-json']) {
      scope = JSON.parse(values['scope-json']);
    } else {
      throw new Error('--scope-file or --scope-json is required');
    }
    setDataScope(state, scope, {
      runDir,
      policiesRoot: values['policies-root'] ? resolve(values['policies-root']) : POLICY_ROOT,
    });
    saveRun(runDir, state);
    process.stdout.write(`${state.data_policy.scope_hash}\n`);
    return;
  }

  if (command === 'advance') {
    if (!values.to) throw new Error('--to is required');
    try {
      advance(state, {
        to: values.to,
        sessionId: values['session-id'],
        machineId: values['machine-id'],
        claimCommentRef: values['claim-comment-ref'],
        claimOperator: values['claim-operator'],
        evidenceRefs,
        summary: values.summary,
      });
      saveRun(runDir, state);
      process.stdout.write(`advanced to ${state.phase}\n`);
    } catch (error) {
      saveRun(runDir, state);
      throw error;
    }
    return;
  }

  if (command === 'resume') {
    if (!values.to) throw new Error('--to is required');
    resumeState(state, {
      to: values.to,
      sessionId: values['session-id'],
      machineId: values['machine-id'],
      evidenceRefs,
      summary: values.summary,
      actor: values.actor,
      policiesRoot: values['policies-root'] ? resolve(values['policies-root']) : undefined,
    });
    saveRun(runDir, state);
    process.stdout.write(`resumed to ${state.phase}\n`);
    return;
  }

  if (command === 'block') {
    blockState(state, {
      reason: values.reason,
      resumePhase: values['resume-phase'],
      condition: values.condition,
      owner: values.owner,
      sessionId: values['session-id'],
      evidenceRefs,
    });
    saveRun(runDir, state);
    process.stdout.write(`blocked; resume_phase=${state.resume_phase}\n`);
    return;
  }

  if (command === 'cancel') {
    cancelState(state, {
      reason: values.reason,
      actor: values.actor ?? values.owner,
      cleanup: values.cleanup,
      sessionId: values['session-id'],
      evidenceRefs,
    });
    saveRun(runDir, state);
    process.stdout.write('cancelled\n');
    return;
  }

  if (command === 'reopen') {
    reopenState(state, {
      runDir,
      reason: values.reason,
      claimId: values['claim-id'],
      sessionId: values['session-id'],
      evidenceRefs,
    });
    saveRun(runDir, state);
    process.stdout.write(`reopened as ${state.current_cycle_id}\n`);
    return;
  }

  if (command === 'render-report') {
    const manifest = readJson(join(runDir, 'evidence', 'manifest.json'));
    writeFileSync(join(runDir, 'report.md'), renderReport(state, manifest), 'utf8');
    state.updated_at = isoNow();
    saveRun(runDir, state);
    process.stdout.write(`${join(runDir, 'report.md')}\n`);
    return;
  }

  throw new Error(`UNKNOWN_COMMAND: ${command}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    main();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
