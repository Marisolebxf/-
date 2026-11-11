import io
import json
from pathlib import Path
import tempfile
import unittest

from t02_m02_batch import chunks, save, digest, validate_resume, verify_expected, check_plan


class BatchSafety(unittest.TestCase):
    def test_chunk_boundary_preserves_pairs(self):
        rows = list(chunks(io.StringIO('\n'.join(json.dumps({'n': n}) for n in range(205))), 100))
        self.assertEqual([len(c) for c in rows], [100, 100, 5])
        self.assertEqual([x['n'] for c in rows for x in c], list(range(205)))

    def test_resume_rejects_foreign_or_resized_plan(self):
        m = dict(sha256='a', batch='b'); s = dict(m, chunk_size=100)
        validate_resume(s, m, 100)
        for changed in [dict(m, sha256='c'), dict(m, batch='c')]:
            with self.assertRaises(ValueError): validate_resume(s, changed, 100)
        with self.assertRaises(ValueError): validate_resume(s, m, 50)

    def test_readback_rejects_partial_write_wrong_weight_and_properties(self):
        e = dict(src='a', dst='b', weight=3, props={'batch': 'x'})
        verify_expected([e], {('a', 'b'): (3, {'batch': 'x'})})
        for result in [{}, {('a', 'b'): (4, {'batch': 'x'})}, {('a', 'b'): (3, {'batch': 'y'})}]:
            with self.assertRaises(RuntimeError): verify_expected([e], result)

    def test_plan_tampering_detected(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as d:
            p = Path(d); data = p / 'edges.jsonl'; data.write_text('{}\n')
            save(p / 'manifest.json', dict(space='demo_gkx_chain',
                 mapping='M02-canonical-all-years-sum-paper-v1', sha256=digest(data)))
            check_plan(p)
            data.write_text('{"changed":true}\n')
            with self.assertRaises(ValueError): check_plan(p)


if __name__ == '__main__': unittest.main()
