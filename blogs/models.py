from django.db import models

# Create your models here.
from accounts.models import UserModel

class blog(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/', null=True,blank=True)
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    post_date = models.DateTimeField(auto_now_add=True)