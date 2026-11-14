// 014 v2: set-repos(JSON数组) + record-plan + verify-repo(--repo-dir) + record-verification(items数组)
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const RUN_DIR = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\014-7168131856';
const TRIAGE = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\_triage-20261114';
const SID = 'cursor-20261114-1317-batch-a';
const MID = 'redfo-win';
const REPO = 'e:\\zhipu\\gkx-lumen\\repos\\lumen-ui-science-pc';
const CANDIDATE = '8fff84b';
const BASE = 'c70a9f9';

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}
function payload(name, obj) {
  const file = join(TRIAGE, name);
  writeFileSync(file, JSON.stringify(obj, null, 2), 'utf8');
  return file;
}

// 1. set-repos：已单独跑成功（1 repos recorded），此处跳过

// 2. record-plan
run(['record-plan', '--run-dir', RUN_DIR, '--input-file', payload('plan-014.json', {
  change_scope: [
    { repo_id: 'ui_pc', file: 'src/views/policy/simulation/simulationLive.mjs',
      why: '恢复 termKpiItems/similarPolicyItems 竖线格式解析（01e86b2 去重时误删），灌数端 mockgen/simulation.py 直写竖线格式' },
  ],
  non_goals: ['不改灌数端格式（后端为真源）', '不动 Java/Python 链路', '不加新依赖'],
  verification_plan: [
    'node src/views/policy/simulation/simulationLive.test.mjs（条件闭集自检，含竖线用例）',
    'pnpm type-check（vue-tsc --build 全仓 0 error）',
    'K8s dev 环境页面复核：新出台预测 → 选政策 → 运行预测 → 短中长期效果卡出 3 枚 KPI',
  ],
  rollback_plan: ['git revert 8fff84b 单提交回退，无数据/无 schema 变更'],
  data_access: false,
})]);

// 3. verify-repo：--repo-dir + 可选 expect
run(['verify-repo', '--run-dir', RUN_DIR,
  '--repo-id', 'ui_pc',
  '--repo-dir', REPO,
  '--candidate-sha', CANDIDATE,
  '--base-sha', BASE]);

// 4. record-verification：items 数组（id/category/behavior/result 必填）
run(['record-verification', '--run-dir', RUN_DIR, '--items-file', payload('verify-014.json', [
  { id: 'V-014-selfcheck', category: 'fix', behavior: 'node src/views/policy/simulation/simulationLive.test.mjs 条件闭集自检（含竖线格式 termKpiItems/similarPolicyItems 用例）', result: 'PASS', evidence: '自检输出「simulationLive 条件闭集自检通过」，exit 0' },
  { id: 'V-014-typecheck', category: 'fix', behavior: 'pnpm type-check（vue-tsc --build 全仓类型门）', result: 'PASS', evidence: 'TYPECHECK_EXIT=0' },
  { id: 'V-014-regression', category: 'regression', behavior: '括号格式与 JSON 数组兜底解析不回归（测试既有用例）', result: 'PASS', evidence: '自检含「短期(2.5,2.6,5)…」与 JSON 数组用例均通过' },
  { id: 'V-014-push', category: 'integration', behavior: 'git push origin dev（先 rejected → pull --rebase → 重推）', result: 'PASS', evidence: 'c70a9f9..8fff84b dev -> dev；HEAD=8fff84b 含修复' },
])]);

console.log('PLAN-VERIFY-014-DONE');
