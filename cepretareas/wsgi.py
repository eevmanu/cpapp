# coding=utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cepretareas.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

# Heroku Setting
application = Cling(get_wsgi_application())
# application = get_wsgi_application()
