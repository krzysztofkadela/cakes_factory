"""
Django settings for cakestore project.
"""

import os
import dj_database_url
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# 1. Load environment variables from .env file
load_dotenv()

# 2. Define BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# 3. Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# 4. Debug Mode
DEBUG = os.getenv("DEVELOPMENT") == "True"

# 5. Allowed Hosts
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "cake-factory-65cd55cbb35d.herokuapp.com",
]

# 6. Stripe Settings
STRIPE_CURRENCY = "usd"
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WH_SECRET = os.getenv("STRIPE_WH_SECRET", "")

# 7. Email Settings
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "Cake Factory <cakefactorystore24@gmail.com>"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASS")
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Cake Factory <cakefactorystore24@gmail.com>")

# 8. Free Delivery Settings
FREE_DELIVERY_THRESHOLD = 50.00
STANDARD_DELIVERY_CHARGE = 5.00

# 9. Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_countries",
    "crispy_forms",
    "crispy_bootstrap5",
    "storages",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "products",
    "orders",
    "users",
    "home",
    "newsletter",
]

# 10. Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# 11. CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://cake-factory-65cd55cbb35d.herokuapp.com"
]

# 12. Root URL Config
ROOT_URLCONF = "cakestore.urls"

# 13. Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "products.context_processors.categories_context",
                "orders.context_processors.cart_context",
            ],
        },
    },
]

# 14. Authentication Backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# 15. Site ID
if DEBUG:
    SITE_ID = 2  # assuming your local site in admin has ID=2
else:
    SITE_ID = 1  # production site ID

# 16. User Authentication / Allauth
AUTH_USER_MODEL = "users.CustomUser"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Cake Factory] "

# Adjust protocol based on environment:
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False

# 17. WSGI Application
WSGI_APPLICATION = "cakestore.wsgi.application"

# 18. Database Configuration (with SSL and health checks)
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=not DEBUG,
        conn_health_checks=True,  # => Reconnect if idle
    )
}

# 19. Static & Media Files
if DEBUG:
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [BASE_DIR / "static"]
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    AWS_STORAGE_BUCKET_NAME = "cake-factory-65cd55cbb35d"
    AWS_S3_REGION_NAME = "eu-west-1"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    AWS_S3_OBJECT_PARAMETERS = {
        "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
        "CacheControl": "max-age=94608000",
    }

    STATICFILES_STORAGE = "custom_storages.StaticStorage"
    DEFAULT_FILE_STORAGE = "custom_storages.MediaStorage"

    STATICFILES_LOCATION = "static"
    MEDIAFILES_LOCATION = "media"

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"

# 20. Messages Framework (Bootstrap Friendly)
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# 21. Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 22. Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 23. Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"