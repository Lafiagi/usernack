from usersnack.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ["api.ile-wa.com"]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ["https://app.usersnack.com"]

FORCE_SCRIPT_NAME = "/usersnack"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
