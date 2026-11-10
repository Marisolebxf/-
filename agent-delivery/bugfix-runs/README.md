# 飞书缺陷运行账本

本目录只保存每个飞书缺陷的运行产物：

```text
<auto_number>-<work_item_id>/
  state.json
  report.md
  evidence/manifest.json
  evidence/raw/                 # 默认不提交
  cycles/<cycle_id>/state.json
  cycles/<cycle_id>/evidence/manifest.json
  local/                         # 本机路径映射，默认不提交
```

Skill 的唯一完整真源、脚本、模板和 policy 位于：

```text
.cursor/skills/feishu-bugfix/
```

不要在本目录新增 Skill 代码、schema、policy 或设计文档。这里只保存单次运行的执行真相和审计材料。

主说明见 [references/README.md](../../.cursor/skills/feishu-bugfix/references/README.md)。
