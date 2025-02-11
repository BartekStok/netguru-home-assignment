import requests

API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/"
# API_URL = 'http://localhost:8000/api/tests/'


def get_cars(car_make):
    """Fetch data from external resource"""
    url = API_URL + car_make
    params = {"format": "json"}
    r = requests.get(url, params=params)
    cars = r.json()
    return cars


def get_model_name(make_models, model_name):
    """Checks if given model exists in external source"""
    if make_models["Count"] > 0:
        for make in make_models["Results"]:
            if make["Model_Name"] == model_name:
                return make["Model_Name"]
    return False
