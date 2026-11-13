/**
 * 飞书官方 OpenAPI MCP 启动包装（@larksuiteoapi/lark-mcp）。
 * 凭证只从 gkx-orchestration/.env 的 FEISHU_APP_ID / FEISHU_APP_SECRET 读取，不进 mcp.json。
 *
 * 官方文档：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/mcp_integration/mcp_installation
 * 首次使用前需用户 OAuth 登录（60 秒内授权）：
 *   node scripts/lark-openapi-mcp-login.mjs
 */
import { spawn } from 'node:child_process';
import { loadDotEnv, ORCH_ROOT } from './lib/feishu-bitable-config.mjs';

loadDotEnv(ORCH_ROOT);

const appId = process.env.FEISHU_APP_ID?.trim();
const appSecret = process.env.FEISHU_APP_SECRET?.trim();
if (!appId || !appSecret) {
  console.error('[lark-mcp] 缺少 FEISHU_APP_ID / FEISHU_APP_SECRET（请写在 gkx-orchestration/.env）');
  process.exit(1);
}

const npxBin = process.platform === 'win32' ? 'npx.cmd' : 'npx';

// 官方推荐：stdio + OAuth 用户身份；默认工具集含 wiki.v2.space.getNode
const args = [
  '-y',
  '@larksuiteoapi/lark-mcp',
  'mcp',
  '-a',
  appId,
  '-s',
  appSecret,
  '-l',
  'zh',
  '--oauth',
  '--token-mode',
  'user_access_token',
  ...process.argv.slice(2),
];

const child = spawn(npxBin, args, {
  stdio: 'inherit',
  cwd: ORCH_ROOT,
  env: process.env,
});

child.on('exit', (code, signal) => {
  if (signal) process.exit(1);
  process.exit(code ?? 1);
});
