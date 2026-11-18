// 计算 enter_dev 绑定所需的哈希（与 bugflow-state.mjs sha256/stableProjection 同源）
import { createHash } from 'node:crypto'
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const runDir = resolve(process.argv[2])
const state = JSON.parse(readFileSync(resolve(runDir, 'state.json'), 'utf8'))

function stableProjection(value) {
  if (Array.isArray(value)) return value.map(stableProjection)
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .filter((key) => value[key] !== undefined)
        .map((key) => [key, stableProjection(value[key])]),
    )
  }
  return value
}

const sha256 = (value) => {
  const payload = typeof value === 'string' ? value : JSON.stringify(stableProjection(value))
  return 'sha256:' + createHash('sha256').update(payload, 'utf8').digest('hex')
}

const binding = {
  repos: [
    {
      repo_id: 'ui_pc',
      repo_name: 'lumen-ui-science-pc',
      base_sha: state.repos[0].base_sha,
      planned_change_scope: state.repos[0].planned_change_scope,
    },
  ],
  diagnosis_hash: sha256({ diagnosis: state.diagnosis ?? null, plan: state.plan ?? null }),
  plan_hash: sha256(state.plan ?? null),
  risk_level: state.risk.level,
  data_policy_version: state.data_policy.policy_version,
  data_policy_hash: state.data_policy.policy_hash,
  data_scope_hash: state.data_policy.scope_hash,
}

const out = resolve(runDir, 'binding-enter-dev.json')
writeFileSync(out, JSON.stringify(binding, null, 2) + '\n')
console.log('binding written:', out)
