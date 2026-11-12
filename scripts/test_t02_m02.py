import unittest
from decimal import Decimal
from t02_m02 import aggregate, insert_query, source_sql


def row(year, count, strength=Decimal('0.9')):
    return dict(institution_id='ins_a', collaborator_institution_id='ins_b',
                statistics_year=year, co_paper_count=count, collaboration_strength=strength)


class AggregationSafety(unittest.TestCase):
    def test_years_sum_absolute_counts_not_relative_strength(self):
        e = aggregate([row(2015, 7), row(2025, 13, Decimal('0.1'))], 'comply-20261111-t02')
        self.assertEqual(e['weight'], 20)
        self.assertEqual(e['props']['year_count'], 2)
        self.assertEqual(e['props']['first_year'], 2015)
        self.assertEqual(e['props']['latest_year'], 2025)
        self.assertEqual(e['src'], 'inst:ins_a')
        self.assertIn('IF NOT EXISTS', insert_query(e))

    def test_duplicate_year_rejected(self):
        with self.assertRaises(ValueError):
            aggregate([row(2025, 1), row(2025, 2)], 'comply-x-t02')

    def test_null_count_rejected_null_strength_preserved(self):
        with self.assertRaises(ValueError): aggregate([row(2025, None)], 'comply-x-t02')
        self.assertIsNone(aggregate([row(2025, 1, None)], 'comply-x-t02')['props']['strength_by_year']['2025'])

    def test_reverse_rejected(self):
        r = row(2025, 1); r['institution_id'], r['collaborator_institution_id'] = 'z', 'a'
        with self.assertRaises(ValueError): aggregate([r], 'comply-x-t02')

    def test_limit_applies_to_pairs_before_year_join(self):
        sql = source_sql(100)
        self.assertEqual(sql.count('LIMIT'), 1)
        self.assertLess(sql.index('LIMIT'), sql.index('LEFT JOIN'))


if __name__ == '__main__': unittest.main()
