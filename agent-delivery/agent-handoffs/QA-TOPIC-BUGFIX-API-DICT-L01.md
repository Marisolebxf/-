# QA-TOPIC-BUGFIX-API-DICT-L01 · A 类编码泄漏根因（接口 VO / 字典）

## 任务认领

| 字段 | 值 |
|------|-----|
| supervised_by | `human:徐滕强` |
| agent | `api-agent` |
| 前置 | 与 `QA-TOPIC-BUGFIX-FE-L01` 字段对齐；前端兜底已落地，本单修根因后可删兜底 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 问题清单（根因在 Java VO，非前端字典 store）

| BUG-ID | 接口/场景 | 现象 | 修复要求 |
|--------|-----------|------|----------|
| 027-002 | `POST .../key-analysis/region-insight` → `type_structure[].tag_name` | 饼图/「查看 xxx 清单」为 tag_code | 返回中文 `tag_name`（join 企业标签字典），code 仅作 id |
| 027-007 | `POST .../sz-status/city-benchmark` → `rows[].object_name` | 下拉/雷达/表为 110000 等 | 完备 `object_name`（含 NATIONAL→全国）；区划码仅 id |
| 028-004 | `POST .../sz-status/enterprise-list` 等清单 VO | 详情抽屉标题为 org_id | 清单项与详情接口均带 `name_cn` |
| 028-006 | 招引推荐结果契约 | 「本次筛选/权重说明」为英文键 | 结果 DTO 回显可读中文或提供 code→name 映射段 |
| 028-008 | 培育推荐结果契约 | 同 028-006 | 同左 |

关联用例：FUNC-00385、FUNC-02120、FUNC-02104、FUNC-01414、FUNC-02195。

## 前端兜底位置（联调通过后评估删除）

| 文件 | 兜底行为 |
|------|----------|
| `TypeRegionPanel.vue` | `tagStore.resolveTagName` |
| `CityBenchmarkPanel.vue` | `OBJECT_NAME_BY_CODE` |
| `EnterpriseSzStatus.vue` | 清单行补 `name_cn` |
| `recruitDisplay.ts` | `resolveRecruitFilterLabel` / `RECRUIT_WEIGHT_LABELS` |

## 联调闸门

1. `USE_MOCK=false` 30892 复测上表 BUG + source_case
2. 与孔东确认 FE 兜底可保留一版或移除
3. note 写「联调通过」+ trace_id 回填 bug-registry

## DoD

- [ ] 上表 5 项 VO/契约在 dev 环境可验证
- [ ] handoff 更新 + task-registry cost 回填
