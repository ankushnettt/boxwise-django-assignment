from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from .packing import fits_in_box


class Product(models.Model):
    name = models.CharField(max_length=200)
    length = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    width = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    height = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    weight = models.DecimalField(
        max_digits=8, decimal_places=3, validators=[MinValueValidator(Decimal("0.001"))]
    )

    def __str__(self):
        return self.name


class Box(models.Model):
    name = models.CharField(max_length=200)
    length = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    width = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    height = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    max_weight = models.DecimalField(
        max_digits=8, decimal_places=3, validators=[MinValueValidator(Decimal("0.001"))]
    )
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_weight(self):
        total = Decimal("0")
        for item in self.items.select_related("product"):
            total += item.product.weight * item.quantity
        return total

    def recommend_box(self):
        items = list(self.items.select_related("product"))
        if not items:
            return None  # rule 1: order must contain products

        total_weight = self.get_total_weight()

        candidates = Box.objects.filter(max_weight__gte=total_weight).order_by(
            "cost", "id"
        )
        for box in candidates:
            if all(fits_in_box(item.product, box) for item in items):
                return box  # cheapest box that passes both checks
        return None  # rule 5: nothing fits

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
