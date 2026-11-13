/**
 * 飞书官方 OpenAPI MCP 用户登录（OAuth）。
 * 终端会打印授权 URL，须在 60 秒内用浏览器打开并点「授权」。
 *
 * 应用侧前置（开发者后台）：
 * 1. 安全设置 → 重定向 URL 增加 http://localhost:3000/callback
 * 2. 开通默认权限（官方批量串）：im:chat:create, im:chat, im:message, wiki:wiki,
 *    wiki:wiki:readonly, docx:document, bitable:app, drive:drive,
 *    docs:document:import, contact:user.id:readonly
 * 3. 若要写经典电子表格，另开 sheets:spreadsheet 并发布版本
 * 4. 创建版本并发布通过审核
 */
import { spawn } from 'node:child_process';
import { loadDotEnv, ORCH_ROOT } from './lib/feishu-bitable-config.mjs';

loadDotEnv(ORCH_ROOT);

const appId = process.env.FEISHU_APP_ID?.trim();
const appSecret = process.env.FEISHU_APP_SECRET?.trim();
if (!appId || !appSecret) {
  console.error('[lark-mcp-login] 缺少 FEISHU_APP_ID / FEISHU_APP_SECRET');
  process.exit(1);
}

console.error('[lark-mcp-login] 即将打开授权流程；请在 60 秒内完成浏览器授权…');

const npxBin = process.platform === 'win32' ? 'npx.cmd' : 'npx';
const child = spawn(
  npxBin,
  ['-y', '@larksuiteoapi/lark-mcp', 'login', '-a', appId, '-s', appSecret, '--scope', 'offline_access'],
  { stdio: 'inherit', cwd: ORCH_ROOT, env: process.env },
);

child.on('exit', (code, signal) => {
  if (signal) process.exit(1);
  process.exit(code ?? 1);
});
