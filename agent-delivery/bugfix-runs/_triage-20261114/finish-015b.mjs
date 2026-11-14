// 015 续跑：verify-repo（全量 SHA）→ review → REVIEWING → VERIFYING → READY_SHIP
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration';
const SCRIPT = join(ROOT, '.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs');
const LOCAL = join(ROOT, 'agent-delivery\\bugfix-runs\\015-7167862142\\local');
const WT = 'E:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug015';
const CANDIDATE = execFileSync('git', ['-C', WT, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
const BASE = '7ef79f4';
const COMMON = ['--auto-number', '015', '--work-item-id', '7167862142'];
mkdirSync(LOCAL, { recursive: true });

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}
function writeJson(path, obj) {
  writeFileSync(path, JSON.stringify(obj, null, 2), 'utf8');
}
console.log('CANDIDATE =', CANDIDATE);

// 1) verify-repo
run([...COMMON, 'verify-repo', '--repo-id', 'ui_pc', '--repo-dir', WT, '--candidate-sha', CANDIDATE, '--base-sha', BASE]);

// 2) 评审（reviewed_sha 须等于 state.repos.candidate_sha = 全量 SHA）
const review = {
  repos: [
    {
      repo_id: 'ui_pc',
      reviewer: 'agent:frontend-agent',
      reviewed_sha: CANDIDATE,
      verdict: 'PASS',
      independent: false,
      scope: '241 关键节点说明：模板区块（流程图卡内逐环节卡四字段）+ scoped 样式族 + FE-POL-03A 断言；scope 差集仅 2 文件',
      findings: [],
      round: 1,
    },
  ],
};
const reviewPath = join(LOCAL, 'review.json');
writeJson(reviewPath, review);
run([...COMMON, 'record-review', '--review-file', reviewPath]);
run([...COMMON, 'advance', '--to', 'REVIEWING', '--session-id', 'cursor-20261114-1317', '--machine-id', 'redfo-win']);

// 3) 验证矩阵 → VERIFYING → READY_SHIP
const matrix = [
  {
    id: 'v-015-fix-241-keynodes',
    category: 'fix',
    behavior: '241 真轨流程图卡出现「关键节点说明」显式区块，逐环节卡含环节名/时间安排/责任主体/说明四字段',
    result: 'PASS',
    repo_ids: ['ui_pc'],
    evidence_refs: ['ev-015-1-selfcheck'],
  },
  {
    id: 'v-015-regression-full',
    category: 'regression',
    behavior: 'FE-POL-03A 全量 50 项断言无回归；vue-tsc 全量类型门 0 错误',
    result: 'PASS',
    repo_ids: ['ui_pc'],
    evidence_refs: ['ev-015-1-selfcheck', 'ev-015-2-typecheck'],
  },
];
const matrixPath = join(LOCAL, 'verification-matrix.json');
writeJson(matrixPath, matrix);
run([...COMMON, 'record-verification', '--items-file', matrixPath]);
run([...COMMON, 'advance', '--to', 'VERIFYING', '--session-id', 'cursor-20261114-1317', '--machine-id', 'redfo-win']);
run([...COMMON, 'advance', '--to', 'READY_SHIP', '--session-id', 'cursor-20261114-1317', '--machine-id', 'redfo-win']);
run([...COMMON, 'render-report']);
console.log('=== 015 -> READY_SHIP（等待用户「提测」口令）');
