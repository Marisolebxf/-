# M_CHAIN_REG_POLICY_COVERAGE 政策覆盖率（链维 / 区域维）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（饱和加权 / 拆词防误判 / 分母 L1 / 国家级覆盖全国）
- **类型**：STAT（比例）
- **is_mock**：false（源表在案有数，端到端真值已实测）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 区域产业评价页（`CHAIN-TOPIC-REGIONAL.yaml` `row_id: TOPIC-REG-019`），主项"政策覆盖率"，子项"支撑力叶子"；页面约束"指数预设叶子；不得用门户 POLICY_MATCH_SCORE 或诊断口径顶替"；上游合成条 `M_CHAIN_REG_ECOSYSTEM` / `M_CHAIN_SUPPORT_POWER` 引用。
- **兄弟条目先例**（`M_CHAIN_REG_COMP_SUPPORT` v1，2026-08-27）："政策覆盖率=相关政策覆盖环节占全链环节数比例"，title/keywords/keypoints/theme 四列文本匹配。
- **白话**：深圳在这条链的 6 个主环节里，政策铺得有多全、多厚。

## 2. 指标定义（v0.2.0）

**政策覆盖率 = Σ(hit_i / (hit_i + 5)) / L1 环节总数 × 100%**

- `hit_i` = 命中第 i 个 L1 环节的有效政策数（区域池含国家级）；
- 饱和参数 k=5：政策越多环节分越高、渐近 1 不爆表（拍板 ①：政策多的环节加分）；
- 分母 = 该链 L1 实体链环节数（拍板 ③：采用链环节定义；INB1701=6，`dwd_industry_chain_info.level=1`）；无命中环节贡献 0；
- 输出 0–100% 纯比例，分档交 UI。

### 命中判定（拍板 ②：拆词但不拆细）

- 匹配面：政策 `title`（keywords/keypoints/theme demo 零填充——0/0/2 行，口径保留待灌，当前仅 title 承重）；
- 词表 = **环节名实体词**（算法侧维护：半导体、集成电路、通信、超高清、智能终端、软件…），环节内多词 OR；
- 停用词剔除（与/及/应用/视频/信息服务/新型）；**泛词不入表**（"网络"、"终端"单独出现不匹配）——实测"网络"一词引入 18 条误判（52→34）；
- 政策与环节多对多：一条政策命中多环节，各环节各计各的，不跨环节去重。

### 政策池（拍板 ④：国家级覆盖全国）

`is_deleted=0 AND status='有效' AND (city = :region_city OR ((city IS NULL OR city='') AND rank LIKE '%国家级%'))`

## 3. Formula（SQL）

```sql
-- 内层：各环节命中数
SELECT l.industry_link_code, COUNT(DISTINCT p.id) AS hit_cnt
FROM demo_gkxlumenx_ods.dwd_industry_chain_info l
JOIN demo_gkxlumenx_ods.dwd_policy_base p
  ON p.is_deleted = 0 AND p.status = '有效'
 AND (p.city = :region_city
   OR ((p.city IS NULL OR p.city = '') AND p.`rank` LIKE '%国家级%'))
 AND (p.title LIKE CONCAT('%', :token_1, '%')
   OR p.title LIKE CONCAT('%', :token_2, '%'))   -- 该环节实体词 OR 展开
WHERE l.is_deleted = 0 AND l.industry_code = :chain_code AND l.level = 1
GROUP BY l.industry_link_code;

-- 外层：覆盖率 = Σ(hit_i/(hit_i+5)) / COUNT(L1 环节)
```

## 4. 表依赖与实核（2026-10-14 demo 库）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_policy_base` | 政策池 | demo 20,000 行（is_deleted=0 全部、status 全"有效"）；city 非空 10,294 / 深圳 879 / 国家级 2,174；rank 为 JSON 数组串（省级 7,449/市级 6,149/…）；**live gkxlumenx_ods 无此表 = 跨库差异注记，非缺口**（2026-08-18 ENT 域观测的即 live 侧） |
| `dwd_industry_chain_info` | 链与 L1 环节字典 | INB1701 L1=6 / L2=26；全局 15 链 L1 合计 28 |
| 环节词表 | 命中判定载体 | 算法侧维护（环节名→实体词组），非库表 |

## 5. 验证记录（2026-10-14，深圳 × INB1701）

| 环节 | 实体词 | 命中政策数 | 贡献 (hit/(hit+5)) |
|---|---|---|---|
| 新型网络与通信 | 通信 | 34 | 0.87 |
| 软件与信息服务 | 软件 | 27 | 0.84 |
| 半导体与集成电路 | 半导体/集成电路 | 18 | 0.78 |
| 超高清视频与显示 | 超高清/显示 | 6 | 0.55 |
| 人工智能与应用 | 人工智能 | 5 | 0.50 |
| 智能终端 | 智能终端 | 1 | 0.17 |
| **加权覆盖率** | | | **61.8%** |

对照：二元口径（命中即 1）= 6/6 = 100%，已无区分度——证明拍板 ① 加权的必要性。全串 LIKE（"半导体与集成电路"整串）= 0 命中，证明拆词必要性；"网络"泛词引入 18 条误判（52→34），证明拍板 ② 防误判必要性。

## 6. 关联条目

- `M_CHAIN_REG_COMP_SUPPORT` / `M_CHAIN_SUPPORT_POWER`：上游合成条引用本输出；其 formula 中"政策命中率/全链环节数"二元描述在复审时按本条加权版对齐（本轮不动）。
