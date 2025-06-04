from django.urls import path
from api.auth.views import RegisterAPI, LoginAPI, RefreshAPI, LogoutAPI

urlpatterns = [
    path("auth/register/", RegisterAPI.as_view(), name="register"),
    path("auth/login/", LoginAPI.as_view(), name="login"),
    path("auth/refresh/", RefreshAPI.as_view(), name="refresh"),
    path("auth/logout/", LogoutAPI.as_view(), name="logout"),
]