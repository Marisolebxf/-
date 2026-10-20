# GDF 协作指南

> **读者**：辜少彬、胡森泉、GDF 产线、徐滕强、本侧 data / 架构（所有和 GDF 对接的人）  
> **日期**：2026-08-13  
> **机器规约**：`.cursor/rules/gdf.mdc`  
> **花名册**：`agent-delivery/team-roster.yaml`（`human:辜少彬` / `human:胡森泉`）

本文是给人看的。Cursor 会话里提一句「按 GDF 协作指南」即可把边界带进 agent。

---

## 1. 三句话

1. GDF 是本项目的 **表 ETL + 编排平面**，不是软件研发组。
2. **辜少彬**管平台和调度；**胡森泉**管「配 GDF」变成可复用 Skill 和配置知识。
3. 胡森泉的成功标准：后面的人才 / 专题 / 政策等维度，以及以后接同一套 GDF 的项目，**只需少量人工验证**，不再需要第二个他。

---

## 2. GDF 在本项目的位置

架构 D7：三方源不进契约面。经数据工厂转换后，ADS 以上零改动。

```text
承诺表 doc/*.xlsx
    → 供应方 gkx（只读，仅 dwd_*；禁止供应方内部 ods_*）
    → Wave A 贴源镜像 → gkxlumenx_ods
    → Wave B Mapping  → gkxlumenx_dwd（DDL 认派单包 10/，字段认 Mapping 明细）
    → GDF DAG 编排 → 触发 ADS/ES（本项目 Python）/ 亿集建图 API
Java 只读 ADS；在线查图走 Java → Python → 亿集。GDF 不直写图库、不改前端/Java。
```

库边界（2026-10-19，全文 [`库边界-产线与中台-2026-10-19.md`](库边界-产线与中台-2026-10-19.md)）：

- 产线库 `gkxlumenx_*`（口头 lumen_xxx）：**我方先建表**，GDF 只往已有表贴源、洗数。
- 中台库 `demo_gkxlumenx_*`（口头 demo_lumen_xx）：我方开发代码只连这套。
- 两套库分开授权、分开验收，互不写入。缺表停工交我方，不另开库、不在中台库建表。
- 本条覆盖 2026-10-14 会前材料 §5.4「中台按明细建表」。

两张 CDC：

| 文件 | 模板名 | 含义 |
|------|--------|------|
| `1、贴源_*.xlsx` | `SRC_DB_CDC_TEMPLATE` | Wave A |
| `2、明细数据_*.xlsx` | `DWD_CDC_TEMPLATE` | Wave B |

本侧生成带 `预填-DRAFT`。GDF 导入跑通回传的才叫 `执行结果/`。填写规则见同目录 [`CDC模板填写规则与预填算法.md`](CDC模板填写规则与预填算法.md)。

---

## 3. 人怎么分工

| 人 | 管 | 不管 |
|----|----|------|
| **徐滕强** | 项目 DWD / ADS 契约；`data-agent` 默认监管 | 在 GDF 里配作业 |
| **辜少彬** | GDF 组织、平台、调度、告警、门 1 列席 | 替甲方拍口径；改业务仓代码 |
| **胡森泉** | Skill、`scripts/gdf-cdc`、GDF 配置知识、派单包改到 **GDF 整包跑通** 并回写规则；MCP 领任务、写 handoff | 创建任务；改公约 / 花名册 / 前端 / Java / 算法 |

指标口径仍归王惠 / 王惠；复杂算法归唐绍祖；图谱融合归亿集，GDF 只调 API。

---

## 4. 胡森泉主责（Skill Owner）

1. **维护技能**（真源 `.cursor/skills/gkx-gdf-cdc-workpack/`，脚本 `scripts/gdf-cdc/`；`.codex/skills/` 只是指针，先改 Cursor 那份）。
2. **沉淀本项目 GDF 常用配置**（占位符 `#ODS_SCHEMA#` 等、数据源名 `GKX_DB` / `EDW_ODS` / `SRC_ENT`、CDC 壳与索引列、六技术字段、`is_deleted = 0`、连接约定）。密码不进 Git。
3. **用跑通反哺自动化**：缺表、字段对不上，在该派单包内自己改到 GDF 能完整跑通（不必先升级徐滕强 / 辜少彬）。可复用部分必须写进 Skill hard rule 或本目录知识页。只改 xlsx 不算完成。缺表进「没找到的表」，不要当已下线从 `02` 删行。

---

## 5. 环境（GDF 成员）

**不要**跑 `scripts/bootstrap.ps1`，**不要**打开 `gkx-lumen.code-workspace`（16 根）。

1. GitLab：只申请 **`gkx-orchestration` Developer**。不要组级 Developer，不要 `lumen-*` / `demo-*` 写权限。胡森泉账号：`husq`。登录：`https://aminer-edu-gitlab.jyzhang.cn`。
2. 只 clone 编排仓。
3. Cursor：`File → Open Workspace from File` → `workspaces/gdf.code-workspace`（与 `orch-only` 相同，仅主仓）。
4. `.env` 填 `GKX_ROOT` 即可。不需要 PAT 去拉业务仓。
5. 确认 MCP 里有 `task-registry`（认领 / 改状态用，禁止手改 yaml）。

git commit 标记：`[human:胡森泉]` / `[human:辜少彬]`。`user.email` 建议能对上 GitLab 账号，否则路径门禁可能认不出 `husq`。

---

## 6. 目录与真源

| 用途 | 路径 |
|------|------|
| 本指南 | `agent-delivery/data/GDF/GDF协作指南.md` |
| 对外派单包 | `agent-delivery/data/GDF/派单包/{域}/GDF-*-WORKPACK-vN/` |
| 企业现行包 | `派单包/企业/GDF-ENT-WORKPACK-v2/`（投递状态以该包 README 为准） |
| Wave A 表清单 | 包内 `02-WaveA-贴源表清单.yaml` |
| Mapping | 包 README 指定的 `09-*Mapping明细*`（短版导读不当字段矩阵） |
| DWD DDL | 包内 `10-DWD-MySQL-DDL/` |
| CDC 预填草稿 | 包内 `预填作业/` |
| GDF 回传 | 包内 `执行结果/` + `05` 回签 |
| 连接 / 过滤 | 包内 `03` / `04`（口令线下，不进仓） |
| 分层用词 | 包内 `01-命名与分层词典.md` |

施工只认该包现行 `02` / `09` 明细 / `10`。禁止用已作废 v1 回件当表清单。`GDF/Mapping/` 平行目录已删除，不要再建。

---

## 7. 任务：接受、执行、handoff

只领 **已 `ready`** 且属于 Skill / 派单包 / GDF 配置知识的叶子。**不创建任务**（`task-create` 归 coordinator / PM）。

Cursor 里用 MCP：

| 动作 | 工具 |
|------|------|
| 查找 | `task-query` / `task-get` |
| 认领 | `task-claim`：`claimed_by=human:胡森泉`；agent 执行时 `supervised_by=human:胡森泉` |
| 推进 | `task-update-status` |
| 回填 cost 等 | `task-update-fields` |
| 阻塞 | `task-set-blocked` |

完工写 `agent-delivery/agent-handoffs/{task-id}.md`（模板 `templates/handoff-template.md`），填 `ponytail:`。Skill / 脚本用 `full`；知识页 / 回签用 `off`。

`.cursorignore` 会挡住直接打开 `task-registry.yaml`，这是故意的。

---

## 8. 日常两种会话

会话开头固定：「只改 GDF 白名单路径；按 GDF 协作指南。」

1. **跑通**：对该派单包改 `02` / `09` / `10` / CDC，导入 GDF 直到整包绿。对照 DRAFT 与 `执行结果/` 用 officecli，不要把 xlsx 当文本改。
2. **沉淀**：把这次差异写进 Skill hard rule 或本目录知识页，并问一句「下一个维度能否少问人」。

预填命令（在 `gkx-orchestration` 根目录）：

```text
python scripts/gdf-cdc/parse_workpack.py --workpack "<包路径>" -o inventory.json
python scripts/gdf-cdc/fill.py both --workpack "<包路径>" --inventory inventory.json --out "<包路径>/预填作业"
```

禁止脚本写入 `执行结果/`，禁止覆盖 GDF 已回传文件。

---

## 9. Git：`husq` 可以提交什么

白名单：

```text
agent-delivery/data/GDF/**
.cursor/skills/gkx-gdf-cdc-workpack/**
.codex/skills/gkx-gdf-cdc-workpack/**
scripts/gdf-cdc/**
agent-delivery/task-registry.yaml
agent-delivery/agent-handoffs/**
```

越界由 CI 作业 `gdf-author-path-guard` 失败。`task-registry.yaml` 是整文件，只允许经 MCP 改自己的 GDF/Skill 任务。handoff 只交自己的 `task-id`。

保护分支：不要直推 `main`。开 MR，标题写清包名 / 技能变更。`CODEOWNERS` 中上述 GDF 路径 owner 为 `@husq`（需 GitLab 管理员打开「需要 CODEOWNERS 批准」才在合并时强制）。

辜少彬若也用 GitLab 提交：账号 `gusb` 补进花名册 `notes` 后再收紧；当前路径门禁只绑 `husq`。

---

## 10. 什么时候才升级

| 情况 | 找谁 |
|------|------|
| 包内缺表 / 字段对不上 / CDC 配不通 | **胡森泉自己闭环**，记 CHANGELOG，回写 Skill |
| 要改 `数据库设计.md`、ADS、Java、前端 | 徐滕强 / 对应 Lead |
| GDF 平台挂了、账号网络、调度告警策略 | 辜少彬 |
| 甲方业务口径 | PM → 客户决策清单，任何人不得代拍 |
| 架构铁律（调用链 / 直写图库） | 架构师 |

---

## 11. 开工检查表

- [ ] 只 clone 了 `gkx-orchestration`，打开的是 `workspaces/gdf.code-workspace`
- [ ] 读过本指南 + 现行派单包 `00` / `01` / `02` / `09` 明细
- [ ] MCP `task-registry` 可用
- [ ] GitLab 没有业务仓写权限
- [ ] 知道 DRAFT 与 `执行结果/` 的区别
- [ ] 第一次跑通后，差异已经写进 Skill 或知识页

---

## 12. 相关文件

| 文件 | 作用 |
|------|------|
| `.cursor/rules/gdf.mdc` | Cursor 角色规约 |
| `.cursor/skills/gkx-gdf-cdc-workpack/SKILL.md` | 生成 CDC 的步骤 |
| `CDC模板填写规则与预填算法.md` | 给产线看的填表规则 |
| `team-members.md` §6.5 | 编制与三项中台目标 |
| `architecture-baseline.md` D7 | 数据工厂与契约面 |
| `data-lineage-policy.md` §2.2 | Phase 2 由 GDF 做 ODS→DWD 映射 |
| `designs/houtai-arch-discussion.md` 第五轮 | GDF 编排面 vs 亿集能力面 |
