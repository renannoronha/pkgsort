import unittest

from src.sort_pkg import sort


class TestSortClassification(unittest.TestCase):
	def test_standard_when_neither_bulky_nor_heavy(self):
		self.assertEqual(sort(10, 10, 10, 1), "STANDARD")
		self.assertEqual(sort(149.9, 100, 5, 19.99), "STANDARD")
		self.assertEqual(sort("10", "10", "10", "0"), "STANDARD")

	def test_special_when_bulky_by_volume_threshold_exact(self):
		# 100 * 100 * 100 = 1_000_000 exactly (bulky), mass below 20
		self.assertEqual(sort(100, 100, 100, 19.9999), "SPECIAL")

	def test_special_when_bulky_by_dimension_threshold_exact(self):
		# Any single dimension >= 150 triggers bulky
		self.assertEqual(sort(150, 1, 1, 0), "SPECIAL")
		self.assertEqual(sort(1, 150, 1, 0), "SPECIAL")
		self.assertEqual(sort(1, 1, 150, 0), "SPECIAL")

	def test_special_when_heavy_threshold_exact(self):
		# mass >= 20 triggers heavy
		self.assertEqual(sort(1, 1, 1, 20), "SPECIAL")

	def test_rejected_when_bulky_and_heavy(self):
		# Bulky by dimension AND heavy by mass
		self.assertEqual(sort(150, 1, 1, 20), "REJECTED")
		# Bulky by volume AND heavy by mass
		self.assertEqual(sort(100, 100, 100, 25), "REJECTED")

	def test_volume_boundary_conditions(self):
		cases = [
			# just below threshold
			((100, 100, 99.9999, 0), "STANDARD"),
			((99.9999, 100, 100, 0), "STANDARD"),
			((100, 99.9999, 100, 0), "STANDARD"),
			# exactly at threshold
			((100, 100, 100, 0), "SPECIAL"),
			# above threshold
			((100, 100, 100.0001, 0), "SPECIAL"),
		]
		for (w, h, l, m), expected in cases:
			with self.subTest(w=w, h=h, l=l, m=m):
				self.assertEqual(sort(w, h, l, m), expected)

	def test_dimension_boundary_conditions(self):
		cases = [
			((149.9999, 1, 1, 0), "STANDARD"),
			((150, 1, 1, 0), "SPECIAL"),
			((150.0001, 1, 1, 0), "SPECIAL"),
		]
		for (w, h, l, m), expected in cases:
			with self.subTest(w=w):
				self.assertEqual(sort(w, h, l, m), expected)

	def test_mass_boundary_conditions(self):
		cases = [
			((1, 1, 1, 19.9999), "STANDARD"),
			((1, 1, 1, 20), "SPECIAL"),
			((1, 1, 1, 20.0001), "SPECIAL"),
		]
		for (w, h, l, m), expected in cases:
			with self.subTest(m=m):
				self.assertEqual(sort(w, h, l, m), expected)

	def test_numeric_strings_and_scientific_notation(self):
		# Accepts strings convertible to float
		# Below bulky threshold and not heavy
		self.assertEqual(sort("1e1", "1e1", "1e1", "1e0"), "STANDARD")
		self.assertEqual(sort("150", 0, 0, "0"), "SPECIAL")  # bulky by dimension
		self.assertEqual(sort("10", "10", "10", "2e1"), "SPECIAL")  # heavy by mass

	def test_invalid_inputs_raise(self):
		invalid_cases = [
			("abc", 1, 1, 1),  # width invalid
			(1, None, 1, 1),    # height invalid
			(1, 1, [], 1),      # length invalid
			(1, 1, 1, {}),      # mass invalid
			("", 1, 1, 1),     # empty string invalid
		]
		for args in invalid_cases:
			with self.subTest(args=args):
				with self.assertRaises((ValueError, TypeError)):
					sort(*args)

	def test_negative_and_zero_values(self):
		# Zero dimensions and mass -> not bulky/heavy
		self.assertEqual(sort(0, 0, 0, 0), "STANDARD")
		# Negative values aren't filtered by implementation
		self.assertEqual(sort(-1, -2, -3, -4), "STANDARD")
		# Negative mass but bulky dimensions -> still SPECIAL (bulky only)
		self.assertEqual(sort(200, 1, 1, -5), "SPECIAL")

	def test_infinities(self):
		inf = float("inf")
		# Infinite dimension -> bulky
		self.assertEqual(sort(inf, 1, 1, 0), "SPECIAL")
		# Infinite mass -> heavy
		self.assertEqual(sort(1, 1, 1, inf), "SPECIAL")
		# Both infinite -> rejected
		self.assertEqual(sort(inf, 1, 1, inf), "REJECTED")

	def test_nans(self):
		nan = float("nan")
		# NaN comparisons are false -> neither bulky nor heavy
		self.assertEqual(sort(nan, nan, nan, nan), "STANDARD")
		# Mixed NaN with normal values keeps comparisons false wherever NaN appears
		self.assertEqual(sort(nan, 1, 1, 0), "STANDARD")
		self.assertEqual(sort(1, nan, 1, 0), "STANDARD")
		self.assertEqual(sort(1, 1, nan, 0), "STANDARD")
		self.assertEqual(sort(1, 1, 1, nan), "STANDARD")

	def test_extremely_large_values_overflow_volume(self):
		# Very large values can overflow volume to inf -> bulky
		a = 1e154
		self.assertEqual(sort(a, a, a, 0), "SPECIAL")

	def test_boolean_inputs(self):
		# bools are valid floats (True->1.0, False->0.0)
		self.assertEqual(sort(True, False, True, False), "STANDARD")


if __name__ == "__main__":
	unittest.main(verbosity=2)

