# 推荐企业数（M_ENT_RECOMMEND_COUNT）

> 口径真源：seed「推荐指数 ≥ 阈值的去重企业数」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：只挂两条 **推荐指数**（MODEL），不挂 demo 评分。  
> **不强行结项**：阈值 Q015 未定；指数本波无出数；无正式落表。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（强制）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_ATTRACTION_INDEX` | 招引推荐指数（MODEL，本波不算） |
| 2 | `M_ENT_CULTIVATION_INDEX` | 培育推荐指数（MODEL，本波不算） |
| 3 | 本条 | `COUNT(DISTINCT org_id) WHERE 指数 >= :threshold` |

**不挂** `M_ENT_ATTRACT_SCORE` / `M_ENT_CULTIVATE_SCORE`（demo 评分，不是指数）。

## 元数据

- **指标ID**：`M_ENT_RECOMMEND_COUNT`
- **指标名称**：推荐企业数
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：招引 / 培育名单规模
- **更新频率**：周（随指数批次）
- **对齐状态**：依赖已钉两条指数；阈值未定；无落表
- **是否在数据库**：正式无指数表、无本条计数表；仅 demo `svc_attraction_recommend` mock
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q015（阈值与权重；本条只用阈值，不定数字、不升 🟢）

## 口径定义

**招引推荐企业数** = 招引指数 ≥ 阈值的 `org_id` 去重数。  
**培育推荐企业数** = 培育指数 ≥ 阈值的 `org_id` 去重数。

指标名是一条「推荐企业数」：页面按招引 / 培育场景各读一个数。是否把两名单 UNION 成一个合计：**待后续**，本波不拍、不写进 8 件套公式。

- 阈值 = Q015，本波不定。没有阈值就不能 WHERE。
- 只国内（指数叶未并国外）。
- 选产业：先随指数过滤后再 COUNT，本条不自己 JOIN 链。
- **禁止** `COUNT(*)` demo `svc_attraction_recommend` / `svc_cultivation_recommend`。
- **禁止**读 `ent_cultivate_candidate` 行数当本条（名单表 ≠ 指数过阈计数）。
- **禁止**用 demo 评分冒充指数。

## 落表

| 目标 | 粒度 | 写什么 | 现网 |
|------|------|--------|------|
| `enterprise_recommend_summary`（建议名） | 场景一条（招引 / 培育）或一行两列 | `attract_recommend_count` / `cultivate_recommend_count` | **缺口：无此表** |

指数本身也无正式落表（demo 才有 `svc_attraction_recommend.attraction_index`）。GDF 暂缓，不建 DDL。待后续讨论。

## 分场景 / 实现方案

### 场景 A · 招引名单规模

指数落表后：`COUNT(DISTINCT org_id) WHERE attraction_index >= :threshold` → 写招引列。

### 场景 B · 培育名单规模

同理用 `cultivation_index`。

### demo / 生产

demo 有 mock 指数表，**不算接通**。生产：周任务等指数批次写入后再 COUNT，禁止请求路径扫全量现算 MODEL。

对应 seed `formula`：过阈 COUNT + **当前无法执行**。

**计算公式文件**：`M_ENT_RECOMMEND_COUNT.md`

## 源表字段

8 件套 `source_tables`（二次，右端 `metric:`；左端指数落表待建，不写 demo `svc_*`）：

```
<- metric: M_ENT_ATTRACTION_INDEX
<- metric: M_ENT_CULTIVATION_INDEX
```

左端表名未定（指数无正式落表），不把 `svc_attraction_recommend` 写进 8 件套。

产出（待建）：`enterprise_recommend_summary`。

来源系统：国内机构要素库、产业链要素库（只经指数间接；政策匹配维还依赖政策库，本条不直连）。

## 现网探针（2026-08-28；不进 8 件套）

- 正式 `gkxlumenx_ads`：无招引/培育指数表；仅 `chain_layout_recommend`（产业链，不是本条）。
- demo：`svc_attraction_recommend`（含 `attraction_index`）、`svc_cultivation_recommend`。
- `gkxlumenx_topic_enterprise.ent_cultivate_candidate`：名单，不是计数结果。
- 无 `enterprise_recommend_summary`。

## 待建 / 缺口（本波只暴露，不结项）

1. 两条指数 MODEL 本波无出数、无正式落表。
2. Q015 阈值未定。
3. 无本条目标表。
4. 招引/培育两个 COUNT 是否再 UNION：待后续。
5. D3 / D4 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.7`；STAT。禁止 demo mock 行数假接通。禁止挂 SCORE。

---
*2026-08-28 COVER-STAT-L01 二次 COUNT 挂两条指数；缺口暴露；不结项*
