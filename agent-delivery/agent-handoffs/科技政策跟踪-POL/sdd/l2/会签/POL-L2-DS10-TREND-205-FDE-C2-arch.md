# POL-L2-DS10-TREND-205-FDE · 波次 C2 · 审稿 · arch-agent

- 日期：2026-11-15
- 身份：arch-agent
- 被审：`sdd/l2/POL-L2-DS10-TREND-ARCH.md` 第 7.6 节，以及第 2 节表里 205 那两行；说明书「#### 205 重点领域政策分析（2026-11-15）」夜改后的正文
- 口径：`.cursor/skills/gkx-fde-design-change/审稿硬清单.md` arch-agent 五问
- 本稿只记审稿。不改 ARCH，不改说明书，不改旧会签，不写代码，不 commit

监管人方案按当次会话理解：中台手动加工，现在不做调度；结果最终落 ADS；展示只读 ADS，不加工。中台当前写 `demo_gkxlumenx_ads`，展示读 `gkxlumenx_ads` 同名表。正式表本次不建。展示页不改接线。

## 硬清单（五问）

1. **调用链**：第 7.6 节把链拆成两条，这一步成立。中台是「中台页面 → demo Java 透传 → Python `/internal/policy/*`」，浏览器不直连 Python。展示是「展示页面 → lumen Java」，打开时不提交加工、不调模型。205 趋势仍走已有 `GET /display/v1/policy/panorama/stats`，不另开一条统计。越层不在第 7.6 节这两句上。同文件第 2 节流程图和第 4.3 节还把影响、深度报告画进缺项表 / `jobs`，和表第 39 行、第 7.6 节不是一条链。见异议 C2-1。
2. **Java 读什么**：205 趋势读已有 `M_POLICY_TIMESERIES` 所在结果表，是 ADS，不在本问停机。展示目标读 `gkxlumenx_ads`，不读 DWD、不读演示库。中台段写「取材可以读演示 DWD 的 `policy_base_info` 和 `policy_industry_rel`」，读的人没有点名，句子紧挨 demo Java。Java 打开这两张 DWD 按本问停机。见异议 C2-2。
3. **D12**：第 7.6 节写明展示不读演示库、不调加工。正文没有 `gkxlumen-*` 去调 `demo-*` 服务。中台停在 demo Java → Python，不把 lumen 接进 demo。本问通过的前提是：以后把行送进 `gkxlumenx_ads` 时，仍不让 lumen 去读 `demo_gkxlumenx_ads`。见异议 C2-3。
4. **D18**：第 7.6 节没有写接口直接返回写死 JSON，也写了失败不删旧行、不写「缺项演示」、没有政策不写 0。本波写入的是 `demo_gkxlumenx_ads`，展示要读的 `gkxlumenx_ads` 同名表本次不建，展示接线不改。本波没有一条展示接口读「被写入的那张表」。见异议 C2-3。
5. **档位**：中档成立，范围只包括本波。规程 §4.2.1：数据源、读口变化是中档；重档是展示 IA 或主路径大改，或增删需规叶子。本波不改卡片排法、不改三个入口的字、不增删叶子、不改展示接线、不建正式表。换到 ADS 是目标读法，正好落在「数据源、读口条件变化」，不升重档。中档不表示「展示已经只读 ADS」已经可签收。

## 异议

[arch] C2-1 · 问题：第 2 节表把 205 趋势留在 `stats`，把四张卡的卡面、全景、影响、深度报告改成展示只读 ADS、中台不走展示路径；第 7.6 节再写成两条链。同节流程图仍把「205 热点影响深度报告」接到 `gkxlumen-element` → `gkxlumenx_gapfill`，紧接着的正文仍写热点、影响、深度报告读缺项表。第 4.3 节仍写这三项不进 Python，由 `jobs` 让 element 读缺项表原样返回。热点不在四张卡的加工里，可以继续读缺项表；影响、深度、卡面、全景不能再留在这条边上。照图实现会让展示打开重新进缺项表，和「展示不加工、不调模型」相反。 · 依据：`POL-L2-DS10-TREND-ARCH.md` 第 38–39 行、第 56 行、第 62 行、第 4.3 节（约第 117–119 行）、第 7.6 节（约第 314–317 行）；硬清单 arch 第 1 问。 · 建议：流程图把「205 热点」单独接到缺项表；卡面、全景、影响、深度改成中台写 `demo_gkxlumenx_ads`、展示目标读 `gkxlumenx_ads`，并注明本波展示这条边不启用。第 4.3 节「三项不进 Python、`jobs` 读缺项表」标明已被第 7.6 节取代，热点除外。

[arch] C2-2 · 问题：中台链写 demo Java 透传，下一句却允许读演示 DWD 的 `policy_base_info`、`policy_industry_rel`，没有写是谁打开表。Java 不写正文、不调模型，挡不住 Java 自己去扫这两张表再把行插入 `demo_gkxlumenx_ads`。Java 读 DWD 按硬清单第 2 问停机。 · 依据：`POL-L2-DS10-TREND-ARCH.md` 第 7.6 节（约第 316 行）；硬清单 arch 第 2 问；调用链是前端 → Java → Python `/internal`，Java 不写正文、不调模型。 · 建议：改成只有 Python `/internal/policy/*` 读这两张演示 DWD，并只写 `demo_gkxlumenx_ads`。demo Java 只透传，不打开这两张表，不插入结果行。这句话没改之前，「Java 读演示 DWD」停机。

[arch] C2-3 · 问题：本波中台写入 `demo_gkxlumenx_ads`，展示要读的是 `gkxlumenx_ads` 同名表，而这张正式表本次不建，展示页不改接线。写入表和展示接口读的表不是一张表，本波也没有任何展示接口去读刚写入的那张表。第 2 节第 39 行和第 7.6 节仍把「展示只读 ADS」写成现行读法，和「正式表不建、接线不改」放在同一段。若为了让展示看见结果而让 lumen 去读 `demo_gkxlumenx_ads`，破 D12。若在正式表不存在时由接口返回写死的卡面、全景或报告，破 D18。新建 `gkxlumenx_ads` 正式表本次要停，不能靠本波建表把两条库接上。 · 依据：`POL-L2-DS10-TREND-ARCH.md` 第 39 行、第 7.6 节（约第 310、317、332 行）；说明书「#### 205」约第 94、179 行；D12（lumen 不读 demo 库、不调 demo 服务）、D18（接口必须读被写入的那张表）、新建正式库表要停机；硬清单 arch 第 3、4 问。 · 建议：第 39 行和第 7.6 节拆成两句。本波：展示读口不动，不读 `demo_gkxlumenx_ads`，不建 `gkxlumenx_ads`，不用旧缺项行或写死句子充当中台结果。目标：正式表作为停机项获批并建表之后，展示 Java 只读 `gkxlumenx_ads` 同名表；行进入正式库的动作不由 lumen 读演示库完成。D18 在目标句落地前，不签「展示已经只读 ADS」。
