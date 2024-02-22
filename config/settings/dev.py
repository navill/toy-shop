from commons.secret_manager import secret_keys, db_secret_keys
from .base import *

load_dotenv()
DEBUG = True
ALLOWED_HOSTS = ['*']
PERSONAL_INFO_FERNET_KEY = secret_keys.get("FERNET_KEY", os.getenv("FERNET_KEY"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_secret_keys.get("NAME", os.getenv("NAME")),
        'USER': db_secret_keys.get("USERNAME", os.getenv("USERNAME")),
        'PASSWORD': db_secret_keys.get("PASSWORD", os.getenv("PASSWORD")),
        'HOST': db_secret_keys.get("HOST", os.getenv("HOST")),
        'PORT': db_secret_keys.get("PORT", os.getenv("PORT")),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     },
#     'slave': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASE_ROUTERS = ["commons.router.DatabaseRouter"]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{os.getenv('CACHE_LOCATION')}/{os.getenv('CACHE_DB')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }
