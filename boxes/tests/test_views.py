from decimal import Decimal
from django.test import TestCase
from boxes.models import Product, Box, Order, OrderItem


class RecommendBoxViewTests(TestCase):
    def setUp(self):
        self.box = Box.objects.create(
            name="Medium",
            length=Decimal("40"),
            width=Decimal("30"),
            height=Decimal("20"),
            max_weight=Decimal("5"),
            cost=Decimal("35"),
        )
        self.product = Product.objects.create(
            name="Laptop",
            length=Decimal("30"),
            width=Decimal("20"),
            height=Decimal("5"),
            weight=Decimal("1.5"),
        )

    def test_returns_recommended_box(self):
        order = Order.objects.create()
        OrderItem.objects.create(order=order, product=self.product, quantity=1)
        response = self.client.get(f"/api/orders/{order.pk}/recommend-box/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["order"], order.pk)
        self.assertEqual(data["recommended_box"]["name"], "Medium")
        self.assertEqual(Decimal(data["recommended_box"]["cost"]), Decimal("35"))

    def test_no_suitable_box(self):
        order = Order.objects.create()  # empty order
        response = self.client.get(f"/api/orders/{order.pk}/recommend-box/")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["recommended_box"])

    def test_order_not_found(self):
        response = self.client.get("/api/orders/9999/recommend-box/")
        self.assertEqual(response.status_code, 404)
