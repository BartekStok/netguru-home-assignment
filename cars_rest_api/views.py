from collections import defaultdict

from botocore.exceptions import ClientError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import typing as t

from .forms import CreateBucketForm, SaveToBucketForm
from .models import Car
from .s3 import S3
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
        serializer = CarSerializer(cars, many=True, context={"request": request})
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
            response = {"Message": "Please provide car_make and model_name"}
            return Response(response, status=422)

        # Call methods from services.py
        make_models = get_cars(serializer.data["car_make"])
        model_name = get_model_name(make_models, serializer.data["model_name"])

        # Returns proper message if data does not exists in external source
        if make_models["Count"] == 0:
            response = {"Message": "Make does not exists"}
            return Response(response, status=404)
        if not model_name:
            response = {"Message": "Model does not exists"}
            return Response(response, status=404)

        car_make = make_models["Results"][0]["Make_Name"]

        # Checks for existence in local DB, if no saves it to DB
        try:
            car = Car.objects.filter(car_make=car_make).get(model_name=model_name)
            response = {"Message": "Model already in Data Base"}
            return Response(response, status=200)
        except ObjectDoesNotExist:
            car = Car.objects.create(car_make=car_make, model_name=model_name)
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
            response = {"Message": "Please provide car_make and model_name"}
            return Response(response, status=422)

        car_make = serializer.data["car_make"]
        model_name = serializer.data["model_name"]

        # Check if car exists in DB
        try:
            car = Car.objects.filter(car_make=car_make).get(model_name=model_name)
        except ObjectDoesNotExist:
            response = {"Message": "Car does not exists in DB"}
            return Response(response, status=404)

        # Check if rating is in request
        if "rating" not in request.data:
            response = {"Message": "Please provide rating for a car"}
            return Response(response, status=422)

        # Validate and save rating to DB
        data = {"rating": request.data["rating"], "car": car.id}
        rating_serializer = RatingSerializer(data=data)
        if rating_serializer.is_valid():
            rating_serializer.save()
            response = {"Message": "Rating added"}
            return Response(response, status=201)

        # Returns error when rating not correct
        response = {"Message": "Rating must be 1 to 5"}
        return Response(response, status=422)


class PopularView(APIView):
    """
    Class shows popular cars, based on rating count :model: Car
    :methods: GET
    """

    def get(self, request):
        """Shows most popular car"""
        cars = Car.objects.all().annotate(rate_count=Count("rating")).order_by("-rate_count")
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status=200)


class WelcomeView(View):
    """Shows welcome view"""

    def get(self, request):
        return render(request, "welcome.html")


class S3BucketView(View):
    """Test view for s3"""

    s3_client = S3.s3_client
    s3_resource = S3.s3_resource

    @staticmethod
    def _get_form(request: t.Type[Request], form_class: t.Type[Form], prefix: str):
        data = request.POST if prefix in request.POST else None
        files = request.FILES
        return form_class(data=data, files=files, prefix=prefix)

    def get(self, request):
        create_bucket_form = CreateBucketForm(prefix="create_bucket_form")
        save_to_bucket_form = SaveToBucketForm(prefix="save_to_bucket_form")
        buckets = S3.get_buckets_name()

        buckets_content: t.Dict[str, list] = defaultdict(list)
        for bucket in buckets:
            for obj in self.s3_resource.Bucket(name=bucket).objects.all():
                buckets_content[bucket].append(obj.key)
        buckets_content.default_factory = None

        context = {
            "create_bucket_form": create_bucket_form,
            "save_to_bucket_form": save_to_bucket_form,
            "buckets": buckets,
            "buckets_content": buckets_content,
        }
        return render(request, "s3-test.html", context)

    def post(self, request):
        create_bucket_form = self._get_form(request, CreateBucketForm, "create_bucket_form")
        save_to_bucket_form = self._get_form(request, SaveToBucketForm, "save_to_bucket_form")
        buckets = S3.get_buckets_name()

        if create_bucket_form.is_bound and create_bucket_form.is_valid():
            bucket_prefix = create_bucket_form.cleaned_data.get("bucket_name")
            bucket_name, response = S3.create_bucket(bucket_prefix=bucket_prefix, s3_connection=self.s3_client)
            return HttpResponse(f"{bucket_name} ----- {response}")
        elif save_to_bucket_form.is_bound and save_to_bucket_form.is_valid():
            bucket_name = save_to_bucket_form.cleaned_data.get("bucket_name")
            file = save_to_bucket_form.cleaned_data.get("file")

            buckets = S3.get_buckets_name()
            if bucket_name not in buckets:
                return HttpResponse("Given bucket does not exists!")

            bucket = self.s3_resource.Bucket(name=bucket_name)
            try:
                bucket.upload_fileobj(file.file, file.name)
            except ClientError as e:
                print(e)
                return False

            return HttpResponse(f"{bucket_name} ----- {file}")

        context = {
            "create_bucket_form": create_bucket_form,
            "save_to_bucket_form": save_to_bucket_form,
            "buckets": buckets,
        }
        return render(request, "s3-test.html", context)
