from django.urls import path
from . import api_views

urlpatterns = [
    path("categories/", api_views.categories_api),
    path("products/", api_views.products_api),
    path("products/<slug:slug>/", api_views.product_detail_api),
    path("delivery-quote/", api_views.delivery_quote_api),
    path("orders/create/", api_views.create_order_api),
    path("orders/<int:order_id>/status/", api_views.order_status_api),
]
