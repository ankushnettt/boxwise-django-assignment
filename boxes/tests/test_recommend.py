from decimal import Decimal
from django.test import TestCase
from boxes.models import Product, Box, Order, OrderItem


class RecommendBoxTests(TestCase):
    def setUp(self):
        # Created out of cost order on purpose, to prove we sort by cost, not by id
        self.large = Box.objects.create(
            name="Large",
            length=Decimal("50"),
            width=Decimal("40"),
            height=Decimal("30"),
            max_weight=Decimal("10"),
            cost=Decimal("60"),
        )
        self.small = Box.objects.create(
            name="Small",
            length=Decimal("35"),
            width=Decimal("25"),
            height=Decimal("10"),
            max_weight=Decimal("2"),
            cost=Decimal("20"),
        )
        self.medium = Box.objects.create(
            name="Medium",
            length=Decimal("40"),
            width=Decimal("30"),
            height=Decimal("20"),
            max_weight=Decimal("5"),
            cost=Decimal("35"),
        )
        self.laptop = self.make_product("Laptop", "30", "20", "5", "1.5")
        self.mouse = self.make_product("Mouse", "10", "5", "3", "0.2")

    def make_product(self, name, l, w, h, weight):
        return Product.objects.create(
            name=name,
            length=Decimal(l),
            width=Decimal(w),
            height=Decimal(h),
            weight=Decimal(weight),
        )

    def make_order(self, *pairs):
        order = Order.objects.create()
        for product, qty in pairs:
            OrderItem.objects.create(order=order, product=product, quantity=qty)
        return order

    def test_cheapest_suitable_box(self):
        # weight 1.9 <= 2 and both products fit in Small, which is the cheapest
        order = self.make_order((self.laptop, 1), (self.mouse, 2))
        self.assertEqual(order.recommend_box(), self.small)

    def test_weight_rules_out_cheaper_box(self):
        # 2 laptops = 3.0 kg: Small (max 2) is rejected, Medium (max 5) is next cheapest
        order = self.make_order((self.laptop, 2))
        self.assertEqual(order.recommend_box(), self.medium)

    def test_dimensions_rule_out_cheaper_boxes(self):
        # 45 x 5 x 5 is longer than Small (35) and Medium (40), so only Large works
        pole = self.make_product("Pole", "45", "5", "5", "0.5")
        order = self.make_order((pole, 1))
        self.assertEqual(order.recommend_box(), self.large)

    def test_no_box_fits(self):
        huge = self.make_product("Huge", "60", "5", "5", "0.5")
        order = self.make_order((huge, 1))
        self.assertIsNone(order.recommend_box())

    def test_empty_order(self):
        self.assertIsNone(Order.objects.create().recommend_box())

    def test_no_boxes_exist(self):
        Box.objects.all().delete()
        order = self.make_order((self.mouse, 1))
        self.assertIsNone(order.recommend_box())
