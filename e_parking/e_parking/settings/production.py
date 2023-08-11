from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]


CORS_ORIGIN_WHITELIST = [

    "https://master.d1v7zmxdk8f3fb.amplifyapp.com"
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/min',
        'anon_day': '50/day',
        'user': '20/min',
        'user_day': '100/day',
    }
}
# Required by DRF Throttler. https://www.django-rest-framework.org/api-guide/throttling/#how-clients-are-identified
NUM_PROXIES = 1


STATIC_URL = '/static/'

# Absolute filesystem path to the directory that will hold static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]