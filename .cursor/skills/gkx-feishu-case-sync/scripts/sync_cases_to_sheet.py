#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「合规演示用例」覆盖表的【输入或选择】同步到飞书表格新增列（只加列，不改原有列）。

用法（PowerShell，先设 $env:LARK_APP_ID / $env:LARK_APP_SECRET）：
  python sync_cases_to_sheet.py --md-dir <用例目录> --spreadsheet <token> --sheet-id <页签>            # 试跑，只出报告
  python sync_cases_to_sheet.py ... --apply                                                          # 实际写入
匹配策略：标题匹配优先（五级/六级功能名），序号+1 偏移兜底；无匹配/歧义只进报告，不写错行。
"""
import argparse, fnmatch, glob, io, json, os, re, sys, time, urllib.request, urllib.error
from datetime import date

BASE = 'https://open.feishu.cn/open-apis'
PUNCT = re.compile(r'[\s·•。,，、;；:：!！?？「」『』（）()《》<>「」"\'`\-\+_/\\|★✅⚠️❌\[\]]')
CELL_CAP = 4500  # 单元格文本上限，超出截断并标记


def http_json(method, url, payload=None, headers=None, retries=2):
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8') if payload is not None else None
    hdr = {'Content-Type': 'application/json; charset=utf-8'}
    if headers:
        hdr.update(headers)
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=hdr, method=method)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            last = RuntimeError('%s %s -> %s: %s' % (method, url, e.code, e.read().decode('utf-8', 'replace')[:400]))
        except Exception as e:
            last = e
        if i < retries:
            time.sleep(3)
    raise last


def get_token(app_id, app_secret):
    r = http_json('POST', BASE + '/auth/v3/tenant_access_token/internal',
                  {'app_id': app_id, 'app_secret': app_secret})
    if r.get('code') != 0:
        raise RuntimeError('token failed: %s' % r)
    return r['tenant_access_token']


IN_HEADER_PREFIX = '合规用例·输入与条件'
SRC_HEADER = '用例来源文件'


def col_letter(n):
    """1-based column index -> A, Z, AA."""
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(ord('A') + r) + s
    return s


def col_number(letter):
    n = 0
    for ch in str(letter).upper():
        n = n * 26 + ord(ch) - 64
    return n


def cell_text(value):
    if value is None:
        return ''
    if isinstance(value, list):
        return ''.join(cell_text(item) for item in value).strip()
    if isinstance(value, dict):
        return str(value.get('text') or value.get('value') or '').strip()
    return str(value).strip()


def resolve_columns(headers, body_rows):
    """按表头定位；两列都没有时用最左两个全空列。

    返回 (输入列, 来源列, how)。how 为 header / empty / partial / no-empty。
    只找到一列表头时不猜测另一列。
    """
    in_i = src_i = None
    for i, header in enumerate(headers):
        text = cell_text(header)
        if in_i is None and text.startswith(IN_HEADER_PREFIX):
            in_i = i
        if src_i is None and text == SRC_HEADER:
            src_i = i
    if (in_i is None) != (src_i is None):
        return None, None, 'partial'
    if in_i is not None:
        return col_letter(in_i + 1), col_letter(src_i + 1), 'header'
    empty = []
    for i in range(len(headers)):
        if cell_text(headers[i]):
            continue
        if any(cell_text(row[i]) if i < len(row) else '' for row in body_rows):
            continue
        empty.append(i)
        if len(empty) == 2:
            break
    if len(empty) < 2:
        return None, None, 'no-empty'
    return col_letter(empty[0] + 1), col_letter(empty[1] + 1), 'empty'


def row_runs(rows, limit):
    """把行号拆成连续段，且每段不超过 limit 行。"""
    buf = []
    for rn in rows:
        if buf and (rn != buf[-1] + 1 or len(buf) >= limit):
            yield buf
            buf = []
        buf.append(rn)
    if buf:
        yield buf


def _self_check():
    dated = '合规用例·输入与条件（自动同步 2026-11-17）'
    headers = [''] * 13 + [dated, SRC_HEADER]
    assert resolve_columns(headers, []) == ('N', 'O', 'header')
    shifted = ['新列'] + headers
    assert resolve_columns(shifted, []) == ('O', 'P', 'header')
    assert resolve_columns(['功能', dated, ''], [])[2] == 'partial'
    body = [['x', '', 'y'], ['x', '有内容', 'y']]
    assert resolve_columns(['功能', '', '备注'], body)[2] == 'no-empty'
    assert resolve_columns(['功能', '', '', '备注'], [['x', '', '', 'z']]) == ('B', 'C', 'empty')
    inserted = ['新列', '功能', '', '', '备注']
    assert resolve_columns(inserted, [['n', 'x', '', '', 'z']]) == ('C', 'D', 'empty')
    assert col_letter(27) == 'AA' and col_number('AA') == 27
    assert list(row_runs([2, 3, 5, 8, 9], 150)) == [[2, 3], [5], [8, 9]]
    assert list(row_runs([2, 3, 4], 2)) == [[2, 3], [4]]
    print('self-check ok')


def norm(s):
    return PUNCT.sub('', s or '')


def tokens(s):
    parts = re.split(r'[·•／/→]|（[^）]*）|\([^)]*\)', s or '')
    return [PUNCT.sub('', p) for p in parts if len(PUNCT.sub('', p)) >= 3]


def parse_md(path):
    """解析一个用例 md：找含「输入或选择」的覆盖表，返回行列表（含坏行）。"""
    rows, bad = [], []
    with io.open(path, 'r', encoding='utf-8-sig') as f:
        lines = f.read().splitlines()
    hdr_i, cols = None, None
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith('|') and '输入或选择' in s:
            cells = [c.strip() for c in s.strip('|').split('|')]
            if '输入或选择' in cells:
                hdr_i, cols = i, cells
                break
    if hdr_i is None:
        return rows, bad
    in_i = cols.index('输入或选择')
    t_i = cols.index('界面') if '界面' in cols else (1 if len(cols) > 1 else None)
    for l in lines[hdr_i + 2:]:
        s = l.strip()
        if not s.startswith('|'):
            break
        cells = s.strip('|').split('|')
        if len(cells) != len(cols):
            bad.append({'file': os.path.basename(path), 'line': s[:100]})
            continue
        c0 = cells[0].strip()
        m = re.match(r'^(\d+)', c0)
        if not m:
            continue  # 分隔行/表尾
        seq = int(m.group(1))
        title = cells[t_i].strip() if t_i is not None else ''
        rem = c0[m.end():].strip()
        if rem:
            title = (title + ' · ' + rem) if title else rem
        rows.append({'seq': seq, 'title': title, 'input': cells[in_i].strip(),
                     'file': os.path.basename(path)})
    return rows, bad


def main():
    if '--self-check' in sys.argv:
        _self_check()
        return
    ap = argparse.ArgumentParser()
    ap.add_argument('--md-dir', required=True)
    ap.add_argument('--spreadsheet', required=True)
    ap.add_argument('--sheet-id', required=True)
    ap.add_argument('--cols', default='', help='显式指定输入列,来源列（如 N,O）。省略则按表头定位，没有表头时用最左两个全空列')
    ap.add_argument('--self-check', action='store_true', help='只跑列定位自检，不访问飞书')
    ap.add_argument('--filter', default='*', help="只取文件名匹配此 glob 的用例文件，如 'POL-*'")
    ap.add_argument('--merge', action='store_true',
                    help='增量刷新：只重写本次匹配的行，其他行（含空行）保持现状；表头只在缺失时补')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--report', default=None)
    args = ap.parse_args()

    app_id = os.environ.get('LARK_APP_ID') or os.environ.get('FEISHU_APP_ID')
    app_secret = os.environ.get('LARK_APP_SECRET') or os.environ.get('FEISHU_APP_SECRET')
    if not app_id or not app_secret:
        sys.exit('[x] 请设置 LARK_APP_ID / LARK_APP_SECRET（或 FEISHU_APP_ID / FEISHU_APP_SECRET，二者等价）')

    tk = get_token(app_id, app_secret)
    hh = {'Authorization': 'Bearer ' + tk}

    def sheet_values(a1):
        chk = http_json('GET', '%s/sheets/v2/spreadsheets/%s/values/%s?valueRenderOption=ToString'
                        % (BASE, args.spreadsheet, urllib.request.quote('%s!%s' % (args.sheet_id, a1), safe='')),
                        headers=hh)
        if chk.get('code') != 0:
            sys.exit('[x] 读取 %s 失败: %s' % (a1, chk))
        return chk['data']['valueRange'].get('values') or []

    # 1. 页签尺寸，并定位要写的两列
    q = http_json('GET', '%s/sheets/v3/spreadsheets/%s/sheets/%s' % (BASE, args.spreadsheet, args.sheet_id), headers=hh)
    grid_props = q['data']['sheet']['grid_properties']
    n_rows = grid_props['row_count']
    n_cols = grid_props.get('column_count') or 26
    rev0 = None
    print('[i] sheet=%s rows=%s cols=%s' % (args.sheet_id, n_rows, n_cols))

    known_header = ''
    if args.cols.strip():
        parts = [c.strip().upper() for c in args.cols.split(',')]
        if len(parts) != 2 or not all(parts):
            sys.exit('[x] --cols 须是两列，如 N,O')
        col_in, col_src = parts
        how = 'explicit'
        top = sheet_values('%s1:%s1' % (col_in, col_in))
        known_header = cell_text(top[0][0]) if top and top[0] else ''
    else:
        header_row = sheet_values('A1:%s1' % col_letter(n_cols))
        headers = list(header_row[0]) if header_row else []
        headers += [''] * (n_cols - len(headers))
        in_i = next((i for i, h in enumerate(headers) if cell_text(h).startswith(IN_HEADER_PREFIX)), None)
        src_i = next((i for i, h in enumerate(headers) if cell_text(h) == SRC_HEADER), None)
        body_rows = []
        if in_i is None and src_i is None:
            empty_at = [i for i, h in enumerate(headers) if not cell_text(h)]
            if empty_at:
                raw = sheet_values('%s2:%s%d' % (col_letter(empty_at[0] + 1), col_letter(n_cols), n_rows))
                width = n_cols - empty_at[0]
                for row in raw:
                    padded = list(row) + [''] * (width - len(row))
                    body_rows.append([''] * empty_at[0] + padded)
        col_in, col_src, how = resolve_columns(headers, body_rows)
        if how == 'header':
            known_header = cell_text(headers[col_number(col_in) - 1])
        if how == 'partial':
            sys.exit('[x] 只找到一列同步表头（须同时有「%s*」和「%s」），不猜测另一列' % (IN_HEADER_PREFIX, SRC_HEADER))
        if how == 'no-empty':
            sys.exit('[x] 未找到表头「%s*」和「%s」，也没有两个全空列' % (IN_HEADER_PREFIX, SRC_HEADER))
    side_by_side = col_number(col_src) == col_number(col_in) + 1
    print('[i] columns via %s: %s(输入) %s(来源)' % (how, col_in, col_src))

    # 2. 安全校验：clean 模式要求目标列数据行为空；merge 模式读现状以便只改本次命中的行
    if side_by_side:
        vals = sheet_values('%s2:%s%d' % (col_in, col_src, n_rows))
    else:
        left = sheet_values('%s2:%s%d' % (col_in, col_in, n_rows))
        right = sheet_values('%s2:%s%d' % (col_src, col_src, n_rows))
        n_body = max(len(left), len(right))
        vals = []
        for i in range(n_body):
            a = left[i][0] if i < len(left) and left[i] else ''
            b = right[i][0] if i < len(right) and right[i] else ''
            vals.append([a, b])
    if args.merge:
        existing = {i + 2: (r[0] or '') for i, r in enumerate(vals)}
        existing_m = {i + 2: (r[1] if len(r) > 1 else '') or '' for i, r in enumerate(vals)}
        pre_filled = sum(1 for v in existing.values() if v)
        print('[i] merge mode: %s 列已有 %d 行内容，本次只重写新匹配的行' % (col_in, pre_filled))
    else:
        dirty = [i + 2 for i, r in enumerate(vals) if any(c not in (None, '') for c in r)]
        if dirty:
            sys.exit('[x] 目标列 %s:%s 已有内容(行 %s...)，中止；增量刷新请加 --merge，或换 --cols，或人工清理' % (col_in, col_src, dirty[:5]))

    # 3. 读功能层级 A:F
    rng = '%s!A1:F%d' % (args.sheet_id, n_rows)
    rr = http_json('GET', '%s/sheets/v2/spreadsheets/%s/values/%s?valueRenderOption=ToString'
                   % (BASE, args.spreadsheet, urllib.request.quote(rng, safe='')), headers=hh)
    rev0 = rr['data']['valueRange']['revision']
    grid = rr['data']['valueRange']['values']
    idx = []
    for i, r in enumerate(grid):
        if i == 0:
            continue  # 表头
        e = (r[4] if len(r) > 4 else '') or ''
        f = (r[5] if len(r) > 5 else '') or ''
        idx.append((i + 1, e, f))

    # 4. 解析本地用例（按 --filter 过滤文件名）
    all_files = sorted(glob.glob(os.path.join(args.md_dir, '*-合规演示用例.md')))
    files = [p for p in all_files if fnmatch.fnmatch(os.path.basename(p), args.filter)]
    if not files:
        sys.exit('[x] --filter %s 无匹配文件（目录内共 %d 个用例文件）' % (args.filter, len(all_files)))
    print('[i] filter=%s -> %d/%d files: %s' % (args.filter, len(files), len(all_files),
                                                ', '.join(os.path.basename(p) for p in files)))
    by_seq, bads = {}, []
    for p in files:
        rows, bad = parse_md(p)
        bads += bad
        for r in rows:
            by_seq.setdefault(r['seq'], []).append(r)
    print('[i] files=%d seqs=%d cases=%d bad_lines=%d' % (len(files), len(by_seq), sum(len(v) for v in by_seq.values()), len(bads)))

    # 5. 匹配：逐个标题词回退（长词优先），词不中换下一个；命中冲突只保留首个并记录
    matched, unmatched, ambiguous, collisions = {}, [], [], []
    row_file, hits = {}, []
    for seq in sorted(by_seq):
        group = by_seq[seq]
        cores = []
        for g in group:
            cores += tokens(g['title'])
        cores = [c for c in sorted(set(cores), key=len, reverse=True) if len(c) >= 4]
        off = seq + 1
        hit, how, amb_note = None, '', None
        for core in cores:
            cands = [rn for rn, e, f in idx if core in norm(e + f)]
            if len(cands) == 1:
                hit, how = cands[0], 'title'
                break
            if not cands:
                continue
            if off in cands:
                hit, how = off, 'title+offset'
                break
            near = [c for c in cands if seq - 2 <= c <= seq + 10]
            if len(near) == 1:
                hit, how = near[0], 'title+near'
                break
            # 泛化词（候选>4 且无近邻收窄能力）不用于定位，防跨区块错配
            if len(near) > 4:
                if amb_note is None:
                    amb_note = (core, cands[:8])
                continue
            if len(near) > 1 and min(abs(c - off) for c in near) <= 2:
                hit, how = min(near, key=lambda c: abs(c - off)), 'title+near-multi'
                break
            if amb_note is None:
                amb_note = (core, cands[:8])
        if not hit:
            if amb_note:
                ambiguous.append((seq, amb_note[0], amb_note[1], sorted(set(g['file'] for g in group))))
            else:
                unmatched.append((seq, cores[:2], sorted(set(g['file'] for g in group))))
            continue
        if hit in matched:
            collisions.append((seq, hit, matched[hit][1], sorted(set(g['file'] for g in group))))
            continue
        # 合并同序号多行：每行带界面名前缀
        parts = []
        for g in group:
            t = g['title'] or ('序号%d' % seq)
            body = g['input'] or ''
            parts.append('【%s】%s' % (t, body))
        text = '\n———\n'.join(parts)
        if len(text) > CELL_CAP:
            text = text[:CELL_CAP - 20] + '\n…(截断，全文见用例md)'
        srcs = '；'.join(sorted(set(g['file'] for g in group)))
        matched[hit] = (text, srcs + '（%s）' % how)
        row_file[hit] = group[0]['file']
        hits.append((seq, hit, group[0]['file'], how))

    # 5c. 文件级偏移学习：同一文件 ≥2 行确定性命中（title*/disambig）共享同一 (row-seq) 偏移时，
    #     将该偏移外推到该文件其余未匹配序号（目标行须空闲且 F 列非空，防越界）

    # 5b. 确定性消歧：同标题词多候选且候选数=同序号用例数时，按行号升序各得一行
    if ambiguous:
        ambmap = {}
        for seq, core, cands, fs in ambiguous:
            ambmap.setdefault(core, []).append((seq, cands))
        for core, items in ambmap.items():
            if len(items) >= 2 and len(set(len(c) for _, c in items)) == 1 and len(items[0][1]) == len(items):
                pool = sorted(set(row for _, c in items for row in c))
                free = [c for c in pool if c not in matched]
                if len(pool) == len(items) and len(free) == len(pool):
                    items.sort(key=lambda x: x[0])
                    for k, (seq, cands) in enumerate(items):
                        group = by_seq[seq]
                        parts = ['【%s】%s' % (g['title'] or ('序号%d' % seq), g['input'] or '') for g in group]
                        text = '\n———\n'.join(parts)
                        if len(text) > CELL_CAP:
                            text = text[:CELL_CAP - 20] + '\n…(截断，全文见用例md)'
                        srcs = '；'.join(sorted(set(g['file'] for g in group)))
                        matched[cands[k]] = (text, srcs + '（disambig-ordered）')
                        row_file[cands[k]] = group[0]['file']
                        hits.append((seq, cands[k], group[0]['file'], 'disambig-ordered'))
                    ambiguous = [a for a in ambiguous if a[1] != core]

    # 5d. 文件级偏移学习：同一文件 ≥2 行确定性命中（title*/disambig）共享同一 (row-seq) 偏移时，
    #     将该偏移外推到该文件其余未匹配序号（目标行须空闲且 F 列非空，防越界）
    file_off_votes = {}
    for (seq, rn, fname, how) in hits:
        if how.startswith('title') or how == 'disambig-ordered':
            file_off_votes.setdefault(fname, {})
            file_off_votes[fname][rn - seq] = file_off_votes[fname].get(rn - seq, 0) + 1
    applied = 0
    still_unmatched = []
    for seq, cores, fs in unmatched:
        fname = fs[0] if len(set(fs)) == 1 else None
        votes = file_off_votes.get(fname, {})
        solid = [o for o, n in votes.items() if n >= 2]
        if len(solid) == 1 and fname:
            rn = seq + solid[0]
            if 2 <= rn <= n_rows and rn not in matched and grid[rn - 1][5]:
                group = by_seq[seq]
                parts = ['【%s】%s' % (g['title'] or ('序号%d' % seq), g['input'] or '') for g in group]
                text = '\n———\n'.join(parts)
                if len(text) > CELL_CAP:
                    text = text[:CELL_CAP - 20] + '\n…(截断，全文见用例md)'
                srcs = '；'.join(sorted(set(g['file'] for g in group)))
                matched[rn] = (text, srcs + '（file-offset%+d）' % solid[0])
                hits.append((seq, rn, fname, 'file-offset'))
                applied += 1
                continue
        still_unmatched.append((seq, cores, fs))
    unmatched = still_unmatched

    print('[i] matched_rows=%d unmatched_seqs=%d ambiguous=%d collisions=%d file_offset_applied=%d' % (len(matched), len(unmatched), len(ambiguous), len(collisions), applied))

    # 6. 写入。两列紧挨着时一次写入；中间插过列则分列写，避免盖住中间列。
    upd_rev = []

    def put_cells(a1, values):
        wr = http_json('PUT', '%s/sheets/v2/spreadsheets/%s/values' % (BASE, args.spreadsheet),
                       {'valueRange': {'range': '%s!%s' % (args.sheet_id, a1), 'values': values}}, headers=hh)
        if wr.get('code') != 0:
            sys.exit('[x] 写入失败 %s: %s' % (a1, wr))
        upd_rev.append(wr.get('data', {}).get('revision'))

    def put_pair(row_from, row_to, pairs):
        if side_by_side:
            put_cells('%s%d:%s%d' % (col_in, row_from, col_src, row_to), pairs)
            return
        put_cells('%s%d:%s%d' % (col_in, row_from, col_in, row_to), [[pair[0]] for pair in pairs])
        put_cells('%s%d:%s%d' % (col_src, row_from, col_src, row_to), [[pair[1]] for pair in pairs])

    if args.apply:
        head_txt = '合规用例·输入与条件（自动同步 %s）' % date.today().isoformat()
        if args.merge:
            if not known_header.startswith(IN_HEADER_PREFIX):
                put_pair(1, 1, [[head_txt, '用例来源文件']])
            # merge：只写本次命中的行；文本与来源都与现状一致才跳过（幂等刷新），
            # 来源列格式为「文件名（匹配方式）」，比对时取全角括号前的文件部分
            mfile = lambda v: ((v or '').split('（')[0]).strip()
            targets = sorted(rn for rn in matched
                             if existing.get(rn) != matched[rn][0] or mfile(existing_m.get(rn)) != mfile(matched[rn][1]))
            skipped_other = sorted(rn for rn in matched if rn not in set(targets))
            seq_of_row = {r: s for (s, r, _fn, _h) in hits}
            for rn in skipped_other:
                if mfile(existing_m.get(rn)) != mfile(matched[rn][1]):  # 只有跨文件抢占才算冲突；同文件幂等跳过不记
                    collisions.append((seq_of_row.get(rn, '?'), rn, existing_m.get(rn) or '(%s列空)' % col_src,
                                       os.path.basename(matched[rn][1] or '?')))
            if targets:
                print('[i] merge 将写 %d 行，防误覆盖跳过 %d 行' % (len(targets), len(skipped_other)))
        else:
            put_pair(1, 1, [[head_txt, '用例来源文件']])
            # clean：整表两列重写（未匹配行写空=清空，保持列内无脏数据）
            targets = list(range(2, n_rows + 1))
        for run in row_runs(targets, 150):
            block = [list(matched.get(rn, ('', ''))) for rn in run]
            put_pair(run[0], run[-1], block)
        print('[i] written rows=%d, revisions=%s' % (len(targets), upd_rev))

    # 7. 报告
    rep = args.report or os.path.join(args.md_dir, '展示系统-用例同步报告-%s.md' % date.today().isoformat())
    if args.filter != '*':
        rep = args.report or os.path.join(args.md_dir, '展示系统-用例同步报告-%s-%s.md' % (args.filter.rstrip('*-').rstrip('-') or 'filter', date.today().isoformat()))
    with io.open(rep, 'w', encoding='utf-8') as f:
        f.write('# 展示系统合规用例 → 飞书表同步报告（%s）\n\n' % date.today().isoformat())
        f.write('- 模式：%s，文件过滤：`%s`（本次 %d 个文件）\n' % ('merge 增量刷新（只动本次命中的行）' if args.merge else 'clean 全列', args.filter, len(files)))
        f.write('- 目标：`%s` 页签 `%s`，列 `%s`(输入与条件) / `%s`(来源)；本次未动过滤范围外的任何文件/行\n' % (args.spreadsheet, args.sheet_id, col_in, col_src))
        f.write('- 本地用例：files=%d，序号数=%d，用例行=%d，坏行=%d\n' % (len(files), len(by_seq), sum(len(v) for v in by_seq.values()), len(bads)))
        f.write('- 匹配写入行=%d；未匹配序号=%d；歧义=%d；冲突跳过=%d\n' % (len(matched), len(unmatched), len(ambiguous), len(collisions)))
        f.write('- revision：%s → %s（apply=%s）\n\n' % (rev0, upd_rev[-1] if upd_rev else '-', args.apply))
        if unmatched:
            f.write('## 未匹配序号（人工核对）\n\n| 序号 | 标题词 | 来源 |\n|---|---|---|\n')
            for seq, cores, fs in unmatched:
                f.write('| %d | %s | %s |\n' % (seq, ' / '.join(cores), '；'.join(fs)))
        if ambiguous:
            f.write('\n## 歧义（多处标题命中，未写）\n\n| 序号 | 标题词 | 候选行 | 来源 |\n|---|---|---|---|\n')
            for seq, core, cands, fs in ambiguous:
                f.write('| %d | %s | %s | %s |\n' % (seq, core, ','.join(map(str, cands)), '；'.join(fs)))
        if collisions:
            f.write('\n## 冲突跳过（目标行已被其他序号写入）\n\n| 序号 | 目标行 | 先占来源 | 本序号来源 |\n|---|---|---|---|\n')
            for seq, hit, prior, fs in collisions:
                f.write('| %s | %s | %s | %s |\n' % (seq, hit, prior, '；'.join(fs) if isinstance(fs, (list, tuple)) else fs))
        if bads:
            f.write('\n## 解析坏行（列数不符，跳过）\n\n')
            for b in bads[:20]:
                f.write('- `%s` %s\n' % (b['file'], b['line'][:90]))
        f.write('\n## 匹配映射附录（Sheet行 ← 用例序号）\n\n| Sheet行 | 用例序号 | 来源 | 匹配方式 |\n|---|---|---|---|\n')
        hit_map = {(s, r): (fn, h) for (s, r, fn, h) in hits}
        for rn in sorted(matched):
            seq_hit = [(s, r) for (s, r) in hit_map if r == rn]
            if seq_hit:
                s, _ = seq_hit[0]
                fn, h = hit_map[(s, rn)]
                f.write('| %d | %d | %s | %s |\n' % (rn, s, fn, h))
    print('[i] report -> %s' % rep)


if __name__ == '__main__':
    main()
