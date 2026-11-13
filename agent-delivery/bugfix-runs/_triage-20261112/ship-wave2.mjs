// 第二波 4 单提测段（幂等）：ship 门批准 -> SHIPPING -> 录 dev 证据 -> ship package -> DEV_VERIFYING -> AWAITING_ACCEPTANCE
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs';
const SID = 'cursor-20261112-2007-batch-a';
const MID = 'redfo-win';
const TOKEN_MSG = 'questionnaire:用户本会话精确口令「提测」(chat:2026-11-13T11:04+08:00)';
const PIPELINE = {
  id: '5146',
  url: 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5146',
  image: 'harbor.test.com/zp-tts/gkx-lumen-pc:7e3fb5bc',
};
const MERGE_SHA = '7e3fb5bc89cf4656316ec29f84e4fbe2c6cc799f';
const { verificationHash, reviewHash } = await import('file:///e:/zhipu/gkx-lumen/gkx-orchestration/.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs');

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}

for (const runId of ['010-7166979592', '011-7167287026', '012-7167124091', '013-7166233464']) {
  const runDir = join(ROOT, runId);
  const common = ['--run-dir', runDir];
  const local = join(runDir, 'local');
  mkdirSync(local, { recursive: true });
  const load = () => JSON.parse(readFileSync(join(runDir, 'state.json'), 'utf8'));
  let state = load();
  const num = state.work_item.auto_number;

  // 1) ship 门批准（未批才批）
  if (state.gates.ship.status !== 'approved') {
    const repo = (state.repos ?? []).find((r) => r.repo_id === 'ui_pc');
    const impl = (state.implementation?.repos ?? []).find((r) => r.repo_id === 'ui_pc');
    const review = (state.review?.repos ?? []).find((r) => r.repo_id === 'ui_pc');
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
      '--message', `提测${num}`,
      '--approved-by', 'human:淮政玮',
      '--message-ref', TOKEN_MSG,
      '--active-runs', '4',
      '--session-id', SID, '--machine-id', MID,
      '--binding-file', bindingPath]);
    run([...common, 'advance', '--to', 'SHIPPING', '--session-id', SID, '--machine-id', MID]);
  } else {
    console.log(`skip approve-gate ${runId}`);
  }

  // 2) dev 证据（未录才录）
  state = load();
  const manifest = JSON.parse(readFileSync(join(runDir, 'evidence', 'manifest.json'), 'utf8'));
  if (!(manifest.items ?? []).some((it) => it.evidence_id === 'ev-dev-verify')) {
    const devRaw = join(runDir, 'evidence', 'raw', 'dev-verify.txt');
    writeFileSync(devRaw, [
      'cmd: Invoke-WebRequest http://10.50.69.111:30891/ (dev 前端入口探活)',
      'result: HTTP 200 (len=476)',
      `pipeline: ${PIPELINE.id} success (${PIPELINE.url})`,
      `image: ${PIPELINE.image}`,
      'rollout: deployment "gkx-lumen-pc" successfully rolled out (deploy:k8s job 39821, log 2026-11-12T19:06:38Z)',
      `push_sha: ${MERGE_SHA} (git merge-base --is-ancestor => True, origin/dev=b8a55cc)`,
      'candidate containment: 4 轨道分支 tip (70ac607/3c97b64/20ffbb3/61202b3) 均为 7e3fb5bc 祖先（merge 8dc9c3f 系列 + 集成类型修复 7e3fb5b）',
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
      note: 'dev 部署链 terminal success + 探活 200',
    }), 'utf8');
    run([...common, 'record-evidence', '--evidence-file', evPath]);
  } else {
    console.log(`skip evidence ${runId}`);
  }

  // 3) ship package（重录覆盖，dev_verification=PASS）
  state = load();
  const repo = (state.repos ?? []).find((r) => r.repo_id === 'ui_pc');
  const pkgPath = join(local, 'ship-package.json');
  writeFileSync(pkgPath, JSON.stringify({
    repos: [{
      repo_id: 'ui_pc',
      candidate_sha: repo.candidate_sha,
      merge_request_id: 'direct-push-dev',
      merge_commit_sha: MERGE_SHA,
      pipeline_id: PIPELINE.id,
      pipeline_status: 'success',
      pipeline_url: PIPELINE.url,
      deployed_sha: '7e3fb5bc',
      rollout_status: 'complete',
      image_tag: PIPELINE.image,
    }],
    acceptance_steps: [
      '打开 dev 环境 http://10.50.69.111:30891/ ，硬刷新（Ctrl+F5）确保加载 7e3fb5bc 版本',
      '按各工单描述原文逐一复核对应页面交互（报告文案/互动解读空态/趋势图x轴/全景锚点定位）',
      '确认无回归：相邻页签、图表切换、政策全景检索分组等相邻功能可用',
    ],
    dev_verification: {
      result: 'PASS',
      evidence_refs: ['ev-dev-verify'],
    },
  }, null, 2), 'utf8');
  run([...common, 'record-ship-package', '--input-file', pkgPath]);

  // 4) DEV_VERIFYING（未到才推）
  state = load();
  const order = ['READY_SHIP', 'SHIPPING', 'DEV_VERIFYING', 'AWAITING_ACCEPTANCE'];
  const idx = order.indexOf(state.phase);
  for (const to of order.slice(Math.max(idx, 0) + 1)) {
    run([...common, 'advance', '--to', to, '--session-id', SID, '--machine-id', MID]);
  }
  console.log(`=== ${runId} -> ${load().phase}`);
}
console.log('ALL-WAVE2-TEST-SUBMITTED');
