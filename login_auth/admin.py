from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Registered_Conference)
admin.site.register(Payment)
admin.site.register(Rejected_payment)