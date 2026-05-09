from django.contrib import admin
from .models import Branch, Category, Product, ProductOption


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("sort_order", "name")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "address")


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "prep_minutes", "is_featured", "is_active")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductOptionInline]
