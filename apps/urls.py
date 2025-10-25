from django.urls import path

from apps.views import (CarBrandListCreateAPIView,
                        CarCategoryRetrieveUpdateDestroyAPIView,
                        CarListCreateAPIView, CarTypeListCreateAPIView,
                        RentCarCreateApiView, SendCodeAPIView,
                        UserCreateAPIView, VerifyCodeAPIView, RentCarRetrieveAPIView, CarRetrieveUpdateDestroyAPIView,
                        CarBrandRetrieveUpdateDestroyAPIView)

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('auth/verify-user',UserCreateAPIView.as_view(),name='user_profile'),
    path('cars', CarListCreateAPIView.as_view(), name='car_model'),
    path('cars/<uuid:id>', CarRetrieveUpdateDestroyAPIView.as_view(),name='car_detail'),
    path('cars/brand', CarBrandListCreateAPIView.as_view(), name='car_detail'),
    path('cars/brand/<uuid:pk>', CarBrandRetrieveUpdateDestroyAPIView.as_view(), name='car_brand_detail'),
    path('cars/category', CarTypeListCreateAPIView.as_view(), name='car_category'),
    path('cars/category/<uuid:pk>', CarCategoryRetrieveUpdateDestroyAPIView.as_view(), name='car_category_detail'),
    path('rents/car' , RentCarCreateApiView.as_view(), name='rent_car'),
    path('user/rentals/<uuid:pk>', RentCarRetrieveAPIView.as_view(),name='rent_user_cars'),

]