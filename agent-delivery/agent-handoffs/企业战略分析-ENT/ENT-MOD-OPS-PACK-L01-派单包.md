# ENT-MOD-OPS-PACK-L01 派单包

## 任务

- Task ID：`ENT-MOD-OPS-PACK-L01`
- 标题：维护管理 — 门1产品定义包（IA、TRACE、USM与Wireframe）
- 执行：`agent:product-agent`
- 监管：`human:高颖`
- Sprint：`2026-W30`
- 阶段：`product_package` / Track-MS

## 权威输入

- `agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.5.6.3、§1.1.1.2.4.5.6.3.1～3.3
- `agent-delivery/acceptance-catalog/catalog-topic-enterprise.yaml#E-37`
- `agent-handoffs/产品整体定义/权限点清单-菜单与按钮.md`
- `agent-handoffs/产品整体定义/level-perms-matrix.yaml`
- `agent-handoffs/产品整体定义/E-31-企业发展/DATA-ENT-CMS-VS-APP-PARTITION-L01.md`

## 产出

- `agent-handoffs/产品整体定义/E-37-企业维护管理/IA-ENT-OPS.md`
- `agent-handoffs/产品整体定义/E-37-企业维护管理/TRACE-ENT-OPS.yaml`
- `agent-handoffs/产品整体定义/E-37-企业维护管理/USM-ENT-OPS.md`
- `agent-handoffs/产品整体定义/E-37-企业维护管理/Wireframe-ENT-OPS.md`

## 执行边界

- 完整映射 E-37 与 Bid 的三组企业发展内容维护能力。
- 区分 CMS 人工运营内容与应用侧计算事实；不把统计、算法结果或数据批次改成人工维护字段。
- 明确 OPS、L0～L4、编辑与审核发布的权限边界；无 Bid 直接依据的规则标记为产品解释或开放项。
- 本任务只完成核心产品包，不代替 METRIC-OPEN、UX、V1 首轮会签或门1 PDR。

## 状态审计

- 2026-07-22：`human:高颖` 确认解锁并监管，`agent:product-agent` 认领。
- 本机缺少标准 coordinator confirm 脚本与 pending 队列，采用显式批准的本地审计兜底；飞书同步待验证。
