
from pathlib import Path

import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str


import os 
from dotenv import load_dotenv

from datetime import timedelta
import dj_database_url

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-it68_3qby^6bxtjbw_+lu*p@%e37#ttam0&-y4lu@hn2g_#f#$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# Application definition
APPS_MODULES = [
    'authentication',
    'denonciationapp',
]

INITIAL_MODULES = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRDS_MODULES = [
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',   
    'drf_yasg',
    'allauth',
    'allauth.account',
]

INSTALLED_APPS = APPS_MODULES + INITIAL_MODULES + THIRDS_MODULES


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'denonciationapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'denonciationapi.wsgi.application'


ALLOWED_HOSTS = ['*']
 
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

#Django Rest Framework strategy

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
     'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

#for allauth
AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]


SIMPLE_JWT = {
    'USER_ID_FIELD': 'email',
    'AUTH_HEADER_TYPES': 'Bearer',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=24*60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.RefreshToken',
    )
}


#Swagger setting configuration
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}



"""DATABASES = {
	'default': {
		'ENGINE': os.getenv('DB_ENGINE','django.db.backends.sqlite3'),
		'NAME':  os.getenv('DB_NAME',os.path.join(BASE_DIR, "db.sqlite3")),  
		'USER': os.getenv('DB_USER','root'),
		'PASSWORD': os.getenv('DB_PASSWORD','root'),
		'HOST': os.getenv('DB_HOST','localhost'),
		'PORT': os.getenv('DB_PORT','5432')
	}
}"""

DATABASES = {
	'default':   dj_database_url.parse(os.environ.get('DATABASE_URL'))

		
	
}

#Djoser settings
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activation/<str:email>/<str:code>',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL' :True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION' : True,

    'USER_CREATE_PASSWORD_RETYPE' : True,
    'SET_USERNAME_RETYPE': True,


    'SET_PASSWORD_RETYPE' : True,
    'PASSWORD_RESET_CONFIRM_RETYPE':True,

    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND' : True,
    'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND' : True,

    'SERIALIZERS': {
        'user_create' : 'authentication.serializers.UserCreateSerializer',
        'user' : 'djoser.serializers.UserSerializer',
        'current_user' : 'djoser.serializers.UserSerializer',
        'user_delete' : 'djoser.serializers.UserSerializer',

        },
    #'EMAIL': EMAIL,

    'LOGIN_FIELD' : 'email'
}

#Email sending Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST =  os.getenv('EMAIL_HOST')

EMAIL_USE_TLS =os.getenv('EMAIL_USE_TLS')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTH_USER_MODEL = 'authentication.Administrator'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



"""
TEST  DATA
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MDUzOTAyNywianRpIjoiODQ5ZWIxYjYwYWZiNGNjNDk5ZDRkYjI3NmMwNzQ1OGMiLCJ1c2VyX2lkIjoic3lhb21hcml1c0BnbWFpbC5jb20ifQ.4OfMu0BcOtWkrD8xMFRWQrcthhr2wZp6VHK5YNiwa5k",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgwMTkzNDI3LCJqdGkiOiJlNGU3OTA0MGNhNDk0MmYzYjBjMWJhMjFhNmQzOGM5OCIsInVzZXJfaWQiOiJzeWFvbWFyaXVzQGdtYWlsLmNvbSJ9.0y19h8eD9BkSXI_YCtI0-mvz-IbKaSJctZ6raEwP_OM"
}

{
  "address": {},
  "profil": "http://127.0.0.1:8000/admin_images/Usecase_hackathon_App_web_Competition_avfZN0h.png",
  "first_name": "Yao Marius",
  "last_name": "SODOKIN",
  "email": "syaomarius@gmail.com",
  "id": 7
}

"""
