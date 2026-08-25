# 科技专题服务系统：原型 vs 正式前端功能差异（补充盘点版）

> **文档性质**: **新建**对照报告（不修改初版 `topic-prototype-vs-lumen-功能差异.md`）  
> **对照日期**: 2026-08-10  
> **原型**: `demo-ui-topic` @ `origin/dev`（盘点时本地已同步；侧栏真源 `Layout.tsx`）  
> **正式**: `lumen-ui-topic`（GitLab: `lumen-ui-science-topic`）@ **`origin/dev`**（`26eb234`）  
> **方法**: 菜单/路由/页面代码盘点 + URL 探测；结合专项盘点  
>   - [Map demo-ui-topic prototype](a7a59cc2-38a1-487c-9bb8-7f091df187d0)  
>   - [Map lumen-ui-topic formal](c682c6e9-7119-45f8-8438-b84856af6882)  
> **约定**: demo = UX 沙箱；企业 Track-MS V2 在 lumen `dev` 直开，禁止 merge 原型进正式仓。

---

## 1. 结论摘要

| 维度 | 结论 |
|------|------|
| 覆盖范围 | 正式仓侧栏仅 **企业分析 1 组**；原型可见约 **5 大域**，另有技术链/科研/人才等 **隐藏域** |
| 企业域深度 | 正式仓是 **企业 V2 深竖切**（约 8 路由 + 大量 component/API），不是空脚手架 |
| 相对原型缺口 | 正式缺：企业发展、维护管理（原型含 15 运维 Tab）、明星企业等；整域缺：产业/政策/服务链/智能/技术链/科研/人才 |
| 分支陷阱 | 正式仓 **`main` = P0 展示系统脚手架**；专题能力必须看 **`origin/dev`** |
| 线上实测 | `:30892` 本环境超时；原型 CI 常见 `http://192.168.88.63/gkx_topic_demo`（本轮未点测） |

**一句话**：正式 ≈ 企业分析 V2 工程实现；原型 ≈ 全专题 IA 沙箱。主差在**未迁域 + 企业运维/发展入口**。

---

## 2. 环境与入口

| 项 | 原型 | 正式（看 `dev`） |
|----|------|------------------|
| 路径 | `${GKX_ROOT}/repos/demo-ui-topic` | `${GKX_ROOT}/repos/lumen-ui-topic` |
| 栈 | React 18 + Vite + Arco | Vue 3 + Vite + Arco Vue |
| 导航 | `src/app/components/Layout.tsx` | `src/router/menu.ts` |
| 路由 | `src/app/routes.tsx` | `src/router/routes.ts` |
| URL | `http://192.168.88.63/gkx_topic_demo`；本地常 `4177`/`5173` | `http://192.168.88.50:30892`；本地 `:3000` |

---

## 3. 侧栏对照

### 3.1 原型可见（`Layout.tsx`，`hidden: false`）

1. **产业链分析**：专题全景 / 产业查询 / 产业链全景图谱 / 产业运行诊断 / 区域产业评价 / 深圳产业决策 / 维护管理  
2. **企业分析**：企业发展 / 企业查询 / 重点企业分析 / 深圳企业现状分析 / 企业评估 / 风险洞察 / 引育推荐 / 维护管理  
3. **政策分析**：政策扶持 / 政策查询 / 政策时序分析 / 区域政策对比 / 深圳政策现状分析 / 维护管理  
4. **产业服务链分析**：专题服务 / 服务机构查询 / 服务机构分析 / 服务链生态分析 / 机构招引培育 / 维护管理  
5. **综合智能分析**：区域创新活力 / 要素 / 协同  

隐藏但仍有路由：技术链、科研机构、人才分析。

### 3.2 正式仓（`menu.ts` @ `dev`）

仅 **企业分析**：

- 企业查询、对比篮、企业评估、风险洞察、重点企业分析、深圳企业现状分析、引育推荐  
- 隐藏路由：企业详情 `enterprise/:orgId`

页面：`src/views/enterprise/*.vue`（约 9 个企业页）。

### 3.3 矩阵

| 原型侧栏能力 | 正式 `dev` |
|--------------|------------|
| 产业链 / 政策 / 服务链 / 综合智能整组 | ❌ |
| 技术链 / 科研 / 人才（隐藏） | ❌ |
| 企业发展 | ❌ |
| 企业维护管理（含 15 Tab 运维原型） | ❌ |
| 企业查询 / 重点 / 深企现状 / 评估 / 风险 / 引育 | ✅ |
| 对比篮 | ✅（正式侧栏显式；原型多为浮层 + `/basket` 路由） |
| 企业详情 | ✅（隐藏路由） |

---

## 4. 企业重叠区页级差异

| 点 | 原型 | 正式 | 差异 |
|----|------|------|------|
| 查询 | `SearchPage` + SearchScaffold | `EnterpriseSearch.vue` + filter/search 组件层 | Vue 重做，需点击走查才能判 1:1 |
| 详情 | `EnterpriseProfilePage` | `EnterpriseDetail.vue` | 正式不进侧栏 |
| 对比篮 | 浮层 + basket 页 | 侧栏「对比篮」页 | 入口形态不同 |
| 企业发展多 Tab | overview：概况/重点/明星/深圳 | 无菜单 | **缺口** |
| 维护管理 | 15 区 Tab（多数 skeleton） | 无 | **缺口** |
| 权限评审 | `perms` + Persona | 有 review 层，无完整 perms 矩阵 | 待运行态核验 |
| 数据 | 企业偏 Mock；产业 API-first | 已挂 topic/v1 API，仍偏 mock/联调 | 数据不同源 |

---

## 5. 工程差异

| 项 | 原型 | 正式 |
|----|------|------|
| 框架 | React | Vue 3 |
| 鉴权 | demo 权限矩阵 | 登录 + `requiresAuth` |
| `main` vs `dev` | 以 `dev` 为主 | **`main` 脚手架勿对照**；V2 只在 `dev` |
| CI | 部署到 `gkx_topic_demo` | NodePort 30892；历史上有 K8s blocked |

---

## 6. 本轮探测记录

| 步骤 | 结果 |
|------|------|
| 两边拉到 `origin/dev` | ✅ |
| 菜单/路由代码盘点 | ✅ |
| `http://192.168.88.50:30892` | ❌ 超时 |
| 点击级/截图对比 | ⏭ 未做 |

---

## 7. 后续建议

1. 恢复 30892 或本地双开 Vite，对企业重叠页做点击走查。  
2. 产品确认：产业/政策/服务链等是否本阶段刻意不做；维护管理、企业发展是否排期。  
3. 验收勿用「原型全菜单都在正式仓」卡企业 V2；应用「已迁入叶子主路径是否可测」。

---

## 8. 相关路径

- 初版报告（未改意图）：`designs/topic-prototype-vs-lumen-功能差异.md`  
- 本文件（新建补充版）：`designs/topic-prototype-vs-lumen-功能差异-补充盘点版.md`  
- `demo-ui-topic/src/app/components/Layout.tsx`  
- `lumen-ui-topic/src/router/menu.ts`  
- `sprints/lumen-ui-topic-企业查询迁移规划.md`
