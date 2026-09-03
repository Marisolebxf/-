# `/goal` · LUMEN-POLICY-E-C1-FE-L0VID-L01

```
/goal LUMEN-POLICY-E-C1-FE-L0VID-L01
角色：frontend-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic · origin/dev
强度：ponytail full
本单由段 E 缺陷包测试驱动。只修本包指向的根因。
复刻：布局+交互+样式+评审+Mock开关。必读 templates/fe-replica-visual-dod.md。
范围：政策三项配置页 PolicyAnalysisConfigPage：页内能选 map L0；URL 已有 chain:INB… 时开始分析可点。
禁止：贴 JSX；页内 MOCK；改 Java 闸门；DDL 正式库；改 IndustryClusterSelect.vue / useIndustryClusters.ts（李伟 CHAIN 叶占用）；lumen 调 demo-*。
对照：缺陷包 + 总控 §0 #8/#9/#10 + 人审集群→map L0。
X-Trace-Id：a15b911860aa8089b8ea3b3fe6f44506
图：POLICY-STORAGE-FLOW 不改工厂拓扑。
```

## 缺陷真源

- QA：[复测集群接口后金路径](0ca011ba-4e47-4baf-8e39-9898ac78afa7) FAIL 1/4
- 缺陷包：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01-defect-pack.md`
- clusters **已 200**（不是 C5）。innov `300ad303`。
- Create 经代理已发出，SHA-256 被 Java 接受。**禁止**再修指纹。

## coordinator 确认类 = C1 FE

根因在 `PolicyAnalysisConfigPage.vue`：

1. `clusterL0Options` + `require-graph-vid` 把 innov 返回的 **INB+4 位**（`INB1303` 等）滤空 → 下拉 disabled。
2. `scopeReady` 同时要 `clusterId` **和** `industryVid`。URL `object_ids[]=INB170101` 已显示 `chain:INB170101`，仍 hint「尚未选择分析对象」，开始分析 disabled，UI 进不了 wait_view。

人审（2026-09-02）：页内先集群（map）再选该 map 下 L0。DIM 种子 L0 **就是** `INB12xx/INB13xx`，不是 `INB170101`。总控 §0 #8 禁止把 ODS 短码**当图点 VID**，不是禁止出现在下拉。

## 必须改（只动政策配置页 + 自检）

1. **下拉**：政策页不要把 map L0 滤成空。能选恰好 1 个 L0（含 `INB\\d{4}`）。无映射仍「无相关产业数据」。禁止 `CL-*` 当产业。
2. **scopeReady**：已选 1 个 map L0，**或**已有 `toPolicyGraphVid` 成功的预填 VID。有 VID 时不得再因 `clusterId` 空挡住开始分析。预填 VID 时用已有 `catalog.clusterForIndustry` 回填集群（没有也不挡提交）。
3. **提交**：`INB`≥6 / `chain:` → `industry_vid=chain:INB…`。map 短码 L0 → 带 `industry_id` 原样；**禁止**伪造 `chain:INB1303` 当图 VID。Java 若拒短码，handoff 记拒包，本叶不改 Java。
4. 点「开始分析」须 `view=processing`（I2-12 仍不自动 create）。
5. `npx vue-tsc --build` 零 error。自检：INB4 出现在选项；INB170101 预填可点开始分析。

## 仓边界

- 只改 `src/views/policy/PolicyAnalysisConfigPage.vue`、`src/views/policy/policyConfig.selfcheck.mjs`（及确需的 registry 一处）。
- **禁止**改 `IndustryClusterSelect.vue`（`LUMEN-CHAIN-INDUSTRY-CLUSTER-L01` / `human:李伟`）。

## 验收

- push `origin/dev`；commit `[agent:frontend-agent]`；禁止 force。
- handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-C1-FE-L0VID-L01.md` + ponytail: full + cost + 需 E0 再滚前端。
- 不要自行 done。
