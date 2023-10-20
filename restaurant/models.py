from django.db import models

# Create your models here.
from accounts.models import UserModel
class RestaurantModel(models.Model):
    restaurant = models.CharField(max_length=50)
    res_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/restaurant', null=True,blank=True)
    location = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    post_date = models.DateTimeField(auto_now_add=True)
    open_at = models.TimeField(auto_now_add=False)
    close_at = models.TimeField(auto_now_add=False)

    def __str__(self):
        return self.restaurant

class FoodItem(models.Model):
    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    price = models.CharField(max_length=60)
    image = models.ImageField(upload_to='media/items', null=True,blank=True)
    description = models.TextField(max_length=255)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.title