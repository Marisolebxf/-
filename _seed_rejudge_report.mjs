import fs from 'node:fs';
import path from 'node:path';

const ORCH = process.cwd();
const DIR = path.join(ORCH, 'agent-delivery/metrics/request/_work/rejudge');
const MERGED = path.join(DIR, '_merged.changes.json');
const OUT = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-rejudge-修正清单.md');

const changes = JSON.parse(fs.readFileSync(MERGED, 'utf8'));

// group by domain (keep order)
const domOrder = ['CHAIN', 'INNOV', 'ENT', 'SYNTH', 'SVC', 'TECH', 'POLICY', 'TALENT', 'ORG', 'COMMON', 'TNIE'];
const byDomain = new Map();
for (const c of changes) {
  if (!byDomain.has(c.domain)) byDomain.set(c.domain, []);
  byDomain.get(c.domain).push(c);
}

// from->to distribution
const ft = {};
for (const c of changes) {
  const k = `${c.from}→${c.to}`;
  ft[k] = (ft[k] || 0) + 1;
}

const L = [];
L.push('# ALGO-LIB-SEED-TYPE-L01 · §2.1 重判修正清单');
L.push('');
L.push(`> 由 \`algorithm-agent\` 按《给人说明-指标与算法工作类型与流程梳理.md》§2.1 枚举表，对 522 条已回填指标中 T2+T3（431 条）逐条重判。`);
L.push(`> T1（11）+ TTEMP（90）= 101 条 A1 表2 已签，**一律保持不动**。`);
L.push(`> 共修正 **${changes.length}** 条，已回填进 seed。`);
L.push('');
L.push('## 一、判断标准（§2.1 轴 A 映射）');
L.push('');
L.push('| algorithm.type | 计算本质信号 | 本次重判应用 |');
L.push('|---|---|---|');
L.push('| STAT | 计数 COUNT/SUM/AVG/MAX/GROUP BY/DISTINCT、占比 A/B、环比、排名 RANK、简单取数 SELECT | 把「XX数/占比/排名/取最新值」从 MODEL 改回 |');
L.push('| COMPUTE | 有公式无模型：纯加权 w1+w2+w3、标准化、阈值分档、固定指数公式(HHI/熵/区位熵) | 把「纯加权指数/评分」从 MODEL 改回 |');
L.push('| MODEL | 评分模型(多维+归一化/等级/排名)、预测、聚类、匹配适配、识别/抽取(NLP)、推荐 | 保留真模型 |');
L.push('| GRAPH | 中心性、路径、子图、边权、实体识别/关系抽取 | 补「关键节点重要性/网络密度」等图算法 |');
L.push('| MIXED | 上列多类组合(如贡献度模型+影响路径) | 补「多维排名/竞争情报比对/贡献度+路径」 |');
L.push('| third_party | 外采 API / G3 Job / LLM | 未改动 |');
L.push('');
L.push('## 二、改动分布');
L.push('');
L.push('| from→to | 条数 | 说明 |');
L.push('|---|---|---|');
for (const [k, v] of Object.entries(ft).sort((a, b) => b[1] - a[1])) {
  const desc = {
    'MODEL→STAT': '计数/占比/排名/取数被误判为模型',
    'MODEL→COMPUTE': '纯加权指数/评分 → 加权计算',
    'MODEL→GRAPH': '关键节点重要性 = 图算法',
    'MODEL→MIXED': '多维排名/竞争情报比对',
    'STAT→COMPUTE': '加权被误判为占比',
    'GRAPH→STAT': 'SELECT/COUNT 被误判为图',
    'GRAPH→COMPUTE': '招引/培育评分 demo 路径',
    'GRAPH→MIXED': '贡献度 + 影响路径',
    'COMPUTE→STAT': '归一化+COUNT 本质计数',
  }[k] || '';
  L.push(`| ${k} | ${v} | ${desc} |`);
}
L.push('');
L.push('## 三、逐条清单');
L.push('');
for (const d of domOrder) {
  const arr = byDomain.get(d);
  if (!arr || !arr.length) continue;
  L.push(`### ${d}（${arr.length} 条）`);
  L.push('');
  L.push('| # | metric_id | from | to | 理由 |');
  L.push('|---|---|---|---|---|');
  let n = 0;
  for (const c of arr) {
    n++;
    L.push(`| ${n} | \`${c.id}\` | ${c.from} | ${c.to} | ${c.reason} |`);
  }
  L.push('');
}

// key decision points
L.push('## 四、需淮政玮/唐绍祖确认的决策点');
L.push('');
L.push('1. **COMPUTE 边界（本次最大变化，30 条 MODEL→COMPUTE）**：§2.1 把「加权、标准化、阈值」明确归 COMPUTE（有公式但无模型）。因此把「纯加权合成指数」（如 `科研实力指数 = 专利密度*w1+论文密度*w2+高校*w3`）从 MODEL 改回 COMPUTE。');
L.push('   - 区分标尺：**纯线性加权（w1+w2+w3，无归一化/等级/排名/主成分）→ COMPUTE；含归一化/等级/排名/主成分/预测/聚类 → MODEL**。');
L.push('   - 佐证：赋号卡 `M_ORG_ATTENTION_TREND` 也明确「指数合成（无训练）→ COMPUTE」；A1 表2 的正式 M_ENT_* 多维加权（如 `COMPETITIVENESS_SCORE` 四维加权+极值归一化）仍是 MODEL。');
L.push('   - 注意：A1 已签的 101 条（含 TTEMP 90 + T1 11）**未动**，其中若存在「无归一化的纯加权」被判 MODEL（如 `M_ENT_TECH_POWER_SCORE` 五维加权平均）属 A1 历史口径，不在本次重判范围，可另议。');
L.push('');
L.push('2. **排名归 STAT**：§2.1 明确 STAT 含「排名」，故 `RANK() OVER ORDER BY` 类（如 `M_ENT_TECH_RANK`、`M_SYNTH_ELEM_RANK`）从 MODEL 改 STAT。');
L.push('');
L.push('3. **关键节点重要性/节点优先级 → GRAPH**：属图节点重要性（PageRank/中心性），非评分模型，从 MODEL 改 GRAPH。');

fs.writeFileSync(OUT, L.join('\n'), 'utf8');
console.log('WROTE', OUT);
console.log('total changes:', changes.length);
