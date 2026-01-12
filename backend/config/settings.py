from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# CORE SETTINGS
# =====================

SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".koyeb.app",
    ".onrender.com",
]

# =====================
# APPLICATIONS
# =====================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "calculator",
]

# =====================
# MIDDLEWARE (ORDER IMPORTANT)
# =====================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# =====================
# URLS / TEMPLATES
# =====================

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# =====================
# DATABASE (KOYEB / POSTGRES)
# =====================

if "DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        )
    }


# =====================
# PASSWORD VALIDATION
# =====================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# =====================
# LANGUAGE / TIMEZONE
# =====================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =====================
# STATIC FILES
# =====================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =====================
# CORS SETTINGS (Vercel → Koyeb)
# =====================

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://stgi-django-calculator-assessment.vercel.app",
]

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# =====================
# SESSION & CSRF (🔥 THIS FIXES 500 ERROR 🔥)
# =====================

SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # frontend needs csrftoken

SESSION_COOKIE_DOMAIN = os.environ.get("SESSION_COOKIE_DOMAIN")
CSRF_COOKIE_DOMAIN = os.environ.get("CSRF_COOKIE_DOMAIN")

# =====================
# SECURITY (OPTIONAL BUT GOOD)
# =====================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False  # Koyeb handles HTTPS

# ===============================
# CORS
# ===============================
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://stgi-django-calculator-assessment.vercel.app",
]

# ===============================
# CSRF
# ===============================
CSRF_TRUSTED_ORIGINS = [
    "https://stgi-django-calculator-assessment.vercel.app",
]

CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"

# ⚠️ VERY IMPORTANT
CSRF_USE_SESSIONS = False
