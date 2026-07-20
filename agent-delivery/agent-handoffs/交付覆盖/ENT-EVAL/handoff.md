# ENT-EVAL Demo v1.6 交接

## 当前状态

- `delivery_stage: v1_hifi_round1`。当前覆盖保持 8 项、18 个声明挂点；`ENT-EVAL-F02-COMP-GAP-TITLE` 已随重复模块删除。
- E-23 当前为 `DEMO`，对应 `DEMO-005`；E-24 当前为 `DEMO`，对应 `DEMO-006`；E-30 当前为 `DEMO`，对应 `DEMO-007`。三项 `planned_tier` / `delivery_tier` 均为 `DEMO`，未认领 `INTEG` 或 `FULL`。
- 顶层只有 E-23 / E-24 / E-30 三个唯一验收单元合同；TECH 只归 E-23，BIZ 只归 E-24，COMP 只归 E-30，OBJ、QUALITY、RESULT、REPORT、HISTORY 分别关联三者，共 18 条 item-to-unit 关联，不使用复合 ID。
- 8 个 Demo 覆盖项当前均登记 `simulated_fixture / pending_source / partial / unchecked / unknown / degraded`，不得解释为真实来源、已完成映射、完整可用、质量通过或当前批次。
- v1.6 挂点集合、业务 / 评审隔离与双模式交互已重新验证：18 个声明挂点完整，业务模式挂点为 0。
- 商业力行业切换沿用确定性模拟预览：默认切换会同时改变 4 个可用指标中的 3 项选中组合及其整数权重，未选中的可用指标权重为 0；配置已修改时由用户明确选择应用行业配置、保留自定义配置或取消。
- 配置视图只在三模式页签上方渲染一个共享评估对象区；切换模式保留同一对象集合，并按技术力 / 商业力至少 2 家、综合竞争力至少 1 家重新校验。
- 技术模式保持单一“技术指标与差距诊断”；综合竞争力模式也已将“优势与短板诊断”和“指标明细与综合差距”归并为单一“综合竞争力与差距诊断”。单企展示企业、综合得分、可信度、集合均值/领先值与优势短板；双企展示双方得分、可信度、维度差值与结论。
- 企业评估契约、design check、生产构建与真实指针验证均通过；三指纹已刷新，`verified_status_valid: true`。

## 未完成边界

- Q014 默认指标与权重仍待甲方确认；K-O7 商业指标数据、行业维度规则、正式算法 / ADS / 报告服务仍待外部输入。
- 不得用模拟值、未登记维度或旧 SRS / 旧 IA / 旧用户故事填补上述缺口。
- Gate 1 / PDR、V1-FINAL、V2 lumen、INTEG、FULL 均未认领完成。

## 恢复验证

先确认 Vite 已在 `127.0.0.1:4177` 提供当前工作树页面。以下命令先确认 9231 未占用，再创建一次性 profile、后台启动 Chrome、验证 CDP、运行 pointer test，并通过 `trap` 清理进程和 profile：

```bash
set -e
if curl --fail --silent --show-error --connect-timeout 2 --max-time 5 \
  http://127.0.0.1:9231/json/version >/dev/null 2>&1; then
  echo 'port 9231 is already occupied' >&2
  exit 1
fi

profile=$(mktemp -d /tmp/gkx-ent-eval-cdp.XXXXXX)
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --headless=new \
  --remote-debugging-port=9231 \
  --user-data-dir="$profile" \
  --disable-gpu \
  --window-size=1440,900 \
  about:blank &
chrome_pid=$!
cleanup() {
  kill "$chrome_pid" 2>/dev/null || true
  wait "$chrome_pid" 2>/dev/null || true
  find "$profile" -depth -delete 2>/dev/null || true
}
trap cleanup EXIT INT TERM

for attempt in {1..50}; do
  if curl --fail --silent --show-error --connect-timeout 2 --max-time 5 \
    http://127.0.0.1:9231/json/version >/dev/null; then
    break
  fi
  sleep 0.1
done
curl --fail --silent --show-error --connect-timeout 2 --max-time 5 \
  http://127.0.0.1:9231/json/version >/dev/null

cd /Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic
node --experimental-strip-types tests/enterprise-evaluation-definition.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-model.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-result-model.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-task-store.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-template-store.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-report.test.mjs
node --experimental-strip-types tests/enterprise-evaluation-v12-contract.test.mjs
node --experimental-strip-types tests/enterprise-review-mount-contract.test.mjs
node --experimental-strip-types tests/review-marker-self-gating.test.mjs
ENT_EVAL_CDP_PORT=9231 node tests/enterprise-evaluation-v12-pointer.test.mjs
node /Users/ying/.codex/skills/gkx-ui-design-standards/scripts/check-composite-labels.mjs \
  src/app/pages/enterprise/EnterpriseEvaluationPage.tsx \
  src/app/pages/enterprise/EnterpriseEvaluationResultWorkspace.tsx \
  src/app/components/common/MetricSpecCard.tsx
npm run design:check
npm run build
```

指针测试会重写以下当前证据：

- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/industry-preview-business-v16.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/industry-preview-review-v16.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/metric-gap-review-v12.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/result-technology-v13.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/result-business-v12.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/result-competitiveness-v16.png`
- `agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence/dual-mode-dom-v16.json`

重新生成证据后，必须按计划重算 definition / implementation / evidence 三指纹，再决定 `verified_status_valid`；不得沿用本交接中的旧哈希。

Definition 指纹沿用计划 Task 5 Step 2 的精确输入与命令：`/Users/ying/Documents/codex/gkx-lumen/repos/demo-ui-topic/docs/superpowers/plans/2026-07-19-enterprise-evaluation-gkx-skill-compliance.md`。Implementation 与 evidence 指纹使用以下精确输入；coverage 文件自身不得进入 implementation 指纹，历史截图不得进入 evidence 指纹：

```bash
cd /Users/ying/Documents/codex/gkx-lumen
implementation_inputs=(
  repos/demo-ui-topic/src/app/components/common/MetricSpecCard.tsx
  repos/demo-ui-topic/src/app/components/common/MockBadge.tsx
  repos/demo-ui-topic/src/app/components/common/PendingBadge.tsx
  repos/demo-ui-topic/src/app/components/common/ReviewMetricBadges.tsx
  repos/demo-ui-topic/src/app/components/common/ReviewTrace.tsx
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseEvaluationPage.tsx
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseEvaluationResultWorkspace.tsx
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseOutputTaskModal.tsx
  repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationModel.ts
  repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationReport.ts
  repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationResultModel.ts
  repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationTasks.ts
  repos/demo-ui-topic/src/app/pages/enterprise/enterpriseEvaluationTrace.tsx
  repos/demo-ui-topic/src/app/pages/personal/PersonalAssetsPage.tsx
  repos/demo-ui-topic/tests/enterprise-evaluation-definition.test.mjs
  repos/demo-ui-topic/tests/enterprise-evaluation-model.test.mjs
  repos/demo-ui-topic/tests/enterprise-evaluation-report.test.mjs
  repos/demo-ui-topic/tests/enterprise-evaluation-result-model.test.mjs
  repos/demo-ui-topic/tests/enterprise-evaluation-task-store.test.mjs
  repos/demo-ui-topic/tests/enterprise-evaluation-template-store.test.mjs
  repos/demo-ui-topic/tests/enterprise-evaluation-v12-contract.test.mjs
  repos/demo-ui-topic/tests/enterprise-evaluation-v12-pointer.test.mjs
  repos/demo-ui-topic/tests/enterprise-review-mount-contract.test.mjs
  repos/demo-ui-topic/tests/enterprise-compare-basket-definition.test.mjs
  repos/demo-ui-topic/tests/review-marker-self-gating.test.mjs
)
shasum -a 256 "${implementation_inputs[@]}" \
  | shasum -a 256 | awk '{print $1}' \
  | tee /tmp/ent-eval-implementation.sha256

evidence_dir=gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-EVAL/evidence
(
  shasum -a 256 "$evidence_dir/industry-preview-business-v16.png"
  shasum -a 256 "$evidence_dir/industry-preview-review-v16.png"
  shasum -a 256 "$evidence_dir/metric-gap-review-v12.png"
  shasum -a 256 "$evidence_dir/result-technology-v13.png"
  shasum -a 256 "$evidence_dir/result-business-v12.png"
  shasum -a 256 "$evidence_dir/result-competitiveness-v16.png"
  shasum -a 256 "$evidence_dir/dual-mode-dom-v16.json"
  cat /tmp/ent-eval-definition.sha256
  cat /tmp/ent-eval-implementation.sha256
) | shasum -a 256 | awk '{print $1}' \
  | tee /tmp/ent-eval-evidence.sha256
```
