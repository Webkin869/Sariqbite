from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.catalog.models import Branch, Category, Product, ProductOption


class Command(BaseCommand):
    help = "Seed demo data for SariqBite"

    def handle(self, *args, **options):
        categories = [
            ("Burgerlar", "burgerlar", "Juicy burgerlar"),
            ("Lavashlar", "lavashlar", "Turli lavashlar"),
            ("Pitsalar", "pitsalar", "Issiq pitsalar"),
            ("Ichimliklar", "ichimliklar", "Sovuq ichimliklar"),
        ]
        for idx, (name, slug, description) in enumerate(categories, start=1):
            Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "description": description, "sort_order": idx},
            )

        branches = [
            ("Yunusobod filial", "yunusobod", "Yunusobod, Tashkent", 41.3662, 69.2880),
            ("Chilonzor filial", "chilonzor", "Chilonzor, Tashkent", 41.2756, 69.2034),
        ]
        for name, slug, address, lat, lng in branches:
            Branch.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "address": address, "latitude": lat, "longitude": lng, "is_active": True},
            )

        product_specs = [
            ("burgerlar", "Golden Smash Burger", "golden-smash-burger", Decimal("38000"), True, 14, 1),
            ("burgerlar", "Double Cheddar Burger", "double-cheddar-burger", Decimal("47000"), True, 16, 0),
            ("lavashlar", "Chicken Lavash", "chicken-lavash", Decimal("32000"), True, 12, 1),
            ("lavashlar", "Spicy Beef Lavash", "spicy-beef-lavash", Decimal("36000"), False, 13, 3),
            ("pitsalar", "Pepperoni Pizza", "pepperoni-pizza", Decimal("76000"), True, 20, 0),
            ("pitsalar", "BBQ Chicken Pizza", "bbq-chicken-pizza", Decimal("82000"), False, 22, 1),
            ("ichimliklar", "Cola 1L", "cola-1l", Decimal("12000"), False, 2, 0),
            ("ichimliklar", "Ice Tea", "ice-tea", Decimal("10000"), False, 2, 0),
        ]

        option_map = {
            "golden-smash-burger": [("Extra cheese", Decimal("5000")), ("Jalapeno", Decimal("3000"))],
            "double-cheddar-burger": [("Extra cheddar", Decimal("6000")), ("Bacon", Decimal("9000"))],
            "chicken-lavash": [("Big size", Decimal("7000")), ("Extra sauce", Decimal("2000"))],
            "pepperoni-pizza": [("Medium", Decimal("0")), ("Large", Decimal("18000"))],
        }

        for category_slug, name, slug, price, featured, prep_minutes, spice in product_specs:
            product, _ = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": Category.objects.get(slug=category_slug),
                    "name": name,
                    "description": f"{name} uchun demo tavsif.",
                    "price": price,
                    "is_featured": featured,
                    "prep_minutes": prep_minutes,
                    "spice_level": spice,
                    "is_active": True,
                    "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1000&q=80",
                },
            )
            ProductOption.objects.filter(product=product).delete()
            for opt_name, extra_price in option_map.get(slug, []):
                ProductOption.objects.create(product=product, name=opt_name, extra_price=extra_price)

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
