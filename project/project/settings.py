# Содержит основные настройки django проекта
# Конфигурация приложений, шаблонов, middleware...

import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ безопасности
SECRET_KEY = config('SECRET_KEY') # Даем понять что нужно обратиться к env по ключу SECRET_KEY

# Режим отладки
DEBUG = config('DEBUG', default=False, cast=bool)

# Список разрешенных хостов ддля получения запросов
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Метод разделения
DJANGO_APPS = [  # Список встроенных django приложений
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django_filters',
]

THIRD_PARTY_APPS = [ # Списко сторонних приложений
    'rest_framework',
    'corsheaders',
]

LOCAL_APPS = [ # Список созданных локальных приложений
    'application',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS  # Общий список приложений

# Список для обработки запросов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

# Корневой url файл проекта
ROOT_URLCONF = 'project.urls'

# Конфигурация шаблонов django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Конфигурация базы данных (переходим на Postgresql)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='modelhub'),
        'USER': config('POSTGRES_USER', default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='password'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
        'ATOMIC_REQUESTS': True,
    }
}

# Валидаторы паролей
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Настройка статических файлов
STATIC_URL = 'static/' # Url статики
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Путь для собранных файлов статики


# Настройка Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Разрешить досутп всем
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle', # Ограничение запросов для анонсов
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour', # Лимит запросов для анонимных пользователей
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Рендеринг в JSON
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser', # Парсинг в JSON
    ]
}


# Настройка cors для разработки и продакшена
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = [  # Разрешенные источники
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]

# Настройка безопасности
SECURE_BROWSER_XSS_FILTER = True # Защита от XSS-атак
SECURE_CONTENT_TYPE_NOSNIFF = True # Запрет MIME-типов
X_FRAME_OPTIONS = 'DENY' # Защита от кликджекинга

# Настройка логирования
LOGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO', # Уровень логирования
            'class': 'logging.FileHandler', # Логирование в файл
            'filename': BASE_DIR / 'debug.log', # Путь к файлу
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'], # Используемый обработчик
            'level': 'INFO', # Уровень логирования
            'propagate': True, # Передача логов родительским логгерам
        }
    }
}