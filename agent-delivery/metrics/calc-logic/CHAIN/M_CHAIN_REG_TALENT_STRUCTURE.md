# M_CHAIN_REG_TALENT_STRUCTURE 人才结构（学术力叶子）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（①主值+分布双形态 ②分母=有学历记录学者 ③只做学历维 ④覆盖率强制披露）
- **类型**：STAT（占比 + 分桶分布）
- **is_mock**：true（scholar_org_id 未灌走名称轨；灌数后切主轨转 live）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 区域产业评价页（`TOPIC-REG-017`），主项"人才结构"，子项"**学术力叶子**"（QC11 临时四力：学术力=科研机构/高校论文/人才结构，权重 8/100）。UI 现状 `industryRegionalModel.ts:213` sourceLabel="人才库"，叶子底分为 Mock 哈希偏移，无真实计算。
- **A1 需规**：`ALGO-CHAIN-DEEP-126` 区域产业指数模型——输入含"人才数据"；"对接…人才数据及配套服务数据等多源信息"。
- **白话**：深圳这条链周围有多少产业相关人才、其学历层次构成（博士/硕士/学士），衡量区域研发"人脑子"厚度，学术力第三叶。
- **跨指标关系**：
  - `M_CHAIN_ACADEMIC_POWER` 学术生态：三维之一"人才储备"=学者去重数；**本指标是其学历结构细分叶子**；
  - `M_CHAIN_SZ_TALENT` 深圳人才维度：**同库先例**——"综合水平=有学位记录者硕博占比"（分母口径同源）；
  - Q103（`M_TALENT_STRUCT_QUERY`）：查询态先例"学历为主分箱"；
  - TAL-B04 缺口卡：**职称/年龄无专核，禁止发明职称/年龄结构 M_***。

## 2. 指标定义（v0.2.0）

**主值**：指定区域内、链上高校与科研机构所属学者，按**最高学历**互斥分桶（博士/硕士/学士/未知）后的**硕博占比** =（博士+硕士）/ 有学历记录学者 × 100%。
**分布（下钻）**：四桶 counts + 占比；未知桶单独展示、**不进分母**。
**覆盖率披露（拍板④，用户 2026-10-14 识别覆盖率偏差后定）**：
- 指标卡**强制同显**"学历覆盖率 = 有学历记录学者 / 链上学者总数"；
- 覆盖率 < 50% 挂 ⚠️"低覆盖样本"角标；≥ 50% 干净展示；
- 禁止只报占比不报覆盖率——unknown≠低学历，录入缺失不得冒充全量结论，也不得反向当非硕博（D9 不伪闭合）。

## 3. Formula（SQL）

```sql
SELECT
  ROUND(100*SUM(bucket IN ('博士','硕士'))/NULLIF(SUM(bucket<>'未知'),0),1) AS master_phd_ratio,
  ROUND(100*SUM(bucket<>'未知')/COUNT(*),1)                               AS edu_coverage,
  SUM(bucket='博士') AS phd, SUM(bucket='硕士') AS master,
  SUM(bucket='学士') AS bachelor, SUM(bucket='未知') AS unknown_cnt
FROM (
  SELECT s.scholar_id,
    CASE WHEN eb.degree_zh LIKE '%博士%' THEN '博士'
         WHEN eb.degree_zh LIKE '%硕士%' THEN '硕士'
         WHEN eb.degree_zh LIKE '%学士%' OR eb.degree_zh LIKE '%本科%' THEN '学士'
         ELSE '未知' END AS bucket          -- 一人多记录 GROUP BY 取最高（博士>硕士>学士）
  FROM dwd_scholar s
  JOIN (SELECT name_cn FROM dwd_org_heis_info      WHERE city=:region_city AND is_deleted=0
        UNION ALL
        SELECT name_cn FROM dwd_research_institute_base_info WHERE city=:region_city AND is_deleted=0) org
    ON s.scholar_org_name_zh LIKE CONCAT('%',org.name_cn,'%')   -- 过渡轨；scholar_org_id 灌数后切等值连
  LEFT JOIN dwd_scholar_education_background eb
    ON eb.scholar_id=s.scholar_id AND eb.is_deleted=0 AND eb.degree_zh<>''
  WHERE s.is_deleted=0
  GROUP BY s.scholar_id                       -- 学者去重
) t;
```

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_org_heis_info` / `dwd_research_institute_base_info` | 高校+院所主档，city 区域轴 | 与 Seq13 RESEARCH_ORG 同源同构 |
| `dwd_scholar`（ODS） | 学者主档 | 21,316 学者；**scholar_org_id 全空**（0/21316）=数据未灌 → 名称轨过渡 |
| `dwd_scholar_education_background` | 学历明细 | 39,142 行；degree_zh 自由文本 100+ 种（"博士/哲学博士/理学硕士/学士学位…"），空 9,825 行；15,851 学者有学位记录（全局覆盖 74%） |
| `dwd_scholar_talent_flag` | 院士标签（仅 academician=112） | 无职称/无年龄 → 不发明（TAL-B04） |

**深圳实测**（名称轨）：194 链上学者（深圳大学 88 / 中科院深圳先进院 35 / 哈工大深圳 20+…）→ 有学历记录 28（**覆盖率 14.4%**）→ 最高学历分桶 博士 27 / 学士 1 / 硕士 0 / 未知 166 → **硕博占比 96.4%**（展示必同框覆盖率 14.4% + ⚠️）。
**一人多学历实锤**：29 人逐记录分桶得 63 人次（27博+15硕+21学）> 29 → 必须按最高学历归桶（15 硕士均兼有博士记录）。

## 5. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| scholar_org_id 全空 | 数据未灌（字段在案） | 名称轨过渡；灌数后切 org_id 等值连、指标转 live |
| 学历覆盖率深圳 14.4% | 样本性缺失（全局 74%） | 不报缺；覆盖率披露机制兜底；数据工厂补录自然抬升 |
| 职称/年龄结构 | 无源、禁发明（TAL-B04） | 本版只做学历维；三方库到位再扩（升版） |
| 链上人才直挂（entity_rel 无 talent） | 无源 | 走高校+院所主档间接归属（与 Seq13 同构） |

## 6. 验证记录（2026-10-14）

- 主值+覆盖率一次查询双出（master_phd_ratio / edu_coverage 同框），UI 只需一条 SQL 的结果集。
- 分桶互斥性：GROUP BY scholar_id + CASE 最高学历优先级，63 人次 → 28 人零重叠。
