from django.contrib import admin

# Register your models here.
from .models import User, Conference, Page, Paper


admin.site.register(User)
admin.site.register(Conference)
admin.site.register(Page)
admin.site.register(Paper)
