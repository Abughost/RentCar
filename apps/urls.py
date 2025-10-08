from django.urls import path

from apps.views import CarModelApi, SendCodeApiView, VerifyCodeApiView

urlpatterns = [
    path('auth/send_code',SendCodeApiView.as_view(),name='send_code'),
    path('auth/verify_code',VerifyCodeApiView.as_view(),name='cerify_code'),
    path('v1/car', CarModelApi.as_view(), name='car=model'),

]