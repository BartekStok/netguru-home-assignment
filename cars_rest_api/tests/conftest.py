import pytest

from cars_rest_api.models import Car
from cars_rest_api.tests.utils import get_cars_list


@pytest.fixture
def api_client():
    """Return API client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def set_up_cars():
    """Returns list of car objects and saves in mark DB"""
    data = []
    for car in get_cars_list():
        obj = Car.objects.create(car_make=car['Make_Name'],
                                 model_name=car['Model_Name'])
        data.append(obj)
    return data
