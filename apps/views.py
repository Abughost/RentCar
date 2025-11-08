from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, ListAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.filters import CarPriceFilter
from apps.models import Car, CarBrand, CarCategory, UserProfile, Rental
from apps.models.base import IsAdminOrReadOnly, IsRegisteredUser
from apps.models.news import New
from apps.paginations import CustomCursorPagination
from apps.serializers import (CarBrandModelSerializer,
                              CarCategoryModelSerializer, CarModelSerializer,
                              LoginSerializer, RentModelSerializer,
                              SendCodeSerializer, VerifiedUserModelSerializer,
                              VerifyCodeSerializer, NewsModelSerializer)
from apps.utils import send_code


@extend_schema(tags=['Cars'])
class CarModelViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarPriceFilter
    search_fields = 'brand_name', 'model'
    permission_classes = [IsAdminOrReadOnly,]
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


@extend_schema(tags=['Car Brand & Categories'])
class CarBrandListCreateAPIView(ListCreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

@extend_schema(tags=['Car Brand & Categories'])
class CarBrandUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]
    lookup_field = 'name'

@extend_schema(tags=['Car Brand & Categories'])
class CarTypeListCreateAPIView(ListCreateAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategoryModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]

@extend_schema(tags=['Car Brand & Categories'])
class CarCategoryRetrieveUpdateDestroyAPIView(UpdateAPIView,DestroyAPIView):
    queryset = CarCategory.objects.all()
    serializer_class = CarCategoryModelSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]
    lookup_field = 'name'

class UserProfileCreateAPIView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = VerifiedUserModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Rentals'])
class RentCarListCreateApiView(ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentModelSerializer
    permission_classes = [IsRegisteredUser]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return ValidationError({"detail":"UserProfile is missing. Please complete profile first."})

        serializer.save(user=profile)


@extend_schema(tags=['Rentals'])
class RentCarRetrieveDestroyAPIView(RetrieveAPIView, DestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentModelSerializer
    permission_classes = [IsRegisteredUser,IsAdminOrReadOnly]

@extend_schema(tags=['Rentals'])
class RentCarHistoryListAPIView(ListAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentModelSerializer
    permission_classes = [IsRegisteredUser, IsAdminOrReadOnly]


@extend_schema(tags=['News'])
class NewsListCreateAPIView(ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewsModelSerializer
    permission_classes = [IsAdminOrReadOnly]
@extend_schema(tags=['News'])
class NewsModelViewSet(ModelViewSet):
    queryset = New.objects.all()
    serializer_class = NewsModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data | serializer.validated_data['contact']


        valid, _ttl = send_code(data)
        if valid:
            return Response({'message': "sms code sent"})
        return Response({'message':f'You have {_ttl} seconds left'})

class VerifyCodeAPIView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_data = serializer.validated_data

        return Response({"message":"successfully registered","data":validate_data}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.get_data())


class LogoutAPIView(APIView):
    def post(self,request):
        logout(self.request)
        return Response({'message':'User logged out successfully'})

class CheckUserLogin(APIView):
    def get(self,request):
        if self.request.user.is_authenticated:
            return Response({'login': True})
        return Response({'Logout':False})
