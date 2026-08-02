#!/usr/bin/env node
/**
 * 删除飞书「状态」列的「评审中」选项（review legacy 选项清理）
 *
 * 飞书 Bitable 单选列删除选项 API：
 *   PUT /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id}
 *   body: { field_id, type, property: { options: [...] } }  // 只保留需要的选项
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ORCH_ROOT = path.resolve(__dirname, '..');

// 读 .env
const envPath = path.join(ORCH_ROOT, '.env');
const env = Object.fromEntries(
  fs.readFileSync(envPath, 'utf8')
    .replace(/^\uFEFF/, '')
    .split('\n')
    .filter(l => l && !l.startsWith('#') && l.includes('='))
    .map(l => {
      const i = l.indexOf('=');
      return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^["']|["']$/g, '')];
    })
);

const APP_ID = env.FEISHU_APP_ID;
const APP_SECRET = env.FEISHU_APP_SECRET;
const APP_TOKEN = 'JI94bBxwsaIzyMsMBrYcPJscnDc';
const TABLE_ID = 'tblb65lPULz31h9U';

if (!APP_ID || !APP_SECRET) {
  console.error('缺少 FEISHU_APP_ID / FEISHU_APP_SECRET');
  process.exit(1);
}

async function getTenantToken() {
  const res = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`get token failed: ${data.msg}`);
  return data.tenant_access_token;
}

async function feishuApi(token, method, p, body) {
  const res = await fetch(`https://open.feishu.cn/open-apis${p}`, {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.json();
}

async function main() {
  const token = await getTenantToken();
  console.log('✅ 获取 tenant_access_token 成功');

  // 1. 列出所有字段，找到「状态」列
  const fieldsRes = await feishuApi(token, 'GET', `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields`);
  if (fieldsRes.code !== 0) throw new Error(`list fields failed: ${fieldsRes.msg}`);
  const statusField = fieldsRes.data.items.find(f => f.field_name === '状态');
  if (!statusField) {
    console.error('❌ 找不到「状态」列');
    process.exit(1);
  }
  console.log(`✅ 找到「状态」列: field_id=${statusField.field_id}, type=${statusField.type}`);

  // 2. 查看当前选项
  const options = statusField.property?.options || [];
  console.log(`\n当前选项 (${options.length} 个):`);
  for (const opt of options) {
    console.log(`   ${opt.name} (id=${opt.id || '无'})`);
  }

  // 3. 找到「评审中」选项
  const reviewOpt = options.find(o => o.name === '评审中');
  if (!reviewOpt) {
    console.log('\n⚠️ 「评审中」选项不存在，无需删除');
    return;
  }
  console.log(`\n🎯 找到「评审中」选项: id=${reviewOpt.id || '无'}`);

  // 4. 删除「评审中」选项（重新 PUT 字段，options 不含「评审中」）
  const newOptions = options.filter(o => o.name !== '评审中').map(o => ({ name: o.name }));
  console.log(`\n删除后剩余选项 (${newOptions.length} 个):`);
  for (const opt of newOptions) {
    console.log(`   ${opt.name}`);
  }

  const updateRes = await feishuApi(token, 'PUT',
    `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields/${statusField.field_id}`,
    {
      field_name: '状态',
      type: statusField.type,
      property: { options: newOptions },
    }
  );

  if (updateRes.code !== 0) {
    console.error(`\n❌ 删除选项失败: code=${updateRes.code} msg=${updateRes.msg}`);
    console.error(JSON.stringify(updateRes, null, 2));
    process.exit(1);
  }

  console.log('\n✅ 「评审中」选项已从飞书「状态」列删除');
  console.log(`   剩余选项: ${updateRes.data.property.options.length} 个`);
}

main().catch(e => { console.error(e); process.exit(1); });
