from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image_url = models.URLField(blank=True)
    prep_minutes = models.PositiveIntegerField(default=20)
    spice_level = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=120)
    extra_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"
