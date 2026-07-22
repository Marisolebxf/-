# DS-25 软科学成果展示 · 数据可用性映射表

> **作用**：把 bid §1.1.1.1.4.6.1 软科学成果展示的需求字段，**精确映射到甲方已提供的真实 ODS 表字段**，避免 ux-agent / ui-agent / data-agent 凭空编造字段名
> **数据真源**：`agent-delivery/data/` 目录下甲方提供的三方采购数据「要素库」(186 张表 / 2253 字段 / v2 版本，2026-06-02 生成)
> **关键发现**：DS-25 不需要纯 Mock —— **核心字段 85% 可基于真实 ODS 表设计**，仅互动/传播/评价反馈类字段需自建用户态 DWD 表
> **必读者**：ux-agent / ui-agent / data-agent / algorithm-agent / api-agent
> **创建**：2026-06-17（PM 在 DS-25 试点启动前据数据真源建立）
> **关联**：
> - `agent-delivery/data/third-party-source/ODS源数据表结构清单(v2).md`（全 186 表清单）
> - `agent-delivery/data/third-party-source/gkx-mysql-raw/gkx_schema_ddl.sql（旧要素库SQL已删；现用三方DDL沙箱）`（精确 DDL）
> - `agent-delivery/data/GDF/Mapping/政策/政策相关-ODS到DWD字段映射分析报告(v2).md`（同类格式参考）
> - `agent-delivery/data-lineage-policy.md`（数据血缘 8 件套规约）

**映射状态图例**：
- ✅ **直接映射**：ODS 已有对应字段
- 🔧 **需算法**：ODS 有原料但需要 algorithm-agent 加工
- ⚠️ **待确认**：字段存在但语义需 PM + 数据 lead 与甲方对齐
- ❌ **无来源**：ODS 无对应字段，需自建用户态/业务 DWD 表
- 🟦 **系统/预留**：审计 / 权限 / 时间戳类字段，应用层自管

---

## 1. ODS 主要可用表（DS-25 直接相关）

| 表名（ODS） | 中文名 | 字段数 | 用于 DS-25 |
|------------|--------|--------|-----------|
| `dwd_zh_project` | 国内项目信息表 | 22 | **核心主表**：课题基本信息 |
| `dwd_zh_project_output` | 国内项目-产出信息 | 25 | **核心成果表**：论文/专利/报告/奖项数 |
| `dwd_rel_project_scholar` | 项目-人才关联 | 4 | 课题负责人/参与人 |
| `dwd_rel_project_paper` | 项目-论文关联 | 5 | 课题论文产出 |
| `dwd_rel_project_patent` | 项目-专利关联 | 4 | 课题专利产出 |
| `dwd_zh_report` | 中文科技报告信息表 | 20 | 课题阶段性报告 |
| `dwd_rel_report_project` | 报告-项目关联 | 5 | 报告与课题关联 |
| `dwd_org_reg_info` | 机构基本信息 | 25 | 承担单位详情 |
| `dwd_org_hels_info` | 高校/科研机构信息 | 21 | 承担单位详情（高校/研究所） |
| `dwd_macro_region_category` | 行政区划维表 | — | 省/市/区分级（地图层级） |

**注**：要素库 SQL 中以 `dwd_` 命名的表实际是**本项目 ODS 贴源层**（数据供应方的命名习惯），不要与项目自建 DWD 标准表混淆（见 `agent-delivery/数据库设计.md`）。

---

## 2. DS-25 子功能字段映射（按 bid §1.1.1.1.4.6.1 7 个三级功能）

### 2.1 §1.1.1.1.4.6.1.1 分布地图与趋势分析

| bid 需求字段 | 映射 | ODS 表.字段 | metric_id 建议 | 备注 |
|------------|------|------------|--------------|------|
| 课题地域分布（国家/省/市/区） | ✅ | `dwd_zh_project.funded_province` | 维度，非 metric | 当前 ODS 只到省级；市/区下钻需关联 `dwd_org_reg_info.address` 或 `dwd_macro_region_category` 补强 |
| 课题数量密度（热力图） | ✅ | COUNT GROUP BY `funded_province` | `M_SS_TOPIC_DENSITY_BY_PROV` | 聚合指标 |
| 单位维度聚集度 | ✅ | COUNT GROUP BY `funded_institution` | `M_SS_TOPIC_BY_INSTITUTION` | 聚合指标 |
| 节点弹窗：课题核心信息 | ✅ | `dwd_zh_project.title / approval_year / project_level / funded_amount / project_host` | 明细，非 metric | 直接展示 |
| 年度发展趋势 | ✅ | COUNT GROUP BY `approval_year` | `M_SS_TOPIC_NEW_COUNT_Y` | 时序指标 |
| 季度新增 | ✅ | COUNT GROUP BY QUARTER(`approval_time`) | `M_SS_TOPIC_NEW_COUNT_Q` | 时序指标 |
| 区域筛选与分布关联 | ✅ | `funded_province` | 维度 | UI 实现 |

**覆盖率**：6/7 ✅（市/区级地图下钻 1 项待确认）

---

### 2.2 §1.1.1.1.4.6.1.2 智能成果筛选与专题检索

| bid 需求字段 | 映射 | ODS 表.字段 | metric_id 建议 | 备注 |
|------------|------|------------|--------------|------|
| 年度筛选 | ✅ | `dwd_zh_project.approval_year` | 维度 | |
| 类别筛选 | ✅ | `dwd_zh_project.fund_category` + `project_level` | 维度 | |
| 单位筛选 | ✅ | `dwd_zh_project.funded_institution` | 维度 | |
| 地理区划筛选 | ✅ | `dwd_zh_project.funded_province` | 维度 | |
| 学科筛选（含软科学过滤） | ✅ | `dwd_zh_project.discipline / discipline_code` | 维度 | **关键**：用 discipline 字段过滤"软科学" |
| 智能关键词检索 | 🔧 | `dwd_zh_project.title / keywords / abstract` 全文 | — | 需 algorithm-agent 建立全文索引 |
| 标签推荐 | 🔧 | 抽取自 `abstract` + `keywords` | — | 需 NLP（algorithm-agent） |
| 热词发现 | 🔧 | 同上 | `M_SS_HOT_KEYWORDS_LIST` | 算法产出 |
| 历史筛选方案保存 | ❌ | — | — | 用户态，需自建 |
| 多维联动（地图 + 统计图） | — | 前端逻辑 | — | UI 实现 |

**覆盖率**：5 ✅ + 3 🔧 + 1 ❌ + 1 前端 / 共 10

---

### 2.3 §1.1.1.1.4.6.1.3 成果详情与案例展示

| bid 需求字段 | 映射 | ODS 表.字段 | metric_id 建议 | 备注 |
|------------|------|------------|--------------|------|
| 项目名称 | ✅ | `dwd_zh_project.title` | 明细 | |
| 承担单位 | ✅ | `dwd_zh_project.funded_institution` | 明细 | |
| 负责人 | ✅ | `dwd_zh_project.project_host` + 关联 `dwd_rel_project_scholar` | 明细 | |
| 立项年份 | ✅ | `dwd_zh_project.approval_year` | 明细 | |
| 难题类型 | ⚠️ | `dwd_zh_project.discipline` + 抽取 `abstract` | 明细 | 学科是基础，"难题类型"需算法 |
| 研究路径 | 🔧 | 抽取自 `abstract` | 明细 | 需算法 |
| 阶段性成果 | ✅ | 关联 `dwd_zh_project_output` 多维度（论文/专利/报告） | 明细 | |
| 附件下载 | ✅ | `dwd_zh_project.project_page_url` + `dwd_zh_report` | 明细 | |
| 难题攻关历程时间轴 | ⚠️ | `approval_time` → `research_period` → `dwd_zh_project_output.output_article_year` | 衍生 | 需自定义时间轴语义 |
| 典型难题案例推荐 | 🔧 | 文本聚类 `abstract` | `M_SS_TYPICAL_CASES_TOPN` | 算法 |
| 影响力评价 | 🔧 | 综合 `dwd_zh_project_output.*_count` | `M_SS_IMPACT_SCORE` | 算法（综合指数） |
| 应用反馈 | ❌ | — | — | 用户态评价，需自建 |

**覆盖率**：6 ✅ + 4 🔧 + 2 ⚠️ + 1 ❌ / 共 13

---

### 2.4 §1.1.1.1.4.6.1.4 多维统计与趋势分析

| bid 需求字段 | 映射 | ODS 表.字段 | metric_id 建议 | 备注 |
|------------|------|------------|--------------|------|
| 课题年度变化折线图 | ✅ | COUNT GROUP BY `approval_year` | `M_SS_TOPIC_NEW_COUNT_Y` | 同 §1 |
| 类型结构饼图 | ✅ | COUNT GROUP BY `fund_category` 或 `project_level` | `M_SS_TOPIC_BY_CATEGORY` | |
| 单位贡献度统计 | ✅ | COUNT GROUP BY `funded_institution` | `M_SS_UNIT_CONTRIBUTION_RATE` | 单位课题数 ÷ 全市总数 |
| 区域贡献度 | ✅ | COUNT GROUP BY `funded_province` | `M_SS_REGION_CONTRIBUTION_RATE` | |
| 资助金额分布 | ✅ | SUM(`funded_amount`) GROUP BY 多维 | `M_SS_FUNDING_TOTAL_Y` | |
| 难题领域分布 | 🔧 | 学科 `discipline` + 关键词聚类 | `M_SS_DOMAIN_DISTRIBUTION` | 部分算法 |
| 热点分析 | 🔧 | `keywords` 词频 | `M_SS_HOT_KEYWORDS_LIST` | 算法 |
| 自定义导出 | — | 前端能力 | — | UI 实现 |
| 时序回溯 | ✅ | `approval_year` 时间窗口 | 同上时序指标 | |

**覆盖率**：6 ✅ + 2 🔧 + 1 前端 / 共 9

---

### 2.5 §1.1.1.1.4.6.1.5 成果互动与传播中心

| bid 需求字段 | 映射 | ODS 表.字段 | metric_id 建议 | 备注 |
|------------|------|------------|--------------|------|
| 评论 | ❌ | — | — | 用户态，需自建 `dwd_user_comment` |
| 点赞 | ❌ | — | — | 用户态，需自建 |
| 答疑 | ❌ | — | — | 用户态 |
| 关注收藏 | ❌ | — | — | 用户态 `dwd_user_favorite` |
| 多渠道分享 | ❌ | — | — | 用户态行为日志 |
| 互动统计 | ❌ | — | — | 用户态聚合 |
| 影响力数据报告 | 🔧 | 综合 `dwd_zh_project_output` 学术影响 + 用户态社交影响 | `M_SS_INFLUENCE_INDEX` | 部分算法 |

**覆盖率**：6 ❌ + 1 🔧 / 共 7

> **重要建议**：本节几乎全部需自建用户态 DWD 表。**建议 Wave 0 试点阶段 ux-agent 对本节按"占位 UI + 标注待自建"处理**，不强求 metric_id，详细方案待 Wave 1 由 data-agent 决策是否纳入。

---

### 2.6 §1.1.1.1.4.6.1.6 数据导出与报告管理

本节为**应用层能力**（导出 / 报告生成 / 权限审计 / 多角色），不依赖 ODS 字段。

| bid 需求字段 | 映射 | 实现 |
|------------|------|------|
| 一键多格式导出 | — | 后端导出服务 + 前端调用 |
| 自动专题报告 | 🔧 | algorithm-agent + 模板渲染 |
| 行为追溯归档 | 🟦 | 应用层 audit 日志（Loki） |
| 多角色报表配置 | 🟦 | 应用层 RBAC + 表单引擎 |

**覆盖率**：纯应用层，UX 阶段画"导出按钮 + 权限提示"即可

---

### 2.7 §1.1.1.1.4.6.1.7 成果进展与跟踪监控中心

| bid 需求字段 | 映射 | ODS 表.字段 | metric_id 建议 | 备注 |
|------------|------|------------|--------------|------|
| 分阶段节点管理（立项/执行/结题/转化） | ⚠️ | `dwd_zh_project.approval_time` + `research_period` + `final_report_abstract` | 维度 | ODS 静态，**实时进度需自建** |
| 阶段成果归档 | ✅ | 关联 `dwd_zh_project_output` + `dwd_zh_report` | 明细 | |
| 分阶段评价反馈 | ❌ | — | — | 用户态 |
| 项目进展统计 | ⚠️ | `approval_year` 已立项数 + 结题状态 | `M_SS_PROJECT_PROGRESS_PCT` | 需 `final_report_abstract IS NOT NULL` 派生结题判定 |
| 预警机制 | 🔧 | 派生：研究期限超期未结题 | `M_SS_PROJECT_OVERDUE_LIST` | 算法 |
| 全周期历史溯源 | ✅ | `dwd_zh_project.updated_time` | 时间戳 | |

**覆盖率**：2 ✅ + 1 🔧 + 2 ⚠️ + 1 ❌ / 共 6

---

## 3. 总体覆盖率（DS-25 全 7 子功能）

| 子功能 | ✅ | 🔧 | ⚠️ | ❌ | 前端/系统 | 总数 | 真实数据覆盖率* |
|--------|---|---|---|---|----------|------|---------------|
| §1 分布地图 | 6 | 0 | 1 | 0 | 0 | 7 | **86%** |
| §2 智能筛选 | 5 | 3 | 0 | 1 | 1 | 10 | **80%**（含算法） |
| §3 详情案例 | 6 | 4 | 2 | 1 | 0 | 13 | **77%**（含算法） |
| §4 多维统计 | 6 | 2 | 0 | 0 | 1 | 9 | **89%** |
| §5 互动传播 | 0 | 1 | 0 | 6 | 0 | 7 | **14%**（多需自建） |
| §6 导出管理 | — | 1 | — | — | 3 | 4 | 应用层 |
| §7 进展跟踪 | 2 | 1 | 2 | 1 | 0 | 6 | **50%** |
| **总计** | **25** | **12** | **5** | **9** | **5** | **56** | **66%（直接） / 87%（含算法）** |

*覆盖率 = (✅ + 🔧 + ⚠️) / 总数；不含纯前端/系统字段

**结论**：
- 主流程（§1/§2/§3/§4 核心展示）真实数据可用性 **80% 以上**
- 互动传播（§5）需要 Wave 1 之后由 data-agent 自建用户态表
- 整体可以做"**真实 ODS 字段为骨 + Mock 填充值**"的高质量原型，**比纯 Mock 高一个台阶**

---

## 4. UX 阶段写 wireframe 时怎么用

### 4.1 字段表"来源"列填法

**旧（纯 Mock 写法）**：

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 课题名称 | string | 明细 | ✅ | "区块链..." | — |

**新（基于真实 ODS）**：

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 课题名称 | string | `dwd_zh_project.title` | ✅ | "区块链在政务中的应用研究" | — |
| 本季度新增 | int | `M_SS_TOPIC_NEW_COUNT_Q` | ✅ | 12 | `M_SS_TOPIC_NEW_COUNT_Q` |
| 单位贡献率 | float% | `M_SS_UNIT_CONTRIBUTION_RATE` | ✅ | 23.5% | `M_SS_UNIT_CONTRIBUTION_RATE` |

**统计字段**：来源列填 metric_id；**明细字段**：来源列填 `表名.字段名`；**待算法**：来源列填 `🔧 待 algorithm-agent` + ODS 原料表

### 4.2 wireframe 末尾"本页 metric_id 清单"扩展

```markdown
## 本页 metric_id 清单

| metric_id | 中文名 | source_tables (ODS) | 算法依赖 | 备注 |
|-----------|--------|---------------------|---------|------|
| M_SS_TOPIC_NEW_COUNT_Q | 本季度软科学课题新增数 | dwd_zh_project | 无（直接 SQL） | discipline LIKE '软科学%' AND QUARTER(approval_time) = current |
| M_SS_UNIT_CONTRIBUTION_RATE | 软科学课题单位贡献率 | dwd_zh_project | 无 | COUNT(*) by funded_institution / total |
| M_SS_HOT_KEYWORDS_LIST | 软科学热点关键词 | dwd_zh_project.keywords | 🔧 algorithm-agent NLP | 关键词词频 TopN |
| ... | | | | |
```

### 4.3 给 data-agent 的接力清单

UX handoff §11【数据血缘汇总】中应明确：

```yaml
data_agent_followup:
  cfg_metric_register:  # 需注册 ~15 个 metric_id（见 §2 表中所有 metric_id 建议）
    - id: M_SS_TOPIC_NEW_COUNT_Q
      source_tables: [dwd_zh_project]
      mock_until: 2026-10-01
    # ... 见 metric_id 清单全表

  user_state_dwd_tables_pending:  # 需自建用户态 DWD 表
    - dwd_user_comment_ss_topic   # 软科学课题评论
    - dwd_user_favorite_ss_topic  # 软科学课题收藏
    - dwd_user_view_log           # 浏览/分享行为日志

algorithm_agent_followup:  # 需算法的指标
    - M_SS_HOT_KEYWORDS_LIST: NLP 关键词词频
    - M_SS_TYPICAL_CASES_TOPN: 文本聚类
    - M_SS_IMPACT_SCORE: 综合影响力指数（学术 + 社交）
    - M_SS_PROJECT_OVERDUE_LIST: 超期预警
```

---

## 5. UI 阶段做 mock 数据时怎么用

### 5.1 mock JSON 字段名严格沿用 ODS

```json
// mocks/ss_topics.json (UI 实现时，30+ 条)
{
  "id": "ZH-2024-SS-0001",
  "title": "粤港澳大湾区数字经济治理创新研究",
  "project_source": "深圳市哲学社会科学规划项目",
  "funded_institution": "深圳大学经济学院",
  "project_level": "市级",
  "funded_amount": 8.0,
  "discipline": "软科学/管理学",
  "discipline_code": "G35",
  "funded_province": "广东",
  "approval_year": 2024,
  "approval_time": "2024-03-15",
  "project_host": "张三",
  "keywords": ["数字经济", "湾区", "治理创新"],
  "abstract": "本课题旨在...",
  "research_period": "2024-03 至 2026-03",
  "project_page_url": "https://..."
}
```

**好处**：未来 Wave 1 切真实数据，**前端代码零改动**（字段名一致）。

### 5.2 数据要"贴近真实"

- 课题名称**风格**对齐：政策研究 / 治理创新 / 战略评估 / 产业分析 类
- 单位**真实存在**：深圳大学 / 南方科技大学 / 中山大学（深圳）/ 深圳社科院 / 深圳综合开发研究院
- 资助金额**合理范围**：5–50 万（软科学一般金额）
- 学科**符合软科学范畴**：管理学 / 公共管理 / 应用经济学 / 社会学 / 政治学
- 立项时间**分布合理**：2018–2026 之间

### 5.3 mock_until + 切换路径

每个 mock 数据顶部加：

```json
{
  "_mock_meta": {
    "batch_id": "mock_20260617_seed42",
    "based_on_ods_schema": "dwd_zh_project v2 (2026-06-02)",
    "real_data_eta": "2026-10-01",
    "switch_mechanism": "cfg_degrade_switch.ss_topic_mock_mode = false"
  },
  "data": [...]
}
```

---

## 6. 关键开放项 → **甲方确认清单**（团队定不了）

> **重要原则**（团队公约 §3.1）：决策不外包给 AI；业务口径 / 范围承诺 / 数据定义 → **永远是甲方拍板**，不是 PM、不是数据 Lead、不是 agent。
> **流程**：试点期间团队按"团队临时默认值"先跑（让 UX/UI agent 不卡住），但**任何展示在界面上的指标 / 字段 / 范围都必须等甲方在下次评审/会议时正式确认**，否则不能上线。
> **此表用法**：PM 把本节直接发给甲方（或带去甲方汇报会），逐条勾选确认。

### 6.1 待甲方确认的 7 项

| # | 开放项 | 团队临时默认（先跑用） | 团队建议（供甲方参考） | 影响 | 甲方决策 | 决策时间 |
|---|--------|---------------------|---------------------|------|---------|---------|
| 1 | "软科学"如何精确过滤 `dwd_zh_project.discipline` 字段？ | `discipline LIKE '软科学%' OR '管理学%' OR '公共管理%' OR '应用经济%' OR '社会学%'` | 建议甲方提供权威"软科学学科目录"或参照《国家社科基金学科分类》 | 影响整个 DS-25 数据范围，所有指标 | ⏳ 待确认 | |
| 2 | 是否在自建 DWD 层做"软科学子集表" `dwd.dwd_ss_topic` | ✅ 做（discipline 过滤逻辑收口） | 利于性能 + 口径一致性，但需要 data-agent 多一道清洗工作 | 算法/api 性能；交付周期 | ⏳ 待确认 | |
| 3 | 市/区级地图下钻数据从哪来（ODS 只到省级） | 关联 `funded_institution` → `dwd_org_reg_info.address` 解析 | 是否要求市/区级精度？精度不足时是否接受省级地图 | UI 多级地图实现复杂度 | ⏳ 待确认 | |
| 4 | "难题攻关历程时间轴"业务语义？ | 立项 → 中期检查 → 结题（基于 `approval_time + research_period` 派生） | 是否有官方阶段定义（如"启动期/执行期/验收期"）？ODS 目前不含中期检查数据 | UI §3 时间轴展示形态 | ⏳ 待确认 | |
| 5 | 互动传播功能（§5 评论/点赞/收藏/分享）Wave 0 是否实现 | 占位 + 标记"Wave 2 后纳入" | ODS 不覆盖，需自建用户态表 + 用户体系；建议先占位，等 Wave 2 用户体系上线再做 | 范围 ±10%；交付周期 | ⏳ 待确认 | |
| 6 | 国外软科学课题 `dwd_en_project` 是否纳入 DS-25 | 默认不纳入（DS-25 = 国内） | bid 原文是"软科学成果"，未明确限定国内；建议确认范围 | 范围 ±10% | ⏳ 待确认 | |
| 7 | 项目"结题判定"逻辑 | `final_report_abstract IS NOT NULL` 视为已结题 | 是否有官方"结题状态"字段？或建议在 DWD 自建 `project_status` 派生字段 | §7 进展跟踪指标 | ⏳ 待确认 | |

### 6.2 PM 操作步骤

1. **本试点期间**（甲方未确认前）：UX/UI/data/algorithm agent 按"团队临时默认"先跑，**界面上对应的指标 / 区域加 ⚠️ 待确认 标签**
2. **下次甲方汇报时**：PM 把本表 §6.1 7 行打印 / 投屏，**逐条获取甲方书面或语音确认**，回填"甲方决策"列
3. **甲方确认后**：data-agent 把决策内容沉淀到 `cfg_metric.definition` 和 `data-source-mapping-registry.yaml`，**口径版本 bump**（如 `M_SS_TOPIC_NEW_COUNT_Q v1.0.0 → v1.1.0`）
4. **决策有冲突时**（甲方决策与团队临时默认值不同）：架构师 + 数据 Lead 评估返工成本，PM 决定是"立即返工"还是"延后到下一 Wave"

### 6.3 如果甲方暂时无法确认怎么办

| 情况 | 处理方式 |
|------|---------|
| 甲方说"你们先按经验来" | PM 书面回复："我们将按表中临时默认值实现，请贵方在 {date} 前给到正式口径，否则视为认可"。**保留邮件/微信截图**作为证据 |
| 甲方要求"等下次专家组会议" | PM 把本表 §6.1 列入下次专家组会议议程（提前 3 个工作日发议程） |
| 甲方多个对接人意见冲突 | PM 升级到甲方项目经理；不接受口头多意见，只接受**1 个甲方对接人书面/纪要的最终意见** |

---

## 7. retro 沉淀建议

试点完成后回填：

| 维度 | 内容 |
|------|------|
| 本表对 ux/ui/data agent 的帮助度 | |
| 未来其他 DS 试点是否复制本表格式 | |
| 数据 Lead 建议的字段映射调整 | |
| 与甲方确认后的真实"软科学"过滤口径 | |
| 甲方对 §6.1 7 项的实际确认时间与方式 | |
| 团队临时默认值与甲方最终决策的差异（返工成本） | |

---

**本表由 PM 与数据 Lead 共同维护；ux/ui/data/algorithm agent 在 wireframe / mock / cfg_metric 中均以本表为输入。**
**§6.1 7 项决策权归甲方**，团队角色（包括 PM）只能临时默认，不能最终拍板。
