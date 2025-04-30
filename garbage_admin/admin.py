from django.contrib import admin
from .models import Profile, ProfileAdmin
from .models import TokenTransaction, TokenTransactionAdmin

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TokenTransaction, TokenTransactionAdmin)