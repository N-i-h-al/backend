from rest_framework import serializers
from .models import  Hotel, Rating
from django.db import models


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["hotels", "description","rating"]