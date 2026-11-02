from .base import *  # noqa: F403
from .base import REST_FRAMEWORK

SECRET_KEY = "test-secret-key"
DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost"]

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_THROTTLE_CLASSES": [],
}

LOGGING = {"version": 1, "disable_existing_loggers": False, "root": {"level": "CRITICAL"}}
