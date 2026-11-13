// 第一波 8 单 ledger 批量推进：CLAIMED -> DIAGNOSED -> READY_DEV -> IMPLEMENTING
// enter_dev 依据：当次会话问卷用户明确选择「启动 A 组第一波 8 单」（2026-11-12 20:03 淮政玮）
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { diagnosisHash, sha256 } from '../../../.cursor/skills/feishu-bugfix/scripts/bugflow-state.mjs';

const SCRIPT = new URL('.', import.meta.url).pathname.replace(/^\/(\w):/, '$1:\\') + '..\\..\\..\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const ROOT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs';
const SID = 'cursor-20261112-2007-batch-a';
const MID = 'redfo-win';
const BASE_SHA = '56bfafe9afc3a6f5113b3fd1401d36fb0882e793';
const REMOTE = 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git';
const TRIAGE = 'gkx-orchestration/agent-delivery/bugfix-runs/_triage-20261112/triage-report.md';

const RUNS = [
  {
    num: '002', id: '7167107397', risk: 'S', branch: 'fix/7167107397-export-format',
    symptom: '政策分析报告可视化呈现页点「导出Excel」，实际导出的文件是 word 格式',
    root: 'analysis/index.vue confirmExportReport() 用三元映射 exportFormat.value === "pdf" ? "pdf" : "word"，把 excel 选项吞成 word',
    scope: ['src/views/policy/analysis/index.vue', 'src/views/policy/analysis/ReportTemplateExport.vue', 'src/views/policy/analysis/policyReportExport.ts'],
    refs: ['feishu:6a687a81e231818dec771f9a#7167107397 描述（报告人黄敬洲 2026-11-12 19:13）', `${TRIAGE}#A组-002`],
    impacts: ['政策分析评价-报告导出弹窗与导出链路', 'Excel 格式真实可用性（查证后定修法：支持则真导 excel，不支持则下线假选项）'],
    nongoals: ['不新增导出格式种类', '不改 word/pdf 导出行为'],
    ver: ['node 自检脚本断言 excel 分支映射正确或 excel 选项已下线', '合并前 vue-tsc 全量类型门', '提测后 dev 部署 chunk grep 导出入口'],
  },
  {
    num: '003', id: '7167153701', risk: 'S', branch: 'fix/7167153701-related-link',
    symptom: '结果解读报告多维展示-诊断详情-「查看关联（演示）」按钮点击无反应；文案含开发期「（演示）」字样',
    root: 'HotIssueDiagnosisBoard.vue 的 a-button 未绑定任何 @click 处理器，纯静态按钮；文案硬编码「（演示）」',
    scope: ['src/views/policy/analysis/interpret/HotIssueDiagnosisBoard.vue'],
    refs: ['feishu:6a687a81e231818dec771f9a#7167153701 描述（报告人黄敬洲 2026-11-12 19:04）', `${TRIAGE}#A组-003`],
    impacts: ['诊断详情关联入口交互', '用户可见文案（去演示字样）'],
    nongoals: ['不伪造关联数据（无数据则诚实空态）', '不改其他 interpret 组件'],
    ver: ['node 自检脚本断言按钮文案无「（演示）」且模板含 @click 绑定', '合并前 vue-tsc 全量类型门', '提测后 dev 部署 chunk grep 按钮文案'],
  },
  {
    num: '004', id: '7166906229', risk: 'S', branch: 'fix/7166906229-toast-copy',
    symptom: '政策舆情评估多处提示框/Toast 暴露开发过程任务细节（jobId、等待秒数、超时阈值、任务状态枚举）',
    root: 'SentimentTab.vue matchStatusText() 与 sentimentLive.ts jobErrMsg 硬编码开发话术（含 ads.policy_match 表名、任务受理内部细节）',
    scope: ['src/views/policy/panorama/components/SentimentTab.vue', 'src/views/policy/panorama/sentimentLive.ts'],
    refs: ['feishu:6a687a81e231818dec771f9a#7166906229 描述（报告人黄敬洲 2026-11-12 15:37）', `${TRIAGE}#A组-004`],
    impacts: ['舆情评估任务进行中/失败/超时提示文案', '用户可见空态文案'],
    nongoals: ['不改任务轮询与状态机逻辑', '不动 D9 评审层 Mock 角标', '不伪造任务成功态'],
    ver: ['node 自检脚本断言用户可见字符串不含 jobId/ads./policy_match 等内部词', '合并前 vue-tsc 全量类型门', '提测后 dev 部署 chunk grep 文案'],
  },
  {
    num: '005', id: '7166930830', risk: 'S', branch: 'fix/7166906229-toast-copy',
    symptom: '政策匹配与推送存在开发逻辑文案；主体显示 E0001 类 code 而非名称',
    root: 'SentimentTab.vue 硬编码表名话术；mapMatchRows 只映射 subject_id 未映射主体名称，模板直出 subjectId',
    scope: ['src/views/policy/panorama/components/SentimentTab.vue', 'src/views/policy/panorama/sentimentLive.ts'],
    refs: ['feishu:6a687a81e231818dec771f9a#7166930830 描述（报告人黄敬洲 2026-11-12 16:25）', `${TRIAGE}#A组-005`, '已验收同口径先例：bugfix-runs/001-7164904200（code 显示 name）'],
    impacts: ['匹配候选/匹配结果空态与主体名称展示'],
    nongoals: ['不伪造匹配分数', '不改 ads.policy_match 数据链路'],
    ver: ['node 自检脚本断言无表名话术且 subjectOptions 反查返回名称', '合并前 vue-tsc 全量类型门', '提测后 dev 部署 chunk grep 主体名称'],
  },
  {
    num: '006', id: '7167087763', risk: 'S', branch: 'fix/7167107397-export-format',
    symptom: '政策分析报告导出（pdf/word）里图表无内容；「周期」字段显示 3y 类 code 而非中文标题',
    root: 'exportAnalysisTemplateReport 导出时未收集页面 ECharts 实例转 PNG 传入模板；period 无 code→标题映射',
    scope: ['src/views/policy/analysis/ReportTemplateExport.vue', 'src/views/policy/analysis/policyReportExport.ts'],
    refs: ['feishu:6a687a81e231818dec771f9a#7167087763 描述（报告人黄敬洲 2026-11-12 18:51）', `${TRIAGE}#A组-006`],
    impacts: ['分析报告导出文档图表完整性', '周期字段中文化'],
    nongoals: ['不改变页面在线图表渲染', '不新增导出格式'],
    ver: ['node 自检脚本断言导出链路带图表 PNG 且 period 映射命中', '合并前 vue-tsc 全量类型门', '提测后 dev 导出产物人工抽验'],
  },
  {
    num: '007', id: '7166817412', risk: 'S', branch: 'fix/7167107397-export-format',
    symptom: '政策新旧对比导出 pdf/word 图表均无数据；word 中图表尺寸过大',
    root: 'VersionCompareModal.vue onExport 时 chartOption 为 null（取图时机早于渲染）；policyReportExport.ts Word 插图 900x420+max-width:100% 无页宽约束',
    scope: ['src/views/policy/panorama/components/VersionCompareModal.vue', 'src/views/policy/panorama/policyReportExport.ts'],
    refs: ['feishu:6a687a81e231818dec771f9a#7166817412 描述（报告人黄敬洲 2026-11-12 16:37）', `${TRIAGE}#A组-007`],
    impacts: ['新旧对比导出文档图表完整性', 'word 插图尺寸（A4 可用宽度定宽）'],
    nongoals: ['不改在线弹窗图表渲染', '不动对比数据逻辑'],
    ver: ['node 自检脚本断言导出兜底取图逻辑存在且插图样式带定宽', '合并前 vue-tsc 全量类型门', '提测后 dev 导出产物人工抽验'],
  },
  {
    num: '008', id: '7166059325', risk: 'M', branch: 'fix/7166059325-industry-state',
    symptom: '行业领域复选框状态不稳定：选项上屏但勾选态未勾上（频繁偶发）；同级第二个选不中',
    root: '三因叠加：value 归一化不一致（label/code 双路径，未知 id 静默丢路径）+ IndustrySelect onOptionLabelClick 用 checkbox.click() DOM 合成点击与受控 value 时序竞争 + collapseIndustrySelectParents 折叠规则吞同级项',
    scope: ['src/views/situation/global-innovation/components/IndustrySelect.vue', 'src/lib/industryCluster/resolve.ts', 'src/views/policy/panorama/search/displayPolicySearchConfig.ts', 'src/views/policy/panorama/index.vue'],
    refs: ['feishu:6a687a81e231818dec771f9a#7166059325 描述（报告人黄敬洲 2026-11-11 18:14）', `${TRIAGE}#A组-008`],
    impacts: ['行业复选框受控状态归一（situation/global-innovation 与 policy/panorama 两处消费方）'],
    nongoals: ['不改组件对外 props 契约（除非归一化必须并在 commit 说明）', '不动选项树数据'],
    ver: ['node 自检脚本断言：未知 label 不丢路径/同级两项共存/单值回灌命中树内 code', '合并前 vue-tsc 全量类型门', '两处消费方页面回归走查（提测后 dev）'],
  },
  {
    num: '009', id: '7167234520', risk: 'M', branch: 'fix/7167153701-related-link',
    symptom: '政策分析评价弦线图实际呈现为关系图（ECharts type:graph circular layout），非弦图形态',
    root: 'StructureLinkPanel.vue 图表 option 用 graph 系列顶替弦图呈现',
    scope: ['src/views/policy/analysis/StructureLinkPanel.vue'],
    refs: ['feishu:6a687a81e231818dec771f9a#7167234520 描述（报告人黄敬洲 2026-11-12 18:39）', `${TRIAGE}#A组-009`],
    impacts: ['弦线图图表类型呈现（echarts 仓内能力内实现，不新增依赖）'],
    nongoals: ['效果传导路径无数据属数据侧缺口，本单不修（保留诚实空态）', '不新增 npm 依赖'],
    ver: ['node 自检脚本断言 option 不再输出 type:graph（输出选定目标类型）', '合并前 vue-tsc 全量类型门', '提测后 dev 页面图表人工抽验'],
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
    '--message-ref', 'questionnaire:启动A组第一波8单(2026-11-12问卷选项)',
    '--active-runs', '8',
    '--session-id', SID, '--machine-id', MID,
    '--binding-file', bindingPath]);
  run([...common, 'advance', '--to', 'IMPLEMENTING', '--session-id', SID, '--machine-id', MID]);
  console.log(`=== ${r.num}-${r.id} -> IMPLEMENTING`);
}
console.log('ALL-WAVE1-SETUP-DONE');
