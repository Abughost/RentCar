from django.urls import path

from apps.views import (CarBrandListCreateAPIView,
                        CarBrandUpdateDestroyAPIView,
                        CarCategoryRetrieveUpdateDestroyAPIView,
                        CarListCreateAPIView, CarRetrieveUpdateDestroyAPIView,
                        CarTypeListCreateAPIView, LoginAPIView,
                        RentCarCreateApiView, RentCarRetrieveAPIView,
                        SendCodeAPIView, UserCreateAPIView, VerifyCodeAPIView)

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('auth/login',LoginAPIView.as_view(),name='login'),
    path('user/register',UserCreateAPIView.as_view(),name='user_profile'),
    path('cars', CarListCreateAPIView.as_view(), name='car_model'),
    path('cars/<uuid:id>', CarRetrieveUpdateDestroyAPIView.as_view(),name='car_detail'),
    path('cars/brand', CarBrandListCreateAPIView.as_view(), name='car_detail'),
    path('cars/brand/<uuid:pk>', CarBrandUpdateDestroyAPIView.as_view(), name='car_brand_detail'),
    path('cars/category', CarTypeListCreateAPIView.as_view(), name='car_category'),
    path('cars/category/<uuid:pk>', CarCategoryRetrieveUpdateDestroyAPIView.as_view(), name='car_category_detail'),
    path('rents/car' , RentCarCreateApiView.as_view(), name='rent_car'),
    path('user/rentals/<uuid:pk>', RentCarRetrieveAPIView.as_view(),name='rent_user_cars'),

]