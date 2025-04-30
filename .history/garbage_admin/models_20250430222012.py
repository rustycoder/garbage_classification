from django.db import models
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    address =  models.CharField(max_length=100)
    city =  models.CharField(max_length=50)
    state =  models.CharField(max_length=50)
    zipcode =  models.CharField(max_length=20)
    tokens = models.IntegerField(default=0)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return("User Profile")    
    

class TokenTransaction(models.Model):

    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='token_transactions')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES, default='debit')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.user.username} - {self.transaction_type} {self.amount} credits on {self.transaction_date.strftime('%Y-%m-%d %H:%M:%S')}"
        return "Token Transaction"


class ProfileAdmin(ModelAdmin):
    list_display = ('created_at', 'otp', 'phone', 'address', 'city', 'state', 'zipcode', 'tokens', 'user_id')

class TokenTransactionAdmin(ModelAdmin):
    list_display = ('user_id', 'amount', 'transaction_type', 'transaction_date')

