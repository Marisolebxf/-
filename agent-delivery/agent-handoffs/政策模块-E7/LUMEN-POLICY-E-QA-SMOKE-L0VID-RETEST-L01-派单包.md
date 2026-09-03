# `/goal` · LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01

```
/goal LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01
角色：qa-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
只认：http://192.168.88.50:30892
强度：ponytail full
金路径：总控 §4 五条（#2 = 页内集群→L0，含 INB4 应能选；不强制篮）。
期望未发生必红。QA 不改代码。
门：前端镜像含 1ce03cc；innov 300ad303；clusters GET 非 500。
禁止：用代理 POST 改判 PASS；拿明文 analysis_fp 当结论；把 e2e:chain-gold 当政策结论。
```

## 背景

上一轮 FAIL：`LUMEN-POLICY-E-QA-SMOKE-CLUSTERS-RETEST-L01`（clusters 已 200；L0 全是 `INB`+4 位被滤空；开始分析 disabled）。  
C1 FE `LUMEN-POLICY-E-C1-FE-L0VID-L01` SHA **`1ce03cc`** 已 push。  
E0 `LUMEN-POLICY-E-DEVOPS-FE-L0VID-L01` 现网 **`gkx-lumen-topic:1ce03cc4`**，30892 HTTP 200。innov 仍 **`300ad303`**。

本叶是**新复测**，不要沿用旧 FAIL 当结论。

## 本轮要核（相对上一轮变了什么）

1. **#2 页内集群→L0**：innov map 的 L0（含 `INB1303` 这类 4 位）**应能选**，不得再滤空导致产业下拉 disabled。
2. **VID 预填**：URL `INB170101` / `chain:INB170101` 时，即使 `clusterId` 空，「开始分析」须可点，点后须进过程页（`view=processing`）。
3. **#3～#5 必须从 UI 点「开始分析」**：过程页 → Job `succeeded` 后 wait_view 点查看结果。**禁止**用 30892 代理 POST 改判 PASS。API success ≠ 金路径 PASS。
4. **提交语义**：图上码走 `industry_vid=chain:INB…`；短码走 `industry_id` 原样，**不得**出现伪造 `chain:INB1303`。Java 若拒短码 `industry_id`：记入缺陷包（建议 C1 Java），**本叶不改 Java**。VID 预填路径仍须把 #3～#5 跑完。
5. **明文 `analysis_fp` 闸本轮不要当结论**（上一轮 Create 已发出且 SHA-256 被 Java 接受）。

## 门（未过则 E1 不开、先停）

| 门 | 期望 |
|----|------|
| 前端 | `gkx-lumen-topic` 镜像含 **`1ce03cc`**（现网应为 `1ce03cc4`） |
| innov | `gkxlumen-innov:300ad303` |
| clusters | `GET /api/topic/v1/meta/industry-clusters?include_l0=true` **非 500** |

## 失败分类

期望未发生必红。C1 必带 `X-Trace-Id`。C1 FE vs C1 Java 写清。不要标 C5（clusters 已 200）。不要自行 done。不要写「联调通过」除非五条全 PASS。

handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01.md`  
缺陷包（若红）：同目录 `…-defect-pack.md`，模板 `templates/long-task-e-defect-pack.md`。
