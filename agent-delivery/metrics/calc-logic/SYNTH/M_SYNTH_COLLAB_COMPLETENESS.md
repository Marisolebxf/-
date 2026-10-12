# 协同网络完整度（M_SYNTH_COLLAB_COMPLETENESS）

> 口径真源：算法 2026-09 回填 → `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：有效边跟 `M_SYNTH_COLLAB_RELATION_INPUT`；本条只做覆盖比。  
> Q-SYNTH-C-01 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-SYNTH-seed.yaml`。

## 依赖（强制）

| 顺序 | 指标 / 集合 | 本条用它做什么 |
|------|-------------|----------------|
| 1 | `M_SYNTH_COLLAB_RELATION_INPUT` | 有效合作边（联合专利 / 合作项目 / 人才流动，门槛在那一叶） |
| 2 | 分析窗口主体全集 | 进入该区域×时间窗链路的 企∪科研机构∪人才（含无边） |
| 3 | 本条 | 有边主体数 / 全集 ×100 |

有效边门槛不在本条重写。上游仅联合专利有 DWD；合作项目/人才流动、主体名册、本条目标表都是缺口。三种边不齐 **不是** 三种齐全的完整度。

## 元数据

- 指标ID：`M_SYNTH_COLLAB_COMPLETENESS`
- 名称：协同网络完整度
- 模块：E8 区域创新协同
- 更新频率：随关系输入批次
- 关联Q：Q-SYNTH-C-01

## 口径定义

所选区域、对比范围、时间窗口内：

```
N = COUNT DISTINCT subject
    WHERE subject ∈ {企业, 科研机构, 人才}
      AND subject 进入本窗口链路

n = COUNT DISTINCT subject
    WHERE subject ∈ N
      AND 至少 1 条有效合作边
      （边 <- metric: M_SYNTH_COLLAB_RELATION_INPUT）

completeness = n / N × 100
```

- 分母**含**无边主体（算法钉）。
- N=0：该次无法计算。n=0 且 N>0：完整度=0。
- 去重键：主体 ID（企/院/人各自唯一键，不对三类混一个码）。
- 选区域 / 窗 / 对比范围是 API。
- **禁止**用密度、中心度、INDEX 冒充本条。禁止把边数当分子。

## 两点分开（强制）

### ① 本条口径

公式完整。RELATION_INPUT 出有效边、窗口有主体名册就能除。现网缺两路边 + 无名册，**不能当三种协同已算完**。

### ② 有没有表

无合作主体/边 ODS、无独立名册：标缺口。**不写「当前无法执行」替代口径**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `<- metric: M_SYNTH_COLLAB_RELATION_INPUT` | 输入叶未出数 |
| 主体全集 | 建议 `ads.synth_collab_subject`（窗口+主体） | **缺口：无此表** |
| 目标 | `ads.synth_collab_completeness`（区域+窗+完整度） | **缺口：无此表** |

源 ≠ 目标。本波不建 GDF DDL。旧 `pending_ods_*` 名不当 FROM。

## 分场景 / 实现方案

### 场景 A · 跑批

窗口定死后：拉全集 N → 用 RELATION_INPUT 边打标 → n/N。生产禁止请求路径全图现算。

### 场景 B · 改区域/年

API 换窗必须重算，禁止抄全库一条完整度。

### demo

演示完整度 **不算接通**。

**计算公式文件**：`M_SYNTH_COLLAB_COMPLETENESS.md`

## 源表字段

```
<- metric: M_SYNTH_COLLAB_RELATION_INPUT
```

无 ODS 右端。`source_systems` 不写 `Mock @ batch`。主体名册缺口只在细稿。

## 待建 / 缺口

1. RELATION_INPUT：现网仅联合专利有表；`coop_project` / `talent_flow` 无对等 DWD。
2. 窗口主体名册表（`ads.synth_collab_subject`）无。
3. **无独立目标表**（`ads.synth_collab_completeness`）。
4. D2/D3/D4 本波不升。`is_mock: true`。

---
*2026-09-07 COVER-STAT-L01：0.3.1 formula 写明上游仅专利一路、无名册、无目标表*
