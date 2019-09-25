from django.contrib import admin
from .models import *

class Conf_PaperAdmin(admin.ModelAdmin):
    search_fields=['paperRefNum']
    # list_filter=['paperRefNum']

# Register your models here.
admin.site.register(Conference)
admin.site.register(Conf_Image)
admin.site.register(Conf_Paper,Conf_PaperAdmin)
admin.site.register(Final_paper)
admin.site.register(Paper_Remark)
admin.site.register(Contest)
admin.site.register(Branch)

