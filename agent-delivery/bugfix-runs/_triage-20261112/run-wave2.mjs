// 第二波 4 单 ledger 批量初始化：010-013（B 组前端半边）
// enter_dev 依据：用户 2026-11-13 01:32 指令「获取所有最新代码，开始修下一批」（本会话 chat 精确指令）
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { diagnosisHash, sha256 } from '../../../.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs';

const SCRIPT = new URL('.', import.meta.url).pathname.replace(/^\/(\w):/, '$1:\\') + '..\\..\\..\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs';
const SID = 'cursor-20261112-2007-batch-a';
const MID = 'redfo-win';
const BASE_SHA = 'd6694bfcce1300c036911a12f6f4f8b49e4b971c';
const REMOTE = 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git';
const TRIAGE = 'gkx-orchestration/agent-delivery/bugfix-runs/_triage-20261112/triage-report.md';
const CLAIM_REF = 'chat:2026-11-13T01:32+08:00 用户指令「提交本地所有文件，然后获取所有最新代码，开始修下一批」';

const RUNS = [
  {
    num: '010', id: '7166979592', risk: 'S', branch: 'fix/7166979592-scheme-copy',
    symptom: '政策分析评价-分析报告无数据时展示开发口吻文案，不适合最终用户阅读',
    root: 'schemeBlockReport.ts L130-179 空块降级文案为开发口吻（「报告无数据」等直述），未转用户话术；上游 eval 载荷无行属数据侧缺口（D9 禁伪造）',
    scope: ['src/views/policy/analysis/schemeBlockReport.ts'],
    refs: ['feishu:6a687a81e231818dec771f9a#7166979592 描述（报告人黄敬洲 2026-11-12 17:37）', `${TRIAGE}#B组-010`],
    impacts: ['分析报告空块/无数据文案用户话术化（诚实空态）'],
    nongoals: ['不伪造报告数据（D9）', '不等数据侧灌数（另登记，不阻塞本单）'],
    ver: ['node 自检脚本断言用户可见文案不含开发口吻词且空态话术齐备', '合并前 vue-tsc 全量类型门', '提测后 dev 人工抽验'],
  },
  {
    num: '011', id: '7167287026', risk: 'S', branch: 'fix/7167287026-topic-copy',
    symptom: '分主题分指标互动解读展示表名/行数等开发逻辑文案给最终用户',
    root: 'interpret/TopicIndicatorInteractive.vue L75-98 空态/提示文案直出表名与行数内部口径',
    scope: ['src/views/policy/analysis/interpret/TopicIndicatorInteractive.vue'],
    refs: ['feishu:6a687a81e231818dec771f9a#7167287026 描述（报告人黄敬洲 2026-11-12 18:57）', `${TRIAGE}#B组-011`],
    impacts: ['互动解读空态/提示文案用户话术化'],
    nongoals: ['不伪造解读行本体（gapfill_policy_eval_shell 灌数属数据侧 D16，另登记）', '不改解读请求链路'],
    ver: ['node 自检脚本断言文案不含表名/行数直出', '合并前 vue-tsc 全量类型门', '提测后 dev 人工抽验'],
  },
  {
    num: '012', id: '7167124091', risk: 'S', branch: 'fix/7167124091-trend-xaxis',
    symptom: '多维指标趋势图 x 轴混入两种时间维度（年+季混排），分组错乱',
    root: 'TrendMetricsChart.vue x 轴按行序直排，未按时间维度（年/季）分组对齐，两类粒度行同轴铺开',
    scope: ['src/views/policy/analysis/TrendMetricsChart.vue'],
    refs: ['feishu:6a687a81e231818dec771f9a#7167124091 描述（报告人黄敬洲 2026-11-12 17:44，含需规「多维切换/组合选取」原文）', `${TRIAGE}#B组-012`],
    impacts: ['趋势图 x 轴时间维度分组呈现'],
    nongoals: ['「组合选取评估指标」交互属需规新增口径，需产品/甲方拍板，本单不实现（另登记客户决策清单）', '不改数据载荷'],
    ver: ['node 自检脚本断言 x 轴类目同粒度分组且不混排', '合并前 vue-tsc 全量类型门', '提测后 dev 人工抽验'],
  },
  {
    num: '013', id: '7166233464', risk: 'S', branch: 'fix/7166233464-panorama-anchor',
    symptom: '政策动向跟踪「查看政策全景」跳回全景后定位不准确，看不出定位了什么',
    root: 'analysis/index.vue openKeyFieldPanorama 跳转未携带路由 query 锚点参数，全景页未做滚动定位+高亮',
    scope: ['src/views/policy/analysis/index.vue', 'src/views/policy/panorama/index.vue'],
    refs: ['feishu:6a687a81e231818dec771f9a#7166233464 描述（报告人黄敬洲 2026-11-11 20:51，含需规「政策全景」原文）', `${TRIAGE}#B组-013`],
    impacts: ['跨页跳转锚点定位+目标卡片高亮'],
    nongoals: ['「定位什么」语义按现有页面结构取最直观呈现（领域锚点+卡片高亮），如需更细口径由产品后续定义', '不改筛选链路逻辑'],
    ver: ['node 自检脚本断言跳转携带锚点 query 且全景页消费 query 定位高亮', '合并前 vue-tsc 全量类型门', '提测后 dev 人工抽验'],
  },
];

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}

for (const r of RUNS) {
  const runDir = join(ROOT, `${r.num}-${r.id}`);
  const local = join(runDir, 'local');
  mkdirSync(local, { recursive: true });
  const common = ['--auto-number', r.num, '--work-item-id', r.id];

  // 1) init（CLAIMED）
  run([...common, 'init',
    '--title', r.symptom,
    '--claim-id', `agent-claim-20261113-wave2-${r.num}`,
    '--claim-comment-ref', CLAIM_REF,
    '--claim-operator', 'agent:coordinator-agent',
    '--project-key', '6a687a81e231818dec771f9a',
    '--risk', r.risk,
    '--session-id', SID, '--machine-id', MID]);

  // 2) 诊断
  const diagPath = join(local, 'diagnosis.json');
  writeFileSync(diagPath, JSON.stringify({
    symptom: r.symptom,
    reproduction: [`按飞书工单描述与截图复现（_triage-20261112/${r.id}-1.png）`],
    root_cause: r.root,
    counter_evidence: [],
    requirement_refs: r.refs,
    impact_scope: r.impacts,
  }, null, 2), 'utf8');
  run([...common, 'record-diagnosis', '--input-file', diagPath]);
  run([...common, 'advance', '--to', 'DIAGNOSED', '--session-id', SID, '--machine-id', MID]);

  // 3) 计划
  const planPath = join(local, 'plan.json');
  writeFileSync(planPath, JSON.stringify({
    change_scope: r.scope,
    non_goals: r.nongoals,
    verification_plan: r.ver,
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
    planned_change_scope: r.scope,
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
    '--message', `进入开发${r.num}`,
    '--approved-by', 'human:淮政玮',
    '--message-ref', CLAIM_REF,
    '--active-runs', '4',
    '--session-id', SID, '--machine-id', MID,
    '--binding-file', bindingPath]);
  run([...common, 'advance', '--to', 'IMPLEMENTING', '--session-id', SID, '--machine-id', MID]);
  console.log(`=== ${r.num}-${r.id} -> IMPLEMENTING`);
}
console.log('ALL-WAVE2-SETUP-DONE');
