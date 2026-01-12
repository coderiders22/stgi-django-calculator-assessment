from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY environment variable is not set!")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".koyeb.app",
    ".vercel.app",
    "stgi-calculatorpro.koyeb.app",
]

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

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Must be FIRST
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ============================================
# CORS Configuration
# ============================================
CORS_ALLOW_CREDENTIALS = True

# ❌ WRONG (with trailing slash):
# "https://stgi-django-calculator-assessment.vercel.app/"

# ✅ CORRECT (no trailing slash):
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://stgi-django-calculator-assessment.vercel.app",  # NO trailing slash!
]

# For development - allows all origins
CORS_ALLOW_ALL_ORIGINS = DEBUG

# ============================================
# CSRF Configuration
# ============================================
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://stgi-django-calculator-assessment.vercel.app",  # NO trailing slash!
    "https://stgi-calculatorpro.koyeb.app",
]

# ============================================
# Session & Cookie Configuration
# ============================================
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_DOMAIN = None

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'
CSRF_COOKIE_HTTPONLY = False  # JavaScript needs to read this
CSRF_COOKIE_DOMAIN = None

# ============================================
# Additional CORS Headers (Add these!)
# ============================================
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ============================================
# Database Configuration
# ============================================
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        ssl_require=not DEBUG,
        default="sqlite:///db.sqlite3"
    )
}

if not DEBUG and "DATABASE_URL" not in os.environ:
    raise Exception("DATABASE_URL environment variable is required in production!")

# ============================================
# Static Files
# ============================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================
# REST Framework
# ============================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}