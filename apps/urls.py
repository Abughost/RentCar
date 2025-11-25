from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.views import (CarBrandListCreateAPIView,
                        CarBrandUpdateDestroyAPIView,
                        CarCategoryRetrieveUpdateDestroyAPIView,
                        CarModelViewSet, CarTypeListCreateAPIView,
                        CheckUserLogin, LoginAPIView, NewsModelViewSet,
                        RentCarHistoryListAPIView, RentCarListCreateApiView,
                        RentCarRetrieveDestroyAPIView, SendCodeAPIView,
                        UserProfileCreateAPIView, VerifyCodeAPIView)

router = DefaultRouter(trailing_slash=False)
router.register('news', NewsModelViewSet, basename='news')
router.register('cars', CarModelViewSet, basename='cars')

urlpatterns = [

    # auth
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login', LoginAPIView.as_view(), name='login'),
    path('auth/user/status', CheckUserLogin.as_view(), name='checking'),
    path('auth/register', UserProfileCreateAPIView.as_view(), name='user_profile'),
    path('user/rentals', RentCarListCreateApiView.as_view(), name='rent_car'),
    path('user/rentals/<uuid:pk>', RentCarRetrieveDestroyAPIView.as_view(), name='rent_user_cars'),
    path('cars/brand', CarBrandListCreateAPIView.as_view(), name='car_detail'),
    path('cars/brand/<str:name>', CarBrandUpdateDestroyAPIView.as_view(), name='car_brand_detail'),
    path('cars/category', CarTypeListCreateAPIView.as_view(), name='car_category'),
    path('cars/category/<str:name>', CarCategoryRetrieveUpdateDestroyAPIView.as_view(), name='car_category_detail'),
    path('rentals/history', RentCarHistoryListAPIView.as_view(), name='rents_history'),

    path('', include(router.urls)),
]
