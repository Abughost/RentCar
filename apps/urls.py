from django.urls import path

from apps.views import CarListCreateAPIView, SendCodeAPIView, VerifyCodeAPIView, RetrieveUpdateDestroyAPIView, \
    CarBrandListAPIView, CarBrandRetrieveAPIView, CarTypeListAPIView, CarTypeRetrieveAPIView

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('car', CarListCreateAPIView.as_view(), name='car_model'),
    path('car/<uuid:uuid>',RetrieveUpdateDestroyAPIView.as_view(), name='car_detail'),
    path('car/brand',CarBrandListAPIView.as_view(), name='car_detail'),
    path('car/brand/<uuid:uuid>',CarBrandRetrieveAPIView.as_view(),name='car_brand_detail'),
    path('car/category',CarTypeListAPIView.as_view()),
    path('car/category/<uuid:uuid>',CarTypeRetrieveAPIView.as_view()),

]
