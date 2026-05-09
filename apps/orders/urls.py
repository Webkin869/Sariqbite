from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/", views.cart_add, name="cart_add"),
    path("cart/<str:key>/change/", views.cart_change, name="cart_change"),
    path("checkout/", views.checkout, name="checkout"),
    path("quote/", views.delivery_quote_view, name="delivery_quote"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
]
