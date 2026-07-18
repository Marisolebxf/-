# ENT-RISK Demo Handoff

## Resume point

- Definition package: frozen and pushed at `gkx-orchestration@132725e`.
- Demo branch: `dev` in `/Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic`.
- Demo local commit: `aaed089` (not pushed).
- Coverage local commit baseline: `24a0c0f`; subsequent verification updates remain local (not pushed).
- Coverage: 0 planned, 0 implemented, 7 verified, 0 blocked implementation items.
- Registry deviation: user explicitly authorized Demo work before task-state reconciliation; do not mark the task `review` or `done` until registry gates are repaired.

## Exact resume command

```bash
cd /Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic
node --experimental-strip-types tests/enterprise-risk-insight-definition.test.mjs
```
