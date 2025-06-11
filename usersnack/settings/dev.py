from usersnack.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost"]

CORS_ALLOW_ALL_ORIGINS = True
# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
