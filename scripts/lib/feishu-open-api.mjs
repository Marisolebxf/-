#!/usr/bin/env node
/**
 * Feishu Open Platform API helpers (tenant token + Bitable record read).
 */

let cachedToken = { value: '', expiresAt: 0 };

export async function feishuTenantToken(appId, appSecret) {
  const now = Date.now();
  if (cachedToken.value && cachedToken.expiresAt > now + 60_000) {
    return cachedToken.value;
  }
  const resp = await fetch(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
    },
  );
  const data = await resp.json();
  if (data.code !== 0 || !data.tenant_access_token) {
    throw new Error(`tenant_access_token failed: ${JSON.stringify(data)}`);
  }
  cachedToken = {
    value: data.tenant_access_token,
    expiresAt: now + (data.expire || 7200) * 1000,
  };
  return cachedToken.value;
}

export async function feishuApi(method, apiPath, token, body) {
  const resp = await fetch(`https://open.feishu.cn/open-apis${apiPath}`, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await resp.json();
  if (data.code !== 0) {
    throw new Error(`Feishu ${method} ${apiPath}: code=${data.code} msg=${data.msg}`);
  }
  return data;
}

export function bitableFieldToString(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string' || typeof value === 'number') return String(value);
  if (Array.isArray(value)) {
    if (!value.length) return '';
    return bitableFieldToString(value[0]);
  }
  if (typeof value === 'object') {
    if (value.text) return String(value.text);
    if (value.name) return String(value.name);
  }
  return String(value);
}

export function bitablePersonToClaim(value, humanPrefix = 'human:', atPrefix = '@') {
  if (value === null || value === undefined) return '';
  let name = '';
  if (typeof value === 'string') {
    name = value.trim();
  } else if (Array.isArray(value) && value.length) {
    const item = value[0];
    if (typeof item === 'string') name = item;
    else if (item?.name) name = item.name;
    else if (item?.text) name = item.text;
  } else if (typeof value === 'object') {
    name = value.name || value.text || '';
  }
  name = String(name).trim().replace(new RegExp(`^${atPrefix}`), '');
  if (!name) return '';
  if (name.startsWith('agent:')) return name;
  if (name.startsWith(humanPrefix)) return name;
  return `${humanPrefix}${name}`;
}

export function readBitableRowFromFields(fields, cfg) {
  if (!fields || typeof fields !== 'object') return null;
  const get = (name) => {
    const v = fields[name];
    if (v !== undefined && v !== null) return bitableFieldToString(v);
    return '';
  };
  return {
    record_id: '',
    task_id: get(cfg.fieldTaskId).trim(),
    title: get(cfg.fieldTitle).trim(),
    status_label: get(cfg.fieldStatus).trim(),
    sprint_id: get(cfg.fieldSprint).trim(),
    priority: get(cfg.fieldPriority).trim(),
    claimed_by: bitablePersonToClaim(fields[cfg.fieldClaimed], cfg.humanPrefix, cfg.atPrefix),
    dispatch_gate_label: cfg.fieldDispatchGate ? get(cfg.fieldDispatchGate).trim() : '',
    dispatch_confirm_by: cfg.fieldDispatchConfirmBy ? get(cfg.fieldDispatchConfirmBy).trim() : '',
    dispatch_trigger: cfg.fieldDispatchTrigger ? get(cfg.fieldDispatchTrigger).trim() : '',
  };
}

export async function fetchBitableRecord(cfg, token, recordId, appToken, tableId) {
  const at = appToken || cfg.appToken;
  const tid = tableId || cfg.tableId;
  const data = await feishuApi(
    'GET',
    `/bitable/v1/apps/${at}/tables/${tid}/records/${recordId}`,
    token,
  );
  const rec = data.data?.record;
  if (!rec) throw new Error(`record not found: ${recordId}`);
  const row = readBitableRowFromFields(rec.fields, cfg);
  row.record_id = rec.record_id || recordId;
  return row;
}

export async function listAllBitableRecords(cfg, token, appToken, tableId) {
  const at = appToken || cfg.appToken;
  const tid = tableId || cfg.tableId;
  const all = [];
  let pageToken = '';
  do {
    const qs = new URLSearchParams({ page_size: '500' });
    if (pageToken) qs.set('page_token', pageToken);
    const data = await feishuApi(
      'GET',
      `/bitable/v1/apps/${at}/tables/${tid}/records?${qs}`,
      token,
    );
    const items = data.data?.items || [];
    all.push(...items);
    pageToken = data.data?.page_token || '';
  } while (pageToken);
  return all;
}
