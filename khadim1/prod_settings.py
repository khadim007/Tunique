
import dj_database_url
from .settings import *


DEBUG = False
TEMPLATE_DEBUG = False

DATABASES['default'] = dj_database_url.config()

SECRET_KEY = 'f7_$#$+*8j4+9_-*waiqhdzfg#jz(!g42x4y$93tylx^qetc8g'

ALLOWED_HOSTS = ['khadim007.herokuapp.com']