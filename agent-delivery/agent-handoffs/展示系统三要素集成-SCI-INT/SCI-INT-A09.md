# SCI-INT-A09 科技创新评估集成卡

- task_id: SCI-INT-A09
- role: product-agent
- task_type: spike
- ponytail: N/A（spike 分析，无代码）

## 范围 / 卡片数 / 差集

科技创新评估（DS-07，excel 139–161）23 张集成卡，卡号 INT-A-X-0800–0822。

| 项 | 结果 |
|---|---|
| scope_count / card_count | 23 / 23 |
| excel | 139–161 各一行，无缺无重 |
| gap | `[]`，差集 0 |
| 自检 | `产物/_work/A09-check.py` 打印 OK（无 TBD、无 skeleton、卡号 800–899） |

调用链已按 `lumen-ui-science-pc/src/api/situation/innovationEvaluation.ts` 核实，不再写「草案」：

- Java：未实现。该文件只声明网关 `GET /situation/v1/innovation-evaluation/meta` 与 `GET /situation/v1/innovation-evaluation/snapshot`（payload 为 filters+weights JSON）；注释写明后端冻结后启用。
- Python：未实现。本文件无 `/internal/*`。
- downstream：未实现。本文件无 ADS、Nebula 或三方下游。
- 时间 / 地域粒度、更新频率：未实现。快照只提交整包，本文件未拆字段。
- demo：已接线。`USE_MOCK=true` 走 `@/mock/modules/innovationEvaluation`（demo 冻结种子）。
- `fe_route` 仍为 null：本文件无路由 path。页路径记在 `status.lumen`。

模式、政策保障力 IP-10、Q140、DS_07 三条 D12 未改写。

## 久新依赖

已挂 counterpart=jiuxin 的 3 张：

| 卡 | excel | 功能 | metric_id | 模式 | jiuxin_row_id |
|---|---|---|---|---|---|
| INT-A-X-0800 | 139 | 科学论文数量分析 | M_TECH_BASE_96_1 | IP-06 | SRS-96 |
| INT-A-X-0804 | 143 | 专利数量统计分析 | M_TECH_BASE_96_1 | IP-06 | SRS-96 |
| INT-A-X-0817 | 156 | 政策扶持力度分析 | M_ORG_DEEP_153_1 | IP-10 | SRS-153 |

页级久新三行在包内为「待确认」，卡片未挂 counterpart：DS-07-SCI-CREATE-003（前沿性，0802）、DS-07-TECH-INNOV-003（技术市场潜力，0806）、DS-07-INDUSTRY-POTENTIAL-002（技术产品成熟度，0811）。

## conflicts

Q140：政策与条件保障力 7 张（excel 155–161，INT-A-X-0816–0822）均记「Q140 用 M_INNOV_PG_*，页面映射用 M_POLICY_*，不拍板」。集成模式保持 IP-10。

## structure_escalation

23 张 `structure_escalation: false`，无升级 id。

DS_07 三条 D12 记在 risks，不升结构：

| 卡 | excel | metric_id |
|---|---|---|
| INT-A-X-0805 | 144 | M_TECH_DS_07_TECH_INNOV_002 |
| INT-A-X-0807 | 146 | M_TECH_DS_07_TECH_INNOV_004 |
| INT-A-X-0809 | 148 | M_TECH_DS_07_TECH_INNOV_006 |

口径：算法位置指向 demo-algo-science，须在 lumen-algo-py 重写。本叶未调用 demo 服务。

## metric_missing

`metric_ids: []` 共 9 张：

| 卡 | excel | 功能 |
|---|---|---|
| INT-A-X-0802 | 141 | 科学研究前沿性分析 |
| INT-A-X-0806 | 145 | 技术市场潜力分析 |
| INT-A-X-0808 | 147 | 技术创新空间分布 |
| INT-A-X-0810 | 149 | 产业投入分析 |
| INT-A-X-0811 | 150 | 技术产品成熟度评估 |
| INT-A-X-0812 | 151 | 产业产值分析 |
| INT-A-X-0818 | 157 | 经费支持分析 |
| INT-A-X-0819 | 158 | 项目支持分析 |
| INT-A-X-0822 | 161 | 政策优化建议 |

## 开放项（最多 3）

1. Q140 政策保障力口径（M_INNOV_PG_* 与 M_POLICY_*）未拍板，7 张保持冲突记录。
2. 9 张无 metric_id，不补挂、不伪闭合。
3. 久新页级三行仍为待确认，未挂 counterpart。

## 偏离

无范围偏离。调用链由「未实现（草案）」改为上述核实结论；demo 由未实现改为 mock 双轨已接线。

## 产物

- `产物/SCI-INT-A09.yaml`（23 张，草案句已改）
- `产物/_work/A09-check.py`（自检 OK）
- 本 handoff
- 未 commit

## 验收证据

`A09-check.py` 退出码 0，标准输出 `OK`。差集 0。

## 架构合规

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 无代码。D12 三条写明须在 lumen-algo-py 重写 |
| 调用链 前端→Java→Python | ✅ 前端只声明网关两条 GET；Java / Python / downstream 核实未实现，未越层 |
| Nebula，禁止 Neo4j | ✅ 未接图谱 |
| 可观测 | ✅ spike 无代码，无新埋点 |
| CI/CD | ✅ 未 push |
| demo 不 merge 进 lumen | ✅ 只读 API 文件，未改 lumen |
| 共享聚合 | ✅ 不适用 |
| Mock 不填正式数 | ✅ 只记录 USE_MOCK 双轨，未把种子写入契约响应 |
| D8 / D10 | ✅ 无 UI |
| D9 | ✅ 未改口径；缺指标保持空列表 |
| D12 | ✅ 三条风险已记；未把 demo-algo-science 当 lumen 下游 |

## 成本

| 字段 | 值 |
|---|---|
| actual_tokens | 90000 |
| model_used | grok-4.7 |
| actual_cost | 1.2 |
| cost_warn | green |

估算低于 $10，不暂停。
