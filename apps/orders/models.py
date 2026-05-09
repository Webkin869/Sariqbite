from django.db import models
from apps.catalog.models import Branch


class Order(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        COOKING = "cooking", "Cooking"
        ON_THE_WAY = "on_the_way", "On the way"
        DELIVERED = "delivered", "Delivered"
        CANCELED = "canceled", "Canceled"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        CLICK = "click", "Click"
        PAYME = "payme", "Payme"

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    note = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    distance_km = models.FloatField(default=0)
    eta_minutes = models.PositiveIntegerField(default=25)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    telegram_chat_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=140)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    options_text = models.CharField(max_length=255, blank=True)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
