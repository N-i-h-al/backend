from django.db import models
from django.utils.text import slugify
from accounts.models import UserModel

# Create your models here.

class Hotel(models.Model):
    hotel_name = models.CharField(max_length= 100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length= 500, blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to = 'media/hotels', null=True, blank=True, default="")
    top_deal = models.BooleanField(default=False)
    location = models.CharField(max_length=100, default='YourDefaultLocation')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.hotel_name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.hotel_name

class Rating(models.Model):
    hotels = models.ForeignKey(Hotel, on_delete= models.CASCADE, related_name="rating")        
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(choices=(
                                                    (1,"1 Star"),
                                                    (2,"2 Star"),
                                                    (3,"3 Star"),
                                                    (4,"4 Star"),
                                                    (5,"5 Star") 
                                                  ))
    rating_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} rating: {self.rating} hotels: {self.hotels}"
    
    class Meta:
        unique_together = ('hotels', 'user')