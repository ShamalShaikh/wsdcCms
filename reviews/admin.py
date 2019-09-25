from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Reviewer)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Remarks)
admin.site.register(AssignedPaperStatus)