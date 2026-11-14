import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const run = 'd:/web/gkx-lumen/gkx-orchestration/agent-delivery/bugfix-runs/7168001613-7168001613';
const state = JSON.parse(readFileSync(join(run, 'state.json'), 'utf8'));

const stableProjection = (value) => {
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
};
const sha256 = (value) => {
  const payload = typeof value === 'string' ? value : JSON.stringify(stableProjection(value));
  return 'sha256:' + createHash('sha256').update(payload, 'utf8').digest('hex');
};

const binding = JSON.parse(readFileSync(join(run, 'gate-enter-dev.json'), 'utf8'));
binding.repos = state.repos.map((r) => ({
  repo_id: r.repo_id,
  repo_name: r.repo_name,
  base_branch: r.base_branch,
  base_sha: r.base_sha,
  planned_change_scope: r.planned_change_scope,
  candidate_sha: null,
  role: r.role,
  depends_on: r.depends_on,
  ship_order: r.ship_order,
}));
binding.diagnosis_hash = sha256({ diagnosis: state.diagnosis, plan: state.plan });
binding.plan_hash = sha256(state.plan);
binding.risk_level = state.risk.level;
binding.data_policy_version = state.data_policy.policy_version;
binding.data_policy_hash = state.data_policy.policy_hash;
binding.data_scope_hash = state.data_policy.scope_hash;

writeFileSync(join(run, 'gate-enter-dev.json'), JSON.stringify(binding, null, 2) + '\n', 'utf8');
console.log('binding synced with state.repos');
