# tools · 测试工具产物区

> 报告模板要求声明测试工具（Postman / JMeter）并内嵌 JMeter 设置截图；工具工程文件统一在此归档，报告 MD 引用相对路径。

| 子目录 | 用途 | 交付关联 |
|---|---|---|
| `jmeter/` | 性能测试 jmx 工程、并发参数快照、结果 jtl/csv | 性能测试报告「性能测试场景」节 + 记录簿 PERF sheet |
| `postman/` | 接口测试 collection、环境变量导出（脱敏） | 集成测试报告「测试工具」节 |

命名约定：`{系统码}-{场景}-{YYYYMMDD}.{ext}`（例：`KJZTFWXT-企业查询并发-20261013.jmx`）。

与 `as-built/tools/` 的分工：本目录服务**总集交付报告**；`as-built/tools/` 是 B 线现场勘察脚本工具，过程态不进交付。
