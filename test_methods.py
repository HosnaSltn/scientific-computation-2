import unittest

from neville_aitken import neville_aitken, neville_table
from simpson_rule import composite_simpson, simpson_panel


class NevilleTests(unittest.TestCase):
    def test_reconstructs_a_polynomial_on_unsorted_nodes(self):
        self.assertAlmostEqual(neville_aitken([3, 0, 2, 1], [10, 1, 5, 2], 1.5), 3.25)

    def test_returns_table_by_degree(self):
        table = neville_table([0, 1, 2, 3], [1, 2, 5, 10], 1.5)
        self.assertEqual(table, [[1, 2, 5, 10], [2.5, 3.5, 2.5], [3.25, 3.25], [3.25]])

    def test_interpolates_a_sample_and_supports_one_node(self):
        self.assertEqual(neville_aitken([0, 1, 2], [2, 3, 9], 1), 3)
        self.assertEqual(neville_aitken([5], [-1], 9), -1)

    def test_rejects_duplicate_nodes_and_unpaired_values(self):
        with self.assertRaisesRegex(ValueError, "distinct"):
            neville_aitken([0, 0], [1, 2], 0.5)
        with self.assertRaisesRegex(ValueError, "same nonzero number"):
            neville_aitken([0, 1], [1], 0.5)

    def test_rejects_a_nonfinite_evaluation_point(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            neville_aitken([0], [4], float("inf"))


class SimpsonTests(unittest.TestCase):
    def test_integrates_a_sampled_cubic_in_both_directions(self):
        x = [0, 1, 2, 3, 4]
        y = [value ** 3 for value in x]
        self.assertAlmostEqual(composite_simpson(x, y), 64)
        self.assertAlmostEqual(composite_simpson(x[::-1], y[::-1]), -64)

    def test_panel_uses_three_adjacent_samples(self):
        self.assertAlmostEqual(simpson_panel([0, 1, 2, 3, 4], [0, 1, 8, 27, 64], 2), 60)
        self.assertAlmostEqual(simpson_panel([0, 2, 3, 4], [0, 4, 9, 16], 1), 56 / 3)

    def test_rejects_an_odd_number_of_intervals(self):
        with self.assertRaisesRegex(ValueError, "even number"):
            composite_simpson([0, 1, 2, 3], [0, 1, 4, 9])

    def test_rejects_nonuniform_samples(self):
        with self.assertRaisesRegex(ValueError, "equally spaced"):
            composite_simpson([0, 1, 3], [0, 1, 9])

    def test_rejects_invalid_panel_indices(self):
        for index in (-1, 1):
            with self.subTest(index=index), self.assertRaisesRegex(ValueError, "panel index"):
                simpson_panel([0, 1, 2], [0, 1, 4], index)
