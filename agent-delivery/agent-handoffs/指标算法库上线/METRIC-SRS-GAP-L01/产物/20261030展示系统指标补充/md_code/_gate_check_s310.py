#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S3-10 批（科学技术全景补立项）8 件 11 项检查运行器
（沿用 S3-09 终跑口径：13 章节结构存在性为准；本批 PANO_008 为「不适用」档——
 功能位存档无 §二 6 小节正文，行数代理对不适用档豁免，先例：阶段0.5 不立项件。）
用法: python3 _gate_check_s310.py [--json /tmp/out.json]
"""
import os, re, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_DIR = os.path.join(BASE, '第三方库指标计算过程')
CODE_DIR = os.path.join(BASE, 'code')

IDS = ['PANO_001','PANO_002','PANO_003','PANO_004','PANO_005','PANO_006','PANO_007','PANO_008']

REQUIRED_SECTIONS = [
    "〇、数据支持度与四判定口径", "## 摘要", "## 一、需求定义概述",
    "## 三、数据支撑情况", "## 四、数据缺失情况", "## 参考文献",
]

def check_one(mid):
    errs, warns = [], []
    md_path = os.path.join(MD_DIR, f'M_SCIUI_{mid}.md')
    py = os.path.join(CODE_DIR, f'M_SCIUI_{mid}.py')
    out = os.path.join(CODE_DIR, f'M_SCIUI_{mid}_out.json')
    if not os.path.exists(md_path): return {'id': mid, 'errors': ['MD 不存在'], 'warns': []}
    text = open(md_path, encoding='utf-8').read()
    # ① 结构契约
    for marker in REQUIRED_SECTIONS:
        if marker not in text: errs.append(f'结构缺 {marker}')
    m = re.search(r'本件判定[：:]\s*\*{0,2}(完全直接支持|完全转换支持|部分支持|完全不支持|不适用)', text)
    if not m: errs.append('文首判档缺失')
    verdict = m.group(1) if m else ''
    na = verdict.startswith('不适用')
    # 完全不支持/不适用档 §二可简；其他档必须有 §二 ≥5 小节 + 复现结果小节
    if not na and verdict != '完全不支持':
        if '## 二、计算过程' not in text: errs.append('非豁免档缺 §二')
        else:
            body = re.search(r'## 二、计算过程([\s\S]*?)(?=\n## 三、)', text)
            subs = re.findall(r'### (2\.\d+)', body.group(1)) if body else []
            if len(subs) < 5: errs.append(f'§二 小节 {len(subs)}<5')
            if '_out.json' not in text: errs.append('复现产物引用缺失')
    # §一 1.1-1.6
    sec1 = re.search(r'## 一、需求定义概述([\s\S]*?)(?=\n## )', text)
    if sec1:
        for i in range(1, 7):
            if f'### 1.{i}' not in sec1.group(1): errs.append(f'§一 缺 1.{i}')
    # ② 禁演示库（demo_*/svc-fseed）
    for m2 in re.finditer(r'demo_(?!fallback|formula)[a-z0-9]+(?:_[a-z0-9]+)*表?', text):
        line_start = text.rfind('\n', 0, m2.start())+1
        line_end = text.find('\n', m2.end())
        ctx = text[line_start:line_end]
        if not re.search(r'禁|造数|演示|披露|陷阱|非真|mock|排除|不参与|虚构|登记|示例|样例|demo_\*|0 张命中|0 列命中|0 命中|扫描|扫 |会话态|Mock|ui_demo_only', ctx):
            errs.append(f'疑似引用 demo 表未披露: {m2.group(0)}'); break
    # ⑥ 判档枚举（MD vs out.json）
    if os.path.exists(out):
        d = json.load(open(out))
        sj = d.get('support_judgment'); sj = sj.get('verdict') if isinstance(sj, dict) else sj
        if sj and verdict and sj != verdict and not (na and sj.startswith('不适用')) and not sj.startswith('不适用（'):
            # 「不适用（…）」长形与「不适用」短形视为一致
            short = sj.split('（')[0]
            if short != verdict: errs.append(f'判档不一致 md={verdict} out={sj}')
        # ③ 基期三字段
        for k in ('base_years_used', 'base_years_missing', 'base_years_note'):
            if k not in d: errs.append(f'产物缺 {k}')
    else:
        errs.append('_out.json 缺失')
    if not os.path.exists(py): errs.append('py 缺失')
    # py 可运行 + 幂等
    if os.path.exists(py):
        import subprocess, hashlib
        p1 = hashlib.md5(open(out,'rb').read()).hexdigest() if os.path.exists(out) else ''
        r = subprocess.run(['python3', py], capture_output=True, text=True, timeout=120)
        if r.returncode != 0: errs.append(f'py 运行失败: {r.stderr.strip()[:80]}')
        p2 = hashlib.md5(open(out,'rb').read()).hexdigest() if os.path.exists(out) else ''
        if p1 and p1 != p2: errs.append('py 非幂等（重跑产物漂移）')
    # ⑦ 死引用
    for m3 in re.finditer(r'`([^`]*code/[A-Za-z0-9_]+\.(?:py|json))`', text):
        ref_path = m3.group(1)
        fname = ref_path.split('/')[-1]
        if os.path.exists(os.path.join(CODE_DIR, fname)): continue
        ws = '/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage'
        found = False
        if '/' in ref_path and '/code/' in ref_path:
            prefix = ref_path.split('/code/')[0]
            cand = os.path.join(ws, prefix, 'code', fname)
            found = os.path.exists(cand)
        if not found and ref_path.startswith('code/'):
            errs.append(f'死引用 {ref_path}')
    # 行数代理（不适用档豁免；warn 不阻断）
    n = text.count('\n')
    if not na and n < 400: warns.append(f'行数 {n}<400（金样板代理）')
    return {'id': mid, 'verdict': verdict, 'lines': n, 'errors': errs, 'warns': warns}

def main():
    results = [check_one(i) for i in IDS]
    fails = [r for r in results if r['errors']]
    print(f"S3-10 11 项检查（结构/禁demo/基期/判档一致/三件套/py幂等/死引用）：{len(results)-len(fails)}/{len(results)} 通过")
    for r in fails:
        print(f"[FAIL] {r['id']}:")
        for e in r['errors']: print('   ✗', e)
    w = [r for r in results if r.get('warns')]
    for r in w: print(f"[warn] {r['id']}: {r['warns'][0]}")
    if '--json' in sys.argv:
        out = sys.argv[sys.argv.index('--json')+1]
        json.dump(results, open(out, 'w'), ensure_ascii=False, indent=1)
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
