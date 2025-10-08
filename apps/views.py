from random import randint

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Car
from apps.serializers import CarModelSerializer, SendCodeSerializer, VerifyCodeSerializer
from apps.utils import send_code


class CarModelApi(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer

class SendCodeApiView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args,**kwargs):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        code = randint(100_000,999_999)
        send_code(phone,code)
        return Response({'message':"sms code sent"},status.HTTP_200_OK)

class VerifyCodeApiView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self,request, *args,**kwargs):
        serializer = VerifyCodeSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())
