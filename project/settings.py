"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

import logging
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q$xc^z%u1x2&2!_wfknarl2im7%5o(8o&q@9fhjiljz(td)@vh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ---------------------------
    # подключаем новые приложения
    #----------------------------

    'simpleapp',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'fpages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
    'rest_framework',
]

SITE_ID = 1 # site_id используется в случае, есл и данный проект управляет несколькими сайтами

# Middleware - объекты промежуточных слоёв
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', # проверка безопасности (XSS, nosniff, HSTS, CORS, SSL, etc)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware', # выполнение стандартных процедур над URL
    'django.middleware.csrf.CsrfViewMiddleware', # проверка безопасности от угроз типа CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # основы аутентификации и идентификации
    # 'django.middleware.cache.UpdateCacheMiddleware', # кэширование на стороне клиента
    # 'django.middleware.cache.FetchFromCacheMiddleware', # кэширование на стороне клиента
    'django.contrib.messages.middleware.MessageMiddleware', # поддержка сообщений, лежащих в основе работы с куки и сессиями
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware', # статистические страницы
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.custom_simplemiddleware.SimpleMiddleware', # кастомный middleware
    'django.middleware.middlewares.TimezoneMiddleware',

]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'debug': {
            'format': '{levelname} - {asctime} - {message} \n',
            'style': '{',
        },
        'info': {
            'format': '{levelname} - {asctime} - {message} - {module} - {pathname} \n',
            'style': '{',
        },
        'warning': {
            'format': '{levelname} - {asctime} - {message} - {pathname} \n',
            'style': '{',
        },
        'error': {
            'format': '{levelname} - {asctime} - {message} - {exc_info} - {pathname} \n',
            'style': '{',
        },
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # обработчики
    'handlers': {
        # 'console_debug': {
        #     'level': 'DEBUG',
        #     'class': 'logging.StreamHandler',
        #     'filters': ['require_debug_true'],
        #     'formatter': 'debug',
        # },
        'console_info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'info',
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'warning',
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'error',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'error',
        },
        'general_log': {
            'level': 'DEBUG',
            'filename': 'logs/general.log',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'debug',
        },
        'errors_log': {
            'level': 'ERROR',
            'filename': 'logs/errors.log',
            'class': 'logging.FileHandler',
            'formatter': 'error',
        },
        'security_log': {
            'level': 'INFO',
            'filename': 'logs/security.log',
            'class': 'logging.FileHandler',
            'formatter': 'info',
        },
    },

    # регистраторы
    'loggers': {
        'django': {
            'handlers': [
                # 'console_debug',
                'console_info',
                'console_warning',
                'console_error',
                'general_log',
            ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errors_log', 'mail_admins',],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['errors_log', 'mail_admins',],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['errors_log',],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['errors_log',],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_log'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

ROOT_URLCONF = 'project.urls'

# локализация
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # аутентификация по username
    'allauth.account.auth_backends.AuthenticationBackend', # бэкенд аутентификации, представленный пакетом allauth (email или сервис-провайдер)
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2', # путь импорта специального модуля Django для работы с конкретным типом БД
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     },
# }



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us' # en-us

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Russian'),
]

TIME_ZONE = 'UTC'

USE_I18N = True # поддержка интернационализации в приложении

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static'] # !!!!!!!!!!!

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/products'

# форма для дополнительной обработки регистрации пользователя \
# (чтобы allauth распознал форму как ту, что должна выполняться вместо формы по умолчанию.)
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

ACCOUNT_EMAIL_REQUIRED = True # поле email является обязательным
ACCOUNT_UNIQUE_EMAIL = True # поле email является уникальным
ACCOUNT_USERNAME_REQUIRED = False # поле username является необязательным
ACCOUNT_AUTHENTICATION_METHOD = 'email' # аутентификация посредством электронной почты
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # верификация почты
ACCOUNT_CONFIRM_EMAIL_ON_GET = True # активация аккаунта сразу после перехода по ссылке
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 4 # храним количество дней, когда доступна ссылка на подтверждение регистрации.

# настройки почты
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # класс отправителя сообщений
EMAIL_PORT = 465 # порт для приёма писем почтовым сервером
EMAIL_HOST = 'smtp.yandex.ru' # хост почтового сервера
EMAIL_HOST_USER = 'online-store.project' # логин пользователя почтового сервиса
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD_ONLINE_STORE') # пароль пользователя почтового сервиса
EMAIL_USE_TLS = False # необходимость использования TLS
EMAIL_USE_SSL = True # необходимость использования SSL

DEFAULT_FROM_EMAIL = 'online-store.project@yandex.ru' # почтовый адрес отправителя по умолчанию

EMAIL_SUBJECT_PREFIX = 'Ура! ' # текст в начале письма с сообщением
SERVER_EMAIL = 'online-store.project@yandex.ru' # адрес почты, от имени которой будет отправляться письмо при вызове mail_admins и mail_manager.
MANAGERS = (
    ('Igor', 'igoroshust75@gmail.com'),
    ('Igor', 'igoroshust@yandex.ru'),
    ('Egor', 'boxforstudies@gmail.com'),
)
#
# ADMINS = (
#     ('Igor', 'igoroshust75@gmail.com'),
#     ('Egor', 'boxforstudies@gmail.com'),
# )

# Пагинация для REST-Framework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


# ======== КЭШИРОВАНИЕ ========
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', # класс, подключающий кэширование к Django. Здесь писана логика работы cache
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # соединяем базовую директорию с файлом 'cache_files'
        'TIMEOUT': 30, # время хранения данных в кэше (в секундах)
    }
}