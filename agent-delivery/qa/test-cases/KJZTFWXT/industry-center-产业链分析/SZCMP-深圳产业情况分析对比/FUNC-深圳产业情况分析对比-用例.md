# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md` **v1.3**（红线见 `qa/as-built/prompts/_case.md`）  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v3.0 · 2026-10-18（对照重写；新号 03288–03326；旧号处置见文末）  
> **模块**：深圳产业情况分析对比（catalog `chain-sz-compare`）  
> **金样**：**03288**（筛选条件 → 开始分析 → 成功结果页）。本页只有这一种发起方式。  
> **环境**：http://111.198.38.90:50892/ · 账号 `admin` / `123456`  
> **入口**：产业链分析 →「深圳产业情况分析对比」  
> **路由**：`/industry-center/shenzhen?workspace=comparison&tab=comparison`  
> **异步**：选满产业和标杆后点「开始分析」；当天同条件再次点开会已有结果且不新增任务；「重新分析」另起新任务。  
> **交付口径**：INTEG  
> **功能点 / 功能点ID**：本步不改同目录 `coverage-fp.md`  
> **关联任务**：`QA-KJZTFWXT-BLINE-CASE-IND-L01`  
> **维护**：agent:qa-agent · 监管 human:黄敬洲  

---

## 关评审控件清单

入口拓扑：

| 区域 | 现场 | 用例 |
|------|------|------|
| 入口 A · 筛选条件发起 | 集群、产业、标杆区域，按钮「开始分析」 | 03288（金样） |
| 入口 B · 已选对象发起 | 无。本页没有对象名单，也不能从名单发起分析 | 无 |
| 任务列表 | 「分析记录」 | 03308、03309、03310 |
| 结果页 | 「深圳产业情况分析对比结果」 | 03299 起 |

结果页（入口 A；入口 B 无，不复制）：

| 组 | 格 | 用例或未覆盖 |
|----|----|--------------|
| 摘要 | 对象 / 主体 / 标杆 / 任务 | 03299 |
| 摘要 | 深圳产业链企业数 | 03300 |
| 摘要 | 投融资总额 | 03301 |
| 筛选下拉 | 无 | 无 |
| 开始分析·当天 | 同条件再次开始分析 | 03306 |
| 工具 | 重新分析 | 03311（点到新结果页） |
| 工具 | 调整条件（复制配置回配置且条件仍在） | 03313 |
| 工具 | 按此配置新建分析 | 03312 |
| 工具 | 报告查看 | 03307 |
| 工具 | 报告目录 | 03314 |
| 工具 | 导出 | 03323 |
| 工具 | 结果搜索 | 无 |
| 表 | 列与四行 | 03302 |
| 表 | 翻页 | 无（矩阵不分页） |
| 表 | 勾选 | 无 |
| 表 | 行按钮 | 无 |
| 详情 | 行抽屉 | 无 |
| 二级 | 无 | 无 |
| 报告 | 生成中 | 未覆盖：打开报告时正文已在，没有单独的生成中页 |
| 报告 | 下载报告 | 03324 |
| 入池 | 无 | 无 |
| 过程页 | 生成中与两个按钮 | 03315、03316 |

入口 B 各格：无。

任务列表：

| 格 | 用例或未覆盖 |
|----|--------------|
| 列：任务、类型、状态、创建时间、操作 | 03308 |
| 任务状态下拉（4 项） | 03309 |
| 失败 → 暂无数据 | 03325 |
| 分析中 → 暂无数据 | 03326 |
| 重置筛选 | 03317 |
| 翻页 | 未覆盖：每页 10 条，现有记录不足一页，没有第二页 |
| 查看结果 × 条件发起 | 03310 |
| 复制配置 × 条件发起 | 03313 |
| 查看报告 × 条件发起 | 03307 |
| 下载报告 × 条件发起 | 03324 |
| 删除取消 × 条件发起 | 03318 |
| 删除确定 × 条件发起 | 03319 |
| 上述操作 × 对象名单起源 | 无（没有第二种发起） |
| 同条件单飞 | 未覆盖：生成过程约 1 秒即结束，构造不出第二条进行中任务 |
| 分析失败的任务 | 未覆盖：现场没有失败任务，造不出失败终态 |
| 第二种账号 | 未覆盖：只有当前登录账号 |

配置区（入口 A 的条件，不代替金样）：

| 格 | 用例 |
|----|------|
| 页标题与路由 | 00732 |
| 双 Tab | 00733 |
| 集群下拉 15 项 | 03289 |
| 产业下拉 7 项 | 03290 |
| 切换集群后产业选项变化 | 03291 |
| 标杆下拉 8 个城市 | 03292 |
| 主体区域深圳只读 | 00737 |
| 切换后深圳与四维模型仍在 | 00736 |
| 四维模型列 | 03293 |
| 权重不可改 | 00739 |
| 只读且行数固定 | 00740 |
| 选择列不可勾选 | 03294 |
| 查看 × 企业 / 专利 / 政策 / 人才 | 03295–03298 |
| 未选标杆不可开始 | 03322 |
| 重置参数 | 00743、00744 |
| Tab 往返条件仍在 | 00748 |
| 只改条件不点开始分析 | 03321 |
| 带入发展分析 | 03320 |

---

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

> 排列：**主流程 → 备选 → 异常**。金样只有 03288。  
> 预期常态 1～3 点。长名单见附录 A。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00732 | 产业链分析 | 深圳产业情况分析对比 | 主流程-入口与路由 | 页头与路由 | 深圳产业情况分析对比 | 进入对比工作区 | 进入「深圳产业情况分析对比」页，路由与页标题正确 | 1、系统正常；2、已登录 | 1.经产业链分析菜单进入「深圳产业情况分析对比」 | 1、路由含 /industry-center/shenzhen；2、工作区与页签均为 comparison；3、页标题为「深圳产业情况分析对比」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 选择目标产业 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-01 | 保留编号。金样改挂 03288 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00733 | 产业链分析 | 深圳产业情况分析对比 | 主流程-入口与路由 | 双 Tab 构成 | 深圳产业情况分析对比 | 双 Tab | 顶部两个页签的名称与默认选中正确 | 1、已进入深圳产业情况分析对比页 | 1.读取顶部页签名称；2.读取默认选中项 | 1、页签为「深圳产业情况分析对比」和「分析记录」；2、默认选中「深圳产业情况分析对比」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 选择目标产业 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-06 | 保留编号 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00736 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 切换后要素保持 | 深圳产业情况分析对比 | 配置保持 | 切换产业后，主体仍为深圳，四维模型行数不变 | 1、已进入页面；2、已选集群 | 1.把产业切换为另一项；2.读取主体区域；3.读取四维模型行数 | 1、主体区域仍为「深圳」；2、四维模型仍为 4 行 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 选择目标产业 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-08 | 保留编号。区块名改为页面原文「四维模型」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00737 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 主体深圳锁定 | 深圳产业情况分析对比 | 主体区域只读 | 主体区域「深圳」不能改成别的地区 | 1、已进入页面 | 1.点击主体区域「深圳」；2.尝试输入其他地区名；3.尝试清空该值 | 1、主体区域保持「深圳」；2、输入和清空都不能改掉该值 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 主体区域固定 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-03 | 保留编号。金样改挂 03288 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00739 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 权重只读 | 深圳产业情况分析对比 | 四维权重只读 | 四维模型四行的权重数值不能修改 | 1、已进入页面 | 1.读取四行指标名称；2.点击权重旁的增减箭头；3.在权重框内输入新值 | 1、四行指标名称为企业、专利、政策、人才；2、权重仍为 25，不能改掉 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 四维模型只读 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-09 | 保留编号。区块名改为「四维模型」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00740 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 行数固定 | 深圳产业情况分析对比 | 四维行数固定 | 四维模型固定四行，没有增删行入口 | 1、已进入页面 | 1.读取四维模型行数；2.在四维模型区域寻找增行或删行按钮 | 1、数据状态四行都显示「可用」；2、没有增行、删行或改指标名的按钮 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 四维模型只读 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-10 | 保留编号 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03288 | 产业链分析 | 深圳产业情况分析对比 | 主流程-开始分析 | 条件发起至结果 | 深圳产业情况分析对比 | 开始分析得到结果 | 选好产业和标杆后，开始分析能打开成功结果页 | 1、已进入分析配置 | 1.在集群下拉选择「新一代信息技术」；2.在产业下拉选择「人工智能与应用」；3.在标杆区域选择「上海市」；4.在标杆区域再选择「北京市」；5.点击「开始分析」；6.若出现「查看分析结果」，点击该按钮 | 1、页面出现标题「深圳产业情况分析对比结果」；2、摘要中主体为深圳，标杆含上海市与北京市 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 开始分析 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 金样。当天已成功时会直接打开已有结果，仍须见到结果页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03289 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 集群下拉 | 深圳产业情况分析对比 | 集群选项 | 集群下拉的选项个数正确 | 1、已进入分析配置 | 1.展开集群下拉 | 1、选项共 15 个，名称见附录 A | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 选择目标产业 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03290 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 产业下拉 | 深圳产业情况分析对比 | 产业选项 | 集群为新一代信息技术时，产业下拉选项个数正确 | 1、集群已是「新一代信息技术」 | 1.展开产业下拉 | 1、选项共 7 个，名称见附录 A | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 选择目标产业 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 未选时占位为「请选择产业」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03291 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 产业随集群变化 | 深圳产业情况分析对比 | 产业联动 | 换成生物产业后，产业选项随之变化 | 1、已进入分析配置 | 1.把集群切换为「生物产业」；2.展开产业下拉 | 1、产业选项变为 3 个，名称见附录 A | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 选择目标产业 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03292 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 标杆城市 | 深圳产业情况分析对比 | 标杆选项 | 标杆区域下拉给出可选城市个数 | 1、已进入分析配置；2、标杆尚未选择 | 1.展开标杆区域下拉 | 1、可选城市共 8 个，名称见附录 A | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 选择标杆区域 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 未选占位原文见附录 A，不写入预期 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03293 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 四维表列 | 深圳产业情况分析对比 | 四维列名 | 四维模型表的列名齐全 | 1、已进入分析配置 | 1.读取四维模型表头 | 1、列共 7 个，名称见附录 A | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 四维模型 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03294 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 选择列 | 深圳产业情况分析对比 | 选择列不可勾 | 四维模型的选择列不能勾上 | 1、已进入分析配置 | 1.点击四维模型「选择」列的勾选框 | 1、勾选框保持未选 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 四维模型只读 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03295 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 查看企业 | 深圳产业情况分析对比 | 企业指标说明 | 「企业」行的查看打开对应说明 | 1、已进入分析配置 | 1.在四维模型点击「企业」行的「查看」 | 1、抽屉标题为「企业 · 指标说明」；2、抽屉内有「说明」和「支撑指标」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 指标说明 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03296 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 查看专利 | 深圳产业情况分析对比 | 专利指标说明 | 「专利」行的查看打开对应说明 | 1、已进入分析配置 | 1.在四维模型点击「专利」行的「查看」 | 1、抽屉标题为「专利 · 指标说明」；2、抽屉内有「说明」和「支撑指标」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 指标说明 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03297 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 查看政策 | 深圳产业情况分析对比 | 政策指标说明 | 「政策」行的查看打开对应说明 | 1、已进入分析配置 | 1.在四维模型点击「政策」行的「查看」 | 1、抽屉标题为「政策 · 指标说明」；2、抽屉内有「说明」和「支撑指标」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 指标说明 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03298 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析配置区 | 查看人才 | 深圳产业情况分析对比 | 人才指标说明 | 「人才」行的查看打开对应说明 | 1、已进入分析配置 | 1.在四维模型点击「人才」行的「查看」 | 1、抽屉标题为「人才 · 指标说明」；2、抽屉内有「说明」和「支撑指标」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 指标说明 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03299 | 产业链分析 | 深圳产业情况分析对比 | 主流程-结果页 | 条件摘要 | 深圳产业情况分析对比 | 结果摘要 | 从开始分析进入的结果页，摘要与所选条件一致 | 1、已用「人工智能与应用」以及上海市、北京市点过「开始分析」 | 1.停留在刚打开的结果页；2.读取标题下的对象、主体、标杆 | 1、摘要中的对象为「人工智能与应用」；2、主体为深圳；3、标杆含上海市与北京市 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 结果摘要 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 从分析记录「查看结果」进入时，摘要曾显示未选，执行时分开记录 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03300 | 产业链分析 | 深圳产业情况分析对比 | 主流程-结果页 | 企业数 | 深圳产业情况分析对比 | 深圳产业链企业数 | 结果页「深圳产业链企业数」有明确空值文案 | 1、已打开成功结果页 | 1.读取「深圳产业链企业数」 | 1、该格显示「暂无」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 结果摘要 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03301 | 产业链分析 | 深圳产业情况分析对比 | 主流程-结果页 | 投融资 | 深圳产业情况分析对比 | 投融资总额 | 结果页「投融资总额」有明确空值文案 | 1、已打开成功结果页 | 1.读取「投融资总额」 | 1、该格显示「数据筹备中」 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 结果摘要 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03302 | 产业链分析 | 深圳产业情况分析对比 | 主流程-结果页 | 对比表 | 深圳产业情况分析对比 | 对比结果表 | 对比结果表带出深圳列和标杆列 | 1、已打开含上海市、北京市的成功结果页 | 1.读取「对比结果」表头；2.读取表的行名 | 1、表头含「维度」「深圳」「上海市」「北京市」；2、行名含产业、专利、政策、人才 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 对比结果 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 不钉死单元格分数 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03303 | 产业链分析 | 深圳产业情况分析对比 | 主流程-结果页 | 对标研判 | 深圳产业情况分析对比 | 对标研判 | 对标研判三块都有正文 | 1、已打开成功结果页 | 1.读取「对标研判」下的三块标题和正文 | 1、三块标题为「独特优势」「差距」「劣势」；2、每块都有一句说明 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 对标研判 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03304 | 产业链分析 | 深圳产业情况分析对比 | 主流程-结果页 | 综合判断 | 深圳产业情况分析对比 | 潜力与阶段 | 综合判断列出市场、技术、链条三项 | 1、已打开成功结果页 | 1.读取「产业化潜力与发展阶段综合判断」 | 1、能看到「市场前景」「技术成熟度」「链条完整性」三项 | P0 |  |  |  |  |  | US-CHAIN-SZ-02 | AC-US-CHAIN-SZ-02-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 综合判断 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03305 | 产业链分析 | 深圳产业情况分析对比 | 主流程-结果页 | 所处阶段 | 深圳产业情况分析对比 | 所处阶段 | 综合判断下方给出所处阶段和阶段特征 | 1、已打开成功结果页 | 1.读取「所处阶段」；2.读取「阶段特征」 | 1、「所处阶段」有一句结论；2、「阶段特征」有一句结论 | P0 |  |  |  |  |  | US-CHAIN-SZ-02 | AC-US-CHAIN-SZ-02-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 所处阶段 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 结论可以是暂无，但不能缺这两块 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03306 | 产业链分析 | 深圳产业情况分析对比 | 主流程-开始分析 | 当天再次开始 | 深圳产业情况分析对比 | 当天不新增任务 | 当天同条件再次开始分析时，任务条数不增加 | 1、当天已对「人工智能与应用」及上海市、北京市成功分析过 | 1.打开分析记录并记住任务条数；2.回到分析配置；3.再次选择同一产业和同一组标杆；4.点击「开始分析」 | 1、进入标题为「深圳产业情况分析对比结果」的页面；2、分析记录的任务条数与点击前相同 | P0 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 当天复用 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 同条件再次点击会打开已有结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03307 | 产业链分析 | 深圳产业情况分析对比 | 主流程-报告 | 查看报告 | 深圳产业情况分析对比 | 查看报告 | 已完成任务可以打开对比报告 | 1、分析记录里有已完成任务 | 1.打开「分析记录」；2.点击一条已完成任务的「查看报告」 | 1、页面标题为「深圳产业情况分析对比报告」；2、报告目录共 7 项，名称见附录 A | P0 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 查看报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 结果页的「查看报告」到达同一报告页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03308 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析记录 | 列名 | 深圳产业情况分析对比 | 记录列 | 分析记录表的列名齐全 | 1、已打开「分析记录」 | 1.读取记录表表头 | 1、列名为任务、类型、状态、创建时间、操作 | P0 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 分析记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 类型列为「深圳产业情况分析对比」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03309 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析记录 | 任务状态 | 深圳产业情况分析对比 | 状态选项 | 任务状态下拉的选项个数正确 | 1、已打开「分析记录」 | 1.展开「任务状态」下拉 | 1、选项共 4 个，名称见附录 A | P0 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 分析记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03310 | 产业链分析 | 深圳产业情况分析对比 | 主流程-分析记录 | 查看结果 | 深圳产业情况分析对比 | 查看结果 | 「查看结果」打开该任务的结果页 | 1、分析记录里有已完成任务 | 1.点击一条已完成任务的「查看结果」 | 1、页面标题为「深圳产业情况分析对比结果」；2、地址中的任务号与所点行一致 | P0 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 查看结果 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00743 | 产业链分析 | 深圳产业情况分析对比 | 备选-操作区 | 重置产业 | 深圳产业情况分析对比 | 重置参数 | 「重置参数」后产业回到未选占位 | 1、产业已选择一项 | 1.点击「重置参数」；2.读取产业下拉 | 1、产业下拉回到「请选择产业」 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 重置参数 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P1-01 | 保留编号 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00744 | 产业链分析 | 深圳产业情况分析对比 | 备选-操作区 | 重置后其余项 | 深圳产业情况分析对比 | 重置后保持 | 重置后深圳仍在，开始分析回到不可点 | 1、已点击「重置参数」 | 1.读取主体区域；2.读取标杆区域；3.读取「开始分析」 | 1、主体区域仍为「深圳」；2、标杆区域回到未选；3、「开始分析」为禁用 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 重置参数 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P1-02 | 保留编号 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00748 | 产业链分析 | 深圳产业情况分析对比 | 备选-分析记录 | 页签往返 | 深圳产业情况分析对比 | 条件保持 | 切到分析记录再切回，已选产业还在 | 1、产业已选「人工智能与应用」 | 1.切到「分析记录」；2.切回「深圳产业情况分析对比」；3.读取已选产业 | 1、两页签内容不叠在一起；2、切回后产业仍为「人工智能与应用」 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 页签切换 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P1-06 | 保留编号 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03311 | 产业链分析 | 深圳产业情况分析对比 | 备选-重新分析 | 新一轮结果 | 深圳产业情况分析对比 | 重新分析 | 「重新分析」会进入新任务的结果页 | 1、复制配置后产业和标杆已回显；2、「重新分析」可点 | 1.点击「重新分析」；2.点击「查看分析结果」 | 1、生成过程中出现一个新的任务号；2、结果页标题为「深圳产业情况分析对比结果」 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 重新分析 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 点击后没有确认框，直接进入生成过程页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03312 | 产业链分析 | 深圳产业情况分析对比 | 备选-结果页 | 按此配置新建 | 深圳产业情况分析对比 | 按此配置新建分析 | 「按此配置新建分析」回到配置并露出重新分析 | 1、已打开成功结果页 | 1.点击「按此配置新建分析」 | 1、回到分析配置；2、页面出现「重新分析」；3、「重新分析」为禁用 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 按此配置新建分析 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 此按钮不会把标杆回显出来。要重跑用 03311 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03313 | 产业链分析 | 深圳产业情况分析对比 | 备选-分析记录 | 复制配置 | 深圳产业情况分析对比 | 复制配置 | 「复制配置」后，产业和标杆仍显示在配置页 | 1、分析记录里有已完成的对比任务 | 1.打开「分析记录」；2.点击一条已完成任务的「复制配置」 | 1、回到分析配置；2、产业名称和标杆城市都回显；3、「开始分析」可点击 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 复制配置 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 调整条件走这一条，不走 03312 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03314 | 产业链分析 | 深圳产业情况分析对比 | 备选-报告 | 报告目录 | 深圳产业情况分析对比 | 目录定位 | 点击报告目录能对上正文标题 | 1、已打开「深圳产业情况分析对比报告」 | 1.点击目录中的「执行摘要」 | 1、正文出现标题「执行摘要」 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 报告目录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03315 | 产业链分析 | 深圳产业情况分析对比 | 备选-生成过程 | 过程页 | 深圳产业情况分析对比 | 生成过程 | 重新分析后先看到生成过程，而不是立刻跳走 | 1、复制配置后「重新分析」可点 | 1.点击「重新分析」 | 1、页面出现「生成中」；2、可见「查看分析结果」；3、过程末项为「分析结果已生成」 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 生成过程 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 过程步骤全文见附录 A。点进结果页归 03311 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03316 | 产业链分析 | 深圳产业情况分析对比 | 备选-生成过程 | 查看分析记录 | 深圳产业情况分析对比 | 从过程页回记录 | 生成过程页可以回到分析记录并看到新任务 | 1、已停在生成过程页 | 1.点击「查看分析记录」 | 1、进入分析记录列表；2、列表中有这次新产生的任务 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 查看分析记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03317 | 产业链分析 | 深圳产业情况分析对比 | 备选-分析记录 | 重置筛选 | 深圳产业情况分析对比 | 重置筛选 | 「重置筛选」把状态拉回全部并重新列出任务 | 1、已打开分析记录 | 1.把任务状态选为「失败」；2.点击「重置筛选」 | 1、任务状态回到「全部状态」；2、已完成任务重新出现在列表中 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 重置筛选 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03318 | 产业链分析 | 深圳产业情况分析对比 | 备选-分析记录 | 删除取消 | 深圳产业情况分析对比 | 删除取消 | 删除时点取消，任务还在 | 1、分析记录里至少有一条已完成任务 | 1.点击该任务的「删除」；2.在弹出框点击「取消」 | 1、该任务仍显示在分析记录中 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 删除记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 弹出框按钮为「取消」和「确定」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03319 | 产业链分析 | 深圳产业情况分析对比 | 备选-分析记录 | 删除确定 | 深圳产业情况分析对比 | 删除确定 | 删除时点确定，该任务从列表消失 | 1、分析记录里有一条可删除的已完成任务 | 1.点击该任务的「删除」；2.在弹出框点击「确定」 | 1、该任务不再出现在分析记录中；2、其他任务仍在 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 删除记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 用本轮新产生的任务做，不要删历史样例任务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03320 | 产业链分析 | 深圳产业情况分析对比 | 备选-结果页 | 带入发展分析 | 深圳产业情况分析对比 | 带入发展分析 | 「带入发展分析」离开对比页，进入发展分析 | 1、已打开成功结果页 | 1.点击「带入发展分析」 | 1、页标题变为「深圳产业发展分析」 | P1 |  |  |  |  |  | US-CHAIN-SZ-02 | AC-US-CHAIN-SZ-02-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 带入发展分析 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 只核离开对比页。发展分析自己的配置不在本册 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03321 | 产业链分析 | 深圳产业情况分析对比 | 备选-开始分析 | 不自动发起 | 深圳产业情况分析对比 | 改条件不发起 | 只改产业、不点开始分析时，不新增任务 | 1、已进入分析配置 | 1.打开分析记录并记住任务条数；2.回到分析配置只切换产业；3.再打开分析记录 | 1、任务条数与切换前相同 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 不自动发起 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03322 | 产业链分析 | 深圳产业情况分析对比 | 异常-开始分析 | 未选标杆 | 深圳产业情况分析对比 | 未选标杆不可开始 | 没选标杆时，开始分析不能发出任务 | 1、标杆区域尚未选择 | 1.记住分析记录的任务条数；2.在分析配置点击「开始分析」；3.再打开分析记录 | 1、「开始分析」为禁用；2、页面提示须选择 1～5 个标杆区域；3、任务条数不变 | P1 |  |  |  |  |  | US-CHAIN-SZ-01 | AC-US-CHAIN-SZ-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 未选标杆 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 只选产业、不选标杆时按钮仍禁用 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03323 | 产业链分析 | 深圳产业情况分析对比 | 异常-报告 | 导出不可用 | 深圳产业情况分析对比 | 导出 | 报告页的「导出」当前点不了 | 1、已打开对比报告 | 1.点击「导出」 | 1、「导出」为禁用；2、点击后仍停留在报告页 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 导出报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 已完成任务的报告上该按钮为禁用 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03324 | 产业链分析 | 深圳产业情况分析对比 | 异常-报告 | 下载报告 | 深圳产业情况分析对比 | 下载报告 | 下载报告失败时给出提示，任务保持已完成 | 1、分析记录里有已完成任务 | 1.点击该任务的「下载报告」 | 1、页面给出失败提示；2、该任务状态仍为「已完成」 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 下载报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 勘察时点击后没有文件，也没有页面提示。无提示则本条不通过 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03325 | 产业链分析 | 深圳产业情况分析对比 | 异常-分析记录 | 失败筛选 | 深圳产业情况分析对比 | 状态为失败 | 筛成失败时，列表为空态 | 1、已打开分析记录 | 1.把任务状态选为「失败」 | 1、列表显示「暂无数据」 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 状态筛选 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 这是筛选空态，不是造出一条失败任务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03326 | 产业链分析 | 深圳产业情况分析对比 | 异常-分析记录 | 分析中筛选 | 深圳产业情况分析对比 | 状态为分析中 | 筛成分析中时，列表为空态 | 1、已打开分析记录 | 1.把任务状态选为「分析中」 | 1、列表显示「暂无数据」 | P1 |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.6 | 状态筛选 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=comparison&tab=comparison |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |

---

## 2. 旧号处置（对照重写）

| 旧号 | 处置 | 说明 |
|------|------|------|
| 00732、00733、00737、00743、00744、00748 | 保留 | 终态与页面原文一致。00732、00737 去掉金样 |
| 00736、00739、00740 | 保留 | 编号不变。区块名改为页面上的「四维模型」 |
| 00734、00735、00738、00741、00742、00745、00746、00747、00749、00750、00753 | 作废 | 停在配置、按钮名或预期与现场不符。新号见上表，旧号不复用 |
| 00751、00752 | 删除 | 只测开关与追溯，不进入本册。旧号不复用 |

新号从 03288 用到 **03326**。03327–03387 未使用。

---

## 3. 红线自检

- 主流程 29 条（00732、00733、00736、00737、00739、00740、03288–03310）不少于备选 14 条加异常 5 条。
- 金样只有 03288，步骤到成功结果页。
- 入口 B、结果搜索、结果行按钮、入池：无。
- 单飞、失败任务、第二页、第二种账号：未覆盖，原因写在清单里。

### 附录 A 长枚举

**集群（03289，15）**：新一代信息技术、生物产业、新能源、新材料、高端装备、智能网联新能源汽车、绿色环保、低空经济与空天、传统与创意产业、海洋产业、未来制造（智能机器人）、未来信息（光载信息、AI 底层生态）、未来能源、未来空间、未来健康（合成生物、细胞基因、脑机工程）。

**产业 · 新一代信息技术（03290，7）**：新一代信息技术、半导体与集成电路、人工智能与应用、智能终端、软件与信息服务、新型网络与通信、超高清视频与显示。

**产业 · 生物产业（03291，3）**：生物、生物医药与生命健康、高端医疗器械。

**标杆城市（03292，8）**：北京市、上海市、杭州市、成都市、武汉市、重庆市、天津市、宁波市。未选时输入框占位原文：「Q016 未定，标杆清单为空；勿冒充沪/京/苏州」。

**四维模型列（03293，7）**：选择、指标名称、分组 / 维度、数据状态、权重、数据来源、指标说明。

**任务状态（03309，4）**：全部状态、分析中、已完成、失败。

**报告目录（03307，7）**：报告身份、执行摘要、对象与范围、关键发现、证据与分析、数据来源与生成说明、局限性与使用边界。

**生成过程（03315）**：任务提交与深圳主体/产业/标杆冻结；校验标杆就绪与四维模型版本；计算企业/专利/政策/人才多维对比；归纳优势差距、产业化潜力与发展阶段；结果可信性校验与结构化快照组装；末项「分析结果已生成」。
