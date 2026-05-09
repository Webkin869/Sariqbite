from .cart import cart_summary as build_cart_summary


def cart_summary(request):
    return {"cart_summary": build_cart_summary(request)}
