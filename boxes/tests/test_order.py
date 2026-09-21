from decimal import Decimal
from django.test import TestCase
from boxes.models import Product, Order, OrderItem


class OrderTotalWeightTests(TestCase):
    def setUp(self):
        self.laptop = Product.objects.create(
            name="Laptop",
            length=Decimal("30"),
            width=Decimal("20"),
            height=Decimal("5"),
            weight=Decimal("1.5"),
        )
        self.mouse = Product.objects.create(
            name="Mouse",
            length=Decimal("10"),
            width=Decimal("5"),
            height=Decimal("3"),
            weight=Decimal("0.2"),
        )

    def test_single_laptop(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.laptop, quantity=1)
        self.assertEqual(order.get_total_weight(), Decimal("1.5"))

    def test_two_laptops(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.laptop, quantity=2)
        self.assertEqual(order.get_total_weight(), Decimal("3.0"))

    def test_laptop_and_two_mice(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.laptop, quantity=1)
        OrderItem.objects.create(order=order, product=self.mouse, quantity=2)
        self.assertEqual(order.get_total_weight(), Decimal("1.9"))

    def test_empty_order(self):
        order = Order.objects.create()
        self.assertEqual(order.get_total_weight(), Decimal("0"))
