# 企业名称维护与核心成果管理展示统一

交付标识：20261105-enterprise-cms-achievement。ponytail: full。

## 范围与实现

用户前端新增基础档案`enterprise_name`及`star_core_achievement`，后端原先忽略名称、未知成果类型；展示侧已有“技术优势→科研成果”，只有`research_results:string[]`，并未接CMS新增成果。

- CMS档案表增量添加可空`enterprise_name`以兼容旧记录。基础档案携带名称保存时，同事务合并`cms_entity_overlay.field_overrides.name`，记录审计；企业视图与管理列表即刻回显，DWD/ES不写。字段不传时不重写原名称。
- 核心成果新建`cms_ent_star_core_achievement`，按企业+产业绑定，`achievements` JSON记录`achievement_name/achievement_type/achievement_year/achievement_summary`。类型限定patent/paper/award/project/product/other，必填和年份校验；复用用户态CRUD、发布/下架、软删除和审计。
- 添加`GET /cms/cms-ops/v1/enterprise/content/published-profile?future_industry_code=...&enterprise_code=...`，与运营接口采用同一Bearer鉴权，无新增匿名路由/权限。只返回该产业该企业已发布且未软删的名称与成果，草稿不公开。
- 前端移除核心成果unsupported标记、映射rows至achievements；基础档案从企业名称缓存回填，保存后同步标题。
- 现有明星展示“科研成果”统一名为“核心成果”，优先显示已发布CMS结构化条目；无CMS时兼容已有research_results。名称头部与当前企业图谱使用已发布名称。切企业/产业时清空旧数据并取消过期响应，未选择具体INB产业时不猜产业、不混用其他产业正文。

## 迁移与契约

- `lumen-svc-platform/db/9zz_gkxlumenx_cms_core_achievement.sql`。
- `scripts/apply_core_achievement_schema.py`检查information_schema后添加名称列，成果表CREATE IF NOT EXISTS；仅CMS增量，迁移已执行。
- 旧档案名称不强制补齐；其他内容类型、核心成果以前的文本展示数据均保留。

## 验证与提交

- 本地Java67项相关回归通过（服务41、元数据18、榜单5、成果3）；成果必填/类型/年份、已发布限定与范围、名称只合并CMS并审计覆盖。
- 前端type-check、生产build、cmsOpsMap字段往返（名称与成果四字段）、cmsRankWiring组件回归通过。
- 后端`cff9e6a`，前端`3ae7268`已推origin/dev；工作区其他会话文件未提交覆盖。
- 待记录：CI部署和线上名称临时修改/恢复、成果草稿隔离/发布回读/下架回退验收。
- 不伪造task-registry或成本记录；当前未提供对应MCP。浏览器视觉验收不等同API回归。
