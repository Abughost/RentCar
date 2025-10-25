from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.filters import CarPriceFilter
from apps.models import Car, CarBrand, CarCategory
from apps.models.base import IsAdminOrReadOnly
from apps.paginations import CustomCursorPagination
from apps.serializers import (CarBrandModelSerializer,
                              CarCategoryModelSerializer,
                              CarDetailModelSerializer, CarModelSerializer,
                              RentModelSerializer, SendCodeSerializer,
                              VerifiedUserModelSerializer,
                              VerifyCodeSerializer)
from apps.utils import send_code


@extend_schema(tags=['Cars'])
class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarPriceFilter
    search_fields = 'brand_name', 'model'
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]


    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


@extend_schema(tags=['Cars'])
class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

@extend_schema(tags=['Car Brand & Category'])
class CarBrandListCreateAPIView(ListCreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

@extend_schema(tags=['Car Brand & Category'])
class CarBrandRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

@extend_schema(tags=['Car Brand & Category'])
class CarTypeListCreateAPIView(ListCreateAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategoryModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

@extend_schema(tags=['Car Brand & Category'])
class CarCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategoryModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

class UserCreateAPIView(CreateAPIView):
    serializer_class = VerifiedUserModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Rental'])
class RentCarCreateApiView(CreateAPIView):
    serializer_class = RentModelSerializer

@extend_schema(tags=['Rental'])
class RentCarRetrieveAPIView(RetrieveAPIView):
    serializer_class = RentModelSerializer


class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        code = randint(100_000, 999_999)
        valid, _ttl = send_code(phone, code)
        if valid:
            return Response({'message': "sms code sent"})
        return Response({'message':f'You have {_ttl} seconds left'})

class VerifyCodeAPIView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())
