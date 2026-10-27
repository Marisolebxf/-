/**
 * 一次性回填 20260826-50892-search-full/scripts/{id}/
 * 原始全量脚本只把 {id,status,note} 回聊天，空目录；本脚本按 schema 写出 result.yaml + steps.md。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const RUN = path.resolve(__dirname, '../runs/20260826-50892-search-full');
const CASES = path.join(RUN, 'scripts');
const SHOT = path.join(RUN, 'screenshots');

const URL = 'https://edu.itic-sci.com/tts/svcz/enterprise/enterprise-search';
const EXEC = '2026-08-26T21:14:02+08:00';
const BACKFILL = '2026-08-27T21:45:00+08:00';

const SMART_NAMES = [
  '深圳市知道人工智能有限公司',
  '广州索迹人工智能科技有限公司',
  '东莞市爱贝壳人工智能有限公司',
  '广州市镜淇人工智能技术有限公司',
  '沧浪之水人工智能科技（深圳）有限公司',
  '深圳云启智联人工智能合伙企业（有限合伙）',
  '深圳抖云引擎人工智能有限公司',
  '良胜数字人工智能（深圳）有限公司',
  '深圳市天枢人工智能应用有限公司',
  '晟淏智算人工智能科技（深圳）有限公司',
  '广州极智云脑人工智能科技有限公司',
  '广州未来人工智能企业孵化有限公司',
  '小惟科技（深圳）有限公司',
  '深圳市愿景人工智能科技有限公司',
  '精准学（广州）人工智能科技有限公司',
  '深圳市新创智慧科技有限公司',
];

const COMPANY_NAMES = [
  '广州索迹人工智能科技有限公司',
  '沧浪之水人工智能科技（深圳）有限公司',
  '良胜数字人工智能（深圳）有限公司',
  '精准学（广州）人工智能科技有限公司',
  '深圳抖云引擎人工智能有限公司',
  '深圳市天枢人工智能应用有限公司',
  '广州未来人工智能企业孵化有限公司',
  '深圳市知道人工智能有限公司',
  '东莞市爱贝壳人工智能有限公司',
  '深圳云启智联人工智能合伙企业（有限合伙）',
  '晟淏智算人工智能科技（深圳）有限公司',
  '广州极智云脑人工智能科技有限公司',
  '深圳市愿景人工智能科技有限公司',
  '广州市镜淇人工智能技术有限公司',
];

const TABS = [
  '工商概况',
  '主要团队',
  '资质荣誉',
  '知识产权',
  '经营财务',
  '供应链关系',
  '关系图谱',
  '舆情动态',
  '风险信息',
  '招投标',
];

function yamlList(arr, indent = 2) {
  return arr.map((x) => `${' '.repeat(indent)}- ${x}`).join('\n');
}

function copyShot(fromRel, destDir, destName) {
  const src = path.join(SHOT, fromRel);
  if (!fs.existsSync(src)) return null;
  const dest = path.join(destDir, destName);
  fs.copyFileSync(src, dest);
  return `screenshots/${destName}`;
}

const meta = [
  {
    id: 'P0-01',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00003',
    title: '登录后企业查询默认智能搜索，四层主视觉可见',
    verdict: 'pass',
    note: '会话已登录。智能搜索 selected；搜索框、搜索按钮、示例查询、热门场景均可见。',
    shots: [['cases/P0-01/after-land.png', 'after-land.png']],
    steps: `1. goto /enterprise/enterprise-search（脚本进入时已在该路由，未重复登录）
2. 断言 URL 含 enterprise-search
3. tab「智能搜索」aria-selected=true
4. 可见长占位搜索框与「搜索」按钮
5. 可见独立区块「示例查询」「热门场景」
6. 截图 after-land.png

判定：pass。`,
  },
  {
    id: 'P0-02',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00004',
    title: '点击示例查询只回填关键词，不自动出检索结果',
    verdict: 'pass',
    note: '点示例「人工智能」后搜索框值为人工智能，当时未见「智能搜索结果」标题。',
    steps: `1. 点示例查询 chip「人工智能」
2. 读搜索框 inputValue = 人工智能
3. 800ms 内不可见「智能搜索结果」

判定：pass（只回填、不自动提交）。`,
  },
  {
    id: 'P0-03',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00002',
    title: '智能搜索「人工智能」返回长卡片结果',
    verdict: 'pass',
    note: '2026-08-26 脚本只记「命中 16 + 有查看画像」。2026-08-27 补采 16 家全名单与卡片字段，见 observed.yaml。',
    observed: 'smart',
    shots: [
      ['cases/P0-03/after-search.png', 'after-search.png'],
      ['smart-16.png', 'smart-16.png'],
    ],
    extraYaml: `actual:
  heading: 智能搜索结果
  hit_text: 命中 16 家企业
  condition: "智能输入：人工智能"
  names:
${yamlList(SMART_NAMES, 4)}
  first_three:
${yamlList(SMART_NAMES.slice(0, 3), 4)}
  name_without_keyword:
    - 小惟科技（深圳）有限公司
  card_fields_seen: [在营, 微型/小型, 法定代表人, 成立, 注册资本(万), 区县]
`,
    steps: `1. 搜索框已为「人工智能」（P0-02）后点「搜索」
2. 等待「智能搜索结果」
3. 2026-08-26：断言命中数字文案 + 「查看画像」可见（未写名单）
4. 2026-08-27 回填：翻第 1/2 页采集 16 张长卡片（名称、经营状态、规模、法人、成立、注册资本）

命中 16 家。第 2 页含「小惟科技（深圳）有限公司」（名称不含关键词）。完整名单见 observed.yaml / ../../observed/smart-search-人工智能.yaml。

判定：pass。公司全名不作硬期望。`,
  },
  {
    id: 'P0-04',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00011',
    title: '打开第一家企业画像抽屉不跳路由，十页签名称冒烟',
    verdict: 'pass',
    note: '抽屉内十页签齐。须在 .arco-drawer 内断言。页内多为暂无数据/待接入，不 Fail。',
    observed: 'drawer',
    shots: [
      ['cases/P0-04/after-drawer.png', 'after-drawer.png'],
      ['drawer-tabs.png', 'drawer-tabs.png'],
    ],
    extraYaml: `opened: 深圳市知道人工智能有限公司
actual:
  jumped_to_detail_route: false
  drawer: true
  tabs:
${yamlList(TABS, 4)}
  missing_tabs: []
  tab_bodies_summary:
    工商概况: 经营范围 - ；注册地址 深圳市福田区沙头街道天安社区泰然四路113号泰然科技园210栋六层6E09；官网/电话/邮箱均为 - ；可见 topic/v1/profile/basic+overview
    主要团队: 列 姓名/职务 · 暂无数据
    资质荣誉: 列 资质荣誉/类别/认定时间 · 暂无数据
    知识产权: 列 专利名称/类型/日期/状态 · 暂无数据
    经营财务: 总资产/净利润/研发投入均为 - ；近年营收趋势 暂无营收趋势
    供应链关系: 列 关联方/关系 · 暂无数据
    关系图谱: 暂无关系图谱
    舆情动态: 暂无舆情
    风险信息: 待源（司法/失信，Q020）；18 类计数均为 0
    招投标: 待源（招投标三方）· 暂无数据
`,
    steps: `1. 点第一家名称「深圳市知道人工智能有限公司」
2. URL 仍为 /enterprise/enterprise-search（不跳 /enterprise/:orgId）
3. 抽屉标题「企业详情」，头部：在营 / 微型 / 法定代表人雷振 / 成立 2026-03-04 / 注册资本(万) 500000
4. 2026-08-26：只核对十页签名称存在
5. 2026-08-27：在 .arco-drawer 内逐个点 [role=tab]，记录每页签可见字段（见 observed.yaml）

判定：pass。页内空/待接入不升 Fail。`,
  },
  {
    id: 'P0-05',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00009',
    title: '结果卡综合竞争力有指标说明入口',
    verdict: 'pass',
    note: '可见「指标说明：综合竞争力」类按钮并可点开。主列表未见 GAP- 字样。',
    steps: `1. Escape 关抽屉（否则挡住列表 ⓘ）
2. 断言按钮 name 含「指标说明：综合竞争力」
3. 点击后出现说明浮层
4. 列表可见文本不含 GAP-

判定：pass。`,
  },
  {
    id: 'P0-06',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00005',
    title: '点击热门场景进入高级筛选并带出结果',
    verdict: 'pass',
    shots: [['cases/P0-06/after-hot-scene.png', 'after-hot-scene.png']],
    note: '点热门场景（专精特新小巨人或首个 chip）后进入高级筛选结果态。as-built：立刻检索，不作「待应用」Fail。',
    steps: `1. goto 企业查询（避免沿用智能搜索结果）
2. 点热门场景 chip
3. 等待「高级筛选结果」或 tab 高级筛选 selected，并出现命中/空态

判定：pass。`,
  },
  {
    id: 'P0-07',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00001',
    title: '查企业按名称关键词搜索，得到长卡片',
    verdict: 'pass',
    note: '2026-08-26 只记命中+占位。2026-08-27 补采名称关键词「人工智能」命中 14 家（少于智能搜索 16）。',
    observed: 'company',
    extraYaml: `actual:
  heading: 查企业结果
  hit_text: 命中 14 家企业
  placeholder: 输入企业名称关键词
  names:
${yamlList(COMPANY_NAMES, 4)}
`,
    steps: `1. goto 企业查询 → tab「查企业」
2. 占位为「输入企业名称关键词」
3. 填「人工智能」→ 搜索
4. 等待「查企业结果」
5. 2026-08-27：翻页采集 14 家名称（9+5）

相对智能搜索少 2 家（小惟科技、深圳市新创智慧科技有限公司）——名称关键词模式不命中非名称匹配。名单见 observed.yaml。

判定：pass。`,
  },
  {
    id: 'P0-08',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00030',
    title: '最近检索可恢复刚才的智能搜索',
    verdict: 'pass',
    note: '最近检索区可见；点含「人工智能」的记录后再次出现智能搜索结果。',
    steps: `1. 滚到 Hub「最近检索」
2. 点含「人工智能」的历史 tag
3. 再次出现「智能搜索结果」

判定：pass。`,
  },
  {
    id: 'P0-09',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00007',
    title: '切换高级筛选后字段库与 Footer 可见',
    verdict: 'pass',
    shots: [['cases/P0-09/advanced-library.png', 'advanced-library.png'], ['advanced-clear.png', 'advanced-clear.png']],
    extraYaml: `actual:
  field_lib_title: 高级筛选 · 字段库
  fields_seen: [企业所属地区, 经营状态]
  footer: [保存为查询方案, 使用查询方案, 清空条件, 应用筛选]
`,
    note: '字段库标题、地区字段、Footer 四按钮均可见。',
    steps: `1. goto → tab「高级筛选」
2. 可见「高级筛选 · 字段库」与「企业所属地区」
3. Footer：保存为查询方案 / 使用查询方案 / 清空条件 / 应用筛选

判定：pass。`,
  },
  {
    id: 'P0-10',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00007',
    title: '叠加地区与经营状态后应用筛选出结果',
    verdict: 'pass',
    note: '叠加经营状态「在营」后点应用筛选，出现高级筛选结果或命中文案。',
    steps: `1. 在字段库点「经营状态」→「在营」
2. 点「应用筛选」
3. 出现「高级筛选结果」或「命中 N 家企业」或明确空态

判定：pass。本轮未钉死命中数字。`,
  },
  {
    id: 'P0-11',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00036',
    title: '企业所属地区为全国级联，非仅深圳区县',
    verdict: 'pass',
    shots: [['cases/P0-11/region-tree.png', 'region-tree.png'], ['region-tree.png', 'region-tree-root.png']],
    extraYaml: `actual:
  provinces_seen: [北京, 广东, 浙江, 上海, 江苏, 山东, 四川]
`,
    note: '地区树可见北京/广东/浙江/上海/江苏/山东/四川，不是只有深圳区县。',
    steps: `1. 高筛点「企业所属地区」→「请选择所属地区」
2. 树节点含多个省级名称

判定：pass。`,
  },
  {
    id: 'P0-12',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00034',
    title: '保存为查询方案后可再使用',
    verdict: 'pass',
    note: '弹出保存筛选模板；首轮曾被双按钮 strict mode 打断，复测通过。使用方案会直接 apply。',
    steps: `1. 已有条件时点 Footer「保存为查询方案」（勿点结果区同名按钮）
2. 弹层「保存筛选模板」，填 as-built-qa-ent-search，确定
3. 使用查询方案可恢复条件（本轮记 modal 打开即过）

判定：pass。`,
  },
  {
    id: 'P0-13',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00009',
    title: '结果区四类排序均可切换',
    verdict: 'pass',
    note: '综合竞争力优先 / 有效专利数 / 最新营收 / 成立时间 均可选，切换后列表仍在。',
    steps: `1. 打开排序 combobox
2. 依次选：有效专利数、最新营收、成立时间、综合竞争力优先
3. 每次切换后仍可见结果列表

判定：pass。不核对数值单调。`,
  },
  {
    id: 'P0-14',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00037',
    title: '结果内再筛可改变列表且可放宽',
    verdict: 'pass',
    note: '工具条「经营状态」再筛可见，可选「在营」。',
    steps: `1. 点结果工具条 combobox「经营状态」
2. 选「在营」，Escape
3. 列表仍在结果态

判定：pass。条数变化未钉死。`,
  },
  {
    id: 'P0-15',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00010',
    title: '命中超过一页时可翻到第 2 页',
    verdict: 'pass',
    observed: 'smart',
    extraYaml: `actual:
  hit: 16
  page_size: 9
  page2_names:
${yamlList(SMART_NAMES.slice(9), 4)}
`,
    note: '命中 16>9，第 2 页 7 家，见 observed。',
    steps: `1. 从「命中 16 家企业」解析 N>9
2. 点分页「2」
3. 2026-08-27 记录第 2 页 7 家名称

判定：pass。`,
  },
  {
    id: 'P0-16',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00010',
    title: '勾选本页至少两家后批量加入对比',
    verdict: 'pass',
    note: '勾选后出现「已选 N 家企业」条；批量「加入对比」可点。无「全选本页」按钮（as-built）。',
    steps: `1. 勾选前两张卡 checkbox
2. 出现「已选」条
3. 点批量「加入对比」

判定：pass。`,
  },
  {
    id: 'P0-17',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00045',
    title: '检索/地区请求走专题 Java 门面，不打 demo-*',
    verdict: 'pass',
    extraYaml: `actual:
  path_prefix: /api/enterprise/topic/v1/*
  demo_star: false
  samples:
    - /api/enterprise/topic/v1/search/meta/
    - recommend
    - search-biz/history
    - compare-basket
  open: 对比篮查询带 user_id=guest（已登录 admin），本轮不升 C1
`,
    note: '请求 /api/enterprise/topic/v1/* ；无 demo-*。对比篮 user_id=guest 记开放项。',
    steps: `1. 汇总本页 performance resource
2. 存在 topic/v1；路径不含 demo-svc / demo-algo

判定：pass。`,
  },
  {
    id: 'P0-18',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00003',
    title: '三个检索 Tab 正向切换，各模式主区正确',
    verdict: 'pass',
    extraYaml: `actual:
  tabs: [智能搜索, 查企业, 高级筛选]
  查企业_placeholder: 输入企业名称关键词
  高级筛选: 字段库可见
  智能搜索: 长占位搜索框可见
`,
    note: '三 Tab 切换：查企业占位、高筛字段库、智能搜索长框均正确。',
    steps: `1. 点「查企业」→ 名称关键词框
2. 点「高级筛选」→ 字段库
3. 点「智能搜索」→ 长占位框

判定：pass。`,
  },
  {
    id: 'P1-01',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00006',
    title: '初始态展示推荐企业',
    verdict: 'n/a',
    shots: [['cases/P1-01/recommend.png', 'recommend.png']],
    note: '本会话进入时已是结果态，多次 goto 未稳定回到推荐区。不升 Fail。',
    steps: `1. goto 企业查询，等待「推荐企业」
2. 本轮多次刷新仍常停在上次检索结果
3. 按 allow 记 n/a，需干净会话再跑

判定：n/a。`,
  },
  {
    id: 'P1-02',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00044',
    title: '推荐卡有单企理由；机制说明随评审开关',
    verdict: 'n/a',
    note: '依赖 P1-01 推荐区，本轮未构成前置。',
    steps: `未进入稳定推荐区，跳过。

判定：n/a。`,
  },
  {
    id: 'P1-03',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00012',
    title: '必无命中词搜索后纠错空态',
    verdict: 'pass',
    extraYaml: `actual:
  keyword: ZZQXNOHIT99999xyz
  empty_hint: 未命中结果
  recommend_visible: false
`,
    note: 'ZZQXNOHIT99999xyz 未命中且无推荐企业分区。',
    steps: `1. 智能搜索填 ZZQXNOHIT99999xyz → 搜索
2. 可见「未命中结果」
3. 不可见「推荐企业」

判定：pass。`,
  },
  {
    id: 'P1-04',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00011',
    title: '结果卡「查看画像」打开抽屉且不跳路由',
    verdict: 'pass',
    observed: 'drawer',
    extraYaml: `actual:
  url_still: /enterprise/enterprise-search
  tabs:
${yamlList(TABS, 4)}
`,
    note: '点「查看画像」抽屉十页签；与 P0-04 同源，详见抽屉 observed。',
    steps: `1. Escape 关已开抽屉
2. 点第一张卡「查看画像」
3. URL 仍含 enterprise-search；页签含工商概况等十项

判定：pass。页内正文见 ../../observed/drawer-深圳市知道人工智能有限公司.yaml。`,
  },
  {
    id: 'P1-05',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00013',
    title: '单企加入对比篮后可打开对比篮',
    verdict: 'pass',
    shots: [['cases/P1-05/basket.png', 'basket.png']],
    note: '工具区「打开对比篮」可见并可打开。',
    steps: `1. 点「打开对比篮」
2. 抽屉/浮层出现

判定：pass。as-built：结果区有对比篮按钮，旧表「页内无聚合」不作 Fail。`,
  },
  {
    id: 'P1-06',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00035',
    title: '高筛 Footer「清空条件」可用',
    verdict: 'pass',
    note: '清空条件后 Footer「保存为查询方案」仍在。',
    steps: `1. 高筛点「清空条件」
2. 保存/应用按钮仍可见

判定：pass。`,
  },
  {
    id: 'P1-07',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00032',
    title: '查企业 Tab 下热门场景同样进入高筛结果',
    verdict: 'pass',
    note: '查企业点热门场景后进入高级筛选结果。',
    steps: `1. tab 查企业
2. 点热门场景 chip
3. 结果标题为高级筛选结果或 tab 高级筛选 selected

判定：pass。`,
  },
  {
    id: 'P1-08',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00033',
    title: '内部评审模式开关控制溯源挂载',
    verdict: 'pass',
    note: '人设菜单内「内部评审模式」开关可点，未踢出企业查询。',
    steps: `1. 点顶栏人设
2. 拨「内部评审模式」开再关
3. 仍在企业查询

判定：pass。`,
  },
  {
    id: 'P1-09',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00038',
    title: '结果内再筛收到 0 条时保留结果工具区',
    verdict: 'n/a',
    note: '本轮未构造再筛 0 命中。allow_skip。',
    steps: `未强制互斥再筛到 0 条。

判定：n/a。`,
  },
  {
    id: 'P1-10',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00039',
    title: '结果工具条「选择区域」可打开级联',
    verdict: 'pass',
    note: '控件「选择区域」可见可点。',
    steps: `1. 点结果工具条「选择区域」
2. 级联打开后 Escape

判定：pass。`,
  },
  {
    id: 'P1-11',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00014',
    title: '导出当前结果打开确认框',
    verdict: 'pass',
    shots: [['cases/P1-11/export-modal.png', 'export-modal.png']],
    extraYaml: `actual:
  modal_title: 确认导出查询清单
  clicked_create_task: false
`,
    note: '弹出「确认导出查询清单」后点取消；未等 PDF。',
    steps: `1. 点「导出当前结果」
2. 弹层「确认导出查询清单」
3. 点取消（不创建导出任务）

判定：pass。`,
  },
  {
    id: 'P1-12',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00002',
    title: '智能搜索页无大模型/意图识别能力承诺',
    verdict: 'pass',
    note: '可见文本不含「大模型」「意图识别」「自然语言理解」。',
    steps: `1. 在智能搜索结果态读 body 文本
2. 无上述能力承诺词

判定：pass。`,
  },
  {
    id: 'P1-13',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00001',
    title: '查企业「热门企业」chip 回填并立即检索',
    verdict: 'pass',
    note: '有热门企业区时点击立即出查企业结果（与示例只回填不同）。',
    steps: `1. tab 查企业
2. 点热门企业区第一个 chip
3. 出现「查企业结果」

判定：pass。`,
  },
  {
    id: 'P1-14',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00005',
    title: '带 mode=advanced 进入时可见面包屑',
    verdict: 'pass',
    extraYaml: `actual:
  crumb: [企业分析, 企业查询, 高级筛选]
`,
    note: '?mode=advanced 可见企业分析 / 企业查询 / 高级筛选。',
    steps: `1. goto /enterprise/enterprise-search?mode=advanced
2. 面包屑含企业分析、企业查询、高级筛选

判定：pass。`,
  },
  {
    id: 'P1-15',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00002',
    title: '智能搜索后出现匹配字段 chip 或兜底文案',
    verdict: 'pass',
    extraYaml: `actual:
  feedback: 智能输入：人工智能（条件摘要 / 已匹配字段类文案）
`,
    note: '有「已匹配字段」或「未命中预设字段」或条件「智能输入：人工智能」。',
    steps: `1. 智能搜索结果态读匹配反馈
2. 本轮可见条件「智能输入：人工智能」

判定：pass。`,
  },
  {
    id: 'P1-16',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00011',
    title: '关闭画像抽屉后仍保留查询结果态',
    verdict: 'pass',
    note: 'Escape 关抽屉后仍可见智能搜索结果。',
    steps: `1. Escape
2. 仍可见「智能搜索结果」与命中条数

判定：pass。`,
  },
  {
    id: 'P1-17',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00008',
    title: '字段库可收起再展开',
    verdict: 'pass',
    note: '收起字段库后出现「展开字段库」，再展开字段标签可见。',
    steps: `1. 高筛点「收起字段库」
2. 点「展开字段库」

判定：pass。`,
  },
  {
    id: 'P1-18',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00008',
    title: '结果态「编辑高级筛选」回到字段库',
    verdict: 'pass',
    note: '点编辑高级筛选回到字段库。',
    steps: `1. 高筛结果态点「编辑高级筛选」
2. 回到「高级筛选 · 字段库」

判定：pass。`,
  },
  {
    id: 'P1-19',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00009',
    title: '结果卡「引育候选」可加入招引候选',
    verdict: 'pass',
    note: '「引育候选」按钮可点，菜单含招引候选。',
    steps: `1. 点「引育候选」
2. 点「招引候选」类菜单项

判定：pass。`,
  },
  {
    id: 'P1-20',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00009',
    title: '结果仅为长卡片，无表格/卡片视图切换',
    verdict: 'pass',
    note: '不可见「表格视图」「卡片视图」。',
    steps: `1. 结果态扫描可见文本
2. 无双视图切换

判定：pass。`,
  },
  {
    id: 'P1-21',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00030',
    title: '清空最近检索后当前模式记录消失',
    verdict: 'pass',
    note: '点最近检索行「清空」；已空则提示暂无最近记录。',
    steps: `1. 点最近检索右侧「清空」（勿点高筛清空条件）
2. 出现暂无最近记录或本轮本已为空

判定：pass。`,
  },
  {
    id: 'P1-22',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00043',
    title: '结果卡单企导出图标可见',
    verdict: 'pass',
    note: '长卡右侧 aria-label「导出」按钮可见。未打开弹层。',
    steps: `1. 断言结果卡「导出」图标按钮可见

判定：pass。`,
  },
  {
    id: 'P1-23',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00009',
    title: '可切换排序升序/降序',
    verdict: 'pass',
    note: '「切换排序方向」按钮存在，点击后列表仍在。',
    steps: `1. 点「切换排序方向」两次
2. 列表不白屏

判定：pass。`,
  },
  {
    id: 'P1-24',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00004',
    title: '清除搜索框可回到未提交引导',
    verdict: 'pass',
    note: '清除后回到示例查询/推荐/引导空态之一。',
    steps: `1. 智能搜索出结果后点输入框清除
2. 离开结果态，可见示例或引导

判定：pass。`,
  },
  {
    id: 'P1-25',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00004',
    title: '其它示例查询同样只回填',
    verdict: 'pass',
    extraYaml: `actual:
  example: 集成电路
  filled: true
  auto_submitted: false
`,
    note: '点示例「集成电路」只回填，不出智能搜索结果。',
    steps: `1. goto 企业查询
2. 点示例「集成电路」
3. 框值为集成电路；不可见「智能搜索结果」

判定：pass。`,
  },
  {
    id: 'P1-26',
    func_id: 'ZNFWJQ-KJZTFWXT-v1.0-FUNC-00040',
    title: '勾选后切换评审模式，已选条数仍在',
    verdict: 'n/a',
    note: '本轮未切评审核对已选集合（脚本只确认 P0-16 后已选条仍在，未拨评审开关）。',
    steps: `未构造「勾选后拨内部评审模式」完整路径。

判定：n/a。`,
  },
];

function observedBlock(kind) {
  if (kind === 'smart') {
    return `observed_file: ../../observed/smart-search-人工智能.yaml
`;
  }
  if (kind === 'company') {
    return `observed_file: ../../observed/company-search-人工智能.yaml
`;
  }
  if (kind === 'drawer') {
    return `observed_file: ../../observed/drawer-深圳市知道人工智能有限公司.yaml
`;
  }
  return '';
}

function writeObservedStub(dir, kind) {
  if (kind === 'smart') {
    fs.writeFileSync(
      path.join(dir, 'observed.yaml'),
      `# 本条数据明细（回填 2026-08-27）。完整卡片字段见共享文件。
ref: ../../observed/smart-search-人工智能.yaml
hit: 16
names:\n${yamlList(SMART_NAMES)}
`,
      'utf8',
    );
  } else if (kind === 'company') {
    fs.writeFileSync(
      path.join(dir, 'observed.yaml'),
      `ref: ../../observed/company-search-人工智能.yaml
hit: 14
names:\n${yamlList(COMPANY_NAMES)}
`,
      'utf8',
    );
  } else if (kind === 'drawer') {
    fs.writeFileSync(
      path.join(dir, 'observed.yaml'),
      `ref: ../../observed/drawer-深圳市知道人工智能有限公司.yaml
company: 深圳市知道人工智能有限公司
tabs:\n${yamlList(TABS)}
bodies: 见共享文件（工商概况有注册地址；其余多为暂无数据；风险/招投标标待接入）
`,
      'utf8',
    );
  }
}

for (const c of meta) {
  const dir = path.join(CASES, c.id);
  const shotDir = path.join(dir, 'screenshots');
  fs.mkdirSync(shotDir, { recursive: true });
  const evidence = [];
  for (const [from, to] of c.shots || []) {
    const p = copyShot(from, shotDir, to);
    if (p) evidence.push(p);
  }
  if (c.observed) evidence.push('observed.yaml');
  const evYaml = evidence.length ? `evidence:\n${yamlList(evidence)}\n` : 'evidence: []\n';
  const result = `id: ${c.id}
verdict: ${c.verdict}
func_id: ${c.func_id}
title: ${c.title}
url: "${URL}"
executed_at: "${EXEC}"
evidence_backfilled_at: "${BACKFILL}"
${evYaml}${c.extraYaml || ''}${observedBlock(c.observed)}note: ${JSON.stringify(c.note)}
trace_id: null
fail_class: null
backfill_note: |
  2026-08-26 全量脚本只把判定 JSON 写到 runs/.../results.yaml，cases/${c.id}/ 当时是空目录。
  本文件按脚本动作 + 复测 note 回填；搜名单/抽屉正文于 2026-08-27 对同一环境补采。
`;
  fs.writeFileSync(path.join(dir, 'result.yaml'), result, 'utf8');
  fs.writeFileSync(
    path.join(dir, 'steps.md'),
    `# ${c.id} ${c.title}\n\n${c.steps}\n`,
    'utf8',
  );
  writeObservedStub(dir, c.observed);
}

const n = meta.length;
const files = fs.readdirSync(CASES).filter((d) => fs.existsSync(path.join(CASES, d, 'result.yaml')));
console.log(`wrote ${n} cases; dirs with result.yaml=${files.length}`);
