from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


IS_VERCEL = bool(os.getenv("VERCEL"))

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-local-development-only-change-me")
DEBUG = env_bool("DEBUG", default=not IS_VERCEL)

# Vercel sometimes sets a custom production domain such as
# sariqbite.vercel.app. Keep the env value, but always append safe defaults
# so a missing ALLOWED_HOSTS variable does not break the deployed site.
def unique_items(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        item = item.strip()
        if item and item not in result:
            result.append(item)
    return result


VERCEL_URL = os.getenv("VERCEL_URL", "").strip()  # example: sariqbite.vercel.app

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",

    # Vercel asosiy domenlar
    ".vercel.app",
    "sariqbite.vercel.app",

    # Hozir xatoda chiqqan domen
    "sariqbite-gcnzgtu1u-webkinminecraft-8525s-projects.vercel.app",
]

# Vercel avtomatik beradigan domainni ham qo‘shadi
VERCEL_URL = os.environ.get("VERCEL_URL")
if VERCEL_URL:
    ALLOWED_HOSTS.append(VERCEL_URL)

CSRF_TRUSTED_ORIGINS = [
    "https://*.vercel.app",
    "https://sariqbite.vercel.app",
    "https://sariqbite-gcnzgtu1u-webkinminecraft-8525s-projects.vercel.app",
]

if VERCEL_URL:
    CSRF_TRUSTED_ORIGINS.append(f"https://{VERCEL_URL}")
BOT_SHARED_KEY = os.getenv("BOT_SHARED_KEY", "")

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.catalog",
    "apps.orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.orders.context_processors.cart_summary",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    if IS_VERCEL:
        raise RuntimeError("DATABASE_URL Vercel environment variables ichida yo'q. Postgres ulang.")
    
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "SariqBite Admin",
    "site_header": "SariqBite",
    "site_brand": "SariqBite",
    "welcome_sign": "SariqBite boshqaruv paneli",
    "site_logo_classes": "img-circle",
    "topmenu_links": [
        {"name": "Storefront", "url": "/", "new_window": True},
    ],
    "custom_css": "css/site.css",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "catalog.Category": "fas fa-layer-group",
        "catalog.Branch": "fas fa-store",
        "catalog.Product": "fas fa-burger",
        "catalog.ProductOption": "fas fa-plus-circle",
        "orders.Order": "fas fa-motorcycle",
        "orders.OrderItem": "fas fa-receipt",
    },
}
