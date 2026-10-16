# cycle deep scout

## spins
```
[
  {
    "i": 0,
    "value": "",
    "placeholder": "空则提交时由 ADS 预填",
    "disabled": false,
    "readonly": false,
    "ariaLabel": "",
    "name": "",
    "nearby": "允许 0–100000 亿元"
  },
  {
    "i": 1,
    "value": "12.8",
    "placeholder": "待相邻年市场规模",
    "disabled": false,
    "readonly": false,
    "ariaLabel": "",
    "name": "",
    "nearby": "允许 -50–100 %"
  },
  {
    "i": 2,
    "value": "10.6",
    "placeholder": "待周期模型闭合",
    "disabled": false,
    "readonly": false,
    "ariaLabel": "",
    "name": "",
    "nearby": "允许 -30–100 %"
  },
  {
    "i": 3,
    "value": "84",
    "placeholder": "待周期模型闭合",
    "disabled": false,
    "readonly": false,
    "ariaLabel": "",
    "name": "",
    "nearby": "允许 0–100 分"
  }
]
```

## tabs
```
[
  {
    "text": "产业周期分析",
    "selected": "true",
    "class": "active"
  },
  {
    "text": "诊断记录",
    "selected": "false",
    "class": ""
  },
  {
    "text": "企业 7/50",
    "selected": "true",
    "class": "active"
  },
  {
    "text": "产业 3/50",
    "selected": "false",
    "class": ""
  },
  {
    "text": "服务机构 1/50",
    "selected": "false",
    "class": ""
  },
  {
    "text": "区域 · 开发中",
    "selected": "false",
    "class": ""
  }
]
```

## selects
```
[
  {
    "text": "新一代信息技术",
    "title": "新一代信息技术",
    "aria": "集群"
  },
  {
    "text": "INB1701",
    "title": "INB1701",
    "aria": "产业"
  },
  {
    "text": "近5年",
    "title": "近5年",
    "aria": ""
  },
  {
    "text": "全部企业类型",
    "title": "",
    "aria": ""
  }
]
```

## versionHits
权重阈值版本, 模型版本, 数据截至, 正式口径, 近5年, 新一代信息技术, INB1701

## timeOptions
["近3年","近5年"]

## startState
{"disabled":false,"text":"开始分析"}

## afterStart snippets
[
  "调整仅对本次任务生效，提交后冻结。市场规模可手填；留空则由 ADS（QC06）预填，禁止写死演示",
  "正式环境服务端联网检索",
  "大语言模型推理归纳",
  "输出阶段判断与趋势预测报告",
  "版本与数据血缘快照；任务创建后冻结（不含业务范围字段）"
]

## textSample
```
产业周期分析
诊断记录
产业周期分析
分析配置
结果仅消费 Java GetResult；无返回时保持空态。不以实时全网检索或生产算法完成态对外宣称。
本次分析上下文
在此选择分析对象；所属产业链按 Tab 决定是否需确认；周期含分析时间范围
分析对象
新一代信息技术
INB1701
分析时间范围
近5年
产业关键参数
可调整本次参数，提交后冻结。
当前为固定演示配置，不作为实时生产结论；阈值正式口径待闭合。
选择
	
指标名称
	
分组 / 维度
	
数据状态
	
参数值
	
数据来源
	
指标说明


	
市场规模
	
产业关键参数
	
可用
	
允许 0–100000 亿元
	
产业市场快照
	
查看


	
市场增长率
	
产业关键参数
	
可用
	
允许 -50–100 %
	
产业景气快照
	
查看


	
利润率
	
产业关键参数
	
可用
	
允许 -30–100 %
	
产业盈利快照
	
查看


	
技术成熟度
	
产业关键参数
	
可用
	
允许 0–100 分
	
技术成熟度快照
	
查看
调整仅对本次任务生效，提交后冻结。市场规模可手填；留空则由 ADS（QC06）预填，禁止写死演示数字。
市场规模（QC06 / M_CHAIN_MARKET_SIZE）走 ADS 预填或用户覆盖；禁止填入 12800 等演示数字。
当前使用临时默认参数；权重状态：本次可调；阈值状态：正式口径待闭合。
参数范围校验通过 · 权重状态：本次可调 · 阈值状态：正式口径待闭合
重置参数
开始分析
数据检索与生成设置
周期模型自定义与报告生成的数据链路
检索数据范围
产业历史数据、市场数据、最新产业动态
检索方式
正式环境服务端联网检索
当前结果仅当 Java 返回检索快照时展示，不伪造事件
报告生成方式
大语言模型推理归纳
输出阶段判断与趋势预测报告
本次分析配置
版本与数据血缘快照；任务创建后冻结（不含业务范围字段）
权重阈值版本
模型版本
数据截至
```
