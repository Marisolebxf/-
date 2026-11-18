# KG-GRAPH-RECALC-02 · 技术点层指标重算与榜单刷新归档

任务：KG-GRAPH-RECALC-02（派单 B，P0）。执行 human:韩梦蕊（Claude Code 辅助），监管 human:唐绍祖。2026-11-18。

## 数据基线

全部结果基于 **2026-11-18 新快照**（19,430 点 / **587,252** 条 tech_rel 边行，KG-GRAPH-COVER-01 补齐 +45,824 条之后），
不是 T09/T10 的旧快照（541,428 边）。快照经 counts 前后守卫与 SHA256 校验（`snapshot-metadata.json`）。
点文件哈希与 T09 快照完全一致（A 包未改点属性）；边文件哈希为新值。
离线计算，不连图库、不发写语句；对图库的全部访问只有两次只读分页导出（快照 + community_id 补充导出）。

587,252 行全部为唯一无向点对（**0 重复对、0 自环、0 空置信度**，`verification.json` quality 门全零），
因此 +45,824 行 = +45,824 个唯一点对，T09-S1 README 声明的「入射=入+出」等价关系在新快照上继续成立。

## 交付文件（七项数据面 + 证据）

| 文件 | 行数 | 说明 |
|---|---:|---|
| `degree-full.json` | 19,430 | 428 无权度整榜（入射边计数，`degree`） |
| `weighted-degree-full.json` | 19,430 | 中台 1 加权度整榜（`weighted_degree_recomputed`，入射边 Σ(confidence/100)，degreeBasis=weight_sum_incident，口径未动） |
| `degree-1500.json` | 1,500 | 新度 Top1500 人口的无权度（对照 T09-S1 同名件） |
| `pagerank-full.json` | 19,430 | 431 PageRank 整榜（alpha=0.85、tol=1e-8、max_iter=1000、confidence 加权，nx 同 T09） |
| `closeness-1500.json` | 1,500 | 429 紧密中心性（新度 Top1500 诱导子图、无权、wf_improved=True） |
| `betweenness-1500.json` | 1,500 | 430 中介中心性（同子图、k=300 采样、seed=42、normalized、无权） |
| `composite-recomputed.json` | 1,500 | 432 综合榜：**四项全部按新数据重算**（T09-S1 版只换 degree、沿用旧 429/430/431 原值——差异见 scope.difference_from_T09-S1），min-max 同人口归一后各 0.25，rank 1..1500 连续、score 单调降 |
| `community-partition.json` | 19,430 | Louvain python-louvain、seed 42、resolution 8.0、全边无权（T10 B′ 同参同实现）：282 群（181 成形 + 101 单点），模块度（nx 同 T10 读数口径）0.2867 |
| `community-summary.json` | 282 | 435/437 行：规模 / 内部边（无序点对去重）/ 平均度 2E/N / 密度 2E/(N(N-1))（单点群 null）/ 核心点 Top5（全图度） |
| `KG-GRAPH-RECALC-02-435-社群属性汇总.md` | — | 上表的人类可读渲染（成形 181 行全表） |
| `community-id-check.json` | — | 范围④：图内 community_id 对拍（以图内为准） |
| `diff-summary.json` | — | 范围⑤：四张 diff 表（新增点 / 分值变化 Top20 / 排名变动 Top20 / 社群迁出迁入） |
| `verification.json` | — | 全部门检、握手恒等式、独立对拍、旧档不变证明、版本与脚本哈希 |
| `snapshot-metadata.json` | — | 新快照 manifest 副本 |
| `recalc02_export_community_ids.py` / `recalc02_run.py` | — | 可复跑脚本（凭据只走 GKX_GRAPH_USER/GKX_GRAPH_PASSWORD） |

行结构与 T09-S1 归档一致（`rows[{rank,id,name,…}]` + `metric_source` + `scope.population_count`），T12 契约透传方式不变。

## 关键数字（对旧版）

- 边：541,428 → 587,252 行 = +45,824（全部新点对）；13,812 个点度数变化；ΣΔ度 = 91,648 = 2×45,824（恒等式精确成立）。
- 锚点「生物序列比较计算方法」：度 2,914 → **3,378**（+464），加权度 1,478.05 → **1,766.95**（+288.90）。
- Top1500 人口：1,458 点沿用，42 出 / 42 入。
- 社群：成形 180 → **181**（+0.56%，±10% 内，未改口径）；总数 287 → 282；单点 107 → 101；模块度 0.2786 → 0.2867。
- 图内 community_id（tgc_* 源表值，1,731 群 / 23 成形）：与本次 partition 不同源（结构性差异，moved 15,165），
  与 T10 签收 partition 也不同源（moved 15,319）。**以图内为准**，差异条数已记录；434/437 若切换新 partition，社群编号会变（T12 §4.3 已预留该语义）。

## 验证（verification.json，全部通过）

快照完整性；质量门四零；SQLite 独立无序点对对拍（19,430 点全量，加权最大误差 1.3e-11）；
无权握手 Σ度=2×587,252、加权握手 Σ加权度=2×Σ(conf/100)；PageRank Σ=1 且不动点残差 < N×1e-8；
综合榜逐行归一化复算与 rank 连续单调；Louvain 覆盖 19,430 点；435 汇总 Σ规模=19,430；
节点集合与旧版逐点相同（无新增/消失点）；T09-S1 / T09 / T10 旧档执行前后 SHA256 不变（只新增不覆盖）。

## 复跑

```bash
# 1) 导新快照（约 6 分钟，只读；凭据走环境变量）
GKX_GRAPH_USER=… GKX_GRAPH_PASSWORD=… python3 -c "…"   # 见主文「生成命令」节
# 2) 导图内 community_id（本目录脚本，只读分页）
GKX_GRAPH_USER=… GKX_GRAPH_PASSWORD=… python3 recalc02_export_community_ids.py <快照目录>
# 3) 离线重算 + diff（不连库；输出目录须为空）
python3 recalc02_run.py
```

环境：networkx 3.4.2、numpy 2.2.6、scipy 1.15.3、python-louvain 0.16（与 T09/T10 同实现栈）。
快照目录 `.local/kg-recalc02-20261118/` 不入 git（仓库仅提交派生指标数据与证据），其他环境复算须按批准方式取得与 manifest 哈希一致的快照。
