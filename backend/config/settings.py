from pathlib import Path
import os
import dj_database_url
from corsheaders.defaults import default_headers

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
    "stgi-calculatorpro.koyeb.app",  # Your backend
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
    "corsheaders.middleware.CorsMiddleware",  # Must be first
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
# CORS Configuration - Frontend can access Backend
# ============================================
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://stgi-django-calculator-assessment.vercel.app/",  # Your FRONTEND
]

# Only for development
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False

# ============================================
# CSRF Configuration
# ============================================
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://stgi-django-calculator-assessment.vercel.app/", 
    "https://stgi-calculatorpro.koyeb.app",  
]

# ============================================
# Session & Cookie Configuration for Cross-Origin
# ============================================
SESSION_COOKIE_SECURE = not DEBUG  # True in production (HTTPS only)
SESSION_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'  # Required for cross-origin
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_DOMAIN = None  # Don't set domain for cross-origin

CSRF_COOKIE_SECURE = not DEBUG  # True in production
CSRF_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'  # Required for cross-origin
CSRF_COOKIE_HTTPONLY = False  # Must be False so JavaScript can read it
CSRF_COOKIE_DOMAIN = None  # Don't set domain for cross-origin

# ============================================
# Database Configuration
# ============================================
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        ssl_require=not DEBUG,
        default="sqlite:///db.sqlite3"  # Fallback for local
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
# REST Framework Configuration
# ============================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}