from django.db import models

# Create your models here.
RATING = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Car(models.Model):
    car_make = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, choices=RATING)
