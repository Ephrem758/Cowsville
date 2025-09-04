from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['cowsville-aau-cvma.com', 'api.cowsville-aau-cvma.com', 'www.cowsville-aau-cvma.com']

# Database - SQLite for now
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORS settings for your frontend
CORS_ALLOWED_ORIGINS = [
    "https://cowsville-aau-cvma.com",
    "https://www.cowsville-aau-cvma.com",
]
