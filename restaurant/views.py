from .models import RestaurantModel, FoodItem
from .serializers import RestaurantSerializer,FoodItemSerializer
from rest_framework import viewsets

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RestaurantModel.objects.all()
    serializer_class = RestaurantSerializer

class FoodItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
