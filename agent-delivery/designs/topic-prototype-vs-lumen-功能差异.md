# 科技专题服务系统：原型 vs 正式前端功能差异（功能测试对照）

> **对照日期**: 2026-08-10  
> **原型**: `demo-ui-topic` @ `origin/dev` (`e07eb30`)  
> **正式**: `lumen-ui-topic`（GitLab: `lumen-ui-science-topic`）@ `origin/dev` (`26eb234`)  
> **方法**: 菜单/路由/页面代码盘点 + 部署 URL 可达性探测（非全量点击用例录屏）  
> **说明**: 按团队约定，`demo-ui-topic` 为 UX 沙箱；企业 Track-MS V2 在 lumen `dev` 直开，**禁止 merge 原型进正式仓**。

---

## 1. 结论摘要

| 维度 | 结论 |
|------|------|
| 覆盖范围 | **正式仓远窄于原型**：原型侧栏可见约 **5 大域 + 多个隐藏域**；正式仓侧栏目前仅 **「企业分析」1 组** |
| 企业域 | 正式仓已落地查询/对比篮/详情/评估/风险/重点/深企现状/引育等页面骨架；相对原型仍缺 **企业发展、维护管理、明星企业** 等入口 |
| 非企业域 | 产业链 / 政策 / 产业服务链 / 综合智能 / 技术链 / 科研机构 / 人才 —— **正式仓基本未挂菜单、无对应 views** |
| 技术栈 | 原型 React；正式 Vue3 + Arco（与展示 PC 栈对齐）——属预期差异，不是功能缺口本身 |
| 部署验证 | `http://10.50.69.111:30892` 本轮探测失败/不可达（历史 handoff 亦记录过 K8s API blocked）；**未能做线上点击级功能测试**，差异以代码对照为主 |

**一句话**：当前正式专题前端 ≈「企业分析子集的 V2 工程实现」；原型 ≈「全专题 IA 沙箱（多域完整菜单 + 大量页面）」——差距主要是**范围裁剪与未迁移模块**，不是单一页面小偏差。

---

## 2. 对照对象与环境

| 项 | 原型 `demo-ui-topic` | 正式 `lumen-ui-topic` |
|----|----------------------|------------------------|
| 本地路径 | `${GKX_ROOT}/repos/demo-ui-topic` | `${GKX_ROOT}/repos/lumen-ui-topic` |
| 分支 | `dev` | `dev`（本地曾停在 `main` 脚手架，本轮已切到 `origin/dev`） |
| 导航真源 | `src/app/components/Layout.tsx` → `navGroups` | `src/router/menu.ts` → `navGroups` |
| 路由 | `src/app/routes.tsx` | `src/router/routes.ts` + `buildNavRoutes()` |
| 目标 URL | 本地 Vite / 既有 demo 部署（视环境） | 设计 NodePort **30892**（`/topic`） |

---

## 3. 侧栏菜单对照（功能入口）

### 3.1 原型可见侧栏（`hidden: false`）

来源：`demo-ui-topic/src/app/components/Layout.tsx`

1. **产业链分析**  
   专题全景 / 产业查询 / 产业链全景图谱 / 产业运行诊断 / 区域产业评价 / 深圳产业决策 / 维护管理  
2. **企业分析**  
   企业发展 / 企业查询 / 重点企业分析 / 深圳企业现状分析 / 企业评估 / 风险洞察 / 引育推荐 / 维护管理  
3. **政策分析**  
   政策扶持 / 政策查询 / 政策时序分析 / 区域政策对比 / 深圳政策现状分析 / 维护管理  
4. **产业服务链分析**  
   专题服务 / 服务机构查询 / 服务机构分析 / 服务链生态分析 / 机构招引培育 / 维护管理  
5. **综合智能分析**  
   区域创新活力分析 / 区域创新要素分析 / 区域创新协同分析  

原型另有 **侧栏隐藏但路由保留** 的域：技术链分析、科研机构、人才分析（直达 URL 仍可能可用）。

### 3.2 正式仓侧栏（当前 `menu.ts`）

仅一组：

1. **企业分析**  
   - 企业查询  
   - 对比篮  
   - 企业评估  
   - 风险洞察  
   - 重点企业分析  
   - 深圳企业现状分析  
   - 引育推荐  
   - （不进菜单）企业详情 `enterprise/:orgId`

对应页面：`src/views/enterprise/*.vue`（Search / Compare / Detail / Evaluation / Risk / KeyAnalysis / SzStatus / Recruit 等）。

### 3.3 菜单差异矩阵

| 原型能力（侧栏） | 正式仓 |
|------------------|--------|
| 产业链分析整组 | ❌ 无菜单、无 views |
| 政策分析整组 | ❌ |
| 产业服务链分析整组 | ❌ |
| 综合智能分析整组 | ❌ |
| 技术链 / 科研机构 / 人才（隐藏域） | ❌ |
| 企业发展 | ❌（原型有；正式无独立菜单项） |
| 企业查询 | ✅ |
| 重点企业分析 | ✅ |
| 深圳企业现状分析 | ✅ |
| 企业评估 | ✅（命名：评估） |
| 风险洞察 | ✅ |
| 引育推荐 | ✅（原型文案「引育推荐」） |
| 企业维护管理 | ❌ |
| 对比篮 | ✅（正式显式菜单；原型多以浮层/系统层存在） |
| 企业详情 | ✅（隐藏路由） |
| 明星企业等发展子页 | ❌ 正式无入口 |

---

## 4. 企业域页级差异（有对照价值的部分）

在「企业分析」重叠范围内，正式仓已按 V2 规划落地多页，但仍与原型不完全同构：

| 点 | 原型 | 正式 | 差异说明 |
|----|------|------|----------|
| 查询工作台 | `SearchPage` / development/search | `EnterpriseSearch.vue` | 正式为 Vue 重做；需联调后才能断言交互 1:1 |
| 企业详情 | `EnterpriseProfilePage` | `EnterpriseDetail.vue` | 正式不进侧栏，依赖查询跳转 |
| 对比篮 | 系统浮层 `SystemCompareBasketLayer` 等 | 独立菜单 + `EnterpriseCompare*.vue` | 交互形态不同（浮层 vs 页面） |
| 维护管理 | 企业中心 maintenance 全量菜单原型 | 无 | **缺口** |
| 企业发展 / 明星企业 / 深企发展入口 | overview / star / shenzhen 等 | 无独立菜单 | **缺口或未迁** |
| 权限 / 角色 / 评审模式 | `perms` + Persona 切换完整 | 规划要求对齐 demo；需在运行态核验 | 代码有 review/stores，本轮未开 UI 实测 |
| Mock / 真 API | 大量本地 mock + 部分真接 | 只调 Java `gkxlumen-topic` 等 | 数据层差异大，功能「看起来像」≠ 数据同源 |

> 页内字段、Tab、抽屉、筛选组件是否与原型像素级一致，需要本地 `pnpm dev` 或 30892 恢复后做点击级走查；本报告不伪称已完成走查。

---

## 5. 非功能 / 工程差异（测试时会感受到）

| 项 | 原型 | 正式 |
|----|------|------|
| 框架 | React +（Arco icon 等） | Vue 3 + Arco Design Vue |
| 鉴权 | demo 权限矩阵 / 角色切换 | OAuth/登录页 + `requiresAuth` |
| 可观测 | demo `track` 埋点 | 平台 OTel / Tempo 体系（页面级因删减而少） |
| CI 部署 | 视 demo 流水线 | NodePort **30892**；历史记录 deploy 曾 blocked |

---

## 6. 本轮「功能测试」执行记录

| 步骤 | 结果 |
|------|------|
| 同步两边 `origin/dev` | ✅ 完成 |
| 解析原型 `Layout.tsx` 全量 `navGroups` | ✅ |
| 解析正式 `menu.ts` + `views/enterprise` | ✅ |
| 访问 `http://10.50.69.111:30892` | ❌ 不可达（本环境） |
| 全页面点击 / 截图对比 | ⏭ 阻塞于部署；建议恢复 K8s 或本地双开 Vite 后补测 |

---

## 7. 建议的后续测试顺序（可执行）

1. **P0 部署**：恢复 `:30892` 或本地 `lumen-ui-topic` + `demo-ui-topic` 双开。  
2. **P0 企业重叠页走查**：查询 → 详情 → 对比篮 → 重点/深企/评估/风险/引育；记录交互与文案差。  
3. **P1 缺口确认（产品）**：产业链/政策/服务链/智能分析是否本阶段刻意不做；维护管理、企业发展、明星企业是否进下一 Sprint。  
4. **P1 数据**：同一企业编码在原型 Mock vs 正式 Java ADS 的字段差（另开数据 gap 表，不与 UI 菜单混报）。

---

## 8. 验收口径建议（防扯皮）

- **不要**用「原型全菜单是否都在正式仓」作为当前 V2 企业子集的失败标准——规划文档已明确正式仓先做企业查询等子集。  
- **要用**「已声明迁入正式仓的企业叶子，是否达到原型对应页的主路径可测验收」作为功能测试门禁。  
- 未声明迁入的域（产业/政策/服务链等）记为 **范围外 / 待排期**，不要记成回归缺陷。

---

## 9. 相关文档

- `agent-delivery/sprints/lumen-ui-topic-企业查询迁移规划.md`  
- `agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-L00-topic-frontend-repo.md`  
- `agent-delivery/agent-handoffs/平台基建-PLATFORM/E-PLATFORM-P0-L07-topic-ui-shell.md`  
- `demo-ui-topic/src/app/components/Layout.tsx`  
- `lumen-ui-topic/src/router/menu.ts`
