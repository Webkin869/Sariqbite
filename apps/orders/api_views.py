import json
from decimal import Decimal

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from apps.catalog.models import Category, Product
from .models import Order, OrderItem
from .services import build_delivery_quote, quantize_money


def _api_forbidden(request):
    if not settings.BOT_SHARED_KEY:
        return False
    return request.headers.get("X-API-Key", "") != settings.BOT_SHARED_KEY


def _bad_method():
    return JsonResponse({"ok": False, "error": "Method not allowed."}, status=405)


@require_GET
def categories_api(request):
    data = [{"id": c.id, "name": c.name, "slug": c.slug} for c in Category.objects.all()]
    return JsonResponse({"ok": True, "results": data})


@require_GET
def products_api(request):
    qs = Product.objects.filter(is_active=True).select_related("category").prefetch_related("options")
    category_slug = request.GET.get("category")
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    data = []
    for product in qs:
        data.append({
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "price": float(product.price),
            "category": product.category.name,
            "image_url": product.image_url,
            "options": [
                {"id": opt.id, "name": opt.name, "extra_price": float(opt.extra_price)}
                for opt in product.options.filter(is_active=True)
            ],
        })
    return JsonResponse({"ok": True, "results": data})


@require_GET
def product_detail_api(request, slug):
    try:
        product = Product.objects.prefetch_related("options", "category").get(slug=slug, is_active=True)
    except Product.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Product not found."}, status=404)
    return JsonResponse({
        "ok": True,
        "result": {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "price": float(product.price),
            "category": product.category.name,
            "prep_minutes": product.prep_minutes,
            "options": [
                {"id": opt.id, "name": opt.name, "extra_price": float(opt.extra_price)}
                for opt in product.options.filter(is_active=True)
            ],
        },
    })


@csrf_exempt
@require_POST
def delivery_quote_api(request):
    if _api_forbidden(request):
        return JsonResponse({"ok": False, "error": "Forbidden."}, status=403)
    try:
        payload = json.loads(request.body or "{}")
        quote = build_delivery_quote(
            distance_km=float(payload.get("distance_km", 0) or 0),
            latitude=float(payload["latitude"]) if payload.get("latitude") is not None else None,
            longitude=float(payload["longitude"]) if payload.get("longitude") is not None else None,
        )
        return JsonResponse({
            "ok": True,
            "result": {
                "distance_km": quote.distance_km,
                "delivery_fee": float(quote.delivery_fee),
                "eta_minutes": quote.eta_minutes,
                "branch": quote.branch.name if quote.branch else None,
            },
        })
    except (TypeError, ValueError, KeyError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid payload."}, status=400)


@csrf_exempt
@require_POST
def create_order_api(request):
    if _api_forbidden(request):
        return JsonResponse({"ok": False, "error": "Forbidden."}, status=403)
    try:
        payload = json.loads(request.body or "{}")
        items = payload["items"]
        if not items:
            return JsonResponse({"ok": False, "error": "Cart is empty."}, status=400)

        latitude = payload.get("latitude")
        longitude = payload.get("longitude")
        distance_km = float(payload.get("distance_km", 0) or 0)
        quote = build_delivery_quote(
            distance_km=distance_km,
            latitude=float(latitude) if latitude is not None else None,
            longitude=float(longitude) if longitude is not None else None,
        )

        subtotal = Decimal("0")
        normalized_items = []
        for raw_item in items:
            product = Product.objects.prefetch_related("options", "category").get(id=raw_item["product_id"], is_active=True)
            quantity = int(raw_item.get("quantity", 1) or 1)
            selected_option_ids = raw_item.get("option_ids", [])
            options = list(product.options.filter(id__in=selected_option_ids, is_active=True))
            unit_price = product.price + sum((opt.extra_price for opt in options), Decimal("0"))
            line_total = unit_price * quantity
            subtotal += line_total
            normalized_items.append((product, quantity, options, unit_price, line_total))

        subtotal = quantize_money(subtotal)
        total = quantize_money(subtotal + quote.delivery_fee)
        order = Order.objects.create(
            full_name=payload["full_name"],
            phone=payload["phone"],
            address=payload["address"],
            note=payload.get("note", ""),
            payment_method=payload.get("payment_method", Order.PaymentMethod.CASH),
            subtotal=subtotal,
            delivery_fee=quote.delivery_fee,
            total=total,
            distance_km=quote.distance_km,
            eta_minutes=quote.eta_minutes,
            branch=quote.branch,
            latitude=float(latitude) if latitude is not None else None,
            longitude=float(longitude) if longitude is not None else None,
            telegram_chat_id=str(payload.get("telegram_chat_id", "")),
        )
        for product, quantity, options, unit_price, line_total in normalized_items:
            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                unit_price=unit_price,
                quantity=quantity,
                options_text=", ".join(opt.name for opt in options),
                line_total=line_total,
            )
        return JsonResponse({
            "ok": True,
            "result": {
                "order_id": order.pk,
                "status": order.status,
                "subtotal": float(order.subtotal),
                "delivery_fee": float(order.delivery_fee),
                "total": float(order.total),
                "eta_minutes": order.eta_minutes,
            },
        })
    except Product.DoesNotExist:
        return JsonResponse({"ok": False, "error": "One of the products does not exist."}, status=404)
    except (TypeError, ValueError, KeyError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid payload."}, status=400)


@require_GET
def order_status_api(request, order_id):
    if _api_forbidden(request):
        return JsonResponse({"ok": False, "error": "Forbidden."}, status=403)
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Order not found."}, status=404)
    return JsonResponse({
        "ok": True,
        "result": {
            "order_id": order.pk,
            "status": order.status,
            "eta_minutes": order.eta_minutes,
            "total": float(order.total),
            "updated_at": order.updated_at.isoformat(),
        },
    })
