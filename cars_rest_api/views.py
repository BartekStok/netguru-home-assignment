from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from .models import Car
from .serializers import CarSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .services import get_cars, get_model_name


# Create your views here.


class CarView(APIView):

    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars,
                                   many=True,
                                   context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)

        if not serializer.is_valid():
            response = {'Message': 'Please provide car_make and model_name'}
            return JsonResponse(response, status=422)

        make_models = get_cars(serializer.data['car_make'])
        model_name = get_model_name(make_models, serializer.data['model_name'])

        if make_models['Count'] == 0:
            response = {'Message': 'Make does not exists'}
            return JsonResponse(response, status=404)
        if not model_name:
            response = {'Message': 'Model does not exists'}
            return JsonResponse(response, status=404)

        car_make = serializer.data['car_make']

        try:
            car = (Car.objects
                   .filter(car_make=car_make)
                   .get(model_name=model_name))
        except ObjectDoesNotExist:
            car = Car.objects.create(
                    car_make=serializer.data['car_make'],
                    model_name=model_name)

        serializer = CarSerializer(data=car)
        if serializer.is_valid():
            return JsonResponse(serializer.data, status=200)


class RatingView(APIView):

    def post(self, request):
        pass


class PopularView(APIView):

    def get(self, request):
        pass
