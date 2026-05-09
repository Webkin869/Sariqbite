import json
from decimal import Decimal

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from apps.catalog.models import Product
from .cart import add_to_cart, cart_summary, clear_cart, remove_item, update_quantity
from .forms import CheckoutForm
from .models import Order, OrderItem
from .services import build_delivery_quote, quantize_money


def cart_detail(request):
    summary = cart_summary(request)
    quote = build_delivery_quote(distance_km=0)
    total = summary["subtotal"] + quote.delivery_fee
    return render(request, "orders/cart.html", {
        "cart": summary,
        "delivery_quote": quote,
        "grand_total": total,
    })


@require_POST
def cart_add(request):
    product = get_object_or_404(Product, id=request.POST.get("product_id"), is_active=True)
    option_ids = [int(item) for item in request.POST.getlist("option_ids") if str(item).isdigit()]
    quantity = int(request.POST.get("quantity", 1) or 1)
    add_to_cart(request, product, quantity=quantity, option_ids=option_ids)
    messages.success(request, f"{product.name} savatga qo'shildi.")
    return redirect("orders:cart")


@require_POST
def cart_change(request, key):
    action = request.POST.get("action")
    if action == "remove":
        remove_item(request, key)
    else:
        quantity = int(request.POST.get("quantity", 1) or 1)
        update_quantity(request, key, quantity)
    return redirect("orders:cart")


def checkout(request):
    summary = cart_summary(request)
    if not summary["items"]:
        messages.warning(request, "Avval savatga mahsulot qo'shing.")
        return redirect("catalog:menu")

    initial = {"payment_method": Order.PaymentMethod.CASH}
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data.get("latitude")
            longitude = form.cleaned_data.get("longitude")
            distance_km = form.cleaned_data.get("distance_km") or 0
            quote = build_delivery_quote(distance_km=distance_km, latitude=latitude, longitude=longitude)
            subtotal = quantize_money(summary["subtotal"])
            total = quantize_money(subtotal + quote.delivery_fee)
            order = Order.objects.create(
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                note=form.cleaned_data.get("note", ""),
                payment_method=form.cleaned_data["payment_method"],
                subtotal=subtotal,
                delivery_fee=quote.delivery_fee,
                total=total,
                distance_km=quote.distance_km,
                eta_minutes=quote.eta_minutes,
                branch=quote.branch,
                latitude=latitude,
                longitude=longitude,
            )
            for item in summary["items"]:
                options_text = ", ".join(opt["name"] for opt in item["options"])
                OrderItem.objects.create(
                    order=order,
                    product_name=item["name"],
                    unit_price=item["unit_price"],
                    quantity=item["quantity"],
                    options_text=options_text,
                    line_total=item["line_total"],
                )
            clear_cart(request)
            messages.success(request, f"Buyurtma #{order.pk} qabul qilindi.")
            return redirect("orders:order_detail", order_id=order.pk)
    else:
        form = CheckoutForm(initial=initial)

    quote = build_delivery_quote(distance_km=0)
    return render(request, "orders/checkout.html", {
        "cart": summary,
        "form": form,
        "delivery_quote": quote,
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items", "branch"), pk=order_id)
    status_rank = {
        Order.Status.RECEIVED: 1,
        Order.Status.COOKING: 2,
        Order.Status.ON_THE_WAY: 3,
        Order.Status.DELIVERED: 4,
        Order.Status.CANCELED: 0,
    }.get(order.status, 0)
    return render(request, "orders/order_detail.html", {"order": order, "status_rank": status_rank})


@require_GET
def delivery_quote_view(request):
    try:
        lat = request.GET.get("latitude")
        lng = request.GET.get("longitude")
        distance = float(request.GET.get("distance_km", 0) or 0)
        quote = build_delivery_quote(
            distance_km=distance,
            latitude=float(lat) if lat else None,
            longitude=float(lng) if lng else None,
        )
        return JsonResponse({
            "ok": True,
            "distance_km": quote.distance_km,
            "delivery_fee": float(quote.delivery_fee),
            "eta_minutes": quote.eta_minutes,
            "branch": quote.branch.name if quote.branch else None,
        })
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "Invalid coordinates or distance."}, status=400)
