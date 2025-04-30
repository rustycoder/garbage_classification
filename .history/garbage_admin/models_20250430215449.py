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
    credits = models.IntegerField(default=10000)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return("User Profile")    
    

class CreditTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_transactions')
    amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} credits on {self.transaction_date.strftime('%Y-%m-%d %H:%M:%S')}"

class ProfileAdmin(ModelAdmin):
    list_display = ('created_at', 'otp', 'phone', 'address', 'city', 'state', 'zipcode', 'user_id')

