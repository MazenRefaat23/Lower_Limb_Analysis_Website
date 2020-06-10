import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lower_Limb_Analysis_Website-master.settings")

application = get_wsgi_application()