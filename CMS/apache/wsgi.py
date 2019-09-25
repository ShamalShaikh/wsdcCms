#wsgi.py
import os, sys
# Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append(project)
sys.path.append("/var/www/html/venv/lib/python2.7/site-packages")

# Add the path to 3rd party django application and to django itself.
sys.path.append('/var/www/html/ConferenceManagement')
#print sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'CMS.apache.override'
os.environ['SECRET_KEY']='so6-chp4olmts+u0-+e4mi)i!3t#x285#vsyt_6!zsb54!fh44'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
