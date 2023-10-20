from .models import Hotel, Rating
from .serializers import HotelSerializer, RatingSerializer
from rest_framework import viewsets

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)