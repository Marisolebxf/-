# 智能服务集群-科技专题服务系统测试用例

> **模块**：系统级多对象对比篮（COMPARE）  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v1.0  
> **规范**：`agent-delivery/qa-test-case-spec.md` v1.0  
> **执行仓**：`lumen-ui-topic`（对比篮 Java 门面已接线）  
> **环境**：`VITE_APP_USE_MOCK=false`；网关见 `.env.development` 的 `VITE_APP_API_URL`  
> **USM**：`agent-handoffs/产品整体定义/ENT-COMPARE/USM-ENT-COMPARE.md`  
> **TRACE**：`TRACE-ENT-COMPARE.yaml`  
> **原始需求**：`bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.2.3`（派生能力，不新增 Bid 叶子）  
> **入口**：已登录后系统对比篮入口，或侧栏「对比篮」（`/enterprise/enterprise-compare`）  
> **交付口径**：INTEG（前端 → Java compare-basket / 候选 / 分发）  
> **关联任务**：`ENT-MOD-COMPARE-QA-ACCEPT-L01`  
> **试点说明**：覆盖 USM 验收场景主干；浮层拖动避让等 P1～P2 下轮补  
> **维护**：qa-agent · 2026-08-08  

---

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00015 | 系统Shell | 对比篮 | 入口与菜单 | 全局入口 | 任意业务页 | 系统浮层入口 | 左侧无对比篮菜单且 Shell 入口显示企业计数 | 1、已登录；2、篮内可有 0～N 企业 | 1.检查企业分析左侧二级菜单；2.查看 Shell 对比篮入口角标/「共 X 项」；3.点击入口 | 1、左侧**无**「对比篮」菜单项；2、入口可见且 X 只计企业；3、当前页展开浮层，不先跳独立页 | P0 | | | | | | US-ENT-CMP-02 | ENT-CMP-USM-14 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | ASC-ENT-COMPARE-SYSTEM-FLOAT |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00016 | 系统Shell | 对比篮 | 收集去重 | 多源加入 | 企业查询等 | 全局去重 | 同一企业多源加入只保留一条 | 1、可从查询与另一入口加入同一企业 | 1.从企业查询加入企业 A；2.从另一入口再次加入 A；3.打开对比篮核对 | 1、篮内仅 1 条 A；2、各入口显示已加入；3、可合并来源/更新时间（来源标签可不展示） | P0 | | | | | | US-ENT-CMP-01 | ENT-CMP-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00017 | 系统Shell | 对比篮 | 容量 | 满员拦截 | 对比篮浮层 | 50 家上限 | 第 51 家单个加入失败提示 | 1、篮内已有 50 家（可用接口或脚本准备满员数据） | 1.再单个加入第 51 家；2.观察提示与篮内数量 | 1、不写入；2、提示已满需移除；3、数量仍为 50 | P0 | | | | | | US-ENT-CMP-01 | ENT-CMP-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | 实现若仍 12 记 GAP |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00018 | 系统Shell | 对比篮 | 恢复 | 刷新恢复 | 对比篮浮层 | 单用户单篮 | 刷新后恢复最近篮且默认近时倒序 | 1、篮内≥2 家并调整过操作时间 | 1.记录当前企业顺序；2.刷新页面；3.再开对比篮 | 1、对象恢复；2、默认按最近操作时间倒序 | P0 | | | | | | US-ENT-CMP-02 | ENT-CMP-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00019 | 系统Shell | 对比篮 | 筛选 | 名称与类型 | 对比篮浮层 | 轻筛 | 仅名称搜索+企业类型筛，重置文案正确 | 1、篮内多家且类型多样 | 1.按名称搜索；2.按企业类型筛选；3.点「重置」；4.确认无「清空筛选」/信用代码搜索/来源筛 | 1、名称与类型筛生效；2、重置恢复默认；3、无禁用外的复杂筛 | P0 | | | | | | US-ENT-CMP-02 | ENT-CMP-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00020 | 系统Shell | 对比篮 | 选择栏 | 全选当前筛选 | 对比篮浮层 | 三态全选 | 底部全选只作用于当前可见且保留隐藏选择 | 1、可筛出子集 | 1.筛选出部分企业；2.全选当前筛选结果；3.改筛选使部分已选不可见；4.点取消选择 | 1、全选三态正确且空结果禁用；2、不可见已选仍保留；3、取消选择清除全部选择；4、底栏顺序含全选→已选→取消→发起分析→招引→培育 | P0 | | | | | | US-ENT-CMP-02 | ENT-CMP-USM-04B | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | DEC-ENT-COMPARE-SELECT-ALL |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00021 | 系统Shell | 对比篮 | 发起分析 | 任务浮层 | 对比篮浮层 | 分发前选择 | 未选不可发起；选后打开任务浮层且选择本身不跳转 | 1、篮内有企业 | 1.未勾选时点发起分析；2.勾选后点发起分析；3.在任务浮层点选一任务但先不点下一步 | 1、未选时不可执行或明确提示；2、打开「选择分析任务」浮层；3、仅选任务不跳转 | P0 | | | | | | US-ENT-CMP-03 | ENT-CMP-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | E-23触点 | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00022 | 系统Shell | 对比篮 | 发起分析 | 评估分发 | 企业评估 | 带参进入 | 下一步携带对象进入评估并显示来自对比篮 | 1、已勾选 1～N 家；2、有评估权限 | 1.发起分析→选评估任务之一→下一步前往配置；2.观察目标页对象条与对比篮面板 | 1、进入评估路由并带 `enterprise_codes[]`；2、显示「来自对比篮 · X 家」与打开对比篮入口；3、成功后篮面板收起但入口保留；4、篮内不出现评分/雷达等结论 | P0 | | | | | | US-ENT-CMP-03 | ENT-CMP-USM-11 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | E-23 | TRACE-ENT-COMPARE.yaml | /enterprise/evaluation | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | 含 ENT-CMP-USM-06 无结论断言 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00023 | 系统Shell | 对比篮 | 发起分析 | 供应链上限 | 对比篮浮层 | 2家校验 | 供应链任务超过 2 家置灰提示 | 1、勾选≥3 家 | 1.发起分析；2.查看供应链关系分析任务状态 | 1、任务仍可见但置灰；2、提示最多 2 家；3、不静默截断 | P1 | | | | | | US-ENT-CMP-03 | ENT-CMP-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.8 | E-28触点 | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00024 | 系统Shell | 对比篮 | 引育候选 | 批量加入 | 对比篮浮层 | 招引/培育 | 加入候选提示新增与重复且不跳转 | 1、勾选企业；2、有写权限（或测无权限态） | 1.点加入招引或培育候选；2.观察提示；3.确认是否自动跳转 | 1、提示已加入 X / 已在名单 Y；2、不自动跳转；3、篮内不生成推荐理由 | P1 | | | | | | US-ENT-CMP-04 | ENT-CMP-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.6 | E-26触点 | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00025 | 系统Shell | 对比篮 | 空态 | 去查询 | 对比篮浮层 | 空篮引导 | 空篮仅来源说明+去企业查询 | 1、清空篮（确认对话框） | 1.清空并确认；2.观察空态 | 1、主操作「去企业查询」；2、无推荐企业；3、有来源说明 | P0 | | | | | | US-ENT-CMP-05 | ENT-CMP-USM-08 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | 含 ENT-CMP-USM-10 清空二次确认 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00026 | 系统Shell | 对比篮 | 旧链兼容 | basket路由 | 兼容打开 | 旧链开浮层 | 旧 basket 兼容路由打开对比篮 | 1、可访问旧 URL | 1.若存在旧 basket 兼容 URL 则打开之；2.观察是否独立菜单页 | 1、打开系统对比篮浮层；2、不渲染旧独立左侧菜单页 | P1 | | | | | | US-ENT-CMP-07 | ENT-CMP-USM-18 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | /enterprise/enterprise-compare | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00027 | 系统Shell | 对比篮 | 多对象壳 | 五Tab | 对比篮浮层 | 开发中占位 | 五 Tab 存在；非企业为开发中且无操作 | 1、打开对比篮 | 1.确认 Tab：企业/产业链/政策/服务机构/区域；2.切到非企业 Tab；3.回企业 Tab | 1、默认企业 Tab 且能力完整；2、开发中空页无数量/搜索/选择/分析；3、回企业后筛选勾选滚动不丢 | P1 | | | | | | US-ENT-CMP-07 | ENT-CMP-USM-19 | 科技信息展示系统和科技专题服务系统.md | 产品增强 ASC | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | 合并 USM-20/22/23 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00028 | 系统Shell | 对比篮 | 系统浮层 | 互斥展开 | 业务页Shell | 任务窗协同 | 任务与对比篮同时可访且只展开一个 | 1、系统任务入口可见 | 1.展开任务面板；2.再点对比篮；3.再点任务入口 | 1、两入口均可访问；2、打开一方自动收起另一方；3、业务状态不丢 | P1 | | | | | | US-ENT-CMP-06 | ENT-CMP-USM-15 | 科技信息展示系统和科技专题服务系统.md | 产品增强 ASC | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | app-shell#system-compare-basket | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00029 | 企业分析 | 企业查询 | 入口去重 | 无聚合角标 | 企业查询 | 宿主去重 | 查询页无页内对比篮聚合按钮 | 1、在企业查询有结果/推荐 | 1.检查推荐区、普通/高级结果工具栏、完整详情顶栏是否有对比篮聚合入口与数量角标 | 1、上述宿主无聚合按钮/角标；2、行内加入/已加入仍可用 | P1 | | | | | | US-ENT-CMP-07 | ENT-CMP-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 派生/COMPARE | TRACE-ENT-COMPARE.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-COMPARE-QA-ACCEPT-L01 | | 与 SEARCH-00013 交叉 |

---

## 2. 覆盖自检

- [x] CMP-01～05、07 主干场景已覆盖
- [x] 浮层互斥 / 五 Tab / 旧链 / 查询去重已覆盖
- [ ] 拖动避让与「恢复默认位置」（ENT-CMP-USM-16/17）本试点未单列，下轮补
- [x] 编号接续 SEARCH：`FUNC-00015`～`00029`
- [ ] 执行记录另档

## 3. 序号台账（本文件）

| 测试类型 | 本文件占用 | 说明 |
|----------|------------|------|
| FUNC | 00015–00029 | 与 SEARCH 共用 KJZTFWXT-FUNC 序号空间 |
