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
    """
    Stores a single car entry
    """
    car_make = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)

    def get_rate_count(self):
        return self.rating_set.all().count()


class Rating(models.Model):
    """
    Stores rating for a car, foreign key to :Car:
    """
    rating = models.IntegerField(choices=RATING)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
