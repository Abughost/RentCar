from django.urls import path

from apps.views import CarListCreateAPIView, SendCodeAPIView, VerifyCodeAPIView, RetrieveUpdateDestroyAPIView, \
    CarBrandListAPIView, CarBrandRetrieveAPIView, CarTypeListAPIView, CarTypeRetrieveAPIView

urlpatterns = [
    path('auth/send_code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify_code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('v1/car', CarListCreateAPIView.as_view(), name='car_model'),
    path('v1/car/<int:uuid>',RetrieveUpdateDestroyAPIView.as_view(), name='car_detail'),
    path('v1/car_brand',CarBrandListAPIView.as_view(), name='car_detail'),
    path('v1/car_brand/<int:uuid>',CarBrandRetrieveAPIView.as_view(),name='car_brand_detail'),
    path('v1/car_category',CarTypeListAPIView.as_view()),
    path('v1/car_category/<int:uuid>',CarTypeRetrieveAPIView.as_view()),

]