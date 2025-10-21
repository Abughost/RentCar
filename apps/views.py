from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.filters import CarPriceFilter
from apps.models import Car, CarBrand, CarCategory, Rental
from apps.serializers import CarModelSerializer, SendCodeSerializer, VerifyCodeSerializer, CarBrandModelSerializer, \
    CarCategoryModelSerializer, CarDetailModelSerializer, VerifiedUserModelSerializer, RentModelSerializer
from apps.utils import send_code


@extend_schema(tags=['Cars'])
class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarPriceFilter
    search_fields = 'brand_name', 'model'

    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


@extend_schema(tags=['Cars'])
class CarRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDetailModelSerializer

    # def put(self, request, pk):
    #     try:
    #         car = Car.objects.filter(id=pk).first()
    #     except Car.DoesNotExist:
    #         return Response({"Detail": 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    #
    #     serializer = CarModelSerializer(car, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Car Brand & Category'])
class CarBrandListAPIView(ListCreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandModelSerializer


@extend_schema(tags=['Car Brand & Category'])
class CarTypeListAPIView(ListAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategoryModelSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = VerifiedUserModelSerializer
    permission_classes = [IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Rental'])
class RentCarCreateApiView(CreateAPIView):
    serializer_class = RentModelSerializer

    # def post(self, request, *args, **kwargs):
    #     user = getattr(request.user, 'userprofile', None)
    #
    #
    #     if not user:
    #         return Response({'message': 'User Not found, Register first'}, status.HTTP_404_NOT_FOUND)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        code = randint(100_000, 999_999)
        send_code(phone, code)
        return Response({'message': "sms code sent"})


class VerifyCodeAPIView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())
