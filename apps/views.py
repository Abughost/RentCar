from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.filters import CarPriceFilter
from apps.models import Car, CarBrand
from apps.serializers import CarModelSerializer, SendCodeSerializer, VerifyCodeSerializer, CarBrandSerializer
from apps.utils import send_code


class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = CarPriceFilter
    search_fields = 'model',

    def get_queryset(self):
        return super().get_queryset().filter(Car.is_available)

class CarBrandListCreateAPIView(ListCreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    search_fields = 'name',



class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args,**kwargs):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        code = randint(100_000,999_999)
        send_code(phone,code)
        return Response({'message':"sms code sent"},status.HTTP_200_OK)

class VerifyCodeAPIView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self,request, *args,**kwargs):
        serializer = VerifyCodeSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())
