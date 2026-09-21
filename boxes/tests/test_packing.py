from decimal import Decimal
from types import SimpleNamespace
from django.test import SimpleTestCase
from boxes.packing import fits_in_box


def dims(l, w, h):
    return SimpleNamespace(length=Decimal(l), width=Decimal(w), height=Decimal(h))


class FitsInBoxTests(SimpleTestCase):
    def test_fits_directly(self):
        self.assertTrue(fits_in_box(dims("10", "8", "5"), dims("15", "10", "8")))

    def test_fits_only_when_rotated(self):
        self.assertTrue(fits_in_box(dims("10", "8", "5"), dims("8", "10", "15")))

    def test_exact_fit(self):
        self.assertTrue(fits_in_box(dims("10", "8", "5"), dims("10", "8", "5")))

    def test_too_long(self):
        self.assertFalse(fits_in_box(dims("20", "8", "5"), dims("15", "10", "8")))

    def test_one_dimension_too_big(self):
        self.assertFalse(fits_in_box(dims("10", "9", "9"), dims("15", "10", "8")))
