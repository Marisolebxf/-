// 015 补登 repo scope（含自检测试文件），与实际计划 3 文件一致
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

const SCRIPT = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\.cursor\\skills\\feishu-bugfix\\scripts\\bugflow-state.mjs';
const repos = [
  {
    repo_id: 'ui_pc',
    repo_name: 'lumen-ui-science-pc',
    remote: 'https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc.git',
    base_branch: 'dev',
    base_sha: '7ef79f4',
    candidate_sha: '5e96b09d8badd432e0d14264bfebd25d60565a35',
    planned_change_scope: [
      'src/views/policy/simulation/interpret/InterpretWorkbench.vue',
      'src/views/policy/simulation/FE-POL-03A.test.mjs',
    ],
    role: 'primary',
    depends_on: [],
    ship_order: 1,
  },
];
const path = 'e:\\zhipu\\gkx-lumen\\gkx-orchestration\\agent-delivery\\bugfix-runs\\015-7167862142\\local\\repos-v2.json';
writeFileSync(path, JSON.stringify(repos, null, 2), 'utf8');
execFileSync('node', [SCRIPT, '--auto-number', '015', '--work-item-id', '7167862142', 'set-repos', '--repos-file', path], { stdio: 'inherit' });
console.log('repos scope updated');
