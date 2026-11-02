from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE, REST_FRAMEWORK, config

DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        *REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"],
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_THROTTLE_CLASSES": [],
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

USE_DEBUG_TOOLBAR = DEBUG and config("USE_DEBUG_TOOLBAR", default=True, cast=bool)

if USE_DEBUG_TOOLBAR:
    try:
        import debug_toolbar  # noqa: F401
    except ImportError:
        USE_DEBUG_TOOLBAR = False

if USE_DEBUG_TOOLBAR:
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]
    INTERNAL_IPS = ["127.0.0.1"]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}
