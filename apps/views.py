from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.filters import CarPriceFilter
from apps.models import Car, CarBrand, CarCategory
from apps.serializers import CarModelSerializer, SendCodeSerializer, VerifyCodeSerializer, CarBrandSerializer, \
    CarTypeSerializer
from apps.utils import send_code


@extend_schema(tags=['Cars'])
class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarPriceFilter
    search_fields = 'model',

    def get_queryset(self):
        return super().get_queryset().filter(Car.is_available)


@extend_schema(tags=['Cars'])
class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer


@extend_schema(tags=['Car Brand & Category'])
class CarBrandListAPIView(ListAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


@extend_schema(tags=['Car Brand & Category'])
class CarBrandRetrieveAPIView(RetrieveAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


@extend_schema(tags=['Car Brand & Category'])
class CarTypeListAPIView(ListAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarTypeSerializer


@extend_schema(tags=['Car Brand & Category'])
class CarTypeRetrieveAPIView(RetrieveAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarTypeSerializer


class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        code = randint(100_000, 999_999)
        send_code(phone, code)
        return Response({'message': "sms code sent"}, status.HTTP_200_OK)


class VerifyCodeAPIView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())
