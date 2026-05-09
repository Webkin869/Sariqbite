# SariqBite Site

Django + Jazzmin asosidagi food delivery MVP.

## Nimalar bor
- sariq uslubdagi storefront
- kategoriya va mahsulotlar
- session-based savat
- km oshgani sari qimmatlashadigan delivery pricing
- Jazzmin admin
- Telegram bot uchun JSON API
- nearest branch bo'yicha delivery hisoblash

## Tez ishga tushirish
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Windowsda copy qiling
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_sariqbite
python manage.py runserver
```

Admin: `/admin/`
Site: `/`

## Demo login
`createsuperuser` bilan o'zingiz yaratasiz.

## Delivery pricing
Default formula:
- 0–2 km: 8 000 so'm
- 2–5 km: har km +2 000
- 5–8 km: har km +3 500
- 8+ km: har km +5 000

Bu qiymatlarni `apps/orders/services.py` ichida o'zgartirish mumkin.

## Bot API endpointlar
- `GET /api/categories/`
- `GET /api/products/`
- `GET /api/products/<slug>/`
- `POST /api/delivery-quote/`
- `POST /api/orders/create/`
- `GET /api/orders/<id>/status/`

Productionda `BOT_SHARED_KEY` qo'yib, botdan `X-API-Key` header yuboring.
