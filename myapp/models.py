from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Spot(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WindCondition(models.Model):
    WIND_DIRECTIONS = [
        ('N', 'North'),
        ('NE', 'Northeast'),
        ('E', 'East'),
        ('SE', 'Southeast'),
        ('S', 'South'),
        ('SW', 'Southwest'),
        ('W', 'West'),
        ('NW', 'Northwest'),
    ]

    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='wind_conditions')
    date = models.DateField()
    wind_speed = models.DecimalField(max_digits=4, decimal_places=1)  # in knots
    wind_direction = models.CharField(max_length=2, choices=WIND_DIRECTIONS)
    temperature = models.DecimalField(max_digits=4, decimal_places=1)  # in Celsius
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.spot.name} - {self.date} - {self.wind_speed}kts"

class Review(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['spot', 'user']

    def __str__(self):
        return f"{self.spot.name} - {self.user.username} - {self.rating}★"

