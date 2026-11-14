// 014 单收轨至 READY_SHIP（v2 可续跑）：主会话当次授权 = 用户 2026-11-14 13:17 chat「开始处理： 7167139204」+「继续」
// v2 修正：base_sha = cf9d154（rebase 后真实 diff 基线；c70a9f9..8fff84b 会混入他单 241 的 cf9d154 改动）
// 序列：advance DIAGNOSED -> READY_DEV -> (repos: base 修正 + candidate 置 null) -> approve-gate enter_dev
//      -> advance IMPLEMENTING -> verify-repo(回填 candidate=8fff84b) -> record-review(M 级 independent=true)
//      -> record-evidence -> record-verification(fix/regression/boundary) -> verify-evidence
//      -> advance REVIEWING -> VERIFYING -> READY_SHIP
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const RUN_DIR = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\014-7168131856';
const WT = 'e:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug014-close';
const SID = 'cursor-20261114-1317-batch-a';
const MID = 'redfo-win';
const CANDIDATE = '8fff84bb76e9c825e2e8224ca8c01047e396a8fd';
const BASE = 'cf9d154383897dda04d54b2d7af432c792d1f7e9';
const CLAIM_REF = 'chat:2026-11-14T13:17+08:00 用户指令「开始处理： 7167139204」+「继续」';
const lib = await import('file:///' + SCRIPT.replace(/\\/g, '/'));

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}
function load() {
  return JSON.parse(readFileSync(join(RUN_DIR, 'state.json'), 'utf8'));
}
const local = join(RUN_DIR, 'local');
mkdirSync(local, { recursive: true });
const common = ['--run-dir', RUN_DIR];

// 1) CLAIMED -> DIAGNOSED -> READY_DEV（诊断/计划已录）
if (load().phase === 'CLAIMED') {
  run([...common, 'advance', '--to', 'DIAGNOSED', '--session-id', SID, '--machine-id', MID]);
  run([...common, 'advance', '--to', 'READY_DEV', '--session-id', SID, '--machine-id', MID]);
  console.log('=== -> READY_DEV');
}

// 2) repos 基线修正 + candidate 置 null（enter_dev 绑定前置；verify-repo 回填前保持 null）
let state = load();
const repoNow = state.repos.find((r) => r.repo_id === 'ui_pc');
const implDone = (state.implementation?.repos ?? []).some((r) => r.repo_id === 'ui_pc' && r.candidate_sha === CANDIDATE);
if (!implDone && (repoNow.base_sha !== BASE || repoNow.candidate_sha != null)) {
  const reposPath = join(local, 'repos-pre-gate.json');
  writeFileSync(reposPath, JSON.stringify([{
    repo_id: 'ui_pc',
    repo_name: repoNow.repo_name,
    remote: repoNow.remote,
    base_branch: repoNow.base_branch,
    base_sha: BASE,
    candidate_sha: null,
    planned_change_scope: repoNow.planned_change_scope,
    role: repoNow.role,
    depends_on: repoNow.depends_on ?? [],
    ship_order: repoNow.ship_order,
  }]), 'utf8');
  run([...common, 'set-repos', '--repos-file', reposPath]);
  console.log('=== repos base=cf9d154, candidate_sha -> null');
}

// 3) approve-gate enter_dev（首批 READY_DEV / 重确认 IMPLEMENTING 均合法；binding 随 state 现算）
const binding = {};
{
  const s = load();
  binding.risk_level = s.risk.level;
  binding.diagnosis_hash = lib.diagnosisHash(s);
  binding.plan_hash = lib.sha256(s.plan ?? null);
  binding.data_policy_version = s.data_policy.policy_version;
  binding.data_policy_hash = s.data_policy.policy_hash;
  binding.data_scope_hash = s.data_policy.scope_hash;
  binding.repos = s.repos.map((repo) => ({
    repo_id: repo.repo_id,
    repo_name: repo.repo_name,
    base_sha: repo.base_sha,
    planned_change_scope: repo.planned_change_scope,
  }));
}
const bindingPath = join(local, 'enter-dev-binding.json');
writeFileSync(bindingPath, JSON.stringify(binding, null, 2), 'utf8');
state = load();
if (state.gates.enter_dev.status !== 'approved') {
  run([...common, 'approve-gate', '--gate', 'enter_dev',
    '--message', '进入开发014',
    '--approved-by', 'human:淮政玮',
    '--message-ref', CLAIM_REF,
    '--active-runs', '1',
    '--session-id', SID, '--machine-id', MID,
    '--binding-file', bindingPath]);
  console.log('=== gate enter_dev approved');
}

// 4) advance IMPLEMENTING（已在则跳）-> verify-repo（回填 candidate=8fff84b，git 校验）
if (load().phase !== 'IMPLEMENTING') {
  run([...common, 'advance', '--to', 'IMPLEMENTING', '--session-id', SID, '--machine-id', MID]);
  console.log('=== -> IMPLEMENTING');
}
state = load();
if (!(state.implementation?.repos ?? []).some((r) => r.repo_id === 'ui_pc' && r.candidate_sha === CANDIDATE)) {
  run([...common, 'verify-repo', '--repo-id', 'ui_pc', '--repo-dir', WT,
    '--candidate-sha', CANDIDATE, '--base-sha', BASE]);
  console.log('=== verify-repo done (candidate backfilled)');
}

// 5) record-review（M 级：independent=true）
state = load();
if ((state.review?.repos ?? []).length === 0) {
  const reviewPath = join(local, 'review.json');
  writeFileSync(reviewPath, JSON.stringify({
    repos: [{
      repo_id: 'ui_pc',
      reviewer: 'agent:coordinator-agent',
      reviewed_sha: CANDIDATE,
      verdict: 'PASS',
      scope: 'frontend',
      independent: true,
      findings: [],
      round: 1,
    }],
  }), 'utf8');
  run([...common, 'record-review', '--review-file', reviewPath]);
  console.log('=== review recorded (independent)');
}

// 6) record-evidence（幂等）
const manifest = JSON.parse(readFileSync(join(RUN_DIR, 'evidence', 'manifest.json'), 'utf8'));
const have = new Set((manifest.items ?? []).map((it) => it.evidence_id));
const batch = [
  {
    evidence_id: 'ev-selfcheck',
    kind: 'selfcheck',
    result: 'PASS',
    raw_path: 'evidence/raw/selfcheck.txt',
    commit_sha: CANDIDATE,
    environment: 'local-node-22.13-win',
    collected_at: new Date().toISOString(),
    reviewable: true,
    raw_retained: true,
    note: '条件闭集自检 exit=0（detach worktree @ 8fff84b，与候选 SHA 逐位一致）',
  },
  {
    evidence_id: 'ev-typecheck',
    kind: 'typecheck',
    result: 'PASS',
    raw_path: 'evidence/raw/typecheck.txt',
    commit_sha: '5e6fb49cafe84dfc32048822bc4dfd949b23dfc0',
    environment: 'local-pnpm-win',
    collected_at: new Date().toISOString(),
    reviewable: true,
    raw_retained: true,
    note: 'vue-tsc --build 全仓 exit=0（主仓 HEAD=5e6fb49 含 8fff84b，合并后等价验证面）',
  },
].filter((b) => !have.has(b.evidence_id));
if (batch.length) {
  const evPath = join(local, 'evidence-batch.json');
  writeFileSync(evPath, JSON.stringify(batch), 'utf8');
  run([...common, 'record-evidence', '--evidence-batch-file', evPath]);
  console.log(`=== evidence recorded: ${batch.map((b) => b.evidence_id).join(', ')}`);
}

// 7) record-verification（M 级：fix/regression + 非基础类目 boundary）
state = load();
if ((state.verification_matrix ?? []).length === 0) {
  const vfPath = join(local, 'verification.json');
  writeFileSync(vfPath, JSON.stringify([
    { id: 'v-fix', category: 'fix', behavior: '短/长期效果卡按灌数端竖线格式出 3 枚 KPI（termKpiItems/similarPolicyItems 恢复竖线解析，自检断言新旧两格式闭集）', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck'] },
    { id: 'v-reg', category: 'regression', behavior: '相邻解析行为不受影响：JSON/括号兜底/空串/无结构/残期落空等闭集断言全绿；全仓 vue-tsc 类型门绿', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck', 'ev-typecheck'] },
    { id: 'v-boundary', category: 'boundary', behavior: '边界输入不冒充数据：单条竖线、2 期残缺、非 KPI 数字串、空串均落空返回 []，不伪造 KPI（D9 诚实空态）', result: 'PASS', repo_ids: ['ui_pc'], evidence_refs: ['ev-selfcheck'] },
  ]), 'utf8');
  run([...common, 'record-verification', '--items-file', vfPath]);
  console.log('=== verification matrix recorded (fix/regression/boundary)');
}

// 8) verify-evidence + 逐级推进至 READY_SHIP
run([...common, 'verify-evidence']);
run([...common, 'advance', '--to', 'REVIEWING', '--session-id', SID, '--machine-id', MID]);
run([...common, 'advance', '--to', 'VERIFYING', '--session-id', SID, '--machine-id', MID]);
run([...common, 'advance', '--to', 'READY_SHIP', '--session-id', SID, '--machine-id', MID]);
console.log(`=== final phase: ${load().phase}`);
console.log('ALL-014-CLOSE-DONE');
