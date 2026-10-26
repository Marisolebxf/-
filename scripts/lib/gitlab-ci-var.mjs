/**
 * GitLab CI/CD variable client.
 * Token comes from gkx-orchestration/.env. Responses never include the value.
 */
import fs from 'node:fs';
import path from 'node:path';

export function parseEnvText(text) {
  const out = {};
  for (const line of String(text).split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx < 1) continue;
    let value = trimmed.slice(idx + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"'))
      || (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    out[trimmed.slice(0, idx).trim()] = value;
  }
  return out;
}

export function loadGitlabEnv(root) {
  const file = path.join(root, '.env');
  if (!fs.existsSync(file)) throw new Error(`missing ${file}`);
  const parsed = parseEnvText(fs.readFileSync(file, 'utf8'));
  if (!parsed.GKX_GITLAB_TOKEN) throw new Error('GKX_GITLAB_TOKEN missing');
  if (!parsed.GKX_GITLAB_BASE) throw new Error('GKX_GITLAB_BASE missing');
  return { token: parsed.GKX_GITLAB_TOKEN, base: parsed.GKX_GITLAB_BASE };
}

export function redact(text, secret) {
  const raw = String(text ?? '');
  if (!secret) return raw.slice(0, 400);
  return raw.split(secret).join('***').slice(0, 400);
}

export function publicVar(variable) {
  const value = typeof variable?.value === 'string' ? variable.value : '';
  return {
    key: variable?.key,
    masked: Boolean(variable?.masked),
    protected: Boolean(variable?.protected),
    raw: Boolean(variable?.raw),
    environment_scope: variable?.environment_scope || '*',
    variable_type: variable?.variable_type || 'env_var',
    value_length: value.length,
  };
}

async function gitlabRequest(env, method, apiPath, body) {
  const fetchImpl = env.fetchImpl || fetch;
  const url = `${env.base.replace(/\/$/, '')}${apiPath}`;
  const headers = { 'PRIVATE-TOKEN': env.token };
  const init = { method, headers };
  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(body);
  }
  const resp = await fetchImpl(url, init);
  const text = await resp.text();
  let data = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }
  if (resp.status < 200 || resp.status >= 300) {
    const secret = body && typeof body.value === 'string' ? body.value : '';
    const msg = redact(typeof data === 'string' ? data : JSON.stringify(data), secret);
    throw new Error(`GitLab ${method} ${apiPath} http=${resp.status} ${msg}`);
  }
  return { status: resp.status, data };
}

export async function resolveProjectId(env, project) {
  const name = String(project || '').trim();
  if (!name) throw new Error('project is required');
  if (/^\d+$/.test(name)) return name;
  const leaf = name.split('/').filter(Boolean).pop();
  const { data } = await gitlabRequest(
    env,
    'GET',
    `/api/v4/projects?search=${encodeURIComponent(leaf)}&simple=true&per_page=100`,
  );
  if (!Array.isArray(data)) throw new Error('GitLab project search failed');
  const hit = data.find((item) => item.path_with_namespace === name);
  if (!hit) {
    const seen = data.map((item) => item.path_with_namespace).filter(Boolean).slice(0, 8).join(', ');
    throw new Error(`project not found: ${name}${seen ? ` (search saw: ${seen})` : ''}`);
  }
  return String(hit.id);
}

export async function listVariables(env, project) {
  const id = await resolveProjectId(env, project);
  const { data } = await gitlabRequest(env, 'GET', `/api/v4/projects/${id}/variables?per_page=100`);
  if (!Array.isArray(data)) throw new Error('GitLab variables response is not a list');
  return {
    project_id: id,
    // ponytail: one page of 100. Upgrade path: follow x-next-page.
    truncated: data.length === 100,
    variables: data.map(publicVar),
  };
}

export async function upsertVariable(env, project, spec) {
  const key = String(spec?.key || '').trim();
  const value = spec?.value;
  if (!key) throw new Error('key is required');
  if (typeof value !== 'string' || value.length === 0) throw new Error('value is required');
  const masked = spec.masked !== false;
  const isProtected = spec.protected === true;
  const raw = spec.raw !== false;
  const environmentScope = spec.environment_scope || '*';
  const id = await resolveProjectId(env, project);
  const listed = await gitlabRequest(env, 'GET', `/api/v4/projects/${id}/variables?per_page=100`);
  const exists = Array.isArray(listed.data) && listed.data.some((item) => item.key === key);
  const payload = {
    value,
    masked,
    protected: isProtected,
    raw,
    variable_type: 'env_var',
    environment_scope: environmentScope,
  };
  if (spec.description) payload.description = String(spec.description);
  let status;
  let data;
  if (exists) {
    payload.filter = { environment_scope: environmentScope };
    const res = await gitlabRequest(
      env,
      'PUT',
      `/api/v4/projects/${id}/variables/${encodeURIComponent(key)}`,
      payload,
    );
    status = res.status;
    data = res.data;
  } else {
    payload.key = key;
    const res = await gitlabRequest(env, 'POST', `/api/v4/projects/${id}/variables`, payload);
    status = res.status;
    data = res.data;
  }
  return {
    action: exists ? 'updated' : 'created',
    http: status,
    project_id: id,
    ...publicVar(data && data.key ? data : { ...payload, key }),
  };
}
