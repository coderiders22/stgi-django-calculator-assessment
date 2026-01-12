


from pathlib import Path
import os
from corsheaders.defaults import default_headers  # 🔥 Add this import
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent

# CORE
SECRET_KEY = os.environ.get("SECRET_KEY", )
DEBUG = os.environ.get("DEBUG", "True") == "True"

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost, ']

# ===============================
# INSTALLED APPS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'calculator',
]

# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 🔥 Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# ===============================
# CORS SETTINGS - COMPLETE FIX
# ===============================
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://stgi-django-calculator-assessment.vercel.app",
]

#  CRITICAL: Allow cookie headers
CORS_ALLOW_HEADERS = list(default_headers) + [
    'set-cookie',
]

CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
    'Set-Cookie',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Cache preflight requests
CORS_PREFLIGHT_MAX_AGE = 86400

# ===============================
# CSRF SETTINGS
# ===============================
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_DOMAIN = None

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://stgi-django-calculator-assessment.vercel.app",
]

# ===============================
# SESSION SETTINGS
# ===============================
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_DOMAIN = None
SESSION_SAVE_EVERY_REQUEST = True

# ===============================
# URL CONFIG
# ===============================
ROOT_URLCONF = 'config.urls'

# ===============================
# TEMPLATES
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ===============================
# DATABASE
# ===============================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'calculator_db',
#         'USER': 'calculator_user',
#         'PASSWORD': 'calculator123',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# DATABASE (SECURE)

if "DATABASE_URL" in os.environ:
   
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        )
    }
    

# ===============================
# STATIC FILES
# ===============================
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'