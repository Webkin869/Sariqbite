from decimal import Decimal
from apps.catalog.models import Product, ProductOption

SESSION_KEY = "sariqbite_cart"


def _make_key(product_id: int, option_ids: list[int]) -> str:
    option_ids = sorted(option_ids)
    return f"{product_id}:{'-'.join(str(i) for i in option_ids)}"


def get_cart(request):
    return request.session.get(SESSION_KEY, {})


def save_cart(request, cart):
    request.session[SESSION_KEY] = cart
    request.session.modified = True


def add_to_cart(request, product: Product, quantity: int = 1, option_ids: list[int] | None = None):
    option_ids = option_ids or []
    options = list(ProductOption.objects.filter(product=product, id__in=option_ids, is_active=True))
    key = _make_key(product.id, [opt.id for opt in options])
    cart = get_cart(request)
    item = cart.get(key, {
        "product_id": product.id,
        "name": product.name,
        "price": str(product.price),
        "quantity": 0,
        "options": [{"id": opt.id, "name": opt.name, "extra_price": str(opt.extra_price)} for opt in options],
    })
    item["quantity"] += max(quantity, 1)
    cart[key] = item
    save_cart(request, cart)


def update_quantity(request, key: str, quantity: int):
    cart = get_cart(request)
    if key not in cart:
        return
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key]["quantity"] = quantity
    save_cart(request, cart)


def remove_item(request, key: str):
    cart = get_cart(request)
    cart.pop(key, None)
    save_cart(request, cart)


def clear_cart(request):
    save_cart(request, {})


def cart_summary(request):
    cart = get_cart(request)
    items = []
    subtotal = Decimal("0")
    for key, row in cart.items():
        base = Decimal(row["price"])
        extras = sum(Decimal(opt["extra_price"]) for opt in row.get("options", []))
        quantity = int(row.get("quantity", 1))
        unit = base + extras
        line_total = unit * quantity
        subtotal += line_total
        items.append({
            "key": key,
            "name": row["name"],
            "quantity": quantity,
            "options": row.get("options", []),
            "unit_price": unit,
            "line_total": line_total,
        })
    return {
        "items": items,
        "count": sum(item["quantity"] for item in items),
        "subtotal": subtotal,
    }
