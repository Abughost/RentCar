from django.urls import path

from apps.views import CarListAPIView, SendCodeAPIView, VerifyCodeAPIView, \
    CarBrandListAPIView, CarTypeListAPIView, CarRetrieveAPIView, UserCreateAPIView, RentCarCreateApiView

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('auth/verify-user',UserCreateAPIView.as_view(),name='user_profile'),
    path('cars', CarListAPIView.as_view(), name='car_model'),
    path('cars/<uuid:pk>', CarRetrieveAPIView.as_view(), name='car_detail'),
    path('cars/brand',CarBrandListAPIView.as_view(), name='car_detail'),
    path('cars/category',CarTypeListAPIView.as_view(), name='car_category'),
    path('rents/car' , RentCarCreateApiView.as_view(), name='rent_car')

]