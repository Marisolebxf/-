# `/goal` · LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01

```
/goal LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01
角色：qa-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
只认：http://10.50.69.111:30892
强度：ponytail full
金路径：总控 §4 五条（#2 = 页内集群→L0，含 INB4 应能选；不强制篮）。
期望未发生必红。QA 不改代码。
门：前端镜像含 7cd3be4；innov 300ad303；clusters GET 非 500。
禁止：用代理 POST 改判 PASS；拿明文 analysis_fp 当结论；把 e2e:chain-gold 当政策结论。
```

## 背景

上一轮 FAIL：`LUMEN-POLICY-E-QA-SMOKE-L0VID-RETEST-L01`（#1/#2 PASS；#3～#5 点开始分析因 HTTP 上 `crypto.subtle` 抛错，未进过程页）。  
C1 `LUMEN-POLICY-E-C1-FE-FP-HTTP-L01` SHA **`7cd3be4`**。  
E0 `LUMEN-POLICY-E-DEVOPS-FE-FP-HTTP-L01` 现网 **`gkx-lumen-topic:7cd3be47`**，30892 HTTP 200。innov 仍 **`300ad303`**。

本叶是**新复测**，不要沿用旧 FAIL 当结论。不要再派 L0 滤空或「subtle 缺失」除非本轮复现。

## 本轮要核

1. 点「开始分析」**不得**再抛 `crypto.subtle` / `digest` TypeError；须从 UI 进 `view=processing`。
2. #3～#5 必须从 UI 点「开始分析」→ 过程页 → Job `succeeded` 后 wait_view 点查看结果。**禁止**代理 POST 改判 PASS。
3. #2 上轮已 PASS，本轮再扫一眼：INB4 能选。选短码后 Create 应 `industry_id` 原样，禁止 `chain:INB1303`。Java 若 4xx 记缺陷包（C1 Java），**不改 Java**；VID 预填路径仍须把 #3～#5 跑完。
4. 指纹失败应有 toast（若仍静默失败则 C1 FE）。明文 `analysis_fp` 闸不要当本轮结论。

## 门（未过则停）

| 门 | 期望 |
|----|------|
| 前端 | `gkx-lumen-topic` 镜像含 **`7cd3be4`**（现网应为 `7cd3be47`） |
| innov | `gkxlumen-innov:300ad303` |
| clusters | GET 非 500 |

handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-FP-HTTP-RETEST-L01.md`  
缺陷包（若红）：同目录 `…-defect-pack.md`。不要自行 done。不要写「联调通过」除非五条全 PASS。
