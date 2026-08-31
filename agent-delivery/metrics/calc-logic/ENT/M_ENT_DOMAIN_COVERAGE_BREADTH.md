# 覆盖广度（M_ENT_DOMAIN_COVERAGE_BREADTH）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01`。派生自 COUNT；分母 = 15 个全开集群。Q068 仍 🟡。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_DOMAIN_COVERAGE_BREADTH`
- **指标名称**：覆盖广度
- **一级模块**：企业分析
- **二级模块**：重点企业领域分布分析
- **三级模块**：领域分布分析
- **更新频率**：日
- **对齐状态**：全集已锁 15 全开；不加权；企业侧 chain_code 仍未对上 INB
- **是否在数据库**：分母 dim 15 行；分子随 COUNT（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q068；不挂 Q013（权重/深度不进本条）

## 口径定义

国内：`M_ENT_DOMAIN_COVERAGE_COUNT / 激活产业集群数`。

- 分子：上一条 `cluster_id` 去重（未映射不计）。
- 分母：**15 个全开** = `COUNT(*) FROM industry_cluster WHERE is_active=1`。不是节点数、不是 L0 条数、不是「仅有映射的集群」。
- 公式落 **0～1**。页面要百分比再 ×100，不进 8 件套公式。
- 不加权。
- 只国内。国外无法计算。
- 分母为 0：**无法计算**。分子为 0 则广度为 0。
- 产业不是分组维。对象同 COUNT。
- 不等于覆盖未来产业数 / 参与深度 / 多元化指数。

## 计算逻辑说明

```
BREADTH = DOMAIN_COVERAGE_COUNT / 15

15 = COUNT(*) FROM industry_cluster WHERE is_active=1
分子落地见 M_ENT_DOMAIN_COVERAGE_COUNT.md
```

对应 seed `formula`：COUNT/15；分母为 0 无法计算；国外无法计算。

**计算公式文件**：`M_ENT_DOMAIN_COVERAGE_BREADTH.md`

## 源表字段

与 COUNT 同链（派生不另找企业表）：

```
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

分母 JOIN `industry_cluster`（项目 dim，不进 8 件套 `source_tables`）。不读 `dwd_industry_chain_info` 节点。

来源系统（`source_systems`）：产业链要素库。

## 现网探针

不单探分子。分母：`demo_gkxlumenx_dim.industry_cluster` 15 行全开（2026-08-27）。企业侧码不对齐见 COUNT 细稿。

## 待建 / 缺口

- Q068 未甲方确认 15 集群对外目录。
- 分子随 COUNT：上链表须灌 INB。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.2`；STAT。禁止把环节数 / L0 数当全集。禁止把 Q013 权重写进本条。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 广度=COUNT/15 全开*
