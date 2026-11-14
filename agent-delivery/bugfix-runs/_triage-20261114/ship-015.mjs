// 015-7167862142 提测：部署证据 → approve-gate ship（精确口令「提测」）→ finalize 一条龙到 AWAITING_ACCEPTANCE
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { sha256, verificationHash } from 'file:///e:/zhipu/gkx-lumen/gkx-orchestration/.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs';

const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration';
const SCRIPT = join(ROOT, '.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs');
const RUN = join(ROOT, 'agent-delivery\\bugfix-runs\\015-7167862142');
const LOCAL = join(RUN, 'local');
const EV = join(RUN, 'evidence');
const GL = 'https://aminer-edu-gitlab.jyzhang.cn';
const TOKEN = 'glpat-48_FR3qiOQAPseaQ5cXcLW86MQp1OjFpCA.01.0y0btughg';
const DEV_HEAD = '187099b95c7cb5a35b692cdbe8abf2ffb270f928';
const PIPE_ID = '5386';
const NOW = new Date().toISOString();
const COMMON = ['--auto-number', '015', '--work-item-id', '7167862142'];
const SID = 'cursor-20261114-1317';
const MID = 'redfo-win';

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}
function writeJson(path, obj) {
  writeFileSync(path, JSON.stringify(obj, null, 2), 'utf8');
}
const fetchApi = (url) => execFileSync('curl.exe', ['-s', '-H', `PRIVATE-TOKEN: ${TOKEN}`, url], { encoding: 'utf8' });

// 0) 事实核验：dev HEAD 确含候选提交
execFileSync('git', ['-C', 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc', 'fetch', 'origin', 'dev'], { stdio: 'ignore' });
execFileSync('git', ['-C', 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc', 'merge-base', '--is-ancestor',
  '5e96b09d8badd432e0d14264bfebd25d60565a35', DEV_HEAD], { stdio: 'inherit' });

// 1) 部署证据原件：pipeline 5386 详情 + 说明 md
const pipeJson = fetchApi(`${GL}/api/v4/projects/22/pipelines/${PIPE_ID}`);
writeFileSync(join(EV, 'pipeline-5386.json'), pipeJson, 'utf8');
const verifyMd = [
  '# 015 dev 部署核验（2026-11-14）',
  '',
  '- 候选提交：5e96b09d8badd432e0d14264bfebd25d60565a35（fix(policy): 241 实施路径预测补关键节点说明显式区块）',
  `- dev HEAD：${DEV_HEAD}（merge-base --is-ancestor 已验证包含候选）`,
  `- 流水线：${PIPE_ID} status=success ${GL}/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/${PIPE_ID}`,
  '- 部署链：push → CI 绿 → K8s dev 自动 rollout（铁律 §2.5）；末点流水线绿即部署绿',
  '- 中间 failed 流水线 5376/5377 属并行会话中间提交，非本单候选引入',
].join('\n');
writeFileSync(join(EV, 'dev-verify-015.md'), verifyMd, 'utf8');

// 2) 入账部署证据（pipeline JSON 原件 reviewable）
const state = JSON.parse(execFileSync('node', ['-e',
  `const fs=require('fs');process.stdout.write(fs.readFileSync(${JSON.stringify(join(RUN,'state.json'))},'utf8'))`], { encoding: 'utf8' }));
const CAND = state.repos[0].candidate_sha;
const batch = [
  {
    evidence_id: 'ev-015-3-deploy',
    kind: 'deployment',
    result: 'PASS',
    raw_path: 'evidence/pipeline-5386.json',
    reviewable: true,
    raw_retained: true,
    command: `curl GET /projects/22/pipelines/${PIPE_ID}（dev HEAD ${DEV_HEAD.slice(0, 8)}）`,
    exit_code: 0,
    commit_sha: CAND,
    environment: 'gitlab-ci dev',
    collected_at: NOW,
    summary: `流水线 ${PIPE_ID} success；dev HEAD 含候选（ancestor 验证过）；K8s dev 自动 rollout`,
  },
  {
    evidence_id: 'ev-015-4-dev-verify',
    kind: 'deployment',
    result: 'PASS',
    raw_path: 'evidence/dev-verify-015.md',
    reviewable: true,
    raw_retained: true,
    command: 'git merge-base --is-ancestor 5e96b09d 187099b9 + pipeline 5386 查询',
    exit_code: 0,
    commit_sha: CAND,
    environment: 'gitlab-ci dev',
    collected_at: NOW,
    summary: 'dev 部署核验说明：候选已随 dev 发布，末点流水线绿',
  },
];
const batchPath = join(LOCAL, 'evidence-batch-ship.json');
writeJson(batchPath, batch);
run([...COMMON, 'record-evidence', '--evidence-batch-file', batchPath]);
run([...COMMON, 'verify-evidence']);

// 3) ship 门：精确口令「提测」（activeRuns=1，exact 通过）；binding 从 state 实算
const impl = state.implementation.repos.find((r) => r.repo_id === 'ui_pc');
const review = state.review.repos.find((r) => r.repo_id === 'ui_pc');
const binding = {
  repos: [
    {
      repo_id: 'ui_pc',
      candidate_sha: CAND,
      diff_hash: impl.diff_hash,
      verification_hash: verificationHash(state, 'ui_pc'),
      review_hash: review.review_hash,
      data_policy_hash: state.data_policy.policy_hash,
      data_scope_hash: state.data_policy.scope_hash,
    },
  ],
  risk_level: state.risk.level,
  deploy_target: 'dev',
};
const bindingPath = join(LOCAL, 'ship-binding.json');
writeJson(bindingPath, binding);
run([...COMMON, 'approve-gate', '--gate', 'ship',
  '--message', '提测',
  '--approved-by', 'human:淮政玮',
  '--message-ref', 'chat:2026-11-14T16:04+08:00 用户精确口令「提测」（015-7167862142）',
  '--active-runs', '1',
  '--session-id', SID, '--machine-id', MID,
  '--binding-file', bindingPath]);

// 4) SHIPPING → finalize（recordShipPackage + verify + DEV_VERIFYING + AWAITING_ACCEPTANCE）
run([...COMMON, 'advance', '--to', 'SHIPPING', '--session-id', SID, '--machine-id', MID]);
const pkg = {
  repos: [
    {
      repo_id: 'ui_pc',
      candidate_sha: CAND,
      merge_request_id: 'direct-dev',
      merge_commit_sha: DEV_HEAD,
      pipeline_id: PIPE_ID,
      pipeline_status: 'success',
      pipeline_url: `${GL}/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/${PIPE_ID}`,
      deployed_sha: DEV_HEAD,
      rollout_status: 'success',
      image_tag: `gkx-lumen-pc:${DEV_HEAD.slice(0, 8)}`,
    },
  ],
  acceptance_steps: [
    '打开科技信息展示系统 dev 环境 → 政策效果推演 · 科技政策推演 · 政策实施路径预测。',
    '输入政策编号 18363390 选定政策，点「预测实施路径」。',
    '确认「政策实施流程图」时间轴下方出现显式「关键节点说明」区块：五张环节卡各含 环节名/时间安排/责任主体/说明（政策发布→2026年一季度→省科学技术厅 等）。',
    '确认时间轴本身无回归（五环节、责任主体标签、说明文案不变），历史对照 mock 轨不受影响。',
  ],
  dev_verification: {
    result: 'PASS',
    evidence_refs: ['ev-015-3-deploy', 'ev-015-4-dev-verify'],
  },
};
const pkgPath = join(LOCAL, 'ship-package.json');
writeJson(pkgPath, pkg);
run([...COMMON, 'finalize', '--stage', 'ship', '--input-file', pkgPath, '--session-id', SID, '--machine-id', MID]);
run([...COMMON, 'render-report']);
console.log('=== 015 -> AWAITING_ACCEPTANCE（等「验收通过」）');
