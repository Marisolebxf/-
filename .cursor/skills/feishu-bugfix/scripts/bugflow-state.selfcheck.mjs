/**
 * Offline self-check for .cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs.
 * Run: node .cursor/skills/feishu-bugfix/scripts/bugflow-state.selfcheck.mjs
 */
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import {
  advance,
  approveGate,
  blockState,
  checkDataWrite,
  createInitialState,
  diagnosisHash,
  loadAndValidatePolicy,
  recordAcceptance,
  recordDiagnosis,
  recordDecision,
  recordEvidence,
  recordFailure,
  recordPlan,
  recordReview,
  recordShipPackage,
  recordVerification,
  renderReport,
  reopenState,
  setDataScope,
  setRepos,
  setRisk,
  sha256,
  takeoverState,
  validateGate,
  validateStateShape,
  verificationHash,
  verifyEvidence,
  verifyRepo,
} from './bugflow-state.mjs';
import { loadPolicy, validatePolicy } from './lib/policy-file.mjs';

const policiesRoot = '.cursor/skills/feishu-bugfix/policies';
const loadedPolicy = loadPolicy('demo-2026-11-10', policiesRoot);

function runGit(cwd, args) {
  return execFileSync('git', ['-C', cwd, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function makeState(overrides = {}) {
  const { phase = 'CLAIMED', ...stateOverrides } = overrides;
  const state = createInitialState({
    autoNumber: '123',
    workItemId: '456',
    title: 'selfcheck bug',
    claimId: 'claim-selfcheck',
    claimCommentRef: 'comment-claim-selfcheck',
    claimOperator: 'human:selfcheck',
    sessionId: 'session-1',
    machineId: 'machine-1',
    phase: 'CLAIMED',
    risk: 'S',
    policyVersion: 'demo-2026-11-10',
    policyHash: loadedPolicy.policy_hash,
    ...stateOverrides,
  });
  state.phase = phase;
  return state;
}

const tmp = mkdtempSync(join(tmpdir(), 'bugflow-selfcheck-'));
const repoDir = join(tmp, 'repo');
const runDir = join(tmp, '123-456');
mkdirSync(repoDir, { recursive: true });
mkdirSync(join(runDir, 'evidence', 'raw'), { recursive: true });
runGit(repoDir, ['init', '-b', 'dev']);
runGit(repoDir, ['config', 'user.email', 'selfcheck@example.invalid']);
runGit(repoDir, ['config', 'user.name', 'selfcheck']);
mkdirSync(join(repoDir, 'src', 'page'), { recursive: true });
writeFileSync(join(repoDir, 'src', 'page', 'index.txt'), 'base\n');
runGit(repoDir, ['add', '.']);
runGit(repoDir, ['commit', '-m', 'base']);
const baseSha = runGit(repoDir, ['rev-parse', 'HEAD']);
writeFileSync(join(repoDir, 'src', 'page', 'index.txt'), 'fixed\n');
runGit(repoDir, ['add', '.']);
runGit(repoDir, ['commit', '-m', 'fix']);
const candidateSha = runGit(repoDir, ['rev-parse', 'HEAD']);
const remote = 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git';
runGit(repoDir, ['remote', 'add', 'origin', 'https://fake-user:fake-password@aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git']);

try {
  assert.throws(() => createInitialState({
    autoNumber: '123', workItemId: '456', title: 'invalid init', claimId: 'claim', phase: 'READY_DEV',
  }), /INIT_PHASE_INVALID/);
  assert.throws(() => createInitialState({
    autoNumber: '../123', workItemId: '456', title: 'path escape', claimId: 'claim',
  }), /auto_number must contain digits only/);
  assert.throws(() => createInitialState({
    autoNumber: '123', workItemId: '456', title: 'missing claim evidence', claimId: 'claim', phase: 'CLAIMED',
  }), /INIT_CLAIM_EVIDENCE_REQUIRED/);
  const downgradeState = makeState({ risk: 'M' });
  assert.throws(() => setRisk(downgradeState, { level: 'S' }), /RISK_DOWNGRADE_FORBIDDEN/);

  const missingFactsState = makeState({ phase: 'READY_DEV' });
  assert.throws(() => approveGate(missingFactsState, {
    gate: 'enter_dev',
    message: '进入开发123',
    binding: {},
    sessionId: 'session-1',
    machineId: 'machine-1',
  }), /diagnosis\.symptom is required/);

  const state = makeState({ phase: 'READY_DEV' });
  setRepos(state, [{
    repo_id: 'ui_pc',
    repo_name: 'lumen-ui-science-pc',
    remote,
    base_branch: 'dev',
    base_sha: baseSha,
    candidate_sha: null,
    planned_change_scope: ['src/page'],
    worktree: '/must/not/persist',
  }]);
  assert.equal(state.repos[0].worktree, undefined);
  assert.deepEqual(validateStateShape(state), []);
  assert.throws(() => setRepos(structuredClone(state), [{
    repo_id: 'not_registered',
    repo_name: 'not_registered',
    remote: 'https://example.invalid/not_registered.git',
    base_branch: 'dev',
    base_sha: baseSha,
    candidate_sha: null,
    planned_change_scope: ['src'],
  }]), /not registered/);

  recordDiagnosis(state, {
    symptom: 'query is empty',
    reproduction: ['open page', 'click query'],
    root_cause: 'missing filter branch',
    counter_evidence: ['API succeeds'],
    requirement_refs: ['REQ-1'],
    impact_scope: ['query page'],
  });
  recordPlan(state, {
    change_scope: ['ui_pc/src/page'],
    non_goals: ['redesign'],
    verification_plan: ['unit', 'browser'],
    rollback_plan: ['revert candidate commit'],
    data_access: true,
  });

  const manifestPath = join(runDir, 'evidence', 'manifest.json');
  const manifest = { schema_version: 1, run_id: state.run_id, updated_at: new Date().toISOString(), items: [] };
  writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
  writeFileSync(join(runDir, 'evidence', 'raw', 'scope.txt'), 'human approved demo table\n');
  recordEvidence(runDir, manifest, {
    evidence_id: 'E-DATA-001',
    kind: 'human_confirmation',
    result: 'PASS',
    raw_path: 'evidence/raw/scope.txt',
    reviewable: true,
    raw_retained: true,
    command: null,
    exit_code: null,
    commit_sha: candidateSha,
    environment: 'demo',
    collected_at: '2026-11-10T18:00:00+08:00',
    summary: 'demo table approved',
  });
  setDataScope(state, {
    status: 'approved',
    tables: [{
      database: 'demo_gkxlumenx_dwd',
      schema: 'demo_gkxlumenx_dwd',
      table: 'sample_table',
      confirmed_by: 'human:owner',
      confirmed_at: '2026-11-10T18:00:00+08:00',
      evidence_ref: 'evidence/manifest.json#E-DATA-001',
    }],
  }, { runDir, policiesRoot });

  const dbWriteInput = {
    environment: 'demo',
    database: 'demo_gkxlumenx_dwd',
    schema: 'demo_gkxlumenx_dwd',
    table: 'sample_table',
    operation: 'insert',
    access_mode: 'python',
    host_ref: 'env:DEMO_MYSQL_HOST',
    account_ref: 'env:DEMO_MYSQL_USER',
  };
  assert.throws(() => checkDataWrite(state, dbWriteInput), /enter_dev gate is not valid/);

  const enterBinding = {
    repos: [{
      repo_id: 'ui_pc',
      repo_name: 'lumen-ui-science-pc',
      base_sha: baseSha,
      candidate_sha: null,
      planned_change_scope: ['src/page'],
    }],
    diagnosis_hash: diagnosisHash(state),
    plan_hash: sha256(state.plan),
    risk_level: 'S',
    data_policy_version: state.data_policy.policy_version,
    data_policy_hash: state.data_policy.policy_hash,
    data_scope_hash: state.data_policy.scope_hash,
  };

  assert.throws(
    () => approveGate(structuredClone(state), { gate: 'enter_dev', message: '进入开发', binding: enterBinding }),
    /GATE_CONTEXT_REQUIRED/,
  );
  assert.throws(
    () => approveGate(structuredClone(state), {
      gate: 'enter_dev', message: '继续开发', binding: enterBinding, sessionId: 'session-1', machineId: 'machine-1',
    }),
    /GATE_TOKEN_INVALID/,
  );
  assert.throws(
    () => approveGate(structuredClone(state), {
      gate: 'enter_dev', message: '【进入开发】123', binding: enterBinding, sessionId: 'session-1', machineId: 'machine-1',
    }),
    /GATE_TOKEN_INVALID/,
  );
  assert.throws(
    () => approveGate(structuredClone(state), {
      gate: 'enter_dev', message: '进入开发', binding: enterBinding, sessionId: 'session-1', machineId: 'machine-1', activeRuns: 2,
    }),
    /GATE_TOKEN_INVALID/,
  );

  approveGate(state, {
    gate: 'enter_dev',
    message: '进入开发123',
    binding: enterBinding,
    sessionId: 'session-1',
    machineId: 'machine-1',
  });
  const dbAuthorization = checkDataWrite(state, dbWriteInput, { sessionId: 'session-1', machineId: 'machine-1' });
  assert.throws(
    () => checkDataWrite(structuredClone(state), dbWriteInput, { sessionId: 'session-2', machineId: 'machine-1' }),
    /session changed/,
  );
  writeFileSync(join(runDir, 'evidence', 'raw', 'db.txt'), 'insert controlled mock rows\n');
  recordEvidence(runDir, manifest, {
    evidence_id: 'E-DB-001',
    kind: 'db',
    result: 'PASS',
    raw_path: 'evidence/raw/db.txt',
    reviewable: true,
    raw_retained: true,
    commit_sha: candidateSha,
    environment: 'demo',
    collected_at: '2026-11-10T18:01:00+08:00',
    summary: 'insert mock rows into sample_table',
    ...dbAuthorization,
  }, { state });
  assert.match(manifest.items.at(-1).write_authorization_id, /^sha256:/);
  assert.equal(verifyEvidence(state, manifest, runDir).result, 'PASS');
  const pendingScopeState = structuredClone(state);
  pendingScopeState.data_policy.scope = { status: 'pending', tables: [] };
  assert.throws(() => checkDataWrite(pendingScopeState, dbWriteInput, { sessionId: 'session-1', machineId: 'machine-1' }), /DATA_WRITE_DENIED/);
  const wrongTableState = structuredClone(state);
  wrongTableState.data_policy.scope.tables[0].table = 'other_table';
  assert.throws(() => checkDataWrite(wrongTableState, dbWriteInput, { sessionId: 'session-1', machineId: 'machine-1' }), /must match exactly one approved run-scope entry/);
  assert.equal(validateGate(state, 'enter_dev', { sessionId: 'session-1', machineId: 'machine-1' }).ok, true);
  assert.equal(validateGate(state, 'enter_dev', { sessionId: 'session-2', machineId: 'machine-1' }).ok, false);
  assert.equal(validateGate(state, 'enter_dev', {}).ok, false);

  const takeover = structuredClone(state);
  assert.throws(() => takeoverState(takeover, {
    message: '接管', claimId: 'claim-new', sessionId: 'session-new', machineId: 'machine-new', reason: 'old session crashed',
  }), /TAKEOVER_TOKEN_INVALID/);
  takeoverState(takeover, {
    message: '接管【123】',
    claimId: 'claim-new',
    claimCommentRef: 'comment-takeover-new',
    claimOperator: 'human:new-owner',
    sessionId: 'session-new',
    machineId: 'machine-new',
    reason: 'old session crashed',
  });
  assert.equal(takeover.ownership.claim_id, 'claim-new');
  assert.equal(takeover.ownership.claim_comment_ref, 'comment-takeover-new');
  assert.equal(takeover.ownership.takeover_history.length, 1);
  assert.equal(takeover.gates.enter_dev.status, 'needs_reconfirm');

  advance(state, { to: 'IMPLEMENTING', sessionId: 'session-1', machineId: 'machine-1' });
  assert.equal(state.phase, 'IMPLEMENTING');
  assert.throws(() => approveGate(structuredClone(state), {
    gate: 'enter_dev',
    message: '进入开发123',
    binding: enterBinding,
    sessionId: 'session-1',
    machineId: 'machine-1',
  }), /GATE_PHASE_INVALID/);
  const reconfirmState = structuredClone(state);
  setRisk(reconfirmState, { level: 'M', reasons: ['cross-component risk discovered'] });
  assert.equal(reconfirmState.gates.enter_dev.status, 'needs_reconfirm');
  approveGate(reconfirmState, {
    gate: 'enter_dev',
    message: '进入开发123',
    binding: { ...enterBinding, risk_level: 'M' },
    sessionId: 'session-1',
    machineId: 'machine-1',
  });
  assert.equal(reconfirmState.gates.enter_dev.status, 'approved');
  const longTaskRouteState = structuredClone(state);
  setRisk(longTaskRouteState, { level: 'L', reasons: ['cross-repository contract change'] });
  assert.equal(longTaskRouteState.gates.enter_dev.status, 'invalidated');
  assert.match(longTaskRouteState.next_action.action, /L 级/);
  assert.match(state.next_action.action, /verify-repo/);
  assert.throws(
    () => advance(structuredClone(state), { to: 'REVIEWING', sessionId: 'session-1', machineId: 'machine-1' }),
    /PHASE_REQUIREMENTS/,
  );

  const repoVerification = verifyRepo(state, { repoId: 'ui_pc', repoDir, candidateSha });
  assert.equal(repoVerification.git_verified, true);
  assert.equal(repoVerification.remote, remote.replace(/\.git$/, ''));
  assert.match(repoVerification.diff_hash, /^sha256:/);
  assert.match(checkDataWrite(state, dbWriteInput, { sessionId: 'session-1', machineId: 'machine-1' }).write_authorization_id, /^sha256:/);
  advance(state, { to: 'REVIEWING', sessionId: 'session-1', machineId: 'machine-1' });
  const riskEvidenceState = structuredClone(state);
  setRisk(riskEvidenceState, { level: 'M', reasons: ['cross-component risk discovered'] });
  assert.equal(riskEvidenceState.gates.enter_dev.status, 'needs_reconfirm');
  assert.equal(verifyEvidence(riskEvidenceState, manifest, runDir).result, 'PASS');

  recordReview(state, {
    repos: [{
      repo_id: 'ui_pc',
      reviewer: 'agent:reviewer',
      independent: true,
      reviewed_sha: candidateSha,
      verdict: 'PASS',
      scope: 'src/page',
      findings: [],
      round: 1,
      review_hash: 'caller-supplied-must-be-ignored',
    }],
  });
  assert.notEqual(state.review.repos[0].review_hash, 'caller-supplied-must-be-ignored');
  advance(state, { to: 'VERIFYING', sessionId: 'session-1', machineId: 'machine-1' });

  writeFileSync(join(runDir, 'evidence', 'raw', 'verify.txt'), 'unit and browser PASS\n');
  const manifest2 = JSON.parse(readFileSync(manifestPath, 'utf8'));
  recordEvidence(runDir, manifest2, {
    evidence_id: 'E-VERIFY-001',
    kind: 'verification',
    result: 'PASS',
    raw_path: 'evidence/raw/verify.txt',
    reviewable: true,
    raw_retained: true,
    command: 'npm test',
    exit_code: 0,
    commit_sha: candidateSha,
    environment: 'local',
    collected_at: '2026-11-10T18:05:00+08:00',
    summary: 'unit and browser passed',
  });
  const onlyFixState = structuredClone(state);
  assert.throws(() => recordVerification(structuredClone(state), [{
    id: 'V-NO-CATEGORY',
    behavior: 'uncategorized',
    result: 'PASS',
    repo_ids: ['ui_pc'],
    evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
  }]), /category is required/);
  recordVerification(onlyFixState, [{
    id: 'V-FIX-ONLY',
    category: 'fix',
    behavior: 'query returns data',
    result: 'PASS',
    repo_ids: ['ui_pc'],
    evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
  }]);
  assert.throws(
    () => advance(onlyFixState, { to: 'READY_SHIP', sessionId: 'session-1', machineId: 'machine-1' }),
    /regression verification is required/,
  );
  recordVerification(state, [
    {
      id: 'V-FIX-001',
      category: 'fix',
      behavior: 'query returns data',
      result: 'PASS',
      repo_ids: ['ui_pc'],
      evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
    },
    {
      id: 'V-REG-001',
      category: 'regression',
      behavior: 'adjacent tab still returns data',
      result: 'PASS',
      repo_ids: ['ui_pc'],
      evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
    },
  ]);
  const mWithoutAdditionalState = structuredClone(state);
  setRisk(mWithoutAdditionalState, { level: 'M', reasons: ['cross-component risk'] });
  assert.throws(
    () => advance(mWithoutAdditionalState, { to: 'READY_SHIP', sessionId: 'session-1', machineId: 'machine-1' }),
    /M\/L requires at least one non-happy-path verification category/,
  );
  const manifest3 = JSON.parse(readFileSync(manifestPath, 'utf8'));
  const evidenceVerification = verifyEvidence(state, manifest3, runDir);
  assert.equal(evidenceVerification.result, 'PASS');
  const preShipState = structuredClone(state);
  advance(state, { to: 'READY_SHIP', sessionId: 'session-1', machineId: 'machine-1' });

  const shipBinding = {
    repos: [{
      repo_id: 'ui_pc',
      candidate_sha: candidateSha,
      diff_hash: state.implementation.repos[0].diff_hash,
      verification_hash: verificationHash(state, 'ui_pc'),
      review_hash: state.review.repos[0].review_hash,
      data_policy_hash: state.data_policy.policy_hash,
      data_scope_hash: state.data_policy.scope_hash,
    }],
    risk_level: 'S',
    deploy_target: 'dev',
  };
  const unratifiedState = structuredClone(state);
  assert.throws(() => recordDecision(structuredClone(state), {
    decision: 'self-ratified change',
    basis: 'agent belief',
    impact: 'shared behavior',
    requires_human_ratification: true,
    ratified_by: 'agent:selfcheck',
  }), /ratified_by must start with human:/);
  recordDecision(unratifiedState, {
    decision: 'continue with a temporary compatibility branch',
    basis: 'temporary workaround',
    impact: 'changes shared behavior',
    alternatives: ['stop and wait'],
    requires_human_ratification: true,
  });
  assert.throws(() => approveGate(unratifiedState, {
    gate: 'ship',
    message: '提测',
    binding: shipBinding,
    sessionId: 'session-1',
    machineId: 'machine-1',
  }), /DECISION_RATIFICATION_REQUIRED/);
  approveGate(state, {
    gate: 'ship',
    message: '提测',
    binding: shipBinding,
    sessionId: 'session-1',
    machineId: 'machine-1',
  });
  const tamperedShip = structuredClone(state);
  tamperedShip.repos[0].candidate_sha = 'different-candidate';
  assert.equal(validateGate(tamperedShip, 'ship', { sessionId: 'session-1', machineId: 'machine-1' }).ok, false);

  advance(state, { to: 'SHIPPING', sessionId: 'session-1', machineId: 'machine-1' });
  const shipReworkState = structuredClone(state);
  shipReworkState.gates.ship.status = 'invalidated';
  approveGate(shipReworkState, {
    gate: 'ship',
    message: '提测',
    binding: shipBinding,
    sessionId: 'session-1',
    machineId: 'machine-1',
  });
  assert.equal(shipReworkState.gates.ship.status, 'approved');
  assert.throws(() => recordShipPackage(structuredClone(state), {
    repos: [{
      repo_id: 'ui_pc',
      candidate_sha: candidateSha,
      merge_request_id: '!10',
      pipeline_id: '4538',
      pipeline_status: 'success',
      pipeline_url: 'https://aminer-edu-gitlab.jyzhang.cn/pipelines/4538',
      deployed_sha: 'squash-deployed-sha-4538',
      rollout_status: 'success',
      image_tag: 'dev-4538',
    }],
    acceptance_steps: ['打开查询页'],
  }), /merge_commit_sha is required/);

  recordShipPackage(state, {
    repos: [{
      repo_id: 'ui_pc',
      candidate_sha: candidateSha,
      merge_request_id: '!10',
      merge_commit_sha: 'merge-commit-4538',
      pipeline_id: '4538',
      pipeline_status: 'success',
      pipeline_url: 'https://aminer-edu-gitlab.jyzhang.cn/pipelines/4538',
      deployed_sha: 'squash-deployed-sha-4538',
      rollout_status: 'success',
      image_tag: 'dev-4538',
    }],
    acceptance_steps: ['打开查询页', '输入筛选条件', '确认返回数据'],
    dev_verification: { result: 'PASS', evidence_refs: ['evidence/manifest.json#E-VERIFY-001'] },
  });
  const postShipEvidence = verifyEvidence(state, JSON.parse(readFileSync(manifestPath, 'utf8')), runDir);
  assert.equal(postShipEvidence.result, 'PASS');
  assert.equal(state.gates.ship.status, 'approved');
  advance(state, { to: 'DEV_VERIFYING', sessionId: 'session-1', machineId: 'machine-1' });
  advance(state, { to: 'AWAITING_ACCEPTANCE', sessionId: 'session-1', machineId: 'machine-1' });
  assert.throws(
    () => advance(state, { to: 'RESOLVED', sessionId: 'session-1', machineId: 'machine-1' }),
    /ACCEPTANCE_NOT_VERIFIED/,
  );
  writeFileSync(join(runDir, 'evidence', 'raw', 'acceptance.txt'), 'Feishu status RESOLVED with human comment\n');
  const manifest4 = JSON.parse(readFileSync(manifestPath, 'utf8'));
  recordEvidence(runDir, manifest4, {
    evidence_id: 'E-ACCEPT-001',
    kind: 'acceptance',
    result: 'PASS',
    raw_path: 'evidence/raw/acceptance.txt',
    reviewable: true,
    raw_retained: true,
    command: null,
    exit_code: null,
    commit_sha: candidateSha,
    environment: 'feishu',
    collected_at: '2026-11-10T18:30:00+08:00',
    summary: 'human moved status to RESOLVED',
  });
  verifyEvidence(state, JSON.parse(readFileSync(manifestPath, 'utf8')), runDir);

  const chatAcceptanceState = structuredClone(state);
  const acceptanceBinding = {
    work_item_id: chatAcceptanceState.work_item.work_item_id,
    claim_id: chatAcceptanceState.ownership.claim_id,
    ship_gate_hash: chatAcceptanceState.gates.ship.gate_hash,
    dev_verification_result: chatAcceptanceState.ship_package.dev_verification.result,
    evidence_manifest_hash: chatAcceptanceState.evidence.verification.manifest_hash,
    current_status: 'IN PROGRESS',
  };
  assert.throws(() => approveGate(structuredClone(chatAcceptanceState), {
    gate: 'acceptance', message: '可以了', binding: acceptanceBinding, sessionId: 'session-1', machineId: 'machine-1',
  }), /GATE_TOKEN_INVALID/);
  assert.throws(() => recordAcceptance(structuredClone(chatAcceptanceState), {
    status: 'approved', mode: 'chat_exact', operator_verified: false, current_status: 'RESOLVED',
    observed_at: '2026-11-10T18:30:00+08:00', evidence_kind: 'chat_exact',
    evidence_ref: 'evidence/manifest.json#E-ACCEPT-001', approval_ref: 'chat:acceptance-2020',
  }, { runDir }), /requires an approved acceptance gate/);
  approveGate(chatAcceptanceState, {
    gate: 'acceptance', message: '验收通过', binding: acceptanceBinding, sessionId: 'session-1', machineId: 'machine-1', messageRef: 'chat:acceptance-2020',
  });
  recordAcceptance(chatAcceptanceState, {
    status: 'approved', mode: 'chat_exact', operator_verified: false, current_status: 'RESOLVED',
    observed_at: '2026-11-10T18:30:00+08:00', evidence_kind: 'chat_exact',
    evidence_ref: 'evidence/manifest.json#E-ACCEPT-001', approval_ref: 'chat:acceptance-2020',
  }, { runDir });
  advance(chatAcceptanceState, { to: 'RESOLVED', sessionId: 'session-1', machineId: 'machine-1', evidenceRefs: ['E-ACCEPT-001'] });
  assert.equal(chatAcceptanceState.phase, 'RESOLVED');
  assert.equal(chatAcceptanceState.acceptance.mode, 'chat_exact');
  assert.equal(chatAcceptanceState.gates.acceptance.status, 'approved');

  recordAcceptance(state, {
    status: 'approved',
    operator_verified: false,
    current_status: 'RESOLVED',
    observed_at: '2026-11-10T18:30:00+08:00',
    evidence_kind: 'current_status+latest_human_comment',
    evidence_ref: 'evidence/manifest.json#E-ACCEPT-001',
  }, { runDir });
  advance(state, { to: 'RESOLVED', sessionId: 'session-1', machineId: 'machine-1', evidenceRefs: ['E-ACCEPT-001'] });
  assert.equal(state.phase, 'RESOLVED');
  assert.match(state.next_action.action, /已验收/);

  const report = renderReport(state, manifest3);
  for (let i = 1; i <= 13; i += 1) assert.match(report, new RegExp(`## ${i}\\.`));
  assert.match(report, /reviewable/);
  assert.match(report, /raw_retained/);
  assert.match(report, /打开查询页/);
  assert.match(report, /merge-commit-4538/);
  assert.match(report, /squash-deployed-sha-4538/);
  assert.match(report, /pipelines\/4538/);
  assert.match(report, /流水线、rollout 和部署 SHA 来自 Agent 对 GitLab 的查询记录/);

  const unknownField = structuredClone(state);
  unknownField.unexpected = true;
  assert.match(validateStateShape(unknownField).join('\n'), /additional property is forbidden/);
  const tooManyRounds = structuredClone(state);
  tooManyRounds.patch_round = 99;
  assert.match(validateStateShape(tooManyRounds).join('\n'), /must be <= 3/);

  const productionScope = structuredClone(state);
  productionScope.data_policy.scope = { status: 'pending', tables: [] };
  assert.throws(() => setDataScope(productionScope, {
    status: 'approved',
    tables: [{
      database: 'gkxlumenx_prod',
      schema: 'gkxlumenx_prod',
      table: 'orders',
      confirmed_by: 'human:owner',
      confirmed_at: '2026-11-10T18:00:00+08:00',
      evidence_ref: 'evidence/manifest.json#E-DATA-001',
    }],
  }, { runDir, policiesRoot }), /rejected by demo-2026-11-10/);
  assert.throws(() => loadAndValidatePolicy(state, policiesRoot, new Date('2030-01-01T00:00:00+08:00')), /expired/);
  const missingApprovalSource = structuredClone(loadedPolicy.policy);
  delete missingApprovalSource.owner_decision.approval_source;
  assert.match(validatePolicy(missingApprovalSource).join('\n'), /approval_source is required/);
  const badReviewPolicy = structuredClone(loadedPolicy.policy);
  badReviewPolicy.owner_decision.review_at = 'not-a-date';
  assert.match(validatePolicy(badReviewPolicy).join('\n'), /owner_decision\.review_at must be a date/);
  const misplacedReviewPolicy = structuredClone(loadedPolicy.policy);
  delete misplacedReviewPolicy.owner_decision.review_at;
  misplacedReviewPolicy.review_at = '2026-11-17';
  assert.match(validatePolicy(misplacedReviewPolicy).join('\n'), /owner_decision\.review_at is required/);

  const bundleState = makeState({ phase: 'READY_DEV', risk: 'M' });
  recordDiagnosis(bundleState, {
    symptom: 'cross-repo contract mismatch',
    reproduction: ['backend returns no series', 'frontend shows empty trend'],
    root_cause: 'producer and consumer changes are coupled',
    counter_evidence: [],
    requirement_refs: ['REQ-BUNDLE'],
    impact_scope: ['backend and frontend BFF'],
  });
  recordPlan(bundleState, {
    change_scope: ['lumen-ui-topic', 'lumen-ui-science-pc'],
    non_goals: [],
    verification_plan: ['repo tests', 'cross-repo integration'],
    rollback_plan: ['revert bundle candidates'],
    data_access: false,
  });
  const bundleRepos = [
    {
      repo_id: 'ui_topic',
      repo_name: 'lumen-ui-science-topic',
      remote: 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-topic.git',
      base_branch: 'dev',
      base_sha: 'topic-base',
      candidate_sha: null,
      planned_change_scope: ['src'],
      role: 'producer',
      depends_on: [],
      ship_order: 1,
    },
    {
      repo_id: 'ui_pc',
      repo_name: 'lumen-ui-science-pc',
      remote,
      base_branch: 'dev',
      base_sha: baseSha,
      candidate_sha: null,
      planned_change_scope: ['src/page'],
      role: 'consumer',
      depends_on: ['ui_topic'],
      ship_order: 2,
    },
  ];
  assert.throws(() => setRepos(bundleState, [
    { ...bundleRepos[0], role: null },
    bundleRepos[1],
  ]), /cross-repo bundle requires repos\[0\]\.role/);
  assert.throws(() => setRepos(bundleState, [
    { ...bundleRepos[0], depends_on: ['ui_pc'] },
    bundleRepos[1],
  ]), /must ship before/);
  setRepos(bundleState, bundleRepos);
  const bundleEnterBinding = {
    repos: bundleState.repos.map((repo) => ({
      repo_id: repo.repo_id,
      repo_name: repo.repo_name,
      base_sha: repo.base_sha,
      candidate_sha: null,
      planned_change_scope: repo.planned_change_scope,
      role: repo.role,
      depends_on: repo.depends_on,
      ship_order: repo.ship_order,
    })),
    diagnosis_hash: diagnosisHash(bundleState),
    plan_hash: sha256(bundleState.plan),
    risk_level: 'M',
    data_policy_version: bundleState.data_policy.policy_version,
    data_policy_hash: bundleState.data_policy.policy_hash,
    data_scope_hash: bundleState.data_policy.scope_hash,
  };
  approveGate(bundleState, {
    gate: 'enter_dev',
    message: '进入开发123',
    binding: bundleEnterBinding,
    sessionId: 'session-1',
    machineId: 'machine-1',
  });
  advance(bundleState, { to: 'IMPLEMENTING', sessionId: 'session-1', machineId: 'machine-1' });
  assert.equal(bundleState.phase, 'IMPLEMENTING');
  assert.deepEqual(bundleState.repos.map((repo) => [repo.repo_id, repo.ship_order]), [['ui_topic', 1], ['ui_pc', 2]]);
  const tamperedBundleGate = structuredClone(bundleState);
  tamperedBundleGate.repos[1].depends_on = [];
  const tamperedBundleValidation = validateGate(tamperedBundleGate, 'enter_dev', { sessionId: 'session-1', machineId: 'machine-1' });
  assert.equal(tamperedBundleValidation.ok, false);
  assert.match(tamperedBundleValidation.errors.join('\n'), /bundle role\/depends_on\/ship_order mismatch/);

  const missingIntegration = structuredClone(preShipState);
  missingIntegration.repos[0].role = 'consumer';
  missingIntegration.repos[0].depends_on = ['ui_topic'];
  missingIntegration.repos[0].ship_order = 2;
  missingIntegration.repos.push({ ...bundleRepos[0] });
  setRisk(missingIntegration, { level: 'M', reasons: ['cross-repo bundle'] });
  recordVerification(missingIntegration, [
    ...missingIntegration.verification_matrix,
    {
      id: 'V-TOPIC-FIX', category: 'fix', behavior: 'topic contract', result: 'PASS',
      repo_ids: ['ui_topic'], evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
    },
    {
      id: 'V-TOPIC-REG', category: 'regression', behavior: 'topic adjacent path', result: 'PASS',
      repo_ids: ['ui_topic'], evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
    },
    {
      id: 'V-TOPIC-BOUNDARY', category: 'boundary', behavior: 'topic empty state', result: 'PASS',
      repo_ids: ['ui_topic'], evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
    },
    {
      id: 'V-PC-BOUNDARY', category: 'boundary', behavior: 'pc empty state', result: 'PASS',
      repo_ids: ['ui_pc'], evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
    },
  ]);
  assert.throws(
    () => advance(missingIntegration, { to: 'READY_SHIP', sessionId: 'session-1', machineId: 'machine-1' }),
    /CROSS_REPO_BUNDLE_INTEGRATION_REQUIRED/,
  );
  recordVerification(missingIntegration, [
    ...missingIntegration.verification_matrix,
    {
      id: 'V-BUNDLE-INTEGRATION', category: 'integration', behavior: 'producer and consumer work together', result: 'PASS',
      repo_ids: ['ui_topic', 'ui_pc'], evidence_refs: ['evidence/manifest.json#E-VERIFY-001'],
    },
  ]);
  assert.doesNotThrow(() => advance(missingIntegration, { to: 'READY_SHIP', sessionId: 'session-1', machineId: 'machine-1' }));

  const reopened = structuredClone(state);
  reopenState(reopened, { runDir, reason: 'regressed', sessionId: 'session-1' });
  assert.equal(reopened.phase, 'REOPENED');
  assert.equal(reopened.cycle_seq, 2);
  assert.equal(reopened.cycles.length, 2);
  assert.equal(reopened.gates.enter_dev.status, 'pending');
  assert.match(reopened.next_action.action, /重新诊断/);
  assert.doesNotThrow(() => validateStateShape(reopened), 'REOPENED state must remain schema-valid');
  const archived = JSON.parse(readFileSync(join(runDir, 'cycles', state.current_cycle_id, 'state.json'), 'utf8'));
  const archivedCycle = archived.cycles.find((cycle) => cycle.cycle_id === state.current_cycle_id);
  assert.match(archivedCycle.closed_at, /^20/);
  assert.equal(archivedCycle.state_ref, `cycles/${state.current_cycle_id}/state.json`);
  assert.equal(JSON.parse(readFileSync(join(runDir, 'cycles', state.current_cycle_id, 'evidence', 'manifest.json'), 'utf8')).items.length > 0, true);
  assert.equal(JSON.parse(readFileSync(manifestPath, 'utf8')).items.length, 0);
  assert.throws(() => recordAcceptance(reopened, {
    status: 'approved',
    current_status: 'RESOLVED',
    observed_at: '2026-11-10T18:30:00+08:00',
    evidence_kind: 'x',
    evidence_ref: 'evidence/manifest.json#E-X',
  }), /cannot record approved acceptance in REOPENED/);

  const failureState = makeState();
  recordFailure(failureState, { stage: 'dev_verify', class: 'product_or_code' });
  recordFailure(failureState, { stage: 'dev_verify', class: 'product_or_code' });
  recordFailure(failureState, { stage: 'dev_verify', class: 'product_or_code' });
  assert.equal(failureState.patch_round, 3);
  assert.throws(() => recordFailure(failureState, { stage: 'dev_verify', class: 'product_or_code' }), /limit is 3/);

  const blocked = makeState();
  blockState(blocked, { reason: 'missing requirement', condition: 'requirement supplied', resumePhase: 'READY_DEV', owner: 'human:owner' });
  assert.equal(blocked.phase, 'BLOCKED');
  assert.deepEqual(validateStateShape(blocked), []);

  const missingRefState = structuredClone(preShipState);
  missingRefState.verification_matrix[0].evidence_refs = ['evidence/manifest.json#E-MISSING'];
  assert.throws(
    () => advance(missingRefState, { to: 'READY_SHIP', sessionId: 'session-1', machineId: 'machine-1' }),
    /E-MISSING is missing from verified manifest/,
  );

  rmSync(join(runDir, 'evidence', 'raw', 'scope.txt'));
  const nonReviewable = structuredClone(manifest3);
  nonReviewable.items[0].reviewable = false;
  nonReviewable.items[0].raw_retained = false;
  nonReviewable.items[0].non_reviewable_reason = 'browser console unavailable';
  const missingRawManifest = structuredClone(manifest3);
  const unretained = recordEvidence(runDir, missingRawManifest, {
    evidence_id: 'E-UNRETAINED-001',
    kind: 'note',
    result: 'SIMULATED',
    raw_path: 'evidence/raw/already-removed.txt',
    sha256: sha256('captured-before-removal'),
    reviewable: false,
    raw_retained: false,
    non_reviewable_reason: 'raw file removed after summarization',
    command: null,
    exit_code: null,
    commit_sha: candidateSha,
    environment: 'local',
    collected_at: '2026-11-10T18:20:00+08:00',
    summary: 'non-reviewable retained as an index only',
  });
  assert.equal(unretained.raw_retained, false);
  writeFileSync(manifestPath, `${JSON.stringify(missingRawManifest, null, 2)}\n`);
  assert.throws(() => recordEvidence(runDir, structuredClone(missingRawManifest), {
    evidence_id: 'E-BAD-REVIEWABLE-001',
    kind: 'note',
    result: 'PASS',
    raw_path: 'evidence/raw/also-removed.txt',
    sha256: sha256('captured-before-removal'),
    reviewable: true,
    raw_retained: false,
    command: null,
    exit_code: null,
    commit_sha: candidateSha,
    environment: 'local',
    collected_at: '2026-11-10T18:21:00+08:00',
  }), /reviewable=true requires raw_retained=true/);

  const reviewState = structuredClone(preShipState);
  const reviewResult = verifyEvidence(reviewState, nonReviewable, runDir);
  assert.equal(reviewResult.result, 'PASS');
  assert.deepEqual(reviewResult.non_reviewable, ['E-DATA-001']);
  assert.match(renderReport(reviewState, nonReviewable), /browser console unavailable/);

  const unsupportedPassState = structuredClone(preShipState);
  unsupportedPassState.verification_matrix[0].evidence_refs = ['evidence/manifest.json#E-DATA-001'];
  unsupportedPassState.evidence.verification = reviewResult;
  assert.throws(
    () => advance(unsupportedPassState, { to: 'READY_SHIP', sessionId: 'session-1', machineId: 'machine-1' }),
    /PASS evidence E-DATA-001 must be reviewable with raw_retained=true/,
  );

  assert.throws(() => loadPolicy('missing-policy', policiesRoot), /POLICY_NOT_FOUND/);
  assert.equal(existsSync(manifestPath), true);
  console.log('bugflow-state.selfcheck ok');
} finally {
  rmSync(tmp, { recursive: true, force: true });
}
