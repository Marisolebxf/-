# M_CHAIN_INVEST_COUNT 投融资事件数 计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（方案A 融资事件同构 + 复合业务键去重 + 窗口参数化）
- **类型**：STAT（事件计数）
- **is_mock**：true（链桥 INB1309 mock 可算；全量挂链跟 CHAIN-P0-5）

## 1. 原始定义档案

- **页面语境**：链详情页"资本"区——这条链上发生了多少笔投融资事件。
- **白话**：链上企业（被投视角）的融资事件去重件数——谁融到了资、哪天、什么轮次。
- **旧稿问题**：v0.1.0 = `COUNT(DISTINCT news_id) WHERE news_type='financing'`——①`news_type` 字段实测不存在（90 行链新闻表无此列）；②拿新闻当投资事件源是语义借用；③QC07 🔴 挂起。**不可执行，废除**。

## 2. 指标定义（v0.2.0，方案A）

**指定产业链链上企业的融资事件去重件数（被投视角），与 `M_CHAIN_REG_FINANCING` 同构（去 region 换 chain_code）。**

| 决策点 | 拍板 | 说明 |
|---|---|---|
| ① 语义 | 融资事件（被投视角） | 与 REG_FINANCING / SUPPORT_POWER 融资维全族同尺；"投资方视角（对外投资）"未来另立指标（见 §4 QC07 处置） |
| ② 去重键 | 复合业务键 `(org_id, completion_date, funding_round)` | **业务去重规则 ≠ 物理唯一索引**：表无 event_id 无 UNIQUE 约束，同企业同日同轮可能多行，`SELECT DISTINCT` 塌缩成 1 件；同日同轮多笔碰撞风险如实注记；供应方补 event_id 后 DISTINCT 冗余可去、口径不动 |
| ③ 时间窗 | 默认全量 + 近 N 年查询参数 | `completion_date` 时间轴（FINANCING 先例同款） |
| ④ 链路 | org_id 全键：融资表 org_id → 链桥 org_id + chain_code | 禁名称匹配（2026-10-14 通则） |

## 3. Formula（SQL）

```sql
-- 全量版（口径本体）
SELECT COUNT(*) AS chain_fin_cnt FROM (
  SELECT DISTINCT f.org_id, f.completion_date, f.funding_round
  FROM demo_gkxlumenx_ods.dwd_org_financing_info f
  JOIN demo_gkxlumenx_dwd.enterprise_industry_chain e
    ON e.org_id = f.org_id AND e.chain_code = :chain_code
  WHERE f.is_deleted = 0
) k;

-- 近 N 年窗口版（查询参数，不进口径）：追加 AND f.completion_date >= :window_start
```

## 4. QC07 处置（🔴 → 🟡）

- 融资事件源已活：`dwd_org_financing_info` 25,654 行实测（completion_date 真业务日期 1963→2026、funding_round 干净中文枚举）；
- QC07 残余问题只剩**投资方视角无事件级源**：`dwd_org_invest_info`（46,967 行）是股权投资关系存量（org_id/inv_org_id/金额/占比），无事件日期、无轮次、无事件 id——"链上企业投了谁"若页面将来要，另立新指标（改名"对外投资关系数"），不混入本条；
- QC07 降 🟡 跟踪，不销项。

## 5. 执行模式建议

- 总量（无窗口）：预计算候选（ADS 快照）；
- 窗口查询：实时参数化 SQL（N 开放集合）；
- 量级评估届时用真实数据（2026-10-14 规则：量级不进口径）。

## 6. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_org_financing_info` | 分子（融资事件） | 25,654 行 / 6,503 家企业；completion_date 真业务日期；轮次中文枚举（股权投资/新三板/战略投资/A轮/IPO 等）；无 event_id（DDL 18 列实核） |
| `dwd.enterprise_industry_chain` | 链桥 | INB1309 mock 2000 行（深圳 1004 家 org_id 全键通）；余链 0 行 |

## 7. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 链桥仅 1 链 mock | 数据未灌 | 跟 CHAIN-P0-5；灌数即真数 |
| 投资方视角无事件级源 | 残余缺口 | QC07 🟡 跟踪；未来另立指标 |
| 旧稿 news_type 写法 | 字段不存在 | 已废除重写 |

## 更新记录

- 2026-08-24: 初版 v0.1.0（news_type 不可执行稿）
- 2026-10-14: v0.2.0 方案A 重写（human:徐滕强 拍板：融资事件同构 + 复合键去重 + QC07 降级）
