from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-only-change-me-before-production')
DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'
ALLOWED_HOSTS = [x.strip() for x in os.getenv('DJANGO_ALLOWED_HOSTS','127.0.0.1,localhost').split(',') if x.strip()]

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
    'django.contrib.messages','django.contrib.staticfiles','vault.apps.VaultConfig',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware','vault.middleware.SecurityHeadersMiddleware',
]
ROOT_URLCONF='cybervault.urls'
TEMPLATES=[{
    'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,
    'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']},
}]
WSGI_APPLICATION='cybervault.wsgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':10}},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE='en-us'; TIME_ZONE='Europe/Istanbul'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; STATIC_ROOT=BASE_DIR/'staticfiles'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_REDIRECT_URL='vault:dashboard'; LOGOUT_REDIRECT_URL='login'; LOGIN_URL='login'
SESSION_COOKIE_HTTPONLY=True; CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Lax'; CSRF_COOKIE_SAMESITE='Lax'
SESSION_COOKIE_AGE=1800; SESSION_SAVE_EVERY_REQUEST=True
SECURE_CONTENT_TYPE_NOSNIFF=True; X_FRAME_OPTIONS='DENY'
if not DEBUG:
    SESSION_COOKIE_SECURE=True; CSRF_COOKIE_SECURE=True
    SECURE_SSL_REDIRECT=True; SECURE_HSTS_SECONDS=31536000; SECURE_HSTS_INCLUDE_SUBDOMAINS=True; SECURE_HSTS_PRELOAD=True
