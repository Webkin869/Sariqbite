from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    return render(request, "catalog/home.html", {
        "categories": categories,
        "featured_products": featured_products,
    })


def menu(request):
    categories = Category.objects.all()
    category_slug = request.GET.get("category")
    products = Product.objects.filter(is_active=True).select_related("category")
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)
    return render(request, "catalog/menu.html", {
        "categories": categories,
        "products": products,
        "active_category": active_category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related("options", "category"), slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})
