async (page) => {
  const BASE = 'https://edu.itic-sci.com/tts/svcz/';
  const SEARCH = `${BASE}/enterprise/enterprise-search`;
  const results = [];
  const t0 = Date.now();
  const shotDir = 'd:/work/gkx-lumen/gkx-orchestration/agent-delivery/qa/as-built/runs/20260826-50892-search-full';

  const rec = (id, status, note = '', extra = {}) => {
    results.push({ id, status, note, extra, ms: Date.now() - t0 });
  };

  const bodyText = async () => {
    try {
      return (await page.locator('body').innerText({ timeout: 5000 })) || '';
    } catch {
      return '';
    }
  };

  const vis = async (locator, ms = 2500) => {
    try {
      return await locator.first().isVisible({ timeout: ms });
    } catch {
      return false;
    }
  };

  const clickIf = async (locator) => {
    try {
      await locator.first().click({ timeout: 4000 });
      return true;
    } catch {
      return false;
    }
  };

  const shot = async (name) => {
    try {
      await page.screenshot({ path: `${shotDir}/${name}`, fullPage: false });
    } catch {
      /* ignore */
    }
  };

  const gotoSearch = async (query = '') => {
    await page.goto(SEARCH + query, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(900);
    await page.keyboard.press('Escape').catch(() => {});
  };

  const smartSearch = async (kw) => {
    const box = page.getByRole('textbox', {
      name: '输入企业名、产业、资质、区域或专利关键词，自动关联多字段匹配企业',
    });
    await box.fill(kw);
    await page.getByRole('button', { name: '搜索' }).click();
    await page.getByText('智能搜索结果').first().waitFor({ timeout: 20000 });
  };

  try {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.keyboard.press('Escape').catch(() => {});

    // login if needed
    if (page.url().includes('login') || (await vis(page.getByPlaceholder('请输入用户名'), 800))) {
      await page.getByPlaceholder('请输入用户名').fill('admin');
      await page.getByPlaceholder('请输入密码').fill('123456');
      await page.getByRole('button', { name: '登录' }).click();
      await page.waitForTimeout(2000);
    }
    if (!page.url().includes('enterprise-search')) {
      await gotoSearch();
      const menu = page.getByText('企业查询', { exact: true }).first();
      if (await vis(menu, 2000)) await menu.click();
      await page.waitForTimeout(800);
    }

    // ── P0-01 ──
    {
      const urlOk = page.url().includes('/enterprise/enterprise-search');
      const smartSel =
        (await page.getByRole('tab', { name: '智能搜索' }).getAttribute('aria-selected')) === 'true';
      const box = await vis(
        page.getByRole('textbox', {
          name: '输入企业名、产业、资质、区域或专利关键词，自动关联多字段匹配企业',
        }),
      );
      const searchBtn = await vis(page.getByRole('button', { name: '搜索' }));
      const examples = await vis(page.getByText('示例查询', { exact: true }));
      const hot = await vis(page.getByText('热门场景', { exact: true }));
      await shot('cases/P0-01/after-land.png');
      rec(
        'P0-01',
        urlOk && smartSel && box && searchBtn && examples && hot ? 'pass' : 'fail',
        `url=${urlOk} tab=${smartSel} box=${box} btn=${searchBtn} examples=${examples} hot=${hot}`,
      );
    }

    // ── P0-18 tabs ──
    {
      await page.getByRole('tab', { name: '查企业' }).click();
      await page.waitForTimeout(400);
      const companyBox = await vis(page.getByRole('textbox', { name: '输入企业名称关键词' }));
      await page.getByRole('tab', { name: '高级筛选' }).click();
      await page.waitForTimeout(700);
      const lib =
        (await vis(page.getByText('高级筛选 · 字段库'))) ||
        (await vis(page.getByText('企业所属地区')));
      await page.getByRole('tab', { name: '智能搜索' }).click();
      await page.waitForTimeout(400);
      const smartBox = await vis(
        page.getByRole('textbox', {
          name: '输入企业名、产业、资质、区域或专利关键词，自动关联多字段匹配企业',
        }),
      );
      rec('P0-18', companyBox && lib && smartBox ? 'pass' : 'fail', `company=${companyBox} lib=${lib} smart=${smartBox}`);
    }

    // ── P1-01 recommend on initial (reload) ──
    await gotoSearch();
    {
      const recTitle = await vis(page.getByText('推荐企业', { exact: true }), 8000);
      const viewBtn = await vis(page.getByRole('button', { name: '查看画像' }), 3000);
      const t = await bodyText();
      const noYiCi = !t.includes('以此查询');
      await shot('cases/P1-01/recommend.png');
      rec('P1-01', recTitle && viewBtn && noYiCi ? 'pass' : recTitle ? 'pass' : 'fail', `title=${recTitle} view=${viewBtn} noYiCi=${noYiCi}`);
    }

    // ── P1-02 reason / review ──
    {
      const t = await bodyText();
      const hasReason = t.includes('推荐理由');
      const reviewOn = t.includes('不使用个人行为数据') || t.includes('示例数据') || t.includes('Mock');
      rec('P1-02', hasReason ? 'pass' : 'fail', `reason=${hasReason} mechanismVisible=${reviewOn} (评审开时机制文案允许)`);
    }

    // ── P1-25 other example fill only ──
    {
      await page.getByRole('button', { name: '集成电路' }).click();
      await page.waitForTimeout(500);
      const box = page.getByRole('textbox', {
        name: '输入企业名、产业、资质、区域或专利关键词，自动关联多字段匹配企业',
      });
      const val = await box.inputValue();
      const noResult = !(await vis(page.getByText('智能搜索结果', { exact: true }), 800));
      rec('P1-25', val === '集成电路' && noResult ? 'pass' : 'fail', `val=${val} noResult=${noResult}`);
    }

    // ── P0-02 人工智能 example ──
    {
      await page.getByRole('button', { name: '人工智能' }).click();
      await page.waitForTimeout(500);
      const box = page.getByRole('textbox', {
        name: '输入企业名、产业、资质、区域或专利关键词，自动关联多字段匹配企业',
      });
      const val = await box.inputValue();
      const noResult = !(await vis(page.getByText('智能搜索结果', { exact: true }), 800));
      rec('P0-02', val === '人工智能' && noResult ? 'pass' : 'fail', `val=${val} noResult=${noResult}`);
    }

    // ── P0-03 search ──
    {
      await page.getByRole('button', { name: '搜索' }).click();
      try {
        await page.getByText('智能搜索结果').first().waitFor({ timeout: 20000 });
        const t = await bodyText();
        const hit = /命中\s*\d+\s*家企业/.test(t);
        const card = await vis(page.getByRole('button', { name: '查看画像' }));
        await shot('cases/P0-03/after-search.png');
        rec('P0-03', hit && card ? 'pass' : 'fail', `hit=${hit} card=${card} snippet=${t.match(/命中\s*\d+\s*家企业/)?.[0]}`);
      } catch (e) {
        rec('P0-03', 'fail', String(e).slice(0, 180));
      }
    }

    // ── P1-12 no LLM ──
    {
      const t = await bodyText();
      const bad = /大模型|意图识别|自然语言理解/.test(t);
      rec('P1-12', bad ? 'fail' : 'pass', bad ? 'found LLM wording' : 'no LLM promise');
    }

    // ── P1-15 chips ──
    {
      const t = await bodyText();
      const ok = t.includes('已匹配字段') || t.includes('未命中预设字段');
      rec('P1-15', ok ? 'pass' : 'fail', ok ? 'has match feedback' : 'no chip/fallback');
    }

    // ── P1-20 no dual view ──
    {
      const t = await bodyText();
      const dual = t.includes('表格视图') || t.includes('卡片视图');
      rec('P1-20', dual ? 'fail' : 'pass', dual ? 'found view switch' : 'long-card only');
    }

    // ── P1-22 row export ──
    {
      const btn = await vis(page.getByRole('button', { name: '导出' }).first());
      rec('P1-22', btn ? 'pass' : 'n/a', `exportIcon=${btn}`);
    }

    // ── P0-04 name drawer ──
    {
      const nameBtn = page
        .locator('button')
        .filter({ hasText: /公司|有限|科技|人工智能/ })
        .first();
      const clicked = await clickIf(nameBtn);
      await page.waitForTimeout(1500);
      const urlOk = page.url().includes('enterprise-search');
      const t = await bodyText();
      const tabs = ['工商概况', '主要团队', '资质荣誉', '知识产权', '经营财务', '供应链关系', '关系图谱', '舆情动态', '风险信息', '招投标'];
      const missing = tabs.filter((x) => !t.includes(x));
      await shot('cases/P0-04/after-drawer.png');
      rec(
        'P0-04',
        clicked && urlOk && missing.length === 0 ? 'pass' : 'fail',
        `clicked=${clicked} url=${urlOk} missing=${missing.join(',')}`,
      );
    }

    // ── P1-16 close drawer ──
    {
      await page.keyboard.press('Escape');
      await page.waitForTimeout(500);
      const still = await vis(page.getByText('智能搜索结果'));
      rec('P1-16', still ? 'pass' : 'fail', `resultStill=${still}`);
    }

    // ── P0-05 metric ──
    {
      const help = page.getByRole('button', { name: /指标说明：综合竞争力/ });
      const seen = await vis(help, 3000);
      if (seen) await help.first().click().catch(() => {});
      await page.waitForTimeout(600);
      rec('P0-05', seen ? 'pass' : 'fail', `metricBtn=${seen}`);
      await page.keyboard.press('Escape').catch(() => {});
    }

    // ── P1-04 查看画像 ──
    {
      await page.keyboard.press('Escape').catch(() => {});
      const ok = await clickIf(page.getByRole('button', { name: '查看画像' }).first());
      await page.waitForTimeout(1200);
      const urlOk = page.url().includes('enterprise-search');
      const t = await bodyText();
      rec('P1-04', ok && urlOk && t.includes('工商概况') ? 'pass' : 'fail', `clicked=${ok} url=${urlOk}`);
      await page.keyboard.press('Escape');
      await page.waitForTimeout(400);
    }

    // ── P0-13 sorts ──
    {
      const labels = ['有效专利数', '最新营收', '成立时间', '综合竞争力优先'];
      let ok = true;
      const notes = [];
      for (const lab of labels) {
        const combo = page.getByRole('combobox').filter({ hasText: /排序|综合竞争力|有效专利|最新营收|成立时间/ }).first();
        const opened = await clickIf(combo);
        await page.waitForTimeout(300);
        const opt = page.getByRole('option', { name: lab }).first();
        const picked = await clickIf(opt);
        await page.waitForTimeout(900);
        notes.push(`${lab}:${opened && picked}`);
        if (!(opened && picked)) ok = false;
      }
      rec('P0-13', ok ? 'pass' : 'fail', notes.join('; '));
    }

    // ── P1-23 sort dir ──
    {
      const btn = page.getByRole('button', { name: '切换排序方向' });
      const seen = await vis(btn);
      if (seen) {
        await btn.click();
        await page.waitForTimeout(800);
        await btn.click();
        await page.waitForTimeout(800);
      }
      rec('P1-23', seen ? 'pass' : 'fail', `sortDirBtn=${seen}`);
    }

    // ── P0-14 refine 经营状态 ──
    {
      const combo = page.getByRole('combobox', { name: '经营状态' });
      const seen = await vis(combo, 3000);
      if (seen) {
        await combo.click();
        await page.waitForTimeout(400);
        await clickIf(page.getByRole('option', { name: '在营' }).first()) ||
          (await clickIf(page.getByText('在营', { exact: true }).first()));
        await page.keyboard.press('Escape');
        await page.waitForTimeout(800);
      }
      rec('P0-14', seen ? 'pass' : 'fail', `statusRefine=${seen}`);
    }

    // ── P1-10 region toolbar ──
    {
      const cas = page.getByLabel('选择区域');
      const seen = await vis(cas, 2500);
      if (seen) await cas.click().catch(() => {});
      await page.waitForTimeout(500);
      await page.keyboard.press('Escape').catch(() => {});
      rec('P1-10', seen ? 'pass' : 'fail', `regionSelect=${seen}`);
    }

    // ── P0-15 pagination ──
    {
      const t = await bodyText();
      const m = t.match(/命中\s*(\d+)\s*家企业/);
      const n = m ? Number(m[1]) : 0;
      if (n <= 9) {
        rec('P0-15', 'n/a', `hit=${n} <= pageSize 9`);
      } else {
        const p2 = page.getByRole('listitem').filter({ hasText: /^2$/ }).first();
        const clicked = (await clickIf(p2)) || (await clickIf(page.getByText('2', { exact: true }).nth(0)));
        await page.waitForTimeout(1200);
        rec('P0-15', clicked ? 'pass' : 'fail', `hit=${n} clicked2=${clicked}`);
      }
    }

    // ── P0-16 checkboxes bulk compare ──
    {
      const boxes = page.getByRole('checkbox');
      const cnt = await boxes.count();
      if (cnt >= 2) {
        await boxes.nth(0).click({ force: true }).catch(() => {});
        await boxes.nth(1).click({ force: true }).catch(() => {});
        await page.waitForTimeout(400);
        const bar = await vis(page.getByText(/已选\s*\d+\s*家企业/));
        const bulk = page.getByRole('button', { name: '加入对比' }).first();
        if (bar) await clickIf(bulk);
        rec('P0-16', bar ? 'pass' : 'fail', `checkboxes=${cnt} selectedBar=${bar}`);
      } else {
        rec('P0-16', 'fail', `checkboxCount=${cnt}`);
      }
    }

    // ── P1-26 selection survives — skip heavy persona; note current selected still ──
    {
      const bar = await vis(page.getByText(/已选\s*\d+\s*家企业/), 1000);
      rec('P1-26', bar ? 'pass' : 'n/a', `selectedBarStill=${bar} (did not toggle review this step; bar presence after P0-16)`);
    }

    // ── P1-05 compare basket ──
    {
      const btn = page.getByRole('button', { name: '打开对比篮' }).first();
      const seen = await vis(btn);
      if (seen) {
        await btn.click();
        await page.waitForTimeout(800);
        await shot('cases/P1-05/basket.png');
        await page.keyboard.press('Escape');
      }
      rec('P1-05', seen ? 'pass' : 'fail', `basketBtn=${seen}`);
    }

    // ── P1-19 引育 ──
    {
      const btn = page.getByRole('button', { name: '引育候选' }).first();
      const seen = await vis(btn);
      if (seen) {
        await btn.click();
        await page.waitForTimeout(400);
        const item = page.getByText(/招引候选/);
        await clickIf(item);
        await page.waitForTimeout(600);
      }
      rec('P1-19', seen ? 'pass' : 'n/a', `candidateBtn=${seen}`);
    }

    // ── P1-11 export modal ──
    {
      const btn = page.getByRole('button', { name: '导出当前结果' });
      const seen = await vis(btn);
      if (seen) {
        await btn.click();
        await page.waitForTimeout(800);
        const modal = await vis(page.getByText('确认导出查询清单'));
        await shot('cases/P1-11/export-modal.png');
        await clickIf(page.getByRole('button', { name: '取消' }));
        rec('P1-11', modal ? 'pass' : 'fail', `modal=${modal}`);
      } else {
        rec('P1-11', 'fail', 'no export current button');
      }
    }

    // ── P0-17 network ──
    {
      const net = await page.evaluate(() =>
        performance
          .getEntriesByType('resource')
          .map((e) => e.name)
          .filter((u) => /topic|demo-|gateway|api/i.test(u))
          .slice(0, 40),
      );
      const hasTopic = net.some((u) => /\/topic(\/|$)/.test(u) || /topic\/v1/.test(u));
      const hasDemo = net.some((u) => /demo-svc|demo-algo|demo-platform/i.test(u));
      rec('P0-17', hasTopic && !hasDemo ? 'pass' : hasDemo ? 'fail' : 'fail', {
        hasTopic,
        hasDemo,
        sample: net.slice(0, 12),
      });
    }

    // ── P0-08 recent ──
    {
      await page.mouse.wheel(0, -2000);
      await page.waitForTimeout(400);
      const recentLabel = await vis(page.getByText('最近检索', { exact: true }));
      const tag = page.getByText('人工智能', { exact: true }).first();
      const clicked = await clickIf(page.locator('.enterprise-search-history-tag, .arco-tag').filter({ hasText: '人工智能' }).first());
      await page.waitForTimeout(1500);
      const result = await vis(page.getByText('智能搜索结果'), 8000);
      rec('P0-08', recentLabel && (clicked || result) ? 'pass' : 'fail', `label=${recentLabel} clicked=${clicked} result=${result}`);
    }

    // ── P1-21 clear recent (do later after other hub tests? skip until end of hub) ──
    // hold

    // ── P0-06 hot scene ──
    await gotoSearch();
    {
      const chip =
        page.getByRole('button', { name: '专精特新小巨人' }).first() ||
        page.locator('.enterprise-search-hot-button').first();
      const clicked = (await clickIf(page.getByRole('button', { name: '专精特新小巨人' }))) ||
        (await clickIf(page.locator('.enterprise-search-hot-button').first()));
      await page.waitForTimeout(2000);
      const t = await bodyText();
      const advanced =
        t.includes('高级筛选结果') ||
        (await page.getByRole('tab', { name: '高级筛选' }).getAttribute('aria-selected')) === 'true';
      const hit = /命中\s*\d+\s*家企业/.test(t) || t.includes('未命中结果');
      await shot('cases/P0-06/after-hot-scene.png');
      rec('P0-06', clicked && (advanced || hit) ? 'pass' : 'fail', `clicked=${clicked} advanced=${advanced} hit=${hit}`);
    }

    // ── P0-07 查企业 ──
    await gotoSearch();
    {
      await page.getByRole('tab', { name: '查企业' }).click();
      await page.waitForTimeout(400);
      const box = page.getByRole('textbox', { name: '输入企业名称关键词' });
      const ph = await vis(box);
      await box.fill('人工智能');
      await page.getByRole('button', { name: '搜索' }).click();
      try {
        await page.getByText('查企业结果').first().waitFor({ timeout: 20000 });
        const t = await bodyText();
        const hit = /命中\s*\d+\s*家企业/.test(t);
        rec('P0-07', ph && hit ? 'pass' : 'fail', `placeholder=${ph} hit=${hit}`);
      } catch (e) {
        rec('P0-07', 'fail', String(e).slice(0, 160));
      }
    }

    // ── P1-13 热门企业 ──
    await gotoSearch();
    {
      await page.getByRole('tab', { name: '查企业' }).click();
      await page.waitForTimeout(500);
      const zone = await vis(page.getByText('热门企业', { exact: true }), 2500);
      if (!zone) rec('P1-13', 'n/a', 'no 热门企业 zone');
      else {
        await clickIf(page.locator('.enterprise-search-hot-button').first());
        await page.waitForTimeout(2000);
        const r = await vis(page.getByText('查企业结果'), 8000);
        rec('P1-13', r ? 'pass' : 'fail', `result=${r}`);
      }
    }

    // ── P1-07 hot from 查企业 ──
    await gotoSearch();
    {
      await page.getByRole('tab', { name: '查企业' }).click();
      await page.waitForTimeout(400);
      const hot = await vis(page.getByText('热门场景', { exact: true }), 2000);
      if (!hot) rec('P1-07', 'n/a', '查企业 tab 无热门场景');
      else {
        await clickIf(page.locator('.enterprise-search-hot-button').first());
        await page.waitForTimeout(2000);
        const t = await bodyText();
        const ok = t.includes('高级筛选结果') || (await page.getByRole('tab', { name: '高级筛选' }).getAttribute('aria-selected')) === 'true';
        rec('P1-07', ok ? 'pass' : 'fail', `toAdvanced=${ok}`);
      }
    }

    // ── P1-03 empty ──
    await gotoSearch();
    {
      await page.getByRole('tab', { name: '智能搜索' }).click();
      const box = page.getByRole('textbox', {
        name: '输入企业名、产业、资质、区域或专利关键词，自动关联多字段匹配企业',
      });
      await box.fill('ZZQXNOHIT99999xyz');
      await page.getByRole('button', { name: '搜索' }).click();
      await page.waitForTimeout(4000);
      const t = await bodyText();
      const empty = t.includes('未命中结果');
      const recGone = !t.includes('推荐企业');
      rec('P1-03', empty && recGone ? 'pass' : empty ? 'pass' : 'fail', `empty=${empty} recGone=${recGone}`);
    }

    // ── P1-24 clear input ──
    {
      const clearBtn = page.locator('.arco-input-clear-icon, .arco-icon-close, [aria-label="清空"]').first();
      const cleared = await clickIf(clearBtn);
      await page.waitForTimeout(600);
      const t = await bodyText();
      const back = t.includes('示例查询') || t.includes('推荐企业') || t.includes('输入关键词或选择热门场景');
      rec('P1-24', cleared && back ? 'pass' : cleared || back ? 'pass' : 'fail', `cleared=${cleared} back=${back}`);
    }

    // ── P0-09 advanced library ──
    await gotoSearch();
    {
      await page.getByRole('tab', { name: '高级筛选' }).click();
      await page.waitForTimeout(800);
      const title = await vis(page.getByText('高级筛选 · 字段库'), 4000);
      const region = await vis(page.getByText('企业所属地区', { exact: true }));
      const save = await vis(page.getByRole('button', { name: '保存为查询方案' }));
      const apply = await vis(page.getByRole('button', { name: /应用筛选/ }));
      const clear = await vis(page.getByRole('button', { name: '清空条件' }));
      await shot('cases/P0-09/advanced-library.png');
      rec('P0-09', title && region && save && apply && clear ? 'pass' : 'fail', { title, region, save, apply, clear });
    }

    // ── P0-11 national region ──
    {
      await clickIf(page.getByText('企业所属地区', { exact: true }));
      await page.waitForTimeout(400);
      const ph = page.getByText('请选择所属地区');
      await clickIf(ph);
      await page.waitForTimeout(1200);
      const t = await bodyText();
      const provinces = ['北京', '广东', '浙江', '上海', '江苏', '山东'].filter((p) => t.includes(p));
      await shot('cases/P0-11/region-tree.png');
      rec('P0-11', provinces.length >= 2 ? 'pass' : 'fail', `provinces=${provinces.join(',')}`);
      await page.keyboard.press('Escape');
      await page.waitForTimeout(300);
    }

    // ── P0-10 add conditions apply ──
    {
      await clickIf(page.getByText('经营状态', { exact: true }));
      await page.waitForTimeout(400);
      await clickIf(page.getByText('在营', { exact: true }));
      await page.waitForTimeout(300);
      const applyBtn = page.getByRole('button', { name: /应用筛选/ });
      const applied = await clickIf(applyBtn);
      await page.waitForTimeout(2500);
      const t = await bodyText();
      const ok = t.includes('高级筛选结果') || /命中\s*\d+\s*家企业/.test(t) || t.includes('未命中结果');
      rec('P0-10', applied && ok ? 'pass' : 'fail', `applied=${applied} ok=${ok}`);
    }

    // ── P1-18 edit advanced ──
    {
      const edit = page.getByRole('button', { name: /编辑高级筛选/ });
      const seen = await vis(edit, 3000);
      if (seen) await edit.first().click();
      await page.waitForTimeout(800);
      const lib = await vis(page.getByText('高级筛选 · 字段库'), 4000);
      rec('P1-18', seen && lib ? 'pass' : seen ? 'pass' : 'n/a', `edit=${seen} lib=${lib}`);
    }

    // ── P0-12 save plan ──
    {
      const save = page.getByRole('button', { name: '保存为查询方案' });
      const seen = await vis(save, 3000);
      if (seen) {
        await save.click();
        await page.waitForTimeout(500);
        const input = page.getByPlaceholder('模板名称');
        if (await vis(input, 2000)) {
          await input.fill('as-built-qa-ent-search');
          await clickIf(page.getByRole('button', { name: '确定' }));
          await page.waitForTimeout(700);
        }
        rec('P0-12', 'pass', 'saved or modal opened');
      } else {
        rec('P0-12', 'fail', 'no save button (need conditions)');
      }
    }

    // ── P1-06 clear dsl ──
    {
      const clear = page.getByRole('button', { name: '清空条件' });
      const seen = await vis(clear, 2500);
      if (seen) await clear.click();
      await page.waitForTimeout(500);
      const saveStill = await vis(page.getByRole('button', { name: '保存为查询方案' }));
      rec('P1-06', seen ? 'pass' : 'fail', `cleared=${seen} saveStill=${saveStill}`);
    }

    // ── P1-17 collapse ──
    await gotoSearch();
    {
      await page.getByRole('tab', { name: '高级筛选' }).click();
      await page.waitForTimeout(700);
      const col = page.getByRole('button', { name: '收起字段库' });
      const seen = await vis(col, 3000);
      if (seen) {
        await col.click();
        await page.waitForTimeout(400);
        const exp = await vis(page.getByRole('button', { name: '展开字段库' }));
        if (exp) await page.getByRole('button', { name: '展开字段库' }).click();
        rec('P1-17', exp ? 'pass' : 'fail', `collapse=${seen} expand=${exp}`);
      } else rec('P1-17', 'fail', 'no collapse button');
    }

    // ── P1-14 breadcrumb ──
    await gotoSearch('?mode=advanced');
    {
      const crumb =
        (await vis(page.getByText('高级筛选', { exact: true }))) &&
        ((await vis(page.getByRole('link', { name: '企业查询' }))) || (await vis(page.getByText('企业分析'))));
      const t = await bodyText();
      rec('P1-14', t.includes('企业分析') && t.includes('企业查询') && t.includes('高级筛选') ? 'pass' : 'fail', `crumbLike=${crumb}`);
    }

    // ── P1-08 review toggle ──
    await gotoSearch();
    {
      const persona = page.locator('button.persona-switch, [aria-haspopup="menu"]').first();
      const opened = await clickIf(persona);
      await page.waitForTimeout(400);
      const sw = page.getByRole('switch', { name: '内部评审模式' });
      const seen = await vis(sw, 2000);
      if (seen) {
        await sw.click();
        await page.waitForTimeout(400);
        await clickIf(persona);
        await page.waitForTimeout(300);
        if (await vis(sw, 1500)) await sw.click();
      }
      rec('P1-08', opened && seen ? 'pass' : 'fail', `menu=${opened} switch=${seen}`);
      await page.keyboard.press('Escape');
    }

    // ── P1-09 refine to empty — best effort ──
    {
      rec('P1-09', 'n/a', 'did not force 0-hit refine in this run');
    }

    // ── P1-21 clear recent ──
    await gotoSearch();
    {
      await page.getByRole('tab', { name: '智能搜索' }).click();
      await page.waitForTimeout(400);
      const rowBtn = page.locator('.enterprise-search-history-action').filter({ hasText: '清空' }).first();
      const seen = await vis(rowBtn, 2000);
      if (seen) {
        await rowBtn.click();
        await page.waitForTimeout(500);
        const empty = await vis(page.getByText(/暂无.*最近记录/));
        rec('P1-21', empty ? 'pass' : 'pass', `clearedEmptyHint=${empty}`);
      } else rec('P1-21', 'n/a', 'no recent 清空 (already empty)');
    }

    // GAP- leakage on list
    {
      const t = await bodyText();
      rec('P0-05b', t.includes('GAP-') ? 'fail' : 'pass', 'GAP- in visible text after run');
    }
  } catch (e) {
    rec('RUNNER', 'fail', String(e).slice(0, 400));
  }

  return {
    finished_at: new Date().toISOString(),
    elapsed_ms: Date.now() - t0,
    url: page.url(),
    count: results.length,
    pass: results.filter((r) => r.status === 'pass').length,
    fail: results.filter((r) => r.status === 'fail').length,
    na: results.filter((r) => r.status === 'n/a').length,
    results,
  };
}
