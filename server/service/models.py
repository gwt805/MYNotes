from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.BigIntegerField(unique=True, null=False)
    name = models.CharField(max_length=255, null=False)
    avatar_url = models.CharField(max_length=1024, null=False)
    email = models.EmailField(null=True, unique=True)
    access_token = models.CharField(max_length=32, null=False)
    refresh_token = models.CharField(max_length=64, null=False)
    created_at = models.IntegerField(null=False)
    expires_in = models.IntegerField(null=False)

    class Meta:
        db_table = "user"

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, null=False)
    article = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "notes"