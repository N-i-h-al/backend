from rest_framework import serializers
from .models import RestaurantModel, FoodItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantModel
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'