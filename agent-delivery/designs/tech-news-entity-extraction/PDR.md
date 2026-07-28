# 科技资讯实体与事件抽取预研（PDR）

> **Task**: `E-TECH-NEWS-ENTITY-PDR-L01`  
> **Epic**: `E-TECH-NEWS-ENTITY-PDR`  
> **阶段**: definition / 沙箱预研（仅 `demo-algo-science`）  
> **监管**: `human:孙英哲` · **执行**: `agent:algorithm-agent`  
> **版本**: v0.1 · 2026-07-27  
> **前置**: `E-TECH-NEWS-IE-M1` 四要素抽取已落地（公司/时间/事项/影响）

---

## 1. 目标与边界

### 1.1 目标

在已有「科技新闻四要素」抽取之上，预研扩展：

1. **7 类实体**：公司、科研机构、政策、产业、技术、专家学者、专利  
2. **事件结构增强**：事件类型、日期、资讯来源（与四要素兼容）  
3. 对齐招标口径：科创事件 + 命名实体识别（见 §5）

### 1.2 非目标（本 PDR 不做）

- 不进 lumen 正式仓 / 不上 Java 门面  
- 不做生产级 NER 模型训练  
- 不替代四要素 API（并行扩展：`/internal/tech-news/entity-extract`）  
- 不替甲方拍板「产业」边界与「事件类型」枚举（登记 🟡，见客户决策清单）

### 1.3 架构合规

| 铁律 | 本预研 |
|------|--------|
| 算法只在 Python | ✅ `innov/tech_news_ie/entity_ext` |
| 调用链 前端→Java→Python `/internal/*` | ✅ 预留同前缀；本期只验 Python |
| demo 沙箱不 merge lumen | ✅ 仅 demo-algo-science + agent-delivery 设计 |
| Nebula / ADS 等 | ⏭ Wave1+ |

---

## 2. 与四要素的兼容策略（方案 A）

```
ExtractResponse (v1 四要素)          EntityExtractResponse (v0.1 扩展)
├─ events[]                          ├─ events[]          # 仍含四要素字段
│   company_name / time / matter /   │   + event_type
│   impact / evidence / confidence   │   + news_source
└─ meta                              ├─ entities[]        # 文级去重实体表
                                     └─ meta.schema_version = entity-v0.1
```

- **兼容**：`events[]` 继续可喂给现有复核 UI / ADS 草案  
- **扩展**：顶层 `entities[]` 供图谱/检索试点；`event_type` / `news_source` 供科创事件分类

真源文件：

- Schema：`schema-v0.1.json`  
- Prompt：`prompt-entity-v0.1.txt`  
- 运行时镜像：`demo-algo-science/innov/tech_news_ie/prompts/entity_extract_v0.1.txt`

---

## 3. 7 类实体定义（团队临时默认 · 🟡）

| type | 中文 | 临时默认边界 | 证据要求 |
|------|------|--------------|----------|
| `company` | 公司 | 企业法人/品牌主体（含「小米」「华为」等简称） | 原文 span |
| `research_org` | 科研机构 | 大学/研究院/实验室/研究所/科学院等 | 原文 span |
| `policy` | 政策 | 具名政策/规划/条例/办法（非泛称「政策支持」） | 原文 span 或规范简称 |
| `industry` | 产业 | 产业链/赛道名（如「新能源汽车」「半导体」） | 🟡 边界待甲方 |
| `technology` | 技术 | 具名技术/产品/型号/平台（如「玄戒O3」「澎湃OS」） | 原文 span |
| `expert` | 专家学者 | 人名 + 可选职务/机构 | 原文人名 |
| `patent` | 专利 | 专利名/公开号/「获批专利」对象 | 原文 span |

---

## 4. 事件类型（团队临时默认 · 🟡）

| event_type | 含义 | 线索词例 |
|------------|------|----------|
| `product_release` | 产品/平台发布 | 发布、推出、上线 |
| `tech_breakthrough` | 技术突破/攻关 | 突破、攻关、首创 |
| `delivery` | 交付/量产/投运 | 交付、量产、投运 |
| `certification` | 备案/认证/合规 | 备案、认证、准入 |
| `collaboration` | 合作/联合攻关 | 联合、签约、共建 |
| `policy_publish` | 政策发布 | 印发、出台、施行 |
| `other` | 其他科技事项 | — |

正式枚举须甲方确认（Q052）。

---

## 5. 招标对齐（差异与演进）

| 招标关注点 | 现状（四要素） | 本预研 | 演进 |
|------------|----------------|--------|------|
| 科创事件主体 | 公司/机构混在 `company_name` | 拆 `company` / `research_org` | 图谱点类型 |
| 命名实体 | 轻量 ORG NER | 7 类实体表 | Wave1 可接领域词典+LLM |
| 事件结构 | 事项+时间+影响 | +类型+来源 | ADS 事件宽表 |
| 日期 | `completion_time` | 复用，禁止用发稿日冒充完成日 | 保持 D8/口径 |

**差异标注**：招标「命名实体识别」偏通用 NER；本预研是**科技资讯业务实体**（含产业/政策），不是 BIO 全词性标注。

---

## 6. 沙箱原型验收

| 项 | 结果 |
|----|------|
| `POST /internal/tech-news/entity-extract` mock 可跑 | ✅ |
| Schema 草案 `schema-v0.1.json` | ✅ |
| Prompt 草案 | ✅ |
| ≥5 篇样例覆盖多实体组合 | ✅ `tests/tech_news_ie/entity_ext` |
| 业务口径 🟡 登记客户决策清单 | ✅ Q051 / Q052 |

---

## 7. 开放问题 / 下一步

1. 甲方确认产业边界与事件类型枚举后，冻结 `schema-v0.1` → `v1.0`  
2. ~~Wave1：LLM 模式实跑 + impact/entity 联合校验~~ → **已关闭（2026-07-28）**：智谱 `glm-4-flash` 对 `pdr_samples.json` **10/10** 实跑成功；证据 `innov/tech_news_ie/entity_ext/samples/pdr_llm_zhipu_20260728.json`；联合校验见 ENTITY-M3-L01  
3. ~~Wave2：Java 门面 + ADS~~ → 已由 ENTITY-M2 / M3 承接  

---

## 8. 产物清单

| 产物 | 路径 |
|------|------|
| 本 PDR | `agent-delivery/designs/tech-news-entity-extraction/PDR.md` |
| Schema | `.../schema-v0.1.json` |
| Prompt | `.../prompt-entity-v0.1.txt` |
| 代码 | `repos/demo-algo-science/innov/tech_news_ie/entity_ext/` |
| 样例+测 | `repos/demo-algo-science/tests/tech_news_ie/entity_ext/` |
| Handoff | `agent-delivery/designs/tech-news-entity-extraction/PDR-handoff.md` |
