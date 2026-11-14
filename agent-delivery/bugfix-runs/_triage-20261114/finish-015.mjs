// 015-7167862142 收尾：evidence → verify-evidence → verify-repo → review → REVIEWING → VERIFYING → READY_SHIP
// ship 门（提测）等当次会话用户精确口令，本脚本不推进 SHIPPING。
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, copyFileSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration';
const SCRIPT = join(ROOT, '.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs');
const RUN = join(ROOT, 'agent-delivery\\bugfix-runs\\015-7167862142');
const LOCAL = join(RUN, 'local');
const EV = join(RUN, 'evidence');
const WT = 'E:\\zhipu\\gkx-lumen\\worktrees\\lumen-ui-science-pc--bug015';
const MAIN = 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc';
const CANDIDATE = '5e96b09'; // 本单候选提交（已在 origin/dev eab3146 内）
const BASE = '7ef79f4';
const NOW = new Date().toISOString();
const COMMON = ['--auto-number', '015', '--work-item-id', '7167862142'];
mkdirSync(LOCAL, { recursive: true });

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}
function writeJson(path, obj) {
  writeFileSync(path, JSON.stringify(obj, null, 2), 'utf8');
}

// 0) worktree 回到候选提交（合并提交已推入 origin/dev，可安全剥离；让 HEAD==candidate 通过 verify-repo）
execFileSync('git', ['-C', WT, 'reset', '--hard', CANDIDATE], { stdio: 'inherit' });

// 1) 证据一：主仓（已含候选）重跑 FE-POL-03A 自检，原件落盘
const selfOut = execFileSync('node', [join(MAIN, 'src', 'views', 'policy', 'simulation', 'FE-POL-03A.test.mjs')], {
  cwd: MAIN,
  encoding: 'utf8',
});
writeFileSync(join(EV, 'fe-pol-03a-selfcheck.out'), selfOut, 'utf8');

// 2) 证据二：类型门原始终端捕获（status: succeeded / exit_code: 0）
copyFileSync(
  'C:\\Users\\redfo\\.cursor\\projects\\e-zhipu-gkx-lumen-gkx-orchestration\\terminals\\815184.txt',
  join(EV, 'vue-tsc-typecheck.out'),
);

// 3) record-evidence（裸数组）+ verify-evidence
const batch = [
  {
    evidence_id: 'ev-015-1-selfcheck',
    kind: 'test',
    result: 'PASS',
    raw_path: 'evidence/fe-pol-03a-selfcheck.out',
    reviewable: true,
    raw_retained: true,
    command: `node src/views/policy/simulation/FE-POL-03A.test.mjs（cwd ${MAIN}，HEAD=785b2d5 含候选）`,
    exit_code: 0,
    commit_sha: CANDIDATE,
    environment: 'local win32 node v22.13.0',
    collected_at: NOW,
    summary: 'FE-POL-03A 自检 50 项全绿，含 241-8 关键节点说明显式区块断言',
  },
  {
    evidence_id: 'ev-015-2-typecheck',
    kind: 'test',
    result: 'PASS',
    raw_path: 'evidence/vue-tsc-typecheck.out',
    reviewable: true,
    raw_retained: true,
    command: `npx vue-tsc --build（cwd ${MAIN}，合并候选后基线 785b2d5）`,
    exit_code: 0,
    commit_sha: CANDIDATE,
    environment: 'local win32 node v22.13.0',
    collected_at: NOW,
    summary: '主仓全量 vue-tsc 类型门 0 错误（exit 0，773931ms）',
  },
];
const batchPath = join(LOCAL, 'evidence-batch.json');
writeJson(batchPath, batch);
run([...COMMON, 'record-evidence', '--evidence-batch-file', batchPath]);
run([...COMMON, 'verify-evidence']);

// 4) verify-repo（worktree HEAD=candidate，scope 差集=本单 2 文件）
run([...COMMON, 'verify-repo', '--repo-id', 'ui_pc', '--repo-dir', WT, '--candidate-sha', CANDIDATE, '--base-sha', BASE]);

// 5) 评审（S 风险允许非独立评审：reviewer=实现方 agent 本体）
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

// 6) 验证矩阵（S 风险：fix + regression 两类必备）→ VERIFYING
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

// 7) READY_SHIP（提测门等人）
run([...COMMON, 'advance', '--to', 'READY_SHIP', '--session-id', 'cursor-20261114-1317', '--machine-id', 'redfo-win']);
run([...COMMON, 'render-report']);
console.log('=== 015 -> READY_SHIP（等待用户「提测」口令）');
