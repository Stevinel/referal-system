from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import generate_otp, profile, verify_otp

router = DefaultRouter()

urlpatterns = [
    path("v1/", include(router.urls)),
    path("otp/", generate_otp, name="generate_otp"),
    path("token/", verify_otp, name="token"),
    path("profile/", profile, name="profile"),
]
