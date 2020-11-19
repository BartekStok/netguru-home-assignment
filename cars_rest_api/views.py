from django.core.exceptions import ObjectDoesNotExist
from .models import Car
from .serializers import CarSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_cars, get_model_name


class CarView(APIView):
    """
    Class displays json responses from :model: Car
    :methods: GET, POST
    """
    def get(self, request):
        """Displays all cars in DB"""
        cars = Car.objects.all()
        serializer = CarSerializer(cars,
                                   many=True,
                                   context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        """
        Post Method validates requested data trough serializer,
        if valid calls method from services to fetch requested data
        from external API https://vpic.nhtsa.dot.gov/api/.
        Then processes data, if valid saves to DB, if no returns
        response with proper message
        """
        serializer = CarSerializer(data=request.data)

        if not serializer.is_valid():
            response = {'Message': 'Please provide car_make and model_name'}
            return Response(response, status=422)

        # Call methods from services.py
        make_models = get_cars(serializer.data['car_make'])
        model_name = get_model_name(make_models, serializer.data['model_name'])

        # Returns proper message if data does not exists in external source
        if make_models['Count'] == 0:
            response = {'Message': 'Make does not exists'}
            return Response(response, status=404)
        if not model_name:
            response = {'Message': 'Model does not exists'}
            return Response(response, status=404)

        car_make = serializer.data['car_make']

        # Checks for existence in local DB, if no saves it to DB
        try:
            car = (Car.objects
                   .filter(car_make=car_make)
                   .get(model_name=model_name))
            response = {'Message': 'Model already in Data Base'}
            return Response(response, status=200)
        except ObjectDoesNotExist:
            car = (Car.objects.create(
                    car_make=car_make,
                    model_name=model_name))
            serializer = CarSerializer(instance=car)
            return Response(serializer.data, status=201)


class RatingView(APIView):
    """
    Class adds rating for model :model: Car
    :methods: POST
    """
    def post(self, request):
        """Updates rating for specific car"""
        serializer = CarSerializer(data=request.data)

        if not serializer.is_valid():
            response = {'Message': 'Please provide car_make and model_name'}
            return Response(response, status=422)

        car_make = serializer.data['car_make']
        model_name = serializer.data['model_name']

        try:
            car = (Car.objects
                   .filter(car_make=car_make)
                   .get(model_name=model_name))
        except ObjectDoesNotExist:
            response = {'Message': 'Car does not exists in DB'}
            return Response(response, status=404)

        if not hasattr(request, 'rating'):
            response = {'Message': 'Please provide rating for a car'}
            return Response(response, status=422)




class PopularView(APIView):

    def get(self, request):
        pass


import json
class Tests(APIView):

    def get(self, request, car_make):
        with open('cars_rest_api/honda.json') as f:
            data = json.load(f)
            return Response(data, status=200)
