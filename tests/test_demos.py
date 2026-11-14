"""Behavioral checks for feasibility, optimality and train-only prediction."""
from pathlib import Path
from collections import Counter
import itertools
import sys
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'projects/doctor-hospital-matching'))
sys.path.insert(0, str(ROOT / 'projects/single-cell-perturbation'))
import assignment as a
from demo import make_synthetic
from baseline_pca_ridge import fit_predict, mrrmse


class MatchingTests(unittest.TestCase):
    def test_example_capacity_and_optimum(self):
        result = a.solve_hungarian(a.preferences, a.capacities)
        counts = Counter(v['hospital'] for v in result.values())
        self.assertEqual(set(result), set(a.preferences))
        self.assertTrue(all(counts[h] <= c for h, c in a.capacities.items()))
        metrics = a.evaluate_assignment(list(a.preferences), result, a.preferences)
        self.assertEqual(metrics['total_cost'], 30)

    def test_small_instances_against_exhaustive_search(self):
        rng = np.random.default_rng(27)
        for n, m in [(1, 3), (2, 3), (3, 3), (3, 5), (4, 5)]:
            for _ in range(12):
                cost = rng.integers(-3, 8, (n, m)).tolist()
                solution = a.hungarian_algorithm(cost)
                actual = sum(cost[i][j] for i, j in enumerate(solution))
                expected = min(sum(cost[i][j] for i, j in enumerate(p))
                               for p in itertools.permutations(range(m), n))
                self.assertEqual(len(set(solution)), n)
                self.assertEqual(actual, expected)

    def test_insufficient_capacity_rejected(self):
        with self.assertRaises(ValueError):
            a.solve_hungarian({'D1': ['H1'], 'D2': ['H1']}, {'H1': 1})

    def test_duplicate_preference_rejected(self):
        with self.assertRaises(ValueError):
            a.solve_hungarian({'D1': ['H1', 'H1']}, {'H1': 1, 'H2': 1})


class PredictionTests(unittest.TestCase):
    def test_metric_is_mean_of_row_rmse(self):
        self.assertAlmostEqual(mrrmse([[0, 0], [0, 0]], [[3, 4], [0, 0]]),
                               (12.5 ** 0.5) / 2)

    def test_unknown_category_predicts_without_fitting_on_validation(self):
        x, y, xv, _ = make_synthetic()
        xv = xv.copy()
        xv['sm_name'] = 'unseen_drug'
        pred = fit_predict(x, y, xv, n_components=12, alpha=0.1)
        self.assertEqual(pred.shape, (len(xv), y.shape[1]))
        self.assertTrue(np.isfinite(pred.to_numpy()).all())
        self.assertTrue(pred.columns.equals(y.columns))
        self.assertTrue(pred.index.equals(xv.index))


if __name__ == '__main__':
    unittest.main()
