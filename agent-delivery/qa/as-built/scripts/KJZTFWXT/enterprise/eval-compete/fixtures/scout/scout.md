# 无头实勘 /enterprise/evaluation?workspace=competitiveness&mode=competitiveness

- surveyed_at: 2026-10-14（headless Chromium · survey-page + 二次探针）
- url: http://111.198.38.90:50892/enterprise/evaluation?workspace=competitiveness&mode=competitiveness
- title: 企业综合竞争力评估 - 科技专题服务系统
- h1: 企业综合竞争力评估
- screenshot: scout.png / page.png

## headings
- 企业综合竞争力评估
- 评估对象
- 评估模板
- 指标与权重
- 数据覆盖与可信度

## 默认态要点
- Tab：当前分析（默认）/ 最近评估
- 空态 CTA：前往对比篮选择企业；开始分析 = disabled
- 模板触发器：综合竞争力标准模板
- 三维：创新能力 40 / 经营能力 40 / 成长能力 20；权重合计：100% · 校验通过
- 分组文案：综合竞争力三域；每行「查看」
- 数据覆盖空态：选择企业后显示数据覆盖与可信度

## 浮层「选择分析企业」（点 CTA 后）
- 副标题：从对比篮勾选本页分析对象，点击「确定」回填；不会发起分析任务。
- 企业 7/50；按企业名称搜索；全部企业类型；重置 / 新增
- 列表：勾选（aria-label^=选择）+ 查看画像 + 移除
- 未勾选：取消选择 / 确定 = disabled
- 产物：scout-overlay-text.txt · scout-overlay.json

## 回填后（勾选确定）
- URL 追加 enterprise_codes[] + source=compare-basket
- 返回对比篮调整对象；按企业名称定位
- 开始分析 = enabled（本环境）
- 可信度区可能仅「全部可信度」+「未找到匹配企业」（五档不全）
- 产物：scout-after-select.json / .png

## 过程态（点开始分析）
- URL：view=processing&analysis_type=competitiveness&task_id=EVAL-YYYYMMDD-NNN
- 文案：综合竞争力评估生成中 / 可视化分析过程 / 取消任务 / 稍后查看
- 2026-10-14 曾见「评估失败 / 生成失败」→ 结果态不可达（脚本 allow_skip）
- 产物：scout-processing.json / .png

## 模板下拉（scout-weights.json）
```
系统模板
综合竞争力标准模板
我的模板（0）
当次自定义配置
当前未保存配置
```

## 权重 spins
- 40 / 40 / 20；readonly=false（与用例「readonly」记载偏差，以实勘为准）
