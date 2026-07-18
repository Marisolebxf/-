# ENT-RISK Validation Report

## Current status

- Stage: local Demo implementation and dual-mode verification completed under explicit task-state override.
- Definition source: frozen four-pack at `132725e`.
- Demo branch: `repos/demo-ui-topic/dev`; local head `ae4eb5c` (`aaed089`, `34fde8b`, `43b325d`, `8675b5e`, `6093cc9`, `ae4eb5c`); not pushed.
- Task registry: intentionally not changed; `review/done` remains blocked until later reconciliation.
- Reference sample: public page returned HTTP 200; no reliably mappable risk-task/result sample values were found, so deterministic simulated fixtures are planned.

## Checks run

- `node --experimental-strip-types tests/enterprise-risk-insight-definition.test.mjs`: PASS after observed missing-module / missing-page RED.
- `node --experimental-strip-types tests/enterprise-risk-insight-task-store.test.mjs`: PASS after observed missing-module RED.
- `node --experimental-strip-types tests/enterprise-risk-insight-report.test.mjs`: PASS after observed missing-module RED.
- `node scripts/check-enterprise-risk-insight.mjs`: PASS.
- `npm run design:check`: PASS.
- `npm run build`: PASS; 5074 modules transformed, production assets emitted; only the existing chunk-size advisory remains.
- `http://127.0.0.1:4177/enterprise-center/risk`: HTTP 200 from `repos/demo-ui-topic/dev`.
- Duplicate in-workbench risk-mode radio group removed; enterprise-center top tabs remain the sole mode switch. Definition contract, static visibility check, design check, and production build: PASS.
- Workbench title dual-mode render check: business mode has no `h1` risk title; review mode renders `h1=风险洞察`; business top tab remains present.
- Compare-basket handoff de-duplication: the enterprise-center banner was removed; the `分析对象` frame is the sole source, object-management, and return entry. Evidence: `evidence/business-config-no-duplicate-handoff.png`.
- Shared-object rule: both analysis tabs retain the same five-object session; supply-chain explicitly blocks above two objects, while pain-point analysis accepts the same five-object set, matching frozen `F-RISK-01` behavior without silent truncation.
- Completed-result edit loop: supply and pain results expose `修改配置并重新分析`; real-page click removed result/task parameters and restored the task's objects and configuration before creating a new immutable task.
- Supply side-panel toggle: real-page click changed the content from `关键节点 / 关系类型 / 节点影响度` to `断链风险 / 风险类型 / 风险依据`; identical dual-classification nodes no longer make the two views appear unchanged.
- Business/review DOM assertions: PASS for configuration, processing, supply result, pain result, history, and report.
- Business-mode leak scan: Q017, Q018, F-RISK, M_ENT_, `riskTaskId`, task snapshot, and report fingerprint absent.
- Screenshots: configuration, processing, supply result, pain result, history, and report stored under `evidence/`.
- Requirement-source copy: `evidence/review-demand-source-copy.png`; the risk title popover shows the verbatim E-28/E-29 feature sentences under `需求原文`, while metric/Q notes use `追溯说明`.

## Manual-review items

- Q017: core-supplier threshold and break-risk rating remain unresolved; Demo values must not be presented as approved formulas.
- Q018: pain dimensions and thresholds remain provisional; V1 uses the confirmed temporary four dimensions.
- Visual sign-off H-01 through H-08 remains pending after implementation.

## Coverage result

- verified: 7
- implemented: 0
- planned: 0
- manual review: Q017, Q018, H-01 through H-08
- blocked implementation items: 0
- registry gate: still blocked by the intentionally deferred task-state reconciliation
