import unittest
from t02_m02_full import partitions,read_source_shard
from t02_m02_audit import acyclic
from unittest.mock import patch


class FullCoverage(unittest.TestCase):
    def test_partitions_cover_each_source_once_including_tail(self):
        ids=[f'ins_{i:05d}' for i in range(1003)]
        result=partitions(ids,100)
        self.assertEqual([x for shard in result for x in shard],ids)
        self.assertEqual(len(result[-1]),3)
        self.assertTrue(all(a[-1]<b[0] for a,b in zip(result,result[1:])))

    def test_noncanonical_source_inventory_is_rejected(self):
        for ids in [['b','a'],['a','a']]:
            with self.assertRaises(ValueError):partitions(ids,100)

    def test_dag_rejects_cycle_and_self_loop(self):
        self.assertTrue(acyclic([('a','b'),('a','c'),('b','d'),('c','d')]))
        self.assertFalse(acyclic([('a','b'),('b','a')]))
        self.assertFalse(acyclic([('a','a')]))

    def test_timed_out_response_discarded_and_source_boundaries_split(self):
        calls=[]
        class Cursor:
            def execute(self,sql,params):
                calls.append(params);self.params=params
                if params==('a','b'):raise RuntimeError('Query timeout')
            def __iter__(self):return iter([{'source':self.params[0]}])
            def close(self):pass
        class Connection:
            def cursor(self):return Cursor()
        with patch('t02_m02_full.time.sleep'):
            rows=read_source_shard(Connection(),['a','b'])
        self.assertEqual(rows,[{'source':'a'},{'source':'b'}])
        self.assertEqual(calls,[('a','b'),('a','a'),('b','b')])


if __name__=='__main__':unittest.main()
