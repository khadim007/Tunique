
import dj_database_url
from .settings import *


DEBUG = True
TEMPLATE_DEBUG = False

DATABASES['default'] = dj_database_url.config()

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['khadim007.herokuapp.com']