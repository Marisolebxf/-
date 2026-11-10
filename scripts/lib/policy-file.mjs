/**
 * Dependency-free parser and matcher for the constrained bug-fix policy YAML.
 * It intentionally supports only the small YAML subset used in policies/*.yaml:
 * nested maps, scalar arrays, inline arrays, booleans, null and numbers.
 */
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

function stripComment(line) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith('#')) return null;
  return line;
}

function splitKeyValue(text) {
  let quote = null;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if ((ch === '"' || ch === "'") && text[i - 1] !== '\\') {
      quote = quote === ch ? null : quote ?? ch;
    }
    if (ch === ':' && !quote) return [text.slice(0, i).trim(), text.slice(i + 1).trim()];
  }
  return null;
}

function parseScalar(text) {
  const value = text.trim();
  if (value === '' ) return '';
  if (value === 'null' || value === '~') return null;
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (/^-?\d+(?:\.\d+)?$/.test(value)) return Number(value);
  if (value.startsWith('[') && value.endsWith(']')) {
    const inner = value.slice(1, -1).trim();
    if (!inner) return [];
    const parts = [];
    let start = 0;
    let quote = null;
    for (let i = 0; i < inner.length; i += 1) {
      const ch = inner[i];
      if ((ch === '"' || ch === "'") && inner[i - 1] !== '\\') quote = quote === ch ? null : quote ?? ch;
      if (ch === ',' && !quote) {
        parts.push(inner.slice(start, i).trim());
        start = i + 1;
      }
    }
    parts.push(inner.slice(start).trim());
    return parts.map(parseScalar);
  }
  if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1).replace(/\\n/g, '\n');
  }
  return value;
}

function parseBlock(lines, start, indent) {
  if (start >= lines.length) return [null, start];
  const isArray = lines[start].indent === indent && lines[start].text.startsWith('-');
  if (isArray) {
    const result = [];
    let i = start;
    while (i < lines.length && lines[i].indent === indent && lines[i].text.startsWith('-')) {
      const rest = lines[i].text.slice(1).trim();
      if (!rest) {
        const childIndent = lines[i + 1]?.indent;
        if (childIndent == null || childIndent <= indent) throw new Error(`YAML array item at line ${lines[i].line} has no child`);
        const [child, next] = parseBlock(lines, i + 1, childIndent);
        result.push(child);
        i = next;
      } else {
        const kv = splitKeyValue(rest);
        if (kv) {
          const item = {};
          item[kv[0]] = parseScalar(kv[1]);
          i += 1;
          while (i < lines.length && lines[i].indent > indent) {
            const nestedKv = splitKeyValue(lines[i].text);
            if (!nestedKv) throw new Error(`YAML map-only array item expected at line ${lines[i].line}`);
            if (nestedKv[1]) item[nestedKv[0]] = parseScalar(nestedKv[1]);
            else {
              const childIndent = lines[i + 1]?.indent;
              if (childIndent == null || childIndent <= lines[i].indent) item[nestedKv[0]] = {};
              else {
                const [child, next] = parseBlock(lines, i + 1, childIndent);
                item[nestedKv[0]] = child;
                i = next - 1;
              }
            }
            i += 1;
          }
          result.push(item);
        } else {
          result.push(parseScalar(rest));
          i += 1;
        }
      }
    }
    return [result, i];
  }

  const result = {};
  let i = start;
  while (i < lines.length && lines[i].indent === indent) {
    const kv = splitKeyValue(lines[i].text);
    if (!kv) throw new Error(`YAML mapping entry expected at line ${lines[i].line}`);
    const [key, rawValue] = kv;
    if (rawValue === '|' || rawValue === '>') {
      const childIndent = lines[i + 1]?.indent;
      if (childIndent == null || childIndent <= indent) throw new Error(`YAML block scalar at line ${lines[i].line} has no content`);
      const chunks = [];
      i += 1;
      while (i < lines.length && lines[i].indent > indent) {
        chunks.push(lines[i].text);
        i += 1;
      }
      result[key] = chunks.join(rawValue === '|' ? '\n' : ' ');
      continue;
    }
    if (rawValue) {
      result[key] = parseScalar(rawValue);
      i += 1;
      continue;
    }
    const childIndent = lines[i + 1]?.indent;
    if (childIndent == null || childIndent <= indent) {
      result[key] = {};
      i += 1;
    } else {
      const [child, next] = parseBlock(lines, i + 1, childIndent);
      result[key] = child;
      i = next;
    }
  }
  return [result, i];
}

export function parseConstrainedYaml(text) {
  const lines = [];
  for (const [index, raw] of text.split(/\r?\n/).entries()) {
    const withoutComment = stripComment(raw);
    if (withoutComment == null) continue;
    const indent = withoutComment.match(/^\s*/)[0].replace(/\t/g, '  ').length;
    lines.push({ line: index + 1, indent, text: withoutComment.slice(indent) });
  }
  if (!lines.length) return {};
  const [value, consumed] = parseBlock(lines, 0, lines[0].indent);
  if (consumed !== lines.length) throw new Error(`Unexpected YAML content at line ${lines[consumed].line}`);
  return value;
}

export function stableJson(value) {
  if (Array.isArray(value)) return value.map(stableJson);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stableJson(value[key])]));
  }
  return value;
}

export function policyHash(policy) {
  return `sha256:${createHash('sha256').update(JSON.stringify(stableJson(policy)), 'utf8').digest('hex')}`;
}

export function loadPolicy(policyVersion, policiesRoot) {
  const file = resolve(policiesRoot, `${policyVersion}.yaml`);
  if (!existsSync(file)) throw new Error(`POLICY_NOT_FOUND: ${file}`);
  const text = readFileSync(file, 'utf8');
  const policy = parseConstrainedYaml(text);
  return { file, text, policy, policy_hash: policyHash(policy) };
}

export function validatePolicy(policy, now = new Date()) {
  const errors = [];
  if (policy.schema_version !== 1) errors.push('policy.schema_version must be 1');
  if (!['active-demo', 'production'].includes(policy.status)) errors.push('policy.status must be active-demo or production');
  if (policy.default_decision !== 'deny') errors.push('policy.default_decision must be deny');
  if (policy.database_is_schema !== true) errors.push('policy.database_is_schema must be true');
  const approvalRef = policy.owner_decision?.approval_ref;
  if (typeof approvalRef !== 'string' || !approvalRef.trim()) errors.push('policy.owner_decision.approval_ref is required');
  if (typeof policy.owner_decision?.decided_by !== 'string' || !policy.owner_decision.decided_by.startsWith('human:')) {
    errors.push('policy.owner_decision.decided_by must start with human:');
  }
  if (typeof policy.owner_decision?.approval_source !== 'string' || !policy.owner_decision.approval_source.trim()) {
    errors.push('policy.owner_decision.approval_source is required');
  }
  const expiresAt = policy.owner_decision?.expires_at;
  if (!expiresAt) {
    errors.push('policy.owner_decision.expires_at is required');
  } else {
    const expires = new Date(expiresAt);
    if (Number.isNaN(expires.getTime())) errors.push('policy.owner_decision.expires_at must be an ISO date-time');
    else if (now > expires) errors.push(`policy expired at ${expiresAt}`);
  }
  const reviewAt = policy.owner_decision?.review_at;
  if (!reviewAt) {
    errors.push('policy.owner_decision.review_at is required');
  } else {
    const review = new Date(reviewAt);
    if (Number.isNaN(review.getTime())) errors.push('policy.owner_decision.review_at must be a date');
  }
  return errors;
}

function tableMatchesGroup(table, group) {
  if (!group || typeof group !== 'object' || group.status === 'disabled') return false;
  if (group.environment && table.environment !== group.environment) return false;
  if (group.database && table.database !== group.database) return false;
  if (group.schema && table.schema !== group.schema) return false;
  if (Array.isArray(group.databases) && !group.databases.includes(table.database)) return false;
  if (Array.isArray(group.schemas) && !group.schemas.includes(table.schema)) return false;
  if (group.table_prefix && !table.table.startsWith(group.table_prefix)) return false;
  return true;
}

export function matchTableToPolicy(policy, table) {
  const groups = Object.entries(policy.allowed ?? {});
  const matched = groups.filter(([, group]) => tableMatchesGroup(table, group));
  if (!matched.length) return { ok: false, reason: 'no base policy group matched' };
  if (matched.length > 1) return { ok: false, reason: `multiple base policy groups matched: ${matched.map(([name]) => name).join(', ')}` };
  const [groupName, group] = matched[0];
  if (group.table_policy !== 'run_scope_required') return { ok: false, reason: `${groupName} requires run_scope_required` };
  if (group.access === 'application_only' && table.access_mode !== 'application_only') {
    return { ok: false, reason: `${groupName} only allows application_only access` };
  }
  return { ok: true, group: groupName };
}
