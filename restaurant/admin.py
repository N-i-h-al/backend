from django.contrib import admin
from .models import RestaurantModel, FoodItem
# Register your models here.
admin.site.register(RestaurantModel)
admin.site.register(FoodItem)