import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from validate import validate


class CertificateTests(unittest.TestCase):
    def check_file(self, certificate):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "factors.txt"
            path.write_text("4 2\nFACTORS\n2 3\n3 1\nCERTIFICATE\n" + certificate)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                validate(path)
            return output.getvalue()

    def test_rejects_infeasible_certificate(self):
        with self.assertRaises(ValueError):
            self.check_file("2 0\n3 0\n")

    def test_accepts_feasible_certificate(self):
        self.assertIn("upper bound: 4", self.check_file("2 1\n3 1\n"))

    def test_missing_certificate_does_not_claim_zero_upper_bound(self):
        self.assertNotIn("upper bound:", self.check_file(""))

    def test_rejects_negative_coefficient(self):
        with self.assertRaises(ValueError):
            self.check_file("2 -1\n3 1\n")

    def test_rejects_constraint_rounded_to_one_by_decimal_context(self):
        with self.assertRaises(ValueError):
            self.check_file("2 0.9999999999999999999999999999999999999999\n3 1\n")

    def test_rejects_nonfinite_coefficients(self):
        for value in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.check_file(f"2 {value}\n3 1\n")

    def test_rejects_duplicate_prime(self):
        with self.assertRaises(ValueError):
            self.check_file("2 1\n2 1\n3 1\n")

    def test_rejects_composite_index(self):
        with self.assertRaises(ValueError):
            self.check_file("2 1\n3 1\n4 1\n")


if __name__ == "__main__":
    unittest.main()
