from .base import *

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
        'default':  dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }

CSRF_TRUSTED_ORIGINS = ['https://resumebuilder.fly.dev/']

CORS_ORIGIN_ALLOW_ALL = True

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)


