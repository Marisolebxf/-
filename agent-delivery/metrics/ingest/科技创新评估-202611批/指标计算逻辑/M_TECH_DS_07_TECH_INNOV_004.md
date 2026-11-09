# 技术创新力综合评估（M_TECH_DS_07_TECH_INNOV_004）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_TECH_DS_07_TECH_INNOV_004 |
| 指标名称 | 技术创新力综合评估 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 技术创新力指标展示 |
| 口径版本 | V1-20260828 |
| 更新频率 | 待确认（pending） |

## 口径定义

将规模（专利数量）、质量（专利质量）、潜力（技术市场潜力）按自定义权重计算的技术创新力综合得分与排名。对象=选定领域，取值 0—100。分数越高技术创新力越强。同M_INNOV_TINN_COMPOSITE计算逻辑。

## 计算逻辑说明

选定领域入集。采用加权平均，三维：专利数量（专利申请量 / 专利授权量）/ 专利质量（家族规模 / 权利要求数 / 被引次数 / 技术宽度 / 法律状态稳定性）/ 技术市场潜力（转让 / 许可 / 诉讼 / 质押 / 开放许可）。

### 第一步：入集

页面年窗、空间（可选）、领域（IPC 前 4 位或关键词落到 `main_classification_ipcr`）。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；领域键 = `main_classification_ipcr` 前 4 位。空间：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`。无命中不剔除领域，只缩小计入的专利。

一行一个 IPC4。本批至少 2 个领域才做极值归一。缺测维不补 0，剩余维权重重归一。

### 第二步：各指标标准化

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

指标得分$ =norm(x)\times 100$。同一维在**本批领域**内归一。

### 第三步：各维度得分

默认维内等权，页面可改权重，须 \(\sum w=1\)。

$$
专利数量=0.5\cdot norm(申请量)+0.5\cdot norm(授权量)
$$

$$
专利质量=\frac{norm(家族规模)+norm(权利要求数)+norm(被引)+norm(技术宽度)+norm(法律状态稳定性)}{5}
$$

$$
技术市场潜力=\frac{norm(转让)+norm(许可)+norm(诉讼)+norm(质押)+norm(开放许可)}{5}
$$

### 第四步：综合得分

默认三维等权（各 1/3），页面可改，须 \(\sum W=1\)。

$$
技术创新力综合得分=\sum_{k=1}^{3} W_k\cdot 维度得分_k\times 100
$$

输出：一行一个 IPC4，含各子项原始值、三维得分、`score`（0—100）、`rank`。

| 维度                 | 指标           | 指标说明                                       | 计算方法                                     | 源表字段                                                     | 待建字段 |
| :------------------- | :------------- | :--------------------------------------------- | :------------------------------------------- | ------------------------------------------------------------ | -------- |
| **专利数量（规模）** | 专利申请量     | 反映特定领域内技术创新活动的活跃程度和规模。   | COUNT(DISTINCT pn)                           | dwd_patent(pn, main_classification_ipcr, apdt_year) — IPC领域,申请年 | 无       |
|                      | 专利授权量     | 反映技术创新成果的获批规模和有效转化能力。     | COUNT(DISTINCT pn WHERE granted_number 非空) | dwd_patent(pn, main_classification_ipcr, granted_number, apdt_year) — IPC领域,授权号,申请年 | 无       |
| **专利质量**         | 家族规模       | 反映专利技术保护的地域范围和国际布局。         | 同族成员数合计 / 专利数；空数组记 1          | dwd_patent(pn, main_classification_ipcr, other_Versions, apdt_year) — 同族专利,IPC领域 | 无       |
|                      | 权利要求数     | 反映专利保护范围宽度。                         | 权利要求项数合计 / 专利数                    | dwd_patent(pn, main_classification_ipcr, claims, apdt_year) — 权利要求,IPC领域 | 无       |
|                      | 被引次数       | 反映专利对后续创新的影响力。                   | SUM(cited_by_nums)                           | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利去重,IPC领域 | 无       |
|                      | 技术宽度       | 反映单件专利覆盖的 IPC 小类广度。              | 每件专利 IPC4 去重数合计 / 专利数            | dwd_patent(pn, main_classification_ipcr, further_classification_ipcr, apdt_year) — 主分类,附加分类 | 无       |
|                      | 法律状态稳定性 | 反映仍处于授权/有效且未失效的专利占比。        | 稳定专利数 / 专利数                          | dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年 | 无       |
| **技术市场潜力**     | 转让           | 发生权利转移的专利占比。                       | 转移专利数 / 专利数                          | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利分母,IPC领域 | 无       |
|                      | 许可           | 法律事件含实施许可（不含开放许可）的专利占比。 | 许可专利数 / 专利数                          | dwd_patent_legal(pn, legal_events) — 法律事件                | 无       |
|                      | 诉讼           | 法律事件含诉讼或无效宣告的专利占比。           | 诉讼专利数 / 专利数                          | dwd_patent_legal(pn, legal_events) — 法律事件                | 无       |
|                      | 质押           | 法律事件含质押的专利占比。                     | 质押专利数 / 专利数                          | dwd_patent_legal(pn, legal_events) — 法律事件                | 无       |
|                      | 开放许可       | 法律事件含开放许可的专利占比。                 | 开放许可专利数 / 专利数                      | dwd_patent_legal(pn, legal_events) — 法律事件                | 无       |

## 源表字段

- dwd_patent(pn, kind, granted_number, first_applicant_name, main_classification_ipcr, further_classification_ipcr, claims, other_Versions, apdt_year) — 专利去重,授权号,申请人对齐,主分类,附加分类,权利要求,同族,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_patent_legal(pn, status, expiration_year, legal_events) — 专利状态,到期年,法律事件
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 专利价值评估|华中科技大学|—|万小丽, 朱雪忠. 专利价值的评估指标体系及模糊综合评价[J]. 科研管理, 2008, 29(2): 185-191.

[2]技术创新力｜上海市统计局｜专利申请量与专利授权量｜2009-11-02｜https://tjj.sh.gov.cn/zcjd/20091102/0014-86183.html.

[3]技术创新力｜华中科技大学｜国家自然科学基金项目（70633003）｜万小丽，朱雪忠. 国际视野下专利质量指标研究的现状与趋势[J]. 情报杂志, 2009, 28(7): 49-54.
