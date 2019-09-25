"""
WSGI config for CMS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

# import os, sys

# from django.core.wsgi import get_wsgi_application
# sys.path.append('/home/cms/ConferenceManagement')
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CMS.settings")
# os.environ["DJANGO_SETTINGS_MODULE"] = "CMS.settings"


# application = get_wsgi_application()
import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/cms/ConferenceManagement')
sys.path.append('/home/cms/ConferenceManagement/conference')
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facultyForm.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'CMS.settings'

application = get_wsgi_application()

