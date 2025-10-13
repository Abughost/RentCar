from django.urls import path

from apps.views import CarListCreateAPIView, SendCodeAPIView, VerifyCodeAPIView, CarBrandListCreateAPIView

urlpatterns = [
    path('auth/send_code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify_code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('v1/car', CarListCreateAPIView.as_view(), name='car_model'),
    path('v1/car_brand',CarBrandListCreateAPIView.as_view(),name='car_brand')

]