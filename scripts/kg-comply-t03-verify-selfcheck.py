"""Synthetic checks for the read-only T03 verifier; never connects to a graph."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

path = Path(__file__).with_name('kg-comply-t03-verify.py')
spec = importlib.util.spec_from_file_location('t03_verify', path)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
v.EXPECTED = dict.fromkeys(v.KINDS, 3)


class FakeReader:
    def __init__(self, rows):
        self.nodes = {kind:{row['id']:{'name':'existing name', 'props':json.dumps(
            {'batch':'T04', **({'institution_type_id':row['props']['institution_type_id']} if kind == 'research' else {})})}
                           for row in rows[kind]} for kind in ('person','research')}
        self.edge_rows = {kind:{(row['src'],row['dst'],0):{'weight':row['weight'],'props':v.canonical(row['props'])}
                               for row in rows[kind]} for kind in ('m01','m04')}
        self.bad_count = False

    def query(self, query):
        for label, statement in v.count_queries().items():
            if query == statement:
                if label in ('m01','m04'):
                    return [[3, 2 if self.bad_count and label == 'm01' else 3,0,0]]
                return [[94824 if label == 'm22_existing' else 3 if label in ('person','research') else 0]]
        raise AssertionError('Unexpected query')

    def vertices(self, tag, vids):
        return {vid:self.nodes[tag][vid] for vid in vids if vid in self.nodes[tag]}

    def edges(self, kind, rows):
        wanted = {(row['src'],row['dst'],0) for row in rows}
        return {key:copy.deepcopy(value) for key,value in self.edge_rows[kind].items() if key in wanted}


class Checks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        snapshot = self.root / 'snapshot'
        snapshot.mkdir()
        self.rows = {
            'person':[{'id':'person:'+str(i),'name':'source name','props':{'batch':v.BATCH}} for i in range(1,4)],
            'research':[{'id':'inst:'+str(i),'name':'source name','props':{'batch':v.BATCH,'institution_type_id':t}}
                        for i,t in enumerate(('education','facility','company'),1)],
            'm01':[{'src':'person:'+str(a),'dst':'person:'+str(b),'rank':0,'weight':1.25,
                    'props':{'batch':v.BATCH,'match_method':'coauthor'}} for a,b in ((1,2),(1,3),(2,3))],
            'm04':[{'src':'person:'+str(i),'dst':'inst:1','rank':0,'weight':0.0,
                    'props':{'batch':v.BATCH,'experience_type':2,'institution_type_id':'education',
                             'is_current':True,'stint_count':1,'source_experience_ids':['exp'+str(i)]}}
                   for i in range(1,4)],
        }
        files = {}
        for kind,rows in self.rows.items():
            path = snapshot / (kind+'.jsonl')
            path.write_text(''.join(v.canonical(row)+'\n' for row in rows),encoding='utf-8')
            files[kind] = {'rows':3,'sha256':v.sha256(path)}
        manifest = {'status':'complete','batch':v.BATCH,'space':v.SPACE,'files':files}
        v.write_json(snapshot/'manifest.json',manifest)
        full = {'status':'verified','stage':'full','space':v.SPACE,'batch':v.BATCH,
                'manifest_sha256':v.sha256(snapshot/'manifest.json'),
                'files':{kind:{'completed':True,'source_records':3,'snapshot_sha256':files[kind]['sha256']}
                         for kind in v.KINDS}}
        v.write_json(self.root/'full-result.json',full)
        self.reader = FakeReader(self.rows)

    def tearDown(self):
        self.temp.cleanup()

    def test_happy_path_preserves_existing_minimal_t04_props(self):
        result = v.verify(self.root,self.reader)
        self.assertEqual(result['status'],'passed')
        self.assertEqual(result['checks']['research_full_types']['checked_rows'],3)
        self.assertEqual(result['checks']['person_sample']['sample_indices'],[0,1,2])

    def test_research_type_mismatch_fails(self):
        self.reader.nodes['research']['inst:1']['props'] = '{"institution_type_id":"company"}'
        result = v.verify(self.root,self.reader)
        self.assertEqual(result['status'],'failed')
        self.assertEqual(result['checks']['research_full_types']['type_mismatch'],1)

    def test_edge_value_and_batch_count_mismatch_fail(self):
        self.reader.bad_count = True
        self.reader.edge_rows['m01'][('person:1','person:2',0)]['weight'] = 999
        result = v.verify(self.root,self.reader)
        self.assertEqual(result['status'],'failed')
        self.assertFalse(result['checks']['counts']['m01']['passed'])
        self.assertEqual(result['checks']['m01_sample']['failures']['weight_mismatch'],1)

    def test_tampered_snapshot_stops_before_graph(self):
        path = self.root/'snapshot/person.jsonl'
        path.write_text(path.read_text(encoding='utf-8')+'\n',encoding='utf-8')
        with self.assertRaises(v.VerificationError):
            v.verify(self.root,self.reader)
        result = json.loads((self.root/'verification.json').read_text(encoding='utf-8'))
        self.assertEqual(result['status'],'failed')
        self.assertFalse(result['checks'])

    def test_spread_sample_includes_first_middle_and_last(self):
        self.assertEqual(v.sample_indices(3),[0,1,2])
        values = v.sample_indices(2525789)
        self.assertEqual((values[0],values[-1],len(values)),(0,2525788,20))


if __name__ == '__main__':
    unittest.main(verbosity=2)
