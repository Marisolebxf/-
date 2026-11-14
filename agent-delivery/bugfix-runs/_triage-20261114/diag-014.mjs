// 014 diag v2：record-diagnosis 走 --input-json（readInput 只认 input-file/input-json）
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const TRIAGE = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\_triage-20261114';
const RUN_DIR = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\014-7168131856';

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
const file = join(TRIAGE, 'diag-014.json');
writeFileSync(file, JSON.stringify(diag, null, 2), 'utf8');
execFileSync('node', [SCRIPT, 'record-diagnosis', '--run-dir', RUN_DIR, '--input-file', file], { stdio: 'inherit' });
console.log('DIAG-014-DONE');
