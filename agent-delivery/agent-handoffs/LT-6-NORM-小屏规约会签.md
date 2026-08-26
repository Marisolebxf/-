# LT-6-NORM · 小屏规约会签（C1–C7）

> 时间：2026-08-26  
> 确认人：`human:孔东`  
> 规范真源：`agent-delivery/Design-mobile.md` v1.0（文首「已确认决议 C1–C7」与下表同文）  
> 体验补签：`human:高颖`（轻量，可后补）

## 决议

| 编号 | 决议 |
|------|------|
| C1 | 手机主库维持 `@arco-design/web-vue`，不换 Vant；密度用 CSS 拉到 44px |
| C2 | App 级滑入侧栏 + 页内底 Tab；不用 Tabbar 做一级 IA |
| C3 | 专题独立仓 `lumen-ui-topic-mobile`。时机：人工全量复制 science-mobile 后再按仓删减 |
| C4 | 产品门只认 `PHONE_MAX_PX=767`；360/430 仅页内密度 |
| C5 | 不下发红线用 Design-mobile §10；观感上限用 `小屏AI出效果备忘.md` |
| C6 | 两仓统一 Vue Router **history**（nginx `try_files`） |
| C7 | 专题小屏内部演示；对外验收仍 PC；Q030 未绿不改权限清单屏幕列 |

## 任务 × 文件 / 仓

| 任务 | repo（目标） | design_refs 应含 |
|------|--------------|------------------|
| `FE-SMALL-SHELL-L01` | `lumen-ui-science-mobile` | `agent-delivery/Design-mobile.md` · `repos/lumen-ui-science-mobile/docs/小屏断点与裁剪规则.md` |
| `FE-SMALL-AI-SPIKE-L01` | `lumen-ui-science-mobile` | 上列 + `repos/lumen-ui-science-mobile/docs/小屏AI出效果备忘.md` |
| `FE-DISPLAY-SMALL-BATCH-A` | `lumen-ui-science-mobile` | Design-mobile + 断点规则 + AI 备忘 |
| `FE-DISPLAY-SMALL-BATCH-B` | `lumen-ui-science-mobile` | 同上 |
| `FE-TOPIC-SMALL-ENT-L01` | **`lumen-ui-topic-mobile`**（原误写 `lumen-ui-topic`） | Design-mobile + 断点规则 §4 + AI 备忘 |
| `FE-TOPIC-SMALL-CHAIN-POL-L01` | `lumen-ui-topic-mobile` | 同上 |
| `FE-TOPIC-SMALL-SVC-COMP-L01` | `lumen-ui-topic-mobile` | 同上 |
| `FE-LARGE-PENDING-L01` | `gkx-orchestration` | 不引用 Design-mobile |

`task-update-fields` 不能改 `repo` / `design_refs`。本叶用 `note` 写下目标关联；`repo` 字段请 coordinator 改 TOPIC 三叶。

## 已回写文档

- `agent-delivery/Design-mobile.md` v1.0
- `agent-delivery/Design.md` §11 / §14
- `agent-delivery/architecture-baseline.md` D4 + 拓扑
- `agent-delivery/repo-registry.yaml` · `paths.yaml`
- `系统-06-多端小屏.md`

## ponytail

`ponytail: off`（定义/会签，不写业务代码）
