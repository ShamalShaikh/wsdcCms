import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMS.settings')

import django
django.setup()

from conference.models import *
import datetime

def addConference(name,alias,max_papers):
	c = Conference()
	c.conference_name = name
	c.conference_alias = alias
	c.startDate = datetime.datetime.now()
	c.endDate = datetime.datetime.now()
	c.description = "Defau"