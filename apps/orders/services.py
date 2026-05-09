from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from math import asin, cos, radians, sin, sqrt
from typing import Iterable, Optional

from apps.catalog.models import Branch

BASE_FEE = Decimal("8000")
MID_RATE = Decimal("2000")
FAR_RATE = Decimal("3500")
PREMIUM_RATE = Decimal("5000")


@dataclass
class DeliveryQuote:
    distance_km: float
    delivery_fee: Decimal
    eta_minutes: int
    branch: Optional[Branch]


def quantize_money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_tiered_delivery(distance_km: float) -> Decimal:
    distance = Decimal(str(max(distance_km, 0)))
    fee = BASE_FEE
    if distance <= Decimal("2"):
        return quantize_money(fee)
    tier2 = min(distance, Decimal("5")) - Decimal("2")
    if tier2 > 0:
        fee += tier2 * MID_RATE
    tier3 = min(distance, Decimal("8")) - Decimal("5")
    if tier3 > 0:
        fee += tier3 * FAR_RATE
    tier4 = distance - Decimal("8")
    if tier4 > 0:
        fee += tier4 * PREMIUM_RATE
    return quantize_money(fee)


def estimate_eta(distance_km: float, prep_minutes: int = 18) -> int:
    drive = 8 + int(max(distance_km, 0) * 3.2)
    return prep_minutes + drive


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return 2 * radius * asin(sqrt(a))


def nearest_branch(latitude: float, longitude: float, branches: Optional[Iterable[Branch]] = None) -> Optional[tuple[Branch, float]]:
    items = list(branches or Branch.objects.filter(is_active=True))
    if not items:
        return None
    ranked = [
        (branch, haversine_km(latitude, longitude, branch.latitude, branch.longitude))
        for branch in items
    ]
    ranked.sort(key=lambda item: item[1])
    return ranked[0]


def build_delivery_quote(distance_km: float = 0, latitude: float | None = None, longitude: float | None = None) -> DeliveryQuote:
    branch = None
    distance = max(distance_km, 0)
    if latitude is not None and longitude is not None:
        nearest = nearest_branch(latitude, longitude)
        if nearest:
            branch, distance = nearest
    fee = calculate_tiered_delivery(distance)
    eta = estimate_eta(distance)
    return DeliveryQuote(distance_km=round(distance, 2), delivery_fee=fee, eta_minutes=eta, branch=branch)
