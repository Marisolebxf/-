import { readFileSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const modPath = resolve('.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs');
const mod = await import(pathToFileURL(modPath).href);
const state = JSON.parse(readFileSync('agent-delivery/bugfix-runs/2581-7168058150/state.json', 'utf8'));
const binding = {
  repos: state.repos.map((r) => ({
    repo_id: r.repo_id,
    repo_name: r.repo_name,
    base_sha: r.base_sha,
    planned_change_scope: r.planned_change_scope,
    role: r.role,
    depends_on: r.depends_on,
    ship_order: r.ship_order,
    candidate_sha: null,
  })),
  diagnosis_hash: mod.diagnosisHash(state),
  plan_hash: mod.sha256(state.plan ?? null),
  risk_level: state.risk.level,
  data_policy_version: state.data_policy.policy_version,
  data_policy_hash: state.data_policy.policy_hash,
  data_scope_hash: state.data_policy.scope_hash,
};
writeFileSync('agent-delivery/bugfix-runs/2581-7168058150/_in-binding-enterdev.json', JSON.stringify(binding, null, 2));
console.log('binding written');
