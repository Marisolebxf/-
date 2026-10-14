# QA-KJZTFWALGO-FUNCLIST-SPLIT-L01 派单包

监管人：`human:黄敬洲`  
执行 Agent：`qa-agent`  
`task_type: tech_task` · Epic：`E-QA-TOTALSET`  
强度：ponytail off

## 范围（已锁）

sheet「深度挖掘算法」· 四级「科技专题服务算法库」· **60 六级**。工作单元 = 一条六级一个子 agent（L01–L60）。

**不纳入**同 sheet 其余约 52 条六级。

## 已拍板

- 七层：API/模型语义，不写界面
- 规则层：模型级（不按维度复制空态/失败）
- 金样：**L31 企业技术力评估模型**（已出 40 条）
- 整表 ≥4000；金样不硬凑 67/六级
- **全量等人口令**

## 步骤

1. 评金样 `work/L31.md` + `review/L31.md`。按本倍率外推约 2400，低于 4000。
2. 下令全量后再生成其余 `prompts/Lxx.md` 并波次并行（每波 8–12）。
3. 60/60 通过后合表：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`；A1=`智能服务集群-科技专题服务算法库功能点拆分`。
4. handoff + MCP；勿自行 `done`。

## 铁律

唯一需求源 = 该六级 prompt 的名称 + 需规全文。禁止读算法仓/五件套。不写测试步骤。
