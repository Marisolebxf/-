# M_CHAIN_REG_TECH_BARRIER 区域技术壁垒（技术力叶子）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（①kind DDL 钉死 ②空白=占比 ③封锁单窗口简化 ④rel DDL 确认+名称过渡轨）
- **类型**：MODEL（两子项合成，负向——进 M_CHAIN_TECH_POWER 时取 1-x）
- **is_mock**：true（rel 0 行走名称过渡轨；灌数后切 org_id 轨转 live）

## 1. 原始定义档案

- **页面语境**：区域产业评价页 `TOPIC-REG-014`，技术力叶子（QC11 四力，权重 8/100）。页面硬约束：**不得用 M_CHAIN_TECH_BARRIER_INDEX（关键环节侧）顶替**。A1 需规 `ALGO-CHAIN-DEEP-126`。
- **白话**：深圳这条链上的企业技术上被卡得多惨——空白（做不出授权发明）+ 封锁（技术方向被同链其他区域隔离）。
- **参考文献**：常晓涵, 何海燕, 等. 关键核心技术壁垒对中国产业链升级的影响[J]. 北京理工大学学报, 2023, 25(6)（Rosenkopf-Almeida 欧氏距离）。

## 2. 指标定义（v0.2.0）

**区域技术壁垒 = (空白得分 + 封锁得分) / 2**，两子项各自同链各区域截面 min-max 到 0–100。

- **kind 语义（拍板①，DDL 注释钉死）**：A=发明申请、**B=发明授权**、U=实用新型授权、S=外观授权；**kind=D（51.9 万件）= 外观设计，等同 S 对待**（human:徐滕强 2026-10-14 二次拍板）。
- **空白子项（拍板②）**：区域链上企业中，统计年及此前连续 3 年（共 4 年度窗）`kind='B'` 且 granted_number 非空的授权量为 0 的企业**占比** ×100（原稿区域级 0/1 太脆，单企业抖动即翻转）。
- **封锁子项（拍板③，简化方案）**：统计年及前推 2 年（3 年窗）`main_classification_ipcr` **首字母 8 大维**占比向量；区域每家链上企业（有 IPC）vs 同链其他区域企业两两欧氏距离取均值；无 IPC 企业剔除，区域全无 IPC → 子项空值不进合成。**砍掉原稿"距离较上期变大记 1"**（两期窗口依赖 + 二值抖动）。
- **链路（拍板④）**：`enterprise_industry_chain`(chain_code) → `dwd_org_base_info`(org_id 等值连 + city 区域筛) → 专利关联。

## 3. Formula（SQL 骨架）

```sql
-- 区域链上企业集合（org_id 全键）
SELECT e.org_id, b.name_cn
FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
JOIN demo_gkxlumenx_ods.dwd_org_base_info b
  ON b.org_id = e.org_id AND b.is_deleted = 0 AND b.city = :region_city
WHERE e.chain_code = :chain_code;

-- 专利关联（过渡名称轨，patent_id 去重）：
--   LEFT JOIN dwd_patent p ON p.first_current_assignee_name = b.name_cn AND p.is_deleted=0
-- rel 灌数后切换（org×patent 去重）：
--   JOIN enterprise_patent_org_rel r ON r.org_id = e.org_id
--        AND r.party_role IN ('APPLICANT','ASSIGNEE')
--   JOIN dwd_patent p ON p.patent_id = r.patent_id AND p.is_deleted = 0

-- 空白：100 * (无授权企业数 / 链上企业数)，窗=统计年及前3年 kind='B'
-- 封锁：IPC 首层占比向量（8维）欧氏距离均值（Python 侧计算，同链跨区域）
-- 合成：两子项 min-max 0-100 后等权平均；进 TECH_POWER 合成取 1-x
```

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd.enterprise_industry_chain` | 链桥 | **2000 行已灌**：INB1309=1984 / INB1204=8 / INB1354=7 / INB1323=1；深圳×INB1309=1004 家（org_id 实测通） |
| `dwd_org_base_info` | 主档区域轴 | 189,116 行 org_id 唯一 |
| `dwd_patent` | 专利主档 | 293 万条 patent_id 全唯一；ipcr 覆盖 82.4%；pbdt_year 2021–2026；kind∈{A,B,D,U}（B=35.3万 授权发明） |
| `dwd.enterprise_patent_org_rel` | org_id 专利关联 | **DDL 满足需求**（patent_id+org_id+party_role APPLICANT/ASSIGNEE+party_sequence，uk 四元去重）；**0 行待灌** |
| ~~`dwd_org_industry_tags`~~ | 老链路 | 104 行/73 企业与主档 **0 命中**（名称、信用代码都 0）——老 B 轨名称匹配链路在 demo 库已断，废 |

## 5. 缺口分型与待办

| 项 | 分型 | 处置 |
|---|---|---|
| `enterprise_patent_org_rel` 0 行 | 数据未灌（DDL 在案且已确认满足） | 名称过渡轨；灌数即切 org_id 轨 |
| rel.patent_id(general_ci) vs dwd_patent.patent_id(0900) collation 不一致 | 结构不一致（轻度） | 灌数时按用户通则 ALTER utf8mb4_0900_ai_ci（demo/正式/设计文档三同步） |
| kind='D' 51.9 万件 DDL 注释未列 | 语义已拍板：=外观设计，等同 S | 不影响本指标（本指标只用 B）；全局口径供其他指标引用 |
| `industry_chain_metric_dist` ADS 0 行 | 结果表未产出 | 派单计算任务后落 ADS |

## 6. 验证记录（2026-10-14）

- 深圳×INB1309 org_id 全键链路实测 1004 家（CAST 双侧 utf8mb4_0900_ai_ci 归一连通）。
- 293 万专利 ipcr 覆盖率 82.4%，封锁子项可用样本充足。
- 6 年公开窗满足"统计年及前 3 年"空白判定窗。
