// 单单 ledger 初始化：015-7167862142（241 政策实施路径预测 · 关键节点说明区块）
// enter_dev 依据：用户 2026-11-14 13:40 本会话指令「按此计划开始」（gkx-display-srs-cover §5 分流 → bugfix 派修）
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { diagnosisHash, sha256 } from '../../../.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs';

const SCRIPT = new URL('.', import.meta.url).pathname.replace(/^\/(\w):/, '$1:\\') + '..\\..\\..\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs';
const SID = 'cursor-20261114-1317';
const MID = 'redfo-win';
const NUM = '015';
const ID = '7167862142';
const BASE_SHA = '7ef79f4';
const REMOTE = 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git';
const GATE_REF = 'chat:2026-11-14T13:40+08:00 用户指令「按此计划开始」（241 需规分句闭合 G2 单路径计划）';
const MATRIX = 'gkx-orchestration/agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/简报/2026-11-14-241-政策实施路径预测-需规分句闭合.md';

const runDir = join(ROOT, `${NUM}-${ID}`);
const local = join(runDir, 'local');
mkdirSync(local, { recursive: true });
const common = ['--auto-number', NUM, '--work-item-id', ID];

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}

// 1) init（CLAIMED）
run([...common, 'init',
  '--title', '政策效果推演-科技政策推演-政策实施路径预测-需规对照有缺失内容：关键节点',
  '--claim-id', `agent-claim-20261114-${NUM}`,
  '--claim-comment-ref', GATE_REF,
  '--claim-operator', 'agent:coordinator-agent',
  '--project-key', '6a687a81e231818dec771f9a',
  '--risk', 'S',
  '--session-id', SID, '--machine-id', MID]);

// 2) 诊断
const symptom = '241 政策实施路径预测：需规两处点名「关键节点 / 关键节点说明」，live 真轨 Timeline 渲染了 stage_text 正文但无「关键节点说明」显式区块，QA 逐字对照找不到该名词（G2：live 砍了形态）';
const diagPath = join(local, 'diagnosis.json');
writeFileSync(diagPath, JSON.stringify({
  symptom,
  reproduction: [
    '打开 政策效果推演 · 科技政策推演 · 政策实施路径预测 子 Tab（USE_MOCK=false）',
    '选政策（样例 18363390）→ 点「预测实施路径」',
    '页面只有「政策实施流程图」时间轴；无「关键节点说明」标题区块，stage_text 混在时间轴项内',
  ],
  root_cause: 'demo 原型 toPathItems 只把 note 混在 Timeline 项内；lumen 复刻保留该形态。需规 241-7/241-8 要「关键节点说明」独立可辨识区块；SDD 功能点表有 241-8 行（节点旁 stage_text）但界面必见清单未列显式区块名。同族先例 7167771715（评价页实施路径与风险辅助·缺关键节点）修法 = PolicyTextAnalysis.vue 显式「关键节点」里程碑卡片区',
  counter_evidence: ['数据侧无缺口：gapfill_policy_sim_result 路径环节五行 stage_text 全非空（policy_id 18363390）', 'mock 轨 policyPathForecastData 与真轨形态缺口无关'],
  requirement_refs: [
    'bid-reference/srs/02-科技信息展示系统/科技政策跟踪/政策效果推演.md 序号241（Excel 244）',
    'sdd/科技政策跟踪-系统详细设计说明书.md §241 功能点 241-8',
    MATRIX,
    'feishu:6a687a81e231818dec771f9a#7167862142 描述（报告人黄敬洲 2026-11-13 15:22）',
  ],
  impact_scope: ['241 子 Tab 真轨区块形态（时间轴下方补关键节点说明卡片行）'],
}, null, 2), 'utf8');
run([...common, 'record-diagnosis', '--input-file', diagPath]);
run([...common, 'advance', '--to', 'DIAGNOSED', '--session-id', SID, '--machine-id', MID]);

// 3) 计划
const planPath = join(local, 'plan.json');
writeFileSync(planPath, JSON.stringify({
  change_scope: [
    'src/views/policy/simulation/interpret/InterpretWorkbench.vue',
    'src/views/policy/simulation/FE-POL-03A.test.mjs',
    '工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS12-SIM-合规演示用例.md',
  ],
  non_goals: [
    '不改 simulation/jobs 契约与 element 读面（数据五行 stage_text 齐备）',
    '不灌历史对照行、不挂历史评估图卡（2026-11-12 卡1=A 维持）',
    '不补 mock 轨形态（缺口只在真轨）',
    '不动说明书（241-8 已有行）',
  ],
  verification_plan: [
    'node 自检：断言 241 真轨模板含「关键节点说明」区块标题且逐环节渲染 stage_name/schedule_text/owner_name/stage_text',
    '合并前 vue-tsc 全量类型门',
    '提测后 dev 环境人工抽验（选 18363390 → 路径预测 → 须见流程图 + 关键节点说明）',
  ],
  rollback_plan: ['git revert 候选 commit 后随下一波 dev 合并回滚；部署回滚走 CI 重发上一 green SHA'],
  data_access: false,
}, null, 2), 'utf8');
run([...common, 'record-plan', '--input-file', planPath]);
run([...common, 'advance', '--to', 'READY_DEV', '--session-id', SID, '--machine-id', MID]);

// 4) repos
const reposPath = join(local, 'repos.json');
writeFileSync(reposPath, JSON.stringify([{
  repo_id: 'ui_pc',
  repo_name: 'lumen-ui-science-pc',
  remote: REMOTE,
  base_branch: 'dev',
  base_sha: BASE_SHA,
  candidate_sha: null,
  planned_change_scope: ['src/views/policy/simulation/interpret/InterpretWorkbench.vue'],
  role: 'primary',
  depends_on: [],
  ship_order: 1,
}], null, 2), 'utf8');
run([...common, 'set-repos', '--repos-file', reposPath]);

// 5) enter_dev 门批准 + IMPLEMENTING
const state = JSON.parse(readFileSync(join(runDir, 'state.json'), 'utf8'));
const binding = {
  diagnosis_hash: diagnosisHash(state),
  plan_hash: sha256(state.plan ?? null),
  risk_level: state.risk.level,
  data_policy_version: state.data_policy.policy_version,
  data_policy_hash: state.data_policy.policy_hash,
  data_scope_hash: state.data_policy.scope_hash,
  repos: state.repos.map((repo) => ({
    repo_id: repo.repo_id,
    repo_name: repo.repo_name,
    base_sha: repo.base_sha,
    planned_change_scope: repo.planned_change_scope,
  })),
};
const bindingPath = join(local, 'enter-dev-binding.json');
writeFileSync(bindingPath, JSON.stringify(binding, null, 2), 'utf8');

run([...common, 'approve-gate', '--gate', 'enter_dev',
  '--message', `进入开发${NUM}`,
  '--approved-by', 'human:淮政玮',
  '--message-ref', GATE_REF,
  '--active-runs', '1',
  '--session-id', SID, '--machine-id', MID,
  '--binding-file', bindingPath]);
run([...common, 'advance', '--to', 'IMPLEMENTING', '--session-id', SID, '--machine-id', MID]);
console.log(`=== ${NUM}-${ID} -> IMPLEMENTING`);
