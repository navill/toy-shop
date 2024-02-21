import os

from dotenv import load_dotenv

from commons.secret_manager import get_secret
from .base import *

load_dotenv()

DEBUG = True
ALLOWED_HOSTS = ['*']
PERSONAL_INFO_FERNET_KEY = b'IcOjQqKvv2UtU_M2a2HqfgcuvD-ThJ1SlG7Uab9QOYk='

secret = get_secret()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret["dbname"],
        'USER': secret["username"],
        'PASSWORD': secret["password"],
        'HOST': secret["host"],
        'PORT': secret["port"],
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
