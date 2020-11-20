from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car
from .serializers import CarSerializer, RatingSerializer
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
        if valid calls method from services.py to fetch requested data
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

        car_make = make_models['Results'][0]['Make_Name']

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
    Class adds rating for model :model: Rating
    :methods: POST
    """
    def post(self, request):
        """Adds rating for specific car"""
        serializer = CarSerializer(data=request.data)

        # Validate data
        if not serializer.is_valid():
            response = {'Message': 'Please provide car_make and model_name'}
            return Response(response, status=422)

        car_make = serializer.data['car_make']
        model_name = serializer.data['model_name']

        # Check if car exists in DB
        try:
            car = (Car.objects
                   .filter(car_make=car_make)
                   .get(model_name=model_name))
        except ObjectDoesNotExist:
            response = {'Message': 'Car does not exists in DB'}
            return Response(response, status=404)

        # Check if rating is in request
        if 'rating' not in request.data:
            response = {'Message': 'Please provide rating for a car'}
            return Response(response, status=422)

        # Validate and save rating to DB
        data = {'rating': request.data['rating'], 'car': car.id}
        rating_serializer = RatingSerializer(data=data)
        if rating_serializer.is_valid():
            rating_serializer.save()
            response = {'Message': 'Rating added'}
            return Response(response, status=201)

        # Returns error when rating not correct
        response = {'Message': 'Rating must be 1 to 5'}
        return Response(response, status=422)


class PopularView(APIView):
    """
    Class shows popular cars, based on rating count :model: Car
    :methods: GET
    """
    def get(self, request):
        """Shows most popular car"""
        cars = (Car.objects.all()
                .annotate(rate_count=Count('rating'))
                .order_by('-rate_count'))
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status=200)
