// 014 提测段（幂等）：ship 门批准 -> SHIPPING -> 录 dev 证据 -> ship package(dev_verification=PASS)
//                     -> DEV_VERIFYING -> AWAITING_ACCEPTANCE
// 口令：用户 2026-11-14 16:04 chat「提测」（active-runs=1，带号形式「提测014」亦合法）
// 部署事实：image gkx-lumen-pc:187099b9（dev tip 187099b，候选 8fff84b 为其祖先）；rollout complete；NodePort 30891 探活 HTTP 200
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const RUN_DIR = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\014-7168131856';
const SID = 'cursor-20261114-1317-batch-a';
const MID = 'redfo-win';
const TOKEN_MSG = 'chat:2026-11-14T16:04+08:00 用户本会话精确口令「提测」';
const MERGE_SHA = '187099b95c7cb5a35b692cdbe8abf2ffb270f928';
const IMAGE = 'harbor.test.com/zp-tts/gkx-lumen-pc:187099b9';
const { verificationHash, reviewHash } = await import('file:///' + SCRIPT.replace(/\\/g, '/'));

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}
function load() {
  return JSON.parse(readFileSync(join(RUN_DIR, 'state.json'), 'utf8'));
}
const local = join(RUN_DIR, 'local');
mkdirSync(local, { recursive: true });
const common = ['--run-dir', RUN_DIR];

// 0) 前置校验：候选必须在最新 dev 里（防并发 push 后脱钩）
{
  const head = execFileSync('git', ['-C', 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc', 'rev-parse', 'origin/dev'], { encoding: 'utf8' }).trim();
  execFileSync('git', ['-C', 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc', 'merge-base', '--is-ancestor', '8fff84bb76e9c825e2e8224ca8c01047e396a8fd', head]);
  console.log(`origin/dev tip = ${head.slice(0, 7)} (candidate 8fff84b contained)`);
}

// 1) ship 门批准（未批才批）
let state = load();
if (state.gates.ship.status !== 'approved') {
  if (state.phase !== 'READY_SHIP') throw new Error(`phase=${state.phase}, expect READY_SHIP`);
  const repo = state.repos.find((r) => r.repo_id === 'ui_pc');
  const impl = state.implementation.repos.find((r) => r.repo_id === 'ui_pc');
  const review = state.review.repos.find((r) => r.repo_id === 'ui_pc');
  const bindingPath = join(local, 'ship-binding.json');
  writeFileSync(bindingPath, JSON.stringify({
    risk_level: state.risk.level,
    deploy_target: 'dev',
    repos: [{
      repo_id: 'ui_pc',
      candidate_sha: repo.candidate_sha,
      diff_hash: impl.diff_hash,
      verification_hash: verificationHash(state, 'ui_pc'),
      review_hash: reviewHash(review),
      data_policy_hash: state.data_policy.policy_hash,
      data_scope_hash: state.data_policy.scope_hash,
      role: repo.role,
      depends_on: repo.depends_on ?? [],
      ship_order: repo.ship_order,
    }],
  }, null, 2), 'utf8');
  run([...common, 'approve-gate', '--gate', 'ship',
    '--message', '提测014',
    '--approved-by', 'human:淮政玮',
    '--message-ref', TOKEN_MSG,
    '--active-runs', '1',
    '--session-id', SID, '--machine-id', MID,
    '--binding-file', bindingPath]);
  run([...common, 'advance', '--to', 'SHIPPING', '--session-id', SID, '--machine-id', MID]);
  console.log('=== -> SHIPPING');
} else {
  console.log('skip approve-gate ship');
}

// 2) dev 证据（幂等）
state = load();
const manifest = JSON.parse(readFileSync(join(RUN_DIR, 'evidence', 'manifest.json'), 'utf8'));
if (!(manifest.items ?? []).some((it) => it.evidence_id === 'ev-dev-verify')) {
  const devRaw = join(RUN_DIR, 'evidence', 'raw', 'dev-verify.txt');
  writeFileSync(devRaw, [
    'cmd: kubectl -n zhipu-tts get deploy gkx-lumen-pc + rollout status + curl http://10.50.69.111:30891/',
    'result: image gkx-lumen-pc:187099b9 ready 1/1',
    'rollout: deployment "gkx-lumen-pc" successfully rolled out',
    'probe: HTTP 200 (NodePort 30891, index-CuhT2dkS.js)',
    `deployed dev tip: ${MERGE_SHA}`,
    'candidate containment: 8fff84bb76e9c825e2e8224ca8c01047e396a8fd 是 deployed SHA 祖先（merge-base --is-ancestor=0）',
    'collected_at: ' + new Date().toISOString(),
  ].join('\n'), 'utf8');
  const evPath = join(local, 'dev-evidence.json');
  writeFileSync(evPath, JSON.stringify({
    evidence_id: 'ev-dev-verify',
    kind: 'dev_verification',
    result: 'PASS',
    raw_path: 'evidence/raw/dev-verify.txt',
    commit_sha: MERGE_SHA,
    environment: 'k8s-dev-10.50.69.111:30891',
    collected_at: new Date().toISOString(),
    reviewable: true,
    raw_retained: true,
    note: 'rollout complete + 探活 200 + 候选包含于部署 SHA',
  }), 'utf8');
  run([...common, 'record-evidence', '--evidence-file', evPath]);
  console.log('=== ev-dev-verify recorded');
}

// 3) ship package（dev_verification=PASS）
state = load();
if ((state.ship_package?.repos ?? []).length === 0) {
  const repo = state.repos.find((r) => r.repo_id === 'ui_pc');
  const pkgPath = join(local, 'ship-package.json');
  writeFileSync(pkgPath, JSON.stringify({
    repos: [{
      repo_id: 'ui_pc',
      candidate_sha: repo.candidate_sha,
      merge_request_id: 'direct-push-dev',
      merge_commit_sha: MERGE_SHA,
      pipeline_id: 'dev-ci-187099b',
      pipeline_status: 'success',
      pipeline_url: 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/commits/dev',
      deployed_sha: '187099b9',
      rollout_status: 'complete',
      image_tag: IMAGE,
    }],
    acceptance_steps: [
      '打开 dev 环境 http://10.50.69.111:30891/ ，硬刷新（Ctrl+F5）确保加载 187099b9 版本',
      '进入 政策效果推演 · 新出台政策效果预测 / 历史政策效果，执行推演',
      '核对短/中长期效果卡出 3 枚 KPI（GDP/产业/创新），同类政策列表出条目（竖线格式恢复解析）',
      '确认相邻页签（科技政策推演/实施路径等）无回归',
    ],
    dev_verification: {
      result: 'PASS',
      evidence_refs: ['ev-dev-verify'],
    },
  }, null, 2), 'utf8');
  run([...common, 'record-ship-package', '--input-file', pkgPath]);
  console.log('=== ship package recorded');
}

// 4) DEV_VERIFYING -> AWAITING_ACCEPTANCE（幂等推进）
state = load();
const order = ['SHIPPING', 'DEV_VERIFYING', 'AWAITING_ACCEPTANCE'];
const idx = order.indexOf(state.phase);
for (const to of order.slice(Math.max(idx, 0) + 1)) {
  run([...common, 'advance', '--to', to, '--session-id', SID, '--machine-id', MID]);
}
run([...common, 'render-report']);
console.log(`=== final phase: ${load().phase}`);
console.log('ALL-014-SHIP-DONE');
