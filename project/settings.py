from pathlib import Path
import os
from . import database

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-8^fq+a!kh-4pm8#y(urc^&zum$01nvb69$s=vnif(#gn6o7)_!'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['thebookstack-2.onrender.com', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
DATABASES = {
    'default': database.config()
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# URLs
READER_REDIRECT_URL = 'https://frontend-pink-nine.vercel.app/'
AUTHOR_REDIRECT_URL = 'https://frontend-pink-nine.vercel.app/authorHome'
LOGIN_REDIRECT_URL = 'https://frontend-pink-nine.vercel.app/'
LOGIN_URL = '/login/'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://frontend-pink-nine.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [ 
    'authorization', 
    'content-type', 
    'x-csrftoken',
]

CORS_EXPOSE_HEADERS = [ 
    'Content-Type', 
    'X-CSRFToken',
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://frontend-pink-nine.vercel.app",
]

SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None

SESSION_COOKIE_HTTPONLY = False

SESSION_COOKIE_DOMAIN = '.thebookstack-2.onrender.com'

# Important for HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (uploads like book cover images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email config (for password resets, etc)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'thebookstack2fa@gmail.com'
EMAIL_HOST_PASSWORD = 'evdx tivi rlax pgah'  # App password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Custom user model
AUTH_USER_MODEL = "api.SiteUser"

# Internal IPs for debug toolbar (optional)
INTERNAL_IPS = ['127.0.0.1']
