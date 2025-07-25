from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-k)w#!4p!9r&k7ds9#d@53y)qur5zv@y5$7z2+49z^gh%+_(*6s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    #'jet' #jet is a third-party Django package providing a modern, customizable admin interface with enhanced features like a responsive dashboard.Install it using pip install django-jet.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist', #
    'authenticate',
    'rest_framework',
    #You don’t need to add rest_framework_simplejwt to INSTALLED_APPS because it’s a library providing 
    # JWT authentication backends, not a Django app requiring migrations. The rest_framework_simplejwt.token_blacklist
    # in INSTALLED_APPS enables token blacklisting for security (e.g., invalidating old refresh tokens).
    # You configure rest_framework_simplejwt in settings.py via the  SIMPLE_JWT dictionary and use its 
    # views (e.g., TokenObtainPairView) in your URL configuration.
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware', #
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
#WhiteNoise middleware serves static files efficiently in production, simplifying deployment without a separate 
# server like Nginx. You must install it using pip install whitenoise. 
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# CORS settings for React frontend

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'OPTIONS']
CORS_ALLOW_HEADERS = ['content-type', 'x-csrftoken']  # Add

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authenticate.authenticate.CustomJWTAuthentication', # class defined in authenticate.py
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '20/minute',
    }
}

'''The REST_FRAMEWORK configuration in settings.py defines settings for Django REST Framework (DRF) 
to enforce HTTP-only cookie-based JWT authentication and control API access. The 
'DEFAULT_AUTHENTICATION_CLASSES' specifies CustomJwtAuthentication from your authenticate app, which 
authenticates requests by validating JWTs stored in HTTP-only cookies, ensuring secure user verification. 
The 'DEFAULT_PERMISSION_CLASSES' with 'rest_framework.permissions.IsAuthenticated' restricts API endpoints to 
authenticated users only, enhancing security. The 'DEFAULT_THROTTLE_CLASSES' and 'DEFAULT_THROTTLE_RATES' limit 
request rates, allowing anonymous users 10 requests per minute ('anon': '10/minute') and authenticated users 20 
requests per minute ('user': '20/minute'), preventing abuse and ensuring fair API usage. This setup integrates 
seamlessly with your React (Vite) frontend, which sends requests with cookies for authentication.'''

# JWT settings for HTTP-only cookie-based authentication
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
}


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Static files (CSS, JavaScript, Images)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Ensure CSRF settings for HTTP-only cookies
CSRF_COOKIE_HTTPONLY = False  # Allow CSRF token to be accessible if needed
CSRF_COOKIE_SECURE = True  # Use with HTTPS in production
CSRF_COOKIE_SAMESITE = 'None'  # Match JWT cookie settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
