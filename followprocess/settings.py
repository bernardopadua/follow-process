import os
from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'followprocess.settings')

#Custom envs
cenv = Env()
cenv.read_env('.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j!hs-$s2ot&m$x#kwxkbd9cf^#c7nkaru!pzi^8=#yw)sh95ss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #Frameworks
    'rest_framework',
    'channels',

    #Internal apps
    'followprocess.process',
]

REDIS_SERVER    = ""
RABBITMQ_SERVER = ""
RABBITMQ_USER   = ""
RABBITMQ_PASS   = ""
RABBITMQ_VHOST  = ""

#Running on Docker ?
IS_DOCKER = cenv.bool("IS_DOCKER")

if IS_DOCKER:
    REDIS_SERVER    = "localhost"#"redis"
    RABBITMQ_SERVER = "localhost"#"rabbitmq"
    RABBITMQ_USER   = "puser"
    RABBITMQ_PASS   = "ppass"
    RABBITMQ_VHOST  = "pvhost"
else:
    REDIS_SERVER    = cenv("REDIS_SERVER")
    REDIS_PORT      = cenv("REDIS_PORT")
    REDIS_USER      = cenv("REDIS_USER")
    REDIS_PASSWORD  = cenv("REDIS_PASSWORD")
    REDIS_HOST      = cenv("REDIS_HOST")
    RABBITMQ_SERVER = cenv("RABBITMQ_SERVER")
    RABBITMQ_USER   = cenv("RABBITMQ_USER")
    RABBITMQ_PASS   = cenv("RABBITMQ_PASS")
    RABBITMQ_VHOST  = cenv("RABBITMQ_VHOST")

#CELERY
REDIS_CHANNELS_HOST       = [(REDIS_SERVER, 6379)]
CELERY_BROKER_URL         = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_SERVER}:5672/{RABBITMQ_VHOST}"
if REDIS_SERVER != '':
    CELERY_RESULT_BACKEND = f"redis://{REDIS_SERVER}:6379/0"
else:
    CELERY_RESULT_BACKEND = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
    REDIS_CHANNELS_HOST   = [CELERY_RESULT_BACKEND]
CELERY_MAX_CACHED_RESULTS = -1

#APP - CONFIG
LOGIN_URL          = "/login"
LOGIN_REDIRECT_URL = '/home'

#WEBSOCKETS - DJANGO CHANNELS
ASGI_APPLICATION   = "followprocess.routing.application"
CHANNEL_LAYERS     = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": REDIS_CHANNELS_HOST,
        },
    },
}

#RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'followprocess.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'followprocess/templates')
        ],
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

WSGI_APPLICATION = 'followprocess.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

#Env vars from docker building
FP_DB_HOST     = cenv('FP_DB_HOST')
FP_DB_PORT     = cenv('FP_DB_PORT')
FP_DB_NAME     = cenv('FP_DB_NAME')
FP_DB_USER     = cenv('FP_DB_USER')
FP_DB_PASSWORD = cenv('FP_DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': FP_DB_HOST,
        'PORT': FP_DB_PORT,
        'NAME': FP_DB_NAME,
        'USER': FP_DB_USER,
        'PASSWORD': FP_DB_PASSWORD,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = BASE_DIR + '/static'
STATIC_URL = '/static/'