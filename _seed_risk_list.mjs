import fs from 'node:fs';
import path from 'node:path';

const ORCH = process.cwd();
const SIGN = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-签收草表.md');
const OUT = path.join(ORCH, 'agent-delivery/metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-T3高风险清单.md');

const text = fs.readFileSync(SIGN, 'utf8');
const lines = text.split(/\r?\n/);

let inT3 = false;
const rows = [];
for (const line of lines) {
  if (line.startsWith('## T3')) { inT3 = true; continue; }
  if (inT3 && line.startsWith('## ')) break;
  if (!inT3) continue;
  const m = line.match(/^\|\s*\d+\s*\|\s*`([^`]+)`\s*\|\s*(\w+)\s*\|([^|]*)\|([^|]*)\|\s*(\w+)\s*\|/);
  if (!m) continue;
  rows.push({ id: m[1], domain: m[2], name: m[3].trim(), formula: m[4].trim(), type: m[5] });
}

const risk = rows.filter((r) => /pending_cosign|pending_algorithm|pending_data_lead|未签|待会签|待定|待补/.test(r.formula));
risk.sort((a, b) => a.domain.localeCompare(b.domain) || a.id.localeCompare(b.id));

const L = [];
L.push('# ALGO-LIB-SEED-TYPE-L01 · T3 高风险清单');
L.push('');
L.push(`> 供 \`human:唐绍祖\` 事后抽查。共 **${risk.length}** 条（T3 共 ${rows.length} 条中的 formula 占位符项）。`);
L.push('> 这些指标的 formula 是 `pending_*` / 未签占位，机器初判 type 主要靠中文名，是 522 条里最可能误判的部分。');
L.push('> 初判 type 已按「全部采纳」回填进 seed；抽查后如需更正，告诉我改哪条即可。');
L.push('');
L.push('| # | metric_id | domain | 中文名 | 初判 type | formula(截断) |');
L.push('|---|---|---|---|---|---|');
let n = 0;
for (const r of risk) {
  n++;
  L.push(`| ${n} | \`${r.id}\` | ${r.domain} | ${r.name.replace(/\|/g, '/')} | ${r.type} | ${r.formula.replace(/\|/g, '/')} |`);
}
L.push('');
const domDist = {};
for (const r of risk) domDist[r.domain] = (domDist[r.domain] || 0) + 1;
L.push('## 分布');
L.push('');
L.push('| domain | 条数 |');
L.push('|---|---|');
for (const [d, c] of Object.entries(domDist).sort((a, b) => b[1] - a[1])) L.push(`| ${d} | ${c} |`);

fs.writeFileSync(OUT, L.join('\n'), 'utf8');
console.log('T3 total:', rows.length, '| risk(占位符):', risk.length);
console.log('domain dist:', JSON.stringify(domDist));
console.log('WROTE', OUT);
