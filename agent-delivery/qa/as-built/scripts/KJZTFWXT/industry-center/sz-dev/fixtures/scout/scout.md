# 无头实勘 /industry-center/shenzhen?workspace=development&tab=development

- surveyed_at: 2026-10-14（BATCH32 · chain-sz-dev）
- url: http://10.50.69.111:30892/industry-center/shenzhen?workspace=development&tab=development
- title: 深圳产业发展分析 - 科技专题服务系统
- h1: 深圳产业发展分析
- screenshot: page.png
- deep: scout-deep.json / scout-probe2.json

## 业务 Tab
- 深圳产业发展分析（默认 aria-selected / class=active）
- 分析记录

## 分析配置（实勘摘要）
- 分析对象：**单级** Select（非对比册双级），placeholder「请选择产业」；选项 15 项（新一代信息技术 / 生物 / 新能源 …）
- 主体区域：readonly input value=`深圳`；文案「主体区域固定为「深圳」，不可更换。」
- 绑定：控件名「有效的深圳产业情况分析对比结果」；placeholder「请显式选择有效结构化结果」（input **readonly**）
- 绑定下拉：有效样例 `CHAIN-20260821-016 · CHAIN-20260821-016`；无效样例 `（无效）导出 PDF 报告 · 不可作为输入`（disabled，点击不绑定）
- 发展目标：checkbox 政策 / 技术 / 人才（默认均勾选）
- 操作：「重置参数」可用；「开始分析」初始 disabled
- 门控：仅选产业仍 disabled；产业 + 有效绑定后 start 可用
- 重置：清绑定回占位、start 回禁用；**产业选中可能残留**（实勘）；目标保持默认勾选；主体深圳不变

## 分析记录
- 过滤：任务状态 / 全部状态
- 失败样例可见时：CHAIN-*-017/018 类型「深圳产业发展分析」状态失败；「查看结果」对失败态 disabled
- 操作集：查看结果 / 复制配置 / 查看报告 / 下载报告 / 删除（空态「暂无数据」时无行）
- 本轮无成功结果态可开（开放项 1）

## 评审（开启态）
- 追溯五枚：深圳产业发展分析×2、系统分析任务交接、深圳对比/发展、发展分析须显式绑定对比结果
- 角标：指标未登记：GAP-CHAIN-SZ-CASE-LIBRARY；口径待甲方确认（开放项 GAP-CHAIN-SZ-CASE-LIBRARY）

## 兄弟隔离
- comparison：有标杆 Q016 / 无发展目标 / 无绑定 placeholder（正向归 chain-sz-compare）
