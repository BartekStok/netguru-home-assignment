import random

import pytest
from django.db.models import Count
from django.urls import reverse
from rest_framework import status

from cars_rest_api.models import Car


@pytest.mark.django_db
def test_get_cars(api_client):
    url = reverse("cars")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    "car_make, model_name, status_code",
    [
        ("wrong_mark", "wrong_model", status.HTTP_404_NOT_FOUND),
        ("Honda", "wrong_model", status.HTTP_404_NOT_FOUND),
        ("wrong_mark", "Civic", status.HTTP_404_NOT_FOUND),
        ("Honda", "Civic", status.HTTP_201_CREATED),
    ],
)
def test_post_cars(api_client, car_make, model_name, status_code):
    url = reverse("cars")
    data = {"car_make": car_make, "model_name": model_name}
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_post_cars_without_required_mark(api_client):
    url = reverse("cars")
    data = {"model_name": "Civic"}
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_post_cars_without_required_model(api_client):
    url = reverse("cars")
    data = {"car_make": "Honda"}
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_post_cars_when_object_already_in_db(api_client):
    Car.objects.create(car_make="HONDA", model_name="Civic")
    url = reverse("cars")
    data = {"car_make": "Honda", "model_name": "Civic"}
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    "car_make, model_name, rating, status_code",
    [
        ("HONDA", "Pilot", 5, status.HTTP_201_CREATED),
        ("HONDA", "Civic", 4, status.HTTP_201_CREATED),
    ],
)
def test_post_rate(api_client, set_up_cars, car_make, model_name, rating, status_code):
    url = reverse("rate")
    data = {"car_make": car_make, "model_name": model_name, "rating": rating}
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "car_make, model_name, rating, status_code",
    [
        ("HONDA", "Pilot", "str", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("HONDA", "Civic", 8, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("wrong_make", "Civic", 5, status.HTTP_404_NOT_FOUND),
        ("HONDA", "wrong_model", 5, status.HTTP_404_NOT_FOUND),
    ],
)
def test_post_rate_with_wrong_data(api_client, set_up_cars, car_make, model_name, rating, status_code):
    url = reverse("rate")
    data = {"car_make": car_make, "model_name": model_name, "rating": rating}
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_post_rate_without_car_make(api_client, set_up_cars):
    url = reverse("rate")
    data = {"model_name": "Civic", "rating": 5}
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_post_rate_without_model_name(api_client, set_up_cars):
    url = reverse("rate")
    data = {"car_make": "HONDA", "rating": 5}
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_post_rate_without_rating(api_client, set_up_cars):
    url = reverse("rate")
    data = {"car_make": "HONDA", "model_name": "Civic"}
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_get_popular(api_client, set_up_cars):
    url = reverse("popular")
    cars = Car.objects.all()
    for _ in range(50):
        car = random.choice(cars)
        car.rating_set.create(rating=random.randint(1, 5))
    cars = Car.objects.all().annotate(rate_count=Count("rating")).order_by("-rate_count")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["id"] == cars[0].id
