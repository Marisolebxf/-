# ENT-RISK Demo Handoff

## Resume point

- Definition package: frozen and pushed at `gkx-orchestration@132725e`.
- Demo branch: `feat/ent-risk-v1` in `/Users/ying/Documents/codex/gkx-lumen/.worktrees/ent-risk-demo`.
- Coverage: 7 planned, 0 implemented, 0 verified, 0 blocked.
- Registry deviation: user explicitly authorized Demo work before task-state reconciliation; do not mark the task `review` or `done` until registry gates are repaired.

## Exact resume command

```bash
cd /Users/ying/Documents/codex/gkx-lumen/.worktrees/ent-risk-demo
node --experimental-strip-types tests/enterprise-risk-insight-definition.test.mjs
```

