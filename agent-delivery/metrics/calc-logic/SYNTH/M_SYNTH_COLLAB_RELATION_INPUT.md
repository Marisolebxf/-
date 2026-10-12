# 协同关系输入统计（M_SYNTH_COLLAB_RELATION_INPUT）

> 口径真源：算法 2026-09 回填（临时默认，未甲方签）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> 本条出**有效合作事件**。`M_SYNTH_COLLAB_COMPLETENESS` 读这些事件当有效边。  
> Q-SYNTH-C-01 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-SYNTH-seed.yaml`。

## 依赖

联合专利走已有专利 DWD（与 `M_ENT_PATENT_TOTAL` 同表）。合作项目、人才流动无对等 DWD，标缺口，不编表。

| 关系类型 | 匹配键 | 去重 | 有效门槛 |
|----------|--------|------|----------|
| 联合专利 | 专利申请号 | 同一专利多申请人合成一条事件 | 至少 2 个不同主体 |
| 合作项目 | 项目号 | 同一项目一条 | 至少跨 2 个机构 |
| 人才流动 | 人员唯一 ID + 机构变更时间 | 同一人同机构连续记录并一条 | 跨机构流动 ≥1 条起 |

口径三种都要算。现网**只有联合专利有 DWD**；合作项目、人才流动标缺口，不算已接通。输出粒度=**事件**（`relation_event_id`）。完整度把事件两端主体当有效边，不在本条改成边 COUNT。

## 元数据

- 指标ID：`M_SYNTH_COLLAB_RELATION_INPUT`
- 名称：协同关系输入统计
- 模块：E8 区域创新协同
- 更新频率：随源批次
- 关联Q：Q-SYNTH-C-01

## 口径定义

窗口内：

```
对每种 relation_type ∈ {joint_patent, coop_project, talent_flow}：
  COUNT(DISTINCT relation_event_id)
  GROUP BY relation_type, region, window
```

事件怎么成：

```
joint_patent:
  relation_event_id = 专利申请号
  申请人去重后 DISTINCT subject ≥ 2 才进

coop_project:
  relation_event_id = 项目号
  DISTINCT 参与机构 ≥ 2 才进

talent_flow:
  relation_event_id = person_id + 机构变更时间
  同人同机构连续记录先合并
  必须跨机构，1 条起算
```

- 选区域 / 窗是 API。
- 单主体专利、单机构项目、未跨机构的任职变动：**不算**。
- **禁止**把完整度、密度、中心度当本条。禁止数 demo 边。

## 两点分开（强制）

### ① 本条口径

三种门槛齐就能按类型 COUNT。现网只有 `joint_patent` 有表；后两种门槛写着，**不算能完整出三种数**。

### ② 有没有表

- 联合专利：`enterprise_patent_detail` 已有，申请人来自 `dwd_patent_assignees`。按申请号聚申请人，`COUNT DISTINCT org_id`（或权利人）≥2 即事件。灌数空是缺口，不进「无法执行」。
- 合作项目 / 人才流动：**缺口：无项目 DWD**。不编 `pending_ods_*` 当 FROM。这两种本波公式仍写门槛，数算不出来。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_patent_detail`（专利） | 有表；项目/流动无对等 DWD |
| 目标 | `ads.synth_collab_relation_input` 建议：`region + window + relation_type + event_count`；明细可另表 | **缺口：无此表** |

源 ≠ 目标。本波不建 GDF DDL。

## 分场景 / 实现方案

### 场景 A · 跑批

现网只洗专利一路 → 按门槛成联合专利事件 → 按类型+区域+窗 COUNT。`coop_project` / `talent_flow` 无源则该类型不出数（空，不当 0 假装扫过）。生产按窗分区，禁止请求路径扫全库。

### 场景 B · 给完整度

本条事件两端主体 = 有效边。完整度不重写门槛。

### demo

演示事件数 **不算接通**。

**计算公式文件**：`M_SYNTH_COLLAB_RELATION_INPUT.md`

## 源表字段

```
enterprise_patent_detail <- ods: dwd_patent
enterprise_patent_detail.assignee_name <- ods: dwd_patent_assignees
```

计算 FROM 只用左端。来源系统：国内机构要素库、国外机构要素库（与 `PATENT_TOTAL` 同）。项目库 / 人才库无对等 DWD，不进 `source_tables`。

## 待建 / 缺口

1. 合作项目、人才流动明细 DWD（专利已有 `enterprise_patent_detail`）。
2. **无独立目标表**。
3. D2/D3/D4 本波不升。`is_mock: true`。

---
*2026-09-07 COVER-STAT-L01：0.3.2 8 件套 formula/definition 写明项目/流动缺口*
