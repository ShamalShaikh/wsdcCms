
COURSEMAP_COURSES = {
    'Biotechnology':'BioTech',
    'Civil Engineering':'CE',
    'Chemical Engineering':'CHE',
    'Chemistry':'CY',
    'Computer Science & Engineering':'CSE', 
    'Electronics & communication Engineering':'ECE',
    'Electrical Engineering':'EEE',
    'Mathematics':'MAT',
    'Mechanical Engineering':'ME' ,
    'Metallurgical & Materials Engineering':'MME',
    'Physics':'PHY',
    'Physical Education':'PE',
    'Humanities & Social Science': 'HSS',
    'School of Management':'SM',
}


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CMS.settings')

import django
django.setup()

from conference.models import *

print "Adding courses"
for course,course_alias in COURSEMAP_COURSES.items():
    b = Branch()
    b.branch_name = course
    b.branch_alias = course_alias
    b.save()
print "Adding other"
b = Branch()
b.branch_name = "Other"
b.branch_name = "Other"
b.save()
print "assigning other to all"
for c in Conference.objects.all():
    c.branch = b