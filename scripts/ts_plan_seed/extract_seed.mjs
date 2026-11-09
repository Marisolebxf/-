#!/usr/bin/env node
/**
 * TS-L2-DS09-SEED-L01 · 种子提取脚本（OV-DATAFLOW-01 的「种子提取脚本」节点）
 *
 * 以 export 实位为准 import 两个事实源，dump 为 seed_dump.json 供 seed_ts_plan.py 消费：
 *   1. lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts（node ≥22 原生 strip-types；
 *      文件头部注释行号陈旧，不依赖行号，只认 export 实位）
 *   2. demo-ui-science/src/techDevelopmentPlan.js（时间轴/点位两块；经其自有
 *      buildTechDevelopmentPlanDataset 投影取 timeline / records / mapRegions / legend，
 *      空筛选下 scaleRecordsByFieldScope share=1 原样返回，records 逐字不缩放）
 *   3. ResearchTab.vue L38/L53 常量段（目标主体/研究领域五选项）正则读取
 *
 * demo-ui-science 内部存在 vite 风格无扩展名目录导入（./lib/industryCluster），
 * 注册 module.registerHooks resolve 钩子补 .ts/.js/index 解析。
 * 只读事实源，不写任何仓内文件；输出仅落本目录 seed_dump.json（生成物，不入 git）。
 */
import { registerHooks } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const GKX_ROOT = process.env.GKX_ROOT || path.resolve(HERE, '..', '..', '..');

// ---- vite 风格扩展名解析钩子（仅相对说明符；失败回落原逻辑报错） ----
registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier.startsWith('.')) {
      const parentDir = context.parentURL
        ? path.dirname(fileURLToPath(context.parentURL))
        : process.cwd();
      const base = path.resolve(parentDir, specifier);
      const candidates = [
        base + '.ts', base + '.js', base + '.mjs',
        path.join(base, 'index.ts'), path.join(base, 'index.js'),
      ];
      for (const cand of candidates) {
        if (existsSync(cand) && statSync(cand).isFile()) {
          // 不指定 format：.ts 交由 node 原生 strip-types 判定，强制 module 会关闭类型剥离
          return { url: pathToFileURL(cand).href, shortCircuit: true };
        }
      }
    }
    return nextResolve(specifier, context);
  },
});

const MOCK_URL = pathToFileURL(
  path.join(GKX_ROOT, 'repos', 'lumen-ui-science-pc', 'src', 'mock', 'modules', 'techDevelopmentPlan.ts'),
).href;
const DEMO_URL = pathToFileURL(
  path.join(GKX_ROOT, 'repos', 'demo-ui-science', 'src', 'techDevelopmentPlan.js'),
).href;
const RESEARCH_TAB = path.join(
  GKX_ROOT, 'repos', 'lumen-ui-science-pc', 'src', 'views', 'situation',
  'tech-development-plan', 'tabs', 'ResearchTab.vue',
);

const mock = await import(MOCK_URL);
const demo = await import(DEMO_URL);
// overlapTimeScopeFactor 非独立 export，藏在 dataset 聚合里（mock L601）——经工厂函数原样取
const mockDataset = mock.createTechDevelopmentPlanDataset();

// ---- ResearchTab.vue 常量段（正则，逐字） ----
const tabSrc = readFileSync(RESEARCH_TAB, 'utf8');
const fieldMatch = tabSrc.match(/const RESEARCH_FIELD_OPTIONS = \[([^\]]*)\]/);
if (!fieldMatch) throw new Error('RESEARCH_FIELD_OPTIONS 未在 ResearchTab.vue 找到');
const researchFieldOptions = [...fieldMatch[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
const targetMatch = tabSrc.match(/targetSubject:\s*'([^']+)'/);
if (!targetMatch) throw new Error('targetSubject 未在 ResearchTab.vue 找到');
const targetSubject = targetMatch[1];

// ---- demo.js 投影（timeline / planRecords / regionCoordinates / legend） ----
const ds = demo.buildTechDevelopmentPlanDataset({});
const timeline = ds.timeline; // title/currentYear/rangeLabel/years/events（demo 默认 2020-2026）
const planRecords = ds.records.map((r) => ({
  id: r.id, name: r.name, region: r.region, year: r.year, score: r.score,
}));
const mapRegions = ds.mapRegions.map((m) => ({
  // position=[lat,lng]（demo regionCoordinates），name=区域名，layerKeys=5 图层
  name: m.name, position: m.position, layerKeys: m.layerKeys,
  source_id: m.detail.id, score: m.detail.score,
}));
const legendResultTypes = demo.techDevelopmentPlanLegend.resultTypes.map((r) => r.key);

const dump = {
  _meta: {
    extracted_at: new Date().toISOString(),
    gkx_root: GKX_ROOT,
    mock: 'repos/lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts (export 实位)',
    demo: 'repos/demo-ui-science/src/techDevelopmentPlan.js (buildTechDevelopmentPlanDataset 投影)',
    research_tab: 'ResearchTab.vue L38/L53 常量段',
  },
  // ---- OV ----
  hotTechData: mock.hotTechData,
  technologyTrendSpaceRegions: mock.technologyTrendSpaceRegions,
  technologyTrendSeriesByRange: mock.technologyTrendSeriesByRange,
  technologyHeatTrendDefinition: mock.technologyHeatTrendDefinition,
  multidimensionalIndicatorCategories: mock.multidimensionalIndicatorCategories,
  localAdvantageChart: mock.localAdvantageChart,
  localAdvantageInnovation: mock.localAdvantageInnovation,
  localAdvantageOutput: mock.localAdvantageOutput,
  talentFlowData: mock.talentFlowData,
  talentInstitutionFlowRows: mock.talentInstitutionFlowRows,
  talentDirectionNodes: mock.talentDirectionNodes,
  // ---- OV tracking（demo.js） ----
  timeline, planRecords, mapRegions, legendResultTypes,
  // ---- KEY ----
  carrierTypes: mock.carrierTypes,
  carrierLocations: mock.carrierLocations,
  industryClusters: mock.industryClusters,
  districtCarrierBaselines: mock.districtCarrierBaselines,
  landUseData: mock.landUseData,
  keyAreaScenarioPlans: mock.keyAreaScenarioPlans,
  keyAreaCompetitivenessMetrics: mock.keyAreaCompetitivenessMetrics,
  keyAreaDimensionScores: mock.keyAreaDimensionScores,
  keyAreaBenchmarkRows: mock.keyAreaBenchmarkRows,
  // ---- RES ----
  researchFieldOptions, targetSubject,
  companies: mock.companies,
  overlapMatrix: mock.overlapMatrix,
  overlapRuleProfiles: mock.overlapRuleProfiles,
  overlapTimeScopeFactor: mockDataset.overlapTimeScopeFactor,
  researchLevelCards: mock.researchLevelCards,
  researchOverlapBenchmarks: mock.researchOverlapBenchmarks,
  researchGraphNodes: mock.researchGraphNodes,
  regionalPlanningInsightRows: mock.regionalPlanningInsightRows,
};

const out = path.join(HERE, 'seed_dump.json');
writeFileSync(out, JSON.stringify(dump, null, 1) + '\n', 'utf8');

// ---- 提取期自检（行源漂移即失败，禁止带病进灌数） ----
const checks = [
  ['hotTechData', mock.hotTechData.length === 8],
  ['series ranges', ['3m', '6m', '12m'].every((k) => k in mock.technologyTrendSeriesByRange)],
  ['indicator categories', mock.multidimensionalIndicatorCategories.length === 7],
  ['timeline events', timeline.events.length === 7],
  ['timeline meta', timeline.title === '科技发展规划研判演进' && timeline.currentYear === '2026'
    && timeline.rangeLabel === '2020-2026' && timeline.years.length === 7],
  ['planRecords', planRecords.length === 7 && planRecords[0].id === 'tdp-global-robot'],
  ['mapRegions', mapRegions.length === 7 && mapRegions.every((m) => m.layerKeys.length === 5)],
  ['legendResultTypes', JSON.stringify(legendResultTypes)
    === JSON.stringify(['hotspot', 'space', 'talent', 'report', 'warning'])],
  ['localAdvantage x3', [mock.localAdvantageChart, mock.localAdvantageInnovation, mock.localAdvantageOutput]
    .every((b) => b.yAxis.length === 6 && b.local.length === 6 && b.globalAvg.length === 6)],
  ['talentDirectionNodes', mock.talentDirectionNodes.length === 6],
  ['talentInstitutionFlowRows', mock.talentInstitutionFlowRows.length === 5],
  ['talentFlowData', mock.talentFlowData.length === 5],
  ['carrierTypes', mock.carrierTypes.length === 6],
  ['carrierLocations', mock.carrierLocations.length === 22],
  ['industryClusters', mock.industryClusters.length === 3],
  ['districtCarrierBaselines', mock.districtCarrierBaselines.length === 6],
  ['landUseData', mock.landUseData.length === 6],
  ['keyAreaScenarioPlans', mock.keyAreaScenarioPlans.length === 3],
  ['keyAreaCompetitivenessMetrics', mock.keyAreaCompetitivenessMetrics.length === 5],
  ['keyAreaDimensionScores', mock.keyAreaDimensionScores.length === 5],
  ['keyAreaBenchmarkRows', mock.keyAreaBenchmarkRows.length === 5],
  ['researchFieldOptions', JSON.stringify(researchFieldOptions)
    === JSON.stringify(['人工智能', '量子科技', '合成生物学', '集成电路', '新能源'])],
  ['targetSubject', targetSubject === '深圳先进技术研究院'],
  ['companies', mock.companies.length === 6],
  ['overlapMatrix', mock.overlapMatrix.length === 6],
  ['overlapRuleProfiles', mock.overlapRuleProfiles.length === 3],
  ['researchLevelCards', mock.researchLevelCards.length === 4],
  ['researchOverlapBenchmarks', mock.researchOverlapBenchmarks.length === 3],
  ['researchGraphNodes', mock.researchGraphNodes.length === 14],
  ['regionalPlanningInsightRows', mock.regionalPlanningInsightRows.length === 4],
];
const failed = checks.filter(([, ok]) => !ok).map(([name]) => name);
if (failed.length) {
  console.error('EXTRACT SELF-CHECK FAILED:', failed.join(', '));
  process.exit(1);
}
console.log(`seed_dump.json written: ${out}`);
console.log(`self-check OK (${checks.length} checks)`);
