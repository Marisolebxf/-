#!/usr/bin/env node
/**
 * Feishu IM helpers — notify a user by open_id (tenant token).
 * MCP wrapper: scripts/feishu-im-mcp-server.mjs（禁止直接传 open_id，见 feishu-im-mcp-usage-guide.md）
 * Requires app scopes: im:message / im:message:send_as_bot.
 */

import { feishuApi, feishuTenantToken } from './feishu-open-api.mjs';

export async function sendTextToOpenId(openId, text, opts = {}) {
  if (!openId) throw new Error('open_id required');
  const body = {
    receive_id: openId,
    msg_type: 'text',
    content: JSON.stringify({ text: String(text || '').slice(0, 4000) }),
  };
  if (opts.dryRun) {
    return { ok: true, dryRun: true, body };
  }
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;
  if (!appId || !appSecret) {
    throw new Error('FEISHU_APP_ID / FEISHU_APP_SECRET required for IM');
  }
  const token = await feishuTenantToken(appId, appSecret);
  const data = await feishuApi(
    'POST',
    '/im/v1/messages?receive_id_type=open_id',
    token,
    body,
  );
  return { ok: true, message_id: data.data?.message_id, data };
}
