# 602 · 波次 C · 审稿 · arch-agent

- 日期：2026-11-10
- 身份：arch-agent
- 范围：`POL-L2-PC1-CLEAN-API.md`、`POL-L2-PC1-CLEAN-METRIC.md`、`POL-L2-PC1-CLEAN-DATA.md`，以及 Storage 的准确性演示节、`CHANGELOG.md`、`01-data-flow.md` 那一句、`stores/README.md` 的 ADS 索引行
- 不审：`POL-L2-PC1-CLEAN-ARCH.md`（本身份刚写过）
- 对照：说明书「#### 602」与文末「已定」、读法方案文末裁定清单、审稿硬清单 arch-agent 五条
- 本稿只记异议。不改设计稿，不替起草身份回写

已知且已选定，不另开缺陷：候选和执行不复用 `governance/results`；不建六条正式事实表；准确性表名 `policy_accuracy_demo` 是这一波的草稿名。

## 硬清单

1. 调用链有越层，见 ARCH-C1、ARCH-C3。页眉仍走原资源 `governance/results`，浏览器仍只打 `/display/v1/policy/**`，不直连 Python，这一句核过（API 第 14–18、116 行）。
2. Java 不读贴源、不读供应方库 `gkx`、不读 `policy_base_info`、不读 `script_state`。两张演示贴源由 Python 只 SELECT。准确性由 Java 只读 `demo_gkxlumenx_ads.policy_accuracy_demo`。不标停机（API 第 88–94 行，DATA 第 19–22、72 行，ads.md 第 101–103 行）。
3. 三份稿和 Storage 新句都没有把 lumen 指到 `demo-svc`、`demo-algo`、`demo-ui`。`demo_gkxlumenx_ads` 是裁定要的演示库，不是 demo 服务。下游镜像没写死的风险并进 ARCH-C1，不另开 D12 停机。
4. 五条结果留在这次响应里，API 写明不允许直接返回写死的质量分数（API 第 131、143 行）。准确性这一块的空行和禁写互相打架，见 ARCH-C2、ARCH-C4。页眉 `M_POLICY_TOTAL_COUNT` 仍走原资源，D4 保持 mock，本波没有给本批条数新开写死口（METRIC 第 17–22 行）。
5. 档位仍是中档。API 写明同步、不进 `gkxlumen-topic-async-service`、不新建清洗 Job、不返回 501（API 第 22–27 行），与读法方案第 1 节一致。指标稿第 2 节的「三档」是可接 / 501 / 跨项，没有把本叶改成轻档或重档；501 为无（METRIC 第 24–28 行）。

## 异议

[arch-agent] ARCH-C1 · 问题：候选和五条由 display 直接转发 `GET /internal/policy/clean-candidates`、`POST /internal/policy/clean-judge`，跳过领域服务。现网治理读面只委托 element，不调 Python。D15 规定展示 BFF 不直连 Python、不直连库。这条直转落到 display 上时，现成的政策 Python 客户端是 `RemotePolicySyncClient`，它打 `gkxlumen-platform-entan-py`，并且带 POST 写同步历史。 · 依据：API.md 第 35、92–94 行；`architecture-baseline.md` D15（展示 BFF 不直连 Python / DB，领域服务再 Feign `/internal`）；`PolicyGovernanceService.java` 第 16–18、22–24 行；`RemotePolicySyncClient.java` 第 14–23、35–40 行。清单第 1 条。 · 建议：display 仍只调 element，准确性已经是这条。候选和五条改由 element 再 Feign 新建的只读路由。不要复用带 POST 的同步历史客户端，也不要打到 demo-*。下游用现网已经挂着 `/internal/policy/**` 的 lumen 算法镜像。

[arch-agent] ARCH-C2 · 问题：DATA 第 1 节写不对 `{ods}`、DWD、ADS、`gkx` 写入，第 5 节又要 Python 把演示行写入 `policy_accuracy_demo`。点击这次的 SELECT 不写 ADS 是对的，第 1 节没有把禁写限定在这一次。禁写若盖过演示表，准确性没有可读写的行，接口只能停在读取失败，或者退回写死数。 · 依据：DATA.md 第 22 行与第 64–71 行；裁定清单第 3 条；D18；ads.md 第 103 行写了 Python 另行写入。清单第 4 条。 · 建议：第 1 节的禁写收成「这一次候选和五条 SELECT 不写 ADS」。演示表的写入留在点击之外，单独成句。

[arch-agent] ARCH-C3 · 问题：`01-data-flow.md` 把 602 点执行写成 Java 只读 `policy_accuracy_demo`，紧下面的图仍是展示全景那条：Java 只连 `demo_gkxlumenx_ads.policy_*`，Python 边只标图/推演。五条的 `/internal/policy/clean-judge` 没有边。按这张图，整次执行会收成 Java 单读 ADS，贴源现算被丢掉。 · 依据：`01-data-flow.md` 第 75–84 行；API.md 第 92–94 行。清单第 1 条。 · 建议：这句话改成只覆盖准确性这一块，并写明五条仍由 Python 只 SELECT 演示贴源两表。工厂主链第 1 节不用改，也不要把这张 DS-10 图改成 602 的时序图。

[arch-agent] ARCH-C4 · 问题：准确性只写了「有演示数」和「表读失败」。本波不连库灌数，读成功但没有该来源和贴源 id 的行时，没有第三句。无匹配行不是读取失败，也不走五条的无加工事实。这一窗会被补成 0 或写死分数，D18 不能签。 · 依据：API.md 第 77–78、94、143 行；DATA.md 第 69、86 行；ads.md 第 97–103 行；说明书 602-7（点过执行后准确性要看得见是演示的数，不得写成已经按原文核过）。清单第 4 条。 · 建议：写明无匹配行时这一块不返回数、不返回 0、不写成已核过，并和读取失败分成两句。灌数仍留在点击之外。

[arch-agent] ARCH-C5 · 问题：`stores/README.md` 的 ADS 索引仍只写 16 张，正文没有 `policy_accuracy_demo`。16 这个数没有算错，ads.md 写明这张草稿表不计入 as-built 16 张。漏的是索引入口，只翻索引会以为 POLICY ADS 没有这张 draft。 · 依据：`stores/README.md` 第 21 行；ads.md 第 18、97–103 行；`CHANGELOG.md` 第 5 行已记草稿表。 · 建议：索引行末加一句「另有 draft：`policy_accuracy_demo`，不计入 16」。不要把 16 改成 17。
