from django.contrib import admin
from .models import Profile, ProfileAdmin
from .models import TokenTransaction

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.registerTokenTransaction)