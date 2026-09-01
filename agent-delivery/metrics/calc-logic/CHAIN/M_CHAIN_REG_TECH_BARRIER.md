# 区域技术壁垒（M_CHAIN_REG_TECH_BARRIER）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_TECH_BARRIER |
| 指标名称 | 区域技术壁垒 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上，因核心技术空白与核心技术封锁形成的技术断链壁垒程度。口径对齐M_CHAIN_TECH_BARRIER_INDEX。

## 计算逻辑说明

第一步：定区域链上专利

从 `dwd_industry_chain_info` 按 `industry_code` 取目标产业链。关联 `dwd_org_industry_tags` 取链上企业（`credit_code`、`company_name`）。用 `credit_code` 关联 `dwd_org_base_info`，按 `province`/`city` 筛目标区域。专利按 `first_applicant_name` 或 `first_current_assignee_name` 与 `company_name` 匹配，按 `patent_id` 去重。

第二步：各指标标准化

各原始指标通过极值归一化法消除量纲，转换为 0—100 之间的标准化得分。对于正向指标（数值越大壁垒越强）：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

其中，\(x_{ij}\) 为区域 \(i\) 在第 \(j\) 个指标上的原始值，\(\min(x_j)\) 和 \(\max(x_j)\) 分别为该指标在同一统计年、同一产业链全部对比区域中的最小值和最大值。全部区域取值相同则该指标得分取 50。

第三步：区域技术壁垒综合得分

$$
区域技术壁垒 = \frac{核心技术空白得分 + 核心技术封锁得分}{2}
$$

| 一级维度 | 具体指标 | 指标定义 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- |
| **技术断链壁垒** | 核心技术空白 | 该区域链上企业连续3年发明专利授权量为0取1，否则取0 | dwd_patent(kind, granted_number, pbdt_year) | 无 |
| | 核心技术封锁 | 区域链上企业在行业内技术距离变大则视为存在技术断链 | dwd_patent(main_classification_ipcr, first_applicant_name) | 无 |

1.核心技术空白

统计年及此前连续3年，该区域链上企业发明专利（`kind` 识别发明，`granted_number` 非空视为授权）授权量为0，则赋值为1；否则赋值为0。公开年用 `pbdt_year`。
$$
核心技术空白 = \begin{cases} 1, & 连续3年发明专利授权量 = 0 \\ 0, & 其他情况 \end{cases}
$$

2.核心技术封锁

基于区域链上企业专利数据，采用 Rosenkopf 和 Almeida 的方法，测算企业间专利类别向量的欧几里得距离。先按企业汇总 `main_classification_ipcr` 占比向量，再计算该区域企业与同产业链其他企业的平均技术距离。若该区域在行业内的技术距离相对上期变大，则视为存在核心技术封锁。
$$
技术距离_{ab} = \sqrt{\sum_{k=1}^{n} (P_{ak} - P_{bk})^2}
$$

其中，\($P_{ak}$) 和 \($P_{bk}$\) 分别为企业 \(a\) 和企业 \(b\) 在第 \(k\) 个专利技术类别上的占比，\(n\) 为专利技术类别总数。技术距离越大，表明企业间的技术差异越大，核心技术封锁越严重。封锁原始值取该区域企业平均技术距离。

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配
- dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市(区域筛选)
- dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, kind, granted_number, pbdt_year, main_classification_ipcr) — 专利去重, 第一申请人匹配, 当前专利权人匹配, 发明识别, 授权判定, 公开年, IPC主分类

## 待建字段

- 无

## 参考文献

- 区域技术壁垒｜北京理工大学管理与经济学院，清华大学公共管理学院｜国家自然科学基金项目（72074027）；北京社科基金重点项目（19JDGLA007）｜常晓涵, 何海燕, 孙磊华, 李浩然. 关键核心技术壁垒对中国产业链升级的影响[J]. 北京理工大学学报（社会科学版）, 2023, 25(6): 184-198.
