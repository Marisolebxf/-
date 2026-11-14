// 014 初始化 v2：init 走 --input-json（CLI 标量参数不含 diagnose），diagnose 走 --input-file
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const TRIAGE = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\_triage-20261114';
const RUN_DIR = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\014-7168131856';
const SID = 'cursor-20261114-1317-batch-a';
const MID = 'redfo-win';

function run(args) {
  execFileSync('node', [SCRIPT, ...args], { stdio: 'inherit' });
}

const initPayload = {
  phase: 'CLAIMED',
  'auto-number': '014',
  'work-item-id': '7168131856',
  title: '政策效果推演-新出台政策效果预测，历史政策效果，短期和长期效果，没有数据',
  'claim-id': SID,
  'claim-comment-ref': 'feishu-comment:2026111413205194246AA978F6E6C4D3F8 ([agent-claim] 014)',
  'claim-operator': 'agent:coordinator-agent(human:淮政玮)',
  'project-key': '6a687a81e231818dec771f9a',
  owner: 'human:淮政玮',
  risk: 'M',
  'session-id': SID,
  'machine-id': MID,
};
writeFileSync(join(TRIAGE, 'init-014.json'), JSON.stringify(initPayload, null, 2), 'utf8');
run(['init', '--run-dir', RUN_DIR, '--input-file', join(TRIAGE, 'init-014.json')]);

const diag = {
  symptom: '政策效果推演：新出台政策效果预测、历史政策效果板块的短期/长期效果无数据（P1，工单仅截图无步骤）',
  reproduction: [
    '打开 政策效果推演 页（src/views/policy/simulation）',
    '新出台政策效果预测 / 历史政策效果：执行推演后查看短中长期效果区块',
    '现象：短期与长期效果无数据（截图 2026-11-13 工单附件）',
  ],
  root_cause: '待分诊：候选=live 接口链未回填 term_kpi_text / 前端取数字段错位 / 数据源未接入(D3/D4)；优先核 EstimateWorkbench.vue 取数与 /display/v1/policy/simulation/jobs kind 链路',
  counter_evidence: [],
  requirement_refs: ['POL-L2-DS12-WIRING-L01'],
  impact_scope: ['src/views/policy/simulation/estimate/EstimateWorkbench.vue', 'src/api/policySimulation.ts', 'src/views/policy/simulation/simulationLive.mjs'],
};
writeFileSync(join(TRIAGE, 'diag-014.json'), JSON.stringify(diag, null, 2), 'utf8');
run(['record-diagnosis', '--run-dir', RUN_DIR, '--input-file', join(TRIAGE, 'diag-014.json')]);
console.log('INIT-014-DONE');
