"""
Django settings for simpdu project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c^-$x(edvg3!dfpx^t0pf$*9n#v!#252dxgta-k+n)f*yf4&cd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'suit',
    'admin_tools.menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'daterange_filter',
    'ckeditor',
    # 'debug_toolbar',
    'mptt',
    'cas',
    'loginas',
    'master',
    'accounts',
    'kepegawaian',
    'perusahaan',
    'izin',
    'pembangunan',
    # 'telebot',
    'raven.contrib.django.raven_compat',
    'mobile',
    'tastypie',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'simpdu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simpdu.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'simpatik',
        'USER':'simpatik',
        'PASSWORD':'!QAZ@WSX',
        'PORT': '3306',
        'HOST': '127.0.0.1',
        # 'OPTIONS': {
        #     "init_command": "SET foreign_key_checks = 0;",
        #     # "init_command": "SET storage_engine=INNODB",
        #  },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_INPUT_FORMATS = [
      "%d-%m-%Y %H.%M.%S", 
      "%d-%m-%Y %H.%M.%S.%f", 
      "%d-%m-%Y %H.%M", 
      "%d-%m-%Y", 
      "%d-%m-%Y %H.%M.%S", 
      "%d-%m-%Y %H.%M.%S.%f", 
      "%d-%m-%Y %H.%M", 
      "%d-%m-%Y", 
      "%m/%d/%Y %H.%M.%S", 
      "%m/%d/%Y %H.%M.%S.%f", 
      "%m/%d/%Y %H.%M", 
      "%m/%d/%Y", 
      "%m/%d/%Y %H.%M.%S", 
      "%m/%d/%Y %H.%M.%S.%f", 
      "%m/%d/%Y %H.%M", 
      "%m/%d/%Y", 
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d"
    ]

DATE_INPUT_FORMATS = ("%d-%m-%Y", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%Y", "%d %b %Y", "%d %B %Y", "%Y-%m-%d")

# configuraton CAS
CAS_SERVER_URL = "http://siabjo.kedirikab.go.id/cas/"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'cas.backends.CASBackend',
    'accounts.backends.CASBackend',
)

CAS_LOGOUT_COMPLETELY = False
CAS_PROVIDE_URL_TO_LOGOUT = True
CAS_GATEWAY = True
CAS_AUTO_CREATE_USER = False
CAS_CUSTOM_FORBIDDEN = 'login_failed'
USE_X_FORWARDED_HOST = True

# Djago Loginas
CAN_LOGIN_AS = 'accounts.views.login_as'
# End Django Loginas

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'files/static-collected/')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'files/media/')

LOGIN_URL = '/admin/login/'

AUTH_USER_MODEL = 'accounts.Account'

# ADMIN_TOOLS_MENU = 'menupembangunan.CustomMenu'
ADMIN_TOOLS_MENU = 'menu.CustomMenu'

#LOGIN_URL = 'frontlogin'

#LOGOUT_URL = 'frontlogout'

LOGIN_REDIRECT_URL = 'frontindex'

HTMLVALIDATOR_ENABLED = True

HTMLVALIDATOR_VNU_JAR = './contrib/vnu.jar'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.kedirikab.go.id'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hariyanti@kedirikab.go.id'
EMAIL_HOST_PASSWORD = 'kediri@4531'
DEFAULT_FROM_EMAIL = 'noreply@simpatik.kedirikab.go.id'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '100%',
    },
}

TELGRAM_API_TOKEN = '321364862:AAFE6CglJ_u8-TGuAbV7YBIiIU0rhqukNTI'
