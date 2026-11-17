<!-- feishu-doc {"doc": "UN2sdu11DofIPdxn1zfcK3XgnAb"} 只改标记下面的文字；不要删改 <!-- b:... --> 标记 -->
<!-- b:Zbn6dEMKMopOwJxwNq9csaskne1 text -->
通过zmate的后端和沙箱统一应用提供Agent服务（无状态数字员工），满足上层应用的搭建。后续上层应用服务和zmate标品服务完全解耦，分为Aaas层和应用层进行运维管理。
<!-- b:InCqdplA4oEa8ExiEa1c7ZSPnDf text -->
标品亮点在于：应用的Agent孵化和迭代完全在zmate内部闭环。可以通过助手的交互直接孵化成目标形式的数字员工，然后通过快照得到元虾（MCP+技能组+人格文件），中间可以插入评测模块启动自动化评测。评测完成后可以发布无状态数字员工给到应用层使用。如果需要更新，则同样可以重新实例化重复上述流程。
<!-- b:IerJdVOVToZha0xWpfkcxH2VnKf text -->
从 数字员工的流转 提升为 数字员工助手到数字员工应用的流转/迭代。且后续所有项目产品都可以通过独立模块进行回流，无需考虑zmate标品的兼容。
<!-- b:ESS7dtL4Ho1uvaxLn0SckOs2nJb heading1 -->
产品方向-双线并行和员工流转
<!-- b:UXQPd0o2GoxrQGxe62Echcacnqc heading2 -->
助手和分身员工组成AI办公平台
<!-- b:IzVBdoUufoOMAoxfAkbcxFoenTg text -->
当前呈现的zmate原始平台能力，支持助手和分身两种形式的数字员工，呈现AI-native的虚拟组织架构。
<!-- b:L2CbdVIVLoPCvnxqDjMc1MRPnfb text -->
适用的客户场景：
<!-- b:KWafd8KOgoSIevxlBducO2janvg ordered -->
类claw产品的AI办公中台（清华基金会）
<!-- b:EMaKdaiGYoG8QRxwvIFcpEden3d ordered -->
泛政府企业沟通提效（张江Agentcity）
<!-- b:LU3qdLnnSoDvtXxgEEKccTQRnkh heading2 -->
无状态员工构建AI原生应用
<!-- b:Vlk4djfYqo5rYFx4g2lcaGmqnpc text -->
通过无状态数字员工，支持上游独立应用服务搭建，赋能业务场景落地（AaaS）。应用服务在标品中都是独立部署的，和zmate标品服务解耦。
<!-- b:QiUEdPDQqoMSy2xvGEmcuuS1nCt text -->
适用的客户场景（构建/规划中）：
<!-- b:LYLKdltvEo3Xy3xkLe8cuSTynMe ordered -->
Deep research及泛deep research场景（国科信深度报告写作，长鑫存储deep research）
<!-- b:DOvBd1cjJo0cHuxTsG6c7LBfnqb ordered -->
Browser use（易方达POC）
<!-- b:Ak5PdJzyFo2BCaxAycEc8FzQnMe ordered -->
合同审核（招晓法）
<!-- b:GVdtdvY9ao7CCrxNJLQcedKsntd ordered readonly -->
智能审单（[mention_user]待沟通）
<!-- b:PzAyd9ynuopIe2xnv7pcHo8JnIc ordered readonly -->
团队模式应用（[mention_user]国科信AI战略顾问）
<!-- b:OKald71Zboy4CGx56zdcvji9nQg text -->
助手是孵化源头，可被孵化成分身或无状态员工。孵化的标准由评测模块系统性给出。一个完整的loop是：
<!-- b:Xd4ydMtCEocEnwxam39cAZJZnFc ordered -->
助手交互进行效果优化，在原子测试集上进行冒泡测试
<!-- b:PYnidPAWYoLHcvxDODFct3x7nBb ordered -->
冒泡测试完成后，通过评测模块进行系统性大规模测试
<!-- b:WNS2d6BLSo1pSexKNrScKDTxnxV ordered -->
测试通过认为达到应用上线标准，发布分身上线
<!-- b:RhfPdhbWso1g0dxoCkJcHhsRn9f text -->

<!-- b:J87rdGm9QoodIsxxIYMc4shonRd heading1 -->
技术方向-应用搭建和多Harness兼容
<!-- b:AaffdvAchoh4s8xFqejcRMcunze ordered readonly -->
Deep research应用搭建技术方案可见：[mention_doc]。后续模式参考deep research应用
<!-- b:JHG7dH2idoxICnxSJ2jcwO1fnCc ordered -->
标准化接口拉齐：接口一即Agent sandbox接口统一为openresponse接口协议。接口二即外部AaaS接口统一按照通用接口进行开发（参考公识接口协议）。
<!-- b:Lmh2dH9ENop5Hhxs6wscGx3Inch ordered -->
迁移标准：openclaw适用通用场景，通过评测对照其他agent结果明确是否执行迁移。未来根据项目提供1-2个除openclaw外的agent harness沙箱，核心制品可以自动化横向迁移。
<!-- b:AHUad41qJoqQQexSKUncVSqKnff ordered -->
附加要求：比如DSH的技能组织中有workflow.js这种硬编码能力的plugin，openclaw无原生plan mode等，无法在不同harness中直接执行迁移，在进行数字员工孵化时需要考虑。
<!-- b:NnvJdL7RUo1FWwxXE8Icd06PnJf text -->

<!-- b:QdgNdDr9AojZOLxih0AcAxgDnfh text -->

