# 产业匹配度（M_ENT_INDUSTRY_MATCH_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_INDUSTRY_MATCH_SCORE |
| 指标名称 | 产业匹配度 |
| 一级模块 | 企业分析 |
| 二级模块 | 引育推荐 |
| 三级模块 | 招引推荐 |
| 更新频率 | 产业标签/目标画像更新后 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q015 |


## 口径定义

指企业主营业务与目标产业在产业结构、产业链协同、资源要素等方面的适配程度，反映企业主营业务与产业发展方向的契合水平。

## 计算逻辑说明

> 来源：陈林等《产业链融入与企业创新——基于微观企业数据的产业链测度新方法》，《中国工业经济》2024年第10期，第62-64页。
 >
 > 测度框架分为三个层次：①基于一阶产业关联测度**产业链关联度 ind_link**；②基于质心运动定理测度**企业产业链质心度 d_f**；③两者相乘得到**企业产业链融入度 ind_chain_f**。



 ##  一、基础矩阵：直接消耗系数矩阵（公式1）

$$
 A = \begin{bmatrix} a_{11} & \cdots & a_{1n} \\ \vdots & \ddots & \vdots \\ a_{n1} & \cdots & a_{nn} \end{bmatrix}_{n \times n}
$$

 **变量说明：**

| 变量                         | 含义                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| $A$                          | 直接消耗系数矩阵（源自《中国投入产出表》），本文使用2007年135部门表 |
| $N = \{1, 2, 3, \ldots, n\}$ | 产业链的行业集合                                             |
| $n$                          | 行业数量                                                     |
| $a_{ij}$                     | 行业 $i$ 与行业 $j$ 之间的**直接消耗系数**，表示生产1单位 $j$ 行业产品所消耗的 $i$ 行业产品的数量 |

 > 构建逻辑：将产业视为有向图中的"点"（vertex），产业间的投入产出关系视为有物质流向的"边"（edge），直接消耗系数 $a_{ij}$ 视为"边权重"。点集、边集和边权重构成整个有向图。

---

 ## 二、产业链关联度 ind_link（公式2-5）

 ### 公式2：加权产业出度（列向量 $A_2$）

$$
 A_2^T = \left[ \sum_{j} a_{1j}, \; \sum_{j} a_{2j}, \; \cdots, \; \sum_{j} a_{nj} \right]_{1 \times n}
$$

$$
 A_2 = \begin{bmatrix} a_1 \\ a_2 \\ \vdots \\ a_n \end{bmatrix}_{n \times 1}, \quad \text{其中} \quad a_i = \sum_{j=1}^{n} a_{ij}
$$

 **含义：** $a_i$ 为行业 $i$ 的**加权产业出度**（weighted outdegree），即将其他产业与产业 $i$ 之间的直接消耗系数逐列相加。表示产业链中 $i$ 产业的产品作为中间投入被各个产业直接消耗的程度。$A_2$ 即"经济序列度"（degree sequence of economy）。

---

 ### 公式3：产业链关联度（均值加权版本）

$$
\text{ind_link} = C_1 \times A_2
$$

 其中 $C_1$ 为由元素 $\frac{1}{n}$ 构成的 $1 \times n$ 阶行向量：

$$
 C_1 = \left[ \frac{1}{n}, \; \frac{1}{n}, \; \cdots, \; \frac{1}{n} \right]_{1 \times n}
$$

 **含义：** 将加权产业出度做**均值加总**，取均值而忽略各产业规模的差异性。参考 Acemoglu et al. (2009, 2010, 2012)。

---

 ### 公式4：收入权重向量 $C_2$

$$
 C_2 = [c_1, \; c_2, \; \cdots, \; c_n]_{1 \times n}
$$

 **变量说明：**

| 变量  | 含义                                                  |
| ----- | ----------------------------------------------------- |
| $c_i$ | 行业 $i$ **主营业务收入占链上全部主营业务收入的比例** |
| 约束  | $\sum_{i=1}^{n} c_i = 1$                              |

 > 参考 Fan & Lang (2000) 以营业收入赋予点权重计算一体化指数的方法。

---

 ### 公式5：产业链关联度（收入加权版本，最终公式）

$$
\boxed{ \text{ind_link} = C_2 \times A_2 }
$$

 **含义：** 最终的产业链关联度指标，以各行业主营业务收入占比为权重，对加权产业出度进行加权求和。该指标越大，表明各产业部门的产出更广泛地参与了其他产业部门生产，即**产业链内部的关联程度越高**。

 > 这是本文最终采用的 `ind_link` 计算公式。公式3为均值版本（参考用），公式5为收入加权版本（正式采用）。

---

 ## 三、企业产业链质心度 $d_f$（公式6-8）

 ### 公式6：行业上游度 $u_i$

$$
 u_i = 1 \times \frac{X_i}{Y_i} + 2 \times \frac{\sum_{j} a_{ij} X_j}{Y_i} + 3 \times \frac{\sum_{j} \sum_{k} a_{ik} a_{kj} X_j}{Y_i} + \cdots
$$

 **变量说明：**

| 变量     | 含义                                              |
| -------- | ------------------------------------------------- |
| $u_i$    | 行业 $i$ 的**上游度**，基于 Antràs et al. (2012)  |
| $Y_i$    | 行业 $i$ 的**总产出**                             |
| $X_i$    | 行业 $i$ 产出中用于**最终消费**的部分             |
| $a_{ij}$ | 每生产1单位 $j$ 行业产品所需的 $i$ 行业产品的消耗 |

 **含义：** $u_i$ 为行业 $i$ 最终产品与各阶段中间产品在总产出中所占比例的加权平均值。$u_i$ 越大，该行业上游度越高，中间产品与最终产品的距离越远，能影响的"下游"行业越多。约束：$u_i \geq 1$，当且仅当 $i$ 行业所有产品都为最终产品时 $u_i = 1$。

---

 ### 公式7：产业链质心

$$
 c = \sum_{i=1}^{n} (u_i \times c_i)
$$

 **变量说明：**

| 变量  | 含义                                              |
| ----- | ------------------------------------------------- |
| $c$   | **产业链质心**（产业链整体的上游度加权位置）      |
| $u_i$ | 行业 $i$ 的上游度                                 |
| $c_i$ | 行业 $i$ 主营业务收入占链上全部主营业务收入的比例 |

 **含义：** 以各行业上游度乘以收入占比，加总得到产业链的质心位置。质心代表产业链的"重心"所在，即产业链核心地位的企业或产业所处的位置。

---

 ### 公式8：企业产业链质心度 $d_f$

$$
 \boxed{ d_f = \left( 1 - \frac{|u_f - c|}{u_{\max} - u_{\min}} \right) \times \text{production}_f }
$$

 **变量说明：**

| 变量                  | 含义                                                         |
| --------------------- | ------------------------------------------------------------ |
| $d_f$                 | 企业 $f$ 的**产业链质心度**，$0 < d_f < 1$                   |
| $u_f$                 | 企业 $f$ 所在行业的产业链上游度                              |
| $c$                   | 产业链质心（公式7）                                          |
| $\|u_f - c\|$         | 企业 $f$ 与产业链质心之间的距离                              |
| $u_{\max} - u_{\min}$ | 产业链总长度，由上游度最高的行业 $u_{\max}$ 与最低的行业 $u_{\min}$ 之间的距离决定 |
| $\text{production}_f$ | 企业 $f$ 总产值占所在产业链总产值的比重                      |

 **含义：** $d_f$ 越大（趋近1），企业 $f$ 与产业链质心之间的相对距离越小，其**产业链质心度越高**，在产业链中越处于核心地位。该指标结合了企业位置（与质心的距离）和企业规模（产值占比）两个维度。

---

 ## 四、企业产业链融入度 $\text{ind_chain}_f$（公式9，最终公式）

$$
\boxed{ \text{ind_chain}_f = d_f \times \text{ind_link} }
$$

 **变量说明：**

| 变量                 | 含义                                                         |
| -------------------- | ------------------------------------------------------------ |
| $\text{ind_chain}_f$ | 企业 $f$ 的**产业链融入度**（本文核心指标）                  |
| $d_f$                | 企业 $f$ 的产业链质心度（公式8，外部联系指标）               |
| $\text{ind_link}$    | 产业链关联度（公式5，内部联系指标，同一条产业链上企业的共有变量） |

 **含义：** 产业链关联度 `ind_link` 越大，代表企业所处的整个产业链上企业间关联的紧密程度越高，是产业链的**内部联系指标**；企业的产业链质心度 $d_f$ 代表了该企业在本地产业链发展中的影响力和带动力，是**外部联系指标**。两者相乘形成了一个既考察一定地理范围内产业链整体关联是否紧密，又反映企业个体在产业链位置上变化的微观层面综合指标。

---

 ## 五、计算流程总结

 ```
 投入产出表 → 直接消耗系数矩阵 A（公式1）
                     ↓
         加权产业出度 A₂（公式2）
                     ↓
     ┌──── 均值加权 C₁ × A₂（公式3，参考版）
     │              ↓
     │     产业链关联度 ind_link（均值版）
     │
     └──── 收入加权 C₂ × A₂（公式5，最终版）
                        ↓
           产业链关联度 ind_link（最终）──────────────────┐
                                                           │
 投入产出表 → 行业上游度 uᵢ（公式6）                       │
                     ↓                                     │
         产业链质心 c = Σ(uᵢ × cᵢ)（公式7）                │
                     ↓                                     │
      企业质心度 d_f = (1-|u_f-c|/(u_max-u_min)) × prod_f（公式8）
                     ↓                                     │
           企业质心度 d_f ────────────────────────────────┘
                     ↓
     企业产业链融入度 ind_chain_f = d_f × ind_link（公式9）
 ```

---

 ## 六、数据来源表字段

------

**一、产业链关联度 ind_link（公式1-5）**

```
dwd_industry_chain_info（industry_code, industry_link_code, level, parent_code, industry_link_name, node_company_count）— 产业链层级结构
dwd_org_industry_tags（credit_code, industry_code, industry_link_code, company_name）— 企业与产业链节点关联
dwd_org_annual_financial_info（org_id, industry_name, main_business_revenue）— c_i 行业主营业务收入及占比
```

**缺口说明：** `a_ij`（直接消耗系数）、`Y_i`（行业总产出）、`X_i`（行业最终消费）来自《投入产出表》，doc 目录的 4 个 xlsx 中**没有这张表**。公式1-2、公式6 无法仅靠现有数据源计算。

------

**二、企业质心度 d_f**

```
dwd_org_base_info（org_id, industry, industry_l1_code, industry_l2_code, industry_l3_code, city, province）— 企业行业归属 + 地级市限定
dwd_org_annual_financial_info（org_id, year, operating_revenue, main_business_revenue）— production_f 企业产值/收入
```

------

**三、企业间关联关系（构建产业链图谱"点"与"边"，DFS 搜链）**

```
dwd_org_shareholder_info（org_id, inv_org_id, owners_name, ownership_percentage）— 股东/持股关系（边）
dwd_org_invest_info（org_id, inv_org_id, investment_amount, investment_ratio）— 对外投资关系（边）
dwd_org_subsidiary_info（org_id, sub_org_id, sub_name_cn）— 母子公司关系（边）
dwd_org_merger_acquisition_info（acquiring_org_id, acquired_org_id, ma_amount）— 并购关系（边）
```

------

**数据缺口汇总**

| 公式变量                    | 需要数据                                                     | doc xlsx 是否覆盖 |
| --------------------------- | ------------------------------------------------------------ | ----------------- |
| `a_ij` 直接消耗系数         | 投入产出表                                                   | ❌ 缺失            |
| `Y_i` 行业总产出            | 投入产出表                                                   | ❌ 缺失            |
| `X_i` 行业最终消费          | 投入产出表                                                   | ❌ 缺失            |
| `c_i` 行业收入占比          | `dwd_main_business_composition_industry`                     | ✅                 |
| `u_f` 企业行业上游度        | 投入产出表 → 行业映射                                        | ❌ 依赖投入产出表  |
| `production_f` 企业产值占比 | `dwd_org_annual_financial_info` / `dwd_org_stock_finance_info` | ✅                 |
| 企业关联关系（边）          | 股东/子公司/投资/并购【任意一个关系即可】                    | ✅投资/并购缺      |
| 产业链节点结构              | `dwd_industry_chain_info`                                    | ✅                 |
| 供应链/客户关系             | `dwd_org_sc_info`                                            | ❌ xlsx 中无此表   |

核心瓶颈是**投入产出表**。doc 目录的 4 个 xlsx 没有收录这张表，导致公式1-2（`A` 矩阵、`A₂`）和公式6（`u_i`）无法计算，进而 `ind_link`、质心 `c`、`d_f`、`ind_chain_f` 全部无法产出。另外 `dwd_org_sc_info`（供应商/客户关系）在 xlsx 中也不存在，产业链图谱的"边"只能依靠股东、投资、子公司、并购、招投标这 5 种关系构建。

## 源表字段

gkx.dwd_industry_chain_info(industry_code, industry_link_code, level, parent_code, industry_link_name, node_company_count) — 产业链层级结构
gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code, company_name) — 企业与产业链节点关联
gkx.dwd_org_annual_financial_info(org_id, industry_name, main_business_revenue) — 行业主营业务收入及占比(c_i)
gkx.dwd_org_base_info(org_id, industry, industry_l1_code, industry_l2_code, industry_l3_code, city, province) — 企业行业归属+地级市限定
gkx.dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue) — 企业产值/收入(production_f)
gkx.dwd_org_shareholder_info(org_id, inv_org_id, owners_name, ownership_percentage) — 股东/持股关系(边)
gkx.dwd_org_subsidiary_info(org_id, sub_org_id, sub_name_cn) — 母子公司关系(边)



【缺口】投入产出表(a_ij直接消耗系数, Y_i行业总产出, X_i行业最终消费) — 缺失，ind_link/c/d_f/ind_chain_f均无法计算

## 待建字段

缺口：《中国投入产出表》
